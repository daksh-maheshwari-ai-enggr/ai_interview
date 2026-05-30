from interviewer.state import app
from interviewer.models import InterviewState
from resume_parser.state import app as resume_pipeline, ResumeGraphState
from resume_parser.resume import load_pdf, clean_resume

config = {"configurable": {"thread_id": "interview_1"}}

def get_recent_history(history: list, n: int = 6) -> list:
    return history[-n:]

def run_interview(resume_path: str):

    print("\n⏳ Parsing your resume...\n")
    text = load_pdf(resume_path)
    cleaned = clean_resume(text)
    layer1 = resume_pipeline.invoke(ResumeGraphState(raw_text=cleaned))
    print("✅ Resume parsed successfully\n")

    state = InterviewState(
        personal_info=layer1["personal_info"],
        skills=layer1["skills"],
        projects=layer1["projects"],
        experience=layer1["experience"],
        achievements=layer1["achievements"],
        leadership=layer1["leadership"],
        interview_hooks=layer1["interview_hooks"],
        risk_flags=layer1["risk_flags"]
    )

    # first run — pauses before evaluate_answer
    app.invoke(state, config=config)

    while True:
        # get current state from checkpointer
        current = app.get_state(config)
        history = current.values["conversation_history"]
        last_message = history[-1]["content"]

        print(f"\n🎙️  Interviewer: {last_message}\n")

        if current.values.get("interview_complete"):
            print("✅ Interview complete!")
            break

        user_input = input("👤 You: ").strip()

        if user_input.lower() in ["exit", "quit", "q"]:
            print("\n👋 Interview ended.")
            break

        # inject answer into paused state
        app.update_state(
            config,
            values={
                "last_answer": user_input,
                "conversation_history": get_recent_history(history)
            }
        )

        # resume graph — will pause again at next evaluate_answer
        app.invoke(None, config=config)


if __name__ == "__main__":
    resume_path = "/home/todoroki/ai_interview/Daksh_Maheshwari_Resume (1).pdf"
    run_interview(resume_path)