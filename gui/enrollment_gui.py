import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import threading
import time

class EnrollmentGUI:
    def __init__(self, camera, detector, encoder, db):
        self.camera = camera
        self.detector = detector
        self.encoder = encoder
        self.db = db
        
        self.root = tk.Tk()
        self.root.title("FaceLock - Enrôlement")
        self.root.geometry("800x600")

        self.label_video = tk.Label(self.root)
        self.label_video.pack(pady=10)

        self.btn_enroll = tk.Button(self.root, text="Enrôler un nouvel utilisateur", command=self.enroll_user, height=2, width=30)
        self.btn_enroll.pack(pady=10)

        self.btn_quit = tk.Button(self.root, text="Quitter", command=self.on_closing)
        self.btn_quit.pack(pady=10)

        self.running = True
        self.thread = threading.Thread(target=self.video_loop)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def video_loop(self):
        if not self.camera.start():
            messagebox.showerror("Erreur", "Impossible d'accéder à la caméra")
            return

        while self.running:
            frame = self.camera.get_frame()
            if frame is not None:
                # Détection pour le feedback visuel
                faces = self.detector.detect_faces(frame)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Conversion pour Tkinter
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label_video.imgtk = imgtk
                self.label_video.configure(image=imgtk)
            
            time.sleep(0.03)

    def enroll_user(self):
        username = simpledialog.askstring("Nom d'utilisateur", "Entrez le nom de l'utilisateur :")
        if not username:
            return

        messagebox.showinfo("Capture", "Regardez la caméra. Capture de l'embedding dans 3 secondes...")
        time.sleep(3)
        
        frame = self.camera.get_frame()
        if frame is not None:
            embedding = self.encoder.get_embedding(frame)
            if embedding is not None:
                if self.db.add_user(username, embedding):
                    messagebox.showinfo("Succès", f"Utilisateur {username} enrôlé avec succès (Image supprimée, embedding stocké).")
                else:
                    messagebox.showerror("Erreur", "Cet utilisateur existe déjà.")
            else:
                messagebox.showerror("Erreur", "Aucun visage détecté. Réessayez.")

    def on_closing(self):
        self.running = False
        self.camera.stop()
        self.root.destroy()
