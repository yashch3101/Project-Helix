"use client";

import { useEffect, useState } from "react";

import { getProjects } from "../services/project";

type Project = {
  id: string;
  name: string;
  description?: string;
};

type Props = {
  selectedProject: string | null;
  onSelect: (id: string) => void;
};

export default function ProjectSelector({
  selectedProject,
  onSelect,
}: Props) {

  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {

    async function load() {

      try {

        const data = await getProjects();

        setProjects(data);

        if (data.length > 0 && !selectedProject) {

          onSelect(data[0].id);

        }

      } catch (err) {

        console.error(err);

      }

    }

    load();

  }, []);

  return (

    <div className="px-3 py-3">

      <select

        value={selectedProject ?? ""}

        onChange={(e)=>onSelect(e.target.value)}

        className="
          w-full
          rounded-lg
          bg-zinc-800
          px-3
          py-2
          outline-none
        "

      >

        {projects.map(project=>(

          <option

            key={project.id}

            value={project.id}

          >

            {project.name}

          </option>

        ))}

      </select>

    </div>

  );

}