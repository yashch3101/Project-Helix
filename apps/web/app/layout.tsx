import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/app/providers/AuthProvider";
import { RepositoryProvider } from "@/app/providers/RepositoryProvider";
import { Toaster } from "sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Project Helix",
  description: "AI-powered Repository Intelligence Platform",
  applicationName: "Project Helix",
  keywords: [
    "AI",
    "Repository Intelligence",
    "Code Graph",
    "RAG",
    "FastAPI",
    "Next.js",
    "LLM",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
  >
      <body className="min-h-screen bg-zinc-950 text-white flex flex-col overflow-hidden">

          <AuthProvider>

              <RepositoryProvider>

                  {children}

                  <Toaster
                      richColors
                      position="top-right"
                  />

              </RepositoryProvider>

          </AuthProvider>

      </body>
    </html>
  );
}
