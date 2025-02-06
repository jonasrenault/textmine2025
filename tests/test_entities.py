from textmine.entities import get_entity_types


def test_get_parents():
    assert get_entity_types("ACCIDENT") == {"ACCIDENT", "EVENT", "ENTITY"}
    assert get_entity_types("TRAFFICKING") == {
        "TRAFFICKING",
        "CRIMINAL_EVENT",
        "EVENT",
        "ENTITY",
    }
    assert get_entity_types("RIOT") == {
        "RIOT",
        "CIVIL_UNREST",
        "EVENT",
        "ENTITY",
    }
    assert get_entity_types("INTERGOVERNMENTAL_ORGANISATION") == {
        "INTERGOVERNMENTAL_ORGANISATION",
        "ORGANIZATION",
        "ACTOR",
        "ENTITY",
    }
    assert get_entity_types("NON_MILITARY_GOVERNMENT_ORGANISATION") == {
        "NON_MILITARY_GOVERNMENT_ORGANISATION",
        "GOVERNMENT_ORGANIZATION",
        "ORGANIZATION",
        "ACTOR",
        "ENTITY",
    }
    assert get_entity_types("QUANTITY_EXACT") == {
        "QUANTITY_EXACT",
        "QUANTITY",
        "ATTRIBUTE",
    }
    assert get_entity_types("LATITUDE") == {
        "LATITUDE",
        "ATTRIBUTE",
    }
