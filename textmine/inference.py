from abc import ABC, abstractmethod

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

from textmine.entities import Entity, Mention
from textmine.relations import Relation, get_template


class RelationInferenceModel(ABC):
    """
    Abstract base class for relation inference models.
    """

    @abstractmethod
    def predict(self, text: str, relation: Relation) -> bool:
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
        input_ids = self.tokenizer.apply_chat_template(
            conversation, return_tensors="pt"
        ).to(self.model.device)

        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        stop_words = ["Yes", "No"]
        stop_token_ids = [
            self.tokenizer(x, return_tensors="pt", add_special_tokens=False)["input_ids"]
            for x in stop_words
        ]

        self.model.generate(
            input_ids,
            streamer=streamer,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.5,
            eos_token_id=self.terminators + stop_token_ids,
        )

        outputs = []
        for text in streamer:
            outputs.append(text)
        return "".join(outputs)


if __name__ == "__main__":
    model = TransformersInferenceModel(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        token="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",
        device="cuda:0",
    )
    # model = DeepSeekInferenceModel(device="cuda:0")
    text = 'Un important incendie a fait des ravages dans une forêt en Autriche. Le départ de feu a été provoqué par le mégot d’une cigarette mal éteinte, jetée par un conducteur de poids lourd. Il aura fallu plusieurs bombardiers d’eau ainsi que des efforts au sol pour parvenir à éteindre le brasier. L\'action a été coordonnée par le Major Duverney. Les pompiers se sont équipés de masques sur le visage et de bouteilles d’air comprimé, ainsi que de combinaisons ignifugées pour combattre le feu au sol. L’ONG "ECO+" a déploré cet évènement qu’elle qualifie de criminel car, dans la forêt en partie incendiée, se trouvaient des espèces animales protégées.'  # noqa: E501

    relation = Relation(
        type="HAS_CATEGORY",
        head=Entity(
            id=5,
            type="MILITARY",
            mentions=[Mention(value="Duverney", start=330, end=338)],
        ),
        tail=Entity(
            id=14,
            type="CATEGORY",
            mentions=[Mention(value="Major", start=324, end=329)],
        ),
    )
    output = model.predict(text, relation)
    print(output)
