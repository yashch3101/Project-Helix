"use client";

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
            title: "Retrieval",
            icon: "🔍",
            value: `${trace.retrieval_chunks} chunks`,
        },

        {
            title: "Graph Expansion",
            icon: "🕸",
            value: `${trace.graph_edges} nodes`,
        },

        {
            title: "Dependency Expansion",
            icon: "📦",
            value: `${trace.dependencies} dependencies`,
        },

        {
            title: "Context Compression",
            icon: "🧠",
            value: `${trace.context_chunks} chunks`,
        },

        {
            title: "Gemini",
            icon: "✨",
            value: "LLM Generation",
        },

        {
            title: "Final Answer",
            icon: "✅",
            value: "Completed",
        },

    ];

    return (

        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-5">

            <h3 className="font-semibold text-white mb-5">

                🧠 AI Reasoning Flow

            </h3>

            <div className="space-y-4">

                {steps.map((step, index) => (

                    <div key={index}>

                        <div className="flex items-center gap-4">

                            <div className="text-2xl">

                                {step.icon}

                            </div>

                            <div>

                                <div className="font-medium">

                                    {step.title}

                                </div>

                                <div className="text-sm text-zinc-400">

                                    {step.value}

                                </div>

                            </div>

                        </div>

                        {index !== steps.length - 1 && (

                            <div className="ml-4 h-6 border-l border-zinc-700 mt-2"></div>

                        )}

                    </div>

                ))}

            </div>

        </div>

    );

}