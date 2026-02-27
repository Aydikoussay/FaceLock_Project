import cv2
import face_recognition

class FaceDetector:
    def __init__(self):
        pass  # No initialization needed for face_recognition

    def detect_faces(self, frame):
        """Détecte les visages et retourne les boîtes englobantes."""
        # Convertir BGR à RGB pour face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        faces = []
        for top, right, bottom, left in face_locations:
            x, y, w, h = left, top, right - left, bottom - top
            faces.append((x, y, w, h))
        return faces

    def crop_face(self, frame, bbox):
        x, y, w, h = bbox
        # Assurer que les coordonnées sont dans l'image
        x, y = max(0, x), max(0, y)
        return frame[y:y+h, x:x+w]
