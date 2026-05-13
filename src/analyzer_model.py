from google import genai
from google.genai import types

from typing import TypeVar, Type
import os
import time
from pydantic import BaseModel, ValidationError
from enum import StrEnum


class GeminiModelType(StrEnum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_3_1_FLASH_LITE = "gemini-3.1-flash-lite"
    GEMMA_4_31B = "gemma-4-31b-it"


S = TypeVar("S", bound=BaseModel)
class GeminiAnalyzerModel:

    def __init__(self, model_type: GeminiModelType, retries: int, retry_delay: int, config: types.GenerateContentConfig | None = None) -> None:
        self.genai_client = genai.Client(api_key=os.getenv("GEMINI_API"))
        self.model_type = model_type
        self.generation_config = config

        self.retries = retries
        self.retry_delay = retry_delay

    def structured_generation(self, content: types.Content, structure_class: Type[S]) -> S | None:
        result: S | None = None

        for retry in range(self.retries + 1):

            print("Retry number: ", retry)

            response = self.genai_client.models.generate_content(
                model=str(self.model_type),
                contents=content,
                config=self.generation_config
            )

            if response.text == None:
                print("Failed to generate a response. Trying again.")
                time.sleep(self.retry_delay)
                continue
            
            try:
                result = structure_class.model_validate_json(response.text)
                break

            except ValidationError as e:
                print(f"Could not validate: {response.text}")
                print(f"Error: ", e)
                result = None
                break

        return result