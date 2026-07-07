MAX_HISTORY_MESSAGES = 10


class HistoryBuilder:

    @staticmethod
    def build(messages):

        if not messages:
            return ""

        history = []

        recent_messages = messages[-MAX_HISTORY_MESSAGES:]

        for message in recent_messages:

            role = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            history.append(
                f"{role}: {message.content}"
            )

        return "\n\n".join(history)