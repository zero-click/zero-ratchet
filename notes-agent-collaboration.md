# Agent协作效率分析：0512 Session根因重诊断

## 🎯 视角转换

**原有视角**: "自动化过度 → 需要人工介入"
**新视角**: "agent协作低效 → 需要改进协作机制"

## 🔍 从0512 Session看到的协作问题

### 问题1: Agent评审质量不稳定

**现象**:
```
第一轮评审 (planner+architect):
- 发现：权限矩阵缺失
- 未发现：事务原子性、审计查询、MCP契约

第二轮评审 (同样的agents):
- 发现：事务原子性、审计查询
- 未发现：retry策略、lease TTL细节

第三轮评审:
- 发现：retry、lease TTL
- 终于PASS
```

**根因**: Agent评审**缺乏一次性完整性检查机制**

**协作缺陷**:
- Planner和Architect之间**没有共享checklist**
- 每轮评审从零开始，**复用之前的发现**
- 没有"评审覆盖度"概念

### 问题2: Agent间上下文割裂

**现象**:
```python
# Gate 1.5: PRD Review
planner_review = {
    "issues": ["权限矩阵缺失"],
    "context": "只看了PRD"
}

# Gate 2.5: Design Review
architect_review = {
    "issues": ["事务原子性未定义"],
    "context": "只看了Design，不知道PRD review已经发现权限问题"
}

# 结果：同样的问题在不同gate重复发现
```

**根因**: **Agents之间没有累积式的共享上下文**

**协作缺陷**:
- 每个gate评审**独立启动agents**
- Agent间看不到彼此的**历史评审记录**
- 无法build on previous feedback

### 问题3: Agent协作协议缺失

**现象**:
```python
# Design Review时的agent行为
architect: "REQUEST_CHANGES - 事务原子性未定义"
assistant: "补上事务原子性设计"
architect: "REQUEST_CHANGES - 审计查询未定义"
assistant: "补上审计查询设计"
architect: "REQUEST_CHANGES - MCP契约未明确"
assistant: "补上MCP契约"

问题：为什么不一次性给出所有发现？
```

**根因**: **Agent没有"完整评审协议"**

**协作缺陷**:
- Agent评审**触达即停止**（发现一个问题就返回）
- 没有"必须检查X/Y/Z维度"的**强制协议**
- 没有"评审完整性自检"

### 问题4: Agent启动开销巨大

**现象**:
```
114个sessions × 平均加载5-10个skills = 每个任务重复初始化1000+次
```

**根因**: **没有持久的agent上下文**

**协作缺陷**:
- 每个gate都**重新创建agent实例**
- Agent的"记忆"在session间**丢失**
- 无法跨session复用agent的学习

### 问题5: Agent间决策分歧处理机制缺失

**现象**（hypothetical但可能发生）:
```python
planner: "这个feature应该先做X"
architect: "但从架构角度应该先做Y"
code-reviewer: "实现角度看Z更合理"

当前工作流: ? 没有明确的冲突解决机制
```

**根因**: **Multi-agent决策一致性机制缺失**

## 🎯 高效Agent协作的必要条件

### 1. 明确的角色契约

**当前状态**: 模糊
```markdown
- planner: "planning specialist" - 具体做什么？
- architect: "architecture review" - 评审什么维度？
- code-reviewer: "code quality review" - 哪些质量属性？
```

**应该有**:
```markdown
## Planner Agent契约
### 职责边界
- 负责: 需求拆解、任务依赖、优先级排序
- 不负责: 技术实现细节、API设计

### 交付物标准
- 必须包含: task breakdown、dependency graph、estimation
- 质量门槛: tasks must be independently completable

### 决策权限
- 可以独立决定: task优先级、拆解粒度
- 必须协同: 涉及架构变更时必须consult architect
```

### 2. 累积式共享上下文

**当前状态**: 每个gate独立评审
```
Gate 1.5 (PRD Review) → planner/architect看PRD → 输出review
Gate 2.5 (Design Review) → planner/architect看Design → 输出review
两个review互不知情
```

**应该有**: 持续累积的评审上下文
```
Shared Review Context:
{
  "prd_review": {
    "issues_found": ["权限矩阵", "user scope"],
    "agent": "planner+architect",
    "timestamp": "2026-05-12 09:00"
  },
  "design_review": {
    "issues_found": ["事务原子性"],
    "builds_on": "prd_review.issues_found",
    "agent": "architect",
    "timestamp": "2026-05-12 10:00"
  }
}
```

### 3. 强制性协作协议

**当前状态**: Agent评审随意
```
architect想评审什么就评审什么
想到多少就说多少
```

**应该有**: 强制性评审协议
```markdown
## Design Review强制协议

### 必须检查的维度（必须全部检查才能返回）:
1. [ ] 数据一致性 (事务、并发、边界条件)
2. [ ] 接口契约 (API设计、错误处理、版本管理)
3. [ ] 性能影响 (查询复杂度、N+1问题、缓存策略)
4. [ ] 安全风险 (权限、审计、敏感数据)
5. [ ] 可测试性 (测试覆盖度、mock策略、e2e可行性)
6. [ ] 运维影响 (监控、日志、部署、回滚)

### 评审完整性自检:
- 所有维度已检查: YES/NO
- 如有NO,必须继续检查直到全部YES
- 只有全部YES才能返回STATUS

### 禁止行为:
- 禁止在第一轮只检查部分维度
- 禁止渐进式发现问题（应该一次性发现所有）
```

### 4. Agent持久化机制

**当前状态**: 每个session重新初始化
```
session_1: 加载planner → 评审 → session结束
session_2: 加载planner → 评审 → session结束
# planner没有记住session_1的评审
```

**应该有**: 跨session的agent记忆
```
Persistent Agent State:
{
  "agent_id": "architect_v1",
  "memory": {
    "previous_reviews": [...],
    "common_issues": ["权限定义经常不完整", "事务边界经常模糊"],
    "successful_patterns": ["在API设计review时用checklist更有效"]
  }
}
```

### 5. Multi-agent决策机制

**当前状态**: 没有明确的分歧处理
```
如果planner和architect意见不一致 → ?
```

**应该有**: 明确的冲突解决协议
```markdown
## Multi-agent决策协议

### 决策层级:
1. domain专家 > 通用专家
   - 安全问题: security-reviewer决定
   - 架构问题: architect决定
   - 计划问题: planner决定

2. 实证 > 意见
   - 有数据支持的决定 > 基于经验的判断

3. 风险规避 > 速度
   - blocking issue优先于non-blocking优化

### 冲突升级路径:
Level 1: agents协商 → 自动解决
Level 2: 查阅共享上下文 → 基于历史决策
Level 3: 触发human-handoff → 人工决策
```

## 💡 具体改进方案

### 改进1: Agent Skill契约化

**当前**: skills只有description
```yaml
name: architect
description: Architecture review and design skill
```

**应该**: skills包含完整的协作契约
```yaml
name: architect
description: Architecture review and design skill
version: 2.0.0

contract:
  role_boundary:
    owns: ["系统架构", "接口设计", "数据模型", "技术选型"]
    consults: ["planner for priority", "security-reviewer for risks"]
    veto_rights: ["架构风险", "性能瓶颈", "可扩展性问题"]

  review_protocol:
    required_dimensions:
      - name: "data_consistency"
        checklist: ["事务边界", "并发控制", "数据完整性"]
        must_pass_before: "implementation"
      - name: "interface_design"
        checklist: ["REST契约", "错误处理", "版本管理"]
        must_pass_before: "implementation"

    quality_standard:
      - "所有维度必须检查"
      - "一次性给出完整反馈"
      - "明确区分blocking vs non-blocking"

    completeness_check:
      - "确认所有required_dimensions已检查"
      - "确认所有checklist items有明确结论"
      - "只有全部满足才能返回STATUS"

  escalation_criteria:
    triggers:
      - condition: "与planner意见冲突且无法协商"
        action: "invoke_woos_human_handoff"
      - condition: "设计风险等级=HIGH"
        action: "require_explicit_approval"
```

### 改进2: 共享评审上下文

**创建文件**: `skills/software-development/woos-review-context/SKILL.md`
```markdown
# Woos Review Context

## Purpose

维护跨gate的累积式评审上下文，确保agents能build on previous feedback。

## Data Structure

```yaml
review_context:
  prd_review:
    gate: "1.5"
    agents: ["planner", "architect"]
    timestamp: "2026-05-12T09:00:00Z"
    issues:
      - category: "scope"
        severity: "blocking"
        description: "权限矩阵未定义"
        resolution: "在capability contract中补充"
    approved: false

  design_review:
    gate: "2.5"
    agents: ["architect"]
    timestamp: "2026-05-12T10:00:00Z"
    builds_on: "prd_review"
    issues:
      - category: "architecture"
        severity: "blocking"
        description: "事务原子性未定义"
        resolution: "补充事务设计"
    resolved_from_previous:
      - "权限矩阵已在API设计中定义"
    approved: false
```

## Usage

在每个review gate启动agent时:

1. **加载历史上下文**:
   ```python
   context = load_review_context()
   previous_issues = context.issues_for_same_artifact()
   ```

2. **Agent评审时引用**:
   ```python
   architect_prompt = f"""
   请评审以下设计文档。

   之前的评审上下文:
   {context.formatted_summary()}

   请特别注意:
   - 检查之前发现的问题是否已解决
   - 不要重复提出已解决的问题
   - 累积式评审，build on previous feedback
   """
   ```

3. **更新上下文**:
   ```python
   context.add_review(
     gate="2.5",
     agent="architect",
     issues=new_issues,
     resolved=resolved_issues
   )
   save_review_context(context)
   ```
```

### 改进3: Agent评审质量强制

**修改agent skills添加强制协议**:

```markdown
# Architect Skill v2.0

## 强制性评审协议

### 前置条件检查（必须全部满足才能开始评审）:
- [ ] Design文档已完整阅读
- [ ] PRD和Capability Contract已阅读
- [ ] 之前的Review Context已加载
- [ ] 理解当前gate在workflow中的位置

### 强制检查维度（必须全部检查才能返回）:

#### 维度1: 数据一致性
必须检查:
- [ ] 所有写操作有明确的事务边界
- [ ] 并发场景有冲突检测或隔离机制
- [ ] 数据完整性约束已定义

输出格式:
```json
{
  "dimension": "data_consistency",
  "status": "PASS|REQUEST_CHANGES",
  "findings": ["具体问题描述"],
  "blocking": true/false
}
```

#### 维度2: 接口契约
必须检查:
- [ ] 所有REST端点遵循命名规范
- [ ] 错误码和错误消息标准化
- [ ] 版本管理策略明确

...（其他维度）

### 完整性自检（必须全部为YES才能返回）:
- [ ] 所有强制维度已检查
- [ ] 每个维度有明确的PASS/FAIL结论
- [ ] 所有REQUEST_CHANGES有明确的修复建议
- [ ] 已确认不是重复之前已提出的问题

### 返回条件:
只有满足以下条件才能返回STATUS:
- 所有强制维度检查完成
- 完整性自检全部为YES
- STATUS对应的证据链完整

### 禁止行为:
- ❌ 在第一轮只检查部分维度
- ❌ 渐进式发现问题（应该一次性发现所有）
- ❌ 不查看previous review context就评审
- ❌ 重复提出已解决的问题
```

### 改进4: Agent持久化

**修改`woos-run-orchestrator`添加agent持久化**:

```python
class AgentPool:
    """持久的agent实例池"""

    def __init__(self):
        self.agents = {}
        self.memories = {}

    def get_agent(self, agent_type):
        """获取或创建agent，保持记忆"""
        if agent_type not in self.agents:
            self.agents[agent_type] = self._create_agent(agent_type)

        # 加载该agent的历史记忆
        memory = self.memories.get(agent_type, self._load_memory(agent_type))
        self.agents[agent_type].set_memory(memory)

        return self.agents[agent_type]

    def save_agent_memory(self, agent_type):
        """保存agent的记忆"""
        agent = self.agents.get(agent_type)
        if agent:
            self.memories[agent_type] = agent.get_memory()
            self._persist_memory(agent_type, self.memories[agent_type])

# 在workflow中使用
orchestrator = AgentPool()

# Gate 1.5
planner = orchestrator.get_agent("planner")
review1 = planner.review(prd)
orchestrator.save_agent_memory("planner")

# Gate 2.5 (同一个planner实例，有记忆)
architect = orchestrator.get_agent("architect")
review2 = architect.review(design, context=review1)
orchestrator.save_agent_memory("architect")
```

### 改进5: Multi-agent决策机制

**创建skill**: `skills/software-development/woos-agent-decision/SKILL.md`

```markdown
# Woos Agent Decision

## Purpose

当agents意见不一致时，提供结构化的决策机制。

## Decision Protocol

### 决策层级

```
Domain专家决策 > 通用专家决策
实证决策 > 经验决策
风险规避 > 速度优先
```

### 权威矩阵

| 决策类型 | 权威Agent | 协商Agent | Veto条件 |
|---------|-----------|----------|---------|
| 架构设计 | architect | planner | 安全风险时security-reviewer可veto |
| 任务优先级 | planner | architect | 技术不可行时architect可veto |
| 安全问题 | security-reviewer | 所有 | 无veto，security-reviewer决定 |
| 性能问题 | architect | code-reviewer | - |
| 代码质量 | code-reviewer | architect | - |

### 决策流程

```python
def resolve_agent_conflict(agent_a_decision, agent_b_decision):
    """
    决策冲突解决流程
    """
    # Level 1: 检查权威矩阵
    if has_authority(agent_a_over_agent_b):
        return agent_a_decision

    # Level 2: 检查实证支持
    evidence_a = extract_evidence(agent_a_decision)
    evidence_b = extract_evidence(agent_b_decision)
    if evidence_a.strength > evidence_b.strength:
        return agent_a_decision

    # Level 3: 检查风险
    risk_a = assess_risk(agent_a_decision)
    risk_b = assess_risk(agent_b_decision)
    if risk_a < risk_b:
        return agent_a_decision

    # Level 4: 升级人工
    return escalate_to_human(
        conflict=(agent_a_decision, agent_b_decision),
        context={evidence_a, evidence_b, risk_a, risk_b}
    )
```

### Escalation触发条件

自动触发human-handoff的条件:
- 同一问题经过3轮agent协商仍不一致
- 涉及多个domain专家的复杂决策
- 风险等级=HIGH且无法自动化解
- 超过决策时间阈值（如2小时）

### 返回格式

```json
{
  "resolution": "agent_a|agent_b|escalated|hybrid",
  "reason": "决策依据",
  "confidence": 0.0-1.0,
  "requires_human": false,
  "next_action": "具体行动建议"
}
```
```

## 🎯 实施优先级

### P0 - 立即实施（本周）

1. **Agent Skill契约化**
   - 为planner/architect/code-reviewer添加`contract` section
   - 定义角色边界、评审协议、完整性自检

2. **强制性评审协议**
   - 在agent skills中添加"强制检查维度"
   - 要求"必须全部检查才能返回"
   - 禁止渐进式发现问题

### P1 - 短期实施（2周）

3. **共享评审上下文**
   - 创建`woos-review-context` skill
   - 维护跨gate的累积式评审记录
   - Agents评审时引用历史上下文

4. **Agent持久化**
   - 修改`woos-run-orchestrator`添加agent pool
   - 跨session复用agent记忆

### P2 - 中期实施（1个月）

5. **Multi-agent决策机制**
   - 创建`woos-agent-decision` skill
   - 定义权威矩阵和冲突解决流程
   - 实现自动escalation

## 📊 成功指标

**协作效率指标**:
- [ ] Agent评审平均轮数 ≤ 1.5 (当前2-3轮)
- [ ] Agent评审完整性 ≥ 95% (一次性发现所有问题)
- [ ] Agent间重复问题率 ≤ 5% (不重复提出已解决的问题)

**工作流效率指标**:
- [ ] 中等复杂度任务完成时间 ≤ 4小时 (当前13小时)
- [ ] Session碎片化 ≤ 10个/任务 (当前114个)
- [ ] Agent重用率 ≥ 80% (跨session复用)

**质量指标**:
- [ ] PRD/Design缺陷率 ≤ 10% (进入实现后)
- [ ] Code review rework率 ≤ 20% (第一轮review后)
- [ ] Gate通过率 ≥ 90% (第一轮尝试)

## 🎯 核心洞察

**问题不是"过度自动化"，而是"低质量协作"**

改进方向不是"减少自动化"，而是"提升agent协作质量"：

1. **明确契约** - 每个agent知道自己的边界和标准
2. **共享上下文** - Agents能build on each other's work
3. **强制协议** - 确保评审的完整性和一致性
4. **持久化** - Agents能跨session学习和改进
5. **决策机制** - 明确的冲突解决和escalation路径

这样既能保持"完全自动化"的目标，又能提升agent协作效率，实现真正的"近无人值守交付"。

---

**生成时间**: 2026-05-12
**视角**: Agent协作效率优化
**核心理念**: 完全自动化 + 高质量协作 = 近无人值守交付
