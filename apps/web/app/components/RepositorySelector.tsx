"use client";

import { useEffect, useState } from "react";

import { getRepositories } from "../services/repository";

type Repository = {
  id: string;
  name: string;
  status: string;
  progress: number;
  current_stage: string;
  github_url: string;
};

type Props = {
  projectId: string;
  selectedRepository: string | null;
  refreshKey:number;
  onSelect: (id: string) => void;
};

export default function RepositorySelector({
  projectId,
  selectedRepository,
  refreshKey,
  onSelect,
}: Props) {

  const [repositories, setRepositories] = useState<Repository[]>([]);

  useEffect(() => {
    if (!projectId && repositories.length > 0) {
        setRepositories([]);
    }
}, [projectId, repositories.length]);

  useEffect(() => {

    if (!projectId) {
        return;
    }

    async function load() {

        try {

            const data = await getRepositories(projectId);

            setRepositories(data);

            if (data.length > 0 && !selectedRepository) {

                onSelect(data[0].id);

            }

        } catch (err) {

            console.error(err);

        }

    }

    load();

}, [projectId, refreshKey]);

if (!projectId) {
    return null;
}

if (repositories.length === 0) {
    return (
        <div className="px-3 pb-3">
            <div className="rounded-xl border border-dashed border-zinc-700 p-4 text-center">

                <p className="text-sm font-semibold text-zinc-300">
                    No Repository Yet
                </p>

                <p className="mt-1 text-xs text-zinc-500">
                    Import your first repository.
                </p>

            </div>
        </div>
    );
}

return (

    <div className="px-3 pb-3">

      <select

        value={selectedRepository ?? ""}

        onChange={(e) => {

            onSelect(e.target.value);

        }}

        className="
          w-full
          rounded-lg
          bg-zinc-800
          px-3
          py-2
          outline-none
        "

      >

        {repositories.map(repo=>(

          <option
            key={repo.id}
            value={repo.id}
          >

            {repo.name}

          </option>

        ))}

      </select>

    </div>

  );

}