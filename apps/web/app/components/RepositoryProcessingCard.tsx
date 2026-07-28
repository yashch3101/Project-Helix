import { useEffect, useState } from "react";

import type { RepositoryStatus } from "../types/repository";

type Props = {
    progress: number;
    stage: string;
    status: RepositoryStatus;
};

const steps = [
    "CLONING",
    "PARSING",
    "GRAPH",
    "CHUNKING",
    "EMBEDDING",
    "INDEXING",
];

const labels: Record<string, string> = {
    CLONING: "Clone Repository",
    PARSING: "Scan & Parse Files",
    GRAPH: "Knowledge Graph",
    CHUNKING: "Create Semantic Chunks",
    EMBEDDING: "Generate Embeddings",
    INDEXING: "Build Hybrid Search",
};

export default function RepositoryProcessingCard({
    progress,
    stage,
    status,
}: Props) {

const currentIndex = steps.indexOf(status);

const aiMessages: Record<string, string> = {
    CLONING: "Downloading repository from GitHub...",
    PARSING: "Reading and understanding your code...",
    GRAPH: "Building repository knowledge graph...",
    CHUNKING: "Creating semantic chunks for retrieval...",
    EMBEDDING: "Generating AI embeddings...",
    INDEXING: "Preparing hybrid search index...",
    READY: "Repository intelligence is ready.",
    FAILED: "Repository processing failed.",
};

const displayMessage =
    aiMessages[status] ??
    stage;

const tips = [
    "Project Helix understands repository structure, not just keywords.",
    "Hybrid search combines embeddings with BM25 for better retrieval.",
    "Knowledge Graph helps AI understand relationships between files.",
    "Large repositories may take slightly longer to process.",
];

const [tipIndex, setTipIndex] = useState(0);

useEffect(() => {

    if (status === "READY") return;

    const timer = setInterval(() => {

        setTipIndex((prev) => (prev + 1) % tips.length);

    }, 5000);

    return () => clearInterval(timer);

}, [status]);

    if (status === "FAILED") {

        return (

            <div
                className="
                    mx-3
                    mb-3
                    rounded-xl
                    border
                    border-red-500/30
                    bg-red-500/10
                    p-4
                "
            >

                <div className="flex items-center gap-3">

                    <span className="text-2xl">
                        ❌
                    </span>

                    <div>

                        <p className="font-semibold text-red-300">
                            Repository Processing Failed
                        </p>

                        <p className="text-sm text-red-200 mt-1">
                            {stage}
                        </p>

                    </div>

                </div>

                <div className="mt-4 rounded-lg bg-zinc-950 p-3">

                    <p className="text-sm text-zinc-300">

                        Please fix the issue and try importing
                        or syncing the repository again.

                    </p>

                </div>

            </div>

        );

    }

    return (

        <div
            className="
                mx-3
                mb-3
                rounded-xl
                border
                border-zinc-800
                bg-zinc-900
                p-4
            "
        >

            <div className="flex items-center gap-2">

                <span className="animate-pulse text-xl">
                    ⚡
                </span>

                <div>

                    <p className="font-semibold">
                        {status === "READY"
                            ? "Repository Ready"
                            : "Building Repository Intelligence"}
                    </p>

                    <p className="text-xs text-zinc-500">

                        {status === "READY"
                            ? "Repository intelligence is ready."
                            : "AI is analyzing your repository. This usually takes 1–2 minutes."
                        }

                    </p>

                </div>

            </div>

            <div className="mt-4">

                <div className="h-2 rounded-full bg-zinc-800 overflow-hidden">

                    <div
                        className="h-full rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500 transition-[width] ease-in-out duration-700"
                        style={{
                            width: `${progress}%`,
                        }}
                    />

                </div>

                <div className="mt-2 flex justify-between text-xs">

                    <span className="text-violet-300 font-medium">
                        {displayMessage}
                    </span>

                    <span>

                        {progress}% Complete

                    </span>

                </div>

                <div className="mt-4 flex items-center justify-between text-xs text-zinc-500">

                    <span>

                        Estimated Time

                    </span>

                    <span>

                        {status === "READY"
                            ? "Completed"
                            : "~1-2 min"}

                    </span>

                </div>

                <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-950 p-3">

                    <p className="text-xs text-zinc-400">

                        💡 AI Tip

                    </p>

                    <p className="mt-1 text-sm text-zinc-300">

                        {tips[tipIndex]}

                    </p>

                </div>

                <div className="mt-5 space-y-2">

                    {steps.map((item, index) => {

                        let icon = "○";

                        if (index < currentIndex) {
                            icon = "✅";
                        } else if (index === currentIndex) {
                            icon = "⏳";
                        }

                        if (status === "READY") {
                            icon = "✅";
                        }

                        return (

                            <div
                                key={item}
                                className={`flex items-center gap-2 rounded-lg px-2 py-1 transition-all duration-300 ${
                                    index === currentIndex
                                        ? "border border-violet-500/20 bg-violet-500/10 shadow-[0_0_12px_rgba(139, 92, 246, 0.15)]"
                                        : ""
                                }`}
                            >
                                <span
                                    className={
                                        index < currentIndex || status === "READY"
                                            ? "text-green-400"
                                            : index === currentIndex
                                            ? "animate-pulse text-violet-400"
                                            : "text-zinc-500"
                                    }
                                >
                                    {icon}
                                </span>

                                <span
                                    className={
                                        index < currentIndex || status === "READY"
                                            ? "text-zinc-100"
                                            : index === currentIndex
                                            ? "text-violet-300"
                                            : "text-zinc-500"
                                    }
                                >
                                    {labels[item]}
                                </span>
                            </div>

                        );

                    })}

                </div>

            </div>

        </div>

    );

}