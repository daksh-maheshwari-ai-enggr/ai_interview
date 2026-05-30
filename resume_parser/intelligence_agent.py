from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm
from resume_parser.models import *
from pydantic import BaseModel, Field
from typing import List

class ExtractedIntelligenceData(BaseModel):
    interview_hooks: List[InterviewHook] = Field(default=[], description="Topics worth deep questioning with probable follow-up questions")
    risk_flags: List[RiskFlag] = Field(default=[], description="Red flags found in resume like shallow skills or buzzword usage")

class IntelligenceState(BaseModel):
    raw_text: str
    projects: List[Project] = []
    skills: List[Skill] = []
    experience: List[Experience] = []
    interview_hooks: List[InterviewHook] = []
    risk_flags: List[RiskFlag] = []

structured_llm = llm.with_structured_output(ExtractedIntelligenceData)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior FAANG interviewer.

        Generate interview hooks and risk flags.

        Interview Hooks:
        - topics worth deep questioning
        - probable follow-up questions
        - suspicious buzzwords

        Risk Flags:
        - shallow skill usage
        - buzzword-heavy resume
        - unrealistic project claims
        - missing depth indicators

        Be skeptical. Think like a real interviewer.
        Avoid generic observations.
        """
    ),
    ("human", "Resume:\n{resume}\n\nProjects:\n{projects}\n\nSkills:\n{skills}\n\nExperience:\n{experience}")
])

def extract_intelligence(state):
    chain = prompt | structured_llm
    result = chain.invoke({
        "resume": state.raw_text,
        "projects": state.projects,
        "skills": state.skills,
        "experience": state.experience
    })
    return {
        "interview_hooks": result.interview_hooks,
        "risk_flags": result.risk_flags
    }