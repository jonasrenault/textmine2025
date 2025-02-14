from textmine.entities import Entity, Mention
from textmine.relations import (
    Relation,
    get_all_possible_relations,
    get_possible_relations,
    get_template,
)


def test_get_possible_relations():
    assert get_possible_relations("MATERIEL", "COLOR") == {"HAS_COLOR"}

    # ACTOR, EVENT RELATIONS
    assert get_possible_relations(
        "GOVERNMENT_ORGANIZATION", "AGITATING_TROUBLE_MAKING"
    ) == {"INITIATED"}

    # ACTOR, ACTOR RELATIONS
    assert get_possible_relations("GOVERNMENT_ORGANIZATION", "CIVILIAN") == {
        "IS_IN_CONTACT_WITH",
        "IS_AT_ODDS_WITH",
        "HAS_CONTROL_OVER",
        "IS_COOPERATING_WITH",
    }

    # ACTOR, PLACE RELATIONS
    assert get_possible_relations("PERSON", "PLACE") == {
        "HAS_CONTROL_OVER",
        "IS_LOCATED_IN",
        "RESIDES_IN",
        "IS_BORN_IN",
    }

    assert get_possible_relations("GOVERNMENT_ORGANIZATION", "PLACE") == {
        "HAS_CONTROL_OVER",
        "IS_LOCATED_IN",
        "OPERATES_IN",
    }

    # PERSON, PERSON RELATIONS
    assert get_possible_relations("PERSON", "PERSON") == {
        "GENDER_MALE",
        "IS_IN_CONTACT_WITH",
        "GENDER_FEMALE",
        "IS_AT_ODDS_WITH",
        "IS_COOPERATING_WITH",
        "HAS_CONTROL_OVER",
        "HAS_FAMILY_RELATIONSHIP",
    }


def test_get_all_possible_relations():
    entities = [
        Entity(id=0, type="FIRE", mentions=[Mention(value="brûlé", start=510, end=515)]),
        Entity(id=1, type="PLACE", mentions=[Mention(value="Lyon", start=64, end=68)]),
    ]
    relations = set(
        (
            Relation(type="IS_LOCATED_IN", head=entities[0], tail=entities[1]),
            Relation(type="STARTED_IN", head=entities[0], tail=entities[1]),
        )
    )
    assert get_all_possible_relations(entities) == relations

    entities = [
        Entity(
            id=8,
            type="CIVILIAN",
            mentions=[
                Mention(value="Arthur Abert", start=404, end=416),
            ],
        ),
        Entity(
            id=1,
            type="TERRORIST_OR_CRIMINAL",
            mentions=[
                Mention(value="Lino Abert", start=49, end=59),
            ],
        ),
    ]
    relations = set(
        (
            Relation(type="GENDER_MALE", head=entities[0], tail=entities[0]),
            Relation(type="GENDER_MALE", head=entities[1], tail=entities[1]),
            Relation(type="GENDER_FEMALE", head=entities[0], tail=entities[0]),
            Relation(type="GENDER_FEMALE", head=entities[1], tail=entities[1]),
            Relation(type="IS_AT_ODDS_WITH", head=entities[0], tail=entities[1]),
            Relation(type="IS_AT_ODDS_WITH", head=entities[1], tail=entities[0]),
            Relation(type="IS_IN_CONTACT_WITH", head=entities[0], tail=entities[1]),
            Relation(type="IS_IN_CONTACT_WITH", head=entities[1], tail=entities[0]),
            Relation(type="HAS_CONTROL_OVER", head=entities[0], tail=entities[1]),
            Relation(type="HAS_CONTROL_OVER", head=entities[1], tail=entities[0]),
            Relation(type="IS_COOPERATING_WITH", head=entities[0], tail=entities[1]),
            Relation(type="IS_COOPERATING_WITH", head=entities[1], tail=entities[0]),
            Relation(type="HAS_FAMILY_RELATIONSHIP", head=entities[0], tail=entities[1]),
            Relation(type="HAS_FAMILY_RELATIONSHIP", head=entities[1], tail=entities[0]),
        )
    )
    assert get_all_possible_relations(entities) == relations


def test_get_template():
    relation = Relation(
        type="IS_LOCATED_IN",
        head=Entity(
            id=8,
            type="CIVILIAN",
            mentions=[
                Mention(value="Arthur Abert", start=404, end=416),
            ],
        ),
        tail=Entity(
            id=1, type="PLACE", mentions=[Mention(value="Lyon", start=64, end=68)]
        ),
    )
    assert get_template(relation) == 'is "Arthur Abert" located in "Lyon"?'

    relation = Relation(
        type="GENDER_MALE",
        head=Entity(
            id=8,
            type="CIVILIAN",
            mentions=[
                Mention(value="Arthur Abert", start=404, end=416),
            ],
        ),
        tail=Entity(
            id=8,
            type="CIVILIAN",
            mentions=[
                Mention(value="Arthur Abert", start=404, end=416),
            ],
        ),
    )
    assert get_template(relation) == 'is "Arthur Abert" a man?'
