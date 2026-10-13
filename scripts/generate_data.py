import argparse
from decision_intelligence.data import save_events

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic observations")
    parser.add_argument("--rows", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/generated/events.csv")
    args = parser.parse_args()
    print(f"Generated synthetic dataset: {save_events(args.output, args.rows, args.seed)}")
