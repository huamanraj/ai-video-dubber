import { Badge } from "@/components/ui/badge";

const statusConfig: Record<string, { label: string; className: string }> = {
  queued: {
    label: "Queued",
    className: "bg-muted text-muted-foreground border-border",
  },
  processing: {
    label: "Processing",
    className: "bg-accent text-warning-foreground border-border",
  },
  completed: {
    label: "Completed",
    className: "bg-accent text-primary border-border",
  },
  failed: {
    label: "Failed",
    className: "bg-destructive/10 text-destructive border-destructive/20",
  },
  cancelled: {
    label: "Cancelled",
    className: "bg-muted text-muted-foreground border-border",
  },
};

export function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status] || statusConfig.queued;
  return (
    <Badge variant="outline" className={`text-xs font-medium ${config.className}`}>
      {config.label}
    </Badge>
  );
}
