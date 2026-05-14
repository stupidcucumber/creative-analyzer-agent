from src.enums.prompt import DatabasePromptPartEnum


class HookTypes(DatabasePromptPartEnum):
    
    QUESTION = (
        "question",
        "Directly addressing the viewer with a query that targets a specific pain point or health curiosity.",
        "Did you know your 'metabolic age' might be 10 years older than your actual age?"
    )

    SHOCKING_FACT = (
        "shocking_fact",
        "Presenting counter-intuitive information or unconventional 'science' to disrupt current beliefs.",
        "Stress literally 'lives' in your hips—that's why traditional crunches aren't fixing your lower belly."
    )

    TRANSFORMATION = (
        "transformation",
        "Highlighting the contrast between a current struggle and a successful future outcome over a set timeframe.",
        "From feeling burnout and constant snacking to 15-minute wall Pilates and high energy in 28 days."
    )

    CALL_TO_ACTION = (
        "call_to_action",
        "A direct instruction to take a low-friction next step, often involving a personalized assessment.",
        "Take the 1-minute quiz now to see your personalized 28-day transformation plan."
    )


class HookVisualFormatType(DatabasePromptPartEnum):

    UGC = (
        "ugc",
        "User-Generated Content style that feels authentic, raw, and relatable. Usually shot on a smartphone.",
        "A person holding their phone in a kitchen, speaking directly into the lens with natural lighting and no fancy edits."
    )

    CINEMATIC = (
        "cinematic",
        "High-production value with professional lighting, color grading, and deliberate camera movements.",
        "A slow-motion close-up of a product being unboxed under moody studio lights with a shallow depth of field."
    )

    MOTION_GRAPHICS = (
        "motion_graphics",
        "Stylized digital animation, typography, and vector elements used to explain concepts or visualize data.",
        "Bold text popping onto a vibrant background in sync with a fast-paced beat, showing a graph trending upwards."
    )
