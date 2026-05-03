import { useRef } from "react";
import {
  Bar, BarChart, Line, LineChart, Area, AreaChart, Pie, PieChart, Cell,
  Scatter, ScatterChart, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import type { ChartSpec } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

const COLORS = ["hsl(var(--primary))", "hsl(var(--accent))", "hsl(var(--success))", "hsl(var(--warning))", "hsl(var(--destructive))"];

export function ChartRenderer({ spec }: { spec: ChartSpec }) {
  const ref = useRef<HTMLDivElement>(null);

  const downloadPng = () => {
    const svg = ref.current?.querySelector("svg");
    if (!svg) return;
    const xml = new XMLSerializer().serializeToString(svg);
    const svg64 = btoa(unescape(encodeURIComponent(xml)));
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = img.width || 800; canvas.height = img.height || 400;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.fillStyle = getComputedStyle(document.body).backgroundColor;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
      const a = document.createElement("a");
      a.href = canvas.toDataURL("image/png");
      a.download = `${spec.title.replace(/\s+/g, "_")}.png`;
      a.click();
    };
    img.src = `data:image/svg+xml;base64,${svg64}`;
  };

  const tooltipStyle = {
    backgroundColor: "hsl(var(--popover))",
    border: "1px solid hsl(var(--border))",
    borderRadius: 8,
    color: "hsl(var(--popover-foreground))",
    fontSize: 12,
  } as const;

  const renderChart = () => {
    switch (spec.type) {
      case "bar":
        return (
          <BarChart data={spec.data}>
            <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey={spec.x} stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "hsl(var(--muted))", opacity: 0.5 }} />
            <Bar dataKey={spec.y} fill="hsl(var(--primary))" radius={[6, 6, 0, 0]} />
          </BarChart>
        );
      case "line":
        return (
          <LineChart data={spec.data}>
            <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey={spec.x} stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <Tooltip contentStyle={tooltipStyle} />
            <Line type="monotone" dataKey={spec.y} stroke="hsl(var(--primary))" strokeWidth={2.5} dot={false} />
          </LineChart>
        );
      case "area":
        return (
          <AreaChart data={spec.data}>
            <defs>
              <linearGradient id={`g-${spec.id}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={0.5} />
                <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey={spec.x} stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <Tooltip contentStyle={tooltipStyle} />
            <Area type="monotone" dataKey={spec.y} stroke="hsl(var(--primary))" fill={`url(#g-${spec.id})`} strokeWidth={2} />
          </AreaChart>
        );
      case "pie":
        return (
          <PieChart>
            <Tooltip contentStyle={tooltipStyle} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Pie data={spec.data} dataKey={spec.y} nameKey={spec.x} cx="50%" cy="50%" outerRadius={100} innerRadius={55} paddingAngle={2}>
              {spec.data.map((_, i) => (<Cell key={i} fill={COLORS[i % COLORS.length]} />))}
            </Pie>
          </PieChart>
        );
      case "scatter":
        return (
          <ScatterChart>
            <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" />
            <XAxis dataKey={spec.x} stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <YAxis dataKey={spec.y} stroke="hsl(var(--muted-foreground))" fontSize={12} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={spec.data} fill="hsl(var(--primary))" />
          </ScatterChart>
        );
    }
  };

  return (
    <div className="rounded-xl border border-border bg-card p-5 shadow-card transition-smooth hover:shadow-elegant">
      <div className="flex items-start justify-between gap-2 mb-4">
        <div>
          <h3 className="font-semibold">{spec.title}</h3>
          {spec.description && <p className="text-xs text-muted-foreground mt-0.5">{spec.description}</p>}
        </div>
        <Button variant="ghost" size="icon" onClick={downloadPng} title="Download PNG">
          <Download className="h-4 w-4" />
        </Button>
      </div>
      <div ref={ref} className="h-[280px]">
        <ResponsiveContainer width="100%" height="100%">{renderChart()}</ResponsiveContainer>
      </div>
    </div>
  );
}