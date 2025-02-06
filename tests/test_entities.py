import json
from pathlib import Path

import pandas as pd
from pydantic import TypeAdapter

from textmine.entities import Entity, get_entity_types

ROOT_DIR = Path(__file__).parent.parent


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


def test_parse_entities():
    ta = TypeAdapter(list[Entity])
    train_df = pd.read_csv(ROOT_DIR / "resources/train.csv")
    train_df = train_df.set_index("id")
    train_df.entities = train_df.entities.apply(ta.validate_json)
    train_df.relations = train_df.relations.apply(json.loads)

    for entity in train_df.sample(1).entities.values[0]:
        assert type(entity) is Entity
