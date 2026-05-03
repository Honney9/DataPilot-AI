import type { Dataset } from "@/services/api";
import { Badge } from "@/components/ui/badge";

export function DataTable({ data }: { data: Dataset }) {
  return (
    <div className="rounded-xl border border-border bg-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-muted/50 text-xs uppercase tracking-wider text-muted-foreground">
            <tr>
              {data.columns.map((c) => (
                <th key={c.name} className="px-4 py-3 text-left font-semibold whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    {c.name}
                    <Badge variant="outline" className="font-normal text-[10px]">{c.type}</Badge>
                    {c.missing > 0 && (
                      <span className="text-warning text-[10px] font-medium">{c.missing} missing</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.rows.map((row, i) => (
              <tr key={i} className="border-t border-border hover:bg-muted/30 transition-smooth">
                {data.columns.map((c) => {
                  const v = row[c.name];
                  return (
                    <td key={c.name} className="px-4 py-2.5 whitespace-nowrap">
                      {v == null ? <span className="text-muted-foreground italic">null</span> : String(v)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="px-4 py-2 text-xs text-muted-foreground border-t border-border bg-muted/30">
        Showing {data.rows.length} of {data.total_rows} rows
      </div>
    </div>
  );
}