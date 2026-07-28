import { api } from "@/app/lib/api";

type Project = {
    id: string;
    name: string;
    description?: string;
};

export async function getProjects() {
    return api<Project[]>("/projects");
}

export async function createProject(
    name: string,
    description: string
) {
    return api<Project>("/projects", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name,
            description,
        }),
    });
}