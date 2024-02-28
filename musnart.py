import tkinter
import customtkinter
import pyperclip
import argparse
import os
import random
import json
import requests
import pprint
import time
import hashlib
import smtplib
import mysql.connector
from PIL import Image
from typing import Optional
from pytube import YouTube
from twilio.rest import Client
import internetdownloadmanager as idm
from cv2 import *

myconn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Varun@123",
    database="MUSNART"
)

print(myconn)
cur = myconn.cursor()
print(cur)

transMessage = ""
shareEmailID = ""

musnart_app = customtkinter.CTk()
musnart_app.geometry("1920x1080")
musnart_app.title("MUSN-ART")
musnart_app.config(background="black")

bg_img = customtkinter.CTkImage(Image.open("musimg.jpeg"), size=(400, 400))
bg_image = customtkinter.CTkLabel(master=musnart_app,image=bg_img,text=" ",bg_color="black")
bg_image.place(relx=0.3,rely=0.55,anchor=tkinter.CENTER)

username_text = customtkinter.CTkLabel(master=musnart_app,text="",text_color="grey",
                                bg_color="black",fg_color="black")
username_text.place(relx=0.655,rely=0.35,anchor=tkinter.CENTER)

username_entry = customtkinter.CTkEntry(master=musnart_app,width=350,height=45,corner_radius=10,
                                border_width=1,bg_color="black",fg_color="white",border_color="black",
                                text_color="black",placeholder_text="Username",placeholder_text_color="grey",
                                state=tkinter.NORMAL)
username_entry.place(relx=0.7,rely=0.4,anchor=tkinter.CENTER)

#password_text = customtkinter.CTkLabel(master=musnart_app,text="Password",text_color="white",
#                                bg_color="black",fg_color="black")
#password_text.place(relx=0.59,rely=0.45,anchor=tkinter.CENTER)

password_entry = customtkinter.CTkEntry(master=musnart_app,width=350,height=45,corner_radius=10,
                                border_width=1,bg_color="black",fg_color="white",border_color="black",
                                text_color="black",placeholder_text="Password",placeholder_text_color="grey",
                                state=tkinter.NORMAL)
password_entry.place(relx=0.7,rely=0.5,anchor=tkinter.CENTER)

def loginPressed():
    print("Login Pressed")
    if(username_entry.get() == "" and password_entry.get() == ""):
        login_status_label.configure(text="Enter Login Credentials")
    elif(username_entry.get() == "" and password_entry.get() != ""):
        login_status_label.configure(text="Enter Username")
    elif(username_entry.get() != "" and password_entry.get() == ""):
        login_status_label.configure(text="Enter Password")
    elif(username_entry.get() != "" and password_entry.get() != ""):
        print("Login Initiated")
        login_status_label.configure(text="")
        username = username_entry.get()
        password = password_entry.get()
        passwordmd5 = hashlib.md5(password.encode())
        print(passwordmd5.digest())
        sql = "SELECT * from credentials\
        WHERE userName = %s and passWord = %s"
        val = (username,passwordmd5.hexdigest())
        cur.execute(sql, val)
        result = cur.fetchone()
        print(result)
        #if(result == None):
        #    login_status_label.configure(text="Incorrect username or password",text_color="red")
        #else:
        login_status_label.configure(text="")
        shareEmailID = username_entry.get()
        musnart_home_page = customtkinter.CTk()
        musnart_home_page.geometry("1920x1080")
        musnart_home_page.title("MUSNART")
        musnart_home_page.config(background="black")

    musnart_title = customtkinter.CTkLabel(master=musnart_home_page,text="MUSN-ART",text_color="white",
                                bg_color="black",fg_color="black",font=("Poppins-Bold",50))
    musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    guest_title = customtkinter.CTkLabel(master=musnart_home_page,text="USER HOME",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
    guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

    def transcribePressed():
        print("Transcribe Pressed")

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

        def returnPressed():
            musnart_transcribe_page.destroy()

        return_button = customtkinter.CTkButton(master=musnart_transcribe_page,text="Return to Menu",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",15),
                                command=returnPressed)
        return_button.place(relx=0.5,rely=0.24,anchor=tkinter.CENTER)

        audio_link_entry = customtkinter.CTkEntry(master=musnart_transcribe_page,width=400,height=45,
                                corner_radius=5,border_width=1,bg_color="black",fg_color="black",
                                border_color="white",text_color="white",placeholder_text="Enter Link",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
        audio_link_entry.place(relx=0.5,rely=0.30,anchor=tkinter.CENTER)

        def submitLinkPressed():
            print("Submit Link Pressed")
            ytLink = audio_link_entry.get()
            ytObject = YouTube(ytLink,on_progress_callback=on_progress)
            audio = ytObject.streams.get_audio_only()
            audio.download(filename="audio.mp3")

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentageOfCompletion = bytes_downloaded / total_size * 100
            per = str(int(percentageOfCompletion))
            guest_title.configure(text=per + '%')
            guest_title.update()
            
            progressbar.set(float(percentageOfCompletion) / 100)

        submit_link_button = customtkinter.CTkButton(master=musnart_transcribe_page,width=40,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="SUBMIT",text_color="black",state=tkinter.NORMAL,
                                command=submitLinkPressed)
        submit_link_button.place(relx=0.383,rely=0.37,anchor=tkinter.CENTER)

        progressbar = customtkinter.CTkProgressBar(master=musnart_transcribe_page,width=320)
        progressbar.place(relx=0.5265,rely=0.37,anchor=tkinter.CENTER)
        progressbar.set(0)

        def doTranscribe():
            API_KEY = "7ca40d1cc29f4f6997538424a196103f"

            def read_file(filename, chunk_size=5242880):
            # Open the file in binary mode for reading
                with open(filename, 'rb') as _file:
                    while True:
                        # Read a chunk of data from the file
                        data = _file.read(chunk_size)
                        # If there's no more data, stop reading
                        if not data:
                            break
                        # Yield the data as a generator
                        yield data

            def upload_file(api_token, path):
                """
                Upload a file to the AssemblyAI API.

                Args:
                api_token (str): Your API token for AssemblyAI.
                path (str): Path to the local file.

                Returns:
                str: The upload URL.
                """
                print(f"Uploading file: {path}")

                # Set the headers for the request, including the API token
                headers = {'authorization': api_token}
    
                # Send a POST request to the API to upload the file, passing in the headers
                # and the file data
                response = requests.post('https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    data=read_file(path))

                # If the response is successful, return the upload URL
                if response.status_code == 200:
                    return response.json()["upload_url"]
                # If the response is not successful, print the error message and return
                # None
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    return None

            def create_transcript(api_token, audio_url):
                """
                Create a transcript using AssemblyAI API.

                Args:
                api_token (str): Your API token for AssemblyAI.
                audio_url (str): URL of the audio file to be transcribed.

                Returns:
                dict: Completed transcript object.
                """
                print("Transcribing audio... This might take a moment.")

                # Set the API endpoint for creating a new transcript
                url = "https://api.assemblyai.com/v2/transcript"

                # Set the headers for the request, including the API token and content type
                headers = {
                    "authorization": api_token,
                    "content-type": "application/json"
                }

                # Set the data for the request, including the URL of the audio file to be
                # transcribed
                data = {
                    "audio_url": audio_url
                }

                # Send a POST request to the API to create a new transcript, passing in the
                # headers and data
                response = requests.post(url, json=data, headers=headers)

                # Get the transcript ID from the response JSON data
                transcript_id = response.json()['id']

                # Set the polling endpoint URL by appending the transcript ID to the API endpoint
                polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

                # Keep polling the API until the transcription is complete
                while True:
                    # Send a GET request to the polling endpoint, passing in the headers
                    transcription_result = requests.get(polling_endpoint, headers=headers).json()

                    # If the status of the transcription is 'completed', exit the loop
                    if transcription_result['status'] == 'completed':
                        break

                    # If the status of the transcription is 'error', raise a runtime error with
                    # the error message
                    elif transcription_result['status'] == 'error':
                        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

                    # If the status of the transcription is not 'completed' or 'error', wait for
                    # 3 seconds and poll again
                    else:
                        time.sleep(3)

                return transcription_result
            
            filename = "./audio.mp3"
            upload_url = upload_file(API_KEY, filename)
            transcript = create_transcript(API_KEY, upload_url)
            print(transcript['text'])

            transRes = transcript['text']
            res = transRes
            transMessage = transRes

            audio_link = audio_link_entry.get()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            transcription_result.configure(text=transRes)

            sql_transcription = "INSERT INTO transcribe_MUSNART\
            VALUES (%s,%s,%s)"
            val_transcription = (current_time,shareEmailID,audio_link_entry)
            cur.execute(sql_transcription,(val_transcription,))
            myconn.commit()

        res = ""
        transcribe_button = customtkinter.CTkButton(master=musnart_transcribe_page,width=400,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="TRANSCRIBE",text_color="black",state=tkinter.NORMAL,
                                command=doTranscribe)
        transcribe_button.place(relx=0.5,rely=0.43,anchor=tkinter.CENTER)

        transcription_result = customtkinter.CTkLabel(master=musnart_transcribe_page,
                                bg_color="black",fg_color="black",text="Result: ",
                                text_color="white",wraplength=1200)
        transcription_result.place(relx=0.5,rely=0.68,anchor=tkinter.CENTER)

        musnart_transcribe_page.mainloop()

    transcribe_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="TRANSCRIBE",
                                font=("Poppins-Bold",30),command=transcribePressed)
    transcribe_menu_button.place(relx=0.2,rely=0.5,anchor=tkinter.CENTER)

    def summarizePressed():
        print("Summarize Pressed")
        musnart_summarize_page = customtkinter.CTk()
        musnart_summarize_page.geometry("1920x1080")
        musnart_summarize_page.title("MUSN-ART: Summarizer")
        musnart_summarize_page.config(background="black")

        musnart_title = customtkinter.CTkLabel(master=musnart_summarize_page,text="MUSN-ART",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins-Bold",50))
        musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        guest_title = customtkinter.CTkLabel(master=musnart_summarize_page,text="SUMMARIZATION",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
        guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

        def returnPressed():
            musnart_summarize_page.destroy()

        return_button = customtkinter.CTkButton(master=musnart_summarize_page,text="Return to Menu",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",15),
                                command=returnPressed)
        return_button.place(relx=0.5,rely=0.24,anchor=tkinter.CENTER)

        audio_link_entry = customtkinter.CTkEntry(master=musnart_summarize_page,width=400,height=45,
                                corner_radius=5,border_width=1,bg_color="black",fg_color="black",
                                border_color="white",text_color="white",placeholder_text="Enter Link",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
        audio_link_entry.place(relx=0.5,rely=0.30,anchor=tkinter.CENTER)

        def submitLinkPressed():
            print("Submit Link Pressed")
            ytLink = audio_link_entry.get()
            ytObject = YouTube(ytLink,on_progress_callback=on_progress)
            audio = ytObject.streams.get_audio_only()
            audio.download(filename="audio.mp3")

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentageOfCompletion = bytes_downloaded / total_size * 100
            per = str(int(percentageOfCompletion))
            guest_title.configure(text=per + '%')
            guest_title.update()
            
            progressbar.set(float(percentageOfCompletion) / 100)

        submit_link_button = customtkinter.CTkButton(master=musnart_summarize_page,width=40,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="SUBMIT",text_color="black",state=tkinter.NORMAL,
                                command=submitLinkPressed)
        submit_link_button.place(relx=0.383,rely=0.37,anchor=tkinter.CENTER)

        progressbar = customtkinter.CTkProgressBar(master=musnart_summarize_page,width=320)
        progressbar.place(relx=0.5265,rely=0.37,anchor=tkinter.CENTER)
        progressbar.set(0)

        def doSummarize():
            print("doSummarize Pressed")

            API_KEY = "7ca40d1cc29f4f6997538424a196103f"

            base_url = "https://api.assemblyai.com/v2"

            headers = {
                "authorization": "7ca40d1cc29f4f6997538424a196103f"
            }

            with open("./audio.mp3", "rb") as f:
                response = requests.post(base_url + "/upload",
                                        headers=headers,
                                        data=f)

            upload_url = response.json()["upload_url"]

            data = {
                "audio_url": upload_url,
                "summarization": True,
                "summary_model": "informative",
                "summary_type": "bullets"
            }

            url = base_url + "/transcript"
            response = requests.post(url, json=data, headers=headers)

            transcript_id = response.json()['id']
            polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

            summ = ""

            import time

            while True:
                transcription_result = requests.get(polling_endpoint, headers=headers).json()
                if transcription_result['status'] == 'completed':
                    summary = transcription_result.get('summary', '')
                    print("Transcription completed!")
                    print(f"Transcription: {transcription_result['text']}")
                    print(f"Summary: {summary}")
                    summ = summary
                    break

                elif transcription_result['status'] == 'error':
                    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

                else:
                    time.sleep(3)

            sql_summarization = "INSERT INTO summarize_MUSNART\
            VALUES (%s,%s,%s)"
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            #val_summarization = (current_time,shareEmailID,audio_link_entry)
            #cur.execute(sql_summarization,val_summarization)
            #myconn.commit()

            summarization_result.configure(text=summary)

        res = ""
        summarize_button = customtkinter.CTkButton(master=musnart_summarize_page,width=400,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="SUMMARIZE",text_color="black",state=tkinter.NORMAL,
                                command=doSummarize)
        summarize_button.place(relx=0.5,rely=0.43,anchor=tkinter.CENTER)

        summarization_result = customtkinter.CTkLabel(master=musnart_summarize_page,
                                bg_color="black",fg_color="black",text="Result: ",
                                text_color="white",wraplength=1200)
        summarization_result.place(relx=0.5,rely=0.68,anchor=tkinter.CENTER)

        musnart_summarize_page.mainloop()

    summarize_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="SUMMARIZE",
                                font=("Poppins-Bold",30),command=summarizePressed)
    summarize_menu_button.place(relx=0.4,rely=0.5,anchor=tkinter.CENTER)

    def transumPressed():
        print("transum Pressed")
        musnart_transum_page = customtkinter.CTk()
        musnart_transum_page.geometry("1920x1080")
        musnart_transum_page.title("MUSN-ART: Summarizer")
        musnart_transum_page.config(background="black")

        musnart_title = customtkinter.CTkLabel(master=musnart_transum_page,text="MUSN-ART",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins-Bold",50))
        musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        guest_title = customtkinter.CTkLabel(master=musnart_transum_page,text="TRANSUM",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
        guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

        def returnPressed():
            musnart_transum_page.destroy()

        return_button = customtkinter.CTkButton(master=musnart_transum_page,text="Return to Menu",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",15),
                                command=returnPressed)
        return_button.place(relx=0.5,rely=0.24,anchor=tkinter.CENTER)

        audio_link_entry = customtkinter.CTkEntry(master=musnart_transum_page,width=400,height=45,
                                corner_radius=5,border_width=1,bg_color="black",fg_color="black",
                                border_color="white",text_color="white",placeholder_text="Enter Link",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
        audio_link_entry.place(relx=0.5,rely=0.30,anchor=tkinter.CENTER)

        def submitLinkPressed():
            print("Submit Link Pressed")
            ytLink = audio_link_entry.get()
            ytObject = YouTube(ytLink,on_progress_callback=on_progress)
            audio = ytObject.streams.get_audio_only()
            audio.download(filename="audio.mp3")

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentageOfCompletion = bytes_downloaded / total_size * 100
            per = str(int(percentageOfCompletion))
            guest_title.configure(text=per + '%')
            guest_title.update()
            
            progressbar.set(float(percentageOfCompletion) / 100)

        submit_link_button = customtkinter.CTkButton(master=musnart_transum_page,width=40,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="SUBMIT",text_color="black",state=tkinter.NORMAL,
                                command=submitLinkPressed)
        submit_link_button.place(relx=0.383,rely=0.37,anchor=tkinter.CENTER)

        progressbar = customtkinter.CTkProgressBar(master=musnart_transum_page,width=320)
        progressbar.place(relx=0.5265,rely=0.37,anchor=tkinter.CENTER)
        progressbar.set(0)

        def doTransum():
            print("doSummarize Pressed")

            API_KEY = "7ca40d1cc29f4f6997538424a196103f"

            def read_file(filename, chunk_size=5242880):
            # Open the file in binary mode for reading
                with open(filename, 'rb') as _file:
                    while True:
                        # Read a chunk of data from the file
                        data = _file.read(chunk_size)
                        # If there's no more data, stop reading
                        if not data:
                            break
                        # Yield the data as a generator
                        yield data

            def upload_file(api_token, path):
                """
                Upload a file to the AssemblyAI API.

                Args:
                api_token (str): Your API token for AssemblyAI.
                path (str): Path to the local file.

                Returns:
                str: The upload URL.
                """
                print(f"Uploading file: {path}")

                # Set the headers for the request, including the API token
                headers = {'authorization': api_token}
    
                # Send a POST request to the API to upload the file, passing in the headers
                # and the file data
                response = requests.post('https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    data=read_file(path))

                # If the response is successful, return the upload URL
                if response.status_code == 200:
                    return response.json()["upload_url"]
                # If the response is not successful, print the error message and return
                # None
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    return None

            def create_transcript(api_token, audio_url):
                """
                Create a transcript using AssemblyAI API.

                Args:
                api_token (str): Your API token for AssemblyAI.
                audio_url (str): URL of the audio file to be transcribed.

                Returns:
                dict: Completed transcript object.
                """
                print("Transcribing audio... This might take a moment.")

                # Set the API endpoint for creating a new transcript
                url = "https://api.assemblyai.com/v2/transcript"

                # Set the headers for the request, including the API token and content type
                headers = {
                    "authorization": api_token,
                    "content-type": "application/json"
                }

                # Set the data for the request, including the URL of the audio file to be
                # transcribed
                data = {
                    "audio_url": audio_url
                }

                # Send a POST request to the API to create a new transcript, passing in the
                # headers and data
                response = requests.post(url, json=data, headers=headers)

                # Get the transcript ID from the response JSON data
                transcript_id = response.json()['id']

                # Set the polling endpoint URL by appending the transcript ID to the API endpoint
                polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

                # Keep polling the API until the transcription is complete
                while True:
                    # Send a GET request to the polling endpoint, passing in the headers
                    transcription_result = requests.get(polling_endpoint, headers=headers).json()

                    # If the status of the transcription is 'completed', exit the loop
                    if transcription_result['status'] == 'completed':
                        break

                    # If the status of the transcription is 'error', raise a runtime error with
                    # the error message
                    elif transcription_result['status'] == 'error':
                        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

                    # If the status of the transcription is not 'completed' or 'error', wait for
                    # 3 seconds and poll again
                    else:
                        time.sleep(3)

                return transcription_result
            
            filename = "./audio.mp3"
            upload_url = upload_file(API_KEY, filename)
            transcript = create_transcript(API_KEY, upload_url)
            print(transcript['text'])

            #transcription_result.configure(text=transcript['text'])

            API_KEY = "7ca40d1cc29f4f6997538424a196103f"

            base_url = "https://api.assemblyai.com/v2"

            headers = {
                "authorization": "7ca40d1cc29f4f6997538424a196103f"
            }

            with open("./audio.mp3", "rb") as f:
                response = requests.post(base_url + "/upload",
                                        headers=headers,
                                        data=f)

            upload_url = response.json()["upload_url"]

            data = {
                "audio_url": upload_url,
                "summarization": True,
                "summary_model": "informative",
                "summary_type": "bullets"
            }

            url = base_url + "/transcript"
            response = requests.post(url, json=data, headers=headers)

            transcript_id = response.json()['id']
            polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

            summ = ""

            while True:
                transcription_result = requests.get(polling_endpoint, headers=headers).json()
                if transcription_result['status'] == 'completed':
                    summary = transcription_result.get('summary', '')
                    print("Transcription completed!")
                    print(f"Transcription: {transcription_result['text']}")
                    print(f"Summary: {summary}")
                    summ = summary
                    break

                elif transcription_result['status'] == 'error':
                    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

                else:
                    time.sleep(3)
            
            summarization_result.configure(text=summ)

            sql_transum = "INSERT INTO transum_MUSNART\
            VALUES (%s,%s,%s)"
            val_transum = (current_time,shareEmailID,audio_link_entry)
            cur.execute(sql_transum,(val_transum,))
            myconn.commit()

        res = ""
        summarize_button = customtkinter.CTkButton(master=musnart_transum_page,width=400,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="TRANSUM",text_color="black",state=tkinter.NORMAL,
                                command=doTransum)
        summarize_button.place(relx=0.5,rely=0.43,anchor=tkinter.CENTER)

        transcription_result = customtkinter.CTkLabel(master=musnart_transum_page,
                                bg_color="black",fg_color="black",text="Result: ",
                                text_color="white",wraplength=1200)
        transcription_result.place(relx=0.5,rely=0.58,anchor=tkinter.CENTER)

        summarization_result = customtkinter.CTkLabel(master=musnart_transum_page,
                                bg_color="black",fg_color="black",text="Result: ",
                                text_color="white",wraplength=1200)
        summarization_result.place(relx=0.5,rely=0.78,anchor=tkinter.CENTER)

        musnart_summarize_page.mainloop()

    transum_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="TRANSCRIBE\n&\nSUMMARIZE",
                                font=("Poppins-Bold",30),command=transumPressed)
    transum_menu_button.place(relx=0.6,rely=0.5,anchor=tkinter.CENTER)

    def wikisumPressed():
        print("Wikisum Pressed")
        musnart_wikisum_page = customtkinter.CTk()
        musnart_wikisum_page.geometry("1920x1080")
        musnart_wikisum_page.title("MUSN-ART: WikiSum")
        musnart_wikisum_page.config(background="black")

        musnart_title = customtkinter.CTkLabel(master=musnart_wikisum_page,text="MUSN-ART",text_color="white",
                                bg_color="black",fg_color="black",font=("Poppins-Bold",50))
        musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        guest_title = customtkinter.CTkLabel(master=musnart_wikisum_page,text="GUEST USER MODE",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
        guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

        import wikipedia

        summary_display_guest = customtkinter.CTkLabel(master=musnart_wikisum_page,width=900,height=500,
                                corner_radius=0,bg_color="black",fg_color="black",text_color="white",
                                text="",wraplength=900)
        summary_display_guest.place(relx=0.5,rely=0.73,anchor=tkinter.CENTER)

        topic_entry = customtkinter.CTkEntry(master=musnart_wikisum_page,width=400,height=45,corner_radius=10,
                                border_width=1,bg_color="black",fg_color="white",border_color="grey",
                                text_color="black",placeholder_text="Enter Topic",placeholder_text_color="grey",
                                state=tkinter.NORMAL)
        topic_entry.place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)

        language_select = customtkinter.CTkComboBox(master=musnart_wikisum_page,values=["Language","English","Hindi"],
                                            width=110,height=30,corner_radius=10,border_width=1,bg_color="black",
                                            fg_color="black",border_color="grey",button_color="grey",
                                            button_hover_color="cyan")
        language_select.place(relx=0.72,rely=0.4,anchor=tkinter.CENTER)

        def topicSubmitPressed():
            print("Topic Submit Pressed")
            searchLang = language_select.get()
            if(searchLang == "Language"):
                summary_display_guest.configure(text="Choose Language")
            elif(searchLang == "English"):
                wikipedia.set_lang("en")
                displaySearchResult()
            elif(searchLang == "Hindi"):
                wikipedia.set_lang("hi")
                displaySearchResult()

        def displaySearchResult():
            searchResult = wikipedia.summary("{}".format(topic_entry.get()),sentences=5)
            print(searchResult)
            if(searchResult == None):
                print("Choose another topic")
                topic_suggest_app = customtkinter.CTk()
                topic_suggest_app.geometry("500x300")
                topic_suggest_app.title("MUSN-ART: Topic Suggest")
                topic_suggest_app.config(background="black")

                suggestion_results = wikipedia.search(topic_entry.get(),results=5)

                suggested_topic_label = customtkinter.CTkLabel(master=topic_suggest_app,width=250,
                        height=150,text=suggestion_results,text_color="white",bg_color="black",
                        fg_color="black")
                suggested_topic_label.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

                topic_suggest_app.mainloop()

            summary_display_guest.configure(text=searchResult)
            sql_wikisum = "INSERT INTO wikisum_MUSNART\
            VALUES (%s,%s,%s)"
            val_wikisum = (current_time,shareEmailID,audio_link_entry)
            cur.execute(sql_wikisum,(val_wikisum,))
            myconn.commit()

        topic_submit_button = customtkinter.CTkButton(master=musnart_wikisum_page,width=400,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="green",hover_color="lightgreen",border_color="white",
                                text_color="black",text_color_disabled="grey",text="SUBMIT",
                                state=tkinter.NORMAL,command=topicSubmitPressed)
        topic_submit_button.place(relx=0.5,rely=0.47,anchor=tkinter.CENTER)

        musnart_wikisum_page.mainloop()

    wikisum_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="WIKI-SUM",
                                font=("Poppins-Bold",30),command=wikisumPressed)
    wikisum_menu_button.place(relx=0.8,rely=0.5,anchor=tkinter.CENTER)

    def vissumPressed():
        print("Vissum Pressed")
        
        #import cv2
        #import pytesseract

        musnart_vissum_page = customtkinter.CTk()
        musnart_vissum_page.geometry("1920x1080")
        musnart_vissum_page.title("MUSN-ART: VIS-SUM")
        musnart_vissum_page.config(background="black")

        musnart_title = customtkinter.CTkLabel(master=musnart_vissum_page,text="MUSN-ART",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins-Bold",50))
        musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        guest_title = customtkinter.CTkLabel(master=musnart_vissum_page,text="VIS-SUM",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
        guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

        def returnPressed():
            musnart_vissum_page.destroy()

        return_button = customtkinter.CTkButton(master=musnart_vissum_page,text="Return to Menu",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",15),
                                command=returnPressed)
        return_button.place(relx=0.5,rely=0.24,anchor=tkinter.CENTER)

        image_link_entry = customtkinter.CTkEntry(master=musnart_vissum_page,width=400,height=45,
                                corner_radius=5,border_width=1,bg_color="black",fg_color="black",
                                border_color="white",text_color="white",placeholder_text="Enter Image Link",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
        image_link_entry.place(relx=0.5,rely=0.30,anchor=tkinter.CENTER)

        def submitImageLinkPressed():
            import internetdownloadmanager as idm
            imageLink = image_link_entry.get()

            def Downloader(url,output):
                pydownloader = idm.Downloader(worker=20,part_size=1000000,resumable=True,)
                pydownloader.download(url,output)

            def textandplay(ret: str):
                from gtts import gTTS
                language = 'en'
                tts = gTTS(text=ret,lang=language,slow=False)
                tts.save("vissumaudio.mp3")

                from playsound import playsound
                playsound("vissumaudio.mp3")

            Downloader(imageLink, "sample.png")

            import pytesseract as pt

            img_file = 'sample.png'
            print ('Opening Sample file using Pillow')
            img_obj = Image.open(img_file)
            print ('Converting %s to string'%img_file)
            ret = pt.image_to_string(img_obj)
            print ('Result is: ', ret)

            extracted_text_label.configure(text=ret)
            textandplay(ret)

            sql_vissum = "INSERT INTO vissum_MUSNART\
            VALUES (%s,%s,%s)"
            val_vissum = (current_time,shareEmailID,audio_link_entry)
            cur.execute(sql_vissum,(val_vissum,))
            myconn.commit()

        submit_image_link_button = customtkinter.CTkButton(master=musnart_vissum_page,width=40,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="grey",
                                fg_color="white",hover_color="lightgreen",border_color="white",
                                text="SUBMIT",text_color="black",state=tkinter.NORMAL,
                                command=submitImageLinkPressed)
        submit_image_link_button.place(relx=0.383,rely=0.37,anchor=tkinter.CENTER)

        extracted_text_label = customtkinter.CTkLabel(master=musnart_vissum_page,text="",
                                text_color="white",wraplength=1000,fg_color="black",bg_color="black")
        extracted_text_label.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        musnart_vissum_page.mainloop()        

    vissum_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="VIS-SUM",
                                font=("Poppins-Bold",30),command=vissumPressed)
    vissum_menu_button.place(relx=0.2,rely=0.8,anchor=tkinter.CENTER)

    def communityPressed():
        print("Community Pressed")
        community_page = customtkinter.CTk()
        community_page.geometry("1920x1080")
        community_page.title("MUSNART: Community")
        community_page.config(background="black")

        guest_title = customtkinter.CTkLabel(master=community_page,text="Made by\n\nABEL BINOY\nFARSEEN MUHAMMED\nK A MUHAMMED\nVARUN MOHAMMED",
            text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
        guest_title.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        def returnPressed():
            community_page.destroy()

        return_button = customtkinter.CTkButton(master=community_page,text="Return to Menu",
            text_color="white",bg_color="black",fg_color="black",font=("Poppins",15),
            command=returnPressed)
        return_button.place(relx=0.5,rely=0.24,anchor=tkinter.CENTER)



    community_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="ABOUT",
                                font=("Poppins-Bold",30),command=communityPressed)
    community_menu_button.place(relx=0.4,rely=0.8,anchor=tkinter.CENTER)

    def historyPressed():
        print("History Pressed")

    history_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="MUSNART",
                                font=("Poppins-Bold",30),command=historyPressed)
    history_menu_button.place(relx=0.6,rely=0.8,anchor=tkinter.CENTER)

    editdetls_menu_button = customtkinter.CTkButton(master=musnart_home_page,width=200,height=200,
                                corner_radius=10,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="black",hover_color="black",border_color="white",text_color="white",
                                text_color_disabled="grey",state=tkinter.NORMAL,text="EDIT-DETAILS",
                                font=("Poppins-Bold",30),command=editdetlsPressed)
    editdetls_menu_button.place(relx=0.8,rely=0.8,anchor=tkinter.CENTER)

    musnart_home_page.mainloop()

login_status_label = customtkinter.CTkLabel(master=musnart_app,width=350,height=20,bg_color=
                                "black",fg_color="black",text="Enter Credentials")
login_status_label.place(relx=0.575,rely=0.53)

login_button = customtkinter.CTkButton(master=musnart_app,width=350,height=40,corner_radius=0,
                                border_width=0,border_spacing=1,bg_color="lightgreen",fg_color="lightgreen",
                                hover_color="green",border_color="white",text_color="black",
                                command=loginPressed,text="LOGIN",font=("Poppins",15))
login_button.place(relx=0.7,rely=0.6,anchor=tkinter.CENTER)

#mainimg = customtkinter.CTkImage(light_image=Image.open("mainimg.png"),dark_image=Image.open("mainimg.png"),
#                                size=(500,500))
#main_image = customtkinter.CTkLabel(master=musnart_app,image=mainimg,text="",bg_color="black",
#                                fg_color="black")
#main_image.place(relx=0.07,rely=0.18)

musnart_title = customtkinter.CTkLabel(master=musnart_app,text="MUSN-ART",text_color="white",
                                bg_color="black",fg_color="black",font=("Poppins-Bold",50))
musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

def registerPressed():
    print("Register Pressed")
    musnart_register_app = customtkinter.CTk()
    musnart_register_app.geometry("1920x1080")
    musnart_register_app.title("MUSN-ART: Registration")
    musnart_register_app.config(background="black")

    #musnart_app.geometry("0x0")

    musnart_title = customtkinter.CTkLabel(master=musnart_register_app,text="MUSN-ART",text_color="white",
                                bg_color="black",fg_color="black",font=("Poppins-Bold",50))
    musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    registration_title = customtkinter.CTkLabel(master=musnart_register_app,text="User Registration",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
    registration_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

    firstname_entry = customtkinter.CTkEntry(master=musnart_register_app,width=200,height=45,
                                corner_radius=10,border_width=1,bg_color="black",fg_color="white",
                                border_color="black",text_color="black",placeholder_text="First Name",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
    firstname_entry.place(relx=0.42,rely=0.4,anchor=tkinter.CENTER)

    lastname_entry = customtkinter.CTkEntry(master=musnart_register_app,width=200,height=45,
                                corner_radius=10,border_width=1,bg_color="black",fg_color="white",
                                border_color="black",text_color="black",placeholder_text="Last Name",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
    lastname_entry.place(relx=0.59,rely=0.4,anchor=tkinter.CENTER)

    mailid_entry = customtkinter.CTkEntry(master=musnart_register_app,width=420,height=45,
                                corner_radius=10,border_width=1,bg_color="black",fg_color="white",
                                border_color="black",text_color="black",placeholder_text="Email Address",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
    mailid_entry.place(relx=0.505,rely=0.485,anchor=tkinter.CENTER)

    password_reg_entry = customtkinter.CTkEntry(master=musnart_register_app,width=200,height=45,
                                corner_radius=10,border_width=1,bg_color="black",fg_color="white",
                                border_color="black",text_color="black",placeholder_text="Password",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
    password_reg_entry.place(relx=0.42,rely=0.57,anchor=tkinter.CENTER)

    password_con_entry = customtkinter.CTkEntry(master=musnart_register_app,width=200,height=45,
                                corner_radius=10,border_width=1,bg_color="black",fg_color="white",
                                border_color="black",text_color="black",placeholder_text="Confirm Password",
                                placeholder_text_color="grey",state=tkinter.NORMAL)
    password_con_entry.place(relx=0.59,rely=0.57,anchor=tkinter.CENTER)

    #image = ImageCaptcha(width=280,height=90)
    #captcha_text = "MUSN-ART"
    #data = image.generate(captcha_text)
    #image.write(captcha_text, 'CAPTCHA.png')

    #captcha_img = customtkinter.CTkImage(light_image=Image.open("CAPTCHA.png"),dark_image=Image.open("CAPTCHA.png"),
    #                            size=(280,90))
    #captcha_image = customtkinter.CTkLabel(master=musnart_register_app,image=captcha_img,text="")
    #captcha_image.place(relx=0.42,rely=0.8,anchor=tkinter.CENTER)

    checkboxVar = customtkinter.IntVar(value=0)

    def buttonStateChange(stateNumber: int):
        print("Button State Change called")
        if(stateNumber == 0):
            register_button.configure(state=tkinter.DISABLED)
        else:
            register_button.configure(state=tkinter.NORMAL)

    def checkboxPressed():
        print("Checkbox Pressed")
        checkboxVar = 1
        print(checkboxVar)
        buttonStateChange(checkboxVar)

    tandc_check = customtkinter.CTkCheckBox(master=musnart_register_app,width=100,height=24,
                                checkbox_height=20,checkbox_width=20,corner_radius=0,
                                border_width=1,bg_color="black",fg_color="black",hover_color="white",
                                border_color="white",checkmark_color="white",text_color="white",
                                text="Agree to the Terms and Conditions",state=tkinter.NORMAL,
                                command=checkboxPressed,variable=checkboxVar)
    tandc_check.place(relx=0.5,rely=0.65,anchor=tkinter.CENTER)

    def registerButtonPressed():
        print("Register Button in New Registration pressed")
        if(mailid_entry.get()!="" and password_reg_entry.get()!="" and password_con_entry.get()!="", firstname_entry.get()!="" and lastname_entry.get()!=""):
            #if(passCheck(password_reg_entry.get()) is True and passCheck(password_con_entry.get() is True)):
            if(password_reg_entry.get() == password_con_entry.get()):
                username = mailid_entry.get()
                password = password_con_entry.get()
                passwordmd5 = hashlib.md5(password.encode()).hexdigest()
                print(passwordmd5)
                sql_register = "SELECT * from credentials\
                WHERE userName = %s and passWord = %s"
                val_register = (username,password)
                cur.execute(sql_register, val_register)
                resultregister = cur.fetchone()
                print(resultregister)
                if(result == None):
                    sqlin = "INSERT INTO credentials (userName, passWord)\
                    VALUES (%s, %s)"
                    valin = (username,password)

                    cur.execute(sqlin, valin)
                    myconn.commit()

                    sql1 = "INSERT INTO userDetails (firstName,lastName,email)\
                    VALUES (%s,%s,%s)"
                    val1 = (firstname_entry.get(),lastname_entry.get(),mailid_entry.get())

                    cur.execute(sql1,val1)
                    myconn.commit()

    register_button = customtkinter.CTkButton(master=musnart_register_app,width=420,height=40,corner_radius=0,
                                border_width=0,border_spacing=1,bg_color="lightgreen",fg_color="lightgreen",
                                hover_color="green",border_color="white",text_color="black",
                                command=registerButtonPressed,text="REGISTER",font=("Poppins",15))
    register_button.place(relx=0.505,rely=0.75,anchor=tkinter.CENTER)

    def returnToLoginPressed():
        print("Return to login pressed")
        musnart_register_app.geometry("0x0")
        pyperclip.copy(mailid_entry.get())
        username_text.configure(text="Press Command+V to paste username")
        musnart_register_app.destroy()

    return_to_login = customtkinter.CTkButton(master=musnart_register_app,width=100,height=30,
                                corner_radius=0,border_width=0,border_spacing=0,bg_color="black",
                                fg_color="black",hover_color="black",border_color="black",
                                text_color="white",text="Account Created? Click to Log-in",
                                state=tkinter.NORMAL,command=returnToLoginPressed)
    return_to_login.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)
                            
    musnart_register_app.mainloop()

signup_button = customtkinter.CTkButton(master=musnart_app,width=170,height=40,corner_radius=0,
                                border_width=0,border_spacing=1,bg_color="orange",fg_color="orange",
                                hover_color="white",border_color="white",text_color="black",
                                command=registerPressed,text="REGISTER",font=("Poppins",15))
signup_button.place(relx=0.638,rely=0.69,anchor=tkinter.CENTER)

def guestPressed():
    print("Guest Pressed")
    musnart_guest_app = customtkinter.CTk()
    musnart_guest_app.geometry("1920x1080")
    musnart_guest_app.title("MUSN-ART: Guest")
    musnart_guest_app.config(background="black")

    musnart_title = customtkinter.CTkLabel(master=musnart_guest_app,text="MUSN-ART",text_color="white",
                                bg_color="black",fg_color="black",font=("Poppins-Bold",50))
    musnart_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    guest_title = customtkinter.CTkLabel(master=musnart_guest_app,text="GUEST USER MODE",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
    guest_title.place(relx=0.5,rely=0.2,anchor=tkinter.CENTER)

    import wikipedia

    summary_display_guest = customtkinter.CTkLabel(master=musnart_guest_app,width=900,height=500,
                                corner_radius=0,bg_color="black",fg_color="black",text_color="white",
                                text="",wraplength=900)
    summary_display_guest.place(relx=0.5,rely=0.73,anchor=tkinter.CENTER)

    trial_desc = customtkinter.CTkLabel(master=musnart_guest_app,text="This is Guest Mode and all the features of our application wont be available",
                                text_color="white",bg_color="black",fg_color="black",font=("Poppins",20))
    trial_desc.place(relx=0.5,rely=0.3,anchor=tkinter.CENTER)

    topic_entry = customtkinter.CTkEntry(master=musnart_guest_app,width=400,height=45,corner_radius=10,
                                border_width=1,bg_color="black",fg_color="white",border_color="grey",
                                text_color="black",placeholder_text="Enter Topic",placeholder_text_color="grey",
                                state=tkinter.NORMAL)
    topic_entry.place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)

    language_select = customtkinter.CTkComboBox(master=musnart_guest_app,values=["Language","English"],
                                            width=110,height=30,corner_radius=10,border_width=1,bg_color="black",
                                            fg_color="black",border_color="grey",button_color="grey",
                                            button_hover_color="cyan")
    language_select.place(relx=0.72,rely=0.4,anchor=tkinter.CENTER)

    def topicSubmitPressed():
        print("Topic Submit Pressed")
        searchLang = language_select.get()
        if(searchLang == "Language"):
            summary_display_guest.configure(text="Choose Language")
        elif(searchLang == "English"):
            wikipedia.set_lang("en")
            displaySearchResult()
        #elif(searchLang == "Hindi"):
        #    wikipedia.set_lang("hi")
        #    displaySearchResult()``

    def displaySearchResult():
        searchResult = wikipedia.summary("{}".format(topic_entry.get()),sentences=10)
        print(searchResult)
        summary_display_guest.configure(text=searchResult)

    topic_submit_button = customtkinter.CTkButton(master=musnart_guest_app,width=400,height=35,
                                corner_radius=5,border_width=1,border_spacing=1,bg_color="black",
                                fg_color="green",hover_color="lightgreen",border_color="white",
                                text_color="black",text_color_disabled="grey",text="SUBMIT",
                                state=tkinter.NORMAL,command=topicSubmitPressed)
    topic_submit_button.place(relx=0.5,rely=0.47,anchor=tkinter.CENTER)

    musnart_guest_app.mainloop()

guest_button = customtkinter.CTkButton(master=musnart_app,width=170,height=40,corner_radius=0,
                                border_width=0,border_spacing=1,bg_color="yellow",fg_color="yellow",
                                hover_color="white",border_color="white",text_color="black",
                                command=guestPressed,text="GUEST",font=("Poppins",15))
guest_button.place(relx=0.761,rely=0.69,anchor=tkinter.CENTER)

musnart_app.mainloop()