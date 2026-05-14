from src.enums.prompt import DatabasePromptPartEnum


class BodyLogic(DatabasePromptPartEnum):
    
    DEMONSTRATION = (
        "demonstration",
        "Showing the product or service in action to prove its ease of use or effectiveness.",
        "A screen-recording of the BetterMe app showing how a user selects their meal plan."
    )

    SOCIAL_PROOF = (
        "social_proof",
        "Using testimonials, reviews, or 'before and after' stories to build trust through others.",
        "A compilation of three different users saying: 'I never thought I could stick to a plan until this'."
    )

    EDUCATIONAL_TEARDOWN = (
        "educational_teardown",
        "Explaining a concept (e.g., biology or psychology) to make the user feel they've learned something new.",
        "Explaining the science of 'cortisol belly' and why high-intensity workouts might be making it worse."
    )

    OBJECTION_HANDLING = (
        "objection_handling",
        "Directly addressing common reasons why people don't sign up (time, cost, effort).",
        "Text overlay: 'Too busy for the gym? These 10-minute routines can be done in your pajamas'."
    )