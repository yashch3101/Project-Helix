"use client";

import { ReactNode } from "react";
import Link from "next/link";
import {
    BrainCircuit,
    GitBranch,
    Search,
    Sparkles,
} from "lucide-react";

interface AuthLayoutProps {
    title: string;
    subtitle: string;
    footerText: string;
    footerLinkText: string;
    footerHref: string;
    children: ReactNode;
}

const features = [
    {
        icon: BrainCircuit,
        title: "AI Repository Intelligence",
        description:
            "Understand complex repositories using LLM-powered reasoning.",
    },
    {
        icon: Search,
        title: "Semantic Code Search",
        description:
            "Search across your entire codebase using natural language.",
    },
    {
        icon: GitBranch,
        title: "Knowledge Graph",
        description:
            "Visualize dependencies, symbols and relationships instantly.",
    },
];

export default function AuthLayout({
    title,
    subtitle,
    footerText,
    footerLinkText,
    footerHref,
    children,
}: AuthLayoutProps) {
    return (
        <div className="relative flex min-h-screen overflow-hidden bg-zinc-950">

            {/* Background Glow */}

            <div className="absolute left-[-150px] top-[-150px] h-[450px] w-[450px] rounded-full bg-violet-700/20 blur-[120px]" />

            <div className="absolute bottom-[-150px] right-[-150px] h-[450px] w-[450px] rounded-full bg-fuchsia-700/20 blur-[120px]" />

            {/* Left */}

            <div className="hidden lg:flex w-1/2 flex-col justify-between border-r border-white/5 px-20 py-16">

                <div>

                    <div className="mb-8 flex items-center gap-3">

                        <div className="rounded-xl bg-violet-600 p-3">

                            <Sparkles className="h-6 w-6" />

                        </div>

                        <div>

                            <h1 className="text-3xl font-bold">

                                Project Helix

                            </h1>

                            <p className="text-zinc-400">

                                Autonomous AI Repository Intelligence

                            </p>

                        </div>

                    </div>

                    <h2 className="max-w-lg text-5xl font-bold leading-tight">

                        Build with an AI that truly understands your code.

                    </h2>

                    <p className="mt-6 max-w-xl text-lg leading-8 text-zinc-400">

                        Repository search, reasoning, dependency graphs,
                        documentation and code intelligence — all powered by AI.

                    </p>

                </div>

                <div className="space-y-6">

                    {features.map((feature) => {

                        const Icon = feature.icon;

                        return (

                            <div
                                key={feature.title}
                                className="flex items-start gap-4"
                            >

                                <div className="rounded-lg bg-zinc-900 p-3">

                                    <Icon className="h-5 w-5 text-violet-400" />

                                </div>

                                <div>

                                    <h3 className="font-semibold">

                                        {feature.title}

                                    </h3>

                                    <p className="mt-1 text-sm text-zinc-400">

                                        {feature.description}

                                    </p>

                                </div>

                            </div>

                        );

                    })}

                </div>

            </div>

            {/* Right */}

            <div className="flex flex-1 items-center justify-center px-6">

                <div className="w-full max-w-md rounded-3xl border border-white/10 bg-zinc-900/70 p-10 shadow-2xl backdrop-blur-xl">

                    <h2 className="text-3xl font-bold">

                        {title}

                    </h2>

                    <p className="mt-2 text-zinc-400">

                        {subtitle}

                    </p>

                    <div className="mt-10">

                        {children}

                    </div>

                    <div className="mt-8 text-center text-sm text-zinc-400">

                        {footerText}{" "}

                        <Link
                            href={footerHref}
                            className="font-medium text-violet-400 hover:text-violet-300"
                        >
                            {footerLinkText}
                        </Link>

                    </div>

                </div>

            </div>

        </div>
    );
}