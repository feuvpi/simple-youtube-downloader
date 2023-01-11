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
root.title("Simple YouTube Downloader")

def login():
    link = entry1.get
    yt = YouTube(link)
    print("Title: ", yt.title)
    print("Views: ", yt.views)
    yd = yt.streams.get_audio_only()
    yt.check_availability()





# adjusting frame settings
frame.pack(pady=20, padx=2, fill="both", expand=True)

# adding elements into frame
label = customtkinter.CTkLabel(master=frame, text="Youtube Downloader", font=("Roboto", 24))
label.pack(pady=12, padx=4)

# adding text entries
entry1 = customtkinter.CTkEntry(master=frame, width=400, placeholder_text="Enter video url:")
entry1.pack(pady=2, padx=2)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox_var = customtkinter.StringVar(value="MP3")  # set initial value
combobox = customtkinter.CTkComboBox(master=frame,
                                     values=['MP4', 'MP3'],
                                     variable='combobox_var',
                                    width=400,
                                     )
combobox['values'] = ('MP4', 'MP3')
combobox.configure(values=['MP4', 'MP3'], variable='combobox_var')
combobox.pack(pady=12, padx=10)



button = customtkinter.CTkButton(master=frame, width=400, text="Download", command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Highest Quality")
checkbox.pack(pady=12, padx=10)



root.mainloop(



)
