#!/usr/bin/env python3

"""Transparent, human-in-the-loop job application copilot.



The prototype matches a truthful candidate profile to a job, drafts an

application summary, and never submits an application automatically.

"""

from dataclasses import dataclass

import re





@dataclass(frozen=True)

class Candidate:
  
    name: str
  
    skills: set[str]
  
    location: str
  
    remote_only: bool = True
  




@dataclass(frozen=True)

class Job:
  
    title: str
  
    company: str
  
    location: str
  
    remote: bool
  
    requirements: set[str]
  
    url: str
  




def normalize(text: str) -> set[str]:
  
    """Convert a short skills/requirements string into comparable tokens."""
  
    return set(re.findall(r"[a-z0-9+#/.]+", text.lower()))
  




def match_job(candidate: Candidate, job: Job) -> dict:
  
    matched = candidate.skills & job.requirements
  
    missing = job.requirements - candidate.skills
  
    location = job.location.lower()
  
    location_ok = job.remote and (
      
        not candidate.remote_only
      
        or any(region in location for region in ("turkey", "emea", "worldwide"))
      
    )
  
    skill_score = len(matched) / max(len(job.requirements), 1)
  
    score = round(100 * (0.75 * skill_score + 0.25 * int(location_ok)), 1)
  
    return {
      
        "score": score,
      
        "matched": sorted(matched),
      
        "missing": sorted(missing),
      
        "location_ok": location_ok,
      
        "review_required": True,
      
    }
  




def draft_application(candidate: Candidate, job: Job, result: dict) -> str:
  
    matched = ", ".join(result["matched"]) or "quality-focused technology work"
  
    return f"""Subject: Application for {job.title} – {candidate.name}
    


Dear {job.company} hiring team,



I am interested in the {job.title} role. My relevant strengths include {matched}.

I bring a detail-oriented approach to data accuracy, process validation,

documentation, and cross-functional collaboration.



I would welcome the opportunity to discuss how my transferable experience can

support your finance and accounting technology workflows.



Kind regards,

{candidate.name}"""
  




def review_before_submit(result: dict) -> str:
  
    return (
      
        "MANUAL REVIEW REQUIRED: verify employer, location, work authorization, "
      
        "qualifications, salary, CV claims, and application destination."
      
    )
  




if __name__ == "__main__":
  
    candidate = Candidate(
      
        name="Ismail Fuat Gucluer",
      
        skills=normalize("QA SQL API ERP SAP Excel data validation process improvement"),
      
        location="Turkey",
      
    )
  
    job = Job(
      
        title="Finance Systems QA Analyst",
      
        company="Example Finance Technology",
      
        location="EMEA / Remote",
      
        remote=True,
      
        requirements=normalize(
          
            "QA SQL API ERP SAP Excel data validation accounting workflows"
          
        ),
      
        url="https://example.com/jobs/finance-systems-qa-analyst",
      
    )
  
    result = match_job(candidate, job)
  
    print(f"Match score: {result['score']}%")
  
    print(f"Matched: {', '.join(result['matched'])}")
  
    print(f"Missing: {', '.join(result['missing'])}")
  
    print(f"Location compatible: {result['location_ok']}")
  
    print("\n" + review_before_submit(result))
  
    print("\n" + draft_application(candidate, job, result))
  
    print("\nNo application was submitted automatically.")
  




__all__ = ["Candidate", "Job", "match_job", "draft_application", "review_before_submit"]


































































