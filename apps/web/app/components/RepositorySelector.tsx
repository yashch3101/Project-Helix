"use client";

import { useEffect, useState } from "react";

import { getRepositories } from "../services/repository";

type Repository = {
  id: string;
  name: string;
  status: string;
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

    if (!projectId) {

        setRepositories([]);

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