#!/usr/bin/env python3

"""Transparent multi-criteria AI project scorer for competition-style submissions.



This educational prototype ranks software project proposals by combining impact,

technical readiness, reproducibility, responsible-AI evidence, and risk. It is

not a judge and must not be presented as an official competition result.

"""

from dataclasses import dataclass





@dataclass(frozen=True)

class Proposal:
  
    name: str
  
    impact: float
  
    technical_readiness: float
  
    reproducibility: float
  
    responsible_ai: float
  
    delivery_risk: float
  




def clamp(value: float) -> float:
  
    """Keep a score in the documented 0-100 range."""
  
    return max(0.0, min(100.0, value))
  




def score(proposal: Proposal) -> float:
  
    """Return an explainable weighted score; risk is a bounded penalty."""
  
    positive = (
      
        0.30 * proposal.impact
      
        + 0.25 * proposal.technical_readiness
      
        + 0.20 * proposal.reproducibility
      
        + 0.15 * proposal.responsible_ai
      
    )
  
    return round(clamp(positive - 0.10 * proposal.delivery_risk), 2)
  




def rank(proposals: list[Proposal]) -> list[tuple[Proposal, float]]:
  
    """Rank proposals from strongest to weakest without breaking ties arbitrarily."""
  
    return sorted(((proposal, score(proposal)) for proposal in proposals), key=lambda item: (-item[1], item[0].name))
  




def explain(proposal: Proposal) -> str:
  
    """Describe the dominant strengths and the largest review concern."""
  
    dimensions = {
      
        "impact": proposal.impact,
      
        "technical readiness": proposal.technical_readiness,
      
        "reproducibility": proposal.reproducibility,
      
        "responsible AI": proposal.responsible_ai,
      
    }
  
    strengths = ", ".join(name for name, value in sorted(dimensions.items(), key=lambda item: item[1], reverse=True)[:2])
  
    return f"strengths={strengths}; review_risk={proposal.delivery_risk:.0f}/100"
  




if __name__ == "__main__":
  
    proposals = [
      
        Proposal("Community Transit Copilot", 92, 78, 88, 90, 18),
      
        Proposal("Supply Chain Vision", 86, 90, 70, 68, 30),
      
        Proposal("Study Rhythm Agent", 78, 82, 92, 84, 12),
      
    ]
  


    print("Competition-style proposal ranking")
  
    for position, (proposal, total) in enumerate(rank(proposals), start=1):
      
        print(f"{position}. {proposal.name} | score={total:.2f} | {explain(proposal)}")
      
    print("Note: scores are a transparent simulation, not an official competition judgment.")
  










































