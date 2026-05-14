from src.enums.prompt import DatabasePromptPartEnum


class EmotionalValenceType(DatabasePromptPartEnum):

    PAIN_AGITATION = (
        "pain_agitation",
        "Focuses on the 'Before' state, highlighting burnout, physical discomfort, or the emotional guilt of failed habits.",
        "It's exhausting to play the 'strong one' for everyone else while your own health and energy take a back seat."
    )

    ASPIRATIONAL_RELIEF = (
        "aspirational_relief",
        "Emphasizes the 'After' state, focusing on the feeling of lightness, confidence, and effortless transformation.",
        "Imagine waking up with natural energy and finally feeling comfortable in your favorite dress after just 28 days."
    )

    DIAGNOSTIC_AUTHORITY = (
        "diagnostic_authority",
        "A calm, objective, and fact-based tone that uses data or terminology to ground the solution in science.",
        "Studies show that somatic exercises can regulate the nervous system and lower cortisol levels more effectively than high-intensity cardio."
    )