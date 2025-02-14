from pydantic import BaseModel

ENTITY_TYPE_PARENTS = {
    "EPIDEMIC": "LARGE_SCALE_EVENT",
    "BOMBING": "CRIMINAL_EVENT",
    "CATEGORY": "ATTRIBUTE",
    "CBRN_EVENT": "EVENT",
    "TIME_MAX": "TIME",
    "HOOLIGANISM_TROUBLEMAKING": "CRIMINAL_EVENT",
    "NON_GOVERNMENTAL_ORGANISATION": "ORGANIZATION",
    "DRUG_OPERATION": "CRIMINAL_EVENT",
    "NON_MILITARY_GOVERNMENT_ORGANISATION": "GOVERNMENT_ORGANIZATION",
    "DEMONSTRATION": "CIVIL_UNREST",
    "ELECTION": "CIVIL_UNREST",
    "CIVIL_WAR_OUTBREAK": "CIVIL_UNREST",
    "TERRORIST_OR_CRIMINAL": "PERSON",
    "COLOR": "ATTRIBUTE",
    "MILITARY": "PERSON",
    "LENGTH": "ATTRIBUTE",
    "CRIMINAL_ARREST": "CRIMINAL_EVENT",
    "COUP_D_ETAT": "CIVIL_UNREST",
    "HEIGHT": "ATTRIBUTE",
    "ACCIDENT": "EVENT",
    "POLLUTION": "LARGE_SCALE_EVENT",
    "WIDTH": "ATTRIBUTE",
    "TIME_MIN": "TIME",
    "POLITICAL_VIOLENCE": "CRIMINAL_EVENT",
    "INTERGOVERNMENTAL_ORGANISATION": "ORGANIZATION",
    "MILITARY_ORGANISATION": "GOVERNMENT_ORGANIZATION",
    "NATURAL_CAUSES_DEATH": "CIVIL_UNREST",
    "GROUP_OF_INDIVIDUALS": "ACTOR",
    "ILLEGAL_CIVIL_DEMONSTRATION": "CIVIL_UNREST",
    "LASTNAME": "ATTRIBUTE",
    "QUANTITY_MAX": "QUANTITY",
    "GATHERING": "CIVIL_UNREST",
    "SUICIDE": "CIVIL_UNREST",
    "FIRE": "LARGE_SCALE_EVENT",
    "STRIKE": "CIVIL_UNREST",
    "FIRSTNAME": "ATTRIBUTE",
    "QUANTITY_FUZZY": "QUANTITY",
    "NATIONALITY": "ATTRIBUTE",
    "MATERIAL_REFERENCE": "ATTRIBUTE",
    "QUANTITY_MIN": "QUANTITY",
    "TIME_FUZZY": "TIME",
    "RIOT": "CIVIL_UNREST",
    "THEFT": "CRIMINAL_EVENT",
    "LONGITUDE": "ATTRIBUTE",
    "LATITUDE": "ATTRIBUTE",
    "AGITATING_TROUBLE_MAKING": "CIVIL_UNREST",
    "PLACE": "ENTITY",
    "CIVILIAN": "PERSON",
    "WEIGHT": "ATTRIBUTE",
    "MATERIEL": "ENTITY",
    "QUANTITY_EXACT": "QUANTITY",
    "TRAFFICKING": "CRIMINAL_EVENT",
    "ECONOMICAL_CRISIS": "LARGE_SCALE_EVENT",
    "TIME_EXACT": "TIME",
    "NATURAL_EVENT": "LARGE_SCALE_EVENT",
    "GOVERNMENT_ORGANIZATION": "ORGANIZATION",
    "ORGANIZATION": "ACTOR",
    "PERSON": "ACTOR",
    "CIVIL_UNREST": "EVENT",
    "CRIMINAL_EVENT": "EVENT",
    "LARGE_SCALE_EVENT": "EVENT",
    "EVENT": "ENTITY",
    "QUANTITY": "ATTRIBUTE",
    "TIME": "ATTRIBUTE",
    "ACTOR": "ENTITY",
}


class Mention(BaseModel):
    value: str
    start: int
    end: int


class Entity(BaseModel):
    id: int
    type: str
    mentions: list[Mention]

    def __hash__(self):
        return self.id.__hash__()

    @property
    def mention(self) -> str:
        return sorted(self.mentions, key=lambda m: len(m.value))[-1].value


def get_entity_types(entity_type: str) -> set[str]:
    """
    Get the set of all parent types for the given entity type

    Args:
        entity_type (str): the entity's type

    Returns:
        set[str]: set of all parent types, including entity_type.
    """
    types = set()
    types.add(entity_type)
    while entity_type in ENTITY_TYPE_PARENTS:
        types.add(ENTITY_TYPE_PARENTS[entity_type])
        entity_type = ENTITY_TYPE_PARENTS[entity_type]

    return types
