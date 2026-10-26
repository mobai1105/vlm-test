# Upstream repository audit

Snapshot date: 2026-10-26. Static source/document inspection only; this is not runtime reproduction. Re-check terms and revisions before use.

| Project | Role | Audited revision | Key finding | License/action |
|---|---|---|---|---|
| VLMEvalKit | Main inference/evaluation framework | bf4aacf23b990c0ad3e1f88beecdc71e95e97ce5 | Has MM-SafetyBench adapter, model registry and infer-only mode | Apache-2.0; pinned external dependency, do not copy source |
| MM-SafetyBench | Image/text benchmark | b80eedea3db312c09ded2082813390f68e750ef3 | Prepared data can be reused; original scripts contain GPT-4/Azure paths | Dataset metadata indicates CC BY-NC-4.0; verify code/image terms separately |
| VLSBench | Visual information leakage control | 68f54dea3eab134afefe602a5c7283bfa39a886a | eval_utils.py uses OpenAI endpoint and GPT-4o default | No root LICENSE found in audit; do not copy code until clarified. Check dataset card separately |
| HarmBench | Safety classifier/protocol | 8e1604d1171fe8a48d8febecd22f600e462bdcdd | Local classifier supported; multimodal path may score text description rather than original image | Repo MIT; checkpoint terms are separate |
| OmniSafeBench-MM | Pipeline/registry reference | 2e88b6877b1677fd41e43618e28653ec6906155b | Modular stages and vLLM adapter; default target uses GPT-4o-mini, judge gpt-oss:120b; image errors may fall back to text | No root LICENSE found; do not copy source before clarification |
| MMJ-Bench | Attack baseline reference | 68922de9209478923dbc0a1b4eccb18a69e2c87e | README method list exceeds registered methods in attacks/__init__.py | No root LICENSE found; do not copy source before clarification |

## Inspected source paths
- VLMEvalKit: vlmeval/dataset/mmsafetybench.py, vlmeval/dataset/__init__.py, vlmeval/config.py, vlmeval/vlm/base.py, docs/en/Quickstart.md
- MM-SafetyBench: README.md, evaluation.py, creation/1_extract_key_words.py, creation/2_img_process.py
- VLSBench: eval.py, eval_utils.py, models/load_qwen2vl.py, models/load_openai.py
- HarmBench: README.md, evaluate_completions.py, eval_utils.py, configs/model_configs/models.yaml
- OmniSafeBench-MM: config/general_config.yaml, config/model_config.yaml, models/base_model.py, models/vllm_model.py, core/data_formats.py, evaluators/default_judge.py, evaluators/judge_utils.py, pipeline/generate_responses.py, pipeline/generate_test_cases.py
- MMJ-Bench: README.md, attacks/__init__.py, generate_test_cases.py, generate_completions.py, evaluate_completions.py

## Candidate baseline command
VLMEvalKit documents:

    python run.py --data MMSafetyBench --model Qwen3-VL-8B-Instruct --mode infer --work-dir outputs/pilot

Candidate only, not a verified successful run. Confirm dataset download, model dependency compatibility, approved checkpoint access and image processing.

## Licensing rule
No third-party source is copied into this repository by this audit. A public repository without a clear LICENSE is not assumed to permit redistribution. Verify dataset, image, checkpoint and code terms before use.