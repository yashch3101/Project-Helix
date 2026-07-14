"use client";

import { useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Citation } from "../types/chat";

type MessageProps = {
    role:"user"|"assistant";
    content:string;
    citations?: Citation[];
    onRegenerate?: ()=>void;
    onEdit?: () => void;
    onCopy?: () => void;
}

export default function Message({
  role,
  content,
  citations,
  onRegenerate,
  onEdit,
  onCopy,
}: MessageProps) {

  const [copied, setCopied] = useState(false);

  return (
    <div
      className={`mb-6 ${
        role === "user"
          ? "text-right"
          : "text-left"
      }`}
    >
      <div
        className={`
          inline-block
          max-w-4xl
          rounded-xl
          px-5
          py-3
          whitespace-pre-wrap
          break-words

          ${
            role === "user"
              ? "bg-blue-600 text-white"
              : "bg-zinc-800 text-white"
          }
        `}
      >

        {content === "Thinking..." && (

        <div className="animate-pulse text-gray-400">

            Thinking...

        </div>

        )}

        {content !== "Thinking..." && (

        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code(props) {
              const { children, className, ...rest } = props;

              const match = /language-(\w+)/.exec(
                className || ""
              );

              if (match) {

                  const code = String(children).replace(/\n$/, "");

                  return (

                      <div className="relative">

                          <button
                              onClick={() => {

                                  navigator.clipboard.writeText(code);

                                  setCopied(true);

                                  setTimeout(() => {

                                      setCopied(false);

                                  }, 2000);

                              }}
                              className="
                                  absolute
                                  right-3
                                  top-3
                                  rounded
                                  bg-zinc-700
                                  hover:bg-zinc-600
                                  px-2
                                  py-1
                                  text-xs
                                  z-10
                              "
                          >

                              {copied ? "Copied!" : "Copy"}

                          </button>

                          <SyntaxHighlighter
                              style={oneDark}
                              language={match[1]}
                              PreTag="div"
                          >

                              {code}

                          </SyntaxHighlighter>

                      </div>

                  );

              }

              return (
                <code
                  className="bg-zinc-900 px-1 py-0.5 rounded"
                  {...rest}
                >
                  {children}
                </code>
              );
            },
          }}
        >
          {content}
        </ReactMarkdown>

        )}

        {role === "user" && onEdit && (

          <div className="mt-2">

          <button
              onClick={onEdit}
              className="
              text-xs
              px-3
              py-1.5
              rounded-md
              bg-zinc-900
              hover:bg-zinc-700
              transition
            "
          >

          ✏ Edit

          </button>

          </div>

          )}

        {role === "assistant" && onCopy && (

          <button

            onClick={onCopy}

            className="
            text-xs
            px-3
            py-1.5
            rounded-md
            bg-zinc-900
            hover:bg-zinc-700
            transition
          "

          >

          📋 Copy

          </button>

          )}

        {role === "assistant" && onRegenerate && (

          <div className="mt-3 flex gap-3 items-center">

          <button

            onClick={onRegenerate}

            className="
              text-xs
              px-3
              py-1.5
              rounded-md
              bg-zinc-900
              hover:bg-zinc-700
              transition
            "

            >

            ↻ Regenerate response

          </button>

          </div>

          )}

        {citations && citations.length > 0 && (

          <div className="mt-5 border-t border-zinc-700 pt-4">

              <div className="text-sm text-gray-400 mb-2">

                  Sources

              </div>

              <div className="space-y-2">

                  {citations.map((c, index)=>(

                      <div
                          key={index}
                          className="rounded-lg bg-zinc-900 px-3 py-2 text-sm"
                      >

                          <div className="font-medium">

                              {c.file_path}

                          </div>

                          <div className="text-gray-500">

                              Lines {c.start_line} - {c.end_line}

                          </div>

                      </div>

                  ))}

              </div>

          </div>

          )}
      </div>
    </div>
  );
}