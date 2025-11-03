import tkinter as tk
import customtkinter as cs
from tkcalendar import Calendar 
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import os
from datetime import datetime

# Functions
def get_filtered_images():
    """Returns a list of filtered image paths based on the selected date and time range."""
    from_datetime = f"{from_calendar.get_date()} {from_hour_spinbox.get()}:{from_minute_spinbox.get()} {from_ampm_combobox.get()}"
    to_datetime = f"{to_calendar.get_date()} {to_hour_spinbox.get()}:{to_minute_spinbox.get()} {to_ampm_combobox.get()}"
    
    from_dt = datetime.strptime(from_datetime, "%Y-%m-%d %I:%M %p")
    to_dt = datetime.strptime(to_datetime, "%Y-%m-%d %I:%M %p")
    
    folder_path = os.path.join(os.path.dirname(__file__), "footages/")
    
    image_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".png"):
            file_path = os.path.join(folder_path, file)
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if from_dt <= creation_time <= to_dt:
                image_files.append(file_path)
    
    return sorted(image_files)  # Sort by creation time


def play_slideshow():
    """Plays a slideshow of filtered images in a separate window."""
    image_files = get_filtered_images()
    if not image_files:
        print("No images found for the selected range.")
        return

    slideshow_window = tk.Toplevel(app)
    slideshow_window.title("Dashcam Footage")
    slideshow_window.geometry("900x600")

    slideshow_label = tk.Label(slideshow_window)
    slideshow_label.pack(expand=True, fill="both", padx=10, pady=10)

    def show_next_image(idx):
        if idx < len(image_files):
            img = Image.open(image_files[idx]).resize((800, 450))
            photo = ImageTk.PhotoImage(img)
            slideshow_label.configure(image=photo)
            slideshow_label.image = photo
            slideshow_window.after(33, show_next_image, idx + 1)  # 30 FPS
        else:
            slideshow_window.destroy()

    show_next_image(0)


def convert_to_video():
    """Converts filtered images into a video and saves it to the desired location."""
    image_files = get_filtered_images()
    if not image_files:
        print("No images found for video conversion.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not save_path:
        return
    
    frame = cv2.imread(image_files[0])
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(save_path, fourcc, 30, (width, height))
    
    for img_path in image_files:
        frame = cv2.imread(img_path)
        video.write(frame)
    
    video.release()
    print(f"Video saved at: {save_path}")


# System settings
cs.set_appearance_mode("dark")
cs.set_default_color_theme("blue")

# App frame
app = cs.CTk()
app.geometry("900x600")
app.title("Dashcam APP")

# UI elements
nav = cs.CTkFrame(app, fg_color="#414A4C")
nav.pack(fill="x", pady=0, padx=0)

cs.CTkLabel(nav, text="Enter the timeframe of the dashcam footage required", font=("Arial", 25, "bold")).pack(pady=30)

mains = cs.CTkFrame(app, fg_color="grey")
mains.pack(fill="both", expand=True)

from_frame = cs.CTkFrame(mains, corner_radius=20)
from_frame.pack(side="left", padx=40, pady=30, anchor="n", fill="both", expand=True)

cs.CTkLabel(from_frame, text="FROM\n\nSelect Date:", font=("Arial", 14, "bold"), text_color="white").pack(anchor="center", padx=10, pady=5)
from_calendar = Calendar(from_frame, selectmode="day", date_pattern="yyyy-mm-dd")
from_calendar.pack(anchor="w", padx=10, pady=10, fill="both", expand=True)

cs.CTkLabel(from_frame, text="Select Time:", font=("Arial", 14, "bold"), text_color="white").pack(anchor="w", padx=10, pady=5, fill="both", expand=True)
from_time_frame = tk.Frame(from_frame)
from_time_frame.pack(anchor="center", padx=10, pady=10)
from_hour_spinbox = ttk.Spinbox(from_time_frame, from_=1, to=12, width=3)
from_hour_spinbox.pack(side="left", padx=5)
from_minute_spinbox = ttk.Spinbox(from_time_frame, from_=0, to=59, width=3, format="%02.0f")
from_minute_spinbox.pack(side="left", padx=5)
from_ampm_combobox = ttk.Combobox(from_time_frame, values=["AM", "PM"], width=5, state="readonly")
from_ampm_combobox.set("AM")
from_ampm_combobox.pack(side="left", padx=5)

to_frame = cs.CTkFrame(mains, corner_radius=20)
to_frame.pack(side="right", padx=40, pady=30, anchor="n", fill="both", expand=True)

cs.CTkLabel(to_frame, text="TO\n\nSelect Date:", font=("Arial", 14, "bold"), text_color="white").pack(anchor="center", padx=10, pady=5)
to_calendar = Calendar(to_frame, selectmode="day", date_pattern="yyyy-mm-dd")
to_calendar.pack(anchor="w", padx=10, pady=10, fill="both", expand=True)

cs.CTkLabel(to_frame, text="Select Time:", font=("Arial", 14, "bold"), text_color="white").pack(anchor="w", padx=10, pady=5, fill="both", expand=True)
to_time_frame = tk.Frame(to_frame)
to_time_frame.pack(anchor="center", padx=10, pady=5)
to_hour_spinbox = ttk.Spinbox(to_time_frame, from_=1, to=12, width=3)
to_hour_spinbox.pack(side="left", padx=5)
to_minute_spinbox = ttk.Spinbox(to_time_frame, from_=0, to=59, width=3, format="%02.0f")
to_minute_spinbox.pack(side="left", padx=5)
to_ampm_combobox = ttk.Combobox(to_time_frame, values=["AM", "PM"], width=5, state="readonly")
to_ampm_combobox.set("AM")
to_ampm_combobox.pack(side="left", padx=5)

cs.CTkButton(mains, text="Submit", command=play_slideshow, height=50, font=("Arial", 20)).pack(expand=True, anchor="center")
cs.CTkButton(mains, text="Convert to Video", command=convert_to_video, height=50, font=("Arial", 20)).pack(expand=True, anchor="center")

app.mainloop()
