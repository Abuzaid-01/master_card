import pandas as pd

from api.pipeline_runner import leakage_resistant_split


def _fixture_dataset() -> pd.DataFrame:
    rows = []
    for index in range(80):
        rows.append(
            {
                "is_fraud": 0,
                "fraud_subtype": "legitimate",
                "timestamp_sec": index,
                "amount": float(index + 1),
            }
        )
    for family_index, family in enumerate(["burst", "ato", "bot", "cnp", "slow_drip"]):
        for row_index in range(8):
            rows.append(
                {
                    "is_fraud": 1,
                    "fraud_subtype": family,
                    "timestamp_sec": 100 + family_index * 10 + row_index,
                    "amount": 10.0,
                }
            )
    return pd.DataFrame(rows)


def test_fraud_families_do_not_cross_pipeline_partitions():
    partitions, manifest = leakage_resistant_split(_fixture_dataset(), "tabular")

    family_sets = []
    for partition in partitions.values():
        fraud_families = set(partition.loc[partition["is_fraud"] == 1, "fraud_subtype"])
        assert fraud_families
        family_sets.append(fraud_families)

    for index, families in enumerate(family_sets):
        for other in family_sets[index + 1 :]:
            assert families.isdisjoint(other)

    assert manifest["no_fraud_family_overlap"] is True
    assert manifest["immutable_evaluation_partition"] is True


def test_legitimate_rows_follow_time_order():
    partitions, manifest = leakage_resistant_split(_fixture_dataset(), "tabular")

    legitimate_times = {
        name: sorted(partition.loc[partition["is_fraud"] == 0, "timestamp_sec"].tolist())
        for name, partition in partitions.items()
    }
    assert max(legitimate_times["train"]) < min(legitimate_times["validation"])
    assert max(legitimate_times["validation"]) < min(legitimate_times["mining"])
    assert max(legitimate_times["mining"]) < min(legitimate_times["evaluation"])
    assert manifest["legitimate_split"] == "temporal"
