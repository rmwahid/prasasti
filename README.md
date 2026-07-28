# PRASASTI

**Photo Recognition Archive for Social And Security Trace Intelligence**

<p align="center">
  <strong>Platform Pengenalan Wajah Berbasis Biometrik untuk Arsip Kasus Kejahatan Indonesia</strong>
</p>

---

## Tentang

PRASASTI adalah sistem pengenalan wajah (face recognition) yang dirancang khusus untuk mengarsipkan dan melacak kasus-kasus kejahatan di Indonesia. Sistem ini bekerja dengan mengekstrak data biometrik wajah, menyimpannya sebagai vektor matematika, lalu mencocokkannya ketika ada foto baru yang diunggah.

### Filosofi

Nama **PRASASTI** terinspirasi dari prasasti batu - batu tulis kuno yang menyimpan catatan sejarah secara permanen. Begitu pula sistem ini: menyimpan jejak digital secara terstruktur, tidak mudah hilang, dan dapat diakses kembali kapan saja.

> "Seperti prasasti yang mengukir sejarah di batu, PRASASTI mengukir jejak kejahatan dalam database."

PRASASTI bukan alat untuk menjatuhkan seseorang. Ini adalah **arsip digital** yang menyimpan data yang sudah ada/disadur di berbagai media - nama, kasus, dan pemberitaan - lalu membuatnya dapat dicari melalui teknologi pengenalan wajah. Tujuannya transparansi dan akuntabilitas.

---

**Photo Recognition Archive for Social And Security Trace Intelligence**

<p align="center">
  <strong>Biometric Face Recognition Archive for Indonesian Crime Cases</strong>
</p>

---

## About

PRASASTI is a face recognition system designed to archive and track criminal cases in Indonesia. The system extracts facial biometric data, stores it as mathematical vectors, and matches them when a new photo is uploaded.

### Philosophy

The name **PRASASTI** is an Indonesian word meaning "stone inscription" - ancient carved stone tablets found across the Indonesian archipelago that have preserved history, laws, and events for centuries. We chose this name because, just as those stones permanently etched records into stone, this system permanently archives digital traces of crime into a searchable database.

> "Like a prasasti that has preserved Indonesian history for centuries, PRASASTI preserves the digital traces of crime for the future."

PRASASTI is not a tool to condemn. It is a **digital archive** that stores data already reported in various media - names, cases, and coverage - and makes it searchable through face recognition technology. The goal is transparency and accountability.

---

## How It Works

1. **Training**: Faces are processed on cloud GPU (RunPod) using FaceNet model. Output: 512-dimensional vector representing facial biometrics.
2. **Inject**: Admin inputs person data (name, bio, criminal cases) along with embedding vectors into the database.
3. **Search**: Mobile user takes/uploads a photo, backend extracts embedding from the photo, matches against all vectors in database, then displays results with confidence score and case history.

---

## Architecture

| Component | Technology | Description |
|---|---|---|
| **Backend API** | Python, FastAPI, SQLAlchemy 2.0 | Layered REST API (endpoints -> services -> repositories -> models) |
| **Database** | PostgreSQL + pgvector | Relational data + face vectors, cosine similarity search with HNSW index |
| **Face Recognition** | FaceNet (facenet-pytorch) | Face recognition model, 512-dim embedding output. Commercial-friendly license |
| **Admin Panel** | SvelteKit + shadcn-svelte | Dashboard for data input, embedding injection, and monitoring |
| **Mobile App** | Flutter | Photo/upload face and view match results |
| **Training** | Python + RunPod (GPU Cloud) | Face training script, runs on RunPod pay-per-use |
| **Deployment** | Docker Compose, Hetzner VPS | All services containerized |

---

## Repo Structure
```
repo/
├── backend/              # Python FastAPI
│   ├── app/
│   │   ├── api/          # Endpoints (route handlers)
│   │   ├── core/         # Config, database, logging
│   │   ├── ml/           # Face recognition engine (FaceNet/InsightFace)
│   │   ├── models/       # SQLAlchemy ORM
│   │   ├── repositories/ # Query database
│   │   ├── schemas/      # Pydantic DTO
│   │   ├── services/     # Business logic
│   │   └── main.py       # Bootstrap app
│   ├── alembic/          # Database migration
│   └── Dockerfile
├── admin/                # SvelteKit + shadcn-svelte
├── mobile/               # Flutter
├── training/             # Script training (RunPod)
├── docker-compose.yml    # Service orchestration
└── .env.example
```
---

## Project Status

| Component | Status | Notes |
|---|---|---|
| Backend API | In Progress | All endpoints including face search |
| Database Schema | In Progress | Alembic migration + pgvector HNSW |
| Face Engine | In Progress | FaceNet + switchable InsightFace |
| Admin Panel | In Progress | SvelteKit + shadcn-svelte |
| Training Script | Pending | Script + Docker + RunPod guide |
| Mobile App | Pending | Flutter |
| Docker Compose | Pending | Full service integration |
| Login & Auth | Pending | Not yet implemented |
| Upvote/Downvote | Pending | Not yet implemented |
| Payment (Coin Topup) | Pending | Not yet implemented |

---

## Development Ideas

### Fugitive Tracking
- **Fugitive Database**: Dedicated database for wanted persons (DPO)
- **Public Reporting**: Users can report sightings of fugitives in public
- **Geotagging**: Uploaded photos with GPS location -> sighting map
- **Police Integration**: API for law enforcement systems

### National Scale
- **Multi-Model Ensemble**: Combine multiple face recognition models for higher accuracy
- **Custom Training**: Indonesian face dataset for better accuracy on Indonesian faces
- **Real-time Streaming**: CCTV integration for real-time face detection
- **Court Archive Integration**: Connect with court decisions (public data from PN/e-Court)

### Ecosystem
- **Open Data API**: Public API for journalists and researchers
- **Crowdsourced Validation**: Collaborative data validation by the public
- **Browser Extension**: Chrome extension to scan faces from web photos
- **Media Integration**: Partnership with investigative media

---

## Ethics & Legal
- All stored data is sourced from publicly available information already reported in various media
- This system is **not** a legal tool -- match results show confidence levels, not legal proof
- "Possibly wrong person" label shown for low-confidence matches
- Model FaceNet chosen for its **commercial-friendly license** (MIT/Apache)

---

## License

TBD

---

<p align="center">
  <em>Dibangun untuk transparansi dan akuntabilitas hukum di Indonesia.</em>
  <br>
  <em>Built for transparency and legal accountability in Indonesia.</em>
</p>
