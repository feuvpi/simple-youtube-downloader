import customtkinter as tk
from pytube import YouTube
from sys import argv


# set appeareance mode
tk.set_appearance_mode("Dark")
tk.set_default_color_theme("dark-blue")

# create the main frame
frame = customtkinter.CTkFrame(master=root)


# build a simple login system
root = tk.CTk()
root.geometry("500x350")
frame.pack(pady=20, padx=2, fill="both", expand=True)
root.title("Simple YouTube Downloader")

# adding label
label = tk.CTkLabel(master=frame, text="Youtube Downloader", font=("Roboto", 24))
label.pack(pady=12, padx=4)

# adding text field for input link
link_field = tk.CTkEntry(master=frame, width=400, placeholder_text="Enter video url:")
link_field.pack(pady=2, padx=2)

# adding dropdown to select the file type
combobox_var = tk.StringVar(value="MP3")  # set initial value
type_field = tk.CTkComboBox(master=frame, values=['MP4', 'MP3'], variable='combobox_var', width=400)
type_field['values'] = ('MP4', 'MP3')
type_field.configure(values=['MP4', 'MP3'], variable='combobox_var')
type_field.pack(pady=12, padx=10)

# adding download button
button = tk.CTkButton(master=frame, width=400, text="Download", command=download)
button.pack(pady=12, padx=10)

def download():
    link = link_field.get
    yt = YouTube(link)
    print("Title: ", yt.title)
    print("Views: ", yt.views)
    yd = yt.streams.get_audio_only()
    yt.check_availability()








# adding text entries


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)







checkbox = customtkinter.CTkCheckBox(master=frame, text="Highest Quality")
checkbox.pack(pady=12, padx=10)


# run the main loop
root.mainloop
