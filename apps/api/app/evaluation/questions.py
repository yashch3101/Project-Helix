from dataclasses import dataclass
from typing import List


@dataclass
class EvaluationQuestion:
    """
    Represents one benchmark question for Project Helix evaluation.
    """

    question: str
    expected_symbol: str
    expected_file: str
    expected_type: str
    difficulty: str = "medium"


QUESTIONS: List[EvaluationQuestion] = [

    EvaluationQuestion(
        question="Explain build_rag",
        expected_symbol="build_rag",
        expected_file="backend/rag/pipeline.py",
        expected_type="function",
        difficulty="easy"
    ),

    EvaluationQuestion(
        question="How does ask_question work?",
        expected_symbol="ask_question",
        expected_file="backend/rag/pipeline.py",
        expected_type="function",
        difficulty="easy"
    ),

    EvaluationQuestion(
        question="Explain RetrievalPipeline.retrieve",
        expected_symbol="retrieve",
        expected_file="app/modules/retrieval/retrieval_pipeline.py",
        expected_type="method",
        difficulty="medium"
    ),

]