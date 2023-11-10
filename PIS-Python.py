import os
import shutil
import tempfile
import requests
import webbrowser
import re
import random
import time
import contextlib
import tkinter as tk
from tkinter import messagebox, filedialog
import wave
import pygame
from playsound import playsound
import keyboard
import configparser
from os import getenv


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
temp_dir = tempfile.mkdtemp()

current_version = '1.1'
user = 'bravuralion'
repo = 'TD2-Driver-PIS-SYSTEM'
api_url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"

# Azure Voice Presets
voices = {
    'EN': ('en-US-JessaNeural', 'en-US'),
    'PL': ('pl-PL-AgnieszkaNeural', 'pl-PL'),
    'DE': ('de-DE-KatjaNeural', 'de-DE')
}    
def load_categories_names():
    with open(categories_config_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Ignorieren von Leerzeilen und Kommentaren
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
        response.raise_for_status()  # Stellt sicher, dass die Anfrage erfolgreich war
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

def on_closing():
    try:
        shutil.rmtree(temp_dir)
    except OSError as e:
        print(f"Error when deleting the temporary folder {temp_dir}: {e}")
    keyboard.unhook_all_hotkeys()    
    root.destroy()

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

def on_hotkey_exit_left():
    announce_exit('left')

def on_hotkey_exit_right():
    announce_exit('right')

def on_hotkey_next_stop_only():
    announce_exit('none')

def register_hotkeys():
    try:
        hotkey_config = config['Hotkey']
        keyboard.add_hotkey(hotkey_config['Left'], on_hotkey_exit_left)
        keyboard.add_hotkey(hotkey_config['Right'], on_hotkey_exit_right)
        keyboard.add_hotkey(hotkey_config['None'], on_hotkey_next_stop_only)
    except KeyError as e:
        messagebox.showerror("Hotkey Error", f"Ein Fehler ist aufgetreten: {e}. Überprüfen Sie, ob der korrekte Schlüssel in der Konfigurationsdatei vorhanden ist.")

register_hotkeys()

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

def load_schedule():
    try:
        response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList")
        response.raise_for_status()
        trains_response = response.json()
        
        selected_train_no = int(train_number_textbox.get())
        selected_train = next((train for train in trains_response if train['trainNo'] == selected_train_no), None)

        if not selected_train:
            messagebox.showinfo("Information", "Train number not found.")
            return
        stations_listbox.delete(0, tk.END)
        stations_listbox.insert(tk.END, selected_train['timetable']['stopList'][0]['stopNameRAW'])

        for stop in selected_train['timetable']['stopList'][1:-1]:
            if 'ph' in stop['stopType'].lower():
                stations_listbox.insert(tk.END, stop['stopNameRAW'])

        if selected_train['timetable']['stopList']:
            stations_listbox.insert(tk.END, selected_train['timetable']['stopList'][-1]['stopNameRAW'])

    except requests.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def announce_exit(exit_side):
    selected_language = language_combobox.get()
    language_key = selected_language[:2].upper()  # "German" -> "DE", "English" -> "EN", "Polish" -> "PL"

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
        response_blacklist = requests.get(blacklist_url)
        if response_blacklist.status_code != 200:
            return        
        blacklist = response_blacklist.text.strip().lower().split('\n')            
        if driver_name in blacklist:
            messagebox.showerror("Blacklist", f"You are on the blacklist for this program. Contact the author for more information.")
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
        convert_text_to_speech(final_announcement, selected_language) 

        if not is_last_station:
            stations_listbox.select_clear(current_index)
            stations_listbox.select_set(current_index + 1)

    except requests.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def play_special_announcement(announcement_number):
    try:
        special_announcement_key = str(announcement_number)
        announcement_text = config['Special'][special_announcement_key]
        selected_language = language_combobox.get()
        convert_text_to_speech(announcement_text, selected_language)
    except KeyError as e:
        messagebox.showerror("Fehler", f"An error has occurred: {e}. Check whether the correct key is present in the configuration file.")

def convert_text_to_speech(text, language):
    if gong_sound_path:
        play_sound(gong_sound_path)
    
    voice_name, lang = voices[language]
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm',
        'User-Agent': 'PythonApp'
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

root = tk.Tk()
root.title('On-board Passenger Information System')
root.geometry('480x400')

train_number_textbox = tk.Entry(root)
train_number_textbox.place(x=10, y=10, width=460, height=20)

load_schedule_button = tk.Button(root, text='Load Schedule', command=load_schedule)
load_schedule_button.place(x=10, y=40, width=460, height=30)

load_schedule_button = tk.Button(root, text='Load Schedule', command=load_schedule)
load_schedule_button.place(x=10, y=40, width=460, height=30)

stations_listbox = tk.Listbox(root)
stations_listbox.place(x=10, y=80, width=460, height=160)

exit_right_button = tk.Button(root, text='Exit right', command=lambda: announce_exit('right'))
exit_right_button.place(x=170, y=250, width=150, height=40)

exit_left_button = tk.Button(root, text='Exit left', command=lambda: announce_exit('left'))
exit_left_button.place(x=10, y=250, width=150, height=40)

exit_none_button = tk.Button(root, text='Next Stop only', command=lambda: announce_exit('none'))
exit_none_button.place(x=330, y=250, width=140, height=40)

gong_button = tk.Button(root, text='Select Gong (.WAV)', command=select_gong)
gong_button.place(x=10, y=300, width=460, height=20)

special_buttons = []
for i in range(1, 6):
    special_button = tk.Button(root, text=f'S{i}',
                               command=lambda i=i: play_special_announcement(i))
    special_button.place(x=10 + 85 * (i-1), y=360, width=75, height=23)
    special_buttons.append(special_button)

language_combobox = tk.StringVar(root)
language_combobox.set('DE')  # default value
language_options = ['DE', 'EN', 'PL']

language_dropdown = tk.OptionMenu(root, language_combobox, *language_options)
language_dropdown.place(x=10, y=330, width=460, height=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
keyboard.unhook_all_hotkeys()