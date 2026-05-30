from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm
from resume_parser.models import *
from pydantic import BaseModel, Field
from typing import List

class ExtractedProjectsData(BaseModel):
    projects: List[Project] = Field(default=[], description="All projects found in resume")
    open_source: List[OpenSourceContribution] = Field(default=[], description="All open source contributions")

class ProjectsState(BaseModel):
    raw_text: str
    projects: List[Project] = []
    open_source: List[OpenSourceContribution] = []

structured_llm = llm.with_structured_output(ExtractedProjectsData)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert technical interviewer.

        Extract ALL projects and open source contributions.

        IMPORTANT:
        - Technologies are EXTREMELY important
        - Detect backend/frontend/AI/devops domains
        - Extract architecture clues
        - Extract deployment technologies
        - Extract databases carefully
        - Extract GitHub/live URLs
        - Detect ownership level
        - Identify complexity indicators
        - Avoid hallucination
        """
    ),
    ("human", "Resume:\n\n{resume}")
])

def extract_projects(state):
    chain = prompt | structured_llm
    result = chain.invoke({"resume": state.raw_text})
    return {
        "projects": result.projects,
        "open_source": result.open_source
    }