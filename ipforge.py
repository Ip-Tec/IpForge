import customtkinter as ctk
from ui.main_window import MainWindow

class IpForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IpForge")
        self.geometry("800x600")

        self.main_window = MainWindow(self)
        self.main_window.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = IpForgeApp()
    app.mainloop()
