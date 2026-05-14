/**
 * API Service Layer — wires the frontend to the FastAPI + LangChain backend.
 *
 * Configure the backend base URL via `VITE_API_BASE_URL` (e.g. http://localhost:8000).
 * If the backend is unreachable OR `VITE_USE_MOCK=true`, requests fall back to mock
 * data so the UI is fully usable during development.
 *
 * Backend endpoints expected:
 *   POST   /upload                  multipart/form-data file upload
 *   GET    /data/raw                raw dataset rows + columns
 *   GET    /data/preview            cleaned dataset rows + columns
 *   GET    /visualizations          list of chart specs
 *   POST   /visualizations/custom   { x, y, type } -> chart spec
 *   GET    /insights                summary stats / correlations / trends / outliers
 *   POST   /report                  trigger report generation -> structured report
 *   GET    /report/download         binary download (pdf/html)
 *   POST   /chat                    { message, session_id } -> { reply, data? }
 *   GET    /health                  { status: "ok" }
 */



let SESSION_ID: string | null = null;

function getSessionId() {
  if (!SESSION_ID) {
    SESSION_ID = crypto.randomUUID();
  }
  return SESSION_ID;
}

export const API_BASE =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") || "";
export const USE_MOCK = false;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!API_BASE) {
    throw new Error("API_BASE not configured. Backend is required.");
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.headers || {}),
    },
  });

  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

export type ColumnMeta = { name: string; type: string; missing: number };
export type Dataset = { columns: ColumnMeta[]; rows: Record<string, unknown>[]; total_rows: number };
export type ChartSpec = {
  id: string;
  title: string;
  type: "bar" | "line" | "area" | "pie" | "scatter";
  x: string;
  y: string;
  data: Record<string, number | string>[];
  description?: string;
};
export type Insights = {
  summary: { rows: number; columns: number; missing: number; duplicates: number };
  stats: { column: string; mean?: number; median?: number; std?: number; min?: number; max?: number }[];
  correlations: { a: string; b: string; value: number }[];
  trends: string[];
  outliers: { column: string; count: number }[];
};
export type ReportSection = { title: string; body: string };
export type Report = { title: string; generated_at: string; sections: ReportSection[] };
export type ChatReply = { reply: string; table?: Dataset; chart?: ChartSpec };

/* ----------------------------- API methods ----------------------------- */



export const api = {
  health: async (): Promise<{ status: string }> => {
    try {
      return await request("/health");
    } catch {
      return USE_MOCK ? { status: "mock" } : { status: "down" };
    }
  },

  uploadFile: async (
  file: File,
  onProgress?: (pct: number) => void
): Promise<{ filename: string; size: number; rows: number; columns: number }> => {

  const session_id = getSessionId();

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE}/upload`);

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress(Math.round((e.loaded / e.total) * 100));
      }
    };

    xhr.onload = () =>
      xhr.status >= 200 && xhr.status < 300
        ? resolve(JSON.parse(xhr.responseText))
        : reject(new Error(xhr.responseText));

    xhr.onerror = () => reject(new Error("Network error"));

    const fd = new FormData();
    fd.append("file", file);
    fd.append("session_id", session_id);   // ✅ ADD THIS

    xhr.send(fd);
  });
},

  getRawData: async (): Promise<Dataset> => {
  const session_id = getSessionId();

  if (!session_id) {
    throw new Error("No session_id found");
  }

  return await request(`/data/raw?session_id=${session_id}`);
},

getPreview: async (): Promise<Dataset> => {
  const session_id = getSessionId();
  return await request(`/data/preview?session_id=${session_id}`);
},

getVisualizations: async (): Promise<ChartSpec[]> => {
  const session_id = getSessionId();
  return await request(`/visualizations?session_id=${session_id}`);
},

getInsights: async (): Promise<Insights> => {
  const session_id = getSessionId();
  return await request(`/insights?session_id=${session_id}`);
},

  downloadCleanedData: () => {
    const session_id = getSessionId();
    return `${API_BASE}/data/download?session_id=${session_id}`;
  },

  reportDownloadUrl: () => {
      const session_id = getSessionId();
      return `${API_BASE}/report/download?session_id=${session_id}`;
  },
  
  generateReport: async (): Promise<Report> => {
  const session_id = getSessionId();

  return await request(`/report?session_id=${session_id}`, {
    method: "POST",
  });
},
  chat: async (message: string): Promise<ChatReply> => {
  const session_id = getSessionId();

  return await request("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // ✅ ADD THIS
      },
      body: JSON.stringify({ message, session_id }),
    });
},

customVisualization: async (payload: {
  x: string;
  y: string;
  type: string;
}): Promise<ChartSpec> => {
  const session_id = getSessionId();

  return await request(`/visualizations/custom?session_id=${session_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
},
};

