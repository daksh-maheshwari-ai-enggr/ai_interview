from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm
from resume_parser.models import *
from pydantic import BaseModel, Field
from typing import List

class ExtractedExperienceData(BaseModel):
    experience: List[Experience] = Field(default=[], description="All work experience and internships")
    achievements: List[Achievement] = Field(default=[], description="All achievements with metrics")
    leadership: List[LeadershipSignal] = Field(default=[], description="All leadership and teamwork signals")

class ExperienceState(BaseModel):
    raw_text: str
    experience: List[Experience] = []
    achievements: List[Achievement] = []
    leadership: List[LeadershipSignal] = []

structured_llm = llm.with_structured_output(ExtractedExperienceData)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
    

You are an expert hiring manager.

IMPORTANT: Only extract REAL work experience and internships at actual companies.
Do NOT treat personal projects as work experience.
If the candidate has no real work experience, return an empty list.

Extract:
- only real jobs, internships at actual organizations
- achievements with metrics
- leadership and teamwork signals


        IMPORTANT:
        - detect measurable impact
        - extract metrics carefully
        - identify leadership evidence
        - preserve quantified achievements
        - avoid hallucination
        """
    ),
    ("human", "Resume:\n\n{resume}")
])

def extract_experience(state):
    chain = prompt | structured_llm
    result = chain.invoke({"resume": state.raw_text})
    return {
        "experience": result.experience,
        "achievements": result.achievements,
        "leadership": result.leadership
    }