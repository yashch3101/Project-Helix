"use client";

import {
    FileText,
    FileCode2,
    Hash,
} from "lucide-react";

import { Evidence } from "../types/chat";

type Props = {
    evidence?: Evidence[];
};

export default function EvidencePanel({
    evidence,
}: Props) {

    if (!evidence || evidence.length === 0)
        return null;

    return (

        <div className="mt-8">

            <div className="flex items-center gap-2 mb-5">

                <FileText className="h-5 w-5 text-violet-400" />

                <div>

                    <h3 className="text-xl font-semibold">

                        Retrieved Evidence

                    </h3>

                    <p className="text-sm text-zinc-500">

                        Source code chunks used to generate this answer

                    </p>

                </div>

            </div>

            <div className="space-y-4">

                {evidence.map((item, index)=>(

                    <div
                        key={index}
                        className="
                            rounded-2xl
                            border
                            border-zinc-800
                            bg-zinc-900/70
                            backdrop-blur
                            p-5
                            transition-all
                            duration-300
                            hover:border-violet-500/40
                            hover:shadow-lg
                            hover:shadow-violet-500/10
                        "
                    >

                        <div className="flex items-start justify-between">

                            <div>

                                <div className="flex items-center gap-2">

                                    <FileCode2 className="h-4 w-4 text-violet-400" />

                                    <h4 className="font-semibold text-white">

                                        {item.symbol}

                                    </h4>

                                </div>

                                <p className="mt-2 text-sm text-zinc-400">

                                    {item.chunk_type}

                                </p>

                            </div>

                            <span
                                className="
                                    rounded-full
                                    border
                                    border-violet-500/30
                                    bg-violet-500/10
                                    px-3
                                    py-1
                                    text-xs
                                    text-violet-300
                                "
                            >

                                Evidence

                            </span>

                        </div>

                        <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500">

                            <Hash className="h-4 w-4" />

                            Lines {item.lines}

                        </div>

                    </div>

                ))}

            </div>

        </div>

    );

}