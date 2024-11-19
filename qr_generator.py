import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Kod Oluşturucu")
        self.root.geometry("400x600")
        self.root.resizable(False, False)  # Pencere boyutunu sabitle
        self.root.configure(bg='#f0f0f0')

        # Ana canvas ve scrollbar
        self.canvas = tk.Canvas(root, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=380)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")

        # Başlık
        title_label = tk.Label(self.scrollable_frame, text="QR Kod Oluşturucu", 
                             font=("Helvetica", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Giriş alanı
        self.input_label = tk.Label(self.scrollable_frame, text="Metin veya URL giriniz:", 
                                  bg='#f0f0f0', font=("Helvetica", 10))
        self.input_label.pack(pady=5)

        self.input_text = tk.Text(self.scrollable_frame, height=3, width=40)
        self.input_text.pack(pady=5)

        # Oluştur butonu
        self.generate_button = tk.Button(self.scrollable_frame, text="QR Kod Oluştur", 
                                       command=self.generate_qr,
                                       bg='#4CAF50', fg='white',
                                       font=("Helvetica", 10, "bold"))
        self.generate_button.pack(pady=10)

        # QR kod gösterim alanı
        self.qr_frame = tk.Frame(self.scrollable_frame, bg='white')
        self.qr_frame.pack(pady=10)
        self.qr_label = tk.Label(self.qr_frame, bg='white')
        self.qr_label.pack(padx=10, pady=10)

        # Kaydet butonu
        self.save_button = tk.Button(self.scrollable_frame, text="QR Kodu Kaydet",
                                   command=self.save_qr,
                                   bg='#2196F3', fg='white',
                                   font=("Helvetica", 10, "bold"))
        self.save_button.pack(pady=20)
        self.save_button.config(state='disabled')

        self.qr_image = None

        # Mouse wheel binding
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def generate_qr(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showerror("Hata", "Lütfen bir metin veya URL girin!")
            return

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)

        self.qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # QR kodu gösterme
        photo_image = ImageTk.PhotoImage(self.qr_image)
        self.qr_label.config(image=photo_image)
        self.qr_label.image = photo_image
        
        self.save_button.config(state='normal')
        
        # Scroll to show save button
        self.canvas.yview_moveto(1.0)

    def save_qr(self):
        if self.qr_image:
            if not os.path.exists('qr_codes'):
                os.makedirs('qr_codes')
            
            text = self.input_text.get("1.0", "end-1c").strip()
            filename = f"qr_codes/qr_{text[:10]}.png"
            
            self.qr_image.save(filename)
            messagebox.showinfo("Başarılı", f"QR kod kaydedildi: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
