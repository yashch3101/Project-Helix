import { auth } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function api<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {

    const token = auth.getToken();

    const response = await fetch(
        `${API_URL}${endpoint}`,
        {
            ...options,
            headers: {
                ...(options.headers ?? {}),
                ...(token
                    ? {
                          Authorization: `Bearer ${token}`,
                      }
                    : {}),
            },
        }
    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(
            error.detail || "Something went wrong"
        );

    }

    return response.json();
}