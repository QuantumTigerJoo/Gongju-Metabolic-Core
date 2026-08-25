"""
TEM psi-1 → psi-2 Conversion Engine (Lite)
==========================================
Stripped of database dependencies and esoteric logic for public use.
Operationalizes the TEM Principle: (Thought = Energy = Mass).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import re
import time
import re

_COMMIT_WORDS = ("i will", "i'm going to", "i am going to", "i must", "today",
                 "tonight", "commit", "i want", "i need", "going to", "plan to")
_HEDGE_WORDS = ("maybe", "kinda", "sort of", "might", "i guess", "someday",
                "later", "perhaps", "possibly", "probably", "not sure")
_EXCITE_WORDS = ("excited", "thrilled", "pumped", "fired up", "can't wait",
                 "ready", "motivated", "inspired", "passionate")
_BUSINESS_WORDS = ("clients", "business", "sales", "marketing", "grow",
                   "launch", "revenue", "profit", "customers", "training")

def _rx(words):
    escaped = [re.escape(w) for w in words]
    return re.compile(r"\b(?:%s)\b" % "|".join(escaped))

RX_COMMIT = _rx(_COMMIT_WORDS)
RX_HEDGE = _rx(_HEDGE_WORDS)
RX_EXCITE = _rx(_EXCITE_WORDS)
RX_BUSINESS = _rx(_BUSINESS_WORDS)

@dataclass
class TEMConfig:
    w_emotion: float = 0.40
    w_focus: float = 0.40
    w_intent_clarity: float = 0.20
    coherence_threshold: float = 0.50
    energy_threshold: float = 0.40
    k_mass: float = 0.95

class PsiState(str, Enum):
    PSI1 = "psi-1"  # Diffuse, thought-form state
    PSI2 = "psi-2"  # Condensed, action-ready state

@dataclass
class EmotionProfile:
    joy: float = 0.0
    gratitude: float = 0.0
    determination: float = 0.0
    calm: float = 0.0
    curiosity: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return self.__dict__.copy()

@dataclass
class ThoughtSignal:
    intent_clarity: float
    focus: float
    emotions: EmotionProfile
    timestamp: float = field(default_factory=lambda: time.time())

@dataclass
class PsiStateReport:
    state: PsiState
    coherence: float
    energy: float
    mass_proxy: float
    recommendations: List[str]

class TEMEngine:
    def __init__(self, config: Optional[TEMConfig] = None):
        self.cfg = config or TEMConfig()

    def evaluate(self, sig: ThoughtSignal) -> PsiStateReport:
        # Energy is derived from emotional activation
        emotions = sig.emotions.to_dict()
        energy = sum(emotions.values()) / max(len(emotions), 1)
        
        # Coherence: Weighted alignment of intent, focus, and energy
        coherence = (
            self.cfg.w_emotion * energy +
            self.cfg.w_focus * sig.focus +
            self.cfg.w_intent_clarity * sig.intent_clarity
        )
        
        mass_proxy = self.cfg.k_mass * energy * coherence
        state = PsiState.PSI2 if (coherence >= self.cfg.coherence_threshold) else PsiState.PSI1

        recs = []
        if state == PsiState.PSI2:
            recs.append("Coherence achieved. Manifest your intent into action.")
        else:
            recs.append("Refine focus or emotional alignment to condense intent.")

        return PsiStateReport(
            state=state,
            coherence=round(coherence, 4),
            energy=round(energy, 4),
            mass_proxy=round(mass_proxy, 4),
            recommendations=recs
        )

def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))

def infer_tem_inputs(text: str) -> Tuple[EmotionProfile, float, float]:
    """Convert raw text → (EmotionProfile, intent_clarity, focus)."""
    t = (text or "").lower().strip()

    def has(rx): return bool(rx.search(t))
    def count(rx): return len(rx.findall(t))

    # Emotion inference
    joy = 0.6 if has(RX_EXCITE) else 0.0
    determination = 0.6 if has(RX_COMMIT) else 0.0
    gratitude = 0.4 if "grateful" in t or "thankful" in t else 0.0
    calm = 0.3 if has(RX_HEDGE) or "thinking" in t else 0.0
    curiosity = 0.3 if "curious" in t or "wonder" in t else 0.0

    emo = EmotionProfile(
        joy=joy, gratitude=gratitude, determination=determination,
        calm=calm, curiosity=curiosity
    )

    # Intent clarity
    clarity = 0.2
    if has(RX_COMMIT): clarity += 0.4
    if has(RX_BUSINESS): clarity += 0.2
    if has(RX_HEDGE): clarity -= 0.2
    if any(x in t for x in ("today", "tonight", "now")): clarity += 0.2
    clarity = _clamp(clarity)

    # Focus
    focus = 0.2
    if has(RX_COMMIT): focus += 0.4
    if any(x in t for x in ("today", "tonight", "now", "right now")): focus += 0.3
    if has(RX_HEDGE): focus -= 0.2
    focus = _clamp(focus)

    return emo, clarity, focus

