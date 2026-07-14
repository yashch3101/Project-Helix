"use client";

import { useEffect, useState, useRef } from "react";
import { MoreHorizontal } from "lucide-react";
import { getSessions, createSession, deleteChat, renameChat } from "../services/chat";
import { ChatSession } from "../types/chat";
import RepositorySelector from "./RepositorySelector";
import ProjectSelector from "./ProjectSelector";
import ImportRepositoryModal from "./ImportRepositoryModal";
import { importRepository } from "../services/repository";

type SidebarProps = {
  selectedSession: string | null;
  setSelectedSession: (id: string) => void;
  selectedRepository: string | null;
  setSelectedRepository: (id:string) => void;
  selectedProject:string|null;
  setSelectedProject:(id:string)=>void;
  repositoryRefreshKey: number;
  triggerRepositoryRefresh: () => void;
};

export default function Sidebar({
  selectedSession,
  setSelectedSession,
  selectedRepository,
  setSelectedRepository,
  selectedProject,
  setSelectedProject,
  repositoryRefreshKey,
  triggerRepositoryRefresh,
}: SidebarProps) {

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [editingSession, setEditingSession] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const [editedTitle, setEditedTitle] = useState("");
  const [importOpen, setImportOpen] = useState(false);

  async function refreshSessions() {

    try {

        if (!selectedRepository) {

            setSessions([]);

            return;

        }

        const data = await getSessions(
            selectedRepository
        );

        setSessions(data.sessions);

    } catch (err) {

        console.error(err);

    }

}

useEffect(() => {

    async function load() {

        try {

            await refreshSessions();

        } finally {

            setLoading(false);

        }

    }

    load();

}, [

  selectedSession,
  selectedRepository,
  
]);

useEffect(() => {

  function handleClickOutside(
    event: MouseEvent
  ) {

    if (
      menuRef.current &&
      !menuRef.current.contains(
        event.target as Node
      )
    ) {

      setMenuOpen(null);

    }

  }

  document.addEventListener(
    "mousedown",
    handleClickOutside
  );

  return () => {

    document.removeEventListener(
      "mousedown",
      handleClickOutside
    );

  };

}, []);

  async function handleNewChat() {

  try {

    if (!selectedRepository) {

        alert("Select repository first");

        return;

    }

    const data = await createSession(
        selectedRepository
    );

    setSelectedSession(data.session_id);

    await refreshSessions();
    setMenuOpen(null);

  } catch (err) {

    console.error(err);

  }

}

async function handleImportRepository(
  githubUrl: string,
) {

  if (!selectedProject) {

    alert("Select project first");

    return;

  }

  try {

    await importRepository(
      githubUrl,
      selectedProject,
    );

    triggerRepositoryRefresh();

    alert("Repository imported successfully.");

  } catch (err) {

    console.error(err);

    alert("Repository import failed.");

  }

}

async function handleDeleteChat(
    sessionId: string
  ) {
    const ok = confirm(
      "Delete this chat?"
    );

    if (!ok) return;

    try {

      await deleteChat(sessionId);

      if (selectedSession === sessionId) {
        setSelectedSession("");
      }

      setMenuOpen(null);

      await refreshSessions();

      if (!selectedRepository) return;

      const data = await getSessions(
          selectedRepository
      );

      setSessions(data.sessions);

      if (data.sessions.length > 0) {

          setSelectedSession(
              data.sessions[0].id
          );

      } else {

          setSelectedSession("");

      }

    } catch (err) {
      console.error(err);
    }
  }

const filteredSessions = sessions.filter((session) =>
  (session.title ?? "New Chat")
    .toLowerCase()
    .includes(search.toLowerCase())
);

async function handleRename(
    sessionId: string
  ) {
    const title = editedTitle.trim();

    if (!title) {
      setEditingSession(null);
      return;
    }

    try {

      await renameChat(
        sessionId,
        title
      );

      setEditingSession(null);

      setMenuOpen(null);

      await refreshSessions();

    } catch (err) {

      console.error(err);

    }
  }

  return (

  <>
    
    <aside className="w-80 bg-[#171717] border-r border-[#303030] flex flex-col">

      {/* Top */}
      <div className="p-3 border-b border-[#303030]">

        <button
          onClick={handleNewChat}
          className="
            w-full
            rounded-xl
            bg-[#2b2b2b]
            hover:bg-[#373737]
            transition
            py-3
            font-medium
          "
        >
          + New Chat
        </button>

      </div>

      <ProjectSelector

        selectedProject={selectedProject}

        onSelect={(projectId)=>{

        setSelectedProject(projectId);

        setSelectedRepository(null);

        setSelectedSession(null);

        }}

        />

        <RepositorySelector

          projectId={selectedProject ?? ""}

          selectedRepository={selectedRepository}

          refreshKey={repositoryRefreshKey}

          onSelect={(repoId)=>{

              setSelectedRepository(repoId);

              setSelectedSession("");

          }}

      />

      <div className="px-3 pb-3">

        <button

          onClick={() => setImportOpen(true)}

          className="
            w-full
            rounded-lg
            bg-zinc-800
            hover:bg-zinc-700
            py-2
            text-sm
            transition
          "

        >

          + Import Repository

        </button>

      </div>

        {/* Chat List */}

        <div className="px-3 pt-3">

          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search chats..."
            className="
              w-full
              rounded-lg
              bg-zinc-800
              px-4
              py-2
              outline-none
              text-sm
            "
          />

        </div>

        <div className="flex-1 overflow-y-auto px-2 py-3 space-y-1">

        {loading ? (
          <p className="px-3 py-2 text-gray-400">Loading...</p>
        ) : (
          filteredSessions.map((session) => (

          <div
            key={session.id}
            className={`
              group
              flex
              items-center
              justify-between
              rounded-lg
              px-3
              py-3
              transition

              ${
                selectedSession === session.id
                  ? "bg-[#2f2f2f]"
                  : "hover:bg-[#2a2a2a]"
              }
            `}
          >

            {editingSession === session.id ? (

              <input
                autoFocus
                value={editedTitle}
                onChange={(e) =>
                  setEditedTitle(e.target.value)
                }

                onBlur={() =>
                  handleRename(session.id)
                }

                onKeyDown={(e) => {

                  if (e.key === "Enter") {

                    handleRename(session.id);

                  }

                  if (e.key === "Escape") {

                    setEditingSession(null);

                  }

                }}

                className="
                  flex-1
                  bg-zinc-800
                  rounded
                  px-2
                  py-1
                  outline-none
                "
              />

            ) : (

              <button
                onClick={() =>
                  setSelectedSession(session.id)
                }
                className="flex-1 text-left truncate"
              >
                {session.title ?? "New Chat"}
              </button>

            )}

            <div
              className="relative"
              ref={
                menuOpen === session.id
                  ? menuRef
                  : null
              }
            >

            <button

                onClick={(e)=>{

                e.stopPropagation();

                setMenuOpen(

                menuOpen===session.id

                ? null

                : session.id

                );

                }}

                  className="
                  opacity-0
                  group-hover:opacity-100
                  transition
                  p-1
                  rounded
                  hover:bg-zinc-700
                  "
                >

              <MoreHorizontal size={18}/>

            </button>

            {
            menuOpen===session.id && (

            <div
            className="
            absolute
            right-0
            top-8
            w-36
            rounded-lg
            bg-zinc-900
            border
            border-zinc-700
            shadow-xl
            z-50
            "
            >

            <button
                onClick={() => {

                  setEditingSession(session.id);

                  setEditedTitle(session.title ?? "New Chat");

                  setMenuOpen(null);

                }}
                className="
                  block
                  w-full
                  text-left
                  px-4
                  py-2
                  hover:bg-zinc-800
                "
              >
                Rename
              </button>

            <button
              onClick={() => handleDeleteChat(session.id)}
              className="
                block
                w-full
                text-left
                px-4
                py-2
                text-red-400
                hover:bg-zinc-800
              "
            >
              Delete
            </button>

            </div>

            )

            }

            </div>

          </div>

      ))
        )}

      </div>

      {/* Bottom */}

      <div className="border-t border-[#303030] p-3">

        <button className="w-full rounded-lg hover:bg-[#2a2a2a] p-3 text-left">
          👤 Yash
        </button>

      </div>

    </aside>

        <ImportRepositoryModal

          open={importOpen}

          onClose={() => setImportOpen(false)}

          onImport={handleImportRepository}

        />
    </>
  );
}