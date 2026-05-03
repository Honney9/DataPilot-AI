import type { Insights } from "@/services/api";
import { TrendingUp, AlertTriangle, GitCompareArrows, Sigma } from "lucide-react";

export function InsightCards({ data }: { data: Insights | null }) {
    if (!data || !data.summary) {
        return <div className="text-sm text-muted-foreground">No insights available</div>;
    }
    const stats = [
        { label: "Rows", value: data.summary?.rows ?? 0 },
        { label: "Columns", value: data.summary?.columns ?? 0 },
        { label: "Missing", value: data.summary?.missing ?? 0 },
        { label: "Duplicates", value: data.summary?.duplicates ?? 0 },
    ];
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="rounded-xl border border-border bg-card p-5 shadow-card">
            <div className="text-xs text-muted-foreground uppercase tracking-wider">{s.label}</div>
            <div className="text-3xl font-bold mt-2 text-gradient">{s.value.toLocaleString()}</div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <Section title="Summary statistics" icon={Sigma}>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-xs text-muted-foreground"><tr>
                <th className="text-left py-2">Column</th><th>Mean</th><th>Median</th><th>Std</th><th>Min</th><th>Max</th>
              </tr></thead>
              <tbody>
                {data.stats.map((s) => (
                  <tr key={s.column} className="border-t border-border">
                    <td className="py-2 font-medium">{s.column}</td>
                    <td className="text-center">{s.mean}</td>
                    <td className="text-center">{s.median}</td>
                    <td className="text-center">{s.std}</td>
                    <td className="text-center">{s.min}</td>
                    <td className="text-center">{s.max}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>

        <Section title="Top correlations" icon={GitCompareArrows}>
          <div className="space-y-3">
            {data.correlations.map((c, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">{c.a} ↔ {c.b}</span>
                  <span className="text-muted-foreground">{c.value.toFixed(2)}</span>
                </div>
                <div className="h-2 rounded-full bg-muted overflow-hidden">
                  <div className="h-full bg-gradient-primary" style={{ width: `${Math.abs(c.value) * 100}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Section>

        <Section title="Trends" icon={TrendingUp}>
          <ul className="space-y-2 text-sm">
            {data.trends.map((t, i) => (
              <li key={i} className="flex gap-2"><span className="text-primary mt-1">▸</span>{t}</li>
            ))}
          </ul>
        </Section>

        <Section title="Outliers" icon={AlertTriangle}>
          <div className="space-y-2">
            {data.outliers.map((o) => (
              <div key={o.column} className="flex items-center justify-between rounded-lg bg-warning/10 px-3 py-2 text-sm">
                <span className="font-medium">{o.column}</span>
                <span className="text-warning font-semibold">{o.count} detected</span>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}

function Section({ title, icon: Icon, children }: { title: string; icon: React.ComponentType<{ className?: string }>; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border bg-card p-5 shadow-card">
      <div className="flex items-center gap-2 mb-4">
        <Icon className="h-4 w-4 text-primary" />
        <h3 className="font-semibold">{title}</h3>
      </div>
      {children}
    </div>
  );
}