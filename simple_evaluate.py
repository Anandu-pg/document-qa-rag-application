"""
Simple Evaluation Script for Document QA - Python OOP PDF
Metrics: Retrieval Precision, Retrieval Accuracy, Contextual Accuracy, Contextual Precision
"""
from app.utils.vectorstore import get_vectorstore
from app.agents.graph import app_graph
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import json
import pandas as pd
from datetime import datetime
import numpy as np

# Load embedding model
print("Loading embedding model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def load_test_questions():
    """Load test questions for Python OOP PDF"""
    return [
        {
            "question": "What is Object-Oriented Programming?",
            "ground_truth": "Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects that contain both data (attributes) and methods (functions) to operate on that data."
        },
        {
            "question": "What are the four pillars of OOP?",
            "ground_truth": "The four pillars of OOP are: Encapsulation, Inheritance, Polymorphism, and Abstraction."
        },
        {
            "question": "What is encapsulation and provide a real-world example?",
            "ground_truth": "Encapsulation means restricting direct access to variables and methods to protect the data. A real-world example is a bank account that hides its balance details and allows controlled access through deposit/withdraw methods."
        },
        {
            "question": "Explain inheritance with an example.",
            "ground_truth": "Inheritance allows one class to acquire the properties and methods of another class. For example, a Dog class can inherit from an Animal class."
        },
        {
            "question": "What is polymorphism in OOP?",
            "ground_truth": "Polymorphism means having many forms. It allows different classes to use the same method name but behave differently."
        },
        {
            "question": "What is abstraction and why is it important?",
            "ground_truth": "Abstraction means hiding the internal implementation and showing only the necessary functionality. It is important because it simplifies complex systems."
        },
        {
            "question": "What are the advantages of OOP?",
            "ground_truth": "The advantages of OOP include: code reusability through inheritance, improved code maintainability and organization, encapsulation provides data security, polymorphism allows flexibility in code, and abstraction hides implementation details."
        },
        {
            "question": "What is the difference between a class and an object?",
            "ground_truth": "A class is a blueprint for creating objects, while an object is an instance of a class."
        },
    ]

def calculate_retrieval_precision(retrieved_contexts, question):
    """
    Retrieval Precision: Proportion of retrieved contexts that are relevant
    """
    question_emb = embedder.encode([question])
    relevant_count = 0
    
    for context in retrieved_contexts:
        context_emb = embedder.encode([context])
        similarity = cosine_similarity(question_emb, context_emb)[0][0]
        if similarity > 0.4:  # Relevance threshold
            relevant_count += 1
    
    return relevant_count / len(retrieved_contexts) if retrieved_contexts else 0

def calculate_retrieval_accuracy(retrieved_contexts, ground_truth):
    """
    Retrieval Accuracy: How well retrieved contexts cover the ground truth
    """
    if not retrieved_contexts:
        return 0
    
    ground_truth_emb = embedder.encode([ground_truth])
    context_text = " ".join(retrieved_contexts)
    context_emb = embedder.encode([context_text])
    
    similarity = cosine_similarity(ground_truth_emb, context_emb)[0][0]
    return similarity

def calculate_contextual_accuracy(answer, ground_truth):
    """
    Contextual Accuracy: How factually accurate the answer is
    """
    answer_emb = embedder.encode([answer])
    truth_emb = embedder.encode([ground_truth])
    return cosine_similarity(answer_emb, truth_emb)[0][0]

def calculate_contextual_precision(answer, question):
    """
    Contextual Precision: How relevant the answer is to the question
    """
    answer_emb = embedder.encode([answer])
    question_emb = embedder.encode([question])
    return cosine_similarity(answer_emb, question_emb)[0][0]

def evaluate():
    """Run evaluation"""
    print("\n" + "=" * 80)
    print(" " * 20 + "DOCUMENT QA EVALUATION - PYTHON OOP")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Document: Python Object-Oriented Programming (OOP) Concepts")
    print("=" * 80)
    print()
    
    test_questions = load_test_questions()
    results = []
    
    print("Connecting to vector database...")
    vectorstore = get_vectorstore()
    
    print(f"📋 Testing {len(test_questions)} questions...\n")
    
    for i, test in enumerate(test_questions, 1):
        print(f"[{i}/{len(test_questions)}] {test['question'][:60]}...")
        
        try:
            # Retrieve contexts
            docs = vectorstore.similarity_search(test['question'], k=4)
            contexts = [doc.page_content for doc in docs]
            
            if not contexts:
                print(f"     ⚠️ No contexts retrieved. Upload PDF first!\n")
                continue
            
            # Get answer from agent
            result = app_graph.invoke({
                "question": test['question'],
                "context": [],
                "answer": "",
                "relevance_score": 0.0
            })
            
            # Calculate all metrics
            retrieval_precision = calculate_retrieval_precision(contexts, test['question'])
            retrieval_accuracy = calculate_retrieval_accuracy(contexts, test['ground_truth'])
            contextual_accuracy = calculate_contextual_accuracy(result['answer'], test['ground_truth'])
            contextual_precision = calculate_contextual_precision(result['answer'], test['question'])
            
            results.append({
                'question': test['question'],
                'answer': result['answer'][:100] + '...',  # Truncate for CSV
                'ground_truth': test['ground_truth'][:100] + '...',
                'retrieval_precision': retrieval_precision,
                'retrieval_accuracy': retrieval_accuracy,
                'contextual_accuracy': contextual_accuracy,
                'contextual_precision': contextual_precision,
                'agent_relevance_score': result['relevance_score']
            })
            
            print(f"     ✓ RP:{retrieval_precision:.2f} RA:{retrieval_accuracy:.2f} CA:{contextual_accuracy:.2f} CP:{contextual_precision:.2f}\n")
            
        except Exception as e:
            print(f"     ❌ Error: {e}\n")
            continue
    
    if not results:
        print("\n❌ No results generated. Make sure:")
        print("  1. Docker containers are running: docker-compose ps")
        print("  2. Python OOP PDF is uploaded via http://localhost:8000")
        print("\nTry:")
        print("  - Go to http://localhost:8000")
        print("  - Upload your Python OOP PDF")
        print("  - Wait for success message")
        print("  - Run this script again")
        return
    
    # Calculate averages
    avg_ret_precision = np.mean([r['retrieval_precision'] for r in results])
    avg_ret_accuracy = np.mean([r['retrieval_accuracy'] for r in results])
    avg_ctx_accuracy = np.mean([r['contextual_accuracy'] for r in results])
    avg_ctx_precision = np.mean([r['contextual_precision'] for r in results])
    overall_score = (avg_ret_precision + avg_ret_accuracy + avg_ctx_accuracy + avg_ctx_precision) / 4
    
    # Display results
    print("\n" + "=" * 80)
    print(" " * 30 + "EVALUATION RESULTS")
    print("=" * 80)
    print()
    print("📊 Performance Metrics (Scale: 0.0 to 1.0)")
    print("-" * 80)
    print(f"Retrieval Precision:              {avg_ret_precision:.4f} ({avg_ret_precision*100:.2f}%)")
    print(f"Retrieval Accuracy:               {avg_ret_accuracy:.4f} ({avg_ret_accuracy*100:.2f}%)")
    print(f"Contextual Accuracy:              {avg_ctx_accuracy:.4f} ({avg_ctx_accuracy*100:.2f}%)")
    print(f"Contextual Precision:             {avg_ctx_precision:.4f} ({avg_ctx_precision*100:.2f}%)")
    print("-" * 80)
    print(f"\n📈 Overall System Score:            {overall_score:.4f} ({overall_score*100:.2f}%)")
    
    # Performance rating
    if overall_score >= 0.8:
        rating = "✅ Excellent - Production Ready"
    elif overall_score >= 0.6:
        rating = "⚠️ Good - Minor Improvements Needed"
    else:
        rating = "❌ Fair - Requires Optimization"
    
    print(f"🎯 Performance Rating:              {rating}")
    print()
    
    # Save detailed results
    df = pd.DataFrame(results)
    df.to_csv("evaluation_results_oop.csv", index=False)
    print("💾 Detailed results saved to: evaluation_results_oop.csv")
    
    # Save summary
    summary = {
        "document": "Python OOP Concepts",
        "evaluation_date": datetime.now().isoformat(),
        "test_questions": len(results),
        "metrics": {
            "retrieval_precision": float(avg_ret_precision),
            "retrieval_accuracy": float(avg_ret_accuracy),
            "contextual_accuracy": float(avg_ctx_accuracy),
            "contextual_precision": float(avg_ctx_precision),
        },
        "overall_score": float(overall_score),
        "rating": rating
    }
    
    with open("evaluation_summary_oop.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("💾 Summary saved to: evaluation_summary_oop.json")
    print()
    
    # Interpretation
    print("=" * 80)
    print(" " * 30 + "INTERPRETATION")
    print("=" * 80)
    print()
    print("🔍 Retrieval Metrics:")
    print(f"  • Retrieval Precision: {avg_ret_precision*100:.1f}% of retrieved chunks are relevant")
    print(f"  • Retrieval Accuracy:  {avg_ret_accuracy*100:.1f}% coverage of required information")
    print()
    print("📝 Answer Quality Metrics:")
    print(f"  • Contextual Accuracy:  {avg_ctx_accuracy*100:.1f}% factual correctness")
    print(f"  • Contextual Precision: {avg_ctx_precision*100:.1f}% answer relevance")
    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    import sys
    import subprocess
    
    print("🔍 Checking system status...")
    
    try:
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True, check=True)
        
        if "Up" in result.stdout:
            print("✅ Docker containers running\n")
        else:
            print("❌ Containers not running. Start with: docker-compose up -d")
            sys.exit(1)
    except:
        print("⚠️ Could not check Docker status. Proceeding anyway...\n")
    
    evaluate()
