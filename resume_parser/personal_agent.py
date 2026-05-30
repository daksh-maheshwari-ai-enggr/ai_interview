from pydantic import BaseModel, Field
from typing import List,Annotated
from resume_parser.models import *
from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm






class ExtractedCoreData(BaseModel):
    personal_info: PersonalInfo | None = Field(
        default=None, 
        description="Full personal information of candidate"
    )
    skills: List[Skill] = Field(
        default=[], 
        description="All technical and soft skills mentioned"
    )
    certifications: List[Certification] = Field(
        default=[], 
        description="All certifications with issuer and date"
    )
    links: ResumeLinks | None = Field(
        default=None, 
        description="All URLs found in resume"
    )



class CoreResumeState(BaseModel):
    raw_text: str
    personal_info: PersonalInfo | None = None
    skills: List[Skill] = []
    certifications: List[Certification] = []
    links: ResumeLinks | None = None



structured_llm = llm.with_structured_output(ExtractedCoreData)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert resume parsing system.

        Extract:
        - personal information (name, email, phone, location, linkedin, github)
        - technical skills with category and proficiency
        - certifications with issuer and date
        - all hyperlinks found

        RULES:
        - Do not hallucinate any information
        - Normalize technology names (e.g. "js" → "JavaScript")
        - Categorize skills carefully (backend, frontend, ml, devops etc)
        - Extract ALL hyperlinks present
        - Return empty lists if section not found, never null for lists
        """
    ),
    (
        "human",
        "Resume:\n\n{resume}"
    )
])


def extract_core(state: CoreResumeState) -> dict:
    chain = prompt | structured_llm


    result: ExtractedCoreData = chain.invoke({
        "resume": state.raw_text
    })


    return {
        "personal_info": result.personal_info,
        "skills": result.skills,
        "certifications": result.certifications,
        "links": result.links
    }




