"use client";

type Props = {
    status: string;
    progress: number;
    currentStage: string;
};

export default function RepositoryStatsCard({
    status,
    progress,
    currentStage,
}: Props) {
    return (
        <div className="mx-3 mb-4 rounded-xl border border-zinc-800 bg-zinc-900 p-4">

            <h3 className="mb-4 text-sm font-semibold text-zinc-300">
                Repository Statistics
            </h3>

            <div className="space-y-3 text-sm">

                <div className="flex justify-between">
                    <span className="text-zinc-500">Status</span>
                    <span className="font-medium text-white">
                        {status}
                    </span>
                </div>

                <div className="flex justify-between">
                    <span className="text-zinc-500">Progress</span>
                    <span className="font-medium text-white">
                        {progress}%
                    </span>
                </div>

                <div className="flex justify-between">
                    <span className="text-zinc-500">Stage</span>
                    <span className="font-medium text-white">
                        {currentStage}
                    </span>
                </div>

            </div>

        </div>
    );
}