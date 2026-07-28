from enum import Enum


class FaceEngine(str, Enum):
    FACENET = "facenet"
    INSIGHTFACE = "insightface"
