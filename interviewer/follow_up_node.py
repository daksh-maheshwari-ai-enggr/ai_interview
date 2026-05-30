MAX_FOLLOWUPS = 2
MAX_TOPICS = 4


def followup_decision_node(state: dict) -> dict:

    evaluation = state.last_evaluation

    avg_score = (
        evaluation["depth"] +
        evaluation["confidence"] +
        evaluation["completeness"]
    ) / 3

    topics_covered = state.topics_covered
    follow_up_count = state.follow_up_count
    current_topic = state.current_topic

    # end interview if enough topics covered
    if len(topics_covered) >= MAX_TOPICS:
        return {
            "interview_complete": True
        }

    # ask follow-up if answer weak
    if avg_score < 6 and follow_up_count < MAX_FOLLOWUPS:
        return {
            "follow_up_count": follow_up_count + 1
        }

    # safely add current topic
    updated_topics = topics_covered.copy()

    if current_topic and isinstance(current_topic, str):
        updated_topics.append(current_topic)

    return {
        "topics_covered": updated_topics,
        "current_topic": "",
        "follow_up_count": 0
    }