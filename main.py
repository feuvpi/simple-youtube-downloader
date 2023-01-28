import threading
import time
import tkinter as ttk
import tkinter.ttk
import customtkinter as tk
from tkinter import filedialog
import pytube
import re
from pytube import YouTube
from sys import argv
from urllib.error import URLError

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

app = tk.CTk()
app.geometry("500x350")
app.title("Simple YouTube Downloader")

widgets = []


# adicionar tratamento de erros
# adicionar progress bar
# adicionar dialog para escolhar de local de salvamento
# adicionar novas telas para cada etapa


class YoutubeDownloader(tk.CTk):
    # declare global variables
    yt = ''
    save_path = ''

    def __init__(self):
        super().__init__()
        self.progress_bar = tkinter.ttk.Progressbar(self, orient='horizontal', length=400, mode='indeterminate')
        self.quality_label = None
        self.type_combobox = None
        self.link_field = None
        self.type_label = None
        self.quality_combobox = None
        self.parts = None
        self.available_streams = None
        self.geometry("1000x350")
        self.title("Simple YouTube Downloader")
        self.configure(pady=2, padx=2)
        self.configure(expand=True, fill="x")
        self.create_widgets()

    def is_youtube_link(self, link):
        youtube_link_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/watch\?v=[a-zA-Z0-9_\-]+'
        match = re.search(youtube_link_regex, link)
        return bool(match)

    def create_widgets(self):

        # create label for the url
        url_label = tk.CTkLabel(master=self, pady=10, padx=2, text="Youtube Downloader", font=("Roboto", 24))
        url_label.pack(pady=10, padx=2)

        # create text field for input link
        self.link_field = tk.CTkEntry(master=self, width=400, placeholder_text="Enter video url:")
        self.link_field.pack(pady=2, padx=2)
        self.link_field.bind("<FocusOut>", self.combobox_fill)
        widgets.append(self.link_field)

        # create label for file type
        self.type_label = tk.CTkLabel(master=self, width=400, text="Choose file type:", font=("Roboto", 14),
                                      anchor=tk.W)
        self.type_label.pack(pady=(10, 2), padx=2)
        widgets.append(self.type_label)

        # create combobox for type

        self.type_combobox = tk.CTkComboBox(master=self, width=400, values=["MP4", "MP3"])
        self.type_combobox.pack(pady=2, padx=2)
        widgets.append(self.type_combobox)

        # create label for quality
        self.quality_label = tk.CTkLabel(master=self, width=400, text="Select quality:", font=("Roboto", 14),
                                         anchor=tk.W)
        # self.quality_label.pack(pady=(10, 2), padx=10)
        widgets.append(self.quality_label)

        # create combobox for quality

        self.quality_combobox = tk.CTkComboBox(master=self, width=400, values=['Choose file type first'])
        # self.quality_combobox.pack(pady=2, padx=2)
        widgets.append(self.quality_combobox)

        # adding download button
        self.button = tk.CTkButton(master=self, width=400, text="Download", command=self.download)
        # self.button.pack(pady=(40, 10), padx=10)
        widgets.append(self.button)

        # add a progress bar
        self.progress_bar = tkinter.ttk.Progressbar(self, orient='horizontal', length=400, mode='indeterminate')

    def combobox_fill(self, event):
        if len(event.widget.get()) > 32 and self.is_youtube_link(event.widget.get()):

            # set-up indeterminate progress bar
            for widget in widgets:
                widget.pack_forget()
            self.progress_bar.pack()
            self.progress_bar.start()
            self.progress_bar.place(relx=0.5, rely=0.5, anchor='center')
            threading.Thread(target=self.get_data).start()


    def get_data(self):
        # request available streams based on type choosed
        try:
            url = self.link_field.get()
            self.yt = YouTube(url)
            if self.type_combobox.get() == "MP3":
                self.available_streams = self.yt.streams.filter(only_audio=True, file_extension='mp3')
            else:
                self.available_streams = self.yt.streams.filter(file_extension='mp4')
        except URLError as er:
            print("Erro ao tentar obter streams mp4 disponveis.", er)

        # filter response and load combobox
        combo_values = [i.resolution for i in self.available_streams.fmt_streams]
        combo_values_filtered = list(set(i for i in combo_values if i is not None))
        self.quality_combobox.configure(values=combo_values_filtered)

        # destroy and replace progress bar
        self.progress_bar.place_forget()
        self.progress_bar.pack_forget()

        self.progress_bar.stop()

        for widget in widgets:
            if widget == self.button:
                widget.pack(pady=(40, 10), padx=10)
            if widget == self.quality_combobox or self.quality_label:
                widget.pack(pady=2, padx=2)


    def progress_function(self, stream, chunk, file_handle, bytes_remaining):
        self.progress_bar['value'] = self.stream.filesize - bytes_remaining
        self.progress_bar.update()


    def download(self):
        for widget in widgets:
            widget.pack_forget()
        self.progress_bar.pack()
        # select save path
        if self.type_combobox.get() == "MP3":
            try:
                self.save_path = filedialog.asksaveasfilename(defaultextension="mp3")
            except BaseException as ex:
                print("Exception ao selecionar savepath mp3.", er)
        else:
            try:
                self.save_path = filedialog.asksaveasfilename(defaultextension="mp4")
            except BaseException as er:
                print("Exception ao selecionar savepath mp4.", er)
        self.parts = self.save_path.rsplit('/', 1)
        # proceed to download file
        try:
            if self.yt == '':
                url = self.link_field.get()
                self.yt = YouTube(url, on_progress_callback=self.progress_function)
            quality = self.quality_combobox.get()
            if self.type_combobox.get() == "MP3":
                self.stream = self.yt.streams.filter(only_audio=True, file_extension='mp3', abr=quality).first()
            else:
                self.stream = self.yt.streams.filter(file_extension='mp4', resolution=quality).first()
            self.progress_bar['maximum'] = stream.filesize

            self.stream = self.yt.streams.get_by_resolution(quality)
            self.stream.download(self.parts[0], self.parts[1])
        except BaseException as er:
            print("Exception realizar download.", er)
        self.progress_bar.pack_forget()
        for widget in widgets:
            if widget == self.button:
                widget.pack(pady=(40, 10), padx=10)
            else:
                widget.pack(pady=2, padx=2)
        ttk.messagebox.showinfo("Download complete", "The video has been downloaded successfully!")


app = YoutubeDownloader()
app.mainloop()
