"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  ReactNode,
} from "react";

import { auth } from "@/app/lib/auth";

import { useRouter } from "next/navigation";

import {
  login as loginService,
  register as registerService,
  getCurrentUser,
  logout as logoutService,
  CurrentUser,
  LoginRequest,
  RegisterRequest,
} from "@/app/services/auth";

interface AuthContextType {
  user: CurrentUser | null;
  loading: boolean;

  login(data: LoginRequest): Promise<void>;

  register(data: RegisterRequest): Promise<void>;

  logout(): void;

  refreshUser(): Promise<void>;

  isAuthenticated: boolean;
}

const AuthContext =
  createContext<AuthContextType | null>(null);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {

  const router = useRouter();

  const [user, setUser] =
    useState<CurrentUser | null>(null);

  const [loading, setLoading] =
    useState(true);

  const refreshUser = useCallback(async () => {

    const token = auth.getToken();

    if (!token) {
        setUser(null);
        setLoading(false);
        return;
    }

    try {

        const current = await getCurrentUser();

        setUser(current);

    } catch {

    // Token invalid ya expire ho gaya
        auth.logout();
        setUser(null);

    } finally {

        setLoading(false);

    }

}, []);

  useEffect(() => {

    void refreshUser();

  }, [refreshUser]);

  async function login(
    payload: LoginRequest
  ) {

    setLoading(true);

    try {

      const current =
        await loginService(payload);

      setUser(current);

      router.replace("/");

    } finally {

      setLoading(false);

    }

  }

  async function register(
    payload: RegisterRequest
  ) {

    setLoading(true);

    try {

      await registerService(payload);

      await login({
        email: payload.email,
        password: payload.password,
      });

    } finally {

      setLoading(false);

    }

  }

  function logout() {

    logoutService();

    setUser(null);

    router.replace("/auth/login");

  }

  const value = useMemo(() => ({

    user,

    loading,

    login,

    register,

    logout,

    refreshUser,

    isAuthenticated: !!user,

  }), [
    user,
    loading,
    refreshUser,
  ]);

  return (

    <AuthContext.Provider value={value}>

      {children}

    </AuthContext.Provider>

  );

}

export function useAuth() {

  const context =
    useContext(AuthContext);

  if (!context) {

    throw new Error(
      "useAuth must be used inside AuthProvider"
    );

  }

  return context;

}