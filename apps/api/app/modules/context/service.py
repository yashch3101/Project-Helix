from app.modules.context.repository import ContextRepository
from app.modules.retrieval.service import RetrievalService


class ContextService:

    @staticmethod
    async def build(
        db,
        repository_id,
        query,
        top_k=5,
    ):

        results = await RetrievalService.search(
            db=db,
            repository_id=repository_id,
            query=query,
            top_k=top_k,
        )

        print("=" * 80)
        print("CONTEXT INPUT SAMPLE")
        print(results[0])
        print("HAS repository_file_id:", "repository_file_id" in results[0])
        print("=" * 80)

        expanded = []

        visited = set()

        print("=" * 80)
        print("RESULT TYPE:", type(results))
        print("FIRST RESULT:", results[0])
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