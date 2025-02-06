from textmine.relations import get_possible_relations


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
