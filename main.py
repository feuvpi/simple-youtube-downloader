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
        #tk.CTk.__init__(self)
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
        url_label.pack(pady=(10), padx=2)


        # create text field for input link
        self.link_field = tk.CTkEntry(master=self, width=400, placeholder_text="Enter video url:")
        self.link_field.pack(pady=2, padx=2)
        self.link_field.bind("<KeyRelease>", self.combobox_fill)
        widgets.append(self.link_field)

        # create label for file type
        self.type_label = tk.CTkLabel(master=self, width=400, text="Choose file type:", font=("Roboto", 14), anchor=tk.W)
        self.type_label.pack(pady=(10, 2), padx=2)
        widgets.append(self.type_label)


        # create combobox for type

        self.type_combobox = tk.CTkComboBox(master=self, width=400, values=["MP4", "MP3"])
        self.type_combobox.pack(pady=2, padx=2)
        widgets.append(self.type_combobox)

        # create label for quality
        self.quality_label = tk.CTkLabel(master=self, width=400, text="Select quality:", font=("Roboto", 14), anchor=tk.W)
        self.quality_label.pack(pady=(10,2), padx=10)
        widgets.append(self.quality_label)

        # create combobox for quality

        self.quality_combobox = tk.CTkComboBox(master=self, width=400, values=['Choose file type first'])
        self.quality_combobox.pack(pady=2, padx=2)
        widgets.append(self.quality_combobox)

        # adding download button
        button = tk.CTkButton(master=self, width=400, text="Download", command=self.download)
        button.pack(pady=(40,10), padx=10)
        widgets.append(button)

        # add a progress bar
        self.progress_bar = tkinter.ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')


    def combobox_fill(self, event):
        if len(event.widget.get()) > 32 and self.is_youtube_link(event.widget.get()):

            # for widget in widgets:
            #     widget.pack_forget()
            #
            # self.progress_bar.pack()
            try:
                url = self.link_field.get()
                self.yt = YouTube(url)
            except URLError as er:
                print("Erro ao real obter informações da url.", er)
            if self.type_combobox.get() == "MP3":
                try:
                    self.available_streams = self.yt.streams.filter(only_audio=True, file_extension='mp3')
                    # combo_values = [i.abr for i in self.available_streams.fmt_streams]
                except URLError as er:
                    print("Erro ao tentar obter streams mp4 disponveis.", er)
            else:
                try:
                    self.available_streams = self.yt.streams.filter(file_extension='mp4')
                except URLError as er:
                    print("Erro ao tentar obter streams mp4 disponveis.", er)
            #  comboValues = [i.abr for i in self.available_streams.fmt_streams]
            combo_values = [i.resolution for i in self.available_streams.fmt_streams]
            combo_values_filtered = list(set(i for i in combo_values if i is not None))
            teste = 1
            self.quality_combobox.configure(values=combo_values_filtered)


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
                self.yt = YouTube(url)
            quality = self.quality_combobox.get()
            if self.type_combobox.get() == "MP3":
                stream = self.yt.streams.filter(only_audio=True, file_extension='mp3', abr=quality).first()
            else:
                stream = self.yt.streams.filter(file_extension='mp4', resolution=quality).first()
            stream.download(self.parts[0], self.parts[1])
        except BaseException as er:
            print("Exception realizar download.", er)
        self.progress_bar.pack_forget()
        for widget in widgets:
            widget.pack()
        ttk.messagebox.showinfo("Download complete", "The video has been downloaded successfully!")






app = YoutubeDownloader()
#app.run()
app.mainloop()

#
# # set appeareance mode
# tk.set_appearance_mode("Dark")
# tk.set_default_color_theme("dark-blue")
#
# # create the main frame
# frame = customtkinter.CTkFrame(master=root)
#
#
# # build a simple login system
# root = tk.CTk()
# root.geometry("500x350")
# frame.pack(pady=20, padx=2, fill="both", expand=True)
# root.title("Simple YouTube Downloader")
#
# # adding label
# label = tk.CTkLabel(master=frame, text="Youtube Downloader", font=("Roboto", 24))
# label.pack(pady=12, padx=4)
#
# # adding text field for input link
# link_field = tk.CTkEntry(master=frame, width=400, placeholder_text="Enter video url:")
# link_field.pack(pady=2, padx=2)
#
# # adding dropdown to select the file type
# combobox_var = tk.StringVar(value="MP3")  # set initial value
# type_field = tk.CTkComboBox(master=frame, values=['MP4', 'MP3'], variable='combobox_var', width=400)
# type_field['values'] = ('MP4', 'MP3')
# type_field.configure(values=['MP4', 'MP3'], variable='combobox_var')
# type_field.pack(pady=12, padx=10)
#
# # adding download button
# button = tk.CTkButton(master=frame, width=400, text="Download", command=download)
# button.pack(pady=12, padx=10)
#
# # def download():
# #     link = link_field.get
# #     yt = YouTube(link)
# #     print("Title: ", yt.title)
# #     print("Views: ", yt.views)
# #     yd = yt.streams.get_audio_only()
# #     yt.check_availability()
#
#
#
#
#
#
#
#
# # adding text entries
#
#
# def combobox_callback(choice):
#     print("combobox dropdown clicked:", choice)
#
#
#
#
#
#
#
# checkbox = customtkinter.CTkCheckBox(master=frame, text="Highest Quality")
# checkbox.pack(pady=12, padx=10)
#
#
# # run the main loop
# root.mainloop
