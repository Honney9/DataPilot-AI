import { createContext, useContext, useEffect, useState } from "react";
import { api } from "@/services/api";
import type { ChartSpec, Dataset } from "@/services/api";

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  table?: Dataset;
  chart?: ChartSpec;
  ts: number;
};

export type FileMeta =
  | { name: string; size: number; rows?: number; columns?: number }
  | null;

type Ctx = {
  file: FileMeta;
  setFile: (f: FileMeta) => void;

  chat: ChatMessage[];
  pushChat: (m: ChatMessage) => void;
  clearChat: () => void;

  sessionId: string;

  theme: "light" | "dark";
  toggleTheme: () => void;

  health: "checking" | "ok" | "down" | "mock";
};

const AppCtx = createContext<Ctx | null>(null);

function getInitialTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "dark";
  return (localStorage.getItem("theme") as "light" | "dark") || "dark";
}

function getSessionId(): string {
  if (typeof window === "undefined") return crypto.randomUUID();

  const existing = localStorage.getItem("session_id");
  if (existing) return existing;

  const id = crypto.randomUUID();
  localStorage.setItem("session_id", id);
  return id;
}

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [file, setFile] = useState<FileMeta>(null);
  const [chat, setChat] = useState<ChatMessage[]>([]);
  const [theme, setTheme] = useState<"light" | "dark">(getInitialTheme);
  const [health, setHealth] = useState<Ctx["health"]>("checking");

  const [sessionId] = useState<string>(getSessionId);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  useEffect(() => {
    let mounted = true;

    const ping = async () => {
      const r = await api.health();
      if (!mounted) return;

      setHealth(
        r.status === "ok" ? "ok" : r.status === "mock" ? "mock" : "down"
      );
    };

    ping();
    const id = setInterval(ping, 30000);

    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, []);

  const value: Ctx = {
    file,
    setFile,

    chat,
    pushChat: (m) => setChat((c) => [...c, m]),
    clearChat: () => setChat([]),

    sessionId,

    theme,
    toggleTheme: () =>
      setTheme((t) => (t === "dark" ? "light" : "dark")),

    health,
  };

  return <AppCtx.Provider value={value}>{children}</AppCtx.Provider>;
}

export function useApp() {
  const ctx = useContext(AppCtx);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}