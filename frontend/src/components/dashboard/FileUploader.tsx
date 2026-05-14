import { useRef, useState } from "react";
import { Upload, FileSpreadsheet, CheckCircle2, AlertCircle, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { api } from "@/services/api";
import { useApp } from "@/store/AppStore";
import { cn } from "@/lib/utils";

const ACCEPT = ".csv,.xlsx,.xls";

function fmtSize(b: number) {
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)} KB`;
  return `${(b / 1024 / 1024).toFixed(2)} MB`;
}

export function FileUploader() {
  const { file, setFile } = useApp();
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const handleFiles = async (files: FileList | null) => {
    if (!files || !files.length) return;
    const f = files[0];
    if (!/\.(csv|xlsx|xls)$/i.test(f.name)) {
      setError("Unsupported format. Use CSV or XLSX."); setStatus("error"); return;
    }
    setError(null); setStatus("uploading"); setProgress(0);
    try {
      const meta = await api.uploadFile(f, setProgress);
      setFile({ name: meta.filename, size: meta.size, rows: meta.rows, columns: meta.columns });
      setStatus("success");
    } catch (e) {
      setError((e as Error).message); setStatus("error");
    }
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); handleFiles(e.dataTransfer.files); }}
        className={cn(
          "relative rounded-2xl border-2 border-dashed p-10 text-center transition-smooth cursor-pointer overflow-hidden",
          "bg-card/60 hover:bg-card",
          drag ? "border-primary bg-primary/5 shadow-elegant" : "border-border"
        )}
        onClick={() => inputRef.current?.click()}
      >
        <div className="absolute inset-0 bg-gradient-glow pointer-events-none opacity-60" />
        <input ref={inputRef} type="file" accept={ACCEPT} className="hidden"
          onChange={(e) => handleFiles(e.target.files)} />
        <div className="relative flex flex-col items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-primary shadow-elegant">
            <Upload className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <div className="font-semibold">Drop your dataset here</div>
            <div className="text-sm text-muted-foreground mt-1">CSV or XLSX</div>
          </div>
          <Button type="button" variant="outline" size="sm" className="mt-2">Browse files</Button>
        </div>
      </div>

      {status === "uploading" && (
        <div className="rounded-xl border border-border bg-card p-4 space-y-2 animate-fade-in">
          <div className="flex items-center justify-between text-sm">
            <span>Uploading…</span><span className="text-muted-foreground">{progress}%</span>
          </div>
          <Progress value={progress} />
        </div>
      )}

      {status === "error" && error && (
        <div className="flex items-start gap-3 rounded-xl border border-destructive/40 bg-destructive/10 p-4 text-sm">
          <AlertCircle className="h-4 w-4 mt-0.5 text-destructive" />
          <div className="flex-1">
            <div className="font-medium text-destructive">Upload failed</div>
            <div className="text-muted-foreground">{error}</div>
          </div>
          <button onClick={() => { setStatus("idle"); setError(null); }}><X className="h-4 w-4" /></button>
        </div>
      )}

      {file && status !== "uploading" && (
        <div className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 animate-fade-in">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <FileSpreadsheet className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-medium truncate">{file.name}</div>
            <div className="text-xs text-muted-foreground">
              {fmtSize(file.size)}{file.rows ? ` · ${file.rows} rows × ${file.columns} cols` : ""}
            </div>
          </div>
          {status === "success" && (
            <div className="flex items-center gap-1.5 text-success text-xs font-medium">
              <CheckCircle2 className="h-4 w-4" /> Uploaded
            </div>
          )}
        </div>
      )}
    </div>
  );
}