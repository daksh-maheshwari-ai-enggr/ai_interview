# interview_graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from interviewer.models import InterviewState
from interviewer.greeting_node import greeting_node
from interviewer.ques_gen_node import question_generator_node
from interviewer.ans_eval_node import answer_evaluator_node
from interviewer.follow_up_node import followup_decision_node


def should_continue(state: dict) -> str:
    if state.interview_complete:
        return "end"
    return "ask_question"


def after_decision(state: dict) -> str:
    if state.interview_complete:
        return "end"
    return "ask_question"


builder = StateGraph(InterviewState)

builder.add_node("greeting", greeting_node)
builder.add_node("ask_question", question_generator_node)
builder.add_node("evaluate_answer", answer_evaluator_node)
builder.add_node("decide_followup", followup_decision_node)

builder.add_edge(START, "greeting")
builder.add_edge("greeting", "ask_question")
builder.add_edge("ask_question", "evaluate_answer")
builder.add_edge("evaluate_answer", "decide_followup")

builder.add_conditional_edges(
    "decide_followup",
    after_decision,
    {
        "ask_question": "ask_question",
        "end": END
    }
)
checkpointer=MemorySaver()
app = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["evaluate_answer"]
)