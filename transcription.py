import tkinter as tk
from tkinter import messagebox
from threading import Event, Thread
from queue import Queue
import sounddevice as sd
import numpy as np


class AudioRecorder:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title("Audio Recorder")
        self.root.geometry("320x400")

        self.is_recording = Event()
        self.recording_thread = None

        self.messages = Queue()
        self.recordings = Queue()
        
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

        if self.is_recording.is_set():
            messagebox.showinfo("Info", "Recording is already in progress.")
            return

        print("Recording started...")

        #Clears old messages from the output box
        self.clear_output()
        self.is_recording.set()

        #Tell thread to keep recording
        self.messages.put(True)

        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(tk.END, "Starting Recording...\n")
        self.output_box.config(state=tk.DISABLED)

        #Thread runs in background recording audio
        record = Thread(target = self.record_microphone, daemon=True)
        record.start()

        #Thread runs in background transcribing audio
        #transcribe = Thread(target = self.speech_recognition, args = (self.output_box,))
        #transcribe.start()

    ''' Deals with the stop button being clicked'''
    def on_click_stop(self):

        if not self.is_recording.is_set():
            messagebox.showinfo("Info", "No recording is in progress.")
            return
        
        print("Recording stopped.")
        self.is_recording.clear()

        if not self.messages.empty():
            self.messages.get()

        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(tk.END, "Stopped Recording.\n")
        self.output_box.config(state=tk.DISABLED)
    
    def record_microphone(self):
        sample_rate = 16000
        channels = 1

        def audio_callback(indata, frames, time, status):

            #Saves small fragments of audio to a queue for processing
            if status:
                print(status)
            self.recordings.put(indata.copy())

            with sd.InputStream(
                samplerate=sample_rate, 
                channels=channels, 
                dtype = 'float32',
                callback=audio_callback
            ):
                while self.is_recording.is_set():
                    sd.sleep(100)


    def clear_output(self):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete(1.0, tk.END)
        self.output_box.config(state=tk.DISABLED)

