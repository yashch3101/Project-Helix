class PromptBuilder:

    @staticmethod
    def build(
        question: str,
        contexts: list,
    ):

        prompt = """
You are an expert software engineer.

Answer ONLY using the repository context.

If the answer is not present,
say that it is not found.

Repository Context

"""

        for i, chunk in enumerate(contexts, 1):

            prompt += f"""

===== Chunk {i} =====

File : {chunk["chunk_name"]}

Type : {chunk["chunk_type"]}

Lines : {chunk["start_line"]}-{chunk["end_line"]}

{chunk["content"]}

"""

        prompt += f"""

==============================

Question:

{question}

Answer:
"""

        return prompt