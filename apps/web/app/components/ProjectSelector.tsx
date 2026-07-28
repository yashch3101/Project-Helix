"use client";

import { useEffect, useState } from "react";

import { getProjects } from "../services/project";

import CreateProjectModal from "./CreateProjectModal";

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
  const [openModal, setOpenModal] = useState(false);

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

  if (projects.length === 0) {

    return (
        <>
            <div className="px-3 py-3">

                <div className="rounded-xl border border-dashed border-zinc-700 p-4">

                    <p className="text-sm font-semibold">
                        No Projects Yet
                    </p>

                    <p className="mt-1 text-xs text-zinc-500">
                        Create your first project to get started.
                    </p>

                    <button
                        onClick={() => setOpenModal(true)}
                        className="
                            mt-4
                            w-full
                            rounded-lg
                            bg-violet-600
                            py-2
                            text-sm
                            font-medium
                        "
                    >
                        + Create Project
                    </button>

                </div>

            </div>

            <CreateProjectModal
                open={openModal}
                onClose={() => setOpenModal(false)}
                onCreated={async () => {

                    const data = await getProjects();

                    setProjects(data);

                    if (data.length > 0) {

                        onSelect(data[0].id);

                    }

                }}
            />
        </>
    );

}

  return (
      <>
          <div className="px-3 py-3">

              <select
                  value={selectedProject ?? ""}
                  onChange={(e) => onSelect(e.target.value)}
                  className="
                      w-full
                      rounded-lg
                      bg-zinc-800
                      px-3
                      py-2
                      outline-none
                  "
              >

                  {projects.map((project) => (

                      <option
                          key={project.id}
                          value={project.id}
                      >
                          {project.name}
                      </option>

                  ))}

              </select>

          </div>

          <CreateProjectModal
              open={openModal}
              onClose={() => setOpenModal(false)}
              onCreated={async () => {

                  const data = await getProjects();

                  setProjects(data);

                  if (data.length > 0) {

                      onSelect(data[0].id);

                  }

              }}
          />
      </>
  );

}