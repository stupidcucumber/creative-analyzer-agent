from src.enums.prompt import DatabasePromptPartEnum


class PointOfViewType(DatabasePromptPartEnum):

    FIRST = (
        "first_person",
        "The narrator speaks from their own perspective using pronouns like I, me, and my to share personal insights or experiences.",
        "I've spent years perfecting this strategy because I wanted to see real results for my own business."
    )

    SECOND = (
        "second_person",
        "The content speaks directly to the audience using you and your, making the reader the protagonist of the narrative.",
        "You deserve a workflow that works as hard as you do, so you can finally focus on the tasks you actually enjoy."
    )

    THIRD = (
        "third_person",
        "The narrator acts as an objective observer, referring to individuals or groups by name or pronouns like he, she, they, and it.",
        "Industry leaders are beginning to realize that efficiency isn't just about speed; it's about how they manage their most valuable assets."
    )
