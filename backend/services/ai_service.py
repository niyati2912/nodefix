# =========================================================
# NODEFIX AI SERVICE
#
# CURRENTLY:
# Local deterministic response
#
# LATER:
# Microsoft Azure AI Foundry
# =========================================================


def generate_response(
    equipment: str,
    problem: str,
    documents: list,
    photo_provided: bool = False
):

    sources = [
        document["title"]
        for document in documents
    ]


    # -----------------------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------------------

    if documents:

        context = " ".join(
            document["content"]
            for document in documents
        )

    else:

        context = (
            "No relevant laboratory documentation "
            "was found."
        )


    # -----------------------------------------------------
    # SIMPLE SAFETY / UNCERTAINTY CHECK
    # -----------------------------------------------------

    critical_words = [
        "smoke",
        "burning",
        "sparks",
        "fire",
        "electric shock",
        "shock",
        "overheating"
    ]


    problem_lower = problem.lower()


    safety_issue = any(
        word in problem_lower
        for word in critical_words
    )


    if safety_issue:

        answer = (
            "This issue may involve a safety-critical condition. "
            "Do not continue operating the equipment. "
            "Disconnect power where it is safe to do so and "
            "ask a laboratory technician to inspect the equipment."
        )

        return {
            "answer": answer,
            "confidence": "Low",
            "sources": sources,
            "escalated": True
        }


    # -----------------------------------------------------
    # NO DOCUMENTATION
    # -----------------------------------------------------

    if not documents:

        return {
            "answer": (
                "I couldn't find relevant documentation for this "
                "equipment. I don't want to invent troubleshooting "
                "instructions, so this issue should be reviewed "
                "by a laboratory technician."
            ),
            "confidence": "Low",
            "sources": [],
            "escalated": True
        }


    # -----------------------------------------------------
    # LOCAL DEMO RESPONSE
    # -----------------------------------------------------

    answer = (
        f"I found relevant documentation for {equipment}.\n\n"

        f"Based on your description:\n"
        f"“{problem}”\n\n"

        "Start with these checks:\n\n"

        "1. Verify the equipment has the expected power supply.\n"
        "2. Check that GND connections are shared correctly.\n"
        "3. Verify the control/signal pin matches the code.\n"
        "4. Inspect wiring for loose or incorrect connections.\n\n"

        f"Relevant documentation indicates: {context}\n\n"

        "These are preliminary troubleshooting steps. "
        "Verify the equipment state before making changes."
    )


    return {
        "answer": answer,
        "confidence": "Demo / Moderate",
        "sources": sources,
        "escalated": False
    }