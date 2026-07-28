"use client";

import {
    Database,
    GitBranch,
    Boxes,
    BrainCircuit,
    Sparkles,
    CheckCircle2,
} from "lucide-react";

type Trace = {
    retrieval_chunks: number;
    graph_edges: number;
    dependencies: number;
    context_chunks: number;
};

export default function ReasoningFlow({
    trace,
}: {
    trace: Trace;
}) {

    const steps = [

        {
            title: "Semantic Retrieval",
            icon: Database,
            value: `${trace.retrieval_chunks} chunks`,
        },

        {
            title: "Knowledge Graph",
            icon: GitBranch,
            value: `${trace.graph_edges} edges`,
        },

        {
            title: "Dependency Expansion",
            icon: Boxes,
            value: `${trace.dependencies} dependencies`,
        },

        {
            title: "Context Compression",
            icon: BrainCircuit,
            value: `${trace.context_chunks} chunks`,
        },

        {
            title: "LLM Reasoning",
            icon: Sparkles,
            value: "Gemini Analysis",
        },

        {
            title: "Final Response",
            icon: CheckCircle2,
            value: "Completed",
        },

    ];

    return (

    <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/70 backdrop-blur-md p-6">

        <div className="flex items-center justify-between mb-6">

            <div>

                <h3 className="text-lg font-semibold text-white">

                    AI Reasoning Pipeline

                </h3>

                <p className="text-sm text-zinc-500 mt-1">

                    Internal execution trace used to generate this answer.

                </p>

            </div>

            <div className="rounded-full bg-violet-500/10 border border-violet-500/20 px-3 py-1 text-xs text-violet-300">

                {steps.length} Steps

            </div>

        </div>

        <div className="space-y-5">

            {steps.map((step, index) => {

                const Icon = step.icon;

                return (

                    <div
                        key={index}
                        className="relative flex gap-4"
                    >

                        <div className="flex flex-col items-center">

                            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-500/10 border border-violet-500/20">

                                <Icon
                                    size={20}
                                    className="text-violet-300"
                                />

                            </div>

                            {index !== steps.length - 1 && (

                                <div className="mt-2 h-10 w-px bg-zinc-700"></div>

                            )}

                        </div>

                        <div className="flex-1 rounded-xl border border-zinc-800 bg-zinc-950/50 p-4 transition-all hover:border-violet-500/30">

                            <div className="flex items-center justify-between">

                                <h4 className="font-medium text-white">

                                    {step.title}

                                </h4>

                                <span className="rounded-full bg-zinc-800 px-2 py-1 text-xs text-zinc-400">

                                    Step {index + 1}

                                </span>

                            </div>

                            <p className="mt-2 text-sm text-zinc-400">

                                {step.value}

                            </p>

                        </div>

                    </div>

                );

            })}

        </div>

    </div>

    );
}