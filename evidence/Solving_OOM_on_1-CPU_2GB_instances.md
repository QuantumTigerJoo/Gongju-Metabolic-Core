# Deterministic Energy Governance: Solving OOM via TEM Physics

Most AI stacks treat LLM token outputs like a black box, leading to Out-Of-Memory (OOM) crashes on low-resource instances. In the **Gongju Metabolic Core**, we replace brute-force context with a **Deterministic Energy Governor** based on the TEM (Thought-Energy-Mass) framework.

## 📐 Geometrizing Intent
Gongju treats user intentionality as a frequency/amplitude ($\psi$). By calculating the **Holistic Energy** ($H$) of the pattern before the model fully commits, the system can "Veto" or refine the rollout to protect hardware constraints.

### The Physics:
$$H = \pi \cdot \psi^2$$

Where:
* **$\psi$**: The "Wave-Amplitude" of the user's intent.
* **$\psi^2$**: The probability density/intensity.
* **$\pi$**: The geometric constant turning a 1D token stream into a 2D "Field of Influence".

## 💻 Implementation

### 1. The Circuit Breaker (Core Physics)
Implemented in `gongju_core.py` to ensure stability on 2GB instances:

```python
def holistic_energy(self):
    """
    H = π × ψ²
    Acts as the 'Circuit Breaker' for instance stability.
    """
    return self.pi * (self.psi ** 2)

Surfacing the "Thinking State" in real-time:
# Lean TEM Context for real-time observability
Lean_TEM_Context = {
    "Resonance Code": f"{psi_report.resonance_code}",
    "Energy Intensity (H)": f"{3.14 * (psi_report.coherence**2):.2f}"
}

### 🎥 Evidence: Logic in Motion

<video src="https://github.com/QuantumTigerJoo/Gongju-Metabolic-Core/blob/main/media/Pre-Inference_CircuitBreaker.mp4?raw=true" width="100%" controls></video>
