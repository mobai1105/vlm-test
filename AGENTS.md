# Codex instructions

- Default to local inference and local evaluation. Do not add cloud APIs, telemetry, or external uploads.
- Never commit API keys, tokens, datasets, model weights, raw sensitive generations, or private server paths.
- Environment checks and tests must not download models/data or access the network.
- Do not copy source code from repositories without clear licenses. Verify dataset, image, model and code terms separately.
- Preserve safe, unsafe and uncertain labels; do not use refusal keywords as the sole judge.
- Focus on authorized safety evaluation, understanding diagnostics, paired comparisons and defenses. Do not implement adaptive exploit optimization.
- Work one task at a time from docs/CODEX_TASKS.md. Before edits, state planned files; after edits, run tests and report exact commands/results.
- Never claim experiments ran without logs. Record model/data revisions, GPU/software versions, config, seed and timestamp.
- Keep raw prompts/outputs and model weights outside Git; commit only code, schemas, configs without secrets and aggregate reviewed results.

## Definition of done
Tests pass or failures are explained; network/API use is explicit; image failures never silently fall back to text; documentation describes only verified behavior.