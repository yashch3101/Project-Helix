from app.modules.ai.intent import IntentAnalyzer
from app.modules.ai.planner import Planner

questions = [
    "Explain build_rag",
    "Review app.py",
    "Generate README",
    "Find authentication bug",
]

for q in questions:

    intent = IntentAnalyzer.analyze(q)

    plan = Planner.create_plan(intent)

    print("-" * 60)
    print(q)
    print(intent)
    print(plan)