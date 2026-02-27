import face_recognition
import numpy as np

class FaceEncoder:
    def __init__(self):
        pass

    def get_embedding(self, frame, bbox=None):
        """
        Génère un embedding de 128 dimensions pour un visage.
        Si bbox est fourni, on encode cette zone. Sinon, on cherche un visage.
        """
        rgb_frame = frame[:, :, ::-1] # BGR to RGB
        
        if bbox:
            x, y, w, h = bbox
            # face_recognition utilise (top, right, bottom, left)
            face_locations = [(y, x + w, y + h, x)]
        else:
            face_locations = face_recognition.face_locations(rgb_frame)

        if not face_locations:
            return None

        encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        return encodings[0] if encodings else None
