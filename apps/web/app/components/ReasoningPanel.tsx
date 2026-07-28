"use client";

import { ReasoningTrace } from "../types/chat";

type Props = {

    trace?: ReasoningTrace;

};

export default function ReasoningPanel({

    trace,

}: Props) {

    if (!trace) return null;

    return (

        <div className="mt-6 rounded-2xl border border-zinc-700 bg-zinc-900/80 backdrop-blur-md shadow-xl p-6">

            <div className="mb-6 flex items-center justify-between">

                <div>

                    <h3 className="text-xl font-semibold text-white">
                        🧠 AI Reasoning
                    </h3>

                    <p className="mt-1 text-sm text-zinc-400">
                        Internal reasoning pipeline execution
                    </p>

                </div>

                <div
                    className="
                        rounded-full
                        border
                        border-violet-500/30
                        bg-violet-500/10
                        px-3
                        py-1
                        text-xs
                        font-medium
                        text-violet-300
                    "
                >
                    Completed
                </div>

            </div>

            <div className="grid grid-cols-2 gap-5">

                <Stat
                    label="Retrieval"
                    value={trace.retrieval_chunks}
                />

                <Stat
                    label="Graph"
                    value={trace.graph_edges}
                />

                <Stat
                    label="Dependency"
                    value={trace.dependencies}
                />

                <Stat
                    label="Context"
                    value={trace.context_chunks}
                />

            </div>

        </div>

    );

}

function Stat({

    label,

    value,

}: {

    label: string;

    value: number;

}) {

    return (

        <div className="rounded-xl border border-zinc-700 bg-zinc-800/60 p-5 transition duration-300 hover:border-violet-500/40 hover:bg-zinc-800">

            <div className="text-xs uppercase tracking-wider text-zinc-500">

                {label}

            </div>

            <div className="mt-3 text-4xl font-bold text-white">

                {value}

            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-zinc-700">

                <div
                    className="h-full rounded-full bg-violet-500"
                    style={{
                        width: `${Math.min(value * 10, 100)}%`,
                    }}
                />

            </div>

        </div>

    );

}