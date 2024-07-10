import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class InvisibilityCloakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invisibility Cloak App")

        self.video_frame = tk.Label(root)
        self.video_frame.pack(padx=10, pady=10)

        self.capture_button = tk.Button(root, text="Start Capture", command=self.start_capture)
        self.capture_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=5)

        self.capture = None
        self.mask = None
        self.background = None

    def start_capture(self):
        self.capture = cv2.VideoCapture(0)  # Use default camera (usually webcam)

        if not self.capture.isOpened():
            print("Error: Unable to open camera.")
            return

        self.root.after(10, self.update_frame)

    def update_frame(self):
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.flip(frame, 1)  # Flip horizontally for mirror view

            # Convert frame to RGB format for displaying in Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)

            # Apply invisibility cloak effect
            self.apply_invisibility_cloak(frame)

        self.root.after(10, self.update_frame)

    def apply_invisibility_cloak(self, frame):
        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range of red color in HSV
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        # Create a mask of red color
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Apply a morphological transformation to remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

        # Create an inverted mask to segment out the red color
        mask_inv = cv2.bitwise_not(mask)

        # Save the background image
        if self.background is None:
            self.background = frame.copy()

        # Use the background image to replace the cloak region
        frame_without_cloak = cv2.bitwise_and(self.background, self.background, mask=mask)
        frame_cloak = cv2.bitwise_and(frame, frame, mask=mask_inv)
        result_frame = cv2.add(frame_without_cloak, frame_cloak)

        # Convert back to RGB for displaying in Tkinter
        result_frame_rgb = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(result_frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvisibilityCloakApp(root)
    root.mainloop()
