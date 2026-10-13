"""Execute the phase 5 reproducible synthetic experiment."""
from pathlib import Path
import json
from decision_intelligence.experimental_design import simulate_experiment, sample_size_two_means, adjust_pvalues


def main():
    output = {'sample_size':sample_size_two_means(effect=.5,std=2),
              'experiment':simulate_experiment(n=500,effect=.4,seed=42),
              'adjusted_pvalues':{'holm':adjust_pvalues([.003,.04,.08,.9], 'holm'),
                                  'fdr_bh':adjust_pvalues([.003,.04,.08,.9], 'fdr_bh')}}
    destination=Path(__file__).resolve().parents[1]/'artifacts'/'phase5_experiment.json'
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output,indent=2))
    print(f"Saved: {destination}")

if __name__ == '__main__':
    main()
