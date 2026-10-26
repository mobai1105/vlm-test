# 当前服务器环境快照

记录来源：用户提供的环境截图。助手未直接登录服务器；以下数值属于截图报告，不是本助手独立测量结果。记录日期：2026-10-26。

| 项 | 报告值 | 备注 |
|---|---|---|
| Python | 3.10.19 | `/bin/python -> python3.10` |
| PyTorch | 2.1.2+cu121 | CUDA 可用；需进行实际 CUDA kernel smoke test |
| GPU | 6 × RTX 5880 Ada | 每卡约 47.4 GiB；请确认这 6 张卡是否都由当前任务独占/可用 |
| Transformers | 4.51.0 | 适合先测试较早支持的模型；Qwen3-VL 需要更晚的 Transformers 版本 |
| vLLM | 未安装 | 暂不在现有环境里直接安装，避免破坏 PyTorch 依赖 |
| Pillow | 10.4.0 | 已安装 |
| pytest | 未安装 | 轻量开发依赖可在项目环境安装 |
| torchvision | 0.16.2+cu121 | 与 torch 2.1.2 系列对应，但需 smoke test |
| flash-attn | 2.5.8 | 安装信息不等于已在当前 GPU 上成功执行；需独立验证 |
| Triton | 2.1.0 | 与当前 torch 版本相关；不要与新 vLLM 随意混装 |
| Accelerate | 1.12.0 | 已安装 |
| datasets | 4.8.4 | 已安装 |
| PEFT | 0.18.1 | 已安装 |
| safetensors | 0.7.0 | 已安装 |
| PyYAML | 6.0.3 | 已安装 |
| pandas | 2.3.3 | 已安装 |
| cuDNN | 8902 | 报告值 |
| BF16 | 支持 | 仍需执行 BF16 运算并同步确认 |
| PyTorch arch list | sm_50/60/70/75/80/86/90 | 未列出 sm_89 本身不是失败结论；必须用真实 kernel 测试，第三方 CUDA 扩展需单独验证 |
| NVIDIA driver | 未知 | 需要在服务器执行 `nvidia-smi` 并记录 driver version |

## 当前决策

1. 先不安装 vLLM、不升级 PyTorch、不下载模型。
2. 运行 `python scripts/check_environment.py` 和 `python scripts/check_cuda.py`。
3. 如果 CUDA FP32/BF16 矩阵运算和同步通过，先用 Transformers 4.51.0 测试一个兼容的图文模型，例如 `Qwen/Qwen2.5-VL-7B-Instruct`。该步骤需要用户明确同意下载模型权重，且应先检查磁盘空间、Hugging Face 访问和模型许可。
4. 将 Qwen3-VL 和 vLLM 作为后续独立环境任务。不要为了一个新模型把目前可用的环境直接覆盖。
5. 先用无害的合成图片完成单次推理，不要一开始就跑越狱数据集。

## 需要补齐的事实

- `nvidia-smi` 完整输出（驱动版本、GPU 数量、是否有其他进程占用）。
- CUDA smoke test 是否通过。
- 每个 GPU 的 BF16 matmul 与同步是否通过。
- 当前环境中 `Qwen2_5_VLForConditionalGeneration` 是否可导入。
- 服务器磁盘剩余空间与 Hugging Face cache 位置。


## Model/framework compatibility note (added after checking official docs)

- Qwen3-VL official README states Transformers >= 4.57.0; the current 4.51.0 environment is not the right environment for Qwen3-VL. See https://github.com/QwenLM/Qwen3-VL/blob/main/README.md
- Qwen2.5-VL is documented in Transformers 4.49.0 and later; its official Qwen quickstart recommends Python >= 3.10 and PyTorch >= 2.3. The current Transformers 4.51.0 may provide the model class, but PyTorch 2.1.2 is below that recommendation. See https://huggingface.co/docs/transformers/v4.49.0/en/model_doc/qwen2_5_vl and https://qwen.readthedocs.io/en/v2.5/getting_started/quickstart.html
- Therefore, keep the existing environment unchanged. After the CUDA smoke test, create a separate candidate environment for Qwen2.5-VL using a mutually compatible PyTorch/torchvision pair (for example PyTorch 2.5.1 + torchvision 0.20.1 for CUDA 12.1) and Transformers 4.51.0. This is a proposed combination, not yet runtime-verified on the server.
- Do not install vLLM into the current environment. Revisit vLLM only after a target model has run successfully through Transformers and the server driver/version constraints are known.
