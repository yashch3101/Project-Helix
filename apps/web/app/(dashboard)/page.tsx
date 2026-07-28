"use client";

import { useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import type { RepositoryStatusResponse } from "../types/repository";

export default function Home() {

  const [selectedSession, setSelectedSession] = useState<string | null>(null);
  const [selectedRepository, setSelectedRepository] = useState<string | null>(null);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [repositoryRefreshKey, setRepositoryRefreshKey] = useState(0);

const [repositoryStatus, setRepositoryStatus] = useState<RepositoryStatusResponse | null>(null);

  return (
    <main className="flex h-screen">

      <Sidebar
        selectedSession={selectedSession}
        setSelectedSession={setSelectedSession}

        selectedRepository={selectedRepository}
        setSelectedRepository={setSelectedRepository}

        selectedProject={selectedProject}
        setSelectedProject={setSelectedProject}

        repositoryRefreshKey={repositoryRefreshKey}
        triggerRepositoryRefresh={() =>
            setRepositoryRefreshKey(prev => prev + 1)
        }

        repositoryStatus={repositoryStatus}
        setRepositoryStatus={setRepositoryStatus}
      />

      <ChatWindow
        sessionId={selectedSession}
        repositoryId={selectedRepository}
        repositoryStatus={repositoryStatus}
      />

    </main>
  );
}