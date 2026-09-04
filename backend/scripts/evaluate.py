"""
Quick evaluation harness against the deployed /chat endpoint.

Run: python backend/scripts/evaluate.py --url https://your-app.railway.app

For deeper metrics (context relevance, faithfulness, answer relevance),
install ragas (`pip install ragas datasets`) and feed the printed
question/answer/context triples into it — kept optional here so this
script has zero extra dependencies for a quick smoke test.
"""
import argparse
import time
import requests

TEST_QUESTIONS = [
    ("What is Varun's CGPA?", "8.32 from IIT Palakkad"),
    ("What projects has Varun built?", "should name the self-updating rag portfolio assist, weather alerting platform and the URL shortener"),
    ("What is the multipacking paper about?", "should summarize the hypercube / broadcast domination research"),
    ("What chess openings does Varun play?", "Sicilian Defence with Black, Ruy Lopez with White"),
    ("What was the accuracy improvement in the internship?", "~72% to ~85% accuracy on the attrition model"),
    ("What is Varun's email?", "varunsani625@gmail.com"),
    ("What is the capital of France?", "should decline — out of scope"),
]


def run(base_url: str):
    session_id = f"eval_{int(time.time())}"
    for question, expectation in TEST_QUESTIONS:
        resp = requests.post(
            f"{base_url}/chat",
            json={"message": question, "session_id": session_id},
            timeout=30,
        )
        data = resp.json()
        print("=" * 70)
        print(f"Q: {question}")
        print(f"Expected: {expectation}")
        print(f"A: {data.get('answer')}")
        print(f"Citations: {[c['text'] for c in data.get('citations', [])]}")
        print(f"Latency: {data.get('latency_ms')} ms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    args = parser.parse_args()
    run(args.url)
