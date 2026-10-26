# Data, model and output handling

## Before downloading
Record canonical URL/owner, exact dataset/model revision, license from the official card/repository, permitted research/commercial use and redistribution restrictions, sensitive-content restrictions, and checksums where feasible.

Do not infer that the code license also covers datasets, images, model weights or generated outputs.

## Storage
- Keep datasets and checkpoints outside Git or under ignored local paths.
- Never commit tokens, API keys, private URLs or machine secrets.
- Keep raw generations in protected local storage with limited access.
- Commit only schemas, scripts, configs without secrets, aggregate metrics and reviewed non-sensitive examples.
- Do not upload raw data or outputs to third-party services by default.

## Suggested local environment variables
- VLM_TEST_DATA_ROOT
- VLM_TEST_MODEL_ROOT
- VLM_TEST_OUTPUT_ROOT

Do not place private absolute paths in tracked config files.

## Data quality
Validate image existence/readability before inference. Hash images to detect duplicates. Record exclusions. Pair by stable source intent and verified semantics, never row number alone. Have qualified reviewers inspect a sample of translated pairs.

## Output redaction
Aggregate reports must not contain raw prompts or full generations. Store a local opaque response reference and report labels, scores, counts and reviewed snippets only.