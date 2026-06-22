# 简历写法（投 Momenta · 个人项目区）

> 这份是项目在简历里的成稿文案。配套面试讲述见 [`INTERVIEW.md`](INTERVIEW.md)。
> 策略：放「个人项目」区，少讲技术栈，突出数据驱动的产品判断（命中 Momenta 飞轮文化）。

---

## 中文版（推荐）

**多语种车载意图路由器** · 个人项目 · 2026.06 ｜ [在线 Demo](#) ｜ [GitHub](#)

> 一句话：针对车机多语种交互中被普遍忽略的"混说"场景，从竞品空白分析到评测体系搭建的完整产品实践。

- **机会识别**：调研 Rasa、wukong-robot、车机固定命令方案、多语种模型底座等 5 类开源/商业方案，产出竞品对比矩阵，识别「混说场景 × 车载域 × 可量化评测」三维市场空白；判断模型层已饱和，PM 价值应聚焦场景定义与质量度量，而非自研模型
- **产品定义**：设计 8 类车控意图集（空调/媒体/导航/车窗/座椅/电话等）与槽位规范，采用可扩展结构——新增功能仅需改动一处配置；以"混说意图准确率"为北极星指标，并定义单语种不退化、兜底误触率、降级可用率等护栏指标
- **评测体系**：构建带标准答案的多语种评测集（中/英/混说三子集，覆盖正式、口语化、带槽位等多种真实表达），搭建按语言维度拆解的质量看板，把"多语种交互好不好"从主观判断变成可量化、可按市场切分的指标
- **架构与产出**：设计云端 LLM 主路径 + 本地规则兜底的双引擎降级架构，保证网络不可用时语音功能不中断（车机可用性刚需）；输出完整 PRD，含竞品矩阵、P0/P1 需求优先级、指标体系、风险缓解与量产路线图

## English Version

**Multilingual In-Car Intent Router** · Personal Project · Jun 2026 ｜ [Live Demo](#) ｜ [GitHub](#)

> One line: An end-to-end product practice targeting the widely overlooked code-switching scenario in multilingual in-car interaction — from competitive gap analysis to an evaluation framework.

- **Opportunity**: Benchmarked 5 open-source/commercial approaches (Rasa, wukong-robot, fixed-command head units, multilingual model foundations); built a competitive matrix and identified the unaddressed intersection of code-switching × in-car domain × quantifiable evaluation; argued the model layer is saturated and PM value lies in scenario definition and quality measurement, not training models
- **Product definition**: Designed an 8-intent vehicle-control schema (climate / media / navigation / windows / seats / phone, etc.) with slot specs in an extensible structure — adding a feature touches a single config; set code-switched intent accuracy as the north-star metric, with guardrail metrics (no monolingual regression, false-trigger rate, fallback availability)
- **Evaluation framework**: Built a ground-truth multilingual eval set (Chinese / English / code-switched subsets, covering formal, colloquial, and slot-bearing expressions) and a language-dimension quality dashboard, turning "is multilingual UX good?" from subjective judgment into a quantifiable, market-segmentable metric
- **Architecture & deliverables**: Designed a dual-engine fallback (cloud LLM primary + local rule-based backup) for offline resilience — a hard requirement for in-car availability; delivered a full PRD covering competitive matrix, P0/P1 prioritization, metric framework, risk mitigation, and a productionization roadmap

---

## 用前必改的两处

1. **把 `#` 链接换成真链**：在线 Demo 填 Streamlit Cloud 地址（见 [`DEPLOY.md`](DEPLOY.md)），GitHub 填仓库地址。
2. **补上量化结果**：当前版本刻意没写准确率数字——因为扩充评测集后，规则引擎的"混说 gap"已不成立（规则引擎只是按关键词瞎撞，真正弱点是口语化表达）。要让"评测体系"那条更有力，接千问/DeepSeek 跑一遍，拿到 **LLM vs 规则引擎** 的真实对比（如"规则引擎总体 84.5%，LLM 路由提升至 XX%，且三语种均衡"），再补进去。这是这份简历从"想法不错"到"做出结果"的关键一跳。

## 可选加分

- 简历技能区加一句"熟悉多语种车载交互产品，覆盖中/英/混说场景评测"，让个人项目呼应工作经验。
- 第一行背景句在一页纸简历里可省略，直接从 bullet 开始；作品集/PPT 里保留更有叙事感。
