import { Database, Eye, BarChart3, Lightbulb, FileText, MessageSquare, Sparkles, Moon, Sun, Activity } from "lucide-react";
import { cn } from "@/lib/utils";
import { useApp } from "@/store/AppStore";
import { Button } from "@/components/ui/button";

export type View = "upload" | "preview" | "visualize" | "insights" | "report" | "chat";

const NAV: { id: View; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
  { id: "upload", label: "Upload", icon: Database },
  { id: "preview", label: "Preview", icon: Eye },
  { id: "visualize", label: "Visualize", icon: BarChart3 },
  { id: "insights", label: "Insights", icon: Lightbulb },
  { id: "report", label: "Report", icon: FileText },
  { id: "chat", label: "Chat", icon: MessageSquare },
];

export function Sidebar({ view, onChange }: { view: View; onChange: (v: View) => void }) {
  const { theme, toggleTheme, health } = useApp();
  const healthColor =
    health === "ok" ? "bg-success" : health === "mock" ? "bg-warning" : health === "down" ? "bg-destructive" : "bg-muted-foreground";
  const healthLabel =
    health === "ok" ? "Backend online" : health === "mock" ? "Mock mode" : health === "down" ? "Backend offline" : "Checking…";

  return (
    <aside className="hidden md:flex w-64 shrink-0 flex-col border-r border-border bg-sidebar">
      <div className="flex items-center gap-3 px-5 py-5 border-b border-sidebar-border">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-primary shadow-elegant">
          <Sparkles className="h-5 w-5 text-primary-foreground" />
        </div>
        <div>
          <div className="text-sm font-semibold tracking-tight text-sidebar-foreground">DataPilot AI</div>
          <div className="text-[11px] text-muted-foreground">Multi-Agent DS</div>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {NAV.map((item) => {
          const Icon = item.icon;
          const active = view === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onChange(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-smooth",
                active
                  ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-sm"
                  : "text-sidebar-foreground hover:bg-sidebar-accent/60"
              )}
            >
              <Icon className={cn("h-4 w-4", active && "text-primary")} />
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="p-3 border-t border-sidebar-border space-y-2">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-sidebar-accent/40 text-xs">
          <span className={cn("h-2 w-2 rounded-full animate-pulse-glow", healthColor)} />
          <Activity className="h-3.5 w-3.5 text-muted-foreground" />
          <span className="text-sidebar-foreground">{healthLabel}</span>
        </div>
        <Button variant="ghost" size="sm" onClick={toggleTheme} className="w-full justify-start gap-2">
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          {theme === "dark" ? "Light mode" : "Dark mode"}
        </Button>
      </div>
    </aside>
  );
}

export function MobileTabs({ view, onChange }: { view: View; onChange: (v: View) => void }) {
  return (
    <div className="md:hidden flex overflow-x-auto gap-1 p-2 border-b border-border bg-card">
      {NAV.map((item) => {
        const Icon = item.icon;
        const active = view === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            className={cn(
              "flex items-center gap-1.5 px-3 py-2 rounded-md text-xs font-medium whitespace-nowrap transition-smooth",
              active ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-muted"
            )}
          >
            <Icon className="h-3.5 w-3.5" />
            {item.label}
          </button>
        );
      })}
    </div>
  );
}