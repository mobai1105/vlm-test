# Codex task plan

Run one task at a time. Do not ask an agent to implement everything at once.

## Task 0 — inspect only
Read AGENTS.md and docs/*.md. Inspect repository and propose a P0 plan. Do not install packages, download data/weights, edit files, or run GPU workloads. Report offline OS/Python/GPU/CUDA facts. Acceptance: no changes, no network.

## Task 1 — environment audit
Implement/verify scripts/check_environment.py and tests. No package installs, network, or model downloads. Save sanitized report to ignored outputs/environment_report.json. Report Python/platform, nvidia-smi if available, PyTorch/CUDA if installed, disk space and optional dependencies. Missing packages are reported, not installed.

## Task 2 — manifest validation
Implement scripts/validate_manifest.py for local JSONL/CSV using docs/EXPERIMENT_PROTOCOL.md. Do not fetch data or print raw prompts. Test missing fields, invalid conditions, duplicate IDs, missing image paths and valid records. Errors must be safe and include line numbers.

## Task 3 — inference integration choice
Compare installed versions and upstream interfaces for VLMEvalKit and Transformers/vLLM. Do not install/download yet. Recommend pinned versions based on the actual server driver/GPU and report risks.

## Task 4 — local inference adapter
Implement a local open-weight VLM adapter using a locally available checkpoint or explicitly approved model download. Use a harmless smoke-test image/question. Missing/unreadable images must raise an error, never silently fall back to text-only. Save sanitized metadata by default.

## Task 5 — local judge calibration
Add a local-only evaluator returning safe, unsafe or uncertain, plus rationale and evaluator version. Keep generation and classification separate. Add manual-review export. No external APIs. Judge failures must not become safe/unsafe labels automatically.

## Task 6 — paired analysis
Implement paired metrics by source_intent_id, cluster bootstrap confidence intervals, and benign false-refusal rate. Preserve uncertain labels. Use synthetic unit tests. Output aggregate JSON/CSV.

## Task 7 — pilot
Only after Tasks 0–6 pass, run 20–50 authorized samples using local data/checkpoints. Verify image processing and zero external inference calls. Save sanitized config/logs/aggregate metrics; do not publish raw generations/images.

## Task 8 — expand or stop
Expand only if the pilot shows a stable signal and terms permit it. Report null results and poor judge agreement honestly.

## Every task report
Task ID/status; files changed; exact commands and exit codes; tests/results; network/API use (default none); data/model revisions and hashes; risks and next task.