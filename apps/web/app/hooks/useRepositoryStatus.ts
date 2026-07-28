"use client";

import { useEffect, useState } from "react";

import { getRepositoryStatus } from "../services/repository";
import type { RepositoryStatusResponse } from "../types/repository";

export function useRepositoryStatus(
    repositoryId: string | null,
) {

    const [status, setStatus] = useState<RepositoryStatusResponse | null>(null);

    useEffect(() => {

        if (!repositoryId) {
            setStatus(null);
            return;
        }

        const id: string = repositoryId;

            if (!id) {

                setStatus(null);

                return;

            }

        let interval: NodeJS.Timeout;

        async function load() {

            try {

                const data = await getRepositoryStatus(id);

                setStatus(data);

                if (data.status !== "READY") {

                    interval = setInterval(async () => {

                        const latest = await getRepositoryStatus(id);

                        setStatus(latest);

                    }, 2000);

                }

            } catch (e) {

                console.error(e);

            }

        }

        load();

        return () => {

            clearInterval(interval);

        };

    }, [repositoryId]);

    return status;

}