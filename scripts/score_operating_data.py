import csv
from collections import defaultdict

scores = defaultdict(list)
quality_failures = defaultdict(float)
value = defaultdict(float)

with open("data/daily_metrics.csv", newline="") as f:
    for row in csv.DictReader(f):
        scores[row["entity_id"]].append(float(row["priority_score"]))

with open("data/data_quality_checks.csv", newline="") as f:
    for row in csv.DictReader(f):
        quality_failures[row["table_name"]] += float(row["failed_records"])

with open("data/recommended_actions.csv", newline="") as f:
    for row in csv.DictReader(f):
        value[row["entity_id"]] += float(row["expected_value_or_cost_avoidance"])

ranked = []
for entity_id, entity_scores in scores.items():
    avg_priority = sum(entity_scores) / len(entity_scores)
    action_value = value[entity_id]
    ranked.append((avg_priority + action_value / 50000, entity_id, avg_priority, action_value))

print("Top entity priorities")
for rank, (score, entity_id, avg_priority, action_value) in enumerate(sorted(ranked, reverse=True)[:10], start=1):
    print(f"{rank}. {entity_id}: composite={score:.1f}, avg_priority={avg_priority:.1f}, action_value=$" + format(action_value, ",.0f"))

print("\nData quality hotspots")
for table_name, failed in sorted(quality_failures.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"{table_name}: failed_records=" + format(failed, ",.0f"))
