import numpy as np
import pytest
from decision_intelligence.uncertainty import (bootstrap_mean_ci,linear_prediction_interval,
 beta_binomial_posterior,correlated_monte_carlo,one_at_a_time_sensitivity,compare_decisions)

def test_bootstrap_deterministic():
 a=bootstrap_mean_ci([1,2,3,4,5],seed=10)
 assert a==bootstrap_mean_ci([1,2,3,4,5],seed=10)
 assert a['lower']<=3<=a['upper']

def test_bootstrap_invalid():
 with pytest.raises(ValueError): bootstrap_mean_ci([1])

def test_bootstrap_nonfinite():
 with pytest.raises(ValueError): bootstrap_mean_ci([1,float('nan')])

def test_prediction_wider_than_mean_ci():
 x=np.arange(20,dtype=float); y=2*x+np.sin(x)
 r=linear_prediction_interval(x,y,[10])
 assert r['prediction_upper'][0]-r['prediction_lower'][0]>r['mean_ci_upper'][0]-r['mean_ci_lower'][0]

def test_prediction_invalid_constant_x():
 with pytest.raises(ValueError): linear_prediction_interval([1,1,1],[1,2,3],[1])

def test_bayesian_posterior():
 r=beta_binomial_posterior(5,10)
 assert r['posterior_mean']==.5
 assert r['credible_lower']<.5<r['credible_upper']

def test_bayesian_invalid_counts():
 with pytest.raises(ValueError): beta_binomial_posterior(11,10)

def test_correlated_mc_analytic_agreement():
 r=correlated_monte_carlo([1,2],[2,3],[[1,.5],[.5,1]],[1,1],draws=30000)
 assert abs(r['mean']-r['analytical_mean'])<.12
 assert abs(r['std']-r['analytical_std'])<.12

def test_correlated_mc_seed():
 args=([1],[2],[[1]],[1])
 assert correlated_monte_carlo(*args,seed=4)==correlated_monte_carlo(*args,seed=4)

def test_invalid_correlation():
 with pytest.raises(ValueError): correlated_monte_carlo([1,2],[1,1],[[1,2],[2,1]],[1,1])

def test_sensitivity_ranking():
 r=one_at_a_time_sensitivity({'x':10,'y':10},{'x':(0,20),'y':(9,11)},lambda x,y: x+y)
 assert r['parameters'][0]['parameter']=='x'

def test_decision_expected_payoff():
 r=compare_decisions({'a':[10,-10],'b':[2,2]},[.5,.5])
 assert r['a']['expected_payoff']==0
 assert r['b']['expected_payoff']==2
 assert r['a']['lower_tail_payoff']==-10

def test_decision_invalid_probability():
 with pytest.raises(ValueError): compare_decisions({'a':[1,2]},[.6,.6])
