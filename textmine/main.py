import json
import logging
from pathlib import Path
from typing import Annotated

import typer
from pydantic.json import pydantic_encoder
from tqdm import tqdm

from textmine.evaluate import Metrics, score
from textmine.inference import TransformersInferenceModel
from textmine.relations import get_all_possible_relations, get_template
from textmine.utils import read_dataframe

ROOT_DIR = Path(__file__).parent.parent
LOGGER = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def predict(
    text_idx: Annotated[
        int, typer.Argument(help="Index of row in input_df to evaluate.")
    ],
    rel_type: Annotated[str, typer.Argument(help="Type of relation to predict.")],
    head: Annotated[int | None, typer.Option(help="Head entity id.")] = None,
    tail: Annotated[int | None, typer.Option(help="Tail entity id.")] = None,
    input: Annotated[
        Path,
        typer.Option(
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
    model: Annotated[
        str, typer.Option(help="Transformers model to use for relation prediction.")
    ] = "mistralai/Mistral-7B-Instruct-v0.3",
    device: Annotated[
        str | None, typer.Option(help="Device for relation prediction.")
    ] = "cuda:0",
):
    # Load row from dataframe
    df = read_dataframe(input)
    row = df.loc[text_idx]

    # load relation prediction model
    rel_model = TransformersInferenceModel(
        model=model,
        token="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",
        device=device,
    )

    # get all possible relations
    relations = [
        relation
        for relation in get_all_possible_relations(row.entities)
        if relation.type == rel_type
    ]
    if head is not None:
        relations = [relation for relation in relations if relation.head.id == head]
    if tail is not None:
        relations = [relation for relation in relations if relation.tail.id == tail]

    if not relations:
        print(
            f"Relation ({head if head is not None else '*'}, {rel_type}, "
            f"{tail if tail is not None else '*'}) does not exist for text {text_idx}"
        )
        return

    relation = relations[0]
    template = get_template(relation)
    prompt = (
        f"In the following text in french, {template} "
        f'Answer with "yes" or "no" only.\n\ntext: {row.text}'
    )
    print(f"Predicting relation {relation}")
    print(f"With prompt:\n{prompt}")
    prediction, valid = rel_model.predict(row.text, relation)
    print(f"Answer: {prediction} ({valid})")


@app.command()
def evaluate(
    input: Annotated[
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
    eval_df = read_dataframe(input)

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
            if rel_model.predict(row.text, relation)[1]
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
    eval_df.to_csv(input)


if __name__ == "__main__":
    app()
