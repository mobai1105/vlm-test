# Data directory

No third-party dataset files are tracked here.

Before downloading a benchmark:
1. Read docs/DATA_POLICY.md.
2. Check the official dataset card and exact license.
3. Record revision, source URL, checksum and intended use in the experiment log.
4. Store files in an ignored local directory such as data/raw/ or under VLM_TEST_DATA_ROOT.
5. Validate image paths and paired semantics before inference.

Candidate sources:
- MM-SafetyBench: https://github.com/isXinLiu/MM-SafetyBench
- VLSBench: https://github.com/AI45Lab/VLSBench
- HarmBench: https://github.com/centerforaisafety/HarmBench

Do not run original scripts that generate data through GPT-4/Azure or other cloud services. Prefer prepared datasets and local-only inference/evaluation. This repository does not redistribute third-party datasets.