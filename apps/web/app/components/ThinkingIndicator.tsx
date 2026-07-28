"use client";

const STAGES = [
    "🧠 Understanding your question...",
    "🔍 Searching repository...",
    "📚 Reading relevant files...",
    "⚡ Generating answer...",
];

export default function ThinkingIndicator() {

    return (

        <div className="space-y-3">

            {STAGES.map((stage,index)=>(

                <div
                    key={stage}
                    className="flex items-center gap-3 animate-pulse"
                    style={{
                        animationDelay:`${index*0.2}s`
                    }}
                >

                    <div className="h-2 w-2 rounded-full bg-violet-500"/>

                    <span className="text-zinc-400">

                        {stage}

                    </span>

                </div>

            ))}

        </div>

    );

}