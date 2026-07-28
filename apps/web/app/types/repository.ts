export type RepositoryStatus =
    | "PENDING"
    | "CLONING"
    | "PARSING"
    | "GRAPH"
    | "CHUNKING"
    | "EMBEDDING"
    | "INDEXING"
    | "READY"
    | "FAILED";

export interface RepositoryStatusResponse {
    status: RepositoryStatus;
    progress: number;
    current_stage: string;
    indexed_at: string | null;
    error_message: string | null;
}