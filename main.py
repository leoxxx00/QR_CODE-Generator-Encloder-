import cv2
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Encoder and Decoder")

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create QR Code Encoder frame
        self.encoder_frame = tk.Frame(root)
        self.encoder_frame.pack(pady=10)

        self.qr_data_label = tk.Label(self.encoder_frame, text="Enter data for QR Code:")
        self.qr_data_label.grid(row=0, column=0, padx=10, pady=10)

        self.qr_data_entry = tk.Entry(self.encoder_frame, width=30)
        self.qr_data_entry.grid(row=0, column=1, padx=10, pady=10)

        self.generate_button = tk.Button(self.encoder_frame, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.grid(row=0, column=2, padx=10, pady=10)

        # Create QR Code Decoder frame
        self.decoder_frame = tk.Frame(root)
        self.decoder_frame.pack(pady=10)

        self.webcam_label = tk.Label(self.decoder_frame, text="Webcam Feed")
        self.webcam_label.grid(row=0, column=0, padx=10, pady=10)

        self.webcam_canvas = tk.Canvas(self.decoder_frame, width=640, height=480)
        self.webcam_canvas.grid(row=1, column=0, padx=10, pady=10)

        self.decode_button = tk.Button(self.decoder_frame, text="Decode QR Code", command=self.decode_qr_code)
        self.decode_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_webcam()

    def generate_qr_code(self):
        data = self.qr_data_entry.get()
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            img.save("qrcode.png")
            messagebox.showinfo("QR Code Generated", "QR Code saved as 'qrcode.png'")
        else:
            messagebox.showwarning("Empty Data", "Please enter data for the QR Code.")

    def decode_qr_code(self):
        ret, frame = self.cap.read()

        if ret:
            detector = cv2.QRCodeDetector()
            retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

            if retval:
                messagebox.showinfo("QR Code Decoded", f"Decoded information: {decoded_info}")
            else:
                messagebox.showinfo("No QR Code Detected", "No QR Code detected in the frame.")

        self.update_webcam()

    def update_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.webcam_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.webcam_canvas.photo = photo
            self.root.after(10, self.update_webcam)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
