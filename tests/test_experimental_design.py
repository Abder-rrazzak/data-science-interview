import numpy as np
import pytest
from decision_intelligence.experimental_design import (
    random_assignment, stratified_assignment, sample_size_two_means,
    ab_test, adjust_pvalues, standardized_mean_difference, simulate_experiment,
)


def test_random_assignment_reproducible():
    a=random_assignment(100,seed=7)
    assert np.array_equal(a,random_assignment(100,seed=7))
    assert a.sum()==50


def test_random_assignment_invalid():
    with pytest.raises(ValueError): random_assignment(3)
    with pytest.raises(ValueError): random_assignment(10,.01)


def test_stratified_balanced():
    a=stratified_assignment(['A']*20+['B']*12)
    assert a[:20].sum()==10 and a[20:].sum()==6


def test_stratified_too_small():
    with pytest.raises(ValueError): stratified_assignment(['A']*3+['B']*10)


def test_sample_size_effect_direction():
    small=sample_size_two_means(.2,1)['n_total']
    large=sample_size_two_means(.5,1)['n_total']
    assert small>large


def test_sample_size_invalid():
    with pytest.raises(ValueError): sample_size_two_means(0,1)


def test_ab_test_detects_difference():
    rng=np.random.default_rng(1)
    result=ab_test(rng.normal(1,1,300),rng.normal(0,1,300))
    assert result['p_value']<.05 and result['confidence_interval'][0]>0


def test_ab_test_invalid():
    with pytest.raises(ValueError): ab_test([1,1,1],[1,1,1])


def test_bonferroni():
    assert adjust_pvalues([.01,.03,.9],'bonferroni')==pytest.approx([.03,.09,1.])


def test_holm():
    assert adjust_pvalues([.04,.001,.02],'holm')==pytest.approx([.04,.003,.04])


def test_bh():
    assert adjust_pvalues([.04,.001,.02],'fdr_bh')==pytest.approx([.04,.003,.03])


def test_pvalues_invalid():
    with pytest.raises(ValueError): adjust_pvalues([1.1])
    with pytest.raises(ValueError): adjust_pvalues([.05],method='none')


def test_smd():
    assert standardized_mean_difference([1,2,3],[1,2,3])==pytest.approx(0)


def test_simulation_reproducible():
    assert simulate_experiment(seed=4)==simulate_experiment(seed=4)
