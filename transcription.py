import tkinter as tk
from tkinter import messagebox


class AudioRecorder:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title("Audio Recorder")
        self.root.geometry("320x400")

        self.is_recording = False
        self.recording_thread = None
        
        #Build the UI 
        self.create_widgets()

    ''' Initializes all GUI elements and their properties. '''
    def create_widgets(self):

        self.record_button = tk.Button(
            self.root,
            text="Record",
            bg="green",
            fg="white",
            font=("Arial", 16),
            width=10,
            command=self.on_click_record
        )
        self.record_button.pack(pady=3)

        self.stop_button = tk.Button(
            self.root,
            text="Stop",
            bg="red",
            fg="white",
            font=("Arial", 16),
            width=10,
            command=self.on_click_stop
        )
        self.stop_button.pack(pady=3)

        self.output_box = tk.Text(
            self.root,
            height=20,
            width=40,
            font=("Arial", 12)
        )
        self.output_box.pack(pady=10)

    ''' Deals with the record button being clicked'''
    def on_click_record(self):
        print("Recording started...")
        self.display_output()

    ''' Deals with the stop button being clicked'''
    def on_click_stop(self):
        print("Recording stopped.")
        self.clear_output()


    def display_output(self):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, "Transcription output will be displayed here.")
        self.output_box.config(state=tk.DISABLED)

    def clear_output(self):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete(1.0, tk.END)
        self.output_box.config(state=tk.DISABLED)

