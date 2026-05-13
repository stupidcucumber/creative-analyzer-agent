from src.enums.prompt import DatabasePromptPartEnum


class ValueType(DatabasePromptPartEnum):
    
    NEWNESS = (
        "newness", 
        "Creating new value propositions and constantly innovating to offer something unique.", 
        "Innovation Managers seeking new technologies, methodologies, or products."
    )

    PERFORMANCE = (
        "performance", 
        "Improving speed, efficiency, or functionality of products or services.", 
        "A software company highlighting how their product increases productivity."
    )

    PERSONALIZATION = (
        "personalization", 
        "Tailoring products or services to fit specific customer needs and unique experiences.", 
        "Nike providing customization options where customers design their own shoes."
    )

    GETTING_JOB_DONE = (
        "getting_job_done", 
        "Helping customers perform specific tasks efficiently and without much effort.", 
        "Rolls Royce taking care of aircraft engine monitoring and maintenance."
    )

    DESIGN = (
        "design", 
        "Emphasizing aesthetics and visual appeal for customers who value well-designed offerings.", 
        "Bang & Olufsen's elegant and stylish audio designs."
    )

    STATUS = (
        "brand_status", 
        "Aligning with customer aspirations and identity, or signaling wealth and success.", 
        "Wearing luxury brands like Rolex or choosing sustainable brands to reflect consciousness."
    )

    PRICE = (
        "price", 
        "Offering products at a lower price point to attract price-sensitive customers.", 
        "Discount retailers or budget airlines."
    )

    COST_REDUCTION = (
        "cost_reduction", 
        "Focusing on the overall cost-effectiveness and lowering operational costs for the customer.", 
        "Medical equipment that reduces operational overhead for healthcare providers."
    )

    RISK_REDUCTION = (
        "risk_reduction", 
        "Mitigating risks and increasing certainty associated with using a product or service.", 
        "Insurance apps that discourage phone use while driving to reduce accident risk."
    )

    ACCESSIBILITY = (
        "accessibility", 
        "Providing products or services to customers who previously lacked access.", 
        "AliExpress enabling customers to access a vast range of global products conveniently."
    )

    CONVENIENCE = (
        "convenience", 
        "Focusing on usability and intuitive experiences to address complexity pain points.", 
        "Apple's iPhone revolutionizing the industry with a user-friendly interface."
    )


class ProofOfValueType(DatabasePromptPartEnum):

    DEMONSTRATION = (
        "demonstration",
        "Showing the product or service in action to prove its capabilities and ease of use.",
        "A live screen recording of a software feature or a 'stress test' video showing a material's durability."
    )

    SOCIAL_PROOF = (
        "social_proof",
        "Leveraging the experiences of existing customers to build trust and validate claims.",
        "Customer testimonials, case studies, star ratings, or logos of well-known companies currently using the solution."
    )

    AUTHORITY_CREDENTIALS = (
        "authority_credentials",
        "Using third-party validation, certifications, or professional expertise to establish credibility.",
        "Industry awards, ISO certifications, endorsements from recognized experts, or years of specialized experience in the field."
    )

    BEFORE_VS_AFTER = (
        "before_vs_after",
        "Highlighting the tangible transformation or improvement a customer experiences after using the solution.",
        "A comparison chart showing a 40% reduction in costs or a visual side-by-side of a workflow before and after automation."
    )
