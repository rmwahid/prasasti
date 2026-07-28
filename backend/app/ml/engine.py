import numpy as np
from PIL import Image
from io import BytesIO

from app.core.logging import logger
from app.ml.config import FaceEngine
from app.core.config import settings


class FaceEngineBase:
    """Base class for face recognition engines.

    Switchable: implement extract() for each engine.
    To add a new engine, subclass this and update create_engine().
    """

    def extract(self, image_bytes: bytes) -> np.ndarray | None:
        """Extract face embedding from image bytes.

        Returns:
            np.ndarray of shape (embedding_dim,) or None if no face detected.
        """
        raise NotImplementedError

    @property
    def embedding_dim(self) -> int:
        return settings.face_embedding_dim


class FaceNetEngine(FaceEngineBase):
    """FaceNet via facenet-pytorch (MTCNN + InceptionResnetV1)."""

    def __init__(self):
        import torch
        from facenet_pytorch import MTCNN, InceptionResnetV1

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"FaceNet: loading on {device}")

        self.mtcnn = MTCNN(
            image_size=160,
            margin=0,
            min_face_size=20,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            device=device,
        )

        # VGGFace2 pretrained model
        self.resnet = InceptionResnetV1(
            classify=False, pretrained="vggface2"
        ).eval().to(device)

        self.device = device
        logger.info("FaceNet: model loaded")

    def extract(self, image_bytes: bytes) -> np.ndarray | None:
        import torch

        img = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Detect + align face
        face_tensor = self.mtcnn(img)
        if face_tensor is None:
            logger.warning("FaceNet: no face detected in image")
            return None

        # Extract embedding
        with torch.no_grad():
            embedding = self.resnet(face_tensor.unsqueeze(0).to(self.device))

        return embedding.cpu().numpy().flatten()


class InsightFaceEngine(FaceEngineBase):
    """InsightFace via insightface package.

    Note: model weights are non-commercial. Use for research/experiment only.
    """

    def __init__(self):
        import insightface
        from insightface.app import FaceAnalysis

        self.app = FaceAnalysis(name="buffalo_l", root="~/.insightface/models")
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        logger.info("InsightFace: model loaded")

    def extract(self, image_bytes: bytes) -> np.ndarray | None:
        import cv2
        import numpy as np

        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        faces = self.app.get(img)
        if not faces:
            logger.warning("InsightFace: no face detected")
            return None

        # Use the largest face if multiple detected
        faces = sorted(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
        return faces[0].embedding


def create_engine(engine_name: str | None = None) -> FaceEngineBase:
    """Factory: create face engine by name (from env or param)."""
    name = (engine_name or settings.face_engine).lower()

    if name == FaceEngine.FACENET:
        return FaceNetEngine()
    elif name == FaceEngine.INSIGHTFACE:
        logger.warning("InsightFace weights are non-commercial licensed!")
        return InsightFaceEngine()
    else:
        raise ValueError(f"Unknown face engine: {name}")
