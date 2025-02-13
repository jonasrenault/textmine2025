import json
import logging
from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder
from tqdm import tqdm

from textmine.entities import Entity
from textmine.evaluate import Metrics, score
from textmine.inference import TransformersInferenceModel
from textmine.relations import get_all_possible_relations

ROOT_DIR = Path(__file__).parent.parent
LOGGER = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def evaluate(
    input_df: Annotated[
        Path,
        typer.Argument(
            help=(
                "Path to input evaluation dataframe with text, entities and "
                "relations columns."
            ),
            exists=True,
            file_okay=True,
            readable=True,
        ),
    ] = ROOT_DIR
    / "resources/train.csv",
    text_idx: Annotated[
        int | None, typer.Option(help="Index of row in input_df to evaluate.")
    ] = None,
    model: Annotated[
        str, typer.Option(help="Transformers model to use for relation prediction.")
    ] = "mistralai/Mistral-7B-Instruct-v0.3",
    device: Annotated[
        str | None, typer.Option(help="Device for relation prediction.")
    ] = "cuda:0",
):
    """
    Run relation prediction on input_df. If text_idx is given, only run predictions
    on specified rows.

    Args:
        input_df (Path, optional): evaluation dataframe.
            Defaults to ROOT_DIR/"resources/train.csv".
        text_idx (int | None, optional): optional index of specific row to evaluate.
            Defaults to None.
        model (str, optional): relation inference model name.
            Defaults to "mistralai/Mistral-7B-Instruct-v0.3".
        device (str | None, optional): device for relation prediction.
            Defaults to "cuda:0".
    """
    # Load evaluation df
    ta = TypeAdapter(list[Entity])
    eval_df = pd.read_csv(input_df)
    eval_df = eval_df.set_index("id")
    eval_df.entities = eval_df.entities.apply(ta.validate_json)
    eval_df.relations = eval_df.relations.apply(json.loads)
    if "predictions" not in eval_df.columns:
        eval_df["predictions"] = pd.Series(dtype="object")
    else:
        eval_df.predictions = eval_df.predictions.apply(
            lambda pred: json.loads(pred) if pd.notna(pred) else pred
        )

    # load relation prediction model
    rel_model = TransformersInferenceModel(
        model=model,
        token="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",
        device=device,
    )

    # if text_idx is not None, select row with text_idx
    rows = eval_df
    if text_idx is not None:
        rows = eval_df.loc[[text_idx]]
    print(f"Running predictions on {rows.shape[0]} rows.")

    # predict relations for each item in the eval dataframe
    metrics = Metrics()
    for index, row in tqdm(rows.iterrows()):
        relations = get_all_possible_relations(row.entities)
        print(
            f"Running predictions for row {index} with "
            f"{len(relations)} possible relations."
        )
        predictions = set(
            relation
            for relation in tqdm(relations)
            if rel_model.predict(row.text, relation)
        )
        eval_df.at[index, "predictions"] = [
            (relation.head.id, relation.type, relation.tail.id)
            for relation in predictions
        ]
        true_positives, false_positives, false_negatives = score(
            set(tuple(relation) for relation in row.relations), predictions
        )
        metrics.update_true_positives(true_positives)
        metrics.update_false_positives(false_positives)
        metrics.update_false_negatives(false_negatives)

    # print eval_df with predictions
    print(eval_df)
    # print metrics
    print(metrics.compute_metrics())

    # save df with predictions
    eval_df.predictions = eval_df.predictions.apply(lambda rels: json.dumps(rels))
    eval_df.relations = eval_df.relations.apply(lambda rels: json.dumps(rels))
    eval_df.entities = eval_df.entities.apply(
        lambda ents: json.dumps(ents, default=pydantic_encoder)
    )
    eval_df.to_csv(input_df)


if __name__ == "__main__":
    app()
