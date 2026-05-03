import { useEffect, useState } from "react";
import { PageHeader } from "@/components/dashboard/PageHeader";
import { InsightCards } from "@/components/dashboard/InsightCards";
import { GridSkeleton } from "@/components/dashboard/Skeleton";
import { api, type Insights } from "@/services/api";

export function InsightsView() {
  const [data, setData] = useState<Insights | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.getInsights().then(setData).finally(() => setLoading(false)); }, []);
  return (
    <div>
      <PageHeader title="Insights" subtitle="Statistical summaries, correlations, trends, and outliers detected by the agents." />
      {loading || !data ? <GridSkeleton count={4} height="h-40" /> : <InsightCards data={data} />}
    </div>
  );
}