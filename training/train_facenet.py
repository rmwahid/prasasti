import os
import json
import numpy as np
from pathlib import Path
from PIL import Image
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

EMBEDDING_DIM = 512

def extract_embedding(mtcnn, resnet, img_path: str) -> np.ndarray | None:
    try:
        img = Image.open(img_path).convert('RGB')
        face_tensor = mtcnn(img)
        if face_tensor is None:
            print(f'  [SKIP] No face detected: {img_path}')
            return None
        with torch.no_grad():
            embedding = resnet(face_tensor.unsqueeze(0)).cpu().numpy().flatten()
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding.tolist()
    except Exception as e:
        print(f'  [ERROR] {img_path}: {e}')
        return None

def main():
    dataset_dir = os.environ.get('DATASET_DIR', './dataset')
    output_file = os.environ.get('OUTPUT_FILE', './output/embeddings.json')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')

    print('Loading MTCNN + InceptionResnetV1...')
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, device=device)
    resnet = InceptionResnetV1(classify=False, pretrained='vggface2').eval().to(device)

    results = []
    person_dirs = sorted([d for d in Path(dataset_dir).iterdir() if d.is_dir()])

    print(f'Found {len(person_dirs)} persons')

    for person_dir in person_dirs:
        name = person_dir.name
        photos = list(person_dir.glob('*.jpg')) + list(person_dir.glob('*.png')) + list(person_dir.glob('*.jpeg'))
        if not photos:
            print(f'  [SKIP] {name}: no images')
            continue

        embeddings = []
        for photo in photos:
            emb = extract_embedding(mtcnn, resnet, str(photo))
            if emb is not None:
                embeddings.append(emb)

        if not embeddings:
            print(f'  [SKIP] {name}: no face detected in any photo')
            continue

        avg_embedding = np.mean(embeddings, axis=0).tolist()
        results.append({
            'person_name': name,
            'model_version': 'facenet-vggface2',
            'vector': avg_embedding,
            'source_photos': [p.name for p in photos],
        })
        print(f'  [OK] {name}: {len(embeddings)}/{len(photos)} faces -> averaged')

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\nDone! {len(results)} persons saved to {output_file}')

if __name__ == '__main__':
    main()
