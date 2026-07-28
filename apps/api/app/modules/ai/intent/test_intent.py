from app.modules.ai.intent import IntentAnalyzer

questions = [
    "Explain build_rag",
    "Review app.py",
    "Generate README",
    "Find authentication bug",
    "Explain architecture",
]

for q in questions:

    result = IntentAnalyzer.analyze(q)

    print("-" * 50)
    print(q)
    print(result)