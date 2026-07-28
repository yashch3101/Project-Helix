"use client";

import { useState } from "react";
import { createProject } from "../services/project";

type Props = {
    open: boolean;
    onClose: () => void;
    onCreated: () => void;
};

export default function CreateProjectModal({
    open,
    onClose,
    onCreated,
}: Props) {

    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(false);

    if (!open) return null;

    async function handleCreate() {

        if (!name.trim()) {
            alert("Project name is required.");
            return;
        }

        setLoading(true);

        try {

            await createProject(
                name,
                description
            );

            setName("");
            setDescription("");

            onCreated();
            onClose();

        } catch (err) {

            console.error(err);

            alert("Failed to create project.");

        } finally {

            setLoading(false);

        }

    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">

            <div className="w-full max-w-md rounded-xl bg-zinc-900 p-6">

                <h2 className="text-xl font-semibold">
                    Create Project
                </h2>

                <input
                    className="mt-5 w-full rounded-lg bg-zinc-800 p-3"
                    placeholder="Project Name"
                    value={name}
                    onChange={(e) =>
                        setName(e.target.value)
                    }
                />

                <textarea
                    className="mt-3 w-full rounded-lg bg-zinc-800 p-3"
                    rows={4}
                    placeholder="Description"
                    value={description}
                    onChange={(e) =>
                        setDescription(e.target.value)
                    }
                />

                <div className="mt-5 flex justify-end gap-3">

                    <button
                        onClick={onClose}
                        className="rounded-lg bg-zinc-800 px-4 py-2"
                    >
                        Cancel
                    </button>

                    <button
                        onClick={handleCreate}
                        disabled={loading}
                        className="rounded-lg bg-violet-600 px-4 py-2"
                    >
                        {loading
                            ? "Creating..."
                            : "Create"}
                    </button>

                </div>

            </div>

        </div>
    );
}