"""Run reproducible synthetic uncertainty examples and save computed output."""
import json
from pathlib import Path
import numpy as np
from decision_intelligence.uncertainty import (bootstrap_mean_ci,linear_prediction_interval,
    beta_binomial_posterior,correlated_monte_carlo,one_at_a_time_sensitivity,compare_decisions)

def main():
    rng=np.random.default_rng(2026)
    observations=rng.normal(10,2,size=180)
    x=np.linspace(0,10,120)
    y=2+1.4*x+rng.normal(0,1.8,size=len(x))
    report={
      'data_notice':'Synthetic examples only; not real operational or security data.',
      'bootstrap':bootstrap_mean_ci(observations,seed=2026),
      'linear_intervals':linear_prediction_interval(x,y,[3,7]),
      'bayesian_rate':beta_binomial_posterior(28,100,prior_a=2,prior_b=2),
      'monte_carlo':correlated_monte_carlo([10,15],[2,3],[[1,.4],[.4,1]],[.6,.4],seed=2026),
      'sensitivity':one_at_a_time_sensitivity({'volume':100.,'cost':4.},
          {'volume':(80,120),'cost':(3,5)},lambda volume,cost:volume*cost),
      'decisions':compare_decisions({'A':[20,5,-30],'B':[12,10,-5]},[.5,.35,.15])}
    path=Path(__file__).resolve().parents[1]/'artifacts'/'phase6_uncertainty.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    print('Saved:',path)

if __name__=='__main__': main()
