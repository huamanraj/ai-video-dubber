import { useState, useCallback, useRef, useEffect } from "react";
import { useSubmitDub } from "@/hooks/use-api";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, FileVideo, X, Loader2, Volume2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

// Only Indian languages supported by Sarvam TTS API
const LANGUAGES = [
  // Indian regional languages (10 supported by Sarvam TTS)
  { value: "hi", label: "Hindi" },
  { value: "bn", label: "Bengali" },
  { value: "ta", label: "Tamil" },
  { value: "te", label: "Telugu" },
  { value: "kn", label: "Kannada" },
  { value: "ml", label: "Malayalam" },
  { value: "mr", label: "Marathi" },
  { value: "gu", label: "Gujarati" },
  { value: "pa", label: "Punjabi" },
  { value: "or", label: "Odia" },
];

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("");
  const [voiceId, setVoiceId] = useState<string>("");
  const [availableVoices, setAvailableVoices] = useState<Array<{id: string, label: string}>>([]);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const submitDub = useSubmitDub();
  const navigate = useNavigate();

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.type.startsWith("video/")) {
      setFile(dropped);
    }
  }, []);

  // Update available voices when language changes
  useEffect(() => {
    if (language) {
      // All available Sarvam AI voices
      const allVoices = [
        "shubh", "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan",
        "simran", "kavya", "amit", "dev", "ishita", "shreya", "ratan", "varun",
        "manan", "sumit", "roopa", "kabir", "aayan", "ashutosh", "advait", "anand",
        "tanya", "tarun", "sunny", "mani", "gokul", "vijay", "shruti", "suhani",
        "mohit", "kavitha", "rehan", "soham", "rupali"
      ];
      
      // Capitalize first letter for display
      const voiceOptions = allVoices.map(id => ({
        id,
        label: id.charAt(0).toUpperCase() + id.slice(1)
      }));
      
      setAvailableVoices(voiceOptions);
      setVoiceId("shubh"); // Set default voice to shubh
    } else {
      setAvailableVoices([]);
      setVoiceId("");
    }
  }, [language]);

  const handleSubmit = () => {
    if (!file || !language) return;
    submitDub.mutate(
      { file, targetLanguage: language, voiceId },
      {
        onSuccess: () => {
          setFile(null);
          setLanguage("");
          setVoiceId("");
          setAvailableVoices([]);
          setTimeout(() => navigate("/dashboard"), 100);
        },
      }
    );
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-lg font-semibold text-foreground">Upload Video</h1>
        <p className="text-sm text-muted-foreground mt-0.5">
          Select a video file and target language to start dubbing
        </p>
      </div>

      <Card className="shadow-card">
        <CardContent className="p-6 space-y-5">
          {/* Drop zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            className={`relative border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors ${
              dragActive
                ? "border-primary bg-accent/50"
                : file
                ? "border-primary/40 bg-accent/30"
                : "border-border hover:border-primary/40 hover:bg-accent/20"
            }`}
          >
            <input
              ref={inputRef}
              type="file"
              accept="video/*"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) setFile(f);
              }}
            />
            {file ? (
              <div className="flex items-center justify-center gap-3 max-w-full px-4">
                <FileVideo className="h-8 w-8 text-primary flex-shrink-0" />
                <div className="text-left flex-1 min-w-0">
                  <p 
                    className="text-sm font-medium text-foreground truncate max-w-[300px]" 
                    title={file.name}
                  >
                    {file.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {(file.size / (1024 * 1024)).toFixed(1)} MB
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 flex-shrink-0"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                  }}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            ) : (
              <div className="space-y-2">
                <Upload className="h-8 w-8 text-muted-foreground/50 mx-auto" />
                <p className="text-sm text-muted-foreground">
                  Drop a video file here, or <span className="text-primary font-medium">browse</span>
                </p>
                <p className="text-xs text-muted-foreground/60">
                  MP4, MKV, AVI, MOV supported
                </p>
              </div>
            )}
          </div>

          {/* Language select */}
          <div className="space-y-1.5">
            <label className="text-sm font-medium text-foreground">Target Language</label>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger>
                <SelectValue placeholder="Select language" />
              </SelectTrigger>
              <SelectContent>
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang.value} value={lang.value}>
                    {lang.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Voice select (only shown when language is selected) */}
          {language && availableVoices.length > 0 && (
            <div className="space-y-1.5">
              <div className="flex items-center gap-1.5">
                <Volume2 className="h-3.5 w-3.5 text-muted-foreground" />
                <label className="text-sm font-medium text-foreground">Voice</label>
              </div>
              <Select value={voiceId} onValueChange={setVoiceId}>
                <SelectTrigger>
                  <SelectValue placeholder="Select voice" />
                </SelectTrigger>
                <SelectContent className="max-h-[300px]">
                  {availableVoices.map((voice) => (
                    <SelectItem key={voice.id} value={voice.id}>
                      {voice.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Using Sarvam AI Bulbul v3 model • 37 voices available
              </p>
            </div>
          )}

          {/* Submit */}
          <Button
            onClick={handleSubmit}
            disabled={!file || !language || submitDub.isPending}
            className="w-full"
          >
            {submitDub.isPending ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Submitting…
              </>
            ) : (
              "Start Dubbing"
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
