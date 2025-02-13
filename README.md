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
