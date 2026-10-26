# Server quickstart

This guide intentionally starts with an offline check. Do not download models until the server configuration is known.

## 1. Clone and inspect

    git clone https://github.com/mobai1105/vlm-test.git
    cd vlm-test
    git status --short
    cat AGENTS.md
    cat docs/CODEX_TASKS.md

## 2. Create a lightweight environment

Use the Python version supported by the selected inference stack. Do not install vLLM/Transformers until the server's NVIDIA driver and CUDA compatibility are recorded. A lightweight initial environment is enough for the offline scripts:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements-dev.txt

## 3. Run P0 only

    python scripts/check_environment.py
    python -m pytest -q

Expected: the environment script writes outputs/environment_report.json; no weights or data are downloaded. Check that outputs/ is ignored by Git.

## 4. Ask Codex to inspect, not install

Use the Task 0 prompt in docs/CODEX_TASKS.md. Ask the agent to report the actual server facts and propose compatible pinned dependencies. Do not let it run a long model download before reviewing the plan.

## 5. After P0 passes

Choose the inference stack based on the actual driver and model architecture. The VLMEvalKit command documented in docs/REPO_AUDIT.md is a candidate only. It is not yet validated on your server. Use infer-only mode for the first pass and a local evaluator; do not enable a cloud judge.

## 6. Save experiment evidence

Each run should include a sanitized config, code commit, model/data revisions, environment report, command, exit code, sample counts, exclusions, judge calibration and aggregate metrics. Keep raw outputs on the secured server.
