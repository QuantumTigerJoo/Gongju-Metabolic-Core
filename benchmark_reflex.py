import time
import statistics
import platform
from datetime import datetime, timezone
from SRC.gongju_core import GongjuCore

class BenchmarkReflex:
    def __init__(self, name: str, threshold_ms: float):
        self.name = name
        self.threshold_ms = threshold_ms
        self.latencies = []

    def run(self, func, n=1000, warmup=10):
        # Warm-up phase (not recorded)
        for _ in range(warmup):
            func()

        # Actual measurement
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
        print(f"   Mean: {mean:.3f} ms | Median: {median:.3f} ms")
        print(f"   p95: {p95:.3f} ms | p99: {p99:.3f} ms")
        print(f"   Min: {mn:.3f} ms | Max: {mx:.3f} ms")
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
            "n": n
        }

def bench_reflex_path(n=1000):
    core = GongjuCore(psi=0.95)

    def local_h_calc():
        return core.holistic_energy()

    bench = BenchmarkReflex("Reflex", 2.0)
    bench.run(local_h_calc, n)
    return bench.report()

if __name__ == "__main__":
    print("🏎 REFLEX BENCHMARK SUITE — VERIFICATION REPORT")
    print(f"Date: {datetime.now(timezone.utc).isoformat()}")
    print(f"Host: {platform.node()}")
    print("═══════════════════════════════════════════════════")

    results = [bench_reflex_path(n=1000)]

    print("═══════════════════════════════════════════════════")
    print(f"OVERALL: {sum(1 for r in results if r['status'] == '✅ PASS')}/{len(results)} CLAIMS VERIFIED")
