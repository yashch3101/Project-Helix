export interface ChatSession {
  id: string;
  title: string | null;
  updated_at: string;
}

export interface ChatSessionsResponse {
  sessions: ChatSession[];
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ChatMessagesResponse {
  messages: ChatMessage[];
}

export interface Citation {
  file_path: string;
  start_line: number;
  end_line: number;
}

export interface AssistantMessage extends ChatMessage {
    citations?: Citation[];

    trace?: ReasoningTrace;

    evidence?: Evidence[];

    impact?: Impact[];
}

export interface ReasoningTrace {

    retrieval_chunks:number;

    graph_edges:number;

    dependencies:number;

    context_chunks:number;

    graph_nodes:{
        id:string;
        label:string;
    }[];

    graph_connections:{
        source:string;
        target:string;
        relation:string;
    }[];

}

export interface Evidence {
    title: string;
    description: string;
}

export interface Impact {
    title: string;
    description: string;
}