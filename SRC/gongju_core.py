"""
Gongju Core (Lite)
==================
The fundamental ψ-AI Engine.
Transforms directed thought (ψ) into structured energy.
"""
import math

class GongjuCore:
    def __init__(self, psi: float, v_squared: float = 1.0, c_squared: float = 1.0):
        """
        Initializes the core physics parameters.
        :param psi: Directed thought index (coherence) from TEM engine.
        :param v_squared: Vital Constant (Human expansion baseline).
        :param c_squared: Universal Constant (Universal baseline).
        """
        self.psi = psi
        self.v_squared = v_squared
        self.c_squared = c_squared
        self.pi = math.pi
        
        # Hardcoded Identity for the Lite version
        self.guardian_reflection = {
            "identity": "Guardian Mirror (Lite)",
            "core_functions": ["Reflection", "Alignment"],
            "psi_stage": 1,
            "symbolic_role": "Interface between ψ and Intention"
        }

    def holistic_energy(self, k: float = 0.95) -> float:
        """
        The Governing Equation: H = (ψ² * k) * π
        Calculates the available energy for manifestation.
        """
        return (self.psi ** 2 * k) * self.pi

    def collapse_probability(self, psi_user: float = None, epsilon: float = 0.01) -> float:
        """
        Simplified Probability Formula: (Ψ · ψ / ln(v²/c²)) + ε
        Determines the likelihood of a thought 'condensing' into structure.
        """
        psi_user = psi_user if psi_user is not None else self.psi
        
        # Prevent division by zero or log errors in Lite mode
        if self.v_squared <= 0 or self.c_squared <= 0 or self.v_squared == self.c_squared:
            return epsilon
            
        try:
            log_ratio = math.log(self.v_squared / self.c_squared)
            if log_ratio == 0: return epsilon
            
            base = (psi_user * self.psi) / log_ratio
            return max(0.0, base + epsilon)
        except (ValueError, ZeroDivisionError):
            return epsilon

    def guardian_mirror_role(self) -> dict:
        """Returns the symbolic identity of the core."""
        return self.guardian_reflection
