import pytest
import json
import os
import sys
sys.path.append(os.getcwd())

from deepeval.metrics import HallucinationMetric, GEval
from deepeval.test_case import LLMTestCase
from core.orchestrator import run_nexus

# Load a subset of questions for assertive testing
with open("data/golden_eval_set.json", "r") as f:
    golden_set = json.load(f)

@pytest.mark.parametrize("test_data", golden_set[:3]) # Test first 3 for CI speed
def test_nexus_intelligence_threshold(test_data):
    """
    DeepEval test suite ensuring each response meets the minimum 'Legal Correctness' threshold.
    """
    query = test_data["question"]
    result = run_nexus(query, "deepeval_automation")
    
    # 1. Setup Test Case
    test_case = LLMTestCase(
        input=query,
        actual_output=result["answer"],
        retrieval_context=result["documents"]
    )
    
    # 2. Metrics
    hallucination_metric = HallucinationMetric(threshold=0.3)
    legal_correctness_metric = GEval(
        name="Legal Correctness",
        criteria="Evaluate if the answer matches the ground truth legal statute accurately.",
        evaluation_params=["input", "actual_output", "retrieval_context"],
        threshold=0.6
    )
    
    # 3. Execution
    hallucination_metric.measure(test_case)
    legal_correctness_metric.measure(test_case)
    
    # 4. Strict Enforcement
    assert not hallucination_metric.is_successful(), f"FAILURE: Hallucination detected for: {query}"
    assert legal_correctness_metric.is_successful(), f"FAILURE: Legal correctness below threshold for: {query}"

if __name__ == "__main__":
    pytest.main([__file__])
