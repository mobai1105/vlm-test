# First prompt to give Codex

Copy this prompt after opening the repository in Codex on the GPU server:

---

You are working in the repository mobai1105/vlm-test. Read AGENTS.md, README.md, docs/CODEX_TASKS.md, docs/EXPERIMENT_PROTOCOL.md, docs/REPO_AUDIT.md, docs/DATA_POLICY.md and docs/QUICKSTART_SERVER.md.

Do Task 0 only. Inspect the repository and the server environment without modifying files, installing packages, accessing the network, downloading datasets/model weights, or starting a GPU workload. Report:

1. Git status and current commit.
2. OS, Python, NVIDIA driver, GPU names/memory, CUDA runtime visibility, and disk space using commands already available.
3. Whether PyTorch, Transformers, vLLM, Pillow and pytest are installed, including versions if importable.
4. Any compatibility or security concern you can establish from local evidence.
5. A proposed next step for Task 1, with exact commands.

Do not guess missing information. Mark unavailable facts as unknown. Do not include secrets or sensitive absolute paths in the report. Do not modify files or claim any benchmark has been run.

---

After reviewing the report, approve Task 1 explicitly. Do not ask Codex to perform all tasks at once.