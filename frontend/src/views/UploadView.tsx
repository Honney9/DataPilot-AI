import { PageHeader } from "@/components/dashboard/PageHeader";
import { FileUploader } from "@/components/dashboard/FileUploader";
import { useApp } from "@/store/AppStore";
import { Database, FileSpreadsheet, Layers, AlertCircle } from "lucide-react";

export function UploadView() {
  const { file } = useApp();
  return (
    <div className="max-w-3xl">
      <PageHeader
        title="Upload your dataset"
        subtitle="Drop a CSV or XLSX file. The backend will clean, profile, and prepare it for analysis."
      />
      <FileUploader />

      {file && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
          <Stat icon={FileSpreadsheet} label="File" value={file.name.length > 14 ? file.name.slice(0, 12) + "…" : file.name} />
          <Stat icon={Database} label="Rows" value={file.rows ?? "—"} />
          <Stat icon={Layers} label="Columns" value={file.columns ?? "—"} />
          <Stat icon={AlertCircle} label="Status" value="Ready" />
        </div>
      )}
    </div>
  );
}

function Stat({ icon: Icon, label, value }: { icon: React.ComponentType<{ className?: string }>; label: string; value: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="flex items-center gap-2 text-xs text-muted-foreground"><Icon className="h-3.5 w-3.5" />{label}</div>
      <div className="font-semibold mt-1">{value}</div>
    </div>
  );
}