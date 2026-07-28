class PromptBuilder:

    @staticmethod
    def build(
        history: str,
        context: str,
        question: str,
    ):

        history = history or ""
        context = context or ""
        question = question or ""

        MAX_HISTORY_CHARS = 3000

        if len(history) > MAX_HISTORY_CHARS:
            history = history[-MAX_HISTORY_CHARS:]

        MAX_CONTEXT_CHARS = 12000

        if len(context) > MAX_CONTEXT_CHARS:
            context = (
                context[:MAX_CONTEXT_CHARS]
                + "\n\n... (repository context truncated due to size) ..."
            )

        return f"""

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

3. Repository Context is the primary source of truth.

Never answer from general knowledge when repository context exists.

Treat every code block inside Repository Context as the ground truth.

When source code is available:

- Explain the actual code line by line.
- Never say implementation is unavailable.
- Never summarize from general knowledge.
- Base every statement on the provided code.

4. If the answer is not present inside the repository,
say that clearly.

5. Never invent APIs or code.

6. Answer like a senior software engineer.

7. Repository Context contains real source code.

Treat every code block as the authoritative implementation.

Do not ignore code blocks.

Explain them directly.

Answer in exactly this format.

Summary

Implementation
(Do NOT paste the entire function.)

Use short code snippets only when necessary.

Do not copy more than 10 consecutive lines of source code.

Execution Flow

Important Calls

Return Value

Related Symbols

Repository Files

Confidence

Choose one:

High
Medium
Low

Answer

Answer:
"""