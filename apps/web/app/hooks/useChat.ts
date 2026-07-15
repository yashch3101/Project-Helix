"use client";

import { useEffect, useState } from "react";

import { ChatMessage, AssistantMessage, Evidence, Impact } from "../types/chat";
import { getMessages, sendMessage  } from "../services/chat";

export function useChat(
    sessionId: string | null
) {

  const [messages, setMessages] = useState<AssistantMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [controller, setController] = useState<AbortController | null>(null);
  const [lastQuestion, setLastQuestion] = useState("");
  const [editingQuestion, setEditingQuestion] = useState("");

  useEffect(() => {

    if (!sessionId) {

        setMessages([]);

        return;

    }

    loadMessages(sessionId);

}, [sessionId]);

  async function loadMessages(sessionId: string) {

    setLoading(true);

    try {

      const data = await getMessages(sessionId);

      setMessages(data.messages);

    } finally {

      setLoading(false);

    }

  }

  async function ask(
    sessionId: string,
    question: string
    ) {

        setLastQuestion(question);

    // User message instantly show

    const userMessage: ChatMessage = {

        id: crypto.randomUUID(),

        role: "user",

        content: question,

        created_at: new Date().toISOString(),

    };

    // Empty assistant message

    const assistantMessage: ChatMessage = {

        id: crypto.randomUUID(),

        role: "assistant",

        content: "Thinking...",

        created_at: new Date().toISOString(),

    };

    setMessages(prev => [

        ...prev,

        userMessage,

        assistantMessage,

    ]);

    setIsStreaming(true);

    const abortController = new AbortController();

    setController(abortController);

    const response = await sendMessage(
        sessionId,
        question,
        abortController.signal
    );

    if (!response.body) return;

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {

        const { done, value } =
        await reader.read();

        if (done) break;

        buffer += decoder.decode(value);

        const events = buffer.split("\n\n");

        buffer = events.pop() || "";

        for (const raw of events) {

        if (!raw.startsWith("event:")) continue;

        const lines = raw.split("\n");

        const event =
            lines[0].replace("event: ", "");

        const data =
            lines[1].replace("data: ", "");

        if (event === "token") {

            const token =
            JSON.parse(data);

            setMessages(prev => {

            const copy = [...prev];

            copy[copy.length - 1] = {

                ...copy[copy.length - 1],

                content:
                copy[copy.length - 1].content === "Thinking..."
                    ? token
                    : copy[copy.length - 1].content + token,

            };

            return copy;

            });

        }

        if (event === "reasoning") {

            const reasoning = JSON.parse(data);

            console.log("========== REASONING ==========");
            console.log(reasoning);
            console.log("===============================");

            setMessages(prev => {

                const copy = [...prev];

                copy[copy.length - 1] = {

                    ...copy[copy.length - 1],

                    trace: reasoning.trace,

                };

                return copy;

            });

        }

        if (event === "citations") {

            const citations = JSON.parse(data);

            setMessages(prev => {

                const copy = [...prev];

                copy[copy.length - 1] = {

                    ...copy[copy.length - 1],

                    citations,

                };

                return copy;

            });

        }

        if (event === "evidence") {

            console.log("EVIDENCE EVENT");
            console.log(data);

            const evidence: Evidence[] =
                JSON.parse(data);

            setMessages(prev => {

                const copy = [...prev];

                copy[copy.length - 1] = {

                    ...copy[copy.length - 1],

                    evidence,

                };

                return copy;

            });

        }

        if (event === "impact") {

            console.log("IMPACT EVENT");
            console.log(data);

            const impact: Impact[] =
                JSON.parse(data);

            setMessages(prev => {

                const copy = [...prev];

                copy[copy.length - 1] = {

                    ...copy[copy.length - 1],

                    impact,

                };

                return copy;

            });

        }

        }

    }

    setIsStreaming(false);

    }

  return {
    messages,
    setMessages,

    loading,
    setLoading,

    isStreaming,

    loadMessages,
    ask,

    stopGeneration() {

        controller?.abort();

        setController(null);

        setIsStreaming(false);

    },

    lastQuestion,

    async regenerate(sessionId: string) {

        if (!lastQuestion) return;

        setMessages((prev) => {

            const copy = [...prev];

            if (
                copy.length > 0 &&
                copy[copy.length - 1].role === "assistant"
            ) {
                copy.pop();
            }

            return copy;
        });

        await ask(sessionId, lastQuestion);

    },

    editingQuestion,

    setEditingQuestion,
  };

}