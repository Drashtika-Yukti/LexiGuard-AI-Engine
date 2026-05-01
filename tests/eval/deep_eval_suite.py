import pytest
from deepeval.metrics import GEval, HallucinationMetric
from deepeval.test_case import LLMTestCase
from core.orchestrator import run_nexus

def test_nexus_response_quality():
    """
    DeepEval test suite to assert response quality and detect hallucinations.
    """
    query = "What is the penalty for perjury?"
    result = run_nexus(query, "deepeval_session")
    
    # 1. Setup Test Case
    test_case = LLMTestCase(
        input=query,
        actual_output=result["final_answer"],
        retrieval_context=result["documents"]
    )
    
    # 2. Define Metrics
    # Metric 1: Hallucination Check
    hallucination_metric = HallucinationMetric(threshold=0.3)
    
    # Metric 2: G-Eval (Human-like reasoning for Legal Correctness)
    legal_correctness_metric = GEval(
        name="Legal Correctness",
        criteria="Determine if the legal advice is accurate based on Indian Statutes.",
        evaluation_params=["input", "actual_output", "retrieval_context"],
        threshold=0.7
    )
    
    # 3. Assertions
    hallucination_metric.measure(test_case)
    legal_correctness_metric.measure(test_case)
    
    assert hallucination_metric.is_successful(), f"Hallucination detected! Score: {hallucination_metric.score}"
    assert legal_correctness_metric.is_successful(), f"Legal correctness too low! Score: {legal_correctness_metric.score}"

if __name__ == "__main__":
    # For manual running
    import pytest
    pytest.main([__file__])
