from collections import defaultdict

from textmine.relations import Relation

type RelationTuple = tuple[int, str, int]


class Metrics:
    false_negative_counts: dict[str, int] = defaultdict(int)
    true_positive_counts: dict[str, int] = defaultdict(int)
    false_positive_counts: dict[str, int] = defaultdict(int)

    def update_false_negatives(self, false_negatives: set[RelationTuple]):
        for _, relation, _ in false_negatives:
            self.false_negative_counts[relation] += 1

    def update_false_positives(self, false_positives: set[RelationTuple]):
        for _, relation, _ in false_positives:
            self.false_positive_counts[relation] += 1

    def update_true_positives(self, true_positives: set[RelationTuple]):
        for _, relation, _ in true_positives:
            self.true_positive_counts[relation] += 1

    def compute_metrics(self):
        f1s = dict()
        for predicate in set(self.true_positive_counts.keys()).union(
            self.false_negative_counts.keys()
        ):
            precision = (
                0
                if self.false_positive_counts[predicate]
                + self.true_positive_counts[predicate]
                == 0
                else self.true_positive_counts[predicate]
                / (
                    self.false_positive_counts[predicate]
                    + self.true_positive_counts[predicate]
                )
            )
            recall = (
                0
                if self.false_negative_counts[predicate]
                + self.true_positive_counts[predicate]
                == 0
                else self.true_positive_counts[predicate]
                / (
                    self.false_negative_counts[predicate]
                    + self.true_positive_counts[predicate]
                )
            )
            f1s[predicate] = (
                0
                if recall + precision == 0
                else 2 * precision * recall / (precision + recall)
            )
        macro_f1 = sum(f1s.values()) / len(f1s)

        return {
            "f1": macro_f1,
            "number_true_positives": sum(self.true_positive_counts.values()),
            "number_false_positives": sum(self.false_positive_counts.values()),
            "number_false_negatives": sum(self.false_negative_counts.values()),
        }


def score(
    gold: set[RelationTuple], predictions: set[Relation]
) -> tuple[set[RelationTuple], set[RelationTuple], set[RelationTuple]]:
    predicted_relations: set[RelationTuple] = set(
        (relation.head.id, relation.type, relation.tail.id) for relation in predictions
    )
    false_positives = predicted_relations - gold
    false_negatives = gold - predicted_relations
    true_positives = gold & predicted_relations
    return true_positives, false_positives, false_negatives
