# TextMine2025

Code pour le défi [TextMine2025](https://www.kaggle.com/competitions/defi-text-mine-2025-permanent).

## Références

- [Système gagnant du défi](https://github.com/AdrienGuille/TextMine2025):

> Adaptation d'un modèle de langue encodeur-décodeur pour l'extraction de relations dans des rapports de renseignement. Adrien Guille. Atelier Fouille de Textes (TextMine @ EGC), Strasbourg (France), 2025

- [Système de RE zero-shot](https://arxiv.org/pdf/2305.11159):

> Zhang, K., B. Jimenez Gutierrez, et Y. Su (2023). Aligning instruction tasks unlocks large language models as zero-shot relation extractors. In Findings of the Association for Computational Linguistics (ACL 2023).

## Installation

This project requires python >=3.12. Install the project in a virtual environment of your choice ([micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) is a good option).

Install either with pip

```console
pip install --editable .
```

or [poetry](https://python-poetry.org/)

```console
poetry install
```

## Usage

The project installs a CLI command to predict relations from an input dataframe and evaluate predictions. Run

```console
textmine --text-id 181 resources/train.csv
```

(preprend with `poetry run` if using poetry) to predict relations for text with id `181` in `resources/train.csv` dataframe. This will display the macro-f1 score for the predicted texts, as well as save results in a csv file in the same directory as the input file.

## Analyse

### Annotation

L'annotation manuelle des données semble lacunaire voire souvent erronée. Prenons l'exemple du document `181` dans le jeu d'entrainement.

> Anam Destresse, président de l'ONG "Ma passion", a été blessé dans un accident. Le 30 juin 2022, un accident de circulation s'est produit entre une moto et un bus sur l'autoroute de Saint-Marin en Italie. Le bus, qui transportait 20 passagers, appartenait à l'ONG. Lors de l'accident, les panneaux de signalisation ont été complètement endommagés et le garde du corps a été blessé. Au total, deux passagers sont morts sur le coup. Anam Destresse, qui faisait partie des blessés, a été transporté en hélicoptère jusqu'à l'hôpital. Le conducteur de la moto a été retrouvé mort en dessous du bus. Il conduisait sans permis et en état d'ivresse.

Les entités annotées dans le texte sont

```python
[Entity(id=0, type='ACCIDENT', mentions=[Mention(value='accident', start=70, end=78), Mention(value='accident de circulation', start=100, end=123), Mention(value='accident', start=275, end=283)]),
 Entity(id=1, type='CIVILIAN', mentions=[Mention(value='Anam Destresse', start=0, end=14), Mention(value='Anam Destresse', start=431, end=445)]),
 Entity(id=2, type='MATERIEL', mentions=[Mention(value='moto', start=148, end=152), Mention(value='moto', start=550, end=554)]),
 Entity(id=3, type='MATERIEL', mentions=[Mention(value='bus', start=159, end=162), Mention(value='bus', start=208, end=211), Mention(value='bus', start=589, end=592)]),
 Entity(id=4, type='MATERIEL', mentions=[Mention(value='panneaux de signalisation', start=289, end=314)]),
 Entity(id=5, type='GROUP_OF_INDIVIDUALS', mentions=[Mention(value='blessés', start=470, end=477)]),
 Entity(id=6, type='MATERIEL', mentions=[Mention(value='hélicoptère', start=499, end=510)]),
 Entity(id=7, type='CIVILIAN', mentions=[Mention(value='garde du corps', start=353, end=367)]),
 Entity(id=8, type='NON_GOVERNMENTAL_ORGANISATION', mentions=[Mention(value='Ma passion', start=36, end=46), Mention(value='ONG', start=260, end=263)]),
 Entity(id=9, type='PLACE', mentions=[Mention(value='autoroute de Saint-Marin', start=169, end=193)]),
 Entity(id=10, type='PLACE', mentions=[Mention(value='Italie', start=197, end=203)]),
 Entity(id=11, type='PLACE', mentions=[Mention(value='hôpital', start=521, end=528)]),
 Entity(id=12, type='GROUP_OF_INDIVIDUALS', mentions=[Mention(value='passagers', start=233, end=242)]),
 Entity(id=13, type='GROUP_OF_INDIVIDUALS', mentions=[Mention(value='passagers', start=397, end=406)]),
 Entity(id=14, type='TERRORIST_OR_CRIMINAL', mentions=[Mention(value='conducteur', start=533, end=543), Mention(value='Il', start=594, end=596)]),
 Entity(id=15, type='TIME_EXACT', mentions=[Mention(value='30 juin 2022', start=83, end=95)]),
 Entity(id=16, type='FIRSTNAME', mentions=[Mention(value='Anam', start=0, end=4)]),
 Entity(id=17, type='LASTNAME', mentions=[Mention(value='Destresse', start=5, end=14)]),
 Entity(id=18, type='CATEGORY', mentions=[Mention(value='président', start=16, end=25)]),
 Entity(id=19, type='CATEGORY', mentions=[Mention(value='garde du corps', start=353, end=367)]),
 Entity(id=20, type='CATEGORY', mentions=[Mention(value='conducteur', start=533, end=543)]),
 Entity(id=21, type='QUANTITY_EXACT', mentions=[Mention(value='deux', start=392, end=396)]),
 Entity(id=22, type='QUANTITY_EXACT', mentions=[Mention(value='20', start=230, end=232)]),
 Entity(id=23, type='FIRSTNAME', mentions=[Mention(value='Anam', start=431, end=435)]),
 Entity(id=24, type='LASTNAME', mentions=[Mention(value='Destresse', start=436, end=445)])]
 ```

 tandis que les relations annotées sont

 ```python
 [[0, 'STARTED_IN', 9],
 [7, 'IS_LOCATED_IN', 9],
 [5, 'IS_LOCATED_IN', 10],
 [1, 'GENDER_FEMALE', 1],
 [12, 'IS_LOCATED_IN', 10],
 [0, 'IS_LOCATED_IN', 10],
 [1, 'IS_LOCATED_IN', 10],
 [13, 'IS_LOCATED_IN', 9],
 [14, 'IS_LOCATED_IN', 10],
 [1, 'HAS_CATEGORY', 18],
 [5, 'IS_LOCATED_IN', 9],
 [9, 'IS_LOCATED_IN', 10],
 [14, 'IS_DEAD_ON', 15],
 [7, 'HAS_CATEGORY', 19],
 [12, 'IS_LOCATED_IN', 9],
 [0, 'IS_LOCATED_IN', 9],
 [7, 'GENDER_MALE', 7],
 [11, 'IS_LOCATED_IN', 10],
 [1, 'IS_LOCATED_IN', 9],
 [14, 'IS_LOCATED_IN', 9],
 [14, 'HAS_CATEGORY', 20],
 [0, 'STARTED_IN', 10],
 [0, 'START_DATE', 15],
 [7, 'IS_LOCATED_IN', 10],
 [0, 'END_DATE', 15],
 [14, 'GENDER_MALE', 14],
 [12, 'IS_OF_SIZE', 22],
 [13, 'IS_LOCATED_IN', 10],
 [1, 'IS_LOCATED_IN', 11],
 [13, 'IS_OF_SIZE', 21]]
 ```

 * `Anam Destresse` est identifié comme `FEMALE` (`[1, 'GENDER_FEMALE', 1]`) alors que ce n'est pas précisé dans le texte (ni par l'accord, ni par les pronoms).
 *
