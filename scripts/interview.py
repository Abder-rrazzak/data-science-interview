"""Local, deterministic interview practice with honest self-scoring."""
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=["python", "sql", "statistics", "visualization", "leadership"])
    parser.add_argument("--difficulty", choices=["beginner", "intermediate", "advanced", "senior"])
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    bank = json.loads((ROOT / "interview_preparation/questions.json").read_text(encoding="utf-8"))
    rng = random.Random(args.seed)
    topics = sorted(set(q["topic"] for q in bank)) if args.full else [args.topic] if args.topic else [rng.choice(sorted(set(q["topic"] for q in bank)))]
    for topic in topics:
        options = [q for q in bank if q["topic"] == topic and (not args.difficulty or q["difficulty"] == args.difficulty)]
        if not options:
            print(f"No questions for {topic} / {args.difficulty}")
            continue
        q = rng.choice(options)
        print(f"\n[{topic.upper()} — {q['difficulty']}] {q['question']}")
        input("Think through your answer, then press Enter to see the rubric...")
        print("Evaluation rubric:", q["rubric"])
    print("\nSelf-score 0–5 per topic; this tool does not invent performance ratings.")

if __name__ == "__main__":
    main()
