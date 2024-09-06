import math

from src.crawler.Crawler import *
from typing import Callable
from timeit import default_timer as timer

from tkinter import StringVar, CENTER
from customtkinter import (
    CTk,
    CTkButton,
    CTkEntry,
    CTkFont,
    CTkImage,
    CTkLabel,
    CTkToplevel,
    set_appearance_mode,
    set_default_color_theme,
)
folderPath_Album = "H:\Pictures\Scrapper\Buondua-Downloader\Albums"
app_name = "Fapello.Downloader"
version = "3.5"

text_color = "#F0F0F0"
app_name_color = "#ffbf00"

crawler = Buondua(folderPath_Album)

def download_button_command() -> None:
    links = list()
    userInputURL = selected_url.get()
    if ".txt" in userInputURL:
        with open(userInputURL,"r") as file:
            links = file.readlines()
    else:
        links.append(userInputURL)
    links = [url for url in links if crawler.hostname in url]

    startTime = timer()
    albums = crawler.ExtractFromURL(links)
    info_message.set(f"Downloading {len(albums)} albums")
    crawler.DownloadAlbum(albums)
    info_message.set(f"Finished Downloading {len(albums)} albums @{math.trunc(1000*(timer()-startTime))/1000}s")


def stop_download_process() -> None:
    info_message.set(f"Stop Downloading {crawler.downloadedItems} from {crawler.totalItems}")

def create_text_box(textvariable, width, heigth):
    return CTkEntry(
        master=window,
        textvariable=textvariable,
        border_width=1,
        width=width,
        height=heigth,
        font=bold11,
        justify="center",
        fg_color="#000000",
        border_color="#404040"
    )


def create_info_button(command: Callable, text: str, width: int = 150) -> CTkButton:
    return CTkButton(
        master=window,
        command=command,
        text=text,
        fg_color="transparent",
        hover_color="#181818",
        text_color="#C0C0C0",
        anchor="w",
        height=22,
        width=width,
        corner_radius=10,
        font=bold12,
        # image=info_icon
    )


def open_info_simultaneous_downloads():
    CTkMessageBox(
        messageType='info',
        title="Simultaneous downloads",
        subtitle="This widget allows to choose how many files are downloaded simultaneously",
        default_value="6",
        option_list=[]
    )


def open_info_tips():
    CTkMessageBox(
        messageType='info',
        title="Tips",
        subtitle="How to download",
        default_value=None,
        option_list=[
            " Directly by using the link to the album or tag",
            " Linking to a txt-file path containing on each line an url to an album or tag",
        ]
    )



def place_app_name():
    app_name_label = CTkLabel(master=window,
                              text=app_name + " " + version,
                              text_color=app_name_color,
                              font=bold20,
                              anchor="w")

    app_name_label.place(relx=0.5,
                         rely=0.1,
                         anchor=CENTER)


def on_app_close() -> None:
    window.grab_release()
    window.destroy()
    stop_download_process()


class CTkMessageBox(CTkToplevel):

    def __init__(
            self,
            messageType: str,
            title: str,
            subtitle: str,
            default_value: str,
            option_list: list,
    ) -> None:

        super().__init__()

        self._running: bool = False

        self._messageType = messageType
        self._title = title
        self._subtitle = subtitle
        self._default_value = default_value
        self._option_list = option_list
        self._ctkwidgets_index = 0

        self.title('')
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10,
                   self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _ok_event(
            self,
            event=None
    ) -> None:
        self.grab_release()
        self.destroy()

    def _on_closing(
            self
    ) -> None:
        self.grab_release()
        self.destroy()

    def createEmptyLabel(
            self
    ) -> CTkLabel:

        return CTkLabel(master=self,
                        fg_color="transparent",
                        width=500,
                        height=17,
                        text='')

    def placeInfoMessageTitleSubtitle(
            self,
    ) -> None:

        spacingLabel1 = self.createEmptyLabel()
        spacingLabel2 = self.createEmptyLabel()

        if self._messageType == "info":
            title_subtitle_text_color = "#3399FF"
        elif self._messageType == "error":
            title_subtitle_text_color = "#FF3131"

        titleLabel = CTkLabel(
            master=self,
            width=500,
            anchor='w',
            justify="left",
            fg_color="transparent",
            text_color=title_subtitle_text_color,
            font=bold22,
            text=self._title
        )

        if self._default_value != None:
            defaultLabel = CTkLabel(
                master=self,
                width=500,
                anchor='w',
                justify="left",
                fg_color="transparent",
                text_color="#3399FF",
                font=bold17,
                text=f"Default: {self._default_value}"
            )

        subtitleLabel = CTkLabel(
            master=self,
            width=500,
            anchor='w',
            justify="left",
            fg_color="transparent",
            text_color=title_subtitle_text_color,
            font=bold14,
            text=self._subtitle
        )

        spacingLabel1.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        titleLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        if self._default_value != None:
            self._ctkwidgets_index += 1
            defaultLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        subtitleLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        spacingLabel2.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

    def placeInfoMessageOptionsText(
            self,
    ) -> None:

        for option_text in self._option_list:
            optionLabel = CTkLabel(master=self,
                                   width=600,
                                   height=45,
                                   corner_radius=6,
                                   anchor='w',
                                   justify="left",
                                   text_color="#C0C0C0",
                                   fg_color="#282828",
                                   bg_color="transparent",
                                   font=bold12,
                                   text=option_text)

            self._ctkwidgets_index += 1
            optionLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=4, sticky="ew")

        spacingLabel3 = self.createEmptyLabel()

        self._ctkwidgets_index += 1
        spacingLabel3.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

    def placeInfoMessageOkButton(
            self
    ) -> None:

        ok_button = CTkButton(
            master=self,
            command=self._ok_event,
            text='OK',
            width=125,
            font=bold11,
            border_width=1,
            fg_color="#282828",
            text_color="#E0E0E0",
            border_color="#0096FF"
        )

        self._ctkwidgets_index += 1
        ok_button.grid(row=self._ctkwidgets_index, column=1, columnspan=1, padx=(10, 20), pady=(10, 20), sticky="e")

    def _create_widgets(
            self
    ) -> None:

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.placeInfoMessageTitleSubtitle()
        self.placeInfoMessageOptionsText()
        self.placeInfoMessageOkButton()


def place_qualityscaler_button():
    qualityscaler_button = CTkButton(
        master=window,
        # image  = logo_qs,
        # command = openqualityscaler,
        width=30,
        height=30,
        border_width=1,
        fg_color="transparent",
        text_color="#C0C0C0",
        border_color="#404040",
        anchor="center",
        text="",
        font=bold11)
    qualityscaler_button.place(relx=0.055, rely=0.8, anchor=CENTER)


def place_link_textbox():
    link_textbox = create_text_box(selected_url, 150, 32)
    link_textbox.place(relx=0.5, rely=0.3, relwidth=0.85, anchor=CENTER)


def place_simultaneous_downloads_textbox():
    cpu_button = create_info_button(open_info_simultaneous_downloads, "Simultaneous downloads")
    cpu_textbox = create_text_box(selected_cpu_number, 110, 32)

    cpu_button.place(relx=0.42, rely=0.42, anchor=CENTER)
    cpu_textbox.place(relx=0.75, rely=0.42, anchor=CENTER)


def place_tips():
    dns_tips_button = create_info_button(open_info_tips, "Tips", width=110)
    dns_tips_button.place(relx=0.8, rely=0.9, anchor=CENTER)


def place_message_label():
    message_label = CTkLabel(
        master=window,
        textvariable=info_message,
        height=25,
        font=bold11,
        fg_color="#ffbf00",
        text_color="#000000",
        anchor="center",
        corner_radius=25
    )
    message_label.place(relx=0.5, rely=0.78, anchor=CENTER)


def place_download_button():
    download_button = CTkButton(
        master=window,
        command=download_button_command,
        text="DOWNLOAD",
        # image      = download_icon,
        width=140,
        height=30,
        font=bold11,
        border_width=1,
        fg_color="#282828",
        text_color="#E0E0E0",
        border_color="#0096FF")
    download_button.place(relx=0.5, rely=0.9, anchor=CENTER)


class CTkMessageBox(CTkToplevel):

    def __init__(
            self,
            messageType: str,
            title: str,
            subtitle: str,
            default_value: str,
            option_list: list,
    ) -> None:

        super().__init__()

        self._running: bool = False

        self._messageType = messageType
        self._title = title
        self._subtitle = subtitle
        self._default_value = default_value
        self._option_list = option_list
        self._ctkwidgets_index = 0

        self.title('')
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10,
                   self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _ok_event(
            self,
            event=None
    ) -> None:
        self.grab_release()
        self.destroy()

    def _on_closing(
            self
    ) -> None:
        self.grab_release()
        self.destroy()

    def createEmptyLabel(
            self
    ) -> CTkLabel:

        return CTkLabel(master=self,
                        fg_color="transparent",
                        width=500,
                        height=17,
                        text='')

    def placeInfoMessageTitleSubtitle(
            self,
    ) -> None:

        spacingLabel1 = self.createEmptyLabel()
        spacingLabel2 = self.createEmptyLabel()

        if self._messageType == "info":
            title_subtitle_text_color = "#3399FF"
        elif self._messageType == "error":
            title_subtitle_text_color = "#FF3131"

        titleLabel = CTkLabel(
            master=self,
            width=500,
            anchor='w',
            justify="left",
            fg_color="transparent",
            text_color=title_subtitle_text_color,
            font=bold22,
            text=self._title
        )

        if self._default_value != None:
            defaultLabel = CTkLabel(
                master=self,
                width=500,
                anchor='w',
                justify="left",
                fg_color="transparent",
                text_color="#3399FF",
                font=bold17,
                text=f"Default: {self._default_value}"
            )

        subtitleLabel = CTkLabel(
            master=self,
            width=500,
            anchor='w',
            justify="left",
            fg_color="transparent",
            text_color=title_subtitle_text_color,
            font=bold14,
            text=self._subtitle
        )

        spacingLabel1.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        titleLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        if self._default_value != None:
            self._ctkwidgets_index += 1
            defaultLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        subtitleLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=0, sticky="ew")

        self._ctkwidgets_index += 1
        spacingLabel2.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

    def placeInfoMessageOptionsText(
            self,
    ) -> None:

        for option_text in self._option_list:
            optionLabel = CTkLabel(master=self,
                                   width=600,
                                   height=45,
                                   corner_radius=6,
                                   anchor='w',
                                   justify="left",
                                   text_color="#C0C0C0",
                                   fg_color="#282828",
                                   bg_color="transparent",
                                   font=bold12,
                                   text=option_text)

            self._ctkwidgets_index += 1
            optionLabel.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=25, pady=4, sticky="ew")

        spacingLabel3 = self.createEmptyLabel()

        self._ctkwidgets_index += 1
        spacingLabel3.grid(row=self._ctkwidgets_index, column=0, columnspan=2, padx=0, pady=0, sticky="ew")

    def placeInfoMessageOkButton(
            self
    ) -> None:

        ok_button = CTkButton(
            master=self,
            command=self._ok_event,
            text='OK',
            width=125,
            font=bold11,
            border_width=1,
            fg_color="#282828",
            text_color="#E0E0E0",
            border_color="#0096FF"
        )

        self._ctkwidgets_index += 1
        ok_button.grid(row=self._ctkwidgets_index, column=1, columnspan=1, padx=(10, 20), pady=(10, 20), sticky="e")

    def _create_widgets(
            self
    ) -> None:

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.placeInfoMessageTitleSubtitle()
        self.placeInfoMessageOptionsText()
        self.placeInfoMessageOkButton()


class App:
    def __init__(self, window):
        window.title('')
        width = 500
        height = 500
        window.geometry("500x500")
        window.minsize(width, height)
        window.resizable(False, False)

        # window.iconbitmap(find_by_relative_path("Assets" + os_separator + "logo.ico"))

        window.protocol("WM_DELETE_WINDOW", on_app_close)

        place_app_name()
        place_qualityscaler_button()
        # place_github_button()
        # place_telegram_button()
        place_link_textbox()
        place_simultaneous_downloads_textbox()
        place_tips()
        place_message_label()
        place_download_button()


if __name__ == "__main__":
    window = CTk()

    selected_url = StringVar()
    info_message = StringVar()
    selected_cpu_number = StringVar()

    font = "Segoe UI"
    bold8 = CTkFont(family=font, size=8, weight="bold")
    bold9 = CTkFont(family=font, size=9, weight="bold")
    bold10 = CTkFont(family=font, size=10, weight="bold")
    bold11 = CTkFont(family=font, size=11, weight="bold")
    bold12 = CTkFont(family=font, size=12, weight="bold")
    bold13 = CTkFont(family=font, size=13, weight="bold")
    bold14 = CTkFont(family=font, size=14, weight="bold")
    bold16 = CTkFont(family=font, size=16, weight="bold")
    bold17 = CTkFont(family=font, size=17, weight="bold")
    bold18 = CTkFont(family=font, size=18, weight="bold")
    bold19 = CTkFont(family=font, size=19, weight="bold")
    bold20 = CTkFont(family=font, size=20, weight="bold")
    bold21 = CTkFont(family=font, size=21, weight="bold")
    bold22 = CTkFont(family=font, size=22, weight="bold")
    bold23 = CTkFont(family=font, size=23, weight="bold")
    bold24 = CTkFont(family=font, size=24, weight="bold")

    app = App(window)
    window.update()
    window.mainloop()
