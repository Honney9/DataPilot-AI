import { useEffect, useRef, useState } from "react";
import { Send, Sparkles, User, Bot, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useApp } from "@/store/AppStore";
import { api } from "@/services/api";
import { DataTable } from "./DataTable";
import { ChartRenderer } from "./ChartRenderer";
import { cn } from "@/lib/utils";

const SUGGESTIONS = [
  "Summarize the dataset",
  "Show revenue by region as a chart",
  "What are the top correlations?",
  "Show me a table of the first rows",
];

export function ChatWindow() {
  const { chat, pushChat, clearChat, sessionId } = useApp();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [chat, loading]);

  const send = async (text: string) => {
    const msg = text.trim();
    if (!msg || loading) return;
    pushChat({ id: crypto.randomUUID(), role: "user", content: msg, ts: Date.now() });
    setInput(""); setLoading(true);
    try {
      const res = await api.chat(msg);
      pushChat({ id: crypto.randomUUID(), role: "assistant", content: res.reply, table: res.table, chart: res.chart, ts: Date.now() });
    } catch (e) {
      pushChat({ id: crypto.randomUUID(), role: "assistant", content: `Error: ${(e as Error).message}`, ts: Date.now() });
    } finally { setLoading(false); }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] rounded-2xl border border-border bg-card shadow-card overflow-hidden">
      <div className="flex items-center justify-between px-5 py-3 border-b border-border bg-gradient-surface">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-primary">
            <Sparkles className="h-4 w-4 text-primary-foreground" />
          </div>
          <div>
            <div className="text-sm font-semibold">Data Agent</div>
            <div className="text-[11px] text-muted-foreground">LangChain · session {sessionId.slice(0, 8)}</div>
          </div>
        </div>
        {chat.length > 0 && (
          <Button variant="ghost" size="sm" onClick={clearChat}>
            <Trash2 className="h-3.5 w-3.5 mr-1" /> Clear
          </Button>
        )}
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-5 space-y-5">
        {chat.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-primary shadow-elegant mb-4">
              <Bot className="h-7 w-7 text-primary-foreground" />
            </div>
            <h3 className="font-semibold text-lg">Ask anything about your data</h3>
            <p className="text-sm text-muted-foreground mt-1 max-w-md">
              The agent can compute statistics, generate charts, find trends, and explain results.
            </p>
            <div className="flex flex-wrap gap-2 justify-center mt-6 max-w-lg">
              {SUGGESTIONS.map((s) => (
                <button key={s} onClick={() => send(s)}
                  className="text-xs px-3 py-2 rounded-full border border-border bg-background hover:bg-muted transition-smooth">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {chat.map((m) => (
          <div key={m.id} className={cn("flex gap-3 animate-fade-in", m.role === "user" && "flex-row-reverse")}>
            <div className={cn(
              "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
              m.role === "user" ? "bg-secondary" : "bg-gradient-primary"
            )}>
              {m.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4 text-primary-foreground" />}
            </div>
            <div className="max-w-[80%] space-y-3">
              <div className={cn(
                "rounded-2xl px-4 py-2.5 text-sm whitespace-pre-wrap",
                m.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
              )}>
                {m.content}
              </div>
              {m.table && <DataTable data={m.table} />}
              {m.chart && <ChartRenderer spec={m.chart} />}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-primary">
              <Bot className="h-4 w-4 text-primary-foreground" />
            </div>
            <div className="rounded-2xl px-4 py-3 bg-muted flex gap-1.5">
              <span className="h-2 w-2 rounded-full bg-muted-foreground animate-pulse-glow" />
              <span className="h-2 w-2 rounded-full bg-muted-foreground animate-pulse-glow" style={{ animationDelay: "0.2s" }} />
              <span className="h-2 w-2 rounded-full bg-muted-foreground animate-pulse-glow" style={{ animationDelay: "0.4s" }} />
            </div>
          </div>
        )}
      </div>

      <form onSubmit={(e) => { e.preventDefault(); send(input); }}
        className="flex items-center gap-2 p-3 border-t border-border bg-background">
        <Input value={input} onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the data agent…" disabled={loading} className="flex-1" />
        <Button type="submit" disabled={!input.trim() || loading} size="icon" className="shrink-0">
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
}