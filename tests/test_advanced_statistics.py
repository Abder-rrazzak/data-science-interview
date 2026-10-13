import numpy as np
import pytest
from decision_intelligence.advanced_statistics import one_way_anova,chi_square_independence,multiple_ols,logistic_regression_demo

def test_anova_detects_mean_difference():
    rng=np.random.default_rng(7)
    a=rng.normal(0,1,80);b=rng.normal(2,1,80);c=rng.normal(4,1,80)
    out=one_way_anova({'a':a,'b':b,'c':c})
    assert out['p_value']<0.001 and 0<out['eta_squared']<1

def test_anova_rejects_insufficient_groups():
    with pytest.raises(ValueError):one_way_anova({'a':[1,2,3]})

def test_chi_square_association():
    result=chi_square_independence([[80,20],[20,80]])
    assert result['p_value']<1e-6 and result['cramers_v']>0.5

def test_chi_square_rejects_negative_counts():
    with pytest.raises(ValueError):chi_square_independence([[1,-1],[2,3]])

def test_ols_recovers_coefficients():
    rng=np.random.default_rng(11)
    x=rng.normal(size=(500,2));y=3+2*x[:,0]-1.5*x[:,1]+rng.normal(0,.2,500)
    result=multiple_ols(x,y,['first','second'])
    assert result['coefficients']['first']==pytest.approx(2,abs=.05)
    assert result['coefficients']['second']==pytest.approx(-1.5,abs=.05)
    assert result['r_squared']>.98
    assert all(0<=v<=1 for v in result['p_values'].values())

def test_ols_rejects_collinearity():
    x=np.arange(20,dtype=float)
    with pytest.raises(ValueError):multiple_ols(np.column_stack([x,2*x]),x)

def test_logistic_demo():
    rng=np.random.default_rng(9);x=rng.normal(size=(400,2));y=rng.binomial(1,1/(1+np.exp(-2*x[:,0])))
    result=logistic_regression_demo(x,y)
    assert result['train_auc']>.7
    assert 'Training metrics' in result['warning']
