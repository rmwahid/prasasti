# RunPod Guide - Training Wajah

## Setup Pod

1. Buka https://www.runpod.io dan buat akun
2. Klik **Deploy > Custom Deploy**
3. Pilih **GPU: RTX 3090** (~$0.4/jam)
4. Di **Docker Image**, masukkan path ke Docker image ini (atau upload folder training)
5. Set **Volume** persistent agar foto & model tersimpan antar sesi

## Struktur Dataset

```
dataset/
  Nama_Koruptor_1/
    foto1.jpg
    foto2.jpg
    foto3.png
  Nama_Koruptor_2/
    foto1.jpg
    ...
```

- Min 5 foto per orang
- Wajah jelas, tidak tertutup
- Beragam sudut jika bisa

## Run Training

```bash
# Kalau pakai Docker
python train_facenet.py

# Atau langsung
DATASET_DIR=./dataset OUTPUT_FILE=./output/embeddings.json python train_facenet.py
```

## Output

File `embeddings.json` berisi:

```json
[
  {
    "person_name": "Nama Koruptor",
    "model_version": "facenet-vggface2",
    "vector": [0.123, -0.456, ...],
    "source_photos": ["foto1.jpg", "foto2.jpg"]
  }
]
```

## Inject ke Admin

1. Download `embeddings.json` dari RunPod
2. Buka Admin Panel > Embeddings
3. Pilih Person dari dropdown
4. Paste vector array dari JSON
5. Klik **Inject Single** (satu) atau **Inject Batch** (banyak sekaligus)

## Tips Hemat
- Matikan pod setelah training selesai
- Pakai persistent volume biar gak upload foto ulang
- Training 50 orang biasanya < 1 jam
