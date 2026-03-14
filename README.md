# AI Video Dub

A full-stack application for automated video dubbing that converts videos to multiple languages using AI-powered speech-to-text, translation, and text-to-speech technologies.

## Overview

AI Video Dub is a production-ready system that takes a source video and creates dubbed versions in different target languages. The application features a React frontend for user interaction and a Python FastAPI backend for processing.

## Architecture

### Backend (FastAPI)
The backend (`main.py`) provides REST APIs for the video dubbing pipeline:
- **Upload Router**: Handles video file uploads
- **Status Router**: Returns job and system status
- **Queue Router**: Manages job queue operations
- **Download Router**: Serves processed output videos
- **Stream Router**: Streams real-time logs and updates

Key features:
- CORS enabled for frontend integration
- Async worker system for job processing
- SQLite database for job persistence
- WebSocket support for real-time updates

### Frontend (React + TypeScript + Vite)
The frontend (`App.tsx`) provides a user-friendly interface with:
- **Queue Page**: View job queue and processing history
- **Upload Page**: Upload videos and select target language
- **Settings Page**: Configure system and API settings
- **Sidebar Navigation**: Easy navigation between pages
- **Health Indicator**: Real-time system health status
- **Log Viewer**: Stream live processing logs

## Processing Pipeline

The pipeline (`runner.py`) consists of 7 sequential stages:

### Stage 1: Extract Audio
- **Technology**: FFmpeg
- Extracts audio track from the input MP4 video
- Converts to mono WAV at 16kHz sample rate (PCM 16-bit)
- Output: `audio.wav`

### Stage 2: Transcribe
- **Technology**: WhisperX (OpenAI Whisper) with PyTorch
- Converts audio to text using speech-to-text model
- Supports GPU acceleration (CUDA) with fallback to CPU
- Generates segments with precise timestamps and alignment
- Model caching to optimize repeated transcriptions
- Automatically detects source language
- Output: Array of text segments with timing information

### Stage 3: Translate
- **Technology**: Google Gemini API
- Translates each text segment to the target language
- Context-aware translation with regional language-specific prompts
- Special handling for Indian languages (Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia, Urdu, Assamese)
- Preserves tone, technical terms, and proper nouns
- Output: Translated text segments

### Stage 4: Text-to-Speech (TTS)
- **Technology**: Sarvam AI API (bulbul:v3 model)
- **Indian Languages**: IndicNLP text normalization + Sarvam TTS with voice selection
  - Normalizes Unicode, punctuation, and number forms for Indian scripts
  - Supports multiple voice options per language
- **Other Languages**: Sarvam TTS with voice selection
- Routes automatically based on target language
- Output: Audio clips for each segment (`.wav` files in `clips/` directory)

### Stage 5: Time Stretching
- **Technology**: FFmpeg (atempo filter) + PyDub
- Adjusts TTS clip duration to match original segment timing
- Applies audio tempo stretching (0.5x to 2.0x range) without changing pitch
- Preserves speech quality while aligning with source timing
- Output: Time-adjusted audio clips

### Stage 6: Audio Timeline Construction
- **Technology**: PyDub
- Builds complete dubbed audio track
- Overlays all clips at precise timestamps
- Maintains total duration matching original video (silent padding)
- Output: `dubbed_audio.wav`

### Stage 7: Video Muxing
- **Technology**: FFmpeg
- Combines original video with dubbed audio
- Removes original audio, replaces with dubbed version
- Uses stream copy for video codec (no re-encoding)
- Output: `output.mp4` (final dubbed video)

## Job Status Flow

```
   ┌─────────────────────────────────────┐
   │      UPLOAD VIDEO & SELECT LANG     │
   │      (Frontend: UploadPage)         │
   └──────────────┬──────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ JOB QUEUED (API)    │
        └─────┬───────────────┘
              │
              ▼
    ┌─────────────────────────────┐
    │ PROCESSING (Pipeline Worker)│
    │  Stage 1-7 with progress    │
    └─────┬───────────────────────┘
          │
          ├─────────► COMPLETED ─────► Download
          │
          └─────────► FAILED ────────► Error Message
```

## Job Object Structure

```json
{
  "job_id": "uuid",
  "status": "queued|processing|completed|failed",
  "video_file": "input.mp4",
  "target_lang": "language_code",
  "voice_id": "optional_voice_id",
  "stage": 1-7,
  "stage_name": "Stage Name",
  "progress": 0-100,
  "started_at": "ISO timestamp",
  "finished_at": "ISO timestamp",
  "error": "error message if failed"
}
```

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Task Queue**: Custom async worker system
- **Database**: SQLite with job persistence
- **Audio/Video Processing**: FFmpeg + FFProbe
- **Audio Library**: PyDub (audio manipulation and muxing)
- **ML & Deep Learning**:
  - **Speech-to-Text**: WhisperX (OpenAI Whisper) with PyTorch
  - **Translation**: Google Gemini API
  - **Text-to-Speech**: Sarvam AI API (bulbul:v3 model)
  - **Indic Language Processing**: IndicNLP (Unicode normalization for Indian scripts)
- **Real-time Updates**: WebSocket for streaming logs
- **Dependencies**: PyTorch, requests, soundfile, pydub

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router
- **State Management**: React Query for API calls
- **UI Components**: Custom shadcn/ui components
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Playwright

## Installation & Setup

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate  # On Windows

pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
bun install  # or npm install
```

## Running the Application

### Start Backend
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

### Start Frontend
```bash
cd frontend
bun run dev  # or npm run dev
# Runs on http://localhost:5173
```

### API Endpoints

**Health Check**
- `GET /health` - System health status
- `GET /` - API info

**Upload**
- `POST /api/upload` - Upload video

**Status**
- `GET /api/status/{job_id}` - Get job status

**Queue**
- `GET /api/queue` - Get all jobs
- `POST /api/queue/{job_id}/restart` - Restart failed job

**Download**
- `GET /api/download/{job_id}` - Download output video

**Stream**
- `WebSocket /api/stream/logs` - Stream real-time logs
- `WebSocket /api/stream/status` - Stream status updates

## Supported Languages

The system supports 200+ languages via NLLB model, with special optimized support for:
- **Indian Languages**: Hindi, Tamil, Telugu, Kannada, Malayalam, Punjabi, etc.
- **European Languages**: English, French, Spanish, German, Italian, Portuguese, etc.
- **Asian Languages**: Chinese, Japanese, Korean, Thai, Vietnamese, etc.

## File Structure

```
ai-video-dub/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration constants
│   ├── job_store.py         # SQLite database layer
│   ├── queue_manager.py     # Job queue worker
│   ├── requirements.txt     # Python dependencies
│   ├── pipeline/
│   │   ├── runner.py        # Main pipeline orchestrator
│   │   ├── stage1_extract.py     # Audio extraction
│   │   ├── stage2_transcribe.py  # Speech-to-text
│   │   ├── stage3_translate.py   # Translation
│   │   ├── stage4_tts.py         # Standard TTS
│   │   ├── stage4_tts_indic.py   # Indic language TTS
│   │   ├── stage5_stretch.py     # Audio time-stretching
│   │   ├── stage6_timeline.py    # Audio timeline building
│   │   └── stage7_mux.py         # Video muxing
│   ├── routers/
│   │   ├── upload.py
│   │   ├── status.py
│   │   ├── queue.py
│   │   ├── download.py
│   │   └── stream.py
│   └── uploads/              # Job working directories
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Main app component
│   │   ├── pages/
│   │   │   ├── QueuePage.tsx      # Job queue view
│   │   │   ├── UploadPage.tsx     # Video upload
│   │   │   └── SettingsPage.tsx   # Settings
│   │   ├── components/       # Reusable UI components
│   │   ├── hooks/            # Custom React hooks
│   │   └── lib/              # Utilities and API client
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
└── README.md
```

## Workflow

1. User uploads a video and selects target language via UploadPage
2. Frontend sends request to `/api/upload`
3. Backend creates job, stores in database, adds to queue
4. Async worker picks up job and starts 7-stage pipeline
5. Each stage updates job progress (0-100%)
6. Frontend polls status or uses WebSocket for real-time updates
7. After completion, user can download `output.mp4`
8. In case of failure, user can retry or view error logs

## Error Handling

- Comprehensive error logging at each pipeline stage
- Job status marked as "failed" with error details
- Frontend displays error messages to user
- Retry mechanism available for failed jobs
- ffmpeg validation ensures output integrity

## Performance Considerations

- Async processing prevents blocking API requests
- Threading for CPU-intensive operations (TTS, translation)
- Real-time progress updates for user feedback
- Modular pipeline stages allow future parallelization
- WebSocket streaming reduces polling overhead

