import { useEffect, useState } from "react";
import { PageHeader } from "@/components/dashboard/PageHeader";
import { ChartRenderer } from "@/components/dashboard/ChartRenderer";
import { CardSkeleton } from "@/components/dashboard/Skeleton";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { api, type ChartSpec } from "@/services/api";
import { Plus } from "lucide-react";

const CHART_TYPES: ChartSpec["type"][] = ["bar", "line", "area", "pie", "scatter"];

export function VisualizeView() {
  const [charts, setCharts] = useState<ChartSpec[]>([]);
  const [loading, setLoading] = useState(true);
  const [columns, setColumns] = useState<string[]>([]);
  const [x, setX] = useState<string>("");
  const [y, setY] = useState<string>("");
  const [type, setType] = useState<ChartSpec["type"]>("bar");

  useEffect(() => {
    Promise.all([api.getVisualizations(), api.getPreview()]).then(([cs, ds]) => {
      setCharts(cs);
      const cols = ds.columns.map((c) => c.name);
      setColumns(cols);
      setX(cols[1] || cols[0] || "");
      setY(cols.find((c) => ds.columns.find((d) => d.name === c)?.type === "number") || cols[0] || "");
    }).finally(() => setLoading(false));
  }, []);

  const addChart = async () => {
    if (!x || !y) return;
    const c = await api.customVisualization({ x, y, type });
    setCharts((p) => [c, ...p]);
  };

  return (
    <div>
      <PageHeader title="Visualizations" subtitle="Charts produced by the visualization agent. Build your own with the controls below." />
      <div className="rounded-xl border border-border bg-card p-4 mb-6 flex flex-wrap items-end gap-3">
        <Field label="X axis"><PickColumn value={x} onChange={setX} options={columns} /></Field>
        <Field label="Y axis"><PickColumn value={y} onChange={setY} options={columns} /></Field>
        <Field label="Chart type">
          <Select value={type} onValueChange={(v) => setType(v as ChartSpec["type"])}>
            <SelectTrigger className="w-36"><SelectValue /></SelectTrigger>
            <SelectContent>{CHART_TYPES.map((t) => <SelectItem key={t} value={t}>{t}</SelectItem>)}</SelectContent>
          </Select>
        </Field>
        <Button onClick={addChart} disabled={!x || !y}><Plus className="h-4 w-4 mr-1" /> Add chart</Button>
      </div>
      {loading ? (
        <div className="grid lg:grid-cols-2 gap-4"><CardSkeleton height="h-80" /><CardSkeleton height="h-80" /></div>
      ) : (
        <div className="grid lg:grid-cols-2 gap-4">{charts.map((c) => <ChartRenderer key={c.id} spec={c} />)}</div>
      )}
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (<div className="space-y-1.5"><div className="text-xs text-muted-foreground">{label}</div>{children}</div>);
}
function PickColumn({ value, onChange, options }: { value: string; onChange: (v: string) => void; options: string[] }) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-40"><SelectValue placeholder="Column" /></SelectTrigger>
      <SelectContent>{options.map((o) => <SelectItem key={o} value={o}>{o}</SelectItem>)}</SelectContent>
    </Select>
  );
}