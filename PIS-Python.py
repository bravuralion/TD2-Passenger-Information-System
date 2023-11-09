import requests
import tkinter as tk
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title('On-board Passenger Information System')
root.geometry('480x400')

gong_sound_path = ''

train_number_textbox = tk.Entry(root)
train_number_textbox.place(x=10, y=10, width=460, height=20)

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

load_schedule_button = tk.Button(root, text='Load Schedule', command=load_schedule)
load_schedule_button.place(x=10, y=40, width=460, height=30)

load_schedule_button = tk.Button(root, text='Load Schedule', command=load_schedule)
load_schedule_button.place(x=10, y=40, width=460, height=30)

stations_listbox = tk.Listbox(root)
stations_listbox.place(x=10, y=80, width=460, height=160)

def announce_exit(exit_side):
    # announcement functionality
    pass

exit_right_button = tk.Button(root, text='Exit right', command=lambda: announce_exit('right'))
exit_right_button.place(x=170, y=250, width=150, height=40)

exit_left_button = tk.Button(root, text='Exit left', command=lambda: announce_exit('left'))
exit_left_button.place(x=10, y=250, width=150, height=40)

exit_none_button = tk.Button(root, text='Next Stop only', command=lambda: announce_exit('none'))
exit_none_button.place(x=330, y=250, width=140, height=40)

def select_gong():
    global gong_sound_path
    gong_sound_path = filedialog.askopenfilename(
        title="Select a WAV File",
        filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*"))
    )

gong_button = tk.Button(root, text='Select Gong (.WAV)', command=select_gong)
gong_button.place(x=10, y=300, width=460, height=20)

def play_special_announcement(announcement):
    # Implement
    pass

special_buttons = []
for i in range(5):
    special_button = tk.Button(root, text=f'S{i+1}',
                               command=lambda i=i: play_special_announcement(f'Special{i+1}'))
    special_button.place(x=10 + 85 * i, y=360, width=75, height=23)
    special_buttons.append(special_button)

language_combobox = tk.StringVar(root)
language_combobox.set('German')  # default value
language_options = ['German', 'English', 'Polish']

language_dropdown = tk.OptionMenu(root, language_combobox, *language_options)
language_dropdown.place(x=10, y=330, width=460, height=20)

root.mainloop()
