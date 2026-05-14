from src.enums.prompt import DatabasePromptPartEnum


class CallToActionType(DatabasePromptPartEnum):

    ASSESSMENT_ENTRY = (
        "assessment_entry",
        "Encouraging the user to start a diagnostic quiz or interactive test to receive personalized insights.",
        "Take the 1-minute quiz to discover your metabolic age and get your custom plan."
    )

    DIRECT_CONVERSION = (
        "direct_conversion",
        "A high-intent instruction to immediately subscribe, start a trial, or claim a time-bound offer.",
        "Start your 28-day challenge now for just $1 and claim your 80% discount."
    )

    LEARN_MORE = (
        "learn_more",
        "A low-pressure request for the user to explore more information about a specific feature or methodology.",
        "Tap 'Learn More' to see how Somatic exercises can help you release stored stress."
    )

    COMMUNITY_ENGAGEMENT = (
        "community_engagement",
        "Inviting the user to interact with the content or join a group to build social proof and habit loops.",
        "Tag a friend who needs to see this 10-minute routine or join our 100M+ community today."
    )


class CallToActionUrgencyType(DatabasePromptPartEnum):

    SCARCITY = (
        "scarcity",
        "Focuses on the limited quantity of the product or service available.",
        "We only have 5 spots left for this month's cohort, so move fast."
    )

    TIME_BOUND = (
        "time_bound",
        "Emphasizes a fast-approaching deadline or the end of a promotion.",
        "This 20% discount expires at midnight, and it won't be back this year."
    )

    LOSS_AVERSION = (
        "loss_aversion",
        "Highlights what the customer will lose or the cost of delaying their decision.",
        "Every day you wait is another day your competitors are gaining an edge in your market."
    )
    
    IMMEDIATE_BENEFIT = (
        "immediate_benefit",
        "Focuses on how quickly the user can see results if they act right now.",
        "Sign up now and get instant access to the dashboard so you can start optimizing within minutes."
    )
