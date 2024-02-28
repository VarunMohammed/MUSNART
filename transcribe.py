import tkinter
import customtkinter
from pytube import YouTube


musnart_transcribe_page = customtkinter.CTk()
musnart_transcribe_page.geometry("1920x1080")
musnart_transcribe_page.title("MUSN-ART: Transcribe")
musnart_transcribe_page.config(background="black")

musnart_title = customtkinter.CTkLabel(master=musnart_transcribe_page,text="MUSN-ART",
                        text_color="white",bg_color="black",fg_color="black",font=("Poppins-Bold",50))
musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

guest_title = customtkinter.CTkLabel(master=musnart_transcribe_page,text="TRANSCRIPTION",
                        text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

audio_link_entry = customtkinter.CTkEntry(master=musnart_transcribe_page,width=400,height=45,
                        corner_radius=5,border_width=1,bg_color="black",fg_color="black",
                        border_color="white",text_color="white",placeholder_text="Enter Link",
                        placeholder_text_color="grey",state=tkinter.CENTER)
audio_link_entry.pack()

submit_link_button = customtkinter.CTkButton(master=musnart_transcribe_page,width=40,height=35,
                        corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                        fg_color="grey",hover_color="lightgreen",border_color="white",
                        text="SUBMIT",text_color="white",state=tkinter.CENTER,
                        command=submitLinkPressed)
submit_link_button.pack()

musnart_transcribe_page.mainloop()