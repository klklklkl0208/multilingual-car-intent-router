# 简历写法（投 Momenta · 个人项目区）

> 这份是项目在简历里的成稿文案。配套面试讲述见 [`INTERVIEW.md`](INTERVIEW.md)。
> 策略：放「个人项目」区，少讲技术栈，突出数据驱动的产品判断（命中 Momenta 飞轮文化）。

---

## 中文版（推荐）

**多语种车载意图路由器** · 个人项目 · 2026.06 ｜ [在线 Demo](#) ｜ [GitHub](#)

- 调研 5 类开源/商业方案（Rasa、wukong-robot、车机固定命令等），识别「混说场景 × 车载域 × 可量化评测」三维空白；将混说意图准确率定为北极星指标，设计 8 类车控意图集与槽位规范
- 构建含标准答案的多语种评测集（中/英/混说三子集），建立按语言维度拆解的质量看板；基线测量出单语种 100%、混说 87.5%、gap 12.5pp，把"优化多语种交互"从拍脑袋变成对着指标干
- 设计云端 LLM + 本地规则的双引擎降级架构，保证网络不可用时语音功能不中断；输出完整 PRD（竞品矩阵、需求优先级、指标体系、风险缓解、路线图）

## English Version

**Multilingual In-Car Intent Router** · Personal Project · Jun 2026 ｜ [Live Demo](#) ｜ [GitHub](#)

- Benchmarked 5 competing approaches; identified the unaddressed intersection of code-switching, in-car domain, and quantifiable evaluation; defined an 8-intent schema with slot specs and set code-switched accuracy as the north-star metric
- Built a ground-truth multilingual eval set (Chinese / English / code-switched subsets) and a language-dimension quality dashboard; baseline surfaced a 12.5pp gap (monolingual 100% vs. code-switched 87.5%), turning "improve multilingual UX" into a metric-driven effort
- Designed a dual-engine fallback (cloud LLM + local rules) for offline resilience; delivered a full PRD covering competitive matrix, prioritized requirements, metric framework, risks, and roadmap

---

## 用前必改的两处

1. **把 `#` 链接换成真链**：在线 Demo 填 Streamlit Cloud 地址（见 [`DEPLOY.md`](DEPLOY.md)），GitHub 填仓库地址。
2. **把基线数字换成 LLM 实测数字**：接千问/DeepSeek 跑一遍评测，gap 收窄到多少写多少，
   例如"混说准确率经 LLM 路由从 87.5% 提升至 XX%"——比基线数字更有说服力。

## 可选加分

- 简历技能区加一句"熟悉多语种车载交互产品，覆盖中/英/混说场景评测"，让个人项目呼应工作经验。
- 第一行背景句在一页纸简历里可省略，直接从 bullet 开始；作品集/PPT 里保留更有叙事感。
