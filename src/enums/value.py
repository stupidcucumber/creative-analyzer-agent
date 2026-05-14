from src.enums.prompt import DatabasePromptPartEnum


class ValueType(DatabasePromptPartEnum):
    
    TRANSFORMATION_OUTCOME = (
        "transformation_outcome", 
        "Focusing on the tangible results and the 'Future Self.' Highlights physical, mental, or aesthetic changes.", 
        "Achieving a '28-day glow up,' losing weight, or moving from 'always tired' to 'high energy', 'stopping the guilt of emotional eating,' 'healing your inner child,' or reducing anxiety.."
    )

    FRICTIONLESS_EASE = (
        "frictionless_ease", 
        "Emphasizing low effort, convenience, and removing barriers to entry like time, equipment, or location.", 
        "Wall Pilates or Pajama Pilates routines that require 'no gym,' 'no equipment,' and only 10 minutes."
    )

    HYPER_PERSONALIZATION = (
        "hyper_personalization", 
        "The promise of a unique experience tailored specifically to the user's data, body type, or goals.", 
        "Promoting a 'customized 28-day plan' based on quiz results or 'AI-powered' daily adjustments."
    )

    ECONOMIC_ADVANTAGE = (
        "economic_advantage", 
        "Focusing on price accessibility, high value-to-cost ratio, or comparing the app to expensive alternatives.", 
        "Ads highlighting a '$1 trial' or claiming the app is 'cheaper than a personal trainer or gym membership'."
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
