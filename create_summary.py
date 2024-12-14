from os import getenv
from pathlib import Path

import typer
from dotenv import load_dotenv
from spacy_llm.util import assemble
from typing_extensions import Annotated


def create_summary(
    text_file: Annotated[
        Path,
        typer.Argument(
            help="Text file that should get summarized.", show_default=False
        ),
    ],
    config_file: Annotated[
        Path,
        typer.Argument(
            help="SpaCy config file describing LLM pipeline.", show_default=False
        ),
    ],
):
    """
    Script to
    1. read a text from a text file
    2. create a summary using an LLM via spacy and OpenWebUI
    3. write that summary back to a text file.
    """
    load_dotenv()

    if not getenv("OPENWEBUI_URL", None):
        print("OpenWebUI URL missing in environment variables.")
        raise typer.Abort()
    if not getenv("OPENWEBUI_API_KEY"):
        print("OpenWebUI API_KEY missing in environment variables.")
        raise typer.Abort()
    if not text_file.exists() or not text_file.is_file():
        print(f"Text file {text_file} does not exit.")
        raise typer.Abort()
    if not config_file.exists():
        print(f"Config file {config_file} does not exit.")
        raise typer.Abort()

    nlp = assemble(
        config_file,
        overrides={
            "openwebui.url": getenv("OPENWEBUI_URL"),
            "openwebui.api_key": getenv("OPENWEBUI_API_KEY"),
        },
    )

    doc = nlp(text_file.read_text(encoding="utf-8"))
    text_file.with_suffix(".summary.txt").write_text(doc._.summary)


if __name__ == "__main__":
    typer.run(create_summary)
