from pydantic import BaseModel
from typing import List

class PersonalInfo(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    location: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

class Skill(BaseModel):
    name: str
    category: str
    proficiency: str | None = None
    mentioned_in: List[str] = []

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    github_url: str | None = None
    live_url: str | None = None
    role: str | None = None
    complexity_level: str | None = None
    domain: str | None = None
    team_size: int | None = None
    duration: str | None = None
    features: List[str] = []
    responsibilities: List[str] = []
    challenges_faced: List[str] = []
    architecture_summary: str | None = None
    database_used: List[str] = []
    deployment_used: List[str] = []
    ai_features: List[str] = []
    impact: str | None = None   

class Experience(BaseModel):
    company_name: str
    role: str
    duration: str
    responsibilities: List[str]
    technologies: List[str]
    leadership: List[str] = []
    team_collaboration: List[str] = []
    metrics: List[str] = []     


class OpenSourceContribution(BaseModel):
    project_name: str
    contribution_type: str
    technologies: List[str]
    pull_requests: List[str] = []
    issue_links: List[str] = []
    description: str

class Certification(BaseModel):
    name: str
    issuer: str
    skills: List[str] = []
    issue_date: str | None = None
    credential_url: str | None = None    

class Achievement(BaseModel):
    title: str
    description: str
    category: str
    related_skills: List[str] = []

class LeadershipSignal(BaseModel):
    activity: str
    evidence: str
    communication_level: str | None = None
    teamwork_level: str | None = None  

class ResumeLinks(BaseModel):
    github_links: List[str] = []
    linkedin_links: List[str] = []
    portfolio_links: List[str] = []
    project_links: List[str] = []
    blog_links: List[str] = []  

class InterviewHook(BaseModel):
    topic: str
    reason: str
    probable_questions: List[str]  

class RiskFlag(BaseModel):
    issue: str
    severity: str
    evidence: str   

class ResumeData(BaseModel):
    personal_info: PersonalInfo
    skills: List[Skill]
    projects: List[Project]
    experience: List[Experience]
    certifications: List[Certification]
    achievements: List[Achievement]
    open_source: List[OpenSourceContribution]
    leadership: List[LeadershipSignal]
    links: ResumeLinks
    interview_hooks: List[InterviewHook]
    risk_flags: List[RiskFlag]               