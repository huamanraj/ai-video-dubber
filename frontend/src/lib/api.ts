const API_BASE = "http://localhost:8000";

export const api = {
  baseUrl: API_BASE,

  async health(): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error("API unreachable");
    return res.json();
  },

  async getQueue(): Promise<QueueItem[]> {
    const res = await fetch(`${API_BASE}/queue`);
    if (!res.ok) throw new Error("Failed to fetch queue");
    return res.json();
  },

  async getStatus(jobId: string): Promise<JobStatus> {
    const res = await fetch(`${API_BASE}/status/${jobId}`);
    if (!res.ok) throw new Error("Failed to fetch status");
    return res.json();
  },

  async submitDub(file: File, targetLanguage: string, voiceId?: string): Promise<{ job_id: string }> {
    const formData = new FormData();
    formData.append("video", file);
    formData.append("target_language", targetLanguage);
    if (voiceId) {
      formData.append("voice_id", voiceId);
    }
    const res = await fetch(`${API_BASE}/dub`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Submission failed" }));
      throw new Error(err.detail || "Submission failed");
    }
    return res.json();
  },

  async cancelJob(jobId: string): Promise<void> {
    const res = await fetch(`${API_BASE}/queue/${jobId}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to cancel job");
  },

  getDownloadUrl(jobId: string): string {
    return `${API_BASE}/download/${jobId}`;
  },

  getStreamUrl(jobId: string): string {
    return `${API_BASE}/stream/${jobId}`;
  },
};

export interface QueueItem {
  job_id: string;
  file_name: string;
  target_language: string;
  status: "queued" | "processing" | "completed" | "failed" | "cancelled";
  progress: number;
  current_step?: string;
  created_at?: string;
}

export interface JobStatus {
  job_id: string;
  status: "queued" | "processing" | "completed" | "failed" | "cancelled";
  progress: number;
  current_step?: string;
  file_name?: string;
  target_language?: string;
  created_at?: string;
  completed_at?: string;
  error?: string;
}
