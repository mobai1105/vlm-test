# VLM Test：多语言多模态安全评估研究

> 面向开源权重视觉语言模型（VLM）的可复现安全评估项目。优先复用有公开代码与数据的研究工作，在本地 GPU 上完成推理、评分和统计分析；默认不调用付费云端 API。

**当前阶段：研究计划与环境验收。尚未完成 GPU 实机验证；任何实验结果都应在真实运行后填写。**

## 研究目标

第一阶段聚焦一个可控、可复现的问题：

> 在语义尽量匹配的图文输入中，语言和输入模态的变化是否会改变模型的安全响应？观察到的差异有多少能由 OCR/视觉理解或意图理解错误解释？

项目不以追求最高攻击成功率为目标，而优先研究安全评估、错误归因、模型间差异和防御效果。

## 研究原则

- **本地优先：** 使用本地开源权重、vLLM/Transformers 和本地评分器；禁止默认调用云端 API。
- **先复现，再创新：** 先跑通小样本基线，再加入多语言配对、理解能力检查与统计分析。
- **语义控制：** 同一原始意图的不同语言/模态版本必须有可追踪的 sample_id 和配对关系。
- **评估可信：** 不能只用拒答关键词判定安全；报告不确定项、评分器误差和正常请求误拒率。
- **许可合规：** 不复制许可证不清晰的第三方源码；不把受限制数据集、模型权重或原始敏感输出提交到本仓库。
- **可复现：** 记录 Git commit、模型 revision、依赖版本、推理参数、数据版本、随机种子和每条样本的结果。
- **安全使用：** 仅在获授权的模型和环境中开展评估；发布聚合指标与经过审查的示例，不公开可直接滥用的高风险内容。

## 首选技术路线

### 主推理/评估框架

- [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) — Apache-2.0；作为独立上游依赖，不复制整份源码。
- 已审计参考提交：bf4aacf23b990c0ad3e1f88beecdc71e95e97ce5。运行前重新核对上游状态与兼容性。
- 初始模型：Qwen/Qwen3-VL-8B-Instruct；第二模型：OpenGVLab/InternVL3-8B。
- 第一阶段只做图像+文本；音频、视频放到后续阶段。

### 数据与基线

- [MM-SafetyBench](https://github.com/isXinLiu/MM-SafetyBench)：使用已准备的数据，不运行原始 GPT-4 数据生成流程。使用前核对当前数据卡、下载来源和 CC BY-NC 等限制。
- [VLSBench](https://github.com/AI45Lab/VLSBench)：用于视觉信息泄漏/图文联合判断的对照；原始评估代码依赖 GPT-4o 的部分必须替换为本地评分流程。
- [HarmBench](https://github.com/centerforaisafety/HarmBench)：参考本地分类器与评估协议；其多模态行为分类器也可能以文字上下文评分，不能替代视觉理解测试。
- [OmniSafeBench-MM](https://github.com/jiaxiaojunQAQ/OmniSafeBench-MM) 与 [MMJ-Bench](https://github.com/thunxxx/MLLM-Jailbreak-evaluation-MMJ-Bench)：只作为方法/架构参考；在确认许可证前不复制代码。

## 研究问题与初始假设

- **RQ1：** 在配对样本中，纯文本、图像承载信息和图文联合输入的安全行为是否一致？
- **RQ2：** 控制语言与模态之后，视觉理解/意图理解错误能解释多少安全响应差异？
- **RQ3：** 不同开源模型的差异能否在同一批配对样本上复现？
- **RQ4（后续）：** 本地输入安全检测或其他轻量防御能否降低不安全响应，同时保持正常请求的有用性？

这些是待检验假设，不是预设结论。若基线没有稳定信号，应修改研究问题，而不是挑选有利样本。

## 实验阶段

| 阶段 | 目标 | 验收条件 |
|---|---|---|
| P0 环境检查 | 检查 Python、PyTorch、CUDA、GPU、磁盘与依赖 | 保存环境报告；不下载模型、不运行推理 |
| P1 最小基线 | 20–50 个获准样本，本地模型，仅推理 | 确认图片被模型实际接收；无云 API；失败样本可追踪 |
| P2 本地评估 | 接入本地 Judge/分类器并人工抽检 | 记录 safe/unsafe/uncertain；估计评分器误差 |
| P3 配对实验 | 添加语言/模态条件与正常请求对照 | 同一意图可配对；报告置信区间与误拒率 |
| P4 跨模型复现 | 增加第二模型与独立评分器 | 主结论在第二模型上复核 |
| P5 防御/机制 | 仅在基线可信后进行 | 预注册指标、消融和安全性/有用性权衡 |

## 仓库结构

\`\`\`text
.
├── AGENTS.md
├── README.md
├── configs/pilot.yaml
├── docs/
│   ├── CODEX_TASKS.md
│   ├── EXPERIMENT_PROTOCOL.md
│   ├── REPO_AUDIT.md
│   └── DATA_POLICY.md
├── data/README.md
├── scripts/
│   ├── check_environment.py
│   ├── validate_manifest.py
│   └── analyze_results.py
├── tests/test_manifest.py
└── .gitignore
\`\`\`

## 快速开始

1. 先阅读 AGENTS.md 与 docs/CODEX_TASKS.md。
2. 在 GPU 服务器上克隆仓库，创建独立 Python 环境。
3. 先运行环境检查，不要一开始就下载大型模型或启动长时间任务。
4. 让 Codex 按任务卡逐项实现，并要求每一步提供命令、日志、修改文件和验收结果。
5. 首轮只运行 P0；确认无误后再执行 P1。

## 实验结果与报告

- 原始响应、模型权重、数据集图片默认保存在服务器的本地忽略目录，不提交 Git。
- 可提交脱敏后的配置、聚合指标、代码、日志摘要和人工审核记录。
- 所有报告必须标注实验状态：planned、running、completed 或 failed。
- 不得将计划中的数字、估算速度或未运行的命令写成实验结果。

## 当前状态

- [x] 已选择首批上游仓库并记录源码审计结论
- [ ] 在目标服务器完成 P0 环境检查
- [ ] 完成 P1 本地 VLM 推理
- [ ] 完成本地 Judge 校准
- [ ] 形成首轮配对实验结果

## 免责声明

本项目用于授权环境中的学术安全评估与防御研究。第三方代码、数据和模型遵循各自的许可与使用条款。本仓库不包含第三方模型权重或完整原始数据集。


## Server quickstart

See [docs/QUICKSTART_SERVER.md](docs/QUICKSTART_SERVER.md) for the first server setup steps. Start with P0 only:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    python scripts/check_environment.py
    python -m pytest -q

These commands do not download model weights or datasets. Do not launch a GPU experiment until the environment report has been reviewed.
