import { useState } from "react";
import { PageHeader } from "@/components/dashboard/PageHeader";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/dashboard/EmptyState";
import { api, type Report } from "@/services/api";
import { FileText, Download, Sparkles, Loader2 } from "lucide-react";

export function ReportView() {
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    try { setReport(await api.generateReport()); } finally { setLoading(false); }
  };

  return (
    <div>
      <PageHeader
        title="Report"
        subtitle="Run the report agent to compile a structured analysis of your dataset."
        actions={
          <div className="flex gap-2">
            <Button onClick={generate} disabled={loading}>
              {loading ? <Loader2 className="h-4 w-4 mr-2 animate-spin" /> : <Sparkles className="h-4 w-4 mr-2" />}
              {report ? "Regenerate" : "Generate report"}
            </Button>
            {report && (
              <Button variant="outline" asChild>
                <a href={api.reportDownloadUrl()} target="_blank" rel="noreferrer">
                  <Download className="h-4 w-4 mr-2" /> Download
                </a>
              </Button>
            )}
          </div>
        }
      />
      {!report && !loading && (
        <EmptyState icon={FileText} title="No report yet" description="Click Generate report to let the agents compile findings." />
      )}
      {loading && <div className="rounded-xl border border-border bg-card h-64 animate-pulse" />}
      {report && (
        <article className="rounded-2xl border border-border bg-card p-8 shadow-card animate-fade-in max-w-3xl">
          <div className="border-b border-border pb-4 mb-6">
            <h2 className="text-2xl font-bold">{report.title}</h2>
            <p className="text-xs text-muted-foreground mt-1">Generated {new Date(report.generated_at).toLocaleString()}</p>
          </div>
          <div className="space-y-6">
            {Array.isArray(report.sections) && report.sections.map((s, i) => (
              <section key={i}>
                <h3 className="font-semibold text-lg mb-2 text-gradient">{s.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{s.body}</p>
              </section>
            ))}
          </div>
        </article>
      )}
    </div>
  );
}