import asyncio
import time
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.evaluation.questions import QUESTIONS
from app.modules.ai.service import AIService


class EvaluationRunner:
    """
    Executes benchmark questions against Helix.
    """

    def __init__(
        self,
        db: AsyncSession,
        repository_id: int,
    ):
        self.db = db
        self.repository_id = repository_id

    async def run(self):

        results = []

        for question in QUESTIONS:

            print("=" * 80)
            print(question.question)
            print("=" * 80)

        return results