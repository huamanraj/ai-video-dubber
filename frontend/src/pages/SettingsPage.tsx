import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { HealthIndicator } from "@/components/HealthIndicator";
import { api } from "@/lib/api";

export default function SettingsPage() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-lg font-semibold text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground mt-0.5">API configuration and status</p>
      </div>

      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="text-base">API Connection</CardTitle>
          <CardDescription>Your dubbing API endpoint</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-foreground">Base URL</label>
            <div className="px-3 py-2 rounded-md border bg-muted/50 font-mono text-sm text-foreground">
              {api.baseUrl}
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-foreground">Status:</span>
            <HealthIndicator />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
