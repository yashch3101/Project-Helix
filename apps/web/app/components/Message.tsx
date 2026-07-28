"use client";

import { useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Citation, Evidence, Impact } from "../types/chat";
import ReasoningPanel from "./ReasoningPanel";
import EvidencePanel from "./EvidencePanel";
import ReasoningFlow from "./ReasoningFlow";
import CodeGraph from "./CodeGraph";
import { ReasoningTrace } from "../types/chat";
import ThinkingIndicator from "./ThinkingIndicator";

type MessageProps = {
    role:"user"|"assistant";
    content:string;
    citations?: Citation[];

    trace?: ReasoningTrace;

    evidence?: Evidence[];

    impact?: Impact[];

    onRegenerate?: ()=>void;
    onEdit?: () => void;
    onCopy?: () => void;
}

export default function Message({
  role,
  content,
  citations,
  trace,
  evidence,
  impact,
  onRegenerate,
  onEdit,
  onCopy,
}: MessageProps) {

  console.log("TRACE:", trace);

  const [copied, setCopied] = useState(false);

  const isThinking = content === "Thinking...";

  const renderedContent =
      role === "assistant" && !isThinking
          ? `${content}▌`
          : content;

  return (
    <div
      className={`
        mb-8
        flex
        ${role === "user"
          ? "justify-end"
          : "justify-start"}
      `}
    >
      <div
        className={`
          relative
          max-w-5xl
          w-fit
          rounded-2xl
          border
          shadow-xl
          backdrop-blur-md
          px-6
          py-5
          transition-all
          duration-300

          whitespace-pre-wrap
          break-words

          ${
            role==="user"

            ?`
            bg-gradient-to-br
            from-blue-600
            to-blue-700
            border-blue-500/40
            text-white
            `

            :`
            bg-zinc-900/80
            border-zinc-700
            text-zinc-100
            `
            }
        `}
      >

      <div className="mb-4 flex items-center gap-3">

        {role === "user" ? (

          <>
            <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center font-bold">
              Y
            </div>

            <div>
              <div className="font-semibold">
                You
              </div>
            </div>
          </>

        ) : (

          <>
            <div className="h-10 w-10 rounded-full bg-violet-600 flex items-center justify-center">
              ⚡
            </div>

            <div>
              <div className="font-semibold">
                Project Helix
              </div>

              <div className="text-xs text-zinc-400">
                Repository Intelligence
              </div>
            </div>
          </>

        )}

      </div>

        {content === "Thinking..." && (

            <ThinkingIndicator />

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
          {renderedContent}
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

        {role === "assistant" && (

          <div className="mt-5 flex flex-wrap gap-3">

              {onCopy && (

                  <button
                      onClick={onCopy}
                      className="
                      h-9
                      rounded-lg
                      border
                      border-zinc-700
                      px-4
                      text-sm
                      hover:bg-zinc-800
                      transition
                      "
                  >
                      📋 Copy
                  </button>

              )}

              {onRegenerate && (

                  <button
                      onClick={onRegenerate}
                      className="
                      h-9
                      rounded-lg
                      border
                      border-zinc-700
                      px-4
                      text-sm
                      hover:bg-zinc-800
                      transition
                      "
                  >
                      ↻ Regenerate
                  </button>

              )}

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

          {role === "assistant" && (

            <>
                <ReasoningPanel
                    trace={trace}
                />

                {trace && (

                  <ReasoningFlow
                      trace={trace}
                  />

              )}

                <EvidencePanel
                    evidence={evidence}
                />

                <CodeGraph
                  trace={trace}
              />
            </>

        )}
      </div>
    </div>
  );
}