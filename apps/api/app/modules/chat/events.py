import json


class ChatEvent:

    @staticmethod
    def token(text: str):

        return (
            f"event: token\n"
            f"data: {json.dumps(text)}\n\n"
        )


    @staticmethod
    def done():

        return (
            "event: done\n"
            "data: {}\n\n"
        )


    @staticmethod
    def error(message: str):

        return (
            f"event: error\n"
            f"data: {json.dumps(message)}\n\n"
        )

    @staticmethod
    def citations(items):

        import json

        return (
            "event: citations\n"
            f"data: {json.dumps(items)}\n\n"
        )