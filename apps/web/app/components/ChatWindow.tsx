"use client";

import { useEffect, useRef } from "react";
import { useChat } from "../hooks/useChat";

import ChatInput from "./ChatInput";
import Message from "./Message";

type ChatWindowProps = {
  sessionId: string | null;
  repositoryId:string|null;
};

export default function ChatWindow({
  sessionId,
  repositoryId,
}: ChatWindowProps) {

  const {
    messages,
    loading,
    isStreaming,
    ask,
    stopGeneration,
    regenerate,
    editingQuestion,
    setEditingQuestion,
  } = useChat(sessionId);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

  bottomRef.current?.scrollIntoView({
    behavior: "smooth",
  });

}, [messages]);

  return (
    <div className="flex-1 flex flex-col">
      <section className="flex-1 overflow-y-auto p-8">

        {!sessionId && (
          <div className="h-full flex items-center justify-center text-gray-500">
            Select a chat
          </div>
        )}

        {loading && (
          <div className="text-gray-400">
            Loading...
          </div>
        )}

        {!loading &&
          messages.map((message, index) => (

          <Message
            key={message.id}
            role={message.role}
            content={message.content}
            citations={message.citations}
            trace={message.trace}
            evidence={message.evidence}
            impact={message.impact}

            onCopy={
              message.role === "assistant"
              ? async () => {

                  await navigator.clipboard.writeText(
                      message.content
                  );

              }
              : undefined
          }

            onEdit={
                message.role === "user"
                ? () => {

                    setEditingQuestion(
                        message.content
                    );

                }
                : undefined
            }

            onRegenerate={
                message.role === "assistant" &&
                index === messages.length - 1
                    ? () => {
                          if (sessionId) {
                              regenerate(sessionId);
                          }
                      }
                    : undefined
            }
          />

        ))}

        {isStreaming && (

          <div className="mb-6 text-left">

            <div
              className="
                inline-block
                rounded-xl
                bg-zinc-800
                px-5
                py-3
              "
            >

              <span className="animate-pulse">

                ▌

              </span>

            </div>

          </div>

        )}
        
        <div ref={bottomRef} />

      </section>

      <ChatInput
          disabled={!sessionId}

          isStreaming={isStreaming}

          stopGeneration={stopGeneration}

          onSend={(question) => {

              if (!sessionId) return;

              ask(sessionId, question);

          }}
      />
    </div>
  );
}