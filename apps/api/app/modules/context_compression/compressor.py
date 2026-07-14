class ContextCompressor:

    @staticmethod
    def compress(chunks):

        unique = []

        visited = set()

        for chunk in chunks:

            if isinstance(chunk, dict):

                chunk_id = chunk["chunk_id"]

            else:

                chunk_id = chunk.id

            if chunk_id in visited:
                continue

            visited.add(chunk_id)

            unique.append(chunk)

        return unique