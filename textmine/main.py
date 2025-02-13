import json
from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from pydantic import TypeAdapter
from tqdm import tqdm

from textmine.entities import Entity
from textmine.evaluate import Metrics, score
from textmine.inference import TransformersInferenceModel, predict

ROOT_DIR = Path(__file__).parent.parent

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
    ] = None,
):
    # Load evaluation df
    ta = TypeAdapter(list[Entity])
    eval_df = pd.read_csv(input_df)
    eval_df = eval_df.set_index("id")
    eval_df.entities = eval_df.entities.apply(ta.validate_json)
    eval_df.relations = eval_df.relations.apply(json.loads)

    # if text_idx is not None, select row with text_idx
    if text_idx is not None:
        eval_df = eval_df.loc[text_idx]

    # load relation prediction model
    rel_model = TransformersInferenceModel(
        model=model,
        token="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",
        device=device,
    )

    # predict relations for each item in the eval dataframe
    metrics = Metrics()
    ids = []
    pred_relations = []
    for index, row in tqdm(eval_df.iterrows()):
        predictions = predict(rel_model, row.text, row.entities)
        ids.append(index)
        pred_relations.append(
            [
                (relation.head.id, relation.type, relation.tail.id)
                for relation in predictions
            ]
        )
        true_positives, false_positives, false_negatives = score(
            set(row.relations), predictions
        )
        metrics.update_true_positives(true_positives)
        metrics.update_false_positives(false_positives)
        metrics.update_false_negatives(false_negatives)

    pred_df = pd.DataFrame({"id": ids, "relations": pred_relations})
    pred_df.relations = pred_df.relations.apply(lambda rels: json.dumps(rels))
    pred_df.set_index("id")
    eval_df.predictions = pred_df.relations
    eval_df.to_csv("eval_df.csv")
    print(metrics.compute_metrics())


if __name__ == "__main__":
    app()
