from abc import ABC, abstractmethod

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

from textmine.entities import Entity
from textmine.relations import Relation, get_all_possible_relations, get_template


class RelationInferenceModel(ABC):
    """
    Abstract base class for relation inference models.
    """

    @abstractmethod
    def predict(self, text: str, relation: Relation) -> tuple[str, bool]:
        pass


class TransformersInferenceModel(RelationInferenceModel):
    """
    Predict whether a relation is present in the given text.
    """

    def __init__(
        self,
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        token: str | None = None,
        device: str | torch.device | None = None,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model, token=token)
        self.model = AutoModelForCausalLM.from_pretrained(model, token=token)
        if isinstance(device, str):
            device = torch.device(device)
        self.model = self.model.to(device)
        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

    def predict(self, text, relation):
        template = get_template(relation)
        prompt = (
            f"In the following text in french, {template} "
            f'Answer with "yes" or "no" only.\n\ntext: {text}'
        )
        conversation = [{"role": "user", "content": prompt}]
        formatted_prompt = self.tokenizer.apply_chat_template(
            conversation, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(
            self.model.device
        )

        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        stop_words = ["Yes", "No", "Oui", "Non"]
        stop_token_ids = [
            token_id
            for stop_word in stop_words
            for token_id in self.tokenizer(
                stop_word, return_tensors="pt", add_special_tokens=False
            )["input_ids"][0]
        ]

        # https://github.com/AdrienGuille/TextMine2025/tree/main sets do_sample to False
        # and num_beams to 1. Not sure it's the best params. Maybe set do_sample to True
        # and set temperature.
        self.model.generate(
            inputs["input_ids"],
            streamer=streamer,
            max_new_tokens=10,
            num_beams=1,
            do_sample=False,
            # temperature=0.5,
            eos_token_id=self.terminators + stop_token_ids,
            pad_token_id=self.tokenizer.eos_token_id,
            attention_mask=inputs["attention_mask"],
        )

        outputs = []
        for text in streamer:
            outputs.append(text.lower())
        output = "".join(outputs)
        return output, "yes" in output or "oui" in output


def predict(
    model: RelationInferenceModel, text: str, entities: list[Entity]
) -> set[Relation]:
    """
    Use RelationInference model to make predictions on possible relations
    between entities present in given text.

    Args:
        model (RelationInferenceModel): the inference model.
        text (str): the text.
        entities (list[Entity]): the list of entities in the text.

    Returns:
        set[Relation]: set of predicted relations.
    """
    predictions = set(
        relation
        for relation in get_all_possible_relations(entities)
        if model.predict(text, relation)[1]
    )
    return predictions
