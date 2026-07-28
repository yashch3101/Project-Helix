import re

from .models import IntentResult, IntentType


class IntentAnalyzer:

    @staticmethod
    def analyze(question: str) -> IntentResult:

        text = question.lower().strip()

        if "readme" in text or "documentation" in text or "docs" in text:
            return IntentResult(IntentType.DOCUMENTATION)

        if "review" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.REVIEW, entity, 0.98)

        if "bug" in text or "issue" in text or "error" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.BUG, entity, 0.97)

        if "refactor" in text or "optimize" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.REFACTOR, entity, 0.96)

        if "architecture" in text:
            return IntentResult(IntentType.ARCHITECTURE)

        if "dependency" in text:
            return IntentResult(IntentType.DEPENDENCY)

        if "class" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.CLASS, entity, 0.95)

        if "file" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.FILE, entity, 0.95)

        if "function" in text or "method" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.FUNCTION, entity, 0.95)

        if "explain" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.EXPLAIN, entity, 0.94)

        if "find" in text or "search" in text:
            entity = IntentAnalyzer.extract_entity(question)
            return IntentResult(IntentType.SEARCH, entity, 0.93)

        return IntentResult(IntentType.GENERAL)

    @staticmethod
    def extract_entity(question: str):

        matches = re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", question)

        ignore = {
            "explain",
            "review",
            "generate",
            "find",
            "search",
            "bug",
            "issue",
            "architecture",
            "function",
            "class",
            "file",
            "dependency",
            "documentation",
            "readme",
        }

        for match in matches:

            if match.lower() not in ignore:

                return match

        return None