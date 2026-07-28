"use client";

import { useEffect, useRef } from "react";
import { useChat } from "../hooks/useChat";

import ChatInput from "./ChatInput";
import Message from "./Message";
import RepositoryTimeline from "./RepositoryTimeline";

type RepositoryStatus = {
    status: string;
    progress: number;
    current_stage: string;
    indexed_at: string | null;
    error_message: string | null;
};

type ChatWindowProps = {
  sessionId: string | null;
  repositoryId:string|null;
  repositoryStatus: RepositoryStatus | null;
};

export default function ChatWindow({
  sessionId,
  repositoryId,
  repositoryStatus,
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

  const repositoryReady = repositoryStatus?.status === "READY";

  console.log({
    sessionId,
    repositoryId,
    repositoryStatus,
    repositoryReady,
  });

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  return (
    <div className="flex-1 flex flex-col">
      <section className="flex-1 overflow-y-auto p-8">

        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">

            <div className="max-w-3xl text-center">

              {!repositoryReady && repositoryStatus && (

                  <RepositoryTimeline
                      status={repositoryStatus.status}
                      progress={repositoryStatus.progress}
                      currentStage={repositoryStatus.current_stage}
                  />

              )}

              <div className="mb-8 text-7xl">

                  ⚡

              </div>

              <h1 className="text-5xl font-bold tracking-tight">

                  Project Helix

              </h1>

              <p className="mt-4 text-lg text-zinc-400">

                  AI-powered Repository Intelligence

              </p>

              <p className="mt-2 text-zinc-500">

                  Ask questions about your codebase and understand any repository instantly.

              </p>

              <div className="mt-12 grid grid-cols-2 gap-4">

                  <button
                    disabled={!repositoryReady}
                    onClick={() => {

                        if (sessionId) {

                            ask(
                                sessionId,
                                "Explain authentication flow"
                            );

                        }

                    }}
                    className="
                        rounded-2xl
                        border
                        border-zinc-800
                        bg-zinc-900
                        p-5
                        text-left
                        transition
                        hover:border-violet-500
                        hover:bg-zinc-800
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                    "
                >

                    🔍 Explain authentication flow

                </button>

                  <button
                    disabled={!repositoryReady}
                    onClick={() => {

                        if (sessionId) {

                            ask(
                                sessionId,
                                "Find JWT implementation"
                            );

                        }

                    }}
                    className="
                        rounded-2xl
                        border
                        border-zinc-800
                        bg-zinc-900
                        p-5
                        text-left
                        transition
                        hover:border-violet-500
                        hover:bg-zinc-800
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                    "
                >

                    📂 Find JWT implementation

                </button>

                  <button
                    disabled={!repositoryReady}
                    onClick={() => {

                        if (sessionId) {

                            ask(
                                sessionId,
                                "Trace execution flow"
                            );

                        }

                    }}
                    className="rounded-2xl
                        border
                        border-zinc-800
                        bg-zinc-900
                        p-5
                        text-left
                        transition
                        hover:border-violet-500
                        hover:bg-zinc-800
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                      "
                >

                🧠 Trace execution flow

                </button>

                  <button
                    disabled={!repositoryReady}
                    onClick={() => {

                        if (sessionId) {

                            ask(
                                sessionId,
                                "Explain repository architecture"
                            );

                        }

                    }}
                    className="rounded-2xl
                        border
                        border-zinc-800
                        bg-zinc-900
                        p-5
                        text-left
                        transition
                        hover:border-violet-500
                        hover:bg-zinc-800
                        disabled:opacity-50
                        disabled:cursor-not-allowed
                      "
                >

                ⚙ Explain repository architecture

                </button>

              </div>

          </div>

          </div>
        )}

        {loading && (

          <div className="space-y-6">

            {[1, 2, 3].map((item) => (

              <div
                key={item}
                className="
                  animate-pulse
                  rounded-xl
                  border
                  border-zinc-800
                  bg-zinc-900
                  p-5
                "
              >

                <div className="mb-4 h-4 w-40 rounded bg-zinc-700" />

                <div className="mb-2 h-3 rounded bg-zinc-800" />

                <div className="mb-2 h-3 w-10/12 rounded bg-zinc-800" />

                <div className="h-3 w-8/12 rounded bg-zinc-800" />

              </div>

            ))}

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

              <div
                  className="
                  inline-flex
                  items-center
                  gap-2
                  rounded-xl
                  border
                  border-zinc-800
                  bg-zinc-900
                  px-5
                  py-3
                "
                >

                <div
                  className="
                  h-2
                  w-2
                  rounded-full
                  bg-violet-500
                  animate-ping
                "/>

                Thinking...

                </div>

            </div>

          </div>

        )}
        
        <div ref={bottomRef} />

      </section>

      <ChatInput
          disabled={!sessionId}
          repositoryReady={repositoryReady}
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