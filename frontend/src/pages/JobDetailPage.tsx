import { useParams, useNavigate } from "react-router-dom";
import { useJobStatus } from "@/hooks/use-api";
import { StatusBadge } from "@/components/StatusBadge";
import { LogViewer } from "@/components/LogViewer";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import {
  ArrowLeft, Download, Mic, FileText, Languages, Volume2,
  Layers, Music2, Film, CheckCircle2, Loader2, Circle, AlertCircle,
} from "lucide-react";

const STAGES = [
  { label: "Extract Audio",       icon: Mic       },
  { label: "Transcribe Speech",   icon: FileText  },
  { label: "Translate Text",      icon: Languages },
  { label: "Synthesize Voice",    icon: Volume2   },
  { label: "Separate Background", icon: Layers    },
  { label: "Mix Audio",           icon: Music2    },
  { label: "Render Output",       icon: Film      },
];

function VideoPlayer({ src, label }: { src: string; label: string }) {
  return (
    <div className="flex flex-col gap-2">
      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">{label}</p>
      <div className="rounded-lg overflow-hidden bg-black border border-border aspect-video">
        <video
          className="w-full h-full object-contain"
          controls
          preload="metadata"
          src={src}
        />
      </div>
    </div>
  );
}

export default function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const { data: job, isLoading, isError } = useJobStatus(jobId!);

  const currentStage = job?.stage ?? 0;
  const progress = job?.progress ?? 0;
  const isFailed = job?.status === "failed";
  const isCompleted = job?.status === "completed";
  const isActive = job?.status === "processing" || job?.status === "queued";

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (isError || !job) {
    return (
      <div className="text-center py-16">
        <AlertCircle className="h-8 w-8 text-destructive mx-auto mb-3" />
        <p className="text-sm text-destructive font-medium">Job not found</p>
        <Button variant="ghost" size="sm" className="mt-4" onClick={() => navigate("/dashboard")}>
          <ArrowLeft className="h-4 w-4 mr-1.5" /> Back to queue
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-start gap-4">
        <Button variant="ghost" size="sm" className="mt-0.5 -ml-2" onClick={() => navigate("/dashboard")}>
          <ArrowLeft className="h-4 w-4 mr-1" /> Queue
        </Button>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h1 className="text-lg font-semibold text-foreground truncate">{job.file_name}</h1>
            <StatusBadge status={job.status} />
          </div>
          <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
            <span className="font-mono">{jobId?.slice(0, 12)}…</span>
            <span>·</span>
            <span className="capitalize">{job.target_language}</span>
            {job.created_at && (
              <>
                <span>·</span>
                <span>{new Date(job.created_at).toLocaleString()}</span>
              </>
            )}
          </div>
        </div>
        {isCompleted && (
          <Button
            size="sm"
            onClick={() => window.open(api.getDownloadUrl(jobId!), "_blank")}
          >
            <Download className="h-3.5 w-3.5 mr-1.5" /> Download
          </Button>
        )}
      </div>

      {/* Progress */}
      <div className="border rounded-lg p-5 bg-card shadow-card space-y-5">
        {/* Overall bar */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{job.current_step || "Waiting in queue"}</span>
            <span className="font-medium text-foreground">{Math.round(progress)}%</span>
          </div>
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-700 ease-out ${
                isFailed ? "bg-destructive" : "bg-primary"
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Stage pipeline */}
        <div className="flex items-start gap-0">
          {STAGES.map((stage, idx) => {
            const stageNum = idx + 1;
            const done = currentStage > stageNum || isCompleted;
            const active = currentStage === stageNum && isActive;
            const failed = isFailed && currentStage === stageNum;
            const Icon = stage.icon;

            return (
              <div key={idx} className="flex items-start flex-1 min-w-0">
                <div className="flex flex-col items-center flex-1 min-w-0">
                  {/* Circle */}
                  <div
                    className={`relative flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all ${
                      done
                        ? "bg-primary border-primary text-primary-foreground"
                        : active
                        ? "border-primary text-primary bg-primary/10"
                        : failed
                        ? "border-destructive text-destructive bg-destructive/10"
                        : "border-border text-muted-foreground bg-muted/50"
                    }`}
                  >
                    {done ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : active ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : failed ? (
                      <AlertCircle className="h-4 w-4" />
                    ) : (
                      <Icon className="h-3.5 w-3.5" />
                    )}
                  </div>
                  {/* Label */}
                  <p
                    className={`mt-1.5 text-center text-[10px] leading-tight px-0.5 truncate w-full ${
                      done
                        ? "text-primary font-medium"
                        : active
                        ? "text-foreground font-medium"
                        : "text-muted-foreground"
                    }`}
                  >
                    {stage.label}
                  </p>
                </div>
                {/* Connector */}
                {idx < STAGES.length - 1 && (
                  <div
                    className={`h-0.5 flex-shrink-0 mt-4 w-full transition-all ${
                      currentStage > stageNum || isCompleted ? "bg-primary" : "bg-border"
                    }`}
                    style={{ maxWidth: "100%", minWidth: 8 }}
                  />
                )}
              </div>
            );
          })}
        </div>

        {/* Error message */}
        {isFailed && job.error && (
          <div className="rounded-md bg-destructive/10 border border-destructive/20 px-3 py-2">
            <p className="text-xs text-destructive font-medium">Error: {job.error}</p>
          </div>
        )}
      </div>

      {/* Video comparison */}
      {(isCompleted || isActive) && (
        <div className="border rounded-lg p-5 bg-card shadow-card">
          <h2 className="text-sm font-medium text-foreground mb-4">Video Preview</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <VideoPlayer src={api.getOriginalVideoUrl(jobId!)} label="Original" />
            {isCompleted ? (
              <VideoPlayer src={api.getDownloadUrl(jobId!)} label="Dubbed Output" />
            ) : (
              <div className="flex flex-col gap-2">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Dubbed Output</p>
                <div className="rounded-lg bg-muted/50 border border-border aspect-video flex flex-col items-center justify-center gap-2">
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground/50" />
                  <p className="text-xs text-muted-foreground">Processing…</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Logs */}
      <div className="border rounded-lg p-5 bg-card shadow-card">
        <h2 className="text-sm font-medium text-foreground mb-3">Live Logs</h2>
        <LogViewer jobId={jobId!} />
      </div>
    </div>
  );
}
