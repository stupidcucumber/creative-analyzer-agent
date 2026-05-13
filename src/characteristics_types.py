from pydantic import BaseModel, Field

from typing import Optional, get_args, get_origin, Union, Self
import json
import random

from src.enums.hook_type import HookTypes, HookVisualFormatType
from src.enums.emotional_valence import EmotionalValenceType
from src.enums.pov import PointOfViewType
from src.enums.value import ValueType, ProofOfValueType
from src.enums.call_to_action import CallToActionType, CallToActionUrgencyType
from src.enums.content import ContentType
from src.enums.prompt import DatabasePromptPartEnum



class AgentCharacteristics(BaseModel):

    @classmethod
    def generate_prompt(cls) -> str:

        structure = """
# Explanations of required fields:

{explanations}

# Example of the output:

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

            # 2. Handle standard strings (use the description or a placeholder)
            elif actual_type is str:
                data[field_name] = f"Sample text for {field_name.replace('_', ' ')}"

            # 3. Handle integers
            elif actual_type is int:
                data[field_name] = random.randint(1, 10)

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
        description="A short, attention-grabbing text or concept used at the very beginning of the visual content."
    )
    content_hook_length_seconds: Optional[int] = Field(
        None, 
        description="The duration of the hook segment in seconds. Usually between 1-5 seconds."
    )
    content_hook_visual_format: Optional[HookVisualFormatType] = Field(
        None, 
        description="The visual style of the hook."
    )
    content_hook_type: Optional[HookTypes] = Field(
        None, 
        description="The rhetorical strategy of the opening line."
    )
    content_hook_emotional_valence: Optional[EmotionalValenceType] = Field(
        None, 
        description="The intended emotional reaction to the hook."
    )
    content_hook_pov_type: Optional[PointOfViewType] = Field(
        None, 
        description="The perspective used in the hook."
    )


class AgentOutputContentValueCharacteristics(AgentCharacteristics):

    content_barrier_reduction: Optional[str] = Field(
        None, 
        description="Text or visual cue that lowers the barrier to entry or addresses a common objection."
    )
    content_value_type: Optional[ValueType] = Field(
        None, 
        description="The primary value proposition offered."
    )
    content_proof_of_value_type: Optional[ProofOfValueType] = Field(
        None, 
        description="The method used to prove the claim."
    )
    content_value_pov_type: Optional[PointOfViewType] = Field(
        None, 
        description="The perspective from which the value is delivered."
    )


class AgentOutputContentCTACharacteristics(AgentCharacteristics):

    content_cta: Optional[str] = Field(
        None, 
        description="The specific directive given to the viewer at the end of the content."
    )
    content_cta_type: Optional[CallToActionType] = Field(
        None, 
        description="The category of the action."
    )
    content_cta_urgency_type: Optional[CallToActionUrgencyType] = Field(
        None, 
        description="The level of time-sensitivity or scarcity attached to the CTA."
    )


class AgentOutputContentCharacteristics(
    AgentOutputContentHookCharacteristics, 
    AgentOutputContentValueCharacteristics, 
    AgentOutputContentCTACharacteristics
):
    pass


class AgentOutputPostTextHookCharacteristics(AgentCharacteristics):

    post_hook: Optional[str] = Field(
        None, 
        description="The opening line or sentence of the post designed to stop the scroll and entice further reading."
    )
    post_hook_type: Optional[HookTypes] = Field(
        None, 
        description="The rhetorical strategy of the opening line."
    )
    post_hook_emotional_valence: Optional[EmotionalValenceType] = Field(
        None, 
        description="The intended emotional reaction to the hook."
    )


class AgentOutputPostTextValueCharacteristics(AgentCharacteristics):

    post_barrier_reduction: Optional[str] = Field(
        None, 
        description="Text within the body that simplifies complex ideas or removes friction/doubt for the reader."
    )
    post_value_type: Optional[ValueType] = Field(
        None, 
        description="The core utility of the text body."
    )
    post_proof_of_value_type: Optional[ProofOfValueType] = Field(
        None, 
        description="How the text validates its claims."
    )


class AgentOutputPostTextCTACharacteristics(AgentCharacteristics):

    post_cta: Optional[str] = Field(
        None, 
        description="The final sentence or phrase that instructs the reader on exactly what to do next."
    )
    post_cta_type: Optional[CallToActionType] = Field(
        None, 
        description="The specific action requested."
    )
    post_cta_urgency_type: Optional[CallToActionUrgencyType] = Field(
        None, 
        description="The framing of the timeline."
    )


class AgentOutputPostTextCharacteristics(
    AgentOutputPostTextHookCharacteristics,
    AgentOutputPostTextValueCharacteristics,
    AgentOutputPostTextCTACharacteristics
):
    pass


class AlgorithmicMetadata(BaseModel):
    published: bool
    content_type: ContentType
    content_format: str
    product: str | None = None
    date_published: str | None = None
    reach: int | None = None
    post_text: str | None = None


class DatabaseEntry(AlgorithmicMetadata, AgentOutputContentCharacteristics, AgentOutputPostTextCharacteristics):
    pass
