import { api } from "@/app/lib/api";
import { auth } from "@/app/lib/auth";

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    full_name: string;
    email: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export interface CurrentUser {
    id: string;
    full_name: string;
    email: string;
}

export async function login(
    payload: LoginRequest
): Promise<CurrentUser> {

    const response = await api<LoginResponse>(
        "/auth/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        }
    );

    auth.saveToken(response.access_token);

    return getCurrentUser();
}

export async function register(
    payload: RegisterRequest
): Promise<void> {

    await api(
        "/auth/register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        }
    );

}

export async function getCurrentUser(): Promise<CurrentUser> {

    const token = auth.getToken();

    if (!token) {

        throw new Error("Unauthorized");

    }

    return api<CurrentUser>(
        "/auth/me",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

}

export function logout() {

    auth.logout();

}