"use client";

import { useState } from "react";

type ChatInputProps = {
  onSend: (question: string) => void;
  disabled?: boolean;

  isStreaming: boolean;

  stopGeneration: () => void;

  question?: string;

  onQuestionChange?: (
    value:string
    )=>void;
};

export default function ChatInput({
  onSend,
  disabled,
  isStreaming,
  stopGeneration,
}: ChatInputProps) {

  const [question, setQuestion] = useState("");

  function handleSend() {

    if (!question.trim()) return;

    onSend(question);

    setQuestion("");
  }

  return (

    <div className="border-t border-[#303030] p-4 flex gap-3">

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
        placeholder="Message Project Helix..."
        className="
          flex-1
          rounded-xl
          bg-[#2b2b2b]
          px-5
          py-4
          outline-none
        "
      />

      {isStreaming ? (

        <button
          onClick={stopGeneration}
          className="
            bg-red-600
            hover:bg-red-500
            px-7
            rounded-xl
          "
        >
          Stop
        </button>

      ) : (

        <button
          onClick={handleSend}
          disabled={disabled}
          className="
            bg-blue-600
            hover:bg-blue-700
            px-7
            rounded-xl
          "
        >
          Send
        </button>

      )}

    </div>

  );
}