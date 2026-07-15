"use client";

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

        <div className="mt-6">

            <h3 className="font-semibold mb-3">

                📄 Retrieved Evidence

            </h3>

            <div className="space-y-2">

                {evidence.map((item, index)=>(

                    <div
                        key={index}
                        className="rounded-lg bg-zinc-900 p-3"
                    >

                        <div className="font-medium">

                            {item.symbol}

                        </div>

                        <div className="text-sm text-gray-400">

                            {item.chunk_type}

                        </div>

                        <div className="text-xs text-gray-500">

                            Lines {item.lines}

                        </div>

                    </div>

                ))}

            </div>

        </div>

    );

}