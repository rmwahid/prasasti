from io import BytesIO

import numpy as np
from PIL import Image

from app.core.logging import logger
from app.ml.engine import FaceEngineBase


class FaceExtractor:
    """Wraps engine.extract() with image validation."""

    def __init__(self, engine: FaceEngineBase):
        self.engine = engine

    def extract(self, image_bytes: bytes) -> np.ndarray | None:
        """Validate image then extract embedding."""
        try:
            # Quick validation: can Pillow open it?
            img = Image.open(BytesIO(image_bytes))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image: {e}")
            return None

        # Re-open after verify (Pillow closes the file after verify)
        embedding = self.engine.extract(image_bytes)
        if embedding is None:
            logger.warning("No face detected in uploaded image")
            return None

        # Normalize to unit vector for cosine similarity
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding
