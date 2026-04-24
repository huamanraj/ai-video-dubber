import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: api.health,
    refetchInterval: 15000,
    retry: 1,
  });
}

export function useQueue() {
  return useQuery({
    queryKey: ["queue"],
    queryFn: api.getQueue,
    refetchInterval: 3000,
  });
}

export function useJobStatus(jobId: string | null) {
  return useQuery({
    queryKey: ["status", jobId],
    queryFn: () => api.getStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: 2000,
  });
}

export function useSubmitDub() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ file, targetLanguage, voiceId }: { file: File; targetLanguage: string; voiceId?: string }) =>
      api.submitDub(file, targetLanguage, voiceId),
    onSuccess: (data) => {
      toast({ title: "Job submitted", description: `Job ID: ${data.job_id}` });
      qc.invalidateQueries({ queryKey: ["queue"] });
    },
    onError: (err: Error) => {
      toast({ title: "Submission failed", description: err.message, variant: "destructive" });
    },
  });
}

export function useCancelJob() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (jobId: string) => api.cancelJob(jobId),
    onSuccess: () => {
      toast({ title: "Job cancelled" });
      qc.invalidateQueries({ queryKey: ["queue"] });
    },
    onError: (err: Error) => {
      toast({ title: "Cancel failed", description: err.message, variant: "destructive" });
    },
  });
}

export function useClearQueue() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.clearQueue(),
    onSuccess: () => {
      toast({ title: "Queue cleared" });
      qc.invalidateQueries({ queryKey: ["queue"] });
    },
    onError: (err: Error) => {
      toast({ title: "Clear failed", description: err.message, variant: "destructive" });
    },
  });
}
