import pathlib
import pandas as pd
import math
from src.characteristics_types import (
    AgentOutputContentCharacteristics,
    AgentOutputPostTextCharacteristics,
    AlgorithmicMetadata,
    DatabaseEntry,
    ContentType
)
from google.genai import types
import cv2
from src.analyzer_model import GeminiAnalyzerModel
from src.system_prompt import SYSTEM_PROMPT


def get_aspect_ratio(width: int, height: int) -> str:
    """Calculates the simplified aspect ratio for given dimensions.
    
    Parameters
    ----------
    width : int 
        The width of the image or video.
    height : int
        The height of the image or video.
        
    Returns
    -------
    str
        The aspect ratio in "W:H" format.
    """
    if height == 0:
        return "Undefined"
    gcd = math.gcd(width, height)
    simplified_width = width // gcd
    simplified_height = height // gcd
    
    return f"{simplified_width}:{simplified_height}"


class Analyzer:

    def __init__(
        self, 
        database: str,
        creatives: list[pathlib.Path], 
        additional_metadata: pd.DataFrame, 
        analyzer_model: GeminiAnalyzerModel,
        prompt: str | None = None
    ) -> None:
        self.database = database

        self.creatives = creatives
        self.additional_metadata = additional_metadata
        self.analyzer_model = analyzer_model

        self.prompt = prompt if prompt else SYSTEM_PROMPT

    def _analyze_content(self, content_path: pathlib.Path) -> AgentOutputContentCharacteristics | None:

        if content_path.suffix == ".mp4":
            mime_type = "video/mp4"

        else:
            mime_type = "image/jpeg"

        content = types.Content(
            parts=[
                types.Part(
                    inline_data=types.Blob(data=content_path.read_bytes(), mime_type=mime_type)
                ),
                types.Part(text=self.prompt + AgentOutputContentCharacteristics.generate_prompt())
            ]
        )
        
        return self.analyzer_model.structured_generation(content=content, structure_class=AgentOutputContentCharacteristics)

    def _analyze_post(self, post: str) -> AgentOutputPostTextCharacteristics | None:

        content = types.Content(
            parts=[
                types.Part(
                    text=(
                        self.prompt + 
                        AgentOutputPostTextCharacteristics.generate_prompt() +
                        """\n\n--- ANALYZE POST BELOW ---\n""" +
                        post
                    )
                ),
            ]
        )
        
        return self.analyzer_model.structured_generation(content=content, structure_class=AgentOutputPostTextCharacteristics)
    
    def _extract_content_format(self, content_path: pathlib.Path) -> str:

        if content_path.suffix == ".mp4":
            video = cv2.VideoCapture(content_path)
            retrieved, frame = video.read()

            if retrieved:
                height, width, _ = frame.shape
            
            else:
                video.release()
                raise ValueError("Could not retrieve frame from the video.")
            
        else:
            image = cv2.imread(content_path)

            if image is not None:
                height, width, _ = image.shape
            
            else: 
                raise ValueError("Could not retrieve shape from the image.")

        return get_aspect_ratio(width=width, height=height)

    def _extract_algorithmic_metadata(self, index: int, creative_path: pathlib.Path, published: bool = True) -> AlgorithmicMetadata:

        if published:
            item = self.additional_metadata.loc[index]
            return AlgorithmicMetadata(
            published=published,
            date_published=item["ad_creation_time"],
            reach=item["reach"],
            post_text=item["ad_text"],
            product=item["product"],
            content_type=(
                ContentType.IMAGE if creative_path.suffix == ".jpg" else ContentType.VIDEO
            ),
            content_format=self._extract_content_format(content_path=creative_path),
            content_id=index
        )

        return AlgorithmicMetadata(
            published=published,
            content_type=(
                ContentType.IMAGE if creative_path.suffix == ".jpg" else ContentType.VIDEO
            ),
            content_format=self._extract_content_format(content_path=creative_path),
            content_id=index
        )

    def analyze(self, evaluate: bool = False) -> tuple[list[DatabaseEntry], list[int]]:

        entries = []
        failed_entries = []
        for creative in self.creatives:

            creative_id = int(creative.stem)
            print("Analyzing creative: ", creative)

            print("\tAnalyzing post.")
            if creative_id in self.additional_metadata.index:
                agent_output_post_characteristics = self._analyze_post(post=self.additional_metadata.loc[creative_id, "ad_text"])
                
            else:
                print(f"\t{creative} did not have enough data for adding to the database. Post analyzation will be skipped.")
                agent_output_post_characteristics = AgentOutputPostTextCharacteristics.null()

            print("\tAnalyzing content.")
            agent_output_content_characteristics = self._analyze_content(content_path=creative)

            if (agent_output_content_characteristics is None or agent_output_post_characteristics is None):
                print(f"Post with id={creative_id} could not be processed.")
                failed_entries.append(creative_id)
                continue

            print("\tExtracting metadata.")
            algorithmic_metadata = self._extract_algorithmic_metadata(
                creative_path=creative, 
                published=creative_id in self.additional_metadata.index,
                index=creative_id
            )

            entry = DatabaseEntry(
                **agent_output_content_characteristics.model_dump(),
                **agent_output_post_characteristics.model_dump(),
                **algorithmic_metadata.model_dump()
            ) # pyright: ignore

            if not evaluate:
                entry.insert_into_table("marketing", db_path=self.database)

            entries.append(entry)

        return entries, failed_entries
