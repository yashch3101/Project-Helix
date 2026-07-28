import type {
    RepositoryStatusResponse,
} from "../types/repository";

const API = process.env.NEXT_PUBLIC_API_URL;

export async function getRepositories(
  projectId: string,
) {

    if (!projectId){

        return [];

    }
    
  const res = await fetch(
    `${API}/repositories/project/${projectId}`
  );

  if (!res.ok) {
    throw new Error(
      "Failed to load repositories"
    );
  }

  return res.json();
}

export async function importRepository(
    githubUrl: string,
    projectId: string,
) {

    const res = await fetch(
        `${API}/repositories/import`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({

                github_url: githubUrl,

                project_id: projectId,

            }),

        }
    );

    if (!res.ok) {

        const error = await res.json();

        throw new Error(
            error.detail || "Import failed"
        );

    }

    return res.json();

}

export async function getRepositoryStatus(
    repositoryId: string,
): Promise<RepositoryStatusResponse> {

    const res = await fetch(
        `${API}/repositories/${repositoryId}/status`
    );

    if (!res.ok) {

        throw new Error(
            "Failed to fetch repository status"
        );

    }

    return res.json();

}