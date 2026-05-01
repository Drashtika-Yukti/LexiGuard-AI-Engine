import os
import sys
import json
sys.path.append(os.getcwd())

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from core.orchestrator import run_nexus

def run_ragas_eval():
    """
    Automated RAGAS Evaluation Suite for Nexus Legal Intelligence.
    Uses the 20-question Golden Set for high-trust scoring.
    """
    # 1. Load Golden Set
    with open("data/golden_eval_set.json", "r") as f:
        golden_set = json.load(f)
    
    eval_questions = [item["question"] for item in golden_set]
    ground_truths = [item["ground_truth"] for item in golden_set]
    
    answers = []
    contexts = []
    
    print(f"🚀 Starting Nexus RAGAS Evaluation on {len(eval_questions)} queries...")
    
    for i, q in enumerate(eval_questions):
        print(f"[{i+1}/{len(eval_questions)}] Processing: {q[:50]}...")
        # Run the real engine
        result = run_nexus(q, f"eval_session_v{i}")
        answers.append(result["answer"])
        contexts.append(result["documents"])
        
    # 2. Format for RAGAS
    data = {
        "question": eval_questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    # 3. Perform Evaluation
    print("📊 Calculating Metrics (Faithfulness, Relevance, Precision)...")
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
        ],
    )
    
    print("\n--- NEXUS FINAL TRUST SCORES ---")
    print(result)
    
    # Save results to a file for the CI to archive
    with open("data/latest_eval_scores.json", "w") as f:
        json.dump(result, f, indent=4)
        
    return result

if __name__ == "__main__":
    run_ragas_eval()
