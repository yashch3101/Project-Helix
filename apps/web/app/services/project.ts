const API = process.env.NEXT_PUBLIC_API_URL;

export async function getProjects() {

    const res = await fetch(

        `${API}/projects`

    );

    if (!res.ok) {

        throw new Error("Failed to load projects");

    }

    return res.json();

}