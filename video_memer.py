import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import os
import random
from PIL import Image, ImageTk
import threading
import time

class VideoMemerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Memer - Black Frame Detector")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.video_path = tk.StringVar()
        self.meme_folder_path = tk.StringVar()
        self.image_duration = tk.DoubleVar(value=2.0)
        self.black_threshold = tk.DoubleVar(value=30.0)
        self.output_path = tk.StringVar()
        
        # Processing variables
        self.is_processing = False
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Memer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Video file selection
        ttk.Label(main_frame, text="Video File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.video_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_video).grid(row=1, column=2, pady=5)
        
        # Meme folder selection
        ttk.Label(main_frame, text="Meme Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.meme_folder_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_meme_folder).grid(row=2, column=2, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        settings_frame.columnconfigure(1, weight=1)
        
        # Image duration
        ttk.Label(settings_frame, text="Image Duration (seconds):").grid(row=0, column=0, sticky=tk.W, pady=5)
        duration_spinbox = ttk.Spinbox(settings_frame, from_=0.5, to=10.0, increment=0.5, textvariable=self.image_duration, width=10)
        duration_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Black threshold
        ttk.Label(settings_frame, text="Black Threshold (0-255):").grid(row=1, column=0, sticky=tk.W, pady=5)
        threshold_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, increment=1, textvariable=self.black_threshold, width=10)
        threshold_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output File:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_output).grid(row=4, column=2, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process video")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process Video", command=self.process_video, style="Accent.TButton")
        self.process_button.grid(row=7, column=0, columnspan=3, pady=20)
        
    def select_video(self):
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.video_path.set(filename)
            # Auto-set output path
            base_name = os.path.splitext(filename)[0]
            self.output_path.set(f"{base_name}_memified.mp4")
    
    def select_meme_folder(self):
        folder = filedialog.askdirectory(title="Select Meme Folder")
        if folder:
            self.meme_folder_path.set(folder)
    
    def select_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output Video",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def is_black_frame(self, frame, threshold):
        """Check if a frame is mostly black"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate mean brightness
        mean_brightness = np.mean(gray)
        return mean_brightness < threshold
    
    def get_meme_images(self, folder_path):
        """Get list of image files from folder"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
        images = []
        
        if not os.path.exists(folder_path):
            return images
            
        for filename in os.listdir(folder_path):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                images.append(os.path.join(folder_path, filename))
        
        return images
    
    def process_video(self):
        if self.is_processing:
            return
            
        # Validate inputs
        if not self.video_path.get():
            messagebox.showerror("Error", "Please select a video file")
            return
        if not self.meme_folder_path.get():
            messagebox.showerror("Error", "Please select a meme folder")
            return
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output file")
            return
            
        # Start processing in separate thread
        self.is_processing = True
        self.process_button.config(state="disabled")
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self._process_video_thread)
        thread.daemon = True
        thread.start()
    
    def _process_video_thread(self):
        try:
            self.status_label.config(text="Loading video...")
            self.progress_var.set(10)

            # Load video with OpenCV
            video_capture = cv2.VideoCapture(self.video_path.get())
            if not video_capture.isOpened():
                raise Exception("Could not open video file")

            # Get video properties
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps
            width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.status_label.config(text="Analyzing video for black frames...")
            self.progress_var.set(20)

            # Find black frame segments
            black_segments = []
            current_segment_start = None
            frame_count = 0

            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                frame_time = frame_count / fps

                if self.is_black_frame(frame, self.black_threshold.get()):
                    if current_segment_start is None:
                        current_segment_start = frame_time
                else:
                    if current_segment_start is not None:
                        black_segments.append((current_segment_start, frame_time))
                        current_segment_start = None

                frame_count += 1

                # Update progress
                if frame_count % 30 == 0:  # Update every 30 frames
                    progress = 20 + (frame_count / total_frames) * 30
                    self.progress_var.set(progress)

            # Handle case where video ends with black frames
            if current_segment_start is not None:
                black_segments.append((current_segment_start, duration))

            video_capture.release()

            self.status_label.config(text=f"Found {len(black_segments)} black segments. Processing...")
            self.progress_var.set(50)

            # Get meme images
            meme_images = self.get_meme_images(self.meme_folder_path.get())
            if not meme_images:
                raise Exception("No image files found in meme folder")

            # Load original video with moviepy
            original_clip = VideoFileClip(self.video_path.get())

            # Create clips list
            clips = []
            last_end = 0

            for start_time, end_time in black_segments:
                # Add non-black segment before this black segment
                if start_time > last_end:
                    non_black_clip = original_clip.subclip(last_end, start_time)
                    clips.append(non_black_clip)

                # Add meme image for black segment
                meme_path = random.choice(meme_images)
                meme_clip = ImageClip(meme_path, duration=self.image_duration.get())
                
                # Resize meme to fit video dimensions
                meme_clip = meme_clip.set_position(('center', 'center')).resize(width=width, height=height)
                clips.append(meme_clip)

                last_end = end_time

            # Add remaining non-black segment
            if last_end < original_clip.duration:
                final_segment = original_clip.subclip(last_end, original_clip.duration)
                clips.append(final_segment)

            self.status_label.config(text="Concatenating video...")
            self.progress_var.set(80)

            # Concatenate all clips
            final_video = concatenate_videoclips(clips, method="compose")

            self.status_label.config(text="Writing output file...")
            self.progress_var.set(90)

            # Write output
            final_video.write_videofile(
                self.output_path.get(),
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a', 
                remove_temp=True
            )

            # Clean up clips
            for clip in clips:
                clip.close()
            final_video.close()
            original_clip.close()

            self.progress_var.set(100)
            self.status_label.config(text="Processing complete!")
            
            messagebox.showinfo("Success", f"Video processed successfully!\nOutput saved to: {self.output_path.get()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Processing failed")
        finally:
            self.is_processing = False
            self.process_button.config(state="normal")

def main():
    root = tk.Tk()
    app = VideoMemerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 