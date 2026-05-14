from pydantic import BaseModel, Field

from typing import Optional, get_args, get_origin, Union, Self
from enum import StrEnum
import json
import random
import sqlite3

from src.enums.pacing import AdPacing
from src.enums.value import ValueType
from src.enums.hook_type import HookTypes, HookVisualFormatType
from src.enums.body_logic import BodyLogic
from src.enums.emotional_valence import EmotionalValenceType
from src.enums.call_to_action import CallToActionType
from src.enums.content import ContentType
from src.enums.prompt import DatabasePromptPartEnum



class AgentCharacteristics(BaseModel):

    @classmethod
    def generate_prompt(cls) -> str:

        structure = """
## Explanations of required fields:

{explanations}

## Example of the output:

{examples}
"""

        prompt_sections = []
        
        for field_name, field_info in cls.model_fields.items():
            description = field_info.description or "No description provided."
            section = f"FIELD: {field_name}\nDESCRIPTION: {description}"
            
            field_type = field_info.annotation
            
            # Handle Optional[...] / Union[..., None] types
            if get_origin(field_type) is Optional or type(None) in get_args(field_type):
                # Filter out NoneType to get the actual class
                inner_types = [t for t in get_args(field_type) if t is not type(None)]
                actual_type = inner_types[0] if inner_types else None
            else:
                actual_type = field_type

            if isinstance(actual_type, type) and issubclass(actual_type, DatabasePromptPartEnum):
                enum_details = [member.prompt() for member in actual_type]
                section += f"\nALLOWED VALUES & DEFINITIONS:\n" + json.dumps(enum_details, indent=4)

            prompt_sections.append(section)
        
        field_explanations = "\n\n---\n\n".join(prompt_sections)
        example = cls.example().model_dump_json(indent=4)
        
        return structure.format(explanations=field_explanations, examples=example)
    
    @classmethod
    def example(cls):
        """Generates a random instance of the class for testing or prompting."""
        data = {}
        
        for field_name, field_info in cls.model_fields.items():
            ftype = field_info.annotation
            
            # Handle Optional/Union types to get the core type
            origin = get_origin(ftype)
            if origin is Optional or origin is Union:
                args = get_args(ftype)
                actual_type = next((t for t in args if t is not type(None)), None)
            else:
                actual_type = ftype

            # 1. Handle our custom Enum types
            if isinstance(actual_type, type) and issubclass(actual_type, DatabasePromptPartEnum):
                # Pick a random member from the Enum
                random_member = random.choice(list(actual_type))
                data[field_name] = random_member

            elif isinstance(actual_type, type) and issubclass(actual_type, StrEnum):
                random_enum = random.choice([value for _, value in actual_type.__members__.items()])
                data[field_name] = random_enum

            # 2. Handle standard strings (use the description or a placeholder)
            elif actual_type is str:
                data[field_name] = f"Sample text for {field_name.replace('_', ' ')}"

            # 3. Handle integers
            elif actual_type is int:
                data[field_name] = random.randint(1, 10)

            elif actual_type is bool:
                data[field_name] = random.choice(seq=[True, False])

            # Default to None for unhandled types
            else:
                data[field_name] = None

        return cls(**data)
    
    @classmethod
    def null(cls) -> Self:
        """Returns an instance of the class with every field explicitly set to None."""
        none_data = {field_name: None for field_name in cls.model_fields}
        return cls(**none_data)


class AgentOutputContentHookCharacteristics(AgentCharacteristics):

    content_hook: Optional[str] = Field(
        None, 
        description=(
            "The primary 'scroll-stopper' or 'pattern interrupt' text/concept. "
            "In BetterMe ads, this typically addresses a specific pain point (e.g., 'Somatic exercises for belly fat') "
            "or a curiosity gap designed to halt the user's feed-scrolling."
        )
    )

    content_hook_length_seconds: Optional[int] = Field(
        None, 
        description=(
            "The precise window of the initial hook. For BetterMe's high-retention clips, "
            "this is usually a tight 1-5 second interval where the core value proposition is established."
        )
    )

    content_hook_visual_format: Optional[HookVisualFormatType] = Field(
        None, 
        description=(
            "The aesthetic delivery method of the hook. Evaluates if the ad uses split-screen comparisons, "
            "raw UGC-style footage for relatability, or data-driven graphical overlays."
        )
    )

    content_hook_type: Optional[HookTypes] = Field(
        None, 
        description=(
            "The psychological mechanism of the opener—whether it's a diagnostic question about the user's body, "
            "a counter-intuitive shocking fact, or an immediate before-and-after transformation teaser."
        )
    )

    content_hook_emotional_valence: Optional[EmotionalValenceType] = Field(
        None, 
        description=(
            "The immediate 'vibe' or emotional resonance of the hook. Identifies if the ad starts with "
            "high-tension 'Pain/Agitation' or leans into the instant 'Aspirational Relief' of the product."
        )
    )


class AgentOutputContentValueCharacteristics(AgentCharacteristics):
    
    content_product_value_type: Optional[ValueType] = Field(
        None, 
        description=(
            "The core promise or 'The Why' behind the ad. In the context of BetterMe, "
            "this focuses on the specific outcome (e.g., Transformation) or the "
            "lifestyle fit (e.g., Frictionless Ease/No-Gym) promised to the user."
        )
    )

    content_body_logic_type: Optional[BodyLogic] = Field(
        None, 
        description=(
            "The rhetorical strategy used to build trust and prove the value. "
            "BetterMe frequently uses educational teardowns (explaining cortisol/somatic science) "
            "or social proof (user-led results) to overcome user skepticism."
        )
    )


class AgentOutputContentCTACharacteristics(AgentCharacteristics):

    content_cta: Optional[str] = Field(
        None, 
        description=(
            "The literal directive or command at the end of the video. "
            "BetterMe usually anchors this in urgency or curiosity, such as "
            "'Take the Quiz,' 'Claim my 28-day plan,' or 'Start my $1 trial'."
        )
    )

    content_cta_type: Optional[CallToActionType] = Field(
        None, 
        description=(
            "The strategic classification of the conversion goal. Focuses on whether "
            "the ad drives the user to an interactive diagnostic "
            "or an immediate subscription/trial start."
        )
    )


class AgentOutputContentCharacteristics(
    AgentOutputContentHookCharacteristics, 
    AgentOutputContentValueCharacteristics, 
    AgentOutputContentCTACharacteristics
):
    
    pacing: Optional[AdPacing] = Field(
        None,
        description="The speed at which ad engages with the user."
    )


class AgentOutputPostTextHookCharacteristics(AgentCharacteristics):

    post_hook: Optional[str] = Field(
        None, 
        description=(
            "The 'First Line' of the caption. In BetterMe copy, this is often a "
            "bold statement or a relatable struggle (e.g., 'Stop fighting your body') "
            "designed to make the reader click 'See More'."
        )
    )
    post_hook_type: Optional[HookTypes] = Field(
        None, 
        description=(
            "The rhetorical structure of the text opener. Evaluates if the post "
            "starts with a 'Shocking Fact' about metabolism or a 'Question' "
            "targeting a specific life archetype like 'The Busy Professional'."
        )
    )
    post_hook_emotional_valence: Optional[EmotionalValenceType] = Field(
        None, 
        description=(
            "The emotional entry point of the text. Often starts with 'Pain/Agitation' "
            "(e.g., burnout symptoms) to build empathy before pivoting to the solution."
        )
    )


class AgentOutputPostTextValueCharacteristics(AgentCharacteristics):

    post_product_value_type: Optional[ValueType] = Field(
        None, 
        description=(
            "The promise embedded in the caption body. This usually articulates the "
            "'Frictionless Ease' of the method (e.g., 'Do it in your PJs') or the "
            "mental 'Transformation' the user will undergo."
        )
    )
    post_body_logic_type: Optional[BodyLogic] = Field(
        None, 
        description=(
            "The evidence provided in the text. BetterMe often uses 'Educational Teardowns' "
            "via bullet points to explain how the app solves a specific physiological "
            "or psychological problem (e.g., cortisol regulation)."
        )
    )


class AgentOutputPostTextCTACharacteristics(AgentCharacteristics):

    post_cta: Optional[str] = Field(
        None, 
        description=(
            "The final closing instruction. BetterMe captions usually end with "
            "a high-urgency command or a curiosity-driven link description like "
            "'Click below to find your metabolic age ⬇️'."
        )
    )
    post_cta_type: Optional[CallToActionType] = Field(
        None, 
        description=(
            "The conversion category for the text. Typically leads to an 'Assessment Entry' "
            "(Quiz) or a 'Direct Conversion' for a limited-time trial offer."
        )
    )


class AgentOutputPostTextCharacteristics(
    AgentOutputPostTextHookCharacteristics,
    AgentOutputPostTextValueCharacteristics,
    AgentOutputPostTextCTACharacteristics
):
    pass


class AlgorithmicMetadata(BaseModel):
    published: bool
    content_id: int
    content_type: ContentType
    content_format: str
    product: str | None = None
    date_published: str | None = None
    reach: int | None = None
    post_text: str | None = None


class DatabaseEntry(AlgorithmicMetadata, AgentOutputContentCharacteristics, AgentOutputPostTextCharacteristics):

    def insert_into_table(self, table_name: str, db_path: str = "database.db"):
        # 1. Convert the model to a dictionary, excluding unset values if desired
        data = self.model_dump(exclude_none=True)
        
        if not data:
            raise ValueError("No data present to insert.")

        columns = ", ".join(data.keys())
        # Create placeholders (e.g., :field_1, :field_2) for safe injection
        placeholders = ", ".join([f":{key}" for key in data.keys()])
        
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # 2. Execute using your preferred database driver
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            print(f"Record inserted into {table_name} successfully.")

    @classmethod
    def create_table(cls, table_name: str, db_path: str = "data.sqlite3"):
        
        columns = cls.database_columns()

        column_str = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {column_str});"
        
        with sqlite3.connect(db_path) as conn:
            conn.execute(sql)

    @classmethod
    def database_columns(cls) -> list[str]:
        type_map = {
            str: "TEXT",
            int: "INTEGER",
            bool: "INTEGER",
        }
        
        columns = []
        for name, field in cls.model_fields.items():
            # Get the core type (handling Optional/Union)
            base_type = get_args(field.annotation)[0] if get_origin(field.annotation) is Union else field.annotation
            sql_type = type_map.get(base_type, "TEXT") # Default Enums/others to TEXT
            null_stmt = "NOT NULL" if field.is_required() else ""
            columns.append(f"{name} {sql_type} {null_stmt}")

        return columns
