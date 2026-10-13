import numpy as np
import pytest
from decision_intelligence.data import generate_events
from decision_intelligence.analysis import compare_regions
from decision_intelligence.model import score_anomalies

def test_generator_reproducible():
    assert generate_events(20, 3).equals(generate_events(20, 3))

def test_generator_rejects_zero():
    with pytest.raises(ValueError):
        generate_events(0)

def test_welch_result():
    result = compare_regions(generate_events(500))
    assert 0 <= result["p_value"] <= 1
    assert result["ci95_lower"] <= result["ci95_upper"]
    assert np.isfinite(result["mean_difference"])

def test_anomalies():
    scored = score_anomalies(generate_events(200))
    assert len(scored) == 200
    assert scored.anomaly_score.notna().all()
    assert scored.is_anomaly.dtype == bool
