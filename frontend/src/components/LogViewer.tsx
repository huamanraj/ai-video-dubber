import { useEffect, useRef } from "react";
import { useLogStream } from "@/hooks/use-log-stream";
import { Terminal } from "lucide-react";

export function LogViewer({ jobId }: { jobId: string }) {
  const { logs, connected } = useLogStream(jobId);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="rounded-md border bg-foreground/[0.03] overflow-hidden">
      <div className="flex items-center gap-2 px-3 py-2 border-b bg-muted/50">
        <Terminal className="h-3.5 w-3.5 text-muted-foreground" />
        <span className="text-xs font-medium text-muted-foreground">Live Logs</span>
        {connected && (
          <span className="ml-auto flex items-center gap-1.5 text-xs text-primary">
            <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse-subtle" />
            Streaming
          </span>
        )}
      </div>
      <div
        ref={containerRef}
        className="h-48 overflow-y-auto p-3 font-mono text-xs leading-relaxed text-muted-foreground"
      >
        {logs.length === 0 ? (
          <span className="text-muted-foreground/60">Waiting for logs…</span>
        ) : (
          logs.map((line, i) => (
            <div key={i} className="whitespace-pre-wrap">
              {line}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
