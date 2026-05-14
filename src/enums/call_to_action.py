from src.enums.prompt import DatabasePromptPartEnum


class CallToActionType(DatabasePromptPartEnum):

    DIRECT_PURCHASE = (
        "direct_purchase",
        "A clear, friction-free instruction to buy or subscribe immediately.",
        "Click the link below to grab your copy and start today."
    )

    LEAD_GENERATION = (
        "lead_generation",
        "An invitation to exchange contact information for a valuable resource or consultation.",
        "Download our free strategy guide to see how these principles apply to your business."
    )

    ENGAGEMENT = (
        "engagement",
        "Encourages the audience to interact with the content to boost reach and build community.",
        "Drop a comment with your biggest takeaway or share this with someone who needs to hear it."
    )

    LEARN_MORE = (
        "learn_more",
        "A low-pressure request for the reader to explore more information before deciding.",
        "Head over to our blog to see the full breakdown of the data."
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
