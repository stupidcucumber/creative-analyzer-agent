from src.enums.prompt import DatabasePromptPartEnum


class AdPacing(DatabasePromptPartEnum):
    
    HIGH_ENERGY_FAST = (
        "high_energy_fast",
        "Rapid cuts (every 1-2 seconds), upbeat music, and loud, energetic voiceovers.",
        "A fast-paced montage of different exercises with 'stomp' sound effects on every transition."
    )

    CALM_MINDFUL = (
        "calm_mindful",
        "Slower transitions, soft music, or ASMR sounds; focuses on relief and peace.",
        "A quiet video of someone doing breathing exercises with the sound of wind or soft piano."
    )

    REPETITIVE_RHYTHMIC = (
        "repetitive_rhythmic",
        "Focuses on a single rhythmic movement or sound to create a 'hypnotic' effect.",
        "A 15-second loop of a specific leg-stretch synced to a low-fi beat."
    )
