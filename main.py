import tkinter as tk
from transcription import AudioRecorder


def main():
    main_window = tk.Tk()
    app = AudioRecorder(main_window)
    main_window.mainloop()

if __name__ == "__main__":
    main()