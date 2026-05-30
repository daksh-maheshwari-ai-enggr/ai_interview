from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm
from pydantic import BaseModel, Field
import json
import re


class AnswerEvaluation(BaseModel):
    depth_score: int = Field(
        description="Technical depth of answer from 1-10"
    )

    confidence_score: int = Field(
        description="Confidence level in answer from 1-10"
    )

    completeness_score: int = Field(
        description="How completely candidate answered from 1-10"
    )

    reasoning: str = Field(
        description="Why these scores were given"
    )

    weak_points: list[str] = Field(
        default_factory=list,
        description="Specific weak points in the answer"
    )

    strong_points: list[str] = Field(
        default_factory=list,
        description="Specific strong points in the answer"
    )


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a strict FAANG technical interviewer evaluating a candidate's answer.

Score honestly:
- depth_score: did they explain WHY not just WHAT
- confidence_score: did they sound sure or vague
- completeness_score: did they address all parts of the question

Rules:
- Be harsh, not generous
- Low scores for buzzword answers with no substance
- High scores only for specific, detailed, reasoned answers
- weak_points must be specific, not generic

IMPORTANT:
Return ONLY valid JSON.
Do NOT return markdown.
Do NOT return code blocks.

All scores MUST be integers not strings.

Correct:
{{
  "depth_score": 7,
  "confidence_score": 6,
  "completeness_score": 8,
  "reasoning": "Good technical explanation",
  "weak_points": ["Missing scalability discussion"],
  "strong_points": ["Good architecture explanation"]
}}

Wrong:
{{
  "depth_score": "7"
}}
"""
    ),
    (
        "human",
        """
Question asked: {question}

Candidate answer:
{answer}

Candidate projects:
{projects}

Candidate skills:
{skills}
"""
    )
])


def answer_evaluator_node(state: dict) -> dict:

    chain = prompt | llm

    response = chain.invoke({
        "question": state.current_question,
        "answer": state.last_answer,
        "projects": [p.name for p in state.projects],
        "skills": [s.name for s in state.skills]
    })

    try:
        # Parse raw JSON response
        cleaned = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(cleaned)

        # Force integer conversion
        data["depth_score"] = int(data["depth_score"])
        data["confidence_score"] = int(data["confidence_score"])
        data["completeness_score"] = int(data["completeness_score"])

        # Validate with Pydantic
        result = AnswerEvaluation(**data)

    except Exception as e:

        print("Evaluation parsing error:", e)
        print("Raw response:", response.content)

        # fallback result
        result = AnswerEvaluation(
            depth_score=0,
            confidence_score=0,
            completeness_score=0,
            reasoning="Failed to evaluate answer properly.",
            weak_points=["Evaluation parsing failed"],
            strong_points=[]
        )

    history = state.conversation_history + [
        {
            "role": "candidate",
            "content": state.last_answer
        }
    ]

    return {
        "last_evaluation": {
            "depth": result.depth_score,
            "confidence": result.confidence_score,
            "completeness": result.completeness_score,
            "reasoning": result.reasoning,
            "weak_points": result.weak_points,
            "strong_points": result.strong_points
        },
        "conversation_history": history
    }