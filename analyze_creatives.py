import pathlib
import json
import pandas as pd
from google.genai import types
from argparse import ArgumentParser, Namespace
from src.analyzer import Analyzer
from src.analyzer_model import GeminiAnalyzerModel, GeminiModelType


def parse_arguments() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "--prompt", type=pathlib.Path, help="System Prompt to pass to the model."
    )

    parser.add_argument(
        "--objects", type=pathlib.Path, help="Objects to analyze with LLM using provided prompts."
    )

    parser.add_argument(
        "--additional-metadata", type=pathlib.Path, help="Path to the CSV that contains additional metadata from Facebook Ads API."
    )

    parser.add_argument(
        "--evaluate", 
        action="store_true", 
        help="""Whether this run is evaluation or testing? If it is evaluation the best prompt 
        will be chosen from the database, and "prompt" argument will be ignored.
        
        During evaluation run:
        - Analyzed entries are loaded into the database.
        - No prompt is saved.

        During not evaluation run:
        - Prompt is stored in the `prompts` table along with calculated metrics.
        - No entries is being loaded into the database, only temporary file is created with run results.

        Requires "--golden-set" to be passed!
        """
    )

    return parser.parse_args()


def load_objects_to_parse(file: pathlib.Path) -> list[pathlib.Path]:
    return [pathlib.Path(file) for file in json.loads(file.read_text())]


def load_prompt(file: pathlib.Path) -> str:
    return file.read_text()


if __name__ == "__main__":

    args = parse_arguments()
    
    objects_to_process = load_objects_to_parse(args.objects)

    analyzer = Analyzer(
        database="data.sqlite3",
        creatives=objects_to_process,
        additional_metadata=pd.read_csv(args.additional_metadata, index_col=0),
        analyzer_model=GeminiAnalyzerModel(
            model_type=GeminiModelType.GEMINI_2_5_FLASH_LITE,
            retries=3,
            retry_delay=2,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                ]
            )
        )
    )

    successfull_entities, failed_entities = analyzer.analyze(evaluate=args.evaluate)

    with open("successfull_entities.json", "w") as f:
        json.dump([entity.model_dump() for entity in successfull_entities], f, indent=4)

    with open("failed_entities.json", "w") as f:
        json.dump(failed_entities, f, indent=4)
