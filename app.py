import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
import json
import os

class PS3WaveStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PS3 Custom Wave Studio & PKG Prep")
        self.geometry("600+550")
        self.config(bg="#1e1e1e")

        # Domyślne wartości z JSON-a użytkownika
        self.wave_data = {
            "title": "Custom Wave - Blue Midnight",
            "state": {
                "color1": "#0070d1",
                "alpha1": 0.75,
                "color2": "#00d4ff",
                "alpha2": 0.5,
                "bgTop": "#4c00ff",
                "bgBottom": "#ff0008",
                "speed": 0.4,
                "amplitude": 100,
                "layers": 5,
                "glow": 50,
                "showIcons": True,
                "time": 18.5
            }
        }

        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        title_label = tk.Label(self, text="PS3 XMB Wave Studio (Windows 7)", font=("Arial", 14, "bold"), fg="#ffffff", bg="#1e1e1e")
        title_label.pack(pady=10)

        # Rama sterowania
        control_frame = tk.Frame(self, bg="#2d2d2d", padx=10, pady=10)
        control_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Kolor 1
        self.btn_c1 = tk.Button(control_frame, text="Kolor Fali 1", bg=self.wave_data["state"]["color1"], fg="white", command=lambda: self.pick_color("color1"))
        self.btn_c1.pack(fill="x", pady=5)

        # Kolor 2
        self.btn_c2 = tk.Button(control_frame, text="Kolor Fali 2", bg=self.wave_data["state"]["color2"], fg="white", command=lambda: self.pick_color("color2"))
        self.btn_c2.pack(fill="x", pady=5)

        # Prędkość
        tk.Label(control_frame, text="Prędkość animacji:", fg="white", bg="#2d2d2d").pack(anchor="w")
        self.scale_speed = tk.Scale(control_frame, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", bg="#2d2d2d", fg="white", highlightbackground="#2d2d2d")
        self.scale_speed.set(self.wave_data["state"]["speed"])
        self.scale_speed.pack(fill="x", pady=5)

        # Amplituda
        tk.Label(control_frame, text="Amplituda:", fg="white", bg="#2d2d2d").pack(anchor="w")
        self.scale_amp = tk.Scale(control_frame, from_=10, to=200, resolution=5, orient="horizontal", bg="#2d2d2d", fg="white", highlightbackground="#2d2d2d")
        self.scale_amp.set(self.wave_data["state"]["amplitude"])
        self.scale_amp.pack(fill="x", pady=5)

        # Przyciski akcji
        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(fill="x", padx=15, pady=15)

        save_btn = tk.Button(btn_frame, text="Eksportuj JSON / QRC", bg="#0070d1", fg="white", font=("Arial", 10, "bold"), command=self.export_files)
        save_btn.pack(side="left", expand=True, fill="x", padx=5)

        exit_btn = tk.Button(btn_frame, text="Zamknij", bg="#d9534f", fg="white", font=("Arial", 10, "bold"), command=self.destroy)
        exit_btn.pack(side="right", expand=True, fill="x", padx=5)

    def pick_color(self, color_key):
        color_code = colorchooser.askcolor(title=f"Wybierz {color_key}")[1]
        if color_code:
            self.wave_data["state"][color_key] = color_code
            if color_key == "color1":
                self.btn_c1.config(bg=color_code)
            elif color_key == "color2":
                self.btn_c2.config(bg=color_code)

    def export_files(self):
        # Pobranie aktualnych wartości z suwaków
        self.wave_data["state"]["speed"] = self.scale_speed.get()
        self.wave_data["state"]["amplitude"] = self.scale_amp.get()

        # Wybór folderu zapisu
        folder_selected = filedialog.askdirectory(title="Wybierz folder do zapisu projektu fali")
        if folder_selected:
            # Zapisz JSON
            json_path = os.path.join(folder_selected, "wave_config.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.wave_data, f, indent=2)

            # Zapisz uproszczony lines.qrc
            qrc_path = os.path.join(folder_selected, "lines.qrc")
            qrc_content = f"""<RCC>
  <qresource prefix="/lines">
    <!-- Wygenerowano przez PS3 Custom Wave Studio -->
    <file>wave_config.json</file>
  </qresource>
</RCC>"""
            with open(qrc_path, "w", encoding="utf-8") as f:
                f.write(qrc_content)

            messagebox.showinfo("Sukces", f"Pomyślnie wyeksportowano pliki do:\n{folder_selected}")

if __name__ == "__main__":
    app = PS3WaveStudio()
    app.mainloop()
