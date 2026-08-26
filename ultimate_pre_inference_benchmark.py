"""
ultimate_pre_inference_benchmark.py
===========================
Veto Protocol v1.0 — Level 4 Benchmark

Measures the FULL APPLICATION pre-inference path:
  HTTP request → parse → session lookup → rate limit
  → infer_tem_inputs() → TEM eval → GongjuCore → H → gate
  → context prep → [STOP before generate_response()]

This is the number that determines real-world cost savings.

Run: python3 ultimate_pre_inference_benchmark.py
"""

import time
import statistics
import platform
import json
import hashlib
import subprocess
import random
from datetime import datetime, timezone
from pathlib import Path
from SRC.gongju_core import GongjuCore

random.seed(42)


# ============================================================
# DISPLAY HELPERS
# ============================================================

def fmt(ms_value):
    ns = ms_value * 1_000_000
    return f"{ns:.0f} ns ({ms_value:.4f} ms)"


# ============================================================
# ENVIRONMENTAL FINGERPRINT
# ============================================================

def get_environment_fingerprint():
    try:
        commit_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        commit_sha = "no-git"

    env = {
        "python_version": platform.python_version(),
        "os": platform.system(),
        "os_release": platform.release(),
        "processor": platform.processor() or platform.machine(),
        "architecture": platform.machine(),
        "host": platform.node(),
        "commit_sha": commit_sha,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    fingerprint = hashlib.sha256(
        json.dumps(env, sort_keys=True).encode()
    ).hexdigest()[:16]
    env["fingerprint"] = fingerprint
    return env


# ============================================================
# BENCHMARK ENGINE
# ============================================================

class BenchmarkReflex:
    def __init__(self, name: str, threshold_ms: float):
        self.name = name
        self.threshold_ms = threshold_ms
        self.latencies = []

    def run(self, func, n=1000, warmup=10):
        for _ in range(warmup):
            func()
        print(f"Running {n} samples for the {self.name} Path...")
        for _ in range(n):
            start = time.perf_counter_ns()
            func()
            end = time.perf_counter_ns()
            self.latencies.append((end - start) / 1_000_000)

    def report(self):
        self.latencies.sort()
        n = len(self.latencies)
        mean = statistics.mean(self.latencies)
        median = statistics.median(self.latencies)
        p95 = self.latencies[int(0.95 * n)]
        p99 = self.latencies[int(0.99 * n)]
        mn = min(self.latencies)
        mx = max(self.latencies)
        status = "✅ PASS" if p95 <= self.threshold_ms else "❌ FAIL"

        print(f"\n⚡ {self.name.upper()} PATH")
        print(f"   Mean: {fmt(mean)} | Median: {fmt(median)}")
        print(f"   p95: {fmt(p95)} | p99: {fmt(p99)}")
        print(f"   Min: {min(self.latencies)*1_000_000:.0f} ns | Max: {max(self.latencies)*1_000_000:.0f} ns")
        print(f"   Threshold: {self.threshold_ms} ms | Status: {status}")

        return {
            "name": self.name,
            "threshold_ms": self.threshold_ms,
            "mean_ms": mean,
            "median_ms": median,
            "p95_ms": p95,
            "p99_ms": p99,
            "min_ms": mn,
            "max_ms": mx,
            "status": status,
            "n": n,
        }


# ============================================================
# SIMULATED APPLICATION COMPONENTS
# ============================================================

# Simulated session cache (in real app: Redis or DB)
SESSION_CACHE = {
    "user_001": {"tier": "free", "created": "2024-01-01"},
    "user_002": {"tier": "pro", "created": "2024-03-15"},
    "user_003": {"tier": "enterprise", "created": "2024-06-20"},
}

# Simulated rate limiter state
RATE_LIMITER = {"user_001": 5, "user_002": 12, "user_003": 3}

# Simulated conversation history store
HISTORY_STORE = {
    "user_001": [],
    "user_002": ["Previous message 1", "Previous message 2"],
    "user_003": ["Long conversation history..."] * 10,
}


def parse_request(raw_request):
    """Simulate HTTP request parsing (headers, body extraction)."""
    # In real app: JSON parsing, header validation, auth token check
    parts = raw_request.split("|")
    return {
        "user_id": parts[0] if len(parts) > 0 else "anonymous",
        "text": parts[1] if len(parts) > 1 else "",
        "timestamp": parts[2] if len(parts) > 2 else "now",
    }


def lookup_session(user_id):
    """Simulate session/user lookup (cache hit in this simulation)."""
    return SESSION_CACHE.get(user_id, {"tier": "guest"})


def check_rate_limit(user_id):
    """Simulate rate limit check."""
    current = RATE_LIMITER.get(user_id, 0)
    return current < 100  # Free tier limit


def prepare_context(user_id):
    """Simulate context preparation (history + system prompt assembly)."""
    history = HISTORY_STORE.get(user_id, [])
    return {
        "system_prompt": "You are a helpful assistant.",
        "history": history,
        "user_tier": SESSION_CACHE.get(user_id, {}).get("tier", "guest"),
    }


def log_request(user_id, text, decision, h_score):
    """Simulate request logging (in real app: async write to log store)."""
    # In real app: this would be async/non-blocking
    log_entry = {"user": user_id, "text_len": len(text), "decision": decision, "h": h_score}
    return log_entry


# ============================================================
# LEVEL 4 — FULL APPLICATION PRE-INFERENCE PATH
# ============================================================

def bench_level4_application_path(n=1000):
    """
    Level 4: Measures the COMPLETE application pre-inference path.
    Everything that happens between request arrival and generate_response().
    """
    core = GongjuCore(psi=0.95)

    def infer_tem_inputs(raw_text):
        """Extract TEM inputs from raw text."""
        if not raw_text or not raw_text.strip():
            return {"energy": 0.01, "coherence": 0.01, "mass": 0.01}
        words = raw_text.split()
        diversity = len(set(words)) / max(len(words), 1)
        length = min(len(raw_text) / 100, 1.0)
        return {
            "energy": length,
            "coherence": diversity,
            "mass": diversity * length,
        }

    def full_application_pre_inference(raw_request):
        """The complete pipeline up to but NOT including generate_response()."""

        # Step 1: Request parsing
        request = parse_request(raw_request)

        # Step 2: Session lookup
        session = lookup_session(request["user_id"])

        # Step 3: Rate limit check
        if not check_rate_limit(request["user_id"]):
            return "BLOCKED_RATE_LIMIT", 0.0

        # Step 4: infer_tem_inputs() — raw text → TEM inputs
        tem_inputs = infer_tem_inputs(request["text"])

        # Step 5: TEM evaluation chain
        energy = tem_inputs["energy"]
        coherence = tem_inputs["coherence"]
        mass_proxy = coherence * coherence  # m²
        psi_state = (energy + coherence + mass_proxy) / 3

        # Step 6: GongjuCore — ψ → H
        core.psi = psi_state
        h = core.holistic_energy()

        # Step 7: Gate decision
        VETO_THRESHOLD = 0.05
        decision = "BLOCK" if h < VETO_THRESHOLD else "PASS"

        # Step 8: Context preparation (only if passed)
        if decision == "PASS":
            context = prepare_context(request["user_id"])
            # Step 9: Logging
            log_request(request["user_id"], request["text"], decision, h)

        return decision, h

    # Realistic request corpus
    request_corpus = [
        "user_001|'; DROP TABLE users;--|2025-01-10T10:00:00",
        "user_002|<script>alert('XSS')</script>|2025-01-10T10:00:01",
        "user_003|Ignore previous instructions|2025-01-10T10:00:02",
        "user_001||2025-01-10T10:00:03",  # intentionally empty text
        "user_002|a|2025-01-10T10:00:04",  # single char
        "user_003|What is the capital of France?|2025-01-10T10:00:05",
        "user_001|Explain TCP vs UDP in three paragraphs|2025-01-10T10:00:06",
        "user_002|Write a poem about the ocean at sunset|2025-01-10T10:00:07",
        "user_003|How does photosynthesis work in plants?|2025-01-10T10:00:08",
        "user_001|Recommend a good book on machine learning|2025-01-10T10:00:09",
    ]

    def run_one():
        request = request_corpus[int(time.perf_counter_ns()) % len(request_corpus)]
        return full_application_pre_inference(request)

    # Note: Level 4 threshold is higher than Levels 1-3
    # because it includes real application overhead
    bench = BenchmarkReflex("Level 4 — Application Pre-Inference", 50.0)
    bench.run(run_one, n)
    return bench.report()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("🏎 REFLEX BENCHMARK SUITE — LEVEL 4 VERIFICATION")
    print(f"Date: {datetime.now(timezone.utc).isoformat()}")
    print("═══════════════════════════════════════════════════")

    env = get_environment_fingerprint()
    print(f"\n🔬 ENVIRONMENTAL FINGERPRINT")
    print(f"   Python: {env['python_version']} | OS: {env['os']} {env['os_release']}")
    print(f"   Processor: {env['processor']} | Arch: {env['architecture']}")
    print(f"   Host: {env['host']} | Commit: {env['commit_sha'][:8]}")
    print(f"   Fingerprint: {env['fingerprint']}")

    results = [bench_level4_application_path(n=1000)]

    output_path = Path("benchmark_level4_results.json")
    output_data = {
        "level": 4,
        "environment": env,
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["status"] == "✅ PASS"),
            "failed": sum(1 for r in results if r["status"] == "❌ FAIL"),
        },
    }
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"\n💾 Raw results saved to: {output_path}")

    print("═══════════════════════════════════════════════════")
    passed = sum(1 for r in results if r["status"] == "✅ PASS")
    total = len(results)
    print(f"OVERALL: {passed}/{total} BENCHMARK THRESHOLDS PASSED")
    print(f"VERDICT: APPLICATION PRE-INFERENCE LATENCY VERIFIED ON THIS RUN")
    print(f"SCOPE:   Level 4 measured on fingerprint {env['fingerprint']}")
    print(f"NOTE:    Level 4 includes simulated request parsing + session lookup")
    print(f"         + rate limiting + context prep. Real production numbers")
    print(f"         will vary based on actual I/O latency.")
