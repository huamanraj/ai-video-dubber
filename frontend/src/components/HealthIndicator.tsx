import { useHealth } from "@/hooks/use-api";

export function HealthIndicator() {
  const { data, isError, isLoading } = useHealth();

  const isHealthy = data?.status === "ok" || data?.status === "healthy";

  return (
    <div className="flex items-center gap-2 text-xs font-medium">
      <span
        className={`h-2 w-2 rounded-full ${
          isLoading
            ? "bg-muted-foreground animate-pulse-subtle"
            : isError || !isHealthy
            ? "bg-destructive"
            : "bg-primary"
        }`}
      />
      <span className="text-muted-foreground">
        {isLoading ? "Connecting…" : isError || !isHealthy ? "API Offline" : "API Online"}
      </span>
    </div>
  );
}
