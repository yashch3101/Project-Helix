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
}