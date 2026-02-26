import time
import cv2
import argparse
from modules.camera_handler import CameraHandler
from modules.face_detector import FaceDetector
from modules.face_encoder import FaceEncoder
from modules.face_authenticator import FaceAuthenticator
from modules.system_controller import SystemController
from modules.database import FaceDatabase
from gui.enrollment_gui import EnrollmentGUI

def main():
    parser = argparse.ArgumentParser(description="FaceLock - Authentification Faciale pour Windows")
    parser.add_argument("--enroll", action="store_true", help="Lancer l'interface d'enrôlement")
    args = parser.parse_args()

    # Initialisation des composants
    db = FaceDatabase()
    camera = CameraHandler()
    detector = FaceDetector()
    encoder = FaceEncoder()
    authenticator = FaceAuthenticator(db)
    system = SystemController()

    if args.enroll:
        EnrollmentGUI(camera, detector, encoder, db)
        return

    print("FaceLock est actif. Appuyez sur Ctrl+C pour arrêter.")
    
    if not camera.start():
        print("Erreur: Impossible d'ouvrir la caméra.")
        return

    last_seen_time = time.time()
    LOCK_TIMEOUT = 10  # Secondes d'absence avant verrouillage
    
    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            faces = detector.detect_faces(frame)
            
            if faces:
                # Un visage est présent, on vérifie l'identité
                embedding = encoder.get_embedding(frame, faces[0])
                if embedding is not None:
                    user = authenticator.authenticate(embedding)
                    if user:
                        # print(f"Utilisateur reconnu : {user}")
                        last_seen_time = time.time()
                        system.prevent_sleep()
                    else:
                        print("Visage non reconnu.")
            
            # Vérification du timeout
            if time.time() - last_seen_time > LOCK_TIMEOUT:
                print("Absence détectée. Verrouillage...")
                system.lock_session()
                # On réinitialise le timer pour éviter de verrouiller en boucle
                last_seen_time = time.time()

            # Petite pause pour ne pas saturer le CPU
            time.sleep(1)

    except KeyboardInterrupt:
        print("Arrêt de FaceLock...")
    finally:
        camera.stop()

if __name__ == "__main__":
    main()
