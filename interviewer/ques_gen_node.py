# agents/question_generator_agent.py
from langchain_core.prompts import ChatPromptTemplate
from resume_parser.llm import llm

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a sharp technical interviewer.

        Based on the candidate profile and conversation so far,
        generate the next interview question.

        Rules:
        - Pick from unused interview hooks first
        - Question must be specific, not generic
        - Reference their actual project or skill by name
        - One question only, no preamble
        - If follow_up_count > 0 you are doing a follow up so go deeper on same topic
        - If follow_up_count is 0 pick a fresh topic from unused hooks
        """
    ),
    (
        "human",
        """
        Candidate skills: {skills}
        Projects: {projects}
        Interview hooks: {hooks}
        Topics already covered: {topics_covered}
        Conversation so far: {history}
        Follow up count on current topic: {follow_up_count}
        Current topic: {current_topic}
        """
    )
])

def question_generator_node(state: dict) -> dict:
    chain = prompt | llm
    result = chain.invoke({
        "skills": [s.name for s in state.skills],
        "projects": [p.name for p in state.projects],
        "hooks": [(h.topic, h.probable_questions) for h in state.interview_hooks],
        "topics_covered": state.topics_covered,
        "history": state.conversation_history,
        "follow_up_count": state.follow_up_count,
        "current_topic": state.current_topic
    })

    question = result.content

    history = state.conversation_history + [
        {"role": "interviewer", "content": question}
    ]

    return {
        "current_question": question,
        "conversation_history": history
    }