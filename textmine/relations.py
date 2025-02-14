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
    "IS_PART_OF": (["ACTOR"], ["ORGANIZATION", "GROUP_OF_INDIVIDUALS"]),
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

TEMPLATES = {
    "ACTOR_IS_LOCATED_IN": "is {head} located in {tail}?",
    "PLACE_IS_LOCATED_IN": "is {head} located in {tail}?",
    "EVENT_IS_LOCATED_IN": "does the event {head} occur in or on {tail}?",
    "IS_OF_NATIONALITY": "is {head} of {tail} nationaly?",
    "CREATED": "did {head} create {tail}?",
    "HAS_CONTROL_OVER": "does {head} have control over {tail}?",
    "INITIATED": "did {head} initiate {tail}?",
    "IS_AT_ODDS_WITH": "is {head} in conflict with or in clear opposition of {tail}?",
    "IS_COOPERATING_WITH": "is {head} explicitly cooperating or working with {tail}?",
    "IS_IN_CONTACT_WITH": "is {head} clearly stated as being in contact with {tail}?",
    "IS_PART_OF": "is {head} part of {tail}?",
    "DEATHS_NUMBER": "is {tail} the number of casualties for {head}?",
    "INJURED_NUMBER": "is {tail} the number of people injured by {head}?",
    "END_DATE": "is {tail} the end date for {head}?",
    "START_DATE": "is {tail} the start date for {head}?",
    "HAS_CONSEQUENCE": "is {tail} the consequence of {head}?",
    "STARTED_IN": "did {head} start in {tail}?",
    "HAS_COLOR": "does {head} have the color {tail}?",
    "HAS_FOR_HEIGHT": "is {tail} the height of {head}?",
    "HAS_FOR_LENGTH": "is {tail} the length of {head}?",
    "HAS_FOR_WIDTH": "is {tail} the width of {head}?",
    "HAS_QUANTITY": "is {tail} the quantity of {head}?",
    "IS_REGISTERED_AS": "is {tail} the reference of {head}?",
    "WEIGHS": "is {tail} the weight of {head}?",
    "WAS_CREATED_IN": "was {head} created in {head}?",
    "WAS_DISSOLVED_IN": "was {head} dissolved in {head}?",
    "OPERATES_IN": "does {head} operate in {head}?",
    "IS_OF_SIZE": "is {tail} the size of {head}?",
    "DIED_IN": "did {head} die in {tail}?",
    "IS_DEAD_ON": "did {head} die on {tail}?",
    "HAS_CATEGORY": "is {head} a {tail}?",
    "HAS_FAMILY_RELATIONSHIP": "is {head} related to or a member of the same family"
    " as {tail}?",
    "GENDER_FEMALE": "is {head} a woman?",
    "GENDER_MALE": "is {head} a man?",
    "HAS_FIRST_NAME": "is {tail} {head}'s first name?",
    "HAS_LAST_NAME": "is {tail} {head}'s last name?",
    "RESIDES_IN": "does {head} reside in {tail}?",
    "IS_BORN_ON": "is {tail} the date of birth of {head}?",
    "IS_BORN_IN": "is {tail} the place of birth of {head}?",
    "HAS_LONGITUDE": "is {tail} the longitutude of {head}?",
    "HAS_LATITUDE": "is {tail} the latitude of {head}?",
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
    """
    Get the set of all possible relations between all pairs of given entities.

    Args:
        entities (list[Entity]): a list of entities.

    Returns:
        set[Relation]: the set of all possible relations between the entities.
    """
    relations = set()
    for head, tail in product(entities, repeat=2):
        if head.id == tail.id:
            if "PERSON" in get_entity_types(head.type):
                relations.add(Relation(type="GENDER_FEMALE", head=head, tail=tail))
                relations.add(Relation(type="GENDER_MALE", head=head, tail=tail))
        else:
            for rel in get_possible_relations(head.type, tail.type):
                if rel not in ("GENDER_MALE", "GENDER_FEMALE"):
                    relations.add(Relation(type=rel, head=head, tail=tail))
    return relations


def get_template(relation: Relation) -> str:
    key = relation.type
    if relation.type == "IS_LOCATED_IN":
        key = (
            (get_entity_types(relation.head.type) & {"ACTOR", "EVENT", "PLACE"}).pop()
            + "_"
            + relation.type
        )

    return TEMPLATES[key].format(
        head=f'"{relation.head.mention}"', tail=f'"{relation.tail.mention}"'
    )
