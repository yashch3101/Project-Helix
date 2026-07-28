"use client";

import { FormEvent, useState } from "react";
import { Mail, Loader2 } from "lucide-react";

import PasswordInput from "./PasswordInput";
import { useAuth } from "@/app/providers/AuthProvider";

export default function LoginForm() {
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    async function handleSubmit(
        e: FormEvent<HTMLFormElement>
    ) {
        e.preventDefault();

        setError("");

        if (!email.trim()) {
            setError("Email is required");
            return;
        }

        if (!password.trim()) {
            setError("Password is required");
            return;
        }

        try {
            setLoading(true);

            await login({
                email,
                password,
            });

        } catch (err) {

            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("Login failed");
            }

        } finally {

            setLoading(false);

        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-6"
        >

            <div className="space-y-2">

                <label className="block text-sm font-medium text-zinc-300">
                    Email
                </label>

                <div className="relative">

                    <Mail
                        size={18}
                        className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500"
                    />

                    <input
                        type="email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        placeholder="you@example.com"
                        className="w-full rounded-xl border border-zinc-700 bg-zinc-900 py-3 pl-12 pr-4 text-white outline-none transition-all placeholder:text-zinc-500 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20"
                    />

                </div>

            </div>

            <PasswordInput
                label="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
                placeholder="••••••••"
            />

            {error && (

                <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">

                    {error}

                </div>

            )}

            <button
                disabled={loading}
                className="flex h-12 w-full items-center justify-center rounded-xl bg-violet-600 font-semibold transition-all hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-60"
            >

                {loading ? (

                    <Loader2
                        size={18}
                        className="animate-spin"
                    />

                ) : (

                    "Sign In"

                )}

            </button>

        </form>
    );
}