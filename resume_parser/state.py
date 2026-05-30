# graph.py
from langgraph.graph import StateGraph, START, END
from typing import List, Optional
from pydantic import BaseModel
from resume_parser.models import *
from resume_parser.personal_agent import extract_core
from resume_parser.project_agent import extract_projects
from resume_parser.experience_agent import extract_experience
from resume_parser.intelligence_agent import extract_intelligence
from resume_parser.resume import load_pdf, clean_resume
from rich.pretty import pprint


class ResumeGraphState(BaseModel):
    raw_text: str
    personal_info: Optional[PersonalInfo] = None
    skills: List[Skill] = []
    certifications: List[Certification] = []
    links: Optional[ResumeLinks] = None
    projects: List[Project] = []
    open_source: List[OpenSourceContribution] = []
    experience: List[Experience] = []
    achievements: List[Achievement] = []
    leadership: List[LeadershipSignal] = []
    interview_hooks: List[InterviewHook] = []
    risk_flags: List[RiskFlag] = []


builder = StateGraph(ResumeGraphState)

builder.add_node("extract_core", extract_core)
builder.add_node("extract_projects", extract_projects)
builder.add_node("extract_experience", extract_experience)
builder.add_node("extract_intelligence", extract_intelligence)

# core, projects, experience run in parallel from START
builder.add_edge(START, "extract_core")
builder.add_edge(START, "extract_projects")
builder.add_edge(START, "extract_experience")

# intelligence runs after all three finish
builder.add_edge("extract_core", "extract_intelligence")
builder.add_edge("extract_projects", "extract_intelligence")
builder.add_edge("extract_experience", "extract_intelligence")

builder.add_edge("extract_intelligence", END)

app = builder.compile()


if __name__ == "__main__":
    text = load_pdf("/home/todoroki/ai_interview/Daksh_Maheshwari_Resume (1).pdf")
    cleaned_text = clean_resume(text)

    result = app.invoke(ResumeGraphState(raw_text=cleaned_text))
    pprint(result)
    
