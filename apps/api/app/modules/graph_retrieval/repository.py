from sqlalchemy import or_, select
from sqlalchemy.orm import aliased

from app.modules.graph.models import GraphEdge
from app.modules.parser.models import CodeSymbol
from app.modules.repository_index.models import RepositoryFile

from app.modules.graph_retrieval.types import GraphEdgeDTO


class GraphRetrievalRepository:

    @staticmethod
    async def get_related_symbols(
        db,
        repository_id,
        symbol_name,
    ):

        SourceSymbol = aliased(CodeSymbol)
        TargetSymbol = aliased(CodeSymbol)

        SourceFile = aliased(RepositoryFile)
        TargetFile = aliased(RepositoryFile)

        result = await db.execute(

            select(

                GraphEdge,

                SourceSymbol,
                TargetSymbol,

                SourceFile,
                TargetFile,

            )

            .join(

                SourceSymbol,

                SourceSymbol.symbol_name
                == GraphEdge.source_symbol,

            )

            .join(

                TargetSymbol,

                TargetSymbol.symbol_name
                == GraphEdge.target_symbol,

            )

            .join(

                SourceFile,

                SourceFile.id
                == SourceSymbol.repository_file_id,

            )

            .join(

                TargetFile,

                TargetFile.id
                == TargetSymbol.repository_file_id,

            )

            .where(
                GraphEdge.repository_id == repository_id
            )

            .where(

                or_(

                    GraphEdge.source_symbol == symbol_name,

                    GraphEdge.target_symbol == symbol_name,

                )

            )

        )

        rows = result.all()

        output = []

        for edge, source, target, source_file, target_file in rows:

            output.append(

                GraphEdgeDTO(

                    source_symbol=edge.source_symbol,

                    source_type=source.symbol_type,

                    source_file=source_file.relative_path,

                    source_start_line=source.line_start,

                    source_end_line=source.line_end,

                    source_docstring=source.docstring,

                    target_symbol=edge.target_symbol,

                    target_type=target.symbol_type,

                    target_file=target_file.relative_path,

                    target_start_line=target.line_start,

                    target_end_line=target.line_end,

                    target_docstring=target.docstring,

                    relation=edge.relation,

                )

            )

        return output