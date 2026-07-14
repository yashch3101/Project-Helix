"use client";

import { useState } from "react";

type Props = {
  open: boolean;
  onClose: () => void;
  onImport: (githubUrl: string) => Promise<void>;
};

export default function ImportRepositoryModal({
  open,
  onClose,
  onImport,
}: Props) {
  const [githubUrl, setGithubUrl] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  async function handleImport() {
    if (!githubUrl.trim()) return;

    try {
      setLoading(true);

      await onImport(githubUrl);

      setGithubUrl("");

      onClose();
    } catch (err) {
      console.error(err);
      alert("Import failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

      <div className="bg-zinc-900 rounded-xl p-6 w-[520px]">

        <h2 className="text-xl font-semibold mb-5">
          Import Repository
        </h2>

        <input
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          placeholder="https://github.com/user/repository"
          className="w-full rounded-lg bg-zinc-800 px-4 py-3 outline-none"
        />

        <div className="flex justify-end gap-3 mt-6">

          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-zinc-700 hover:bg-zinc-600"
          >
            Cancel
          </button>

          <button
            onClick={handleImport}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700"
          >
            {loading ? "Importing..." : "Import"}
          </button>

        </div>

      </div>

    </div>
  );
}