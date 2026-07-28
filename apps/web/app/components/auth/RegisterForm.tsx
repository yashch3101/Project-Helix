"use client";

import { useState } from "react";

import { useAuth } from "@/app/providers/AuthProvider";
import PasswordInput from "./PasswordInput";

export function RegisterForm() {
    const { register } = useAuth();

    const [full_name, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(
        e: React.FormEvent<HTMLFormElement>
    ) {
        e.preventDefault();

        setLoading(true);
        setError("");

        try {
            await register({
                full_name,
                email,
                password,
            });
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("Registration failed");
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-5"
        >
            <input
                type="text"
                placeholder="Full Name"
                value={full_name}
                onChange={(e) =>
                    setFullName(e.target.value)
                }
                className="w-full rounded-lg border border-zinc-700 bg-zinc-900 p-3 text-white outline-none"
            />

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
                className="w-full rounded-lg border border-zinc-700 bg-zinc-900 p-3 text-white outline-none"
            />

            <PasswordInput
                label="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
                placeholder="Enter your password"
                error={error}
            />

            <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-violet-600 py-3 font-medium transition hover:bg-violet-500 disabled:opacity-50"
            >
                {loading
                    ? "Creating Account..."
                    : "Create Account"}
            </button>
        </form>
    );
}