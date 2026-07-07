from app.modules.ai.prompt import SYSTEM_PROMPT


class PromptBuilder:

    @staticmethod
    def build(
        history: str,
        context: str,
        question: str,
    ):

        return f"""
{SYSTEM_PROMPT}

==============================
CONVERSATION HISTORY
==============================

{history}

==============================
REPOSITORY CONTEXT
==============================

{context}

==============================
CURRENT USER QUESTION
==============================

{question}

==============================
INSTRUCTIONS
==============================

1. Continue the existing conversation naturally.

2. Resolve references like:
   - it
   - this
   - that
   - they
   - previous answer

using Conversation History.

3. Use Repository Context only when it is relevant.

4. If the answer is not present inside the repository,
say that clearly.

5. Never invent APIs or code.

6. Answer like a senior software engineer.

Answer:
"""