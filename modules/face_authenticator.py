import numpy as np
import face_recognition

class FaceAuthenticator:
    def __init__(self, db, threshold=0.6):
        self.db = db
        self.threshold = threshold

    def authenticate(self, current_embedding):
        """
        Compare l'embedding actuel avec la base de données.
        Retourne le nom de l'utilisateur si match, sinon None.
        """
        known_users = self.db.get_all_users()
        if not known_users:
            return None

        known_embeddings = [np.array(u['embedding']) for u in known_users]
        known_names = [u['username'] for u in known_users]

        # face_recognition.compare_faces utilise la distance euclidienne
        matches = face_recognition.compare_faces(known_embeddings, current_embedding, tolerance=self.threshold)
        
        if True in matches:
            # Trouver le meilleur match (distance minimale)
            distances = face_recognition.face_distance(known_embeddings, current_embedding)
            best_match_index = np.argmin(distances)
            if matches[best_match_index]:
                return known_names[best_match_index]
        
        return None
