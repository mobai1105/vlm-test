#!/usr/bin/env python3
"""Offline environment audit. Does not install packages or download models/data."""
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

OPTIONAL = ["torch", "transformers", "vllm", "PIL", "yaml", "pandas", "pytest"]

def command_output(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=8, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout.strip()[:12000], "stderr": p.stderr.strip()[:2000]}
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "reason": type(exc).__name__}

def main():
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "unset"),
        "nvidia_smi": command_output(["nvidia-smi"]),
        "disk_free_bytes": shutil.disk_usage(Path.cwd()).free,
        "optional_packages": {},
        "network_used": False,
        "weights_downloaded": False,
    }
    for name in OPTIONAL:
        try:
            module = __import__(name)
            report["optional_packages"][name] = getattr(module, "__version__", "installed")
            if name == "torch":
                report["torch_cuda"] = {
                    "torch_cuda_version": getattr(module.version, "cuda", None),
                    "cuda_available": bool(module.cuda.is_available()),
                    "device_count": int(module.cuda.device_count()) if module.cuda.is_available() else 0,
                    "devices": [module.cuda.get_device_name(i) for i in range(module.cuda.device_count())] if module.cuda.is_available() else [],
                }
        except Exception as exc:
            report["optional_packages"][name] = {"available": False, "reason": type(exc).__name__}
    output = Path(os.environ.get("VLM_TEST_OUTPUT_ROOT", "outputs"))
    output.mkdir(parents=True, exist_ok=True)
    target = output / "environment_report.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"report_path": str(target), "network_used": False, "weights_downloaded": False,
                      "python": sys.version.split()[0], "platform": platform.system(),
                      "gpu_query_available": "returncode" in report["nvidia_smi"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
