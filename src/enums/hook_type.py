from src.enums.prompt import DatabasePromptPartEnum


class HookTypes(DatabasePromptPartEnum):
    
    QUESTION = (
        "question",
        "Start with a thought-provoking question to engage the reader's curiosity.",
        "Have you ever wondered why some people succeed where others fail?"
    )

    SURPRISING_FACTS = (
        "surprising_facts",
        "Present surprising facts or statistics that demand attention.",
        "Did you know that 65% of the population are visual learners?"
    )

    STORYTELLING = (
        "storytelling",
        "Begin with a compelling narrative or historical anecdote.",
        "In 1998, two college friends started a small venture from a dorm room. That venture became Google."
    )

    CHALLENGE = (
        "challenge",
        "Challenge a common belief or standard industry view.",
        "Contrary to popular belief, multitasking doesn't increase productivity."
    )

    IMAGINE_THIS = (
        "imagine_this",
        "Paint a scenario to engage the reader's imagination and empathy.",
        "Imagine a world where electric cars are the norm, not the exception."
    )

    IF_THEN = (
        "if_then",
        "Show a direct cause-and-effect relationship or a hypothetical value proposition.",
        "If you could reduce email time by 20%, you'd gain back a full day each month."
    )

    QUOTATION = (
        "quotation",
        "Begin with an inspirational or authoritative quote from a recognized figure.",
        "As Steve Jobs once said, Innovation distinguishes between a leader and a follower."
    )

    BENEFIT = (
        "benefit",
        "Directly highlight the key value or transformation the reader will gain.",
        "Learn three simple tips that can boost your conversion rates by up to 40%."
    )

    CURIOSITY = (
        "curiosity",
        "Tease the reader with an incomplete 'loop' or secret that forces them to read more.",
        "The secret to gaining 1,000 Instagram followers lies in an overlooked feature…"
    )

    PROBLEM_SOLVING = (
        "problem_solving",
        "Identify a specific pain point and immediately propose a path to a solution.",
        "Struggling with low organic reach? Our unique SEO strategy can change that."
    )

    FEAR_FACTOR = (
        "fear_factor",
        "Highlight a potential threat, risk, or the cost of inaction.",
        "Ignoring this cybersecurity protocol could cost you more than you think."
    )

    TESTIMONIAL = (
        "testimonial",
        "Use an authentic third-party success story to build immediate trust.",
        "John increased his ROI by 150% in 3 months using our marketing guide."
    )

    CELEBRITY = (
        "celebrity",
        "Leverage the influence and name recognition of a well-known person.",
        "Find out how Elon Musk revolutionized the space industry."
    )

    ANALOGY = (
        "analogy",
        "Use a parallel situation to simplify and explain a complex topic.",
        "Marketing a product is like sowing a seed; it requires the right soil and patience."
    )

    CONTROVERSY = (
        "controversy",
        "Begin with a polarizing or controversial statement to spark debate.",
        "Traditional marketing is dead, and here's why."
    )

    MISCONCEPTION = (
        "misconception",
        "Correct a widely held but false belief to establish authority.",
        "Think all fats are bad for you? Think again."
    )

    PREDICTION = (
        "prediction",
        "Forecast a future trend or inevitable change in the landscape.",
        "In five years, AI will have completely reshaped the entry-level job market."
    )

    PERSONAL_EXPERIENCE = (
        "personal_experience",
        "Share a vulnerable personal anecdote or an 'I was there' moment.",
        "When I first started my business, I made a mistake that nearly cost me everything."
    )

    SHOCK_VALUE = (
        "shock_value",
        "Use a shocking revelation or counter-intuitive truth to stop the scroll.",
        "Only 1% of the world's water is suitable for drinking."
    )

    NEWS = (
        "news",
        "Tie the message to a recent event, update, or trending headline.",
        "Following the latest Google algorithm update, SEO will never be the same."
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
