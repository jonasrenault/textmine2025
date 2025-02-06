from itertools import product

from pydantic import BaseModel
from textmine.entities import Entity, get_entity_types


RELATIONS = {
    "IS_LOCATED_IN": (["ACTOR", "EVENT", "PLACE"], ["PLACE"]),
    "IS_OF_NATIONALITY": (["ACTOR", "PLACE"], ["NATIONALITY"]),
    "CREATED": (["ACTOR"], ["ORGANIZATION"]),
    "HAS_CONTROL_OVER": (["ACTOR"], ["ACTOR", "MATERIEL", "PLACE"]),
    "INITIATED": (["ACTOR"], ["EVENT"]),
    "IS_AT_ODDS_WITH": (["ACTOR"], ["ACTOR"]),
    "IS_COOPERATING_WITH": (["ACTOR"], ["ACTOR"]),
    "IS_IN_CONTACT_WITH": (["ACTOR"], ["ACTOR"]),
    "IS_PART_OF": (["ACTOR"], ["ORGANIZATION"]),
    "DEATHS_NUMBER": (["EVENT"], ["QUANTITY"]),
    "END_DATE": (["EVENT"], ["TIME"]),
    "HAS_CONSEQUENCE": (["EVENT"], ["EVENT"]),
    "INJURED_NUMBER": (["EVENT"], ["QUANTITY"]),
    "START_DATE": (["EVENT"], ["TIME"]),
    "STARTED_IN": (["EVENT"], ["PLACE"]),
    "HAS_COLOR": (["MATERIEL"], ["COLOR"]),
    "HAS_FOR_HEIGHT": (["MATERIEL"], ["HEIGHT"]),
    "HAS_FOR_LENGTH": (["MATERIEL"], ["LENGTH"]),
    "HAS_FOR_WIDTH": (["MATERIEL"], ["WIDTH"]),
    "HAS_QUANTITY": (["MATERIEL"], ["QUANTITY"]),
    "IS_REGISTERED_AS": (["MATERIEL"], ["MATERIAL_REFERENCE"]),
    "WEIGHS": (["MATERIEL"], ["WEIGHT"]),
    "WAS_CREATED_IN": (["ORGANIZATION"], ["TIME"]),
    "WAS_DISSOLVED_IN": (["ORGANIZATION"], ["TIME"]),
    "IS_OF_SIZE": (["ORGANIZATION"], ["QUANTITY"]),
    "OPERATES_IN": (["ORGANIZATION"], ["PLACE"]),
    "DIED_IN": (["PERSON"], ["EVENT"]),
    "HAS_CATEGORY": (["PERSON"], ["CATEGORY"]),
    "HAS_FAMILY_RELATIONSHIP": (["PERSON"], ["PERSON"]),
    "GENDER_FEMALE": (["PERSON"], ["PERSON"]),
    "HAS_FIRST_NAME": (["PERSON"], ["FIRSTNAME"]),
    "HAS_LAST_NAME": (["PERSON"], ["LASTNAME"]),
    "IS_DEAD_ON": (["PERSON"], ["TIME"]),
    "GENDER_MALE": (["PERSON"], ["PERSON"]),
    "RESIDES_IN": (["PERSON"], ["PLACE"]),
    "IS_BORN_ON": (["PERSON"], ["TIME"]),
    "IS_BORN_IN": (["PERSON"], ["PLACE"]),
    "HAS_LONGITUDE": (["PLACE"], ["LONGITUDE"]),
    "HAS_LATITUDE": (["PLACE"], ["LATITUDE"]),
}


class Relation(BaseModel, frozen=True):  # type: ignore
    type: str
    head: Entity
    tail: Entity


def get_possible_relations(head_entity_type: str, tail_entity_type: str) -> set[str]:
    """
    Get the set of possible relations given the head and tail entities' types.

    Args:
        head_entity_type (str): head entity type
        tail_entity_type (str): tail entity type

    Returns:
        set[str]: set of possible relations between the two entities
    """
    head_types = get_entity_types(head_entity_type)
    tail_types = get_entity_types(tail_entity_type)
    relations = set(
        relation
        for relation, (head, tail) in RELATIONS.items()
        if head_types & set(head) and tail_types & set(tail)
    )
    return relations


def get_all_possible_relations(entities: list[Entity]) -> set[Relation]:
    relations = set()
    for head, tail in product(entities, repeat=2):
        if head.id == tail.id:
            if "PERSON" in get_entity_types(head.type):
                relations.add(Relation(type="GENDER_FEMALE", head=head, tail=tail))
                relations.add(Relation(type="GENDER_MALE", head=head, tail=tail))
        else:
            for rel in get_possible_relations(head.type, tail.type):
                relations.add(Relation(type=rel, head=head, tail=tail))
    return relations
