import { useState, useEffect } from "react";
import { useQueue, useCancelJob } from "@/hooks/use-api";
import { StatusBadge } from "@/components/StatusBadge";
import { LogViewer } from "@/components/LogViewer";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { api } from "@/lib/api";
import { Download, X, ChevronDown, ChevronRight, Loader2, InboxIcon } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";



export default function QueuePage() {
  const { data: queue, isLoading, isError } = useQueue();
  const cancelJob = useCancelJob();
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [cancelId, setCancelId] = useState<string | null>(null);
  const [progressAnimations, setProgressAnimations] = useState<Record<string, number>>({});

  // Animate progress bars
  useEffect(() => {
    if (!queue) return;
    
    const newAnimations: Record<string, number> = {};
    queue.forEach(job => {
      if (job.status === "processing" || job.status === "queued") {
        // Smooth animation for processing jobs
        const targetProgress = job.progress;
        const currentProgress = progressAnimations[job.job_id] || 0;
        
        if (Math.abs(targetProgress - currentProgress) > 1) {
          newAnimations[job.job_id] = currentProgress + (targetProgress - currentProgress) * 0.3;
        } else {
          newAnimations[job.job_id] = targetProgress;
        }
      } else {
        newAnimations[job.job_id] = job.progress;
      }
    });
    
    setProgressAnimations(newAnimations);
  }, [queue]);

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  const handleDownload = (jobId: string) => {
    window.open(api.getDownloadUrl(jobId), "_blank");
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-lg font-semibold text-foreground">Queue</h1>
        <p className="text-sm text-muted-foreground mt-0.5">
          Monitor and manage your dubbing jobs
        </p>
      </div>

      <div className="border rounded-lg overflow-hidden bg-card shadow-card">
        {isLoading ? (
          <div className="p-6 space-y-3">
            {[...Array(4)].map((_, i) => (
              <Skeleton key={i} className="h-10 w-full" />
            ))}
          </div>
        ) : isError ? (
          <div className="p-12 text-center">
            <p className="text-sm text-destructive font-medium">Failed to load queue</p>
            <p className="text-xs text-muted-foreground mt-1">
              Make sure your API server is running at {api.baseUrl}
            </p>
          </div>
        ) : !queue || queue.length === 0 ? (
          <div className="p-12 text-center">
            <InboxIcon className="h-10 w-10 text-muted-foreground/40 mx-auto mb-3" />
            <p className="text-sm font-medium text-muted-foreground">No jobs in queue</p>
            <p className="text-xs text-muted-foreground/70 mt-1">
              Upload a video to get started
            </p>
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead className="w-10" />
                <TableHead>Job ID</TableHead>
                <TableHead>File</TableHead>
                <TableHead>Language</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-[180px]">Progress</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {queue.map((job) => (
                <>
                  <TableRow
                    key={job.job_id}
                    className="cursor-pointer"
                    onClick={() => toggleExpand(job.job_id)}
                  >
                    <TableCell className="pr-0">
                      {expandedId === job.job_id ? (
                        <ChevronDown className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      )}
                    </TableCell>
                    <TableCell className="font-mono text-xs">
                      {job.job_id.slice(0, 8)}…
                    </TableCell>
                    <TableCell className="text-sm max-w-[200px] truncate">
                      {job.file_name}
                    </TableCell>
                    <TableCell className="text-sm capitalize">
                      {job.target_language}
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={job.status} />
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <div className="text-xs text-muted-foreground">
                              Stage {job.stage || 0}/7
                            </div>
                            <div className="flex-1">
                              <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-primary transition-all duration-500 ease-out"
                                  style={{ 
                                    width: `${progressAnimations[job.job_id] || job.progress}%`,
                                    transition: 'width 0.5s ease-in-out'
                                  }}
                                />
                              </div>
                            </div>
                            <span className="text-xs text-muted-foreground w-8 text-right">
                              {Math.round(progressAnimations[job.job_id] || job.progress)}%
                            </span>
                          </div>
                          <div className="text-xs text-muted-foreground truncate">
                            {job.current_step || "Waiting in queue"}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-right" onClick={(e) => e.stopPropagation()}>
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-7 w-7 p-0"
                          onClick={() => handleDownload(job.job_id)}
                          disabled={job.status !== "completed"}
                          title={
                            job.status === "completed"
                              ? "Download dubbed video"
                              : "Download available after completion"
                          }
                        >
                          <Download className="h-3.5 w-3.5" />
                        </Button>
                        {(job.status === "queued" || job.status === "processing") && (
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-7 w-7 p-0 text-destructive hover:text-destructive"
                            onClick={() => setCancelId(job.job_id)}
                            disabled={cancelJob.isPending}
                          >
                            {cancelJob.isPending ? (
                              <Loader2 className="h-3.5 w-3.5 animate-spin" />
                            ) : (
                              <X className="h-3.5 w-3.5" />
                            )}
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                  {expandedId === job.job_id && (
                    <TableRow key={`${job.job_id}-logs`} className="hover:bg-transparent">
                      <TableCell colSpan={7} className="p-4">
                        {job.current_step && (
                          <p className="text-xs text-muted-foreground mb-2">
                            Current step: <span className="font-medium text-foreground">{job.current_step}</span>
                          </p>
                        )}
                        <LogViewer jobId={job.job_id} />
                      </TableCell>
                    </TableRow>
                  )}
                </>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      <AlertDialog open={!!cancelId} onOpenChange={() => setCancelId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Cancel this job?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. The job will be stopped and removed from the queue.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Keep running</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={() => {
                if (cancelId) cancelJob.mutate(cancelId);
                setCancelId(null);
              }}
            >
              Cancel job
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
