# Local Video Dubbing Backend

Runs entirely locally on a GTX 1650 (4GB VRAM, 8GB RAM). Zero paid APIs, zero cloud calls.

---

## Prerequisites

Install these before anything else:

- **Python 3.12**
- **CUDA 12.1** — [download](https://developer.nvidia.com/cuda-12-1-0-download-archive)
- **ffmpeg** (must be on PATH) — [download](https://ffmpeg.org/download.html)
  - Verify: `ffmpeg -version` and `ffprobe -version`
- **Git** (needed to install whisperx from source)

---

## Project Structure

```
backend/
├── main.py
├── config.py
├── job_store.py
├── queue_manager.py
├── requirements.txt
├── pipeline/
│   ├── stage1_extract.py
│   ├── stage2_transcribe.py
│   ├── stage3_translate.py
│   ├── stage4_tts.py
│   ├── stage5_stretch.py
│   ├── stage6_timeline.py
│   ├── stage7_mux.py
│   └── runner.py
└── routers/
    ├── upload.py
    ├── stream.py
    ├── status.py
    ├── download.py
    ├── queue.py
    └── health.py
```

---

## Setup

### 1. Create and activate virtual environment

```bash
cd "c:\Users\amanr\OneDrive\Desktop\AI VIDEO DUBBING\backend"
python -m venv venv
venv\Scripts\activate
```

### 2. Install PyTorch with CUDA 12.1 first

```bash
pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

### 3. Install remaining dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify GPU is detected

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Expected output: `True  NVIDIA GeForce GTX 1650`

---

## Running the Server

```bash
cd "c:\Users\amanr\OneDrive\Desktop\AI VIDEO DUBBING\backend"
venv\Scripts\activate
venv\Scripts\python.exe main.py
```

If you use Git Bash, prefer:

```bash
./venv/Scripts/python.exe main.py
```

This avoids accidentally launching system Python (which may not have `whisperx` installed).

Server starts at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/docs**

---

## API Usage

### Submit a dubbing job

```bash
curl -X POST http://localhost:8000/dub \
  -F "video=@myvideo.mp4" \
  -F "target_language=hi"
```

Response:
```json
{ "job_id": "abc123...", "queue_position": 1 }
```

### Check job status

```bash
curl http://localhost:8000/status/abc123...
```

Response fields:
| Field | Description |
|---|---|
| `status` | `queued` / `processing` / `done` / `failed` |
| `stage` | Stage number 1–7 |
| `stage_name` | Human-readable stage description |
| `progress` | 0–100 within current stage |
| `queue_position` | Position in queue (0 = currently running) |
| `error` | Error message if failed |

### Stream live progress (SSE)

```bash
curl -N http://localhost:8000/stream/abc123...
```

Pushes full job state JSON on every change until `done` or `failed`.

### Download result

```bash
curl -OJ http://localhost:8000/download/abc123...
```

Saves as `originalname_dubbed.mp4`.

### View queue

```bash
curl http://localhost:8000/queue
```

### Cancel a queued job

```bash
curl -X DELETE http://localhost:8000/queue/abc123...
```

Cannot cancel a job that is already `processing`.

### Health check

```bash
curl http://localhost:8000/health
```

Response:
```json
{ "status": "ok", "gpu_vram_free_mb": 3800.0, "jobs_in_queue": 2 }
```

---

## Supported Target Languages

| Code | Language | TTS Engine |
|------|----------|------------|
| `es` | Spanish | F5-TTS |
| `fr` | French | F5-TTS |
| `de` | German | F5-TTS |
| `pt` | Portuguese | F5-TTS |
| `ar` | Arabic | F5-TTS |
| `ja` | Japanese | F5-TTS |
| `ko` | Korean | F5-TTS |
| `zh` | Chinese | F5-TTS |
| `tr` | Turkish | F5-TTS |
| `it` | Italian | F5-TTS |
| `hi` | Hindi | IndicF5 🇮🇳 |
| `bn` | Bengali | IndicF5 🇮🇳 |
| `ta` | Tamil | IndicF5 🇮🇳 |
| `te` | Telugu | IndicF5 🇮🇳 |
| `kn` | Kannada | IndicF5 🇮🇳 |
| `ml` | Malayalam | IndicF5 🇮🇳 |
| `mr` | Marathi | IndicF5 🇮🇳 |
| `gu` | Gujarati | IndicF5 🇮🇳 |
| `pa` | Punjabi | IndicF5 🇮🇳 |
| `or` | Odia | IndicF5 🇮🇳 |
| `ur` | Urdu | Indic Parler-TTS 🇮🇳 |

### Indian Language Notes

- **IndicF5** (10 languages) — F5-TTS fine-tuned by AI4Bharat (IIT Madras) on 1,417 hours of Indian speech. Supports voice cloning from the original speaker.
- **Indic Parler-TTS** (Urdu fallback) — No voice cloning; uses a preset natural voice. Covers 21 Indian languages.
- **Voice cloning quality** — Cloned voices for Indian languages have a slight accent overlay from training data. This is the current best open-source option.

---

## Pipeline Stages

| # | Name | Tool | Device |
|---|------|------|--------|
| 1 | Extracting audio | ffmpeg | CPU |
| 2 | Transcribing audio | WhisperX medium int8 | GPU |
| 3 | Translating segments | NLLB-200-distilled-600M | CPU |
| 4 | Generating dubbed speech | F5-TTS (voice cloning) | GPU |
| 5 | Syncing audio timing | ffmpeg atempo filter | CPU |
| 6 | Assembling audio track | pydub | CPU |
| 7 | Muxing final video | ffmpeg | CPU |

> **Note:** WhisperX and F5-TTS are never loaded in VRAM at the same time.
> VRAM is fully cleared between stages 2 and 4.

---

## Output Files

All job files are stored under `uploads/{job_id}/`:

```
uploads/{job_id}/
├── input.mp4          # uploaded video
├── audio.wav          # extracted 16kHz mono audio
├── ref_6sec.wav       # voice reference for cloning
├── clips/
│   ├── clip_0.wav     # raw TTS clip per segment
│   ├── stretched_0.wav
│   └── ...
├── dubbed_audio.wav   # assembled audio track
└── output.mp4         # final dubbed video
```

---

## Troubleshooting

**`ffmpeg` or `ffprobe` not found**
→ Add ffmpeg's `bin/` folder to your system PATH and restart the terminal.

**CUDA out of memory**
→ Close other GPU applications. Only one job runs at a time but the GTX 1650 has 4GB — large videos with many segments may be tight.

**WhisperX download fails**
→ Ensure Git is installed and run: `pip install git+https://github.com/m-bain/whisperX.git`

**`No module named 'whisperx'` at Stage 2**
→ Install in the same environment used to run the backend:
`python -m pip install whisperx`

**NumPy or `pkg_resources` errors while importing WhisperX**
→ Use compatible versions:
`python -m pip install "numpy<2" "setuptools<81"`

**Repeated HuggingFace Xet fallback warning**
→ Install optional accelerator package:
`python -m pip install hf_xet`

**WhisperX says no language specified / slower first stage**
→ If your source audio language is known, set once before running backend:
`set WHISPER_SOURCE_LANGUAGE=hi`
This skips language auto-detection in stage 2.

**Models downloading on first run**
→ WhisperX (`medium`, ~1.5GB) and NLLB-200 (~2.4GB) download automatically to the HuggingFace cache on first use. Subsequent runs use the cache.
