from app.modules.context.repository import ContextRepository


class ContextService:

    @staticmethod
    async def build(
        db,
        retrieval_results,
    ):

        results = retrieval_results

        if not results:
            print("=" * 80)
            print("No retrieval results found.")
            print("=" * 80)
            return []

        print("=" * 80)
        print("CONTEXT INPUT SAMPLE")
        print(results[0])
        print("HAS repository_file_id:", "repository_file_id" in results[0])
        print("=" * 80)

        expanded = []

        visited = set()

        print("=" * 80)
        print("RESULT TYPE:", type(results))
        print("TOTAL RESULTS:", len(results))
        print("FIRST RESULT TYPE:", type(results[0]))
        print("=" * 80)

        for chunk in results:

            expanded.append(chunk)

            visited.add(str(chunk["chunk_id"]))

            neighbours = await ContextRepository.get_neighbour_chunks(

                db=db,

                repository_file_id=chunk["repository_file_id"],

                start_line=chunk["start_line"],

            )

            for neighbour in neighbours:

                if str(neighbour.id) not in visited:

                    expanded.append(
                        {
                            "id": str(neighbour.id),
                            "chunk_id": str(neighbour.id),
                            "chunk_name": neighbour.chunk_name,
                            "chunk_type": neighbour.chunk_type,
                            "repository_file_id": str(neighbour.repository_file_id),
                            "start_line": neighbour.start_line,
                            "end_line": neighbour.end_line,
                            "content": neighbour.content,
                        }
                    )

                    visited.add(neighbour.id)

        return expanded