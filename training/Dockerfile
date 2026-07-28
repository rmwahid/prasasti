FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train_facenet.py .

ENV DATASET_DIR=/app/dataset
ENV OUTPUT_FILE=/app/output/embeddings.json

CMD ["python", "train_facenet.py"]
