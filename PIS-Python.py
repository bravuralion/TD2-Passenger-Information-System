# -*- coding: utf-8 -*-
import clipboard
import os
import shutil
import tempfile
import requests
import webbrowser
import re
import random
import time
import threading
import contextlib
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import wave
import pygame
from playsound import playsound
import configparser
from os import getenv
from global_hotkeys import *
from PIL import Image, ImageTk
import datetime
from tkinter import END
import unidecode
import pyperclip
import zipfile
from io import BytesIO
from pypresence import Presence

def clean_string(s):
    return unidecode.unidecode(s)

api_key = ''
resource_region = 'westeurope'
tts_url = f'https://{resource_region}.tts.speech.microsoft.com/cognitiveservices/v1'
blacklist_url = "https://cloud.furry.fm/index.php/s/XBoYMxZXsmweK8D/download/TD2-PIS.txt"
config_file_path = 'config/config.cfg'
config = configparser.ConfigParser()
categories_config_path = 'config/categories.cfg'
categories_names = {}
wav_output_path = f"{getenv('APPDATA')}\\TD2-AN.wav"
gong_sound_path = None
CLIENT_ID = ''  
discord_rpc = Presence(CLIENT_ID)

pygame.mixer.init()
temp_dir = tempfile.mkdtemp()

global train_number_textbox, stations_listbox, language_combobox

current_version = '2.0'
user = 'bravuralion'
repo = 'TD2-Driver-PIS-SYSTEM'
api_url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"

# Azure Voice Presets
voices = {
    'EN': ('en-US-JessaNeural', 'en-US'),
    'PL': ('pl-PL-AgnieszkaNeural', 'pl-PL'),
    'DE': ('de-DE-KatjaNeural', 'de-DE'),
    'PT': ('pt-PT-RaquelNeural', 'pt-PT')
}

def connect_discord():
    discord_rpc.connect()

def update_discord_status(mode, train_number=None, end_station=None):
    state = "TD2 Driver Mode, No Train loaded" if mode == "Driver Mode" else "Dispatcher Mode"
    details = f"Driving Train: {train_number} to {end_station}" if train_number and end_station else "Idle"

    if details:  # Stellen Sie sicher, dass 'details' nicht leer ist
        discord_rpc.update(state=state, details=details)

def close_discord():
    discord_rpc.close()

def start_main_window(operation_mode):
    if operation_mode == "Driver Mode":
        start_window.withdraw()
        create_driver_window()
    elif operation_mode == "Dispatcher Mode":
        start_window.withdraw()
        create_dispatcher_window()
        pass
def register_hotkeys(exit_left_func, exit_right_func, next_stop_only_func):
    hotkeys = [
        (config['Hotkey']['Left'], None, exit_left_func),
        (config['Hotkey']['Right'], None, exit_right_func),
        (config['Hotkey']['None'], None, next_stop_only_func),
    ]

    for hotkey, modifiers, callback in hotkeys:
        try:
            register_hotkey(hotkey, modifiers, callback)
        except KeyError as e:
            messagebox.showerror("Hotkey Error", f"Ein Fehler ist aufgetreten: {e}. Überprüfen Sie, ob der korrekte Schlüssel in der Konfigurationsdatei vorhanden ist.")
    start_checking_hotkeys()

def create_start_window():
    global start_window
    start_window = tk.Tk()
    start_window.title("TD2 Passenger Information System")
    start_window.iconbitmap("res/favicon.ico")
    
    ws = start_window.winfo_screenwidth()
    hs = start_window.winfo_screenheight()
    x = (ws/2) - (400/2)
    y = (hs/2) - (400/2)
    start_window.geometry('%dx%d+%d+%d' % (400, 460, x, y))

    with zipfile.ZipFile('res/ressources.pak', 'r') as z:
        with z.open('logo.png') as logo_file:
            logo_image = Image.open(BytesIO(logo_file.read()))
            logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(start_window, image=logo_photo)
    logo_label.image = logo_photo  
    logo_label.pack()

    operation_mode_label = tk.Label(start_window, text="Operation Mode")
    operation_mode_label.pack()
    operation_mode = ttk.Combobox(start_window, values=["Driver Mode", "Dispatcher Mode"])
    operation_mode.pack()
    operation_mode.set("Driver Mode")

    start_button = tk.Button(start_window, text="Start", command=lambda: start_main_window(operation_mode.get()))
    start_button.pack()

    start_window.mainloop()

def get_station_names():
    response = requests.get("https://stacjownik.spythere.pl/api/getSceneries")
    if response.status_code == 200:
        station_data = response.json()
        station_names = [station['name'] for station in station_data]
        return station_names
    else:
        print("Error when retrieving the stations: HTTP status", response.status_code)
        return []

def load_categories_names():
    with open(categories_config_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                pair = line.split('=', 1)
                if len(pair) == 2:
                    key = pair[0].strip()
                    value = pair[1].strip()
                    categories_names[key] = value
load_categories_names()

def check_for_update():
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        latest_release = response.json()
        latest_version = latest_release['tag_name']
        download_url = latest_release['assets'][0]['browser_download_url']
        
        if current_version != latest_version:
            message = f"A new version ({latest_version}) is available. Would you like to download the update now?"
            title = "Update available"
            if messagebox.askyesno(title, message):
                webbrowser.open(download_url)
    except requests.RequestException as e:
        messagebox.showerror("Update Check Failed", f"An error occurred while checking for updates: {e}")
check_for_update()

def play_sound(wav_path):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    pygame.mixer.music.load(wav_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.delay(200)

def load_config():
    global config_file_path 
    if not os.path.exists(config_file_path):
        messagebox.showwarning("File Not Found", "The configuration file 'config.cfg' was not found. You will be prompted to select the file in the next step.")
        config_file_path = filedialog.askopenfilename(
            title="Select config file",
            initialdir=".",
            filetypes=(("Config files", "*.cfg"), ("All files", "*.*"))
        )        
        if config_file_path:
            config.read(config_file_path, encoding='utf-8')
        else:
            print("Configuration file was not specified. The script will exit.")
            exit()
    else:
        config.read(config_file_path, encoding='utf-8')
load_config()

def get_wav_duration(wav_path):
    with contextlib.closing(wave.open(wav_path, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration_seconds = frames / float(rate)
        return duration_seconds
    
def select_gong():
    global gong_sound_path
    gong_sound_path = filedialog.askopenfilename(
        title="Select a WAV File",
        filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*"))
    )

def load_schedule(train_number_textbox, stations_listbox, blacklist_url, messagebox):
    try:
        response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList")
        response.raise_for_status()
        trains_response = response.json()
        
        train_number = train_number_textbox.get().strip()
        if not train_number:
            messagebox.showinfo("Information", "Please enter a train number.")
            return
        
        selected_train_no = int(train_number)
        selected_train = next((train for train in trains_response if train['trainNo'] == selected_train_no), None)
        end_station = selected_train['timetable']['stopList'][-1]['stopNameRAW']
        update_discord_status("Driver Mode", train_number, end_station)
        if not selected_train:
            messagebox.showinfo("Information", "Train number not found.")
            return

        driver_name = selected_train.get('driverName', '').strip().lower()
        response_blacklist = requests.get(blacklist_url)
        blacklist = response_blacklist.text.strip().lower().split('\n') if response_blacklist.status_code == 200 else []
        
        if driver_name in blacklist:
            messagebox.showerror("Blacklist", "The driver of this train is on the blacklist of this program.")
            return
        
        stations_listbox.delete(0, tk.END)
        for stop in selected_train['timetable']['stopList']:
            if 'ph' in stop['stopType'].lower() or stop == selected_train['timetable']['stopList'][0] or stop == selected_train['timetable']['stopList'][-1]:
                stations_listbox.insert(tk.END, stop['stopNameRAW'])

    except requests.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def announce_exit(exit_side,language_combobox,train_number_textbox,stations_listbox):
    selected_language = language_combobox.get()
    language_key = selected_language[:2].upper()
    selected_train_no = train_number_textbox.get()
    
    try:
        response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList")
        response.raise_for_status()
        trains_response = response.json()
        
        selected_train = next((train for train in trains_response if str(train['trainNo']) == selected_train_no), None)
        driver_name = selected_train.get('driverName', '').strip().lower()
        if not selected_train:
            messagebox.showinfo("Information", "Train number not found.")
            return
        
        category_key = selected_train['timetable']['category']
        category_name = categories_names.get(category_key, category_key)

        current_index = stations_listbox.curselection()[0]
        is_first_station = current_index == 0
        is_last_station = current_index == len(stations_listbox.get(0, tk.END)) - 1
        station_name = stations_listbox.get(current_index).rstrip(' po.')
        last_station_name = stations_listbox.get(tk.END).rstrip(' po.')

        base_announcement = ""
        exit_announcement = ""
        additional_announcement = ""
        final_announcement = ""

        if is_first_station:
            base_announcement = config['Start_Station'][f'01_{language_key}'] + " " + \
                                category_name + " " + \
                                config['Start_Station'][f'02_{language_key}'] + " " + \
                                last_station_name + \
                                config['Start_Station'][f'03_{language_key}']
        else:
            base_announcement = config['next_station'][language_key] + " " + station_name
        
        if exit_side == "left" and not is_first_station:
            exit_announcement = config['exit_left'][language_key]
        elif exit_side == "right" and not is_first_station:
            exit_announcement = config['exit_right'][language_key]

        if not is_last_station and not is_first_station and random.randint(1, 6) <= 2:
            additional_announcement = config['additional_Announcement'][language_key]

        final_announcement = f"{base_announcement} {exit_announcement} {additional_announcement}".strip()
        
        if is_last_station:
            final_announcement += config['last_station_final_stop'][language_key]

        print(final_announcement)  #Debugging
        start_convert_text_to_speech_thread(final_announcement, selected_language)

        if not is_last_station:
            stations_listbox.select_clear(current_index)
            stations_listbox.select_set(current_index + 1)

    except requests.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def play_special_announcement(announcement_number,language_combobox):
    try:
        special_announcement_key = str(announcement_number)
        announcement_text = config['Special'][special_announcement_key]
        selected_language = language_combobox.get()
        start_convert_text_to_speech_thread(announcement_text, selected_language)
    except KeyError as e:
        messagebox.showerror("Fehler", f"An error has occurred: {e}. Check whether the correct key is present in the configuration file.")

def start_convert_text_to_speech_thread(text, language):
    thread = threading.Thread(target=convert_text_to_speech, args=(text, language))
    thread.daemon = True
    thread.start()

def convert_text_to_speech(text, language):
    if gong_sound_path:
        play_sound(gong_sound_path)
    
    voice_name, lang = voices[language]
    print(text)
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
        "User-Agent": "PythonApp"
    }
    body = f"""
    <speak version='1.0' xml:lang='{lang}'>
        <voice xml:lang='{lang}' xml:gender='Female' name='{voice_name}'>
            {text}
        </voice>
    </speak>
    """
    
    response = requests.post(tts_url, headers=headers, data=body.encode('utf-8'))
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav', dir=temp_dir) as audio_file:
            temp_path = audio_file.name
            audio_file.write(response.content)

        play_sound(temp_path)
    else:
        messagebox.showerror("Error", f"Error with the text-to-speech service: {response.status_code}\n{text}")

def adjust_volume(value):
    new_volume = float(value) / 100
    pygame.mixer.music.set_volume(new_volume)

def create_driver_window():
    def on_closing():
        try:
            shutil.rmtree(temp_dir)
        except OSError as e:
            print(f"Error when deleting the temporary folder {temp_dir}: {e}")
        stop_checking_hotkeys()
        if 'start_window' in globals():
            start_window.destroy()
        if 'driver_w' in globals():
            driver_w.destroy()
        if 'dispatcher_w' in globals():
            dispatcher_w.destroy()
        #close_discord()
        pygame.quit()
        os._exit(0)
    #connect_discord()  # Verbinden mit Discord beim Starten des Fahrermodus
    #update_discord_status("Driver Mode")
    driver_w = tk.Toplevel()
    driver_w.title('On-board Passenger Information System')
    driver_w.geometry('480x430')

    train_number_textbox = tk.Entry(driver_w)
    train_number_textbox.place(x=10, y=10, width=460, height=20)

    stations_listbox = tk.Listbox(driver_w)
    stations_listbox.place(x=10, y=80, width=460, height=160)

    load_schedule_button = tk.Button(driver_w, text='Load Schedule', command=lambda: load_schedule(train_number_textbox, stations_listbox, blacklist_url, messagebox))
    load_schedule_button.place(x=10, y=40, width=460, height=30)

    exit_right_button = tk.Button(driver_w, text='Exit right', command=lambda: announce_exit('right',language_combobox,train_number_textbox,stations_listbox))
    exit_right_button.place(x=170, y=250, width=150, height=40)

    exit_left_button = tk.Button(driver_w, text='Exit left', command=lambda: announce_exit('left',language_combobox,train_number_textbox,stations_listbox))
    exit_left_button.place(x=10, y=250, width=150, height=40)

    exit_none_button = tk.Button(driver_w, text='Next Stop only', command=lambda: announce_exit('none',language_combobox,train_number_textbox,stations_listbox))
    exit_none_button.place(x=330, y=250, width=140, height=40)

    gong_button = tk.Button(driver_w, text='Select Gong (.WAV)', command=select_gong)
    gong_button.place(x=10, y=300, width=460, height=20)

    special_buttons = []
    for i in range(1, 6):
        special_button = tk.Button(driver_w, text=f'S{i}',
                                command=lambda i=i: play_special_announcement(i,language_combobox))
        special_button.place(x=10 + 85 * (i-1), y=360, width=75, height=23)
        special_buttons.append(special_button)

    volume_label = tk.Label(driver_w, text='Volume:')
    volume_label.place(x=10, y=410) 

    volume_control = tk.Scale(driver_w, from_=0, to=100, orient='horizontal', command=adjust_volume)
    volume_control.set(50) 
    volume_control.place(x=60, y=390, width=140, height=50)

    donate_button = tk.Button(driver_w, text='Donate', command=lambda: webbrowser.open("https://paypal.me/furryfm"))
    donate_button.place(x=350, y=405, width=75, height=20)

    language_combobox = tk.StringVar(driver_w)
    language_combobox.set('DE')
    language_options = ['DE', 'EN', 'PL', 'PT']

    language_dropdown = tk.OptionMenu(driver_w, language_combobox, *language_options)
    language_dropdown.place(x=10, y=330, width=460, height=20)

    driver_w.protocol("WM_DELETE_WINDOW", on_closing)
    def on_hotkey_exit_left():
        if train_number_textbox and stations_listbox and language_combobox:
            announce_exit('left', language_combobox, train_number_textbox, stations_listbox)
    def on_hotkey_exit_right():
        if train_number_textbox and stations_listbox and language_combobox:
            announce_exit('right', language_combobox, train_number_textbox, stations_listbox)
    def on_hotkey_next_stop_only():
        if train_number_textbox and stations_listbox and language_combobox:
            announce_exit('none', language_combobox, train_number_textbox, stations_listbox)
    register_hotkeys(on_hotkey_exit_left, on_hotkey_exit_right, on_hotkey_next_stop_only)

    pass

def DP_add_to_log(log_console, message):
    """
    Adds a timestamp message to the log console widget.
    
    Args:
    log_console (tk.Text): The text widget that serves as the log console.
    message (str): The message to be logged.
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"{timestamp}: {message}\n"
    log_console.insert(END, log_entry)
    log_console.see(END)

def DP_update_button_click(station_dropdown, train_dropdown, log_console):
    selected_station_name = station_dropdown.get()
    if selected_station_name:
        try:
            trains_response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList").json()
            relevant_trains = [train for train in trains_response if train['currentStationName'] == selected_station_name]
            train_numbers = [train['trainNo'] for train in relevant_trains]
            
            train_dropdown['values'] = train_numbers
            train_dropdown.set('')
            DP_add_to_log(log_console, "Updating Train List")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"An error occurred while updating the train list: {e}")

def DP_generate_passing(track, gong_sound_path, audio_checkbox_var, language_combobox, log_console):
    combined_announcement = ""
    announcements = {
        "EN": f"*STATION ANNOUNCEMENT* Attention at track {track}, A train is passing through. Please stand back.",
        "PL": f"*OGŁOSZENIE STACYJNE* Uwaga! Na tor numer {track} wjedzie pociąg bez zatrzymania. Prosimy zachować ostrożność i nie zbliżać się do krawędzi peronu.",
        "DE": f"*Bahnhofsdurchsage* Achtung am Gleis {track}, Zugdurchfahrt. Zurückbleiben bitte."
    }

    selected_language = language_combobox.get()
    selected_languages = [selected_language] 

    for lang_code in selected_languages:
        announcement = announcements[lang_code].format(track=track)
        combined_announcement += announcement + " "              
        announcement_for_speech = re.sub(r'\*.*?\*', '', announcement)
            
        if audio_checkbox_var.get():  
            DP_add_to_log(log_console, f"Generating Audio announcement for {lang_code}.")
            start_convert_text_to_speech_thread(announcement_for_speech, lang_code)

        clipboard.copy(combined_announcement)
        messagebox.showinfo("Announcement", f"The following text has been copied to your clipboard:\n\n{combined_announcement}")
        DP_add_to_log(log_console,"Job complete")

def convert_to_proper_case(name):
    return name.title()

def convert_time_for_audio(time_str):
    """Konvertiert die Zeit im Format HH:MM für die deutsche Audioansage."""
    try:
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%H Uhr %M')  # z.B. "15:30" zu "15 Uhr 30"
    except ValueError:
        return time_str  # Bei Fehler, zurückgeben des Original-Strings

def generate_announcements(selected_languages, categories_names, selected_train, start_station, end_station, arrival_time, departure_time, track_dropdown, delay_minutes, stop_details):
    announcements = {}
    for lang in selected_languages:
        if lang == 'EN':
            if delay_minutes > 5:
                text = f"*STATION ANNOUNCEMENT* The {categories_names[selected_train['timetable']['category']]} from station {start_station} to station {end_station}, scheduled arrival {arrival_time.strftime('%H:%M')}, will arrive approximately {delay_minutes} minutes late at platform {track_dropdown.get()}. The delay is subject to change. Please pay attention to announcements."
                audio = f"The {categories_names[selected_train['timetable']['category']]} from station {start_station} to station {end_station}, scheduled arrival {arrival_time.strftime('%H:%M')}, will arrive approximately {delay_minutes} minutes late at platform {track_dropdown.get()}. The delay is subject to change. Please pay attention to announcements."
            elif stop_details.get('terminatesHere'):
                text = f"*STATION ANNOUNCEMENT* Attention at track {track_dropdown.get()}, the {categories_names[selected_train['timetable']['category']]} from {start_station} is arriving. This train ends here, please do not board the train."
                audio = f"Attention at track {track_dropdown.get()}, the {categories_names[selected_train['timetable']['category']]} from {start_station} is arriving. This train ends here, please do not board the train."
            else:
                text = f"*STATION ANNOUNCEMENT* Attention at track {track_dropdown.get()}, The {categories_names[selected_train['timetable']['category']]} from {start_station} to {end_station} is arriving. The planned Departure is {departure_time.strftime('%H:%M')}."
                audio = f"Attention at track {track_dropdown.get()}, The {categories_names[selected_train['timetable']['category']]} from {start_station} to {end_station} is arriving. The planned Departure is {departure_time.strftime('%H:%M')}."
            announcements['EN'] = {'text': text, 'audio': audio}
        elif lang == 'DE':
            if delay_minutes > 5:
                arrival_time_str = convert_time_for_audio(arrival_time.strftime('%H:%M'))
                text = f"*Bahnhofsdurchsage* Der {categories_names[selected_train['timetable']['category']]} von {start_station} nach {end_station}, geplante Ankunft {arrival_time.strftime('%H:%M')} , wird voraussichtlich mit einer Verspätung von {delay_minutes} Minuten auf Gleis {track_dropdown.get()} eintreffen. Bitte beachten Sie die Ansagen."
                audio = f"Der {categories_names[selected_train['timetable']['category']]} von {start_station} nach {end_station}, geplante Ankunft {arrival_time_str}, wird voraussichtlich mit einer Verspätung von {delay_minutes} Minuten auf Gleis {track_dropdown.get()} eintreffen. Bitte beachten Sie die Ansagen."
            elif stop_details.get('terminatesHere'):
                text = f"*Bahnhofsdurchsage* Achtung am Gleis {track_dropdown.get()}, der {categories_names[selected_train['timetable']['category']]} von {start_station} fährt ein. Dieser Zug endet hier, bitte nicht einsteigen."
                audio = f"Achtung am Gleis {track_dropdown.get()}, der {categories_names[selected_train['timetable']['category']]} von {start_station} fährt ein. Dieser Zug endet hier, bitte nicht einsteigen."
            else:
                departure_time_str = convert_time_for_audio(departure_time.strftime('%H:%M'))
                text = f"*Bahnhofsdurchsage* Achtung am Gleis {track_dropdown.get()}, Der {categories_names[selected_train['timetable']['category']]} von {start_station} nach {end_station} fährt ein. Die planmässige Abfahrt ist um {departure_time.strftime('%H:%M')} ."
                audio = f"Achtung am Gleis {track_dropdown.get()}, Der {categories_names[selected_train['timetable']['category']]} von {start_station} nach {end_station} fährt ein. Die planmässige Abfahrt ist um {departure_time_str} ."
            announcements['DE'] = {'text': text, 'audio': audio}
        elif lang == 'PL':
            if delay_minutes > 5:
                text = f"*OGŁOSZENIE STACYJNE* Uwaga! Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station} do stacji {end_station}, planowy przyjazd {arrival_time.strftime('%H:%M')}, przyjedzie z opóźnieniem około {delay_minutes} minut na tor {track_dropdown.get()}. Opóźnienie może ulec zmianie. Prosimy o zwracanie uwagi na komunikaty."
                audio = f"Uwaga! Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station} do stacji {end_station}, planowy przyjazd {arrival_time.strftime('%H:%M')}, przyjedzie z opóźnieniem około {delay_minutes} minut na tor {track_dropdown.get()}. Opóźnienie może ulec zmianie. Prosimy o zwracanie uwagi na komunikaty."
            elif stop_details.get('terminatesHere'):
                text = f"*OGŁOSZENIE STACYJNE* Uwaga na tor numer {track_dropdown.get()}, przyjedzie Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station}. Pociąg kończy bieg. Prosimy zachować ostrożność i nie zbliżać się do krawędzi peronu."
                audio = f"Uwaga na tor numer {track_dropdown.get()}, przyjedzie Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station}. Pociąg kończy bieg. Prosimy zachować ostrożność i nie zbliżać się do krawędzi peronu."
            else:
                text = f"*OGŁOSZENIE STACYJNE* Uwaga! Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station} do stacji {end_station} wjedzie na tor numer {track_dropdown.get()}, Planowy odjazd pociągu o godzinie {departure_time.strftime('%H:%M')}."
                audio = f"Uwaga! Pociąg {categories_names[selected_train['timetable']['category']]} ze stacji {start_station} do stacji {end_station} wjedzie na tor numer {track_dropdown.get()}, Planowy odjazd pociągu o godzinie {departure_time.strftime('%H:%M')}."
            announcements['PL'] = {'text': text, 'audio': audio}
    return announcements

def generate_button_click(station_dropdown, train_dropdown, track_dropdown, categories_names, log_console, language_combobox,audio_checkbox_var):
    selected_train_no = train_dropdown.get().strip()
    selected_train_no = int(selected_train_no)

    trains_response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList").json()
    selected_train = next((train for train in trains_response if train['trainNo'] == selected_train_no), None)
    selected_station_name = station_dropdown.get()
    selected_track = track_dropdown.get()
    stop_list = selected_train['timetable']['stopList']
    if selected_station_name and selected_train_no and selected_track:
        stop_details = next((stop for stop in stop_list if selected_station_name in stop['stopNameRAW'] and stop.get('mainStop')), None)

        if not stop_details:
            main_station_name = selected_station_name.split(' ')[0]
            stop_details = next((stop for stop in stop_list if main_station_name in stop['stopNameRAW'] and stop.get('mainStop')), None)

        if not stop_details:
            main_station_name = selected_station_name.split(' ')[-1]
            stop_details = next((stop for stop in stop_list if main_station_name in stop['stopNameRAW'] and stop.get('mainStop')), None)
        
        print("stop_details:")
        print(stop_details)

        if stop_details and not stop_details.get('stopType', '').strip() in ['', 'pt', 'pm', 'pt,pm']:
            start_station = selected_train['timetable']['stopList'][0]['stopNameRAW']
            end_station = selected_train['timetable']['stopList'][-1]['stopNameRAW']
            departure_timestamp = stop_details['departureTimestamp']
            arrival_timestamp = stop_details['arrivalTimestamp']

            departure_time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=departure_timestamp / 1000)
            arrival_time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=arrival_timestamp / 1000)

            delay_minutes = stop_details['departureDelay']
            selected_language = language_combobox.get() 
            selected_languages = [selected_language]

            announcements = generate_announcements(selected_languages, categories_names, selected_train, start_station, end_station, arrival_time, departure_time, track_dropdown, delay_minutes, stop_details)

            for lang in announcements:
                pyperclip.copy(announcements[lang]['text'])                
                start_convert_text_to_speech_thread(announcements[lang]['audio'], lang)
                messagebox.showinfo("Announcement", f"The following text has been copied to your clipboard:\n\n{announcements[lang]['text']}")

        else:
            DP_add_to_log(log_console, "No Stop Details found, Generating Train Passing Version")
            DP_generate_passing(selected_track,gong_sound_path,audio_checkbox_var,language_combobox,log_console)

def create_dispatcher_window():
    def on_closing():
        try:
            shutil.rmtree(temp_dir)
        except OSError as e:
            print(f"Error when deleting the temporary folder {temp_dir}: {e}")
        stop_checking_hotkeys()
        if 'start_window' in globals():
            start_window.destroy()
        if 'driver_w' in globals():
            driver_w.destroy()
        if 'dispatcher_w' in globals():
            dispatcher_w.destroy()
        pygame.quit()
        os._exit(0)
    dispatcher_w = tk.Toplevel()
    dispatcher_w.title("TD2 Station Announcement Tool")
    dispatcher_w.geometry("570x257")
    dispatcher_w.resizable(False, False)

    settings_group = tk.LabelFrame(dispatcher_w, text="Settings", width=177, height=121)
    settings_group.place(x=381, y=10)
    train_passing_group = tk.LabelFrame(dispatcher_w, text="Train Passing at", width=177, height=79)
    train_passing_group.place(x=381, y=166)

    tk.Label(dispatcher_w, text="Track").place(x=9, y=103)
    tk.Label(dispatcher_w, text="Train").place(x=9, y=57)
    tk.Label(dispatcher_w, text="Station").place(x=9, y=10)
    tk.Label(dispatcher_w, text="Language").place(x=192, y=10)

    station_Dropdown = ttk.Combobox(dispatcher_w)
    station_Dropdown.place(x=12, y=29, width=162)

    train_Dropdown = ttk.Combobox(dispatcher_w)
    train_Dropdown.place(x=12, y=79, width=162)

    trackDropdown = ttk.Combobox(dispatcher_w)
    trackDropdown.place(x=12, y=122, width=162)

    Auto_Update_Checkbox = tk.Checkbutton(settings_group, text="Auto Update", state=tk.DISABLED)
    Auto_Update_Checkbox.place(x=6, y=0)

    Announce_Delays_Checkbox = tk.Checkbutton(settings_group, text="Announce Delays", state=tk.DISABLED)
    Announce_Delays_Checkbox.place(x=6, y=22)

    audio_checkbox_var = tk.IntVar(value=0)
    audio_checkbox = tk.Checkbutton(settings_group, text="Play Audio", variable=audio_checkbox_var)
    audio_checkbox.place(x=6, y=42)
    gong_button = tk.Button(settings_group, text="Station Gong", command=select_gong)
    gong_button.place(x=6, y=62, width=110, height=23)

    language_combobox_var = tk.StringVar()
    language_combobox = ttk.Combobox(dispatcher_w, textvariable=language_combobox_var, state='readonly')
    language_combobox['values'] = ['EN', 'PL', 'DE']
    language_combobox.set('EN')  # Standardwert setzen
    language_combobox.place(x=192, y=29, width=147, height=23)

    Update_Trains_button = tk.Button(dispatcher_w, text="Update Trains", command=lambda: DP_update_button_click(station_Dropdown,train_Dropdown,log_console))
    Update_Trains_button.place(x=192, y=59, width=147, height=23)  
    Gernate_Announcement_Button = tk.Button(dispatcher_w, text="Generate Announcement", command=lambda: generate_button_click(station_Dropdown, train_Dropdown, trackDropdown, categories_names, log_console,language_combobox,audio_checkbox_var))
    Gernate_Announcement_Button.place(x=192, y=89, width=147, height=23)

    donate_button = tk.Button(dispatcher_w, text='Donate', command=lambda: webbrowser.open("https://paypal.me/furryfm"))
    donate_button.place(x=400, y=138, width=147, height=23)  

    tk.Button(train_passing_group, text="1", command=lambda: DP_generate_passing('1', gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=6, y=0, width=28, height=23)
    tk.Button(train_passing_group, text="2", command=lambda: DP_generate_passing("2", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=40, y=0, width=28, height=23)
    tk.Button(train_passing_group, text="3", command=lambda: DP_generate_passing("3", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=74, y=0, width=28, height=23)
    tk.Button(train_passing_group, text="4", command=lambda: DP_generate_passing("4", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=108, y=0, width=28, height=23)
    tk.Button(train_passing_group, text="5", command=lambda: DP_generate_passing("5", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=142, y=0, width=28, height=23)
    tk.Button(train_passing_group, text="6", command=lambda: DP_generate_passing("6", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=6, y=30, width=28, height=23)
    tk.Button(train_passing_group, text="7", command=lambda: DP_generate_passing("7", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=40, y=30, width=28, height=23)
    tk.Button(train_passing_group, text="8", command=lambda: DP_generate_passing("8", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=74, y=30, width=28, height=23)
    tk.Button(train_passing_group, text="9", command=lambda: DP_generate_passing("9", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=108, y=30, width=28, height=23)
    tk.Button(train_passing_group, text="10", command=lambda: DP_generate_passing("10", gong_sound_path, audio_checkbox_var, language_combobox, log_console)).place(x=142, y=30, width=28, height=23)

    log_console = tk.Text(dispatcher_w, wrap='word', height=5, width=40)
    log_console.place(x=12, y=166, width=363, height=79)
    
    for i in range(1, 601):
        trackDropdown['values'] = (*trackDropdown['values'], str(i))
    response = requests.get("https://stacjownik.spythere.pl/api/getSceneries")
    if response.status_code == 200:  
        stationNames = [scenery['name'] for scenery in response.json()]  
        stationNames.sort()
        station_Dropdown['values'] = stationNames

    dispatcher_w.protocol("WM_DELETE_WINDOW", on_closing)
    pass
create_start_window()

