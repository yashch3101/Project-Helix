import re


class Tokenizer:

    @staticmethod
    def tokenize(text: str):

        text = text.lower()

        return re.findall(
            r"[a-zA-Z0-9_]+",
            text,
        )