"use client";

import { Trace } from "../types/chat";

type Props = {

    trace?: Trace;

};

export default function ReasoningPanel({

    trace,

}: Props) {

    if (!trace) return null;

    return (

        <div className="mt-5 rounded-xl bg-zinc-900 border border-zinc-800 p-4">

            <h3 className="font-semibold text-white mb-4">

                🧠 Reasoning

            </h3>

            <div className="grid grid-cols-2 gap-4">

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

        <div className="rounded-lg bg-zinc-800 p-3">

            <div className="text-sm text-zinc-400">

                {label}

            </div>

            <div className="text-2xl font-bold mt-1">

                {value}

            </div>

        </div>

    );

}