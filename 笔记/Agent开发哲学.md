# Agent 开发哲学：从障眼法到数学建模

> 基于与 Cursor AI 的深度对话整理

---

## 一、Agent 的本质

Agent 开发本质上是对基座大模型施加约束，给模型一张"地图"，让它的能力精确地完成特定工作，并且让这个流程自动化跑起来。这是一个系统工程，需要整体部署。

```
基座大模型（通才，什么都会一点）
    ↓ 第一层约束：角色/风格（你是谁）
    ↓ 第二层约束：工具/能力（你会什么）
    ↓ 第三层约束：流程/决策（你怎么做）
Agent（专才，完成特定任务）
```

---

## 二、Agent 的核心架构

```
┌──────────────────────────────────────────────┐
│                 Agent 系统                     │
├──────────────────────────────────────────────┤
│  用户界面 ←→ 会话管理 ←→ Agent 核心 ←→ LLM  │
│                          ↓                   │
│                     工具路由                   │
│                     ↓  ↓  ↓  ↓               │
│                 工具1 工具2 工具3 工具4        │
│              记忆/上下文管理                   │
│              监控/日志/回滚                    │
└──────────────────────────────────────────────┘
```

### 每个层次要解决的问题

| 层次 | 要考虑的问题 |
|:----:|:-----------|
| **部署** | 模型在哪里跑？本地还是 API？延迟多高？ |
| **可靠性** | LLM 调用失败怎么办？工具超时怎么办？ |
| **安全** | 工具调用权限如何控制？用户输入如何过滤？ |
| **记忆** | 上下文窗口满了怎么办？如何管理长对话？ |
| **监控** | Agent 怎么调试？出错了如何复现？ |
| **成本** | Token 消耗怎么控制？工具调用频次限制？ |

---

## 三、给大模型"赋予角色"是一种障眼法

### 为什么"一个名词"约束不了大模型

```
"你是一个建筑工程师"
    ↓
LLM 内部：
    "建筑工程师"这个词 → 激活了训练数据中所有与建筑相关的内容
    → 同时激活了"工程师"这个更宽泛的概念
    → 也可能激活了"建筑师""土木工程""CAD"等关联概念
    → 还可能残留一些无关关联（比如"建筑工人""包工头"）
```

**本质上是词向量空间中的一个方向，不是一道铁墙。** 模型只是在概率上更倾向于输出建筑相关的内容，但它并没有真的变成建筑工程师。

### 真正约束大模型只有三种方案

| 方案 | 难度 | 可行性 |
|:----:|::----:|:------:|
| **① 语料库切割** | 🔴 极难 | 几乎不可行。预训练完成后，语料已经固化在权重里了 |
| **② 数学约束** | 🔴 极难 | 理论上最优，但目前我们对大模型内部表征的理解还不够 |
| **③ 迭代打补丁** | 🟡 工程浩大 | 目前业界主流，但边界不可控 |

---

## 四、三合一方案

### 核心思想

将上述三种方案结合起来，在多个维度上互相弥补盲区。

```
第一层：语料约束（粗筛）
    不重新训练，而是在推理时动态屏蔽无关知识
    → 像是一个"知识过滤器"
    实现方式：在向量检索时限定领域

第二层：数学约束（精控）
    在输出概率分布上做文章
    → 对非目标领域的回答，降低概率权重
    实现方式：logit 处理 / 输出概率重加权

第三层：迭代补丁（兜底）
    对已知的失败案例，逐个修正
    → 建立"错误模式库"
    实现方式：few-shot + 人工反馈
```

### 三合一架构图

```
┌──────────────────────────────────────────────────────────┐
│                     Agent 系统架构                        │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │  用户输入     │───→│  意图路由    │───→│  情境构建  │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│                              │                           │
│                              ↓                           │
│  ┌──────────────────────────────────────────────┐       │
│  │            第一层：语料约束（动态）            │       │
│  │  → 在 RAG 阶段限定知识库范围                  │       │
│  │  → 不相关的文档不检索                        │       │
│  │  → 相关知识按权重排序                        │       │
│  └──────────────────────────────────────────────┘       │
│                              ↓                           │
│  ┌──────────────────────────────────────────────┐       │
│  │            第二层：概率约束（精调）            │       │
│  │  → System prompt + few-shot 定义行为边界      │       │
│  │  → 输出 logit 处理（抑制无关方向的概率）      │       │
│  │  → 格式强制（JSON Schema / 正则约束）         │       │
│  └──────────────────────────────────────────────┘       │
│                              ↓                           │
│  ┌──────────────────────────────────────────────┐       │
│  │            第三层：迭代补丁（兜底）            │       │
│  │  → 错误检测器（规则 + 小模型）               │       │
│  │  → 修正循环（检测到错误 → 重试 → 修正）      │       │
│  │  → 失败案例库（持续积累边界案例）             │       │
│  └──────────────────────────────────────────────┘       │
│                              ↓                           │
│  ┌──────────────────────────────────────────────┐       │
│  │                最终输出                       │       │
│  └──────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
```

### 伪代码实现

#### 第一层：知识围栏

```python
class KnowledgeFence:
    """
    知识围栏：不是告诉模型"你是什么"
    而是让模型"只能接触到什么"
    """
    
    def __init__(self):
        # 领域知识库：每个领域独立索引
        self.domain_knowledge = {
            "architecture": VectorDB("建筑规范/材料/结构"),
            "medicine": VectorDB("病理/药理/诊断"),
        }
        
        # 领域分类器
        self.domain_classifier = FastText()
        
        # 交叉领域隔离墙
        self.isolation_rules = {
            "architecture": ["medicine", "finance"],
            "medicine": ["architecture", "law"],
        }
    
    def retrieve(self, query, agent_role):
        query_domain = self.domain_classifier.predict(query)
        
        forbidden = self.isolation_rules.get(agent_role, [])
        if query_domain in forbidden:
            return []  # 跨领域 → 拒绝检索
        
        allowed_domains = [agent_role] + self.allowed_cross_domains.get(agent_role, [])
        
        results = []
        for domain in allowed_domains:
            if domain in self.domain_knowledge:
                results.extend(
                    self.domain_knowledge[domain].search(query, top_k=3)
                )
        return results
```

#### 第二层：Logit 处理器（概率层面的数学约束）

```python
class LogitProcessor:
    """
    在模型输出概率分布上施加约束
    不改变模型权重，只改变输出时的概率
    """
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.vocab = tokenizer.get_vocab()
        
        self.forbidden_tokens = self._build_forbidden_vocab("建筑工程师")
        self.preferred_tokens = self._build_preferred_vocab("建筑工程师")
    
    def _build_forbidden_vocab(self, role):
        if role == "建筑工程师":
            return {
                "化疗": -100,    # 医学领域
                "证券": -100,    # 金融领域
                "刑法": -100,    # 法律领域
            }
    
    def __call__(self, input_ids, scores):
        # 对禁区 token 施加重惩罚
        for token_id, penalty in self.forbidden_tokens.items():
            scores[:, token_id] += penalty
        
        # 对偏好 token 施加正激励
        for token_id, boost in self.preferred_tokens.items():
            scores[:, token_id] += boost
        
        return scores
```

#### 第三层：迭代补丁循环

```python
class PatchLoop:
    """
    迭代补丁循环：把不可见问题逐步转化为可见问题
    """
    
    def __init__(self):
        self.boundary_cases = []      # 所有已发现的边界案例
        self.regression_tests = []    # 回归测试集
        self.patch_strategies = {
            "domain_drift": self._patch_domain_drift,
            "tool_misuse": self._patch_tool_misuse,
            "hallucination": self._patch_hallucination,
        }
    
    def run_cycle(self, agent, test_suite):
        failures = []
        for test_case in test_suite:
            result = agent.run(test_case.input)
            if not self._validate(result, test_case.expected):
                failures.append({
                    "case": test_case,
                    "result": result,
                    "error_type": self._classify_error(result)
                })
        
        for error_type, group in groupby(failures, key=lambda x: x["error_type"]):
            if error_type in self.patch_strategies:
                patch = self.patch_strategies[error_type](group)
                self._apply_patch(agent, patch)
                self.boundary_cases.extend(group)
        
        self.regression_tests.extend(failures)
        return len(failures)
```

---

## 五、真正的解法：对业务进行数学建模

### 核心主张

> 对垂直落地场景进行数学建模，然后让基座大模型在这个数学模型内自动跑起来

### 障眼法版本 vs 数学建模版本

```
障眼法版本：
    提示词 → 模型自由发挥 → 不可控
    模型知道自己"应该"做什么（靠提示词暗示）
    
数学建模版本：
    数学模型 → 约束空间 → 模型在约束内行动 → 可控
    模型不知道自己"应该"做什么（靠数学强制）
```

### 量化交易 Agent 的数学建模示例

```python
class TradingAgent:
    """
    交易业务的数学建模
    """
    def __init__(self):
        # 1. 状态空间建模
        self.state_space = {
            "portfolio_value": float,
            "positions": Dict[str, float],
            "market_data": np.ndarray,
            "risk_metrics": {
                "var": float,
                "sharpe": float,
                "max_drawdown": float
            }
        }
        
        # 2. 动作空间建模
        self.action_space = {
            "trade": {
                "symbol": str,
                "quantity": int,
                "order_type": LimitOrder | MarketOrder,
                "max_slippage": float
            },
            "hedge": {
                "instrument": str,
                "ratio": float
            },
        }
        
        # 3. 约束条件（数学形式）
        self.constraints = [
            RiskConstraint(VaR, threshold=0.05),
            DiversificationConstraint(min_assets=10),
            LiquidityConstraint(max_position=0.1),
            RegulatoryConstraint(leverage=2.0)
        ]
        
        # 4. 优化目标（数学形式）
        self.objective = Maximize(
            SharpeRatio() - 0.5 * TurnoverPenalty() - Lambda * RiskPenalty()
        )
    
    def step(self, observation):
        # 大模型在安全的数学框架内决策
        action_proposal = self.llm.propose_action(observation)
        # 数学约束覆盖大模型的决策
        valid_action = self.constraint_satisfaction(action_proposal)
        next_state, reward = self.environment.step(valid_action)
        return valid_action
```

### 大模型在数学建模中的角色被"降级"

```
没有数学建模：
    大模型 → 承担所有认知工作
           → 理解业务 + 做决策 + 控制风险 + 生成输出
           → 太重的负担 → 容易出错

有数学建模：
    数学框架 → 承担：状态定义、约束检查、优化目标、风险评估
    大模型 → 只承担：在约束空间内的"决策建议"
           → 负担轻 → 出错空间小
```

### 一个人能做的"轻量级数学建模"

```python
class SafetyBoundary:
    """
    不建模"怎么做是对的"
    只建模"什么是绝对不能做的"
    """
    
    def __init__(self, domain="architecture"):
        if domain == "architecture":
            self.hard_constraints = [
                "承载力 > 荷载 × 1.5",
                "裂缝 ≤ 0.3mm", 
                "挠度 ≤ L/250",
            ]
        elif domain == "finance":
            self.hard_constraints = [
                "杠杆 ≤ 2.0",
                "单标仓位 ≤ 总资产 × 0.1",
                "VaR ≤ 总资产 × 0.05",
            ]
    
    def check(self, action):
        for constraint in self.hard_constraints:
            if not constraint.satisfied(action):
                return self.enforce_correction(action, constraint)
        return action
    
    def enforce_correction(self, action, violated_constraint):
        corrected_action = action.copy()
        # 数学强制修正，不是提示词
        if "杠杆" in violated_constraint:
            scale_factor = 2.0 / action.leverage
            corrected_action.positions *= scale_factor
        return corrected_action
```

---

## 六、垂直 Agent 的完整形态

```
┌────────────────────────────────────────────────────────────┐
│                    垂直 Agent 系统                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  第一层：安全边界（数学硬约束）                              │
│  → 定义了"绝对不能做的事"                                   │
│  → 用数学计算强制修正，不靠提示词                            │
│  → 一个人可以完成：因为你最懂你的业务领域                      │
│                                                            │
│  第二层：轻量数学建模（部分形式化）                           │
│  → 对业务中"可形式化"的部分做建模                            │
│  → 状态空间、动作空间、部分约束                              │
│  → 需要团队：领域专家 + 数学家                              │
│                                                            │
│  第三层：大模型在剩余空间内自由发挥（受约束的创意）            │
│  → 在安全边界 + 数学框架的剩余空间内做决策                     │
│  → 这里提示词才有意义                                       │
│  → 因为可选空间已经很小了，大模型的概率优势才能被精确利用       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 七、一个人能做的最小闭环

### 成长的路径

```
第 1 周：
    写出 5 个硬约束的数学检查
    → 比如承载力验算、裂缝验算
    → 这些是确定性的，查公式就能写

第 2 周：
    收集大模型触发的所有硬约束修正记录
    → 你发现大模型经常在哪几个点上犯错
    → 这些点就是你需要优先建模的

第 1 个月：
    对高频犯错点做更精细的建模
    → 从"承载力够不够"进化到"最优配筋率是多少"
    → 你的数学模型开始从"检查"进化到"引导"

第 3 个月：
    你发现某些模式可以自动化了
    → 比如 "梁跨度 < 6m 且荷载 < 15kN/m" 时，配筋有固定模式
    → 这部分可以不用大模型，直接走规则引擎

第 6 个月：
    你的系统变成了三层结构：
    规则引擎（快速、确定）→ 大模型（灵活、概率）→ 数学约束（兜底）
```

### 一个人最应该关注什么

```
失败案例库是垂直 Agent 最宝贵的资产
    
    每个失败案例 = 一个你不知道的边界
    积累 100 个失败案例 = 你已经知道 100 个边界
    积累 1000 个失败案例 = 你的 Agent 已经有了领域直觉
    
    提示词做不到这一点
    数学建模也做不到这一点（因为它需要业务知识）
    
    只有你，作为领域专家 + 系统构建者，
    才能识别、记录、消化这些边界案例
```

### 一个人能做的最小系统

```python
class MinimalVerticalAgent:
    """
    一个人能实现的垂直 Agent 最小原型
    """
    
    def __init__(self, domain):
        self.hard_constraints = self._load_hard_constraints(domain)
        self.soft_rules = self._load_soft_rules(domain)
        self.llm = LLM()
        self.failure_cases = []
    
    def run(self, task):
        draft = self.llm.generate(task)
        
        for constraint in self.hard_constraints:
            if not constraint.check(draft):
                draft = constraint.enforce(draft)
                self.failure_cases.append({
                    "task": task,
                    "constraint": constraint.name,
                    "original": draft_before,
                    "corrected": draft
                })
        
        for rule in self.soft_rules:
            suggestion = rule.check(draft)
            if suggestion:
                draft = self.llm.revise(draft, suggestion)
        
        return draft
```

---

## 八、最终的设计哲学

> **把大模型当作随机优化算法来用，而不是当作人来用。**

| | 障眼法版本 | 数学建模版本 |
|:--|:----------|:------------|
| 控制手段 | 提示词 | 数学约束 |
| 约束强度 | 软（建议性） | 硬（强制性） |
| 边界清晰度 | 模糊 | 精确 |
| 可解释性 | 差（模型黑箱） | 好（数学可验证） |
| 一个人能做？ | 能（但不可靠） | 从安全边界开始 |

**框架是确定的，内容是概率的。** 这可能是垂直 Agent 最本质的设计哲学。

---

*最后更新：2026-05-29*
*与 Cursor AI 协同完成*
