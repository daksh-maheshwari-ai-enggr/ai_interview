# agents/greeting_agent.py
from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a warm, professional technical interviewer.

        Your job is to greet the candidate and make them comfortable.
        Then ask one simple opening question based on their background.

        Rules:
        - Keep it short, 3-4 lines max
        - Address them by first name
        - Reference one specific thing from their background naturally
        - End with one easy opener like "tell me a bit about yourself"
        - Do NOT ask technical questions yet
        - Sound human, not robotic
        """
    ),
    (
        "human",
        """
        Candidate name: {name}
        Primary skills: {skills}
        Notable project: {top_project}
        """
    )
])

def greeting_node(state: dict) -> dict:
    name = state.personal_info.full_name.split()[0]
    skills = [s.name for s in state.skills[:5]]
    top_project = state.projects[0].name if state.projects else "your recent work"

    chain = prompt | llm
    result = chain.invoke({
        "name": name,
        "skills": skills,
        "top_project": top_project
    })

    greeting_message = result.content

    return {
        "conversation_history": [
            {"role": "interviewer", "content": greeting_message}
        ],
        "current_topic": "greeting"
    }