import { useEffect, useRef, useState, useCallback } from "react";
import { api } from "@/lib/api";

export function useLogStream(jobId: string | null) {
  const [logs, setLogs] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  const disconnect = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
      setConnected(false);
    }
  }, []);

  useEffect(() => {
    if (!jobId) return;
    setLogs([]);

    const es = new EventSource(api.getStreamUrl(jobId));
    esRef.current = es;

    es.onopen = () => setConnected(true);
    es.onmessage = (e) => {
      setLogs((prev) => [...prev, e.data]);
    };
    es.onerror = () => {
      setConnected(false);
      es.close();
    };

    return () => {
      es.close();
      esRef.current = null;
      setConnected(false);
    };
  }, [jobId]);

  return { logs, connected, disconnect };
}
