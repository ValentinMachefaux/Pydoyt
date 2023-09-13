import json
import os
import subprocess
from tkinter import filedialog
import yt_dlp
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

        self.browse_path = customtkinter.CTkButton(self.path_frame2, text="Browse", command=lambda: self.give_path())
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

        # Bouton pour dl
        self.label_complete = customtkinter.CTkLabel(self, text="")
        self.label_complete.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.input_dl = customtkinter.CTkButton(self, text="Telecharger", command=lambda: self.download_yt())
        self.input_dl.grid(row=3, column=0, padx=10, pady=10, sticky="sew", columnspan=3)

    # Fonction pour definir un chemin
    def give_path(self):
        dir = filedialog.askdirectory()
        self.path.set(dir)
        self.label_browse = customtkinter.CTkLabel(self.path_frame2, text=f"{self.path.get()}")
        self.label_browse.grid(row=2, column=0, padx=10, pady=10)

    # Fonction pour calculer le pourcentage de dl d'un audio
    def percent(self, d):
        downloaded_bytes = d['downloaded_bytes']
        total_bytes = d['total_bytes']
        percentage = (downloaded_bytes / total_bytes * 100)
        per = str(int(percentage))
        self.pourcent.configure(text=per + '%')
        self.pourcent.update()
        self.progress_bar.set(float(percentage) / 100)
        self.progress_bar.update()

    # Fonction pour calculer le pourcentage fait des chapitres
    def percent_convert(self, chapter, total):
        finished = chapter
        totals = total
        percentage = (chapter / total * 100)
        per = str(int(percentage))
        self.pourcent.configure(text=per + '%')
        self.pourcent.update()
        self.progress_bar.set(float(percentage) / 100)
        self.progress_bar.update()

    # Fonction pour convertir les chapitres
    def convert_chapters(self, video_url, preferred_codec, path, videotitle):
        # Recuperation des infos de la video
        info_dict = yt_dlp.YoutubeDL().extract_info(video_url, download=False)
        chapters = info_dict.get('chapters')
        i = 0

        # Boucle sur les chapitres
        for chapter in chapters:
            title = chapter['title']

            # Remove le fichier si y'a doublon
            removed_existed_files = os.path.join(path, videotitle, f"{title}.{preferred_codec}")
            if os.path.exists(removed_existed_files):
                os.remove(removed_existed_files)

            # Le nom du fichier en entree
            input_filename = f"{title}.webm"

            # Le nom du fichier avec le repertoire en entree
            input_filepath = os.path.join(path,videotitle, input_filename)

            # Le nom du fichier en sortie
            output_filename = f"{title}.{preferred_codec}"

            # Le nom du fichier et du repertoire en sortie
            output_filepath = os.path.join(path, videotitle, output_filename)

            try:

                # Cree un subprocess pour run FFmpeg et convertir le fichier
                subprocess.check_output([
                    'ffmpeg', '-hide_banner', '-i', input_filepath,
                    '-c:a', preferred_codec, '-strict', '-2',
                    '-b:a', '128k',
                    output_filepath
                ])

                # Update visuel d'où en est le process
                i += 1
                self.label_complete.configure(text=f"Chapter :\n {i}/{len(chapters)}", text_color="green")
                self.label_complete.update()
                self.percent_convert(i, len(chapters))
                print(f"Conversion finished for : {output_filename}")

                # Remove les fichiers originaux
                if os.path.exists(input_filepath):
                    os.remove(input_filepath)

            except Exception as e:
                print(f'Erreur : {e}')

    # Fonction Download
    def download_yt(self):
        # sample chapter video https://youtu.be/2F0G8LKvtnE

        self.label_complete.configure(self, text="")
        ytlink = self.input_link.get()
        ytpath = self.path.get()
        # videotitle = None

        # Parametres de youtube dl
        ydl_opts = {
            "format": 'bestaudio/best',
            "ignoreerrors": True,
            "outtmpl": {
                "default": f"{ytpath}/%(uploader)s/%(title)s.%(ext)s",
                "chapter": f"{ytpath}/%(title)s/%(section_title)s.%(ext)s"
            },
            "postprocessors": [
                {
                    "key": "FFmpegSplitChapters",
                    "force_keyframes": False,
                },
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.format_option.get(),
                }, ],
            "prefer_ffmpeg": True,
            "progress_hooks": [],
            "chapter": True,
            # "verbose": True, # Parametre pour avoir plus de details
        }

        # Verification si lien Youtube
        if "youtube" in ytlink or "youtu.be" in ytlink:

            # Si playlist change le template d'output
            if "playlist" in ytlink:
                ydl_opts.update({"outtmpl": "%(playlist)s/%(uploader)s/%(title)s.%(ext)s"})

            # Ajoute la fonction percent au progress hook
            ydl_opts.update({"progress_hooks": [self.percent]})

        # Verification si lien SoundCloud
        if "soundcloud" in ytlink:
            pass

        # Progress bar
        self.pourcent = customtkinter.CTkLabel(self, text='0%')
        self.pourcent.grid(row=2, column=2, padx=20, pady=10, sticky="ew")
        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky="ew")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(ytlink, download=False)
                videotitle = info['title']

                ydl.download([ytlink])

                if info.get('chapters') is not None:
                    self.convert_chapters(ytlink, self.format_option.get(), ytpath, videotitle)

                self.label_complete.configure(text="Téléchargement terminé", text_color="green")
                print('Process finished !')

        except Exception as e:
            self.label_complete.configure(text=f"Erreur : {str(e)}", text_color="red")
            print(f"Erreur : {str(e)}")


# Run l'app
if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("App exited")

# TODO - V2, faire en sorte qu'elle reconnaisse les lien si ils sont de youtube ou de soundcloud et inclure ffmpeg pour le build
