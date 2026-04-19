import time
from SRC.gongju_core import GongjuCore

def test_reflex_latency():
    core = GongjuCore(psi=0.95)
    start = time.perf_counter()
    h = core.holistic_energy() # H = π * ψ²
    end = time.perf_counter()
    print(f"H-Energy calculated: {h}")
    print(f"Reflex Latency: {(end - start) * 1000:.4f} ms")

if __name__ == "__main__":
    test_reflex_latency()
