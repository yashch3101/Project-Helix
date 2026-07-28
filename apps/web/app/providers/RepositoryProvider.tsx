"use client";

import {
    createContext,
    useContext,
    useState,
    ReactNode,
} from "react";

export type RepositoryStatus = {
    status: string;
    progress: number;
    current_stage: string;
    indexed_at: string | null;
    error_message: string | null;
};

type RepositoryContextType = {
    repositoryStatus: RepositoryStatus | null;
    setRepositoryStatus: (
        value: RepositoryStatus | null
    ) => void;
};

const RepositoryContext =
    createContext<RepositoryContextType | null>(null);

export function RepositoryProvider({
    children,
}: {
    children: ReactNode;
}) {

    const [
        repositoryStatus,
        setRepositoryStatus,
    ] = useState<RepositoryStatus | null>(null);

    return (

        <RepositoryContext.Provider
            value={{
                repositoryStatus,
                setRepositoryStatus,
            }}
        >

            {children}

        </RepositoryContext.Provider>

    );

}

export function useRepository() {

    const context =
        useContext(RepositoryContext);

    if (!context) {

        throw new Error(
            "useRepository must be used inside RepositoryProvider"
        );

    }

    return context;

}