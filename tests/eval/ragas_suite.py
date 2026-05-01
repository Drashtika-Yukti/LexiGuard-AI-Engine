import os
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from core.orchestrator import run_nexus

def run_ragas_eval():
    """
    Automated RAGAS Evaluation Suite for Nexus Legal Intelligence.
    Measures Faithfulness, Relevance, and Precision.
    """
    # 1. Prepare Evaluation Dataset (Golden Set)
    eval_questions = [
        "What is the penalty for theft in BNS?",
        "How is a contract formed under Indian Law?",
        "What are the rights of a tenant in case of eviction?"
    ]
    
    # In a real scenario, these would be the ground truths from your legal experts
    ground_truths = [
        "The penalty for theft is defined under Section 303 of BNS...",
        "A contract requires offer, acceptance, and consideration...",
        "A tenant has the right to notice and a fair hearing..."
    ]
    
    answers = []
    contexts = []
    
    print("🚀 Starting Nexus RAGAS Evaluation...")
    
    for q in eval_questions:
        # Run the real engine
        result = run_nexus(q, "eval_session")
        answers.append(result["final_answer"])
        contexts.append(result["documents"]) # RAGAS needs the retrieved context
        
    # 2. Format for RAGAS
    data = {
        "question": eval_questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    # 3. Perform Evaluation
    print("📊 Calculating Scores...")
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
        ],
    )
    
    print("\n--- NEXUS RAGAS SCORES ---")
    print(result)
    return result

if __name__ == "__main__":
    run_ragas_eval()
