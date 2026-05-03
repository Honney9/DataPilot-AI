import { useEffect, useState } from "react";
import { PageHeader } from "@/components/dashboard/PageHeader";
import { DataTable } from "@/components/dashboard/DataTable";
import { CardSkeleton } from "@/components/dashboard/Skeleton";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { api, type Dataset } from "@/services/api";

export function PreviewView() {
  const [mode, setMode] = useState<"raw" | "clean">("clean");
  const [data, setData] = useState<Dataset | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true); setErr(null);
    (mode === "raw" ? api.getRawData() : api.getPreview())
      .then(setData).catch((e) => setErr((e as Error).message))
      .finally(() => setLoading(false));
  }, [mode]);

  return (
    <div>
      <PageHeader
        title="Data preview"
        subtitle="Inspect the dataset before and after the cleaning agent processes it."
        actions={
          <Tabs value={mode} onValueChange={(v) => setMode(v as "raw" | "clean")}>
            <TabsList>
              <TabsTrigger value="raw">Raw</TabsTrigger>
              <TabsTrigger value="clean">Cleaned</TabsTrigger>
            </TabsList>
          </Tabs>
        }
      />
      {loading && <CardSkeleton height="h-96" />}
      {err && <div className="text-destructive text-sm">{err}</div>}
      {data && !loading && <DataTable data={data} />}
    </div>
  );
}