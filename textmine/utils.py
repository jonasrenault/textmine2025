import json
from pathlib import Path

import pandas as pd
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder

from textmine.entities import Entity


def read_dataframe(input: Path) -> pd.DataFrame:
    # Load evaluation df
    ta = TypeAdapter(list[Entity])
    df = pd.read_csv(input)
    df = df.set_index("id")
    df.entities = df.entities.apply(ta.validate_json)
    if "relations" not in df.columns:
        df["relations"] = pd.Series(dtype="object")
    else:
        df.relations = df.relations.apply(json.loads)
    if "predictions" not in df.columns:
        df["predictions"] = pd.Series(dtype="object")
    else:
        df.predictions = df.predictions.apply(
            lambda pred: json.loads(pred) if pd.notna(pred) else pred
        )

    return df


def save_dataframe(df: pd.DataFrame, output: Path):
    # save df with predictions
    df.predictions = df.predictions.apply(lambda rels: json.dumps(rels))
    df.relations = df.relations.apply(lambda rels: json.dumps(rels))
    df.entities = df.entities.apply(
        lambda ents: json.dumps(ents, default=pydantic_encoder)
    )
    df.to_csv(output)
