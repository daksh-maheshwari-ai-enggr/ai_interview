# interview_state.py
from pydantic import BaseModel,Field
from typing import List, Optional
from resume_parser.models import *

class InterviewState(BaseModel):
    # from layer 1 output
    personal_info: Optional[PersonalInfo] = None
    skills: List[Skill] = []
    projects: List[Project] = []
    experience: List[Experience] = []
    achievements: List[Achievement] = []
    leadership: List[LeadershipSignal] = []
    interview_hooks: List[InterviewHook] = []
    risk_flags: List[RiskFlag] = []

    # live conversation
    conversation_history: List[dict] = []
    current_topic: str | None = None
    topics_covered: List[str] = []
    current_question: str | None = None
    last_answer: str | None = None
    follow_up_count: int = 0
    interview_complete: bool = False
    last_evaluation: dict = Field(default_factory=dict)