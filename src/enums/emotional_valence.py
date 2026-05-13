from src.enums.prompt import DatabasePromptPartEnum


class EmotionalValenceType(DatabasePromptPartEnum):

    NEGATIVE = (
        "negative",
        "Focuses on pain points, risks, or the consequences of inaction to create urgency or empathy through shared struggle.",
        "It's frustrating to watch your hard work go unnoticed while competitors with inferior products take your market share."
    )

    POSITIVE = (
        "positive",
        "Emphasizes growth, success, and the aspirational benefits of a solution to inspire and motivate the audience.",
        "Imagine the sense of relief and excitement you'll feel when your workflow finally runs on autopilot, giving you your weekends back."
    )

    NEUTRAL = (
        "neutral",
        "A balanced, objective, and fact-based tone that prioritizes information delivery and professional credibility over emotional appeal.",
        "The latest industry data indicates a 15% shift toward automated logistics, suggesting a change in standard operating procedures."
    )