import json
from tkinter import filedialog
import yt_dlp
from yt_dlp.utils import download_range_func
import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Creation de la fenetre de l'app
        self.pourcent = None
        self.progress_bar = None
        self.path = customtkinter.StringVar()
        self.yt_link = customtkinter.StringVar()
        self.geometry("800x400")
        self.maxsize(800, 400)
        self.title("Pydoyt")
        self.iconbitmap("Pydoyt.ico")
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("nighty")

        # Configuration du grid
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Creation de la frame pour le lien Youtube avec label et input
        self.yt_link_frame1 = customtkinter.CTkFrame(self)
        self.yt_link_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.yt_link_frame1.grid_columnconfigure(0, weight=1)
        self.yt_link_frame1.grid_rowconfigure(0, weight=1)
        self.yt_link_frame2 = customtkinter.CTkFrame(self.yt_link_frame1)
        self.yt_link_frame2.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.yt_link_frame2.grid_columnconfigure(0, weight=1)
        self.label_link = customtkinter.CTkLabel(self.yt_link_frame2, text="Lien Youtube : ")
        self.label_link.grid(row=0, column=0, padx=10, pady=10)
        self.input_link = customtkinter.CTkEntry(self.yt_link_frame2, textvariable=self.yt_link)
        self.input_link.grid(row=1, column=0, padx=10, pady=10)

        # Creation de la frame pour le chemin d'installation
        self.path_frame1 = customtkinter.CTkFrame(self)
        self.path_frame1.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.path_frame1.grid_columnconfigure(0, weight=1)
        self.path_frame1.grid_rowconfigure(0, weight=1)
        self.path_frame2 = customtkinter.CTkFrame(self.path_frame1)
        self.path_frame2.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.path_frame2.grid_columnconfigure(0, weight=1)

        self.label_path = customtkinter.CTkLabel(self.path_frame2, text="Chemin d'installation : ")
        self.label_path.grid(column=0, padx=10, pady=10)

        self.browse_path = customtkinter.CTkButton(self.path_frame2, text="Browse", command=lambda: self.browsepath())
        self.browse_path.grid(row=2, column=0, padx=10, pady=10)

        # Creation de la frame pour l'option de format
        self.format_frame1 = customtkinter.CTkFrame(self)
        self.format_frame1.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nsew")
        self.format_frame1.grid_columnconfigure(0, weight=1)
        self.format_frame1.rowconfigure(0, weight=1)
        self.format_frame2 = customtkinter.CTkFrame(self.format_frame1)
        self.format_frame2.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.format_frame2.grid_columnconfigure(0, weight=1)
        self.label_format = customtkinter.CTkLabel(self.format_frame2, text="Format : ")
        self.label_format.grid(column=0, padx=10, pady=10)
        self.format_option = customtkinter.CTkOptionMenu(
            self.format_frame2, values=[
                "mp3",
                "opus",
                "flac",
                "vorbis",
            ])
        self.format_option.set("opus")
        self.format_option.grid(row=1, column=0, padx=10, pady=10)

        # # Barre de progression
        # self.pourcent = customtkinter.CTkLabel(self, text='0%')
        # self.pourcent.grid(row=2, column=2, padx=20, pady=10, sticky="ew")
        # self.progress_bar = customtkinter.CTkProgressBar(self)
        # self.progress_bar.set(0)
        # self.progress_bar.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky="ew")

        # Bouton pour dl
        self.label_complete = customtkinter.CTkLabel(self, text="")
        self.label_complete.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.input_dl = customtkinter.CTkButton(self, text="Telecharger", command=lambda: self.downloadyt())
        self.input_dl.grid(row=3, column=0, padx=10, pady=10, sticky="sew", columnspan=3)

    # Fonction pour definir un chemin
    def browsepath(self):
        dir = filedialog.askdirectory()
        self.path.set(dir)
        self.label_browse = customtkinter.CTkLabel(self.path_frame2, text=f"{self.path.get()}")
        self.label_browse.grid(row=2, column=0, padx=10, pady=10)

    # Fonction Download
    def downloadyt(self):

        self.label_complete.configure(self, text="")
        ytlink = self.input_link.get()
        # ytlink = 'https://youtu.be/2F0G8LKvtnE'
        ytpath = {'home': self.path.get()}

        ydl_opts = {
            'format': self.format_option.get() + "/bestaudio/best",
            'paths': ytpath,
            'ignoreerrors': True,
            'outtmpl': '%(uploader)s/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.format_option.get(),
            }],
            'prefer_ffmpeg': True,
            'progress_hooks': None,
            # 'download_ranges': download_range_func()

        }

        if "youtube" in ytlink or "youtu.be" in ytlink:
            if "playlist" in ytlink:
                ydl_opts.update({'outtmpl': '%(playlist)s/%(uploader)s/%(title)s.%(ext)s'})

            ydl_opts.update({'progress_hooks': [self.percent]})


        if "soundcloud" in ytlink:
            pass


        # Barre de progression
        self.pourcent = customtkinter.CTkLabel(self, text='0%')
        self.pourcent.grid(row=2, column=2, padx=20, pady=10, sticky="ew")
        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky="ew")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # info = ydl.extract_info(ytlink, download=False)
            # print(json.dumps(info['chapters']))
            ydl.download(ytlink)
            self.label_complete.configure(self, text="Telechargement terminé", text_color="green")

    # except:
    #     self.label_complete.configure(text="Lien Youtube invalide", text_color="orange")

    def percent(self, d):
        downloaded_bytes = d['downloaded_bytes']
        total_bytes = d['total_bytes']
        percentage = (downloaded_bytes / total_bytes * 100)
        per = str(int(percentage))
        self.pourcent.configure(text=per + '%')
        self.pourcent.update()
        self.progress_bar.set(float(percentage) / 100)
        self.progress_bar.update()



# Run l'app
app = App()
app.mainloop()

# TODO - V2, faire en sorte qu'elle reconnaisse les lien si ils sont de youtube ou de soundcloud et inclure ffmpeg lors pour le build
# TODO - V3, recuperer des metadatas puis proposer l'album de la dites musique si il y'a ainsi que la possibilité de la dl
