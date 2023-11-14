# -*- coding: utf-8 -*-
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
import requests


#Global Vars
gong_sound_path = None

def add_to_log(log_console, message):
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

def check_for_update(current_version, api_url):
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

def load_categories_names(categories_config_path):
    categories_names = {}
    with open(categories_config_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                categories_names[key.strip()] = value.strip()
    return categories_names

def load_schedule():
    try:
        response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList")
        response.raise_for_status()
        trains_response = response.json()
        
        selected_train_no = int(train_number_textbox.get())
        selected_train = next((train for train in trains_response if train['trainNo'] == selected_train_no), None)
        driver_name = selected_train.get('driverName', '').strip().lower()
        response_blacklist = requests.get(blacklist_url)
        if response_blacklist.status_code != 200:
            return        
        blacklist = response_blacklist.text.strip().lower().split('\n')            
        if not selected_train:
            messagebox.showinfo("Information", "Train number not found.")
            return
        if driver_name in blacklist:
            messagebox.showerror("Blacklist", f"The driver of this train is on the blacklist of this program. Contact the author of this app if you need help.")
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

def update_button_click(station_dropdown, train_dropdown, log_console):
    selected_station_name = station_dropdown.get()
    if selected_station_name:
        try:
            trains_response = requests.get("https://stacjownik.spythere.pl/api/getActiveTrainList").json()
            relevant_trains = [train for train in trains_response if train['currentStationName'] == selected_station_name]
            train_numbers = [train['trainNo'] for train in relevant_trains]
            train_dropdown['values'] = train_numbers
            train_dropdown.set('')
            add_to_log(log_console, "Updating Train List")
        except requests.RequestException as e:
            add_to_log(log_console, "An error occurred while updating the train list: {e}")

def select_gong():
    global gong_sound_path
    gong_sound_path = filedialog.askopenfilename(
        title="Select a WAV File",
        filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*"))
    )

def get_wav_duration(wav_path):
    with contextlib.closing(wave.open(wav_path, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration_seconds = frames / float(rate)
        return duration_seconds
    
def play_sound(wav_path):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    pygame.mixer.music.load(wav_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.delay(200)