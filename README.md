
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/W9ejkj84sYZSnAy?file=&fileId=1093913&x=1926&y=1056&a=true)
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/a7Xkk97Ys8wALPi?file=&fileId=1093616&x=3844&y=1951&a=true)

This program simulates a Passenger Information System for the game Train Driver 2. The tool was created from 2 individual Powershell programs which have now been rewritten in Python and have been combined. There is a separate mode for the train driver to generate announcements for the train and its passengers and a mode for the dispatcher to generate platform announcements. The tool is designed to maximize the degree of automation with minimal input from the user. 

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/R7CXwYWC3wfx3wo?file=&fileId=1093632&x=3844&y=1951&a=true)

-  General: If a new version is detected, you can download the new version via the app
-  General: Support for English, German and Polish
-  Driver Mode: Automatic determination of the timetable
-  Driver Mode: Custom Announcement for the Starting Station
-  Driver Mode: Custom Announcement for the Last Station
-  Driver Mode: Announcement option for exiting right or left, alternatively only the announcement of the next stop.
-  Driver Mode: 5 Buttons for Special Announcements
-  Driver Mode: Option to use a chime that is played before each announcement.
-  Driver Mode: Auto selection of the next Station
-  Driver Mode: All Audio Announcements can be customized
-  Driver Mode: Announcements can be played via a Hotkey
-  Driver Mode: Adjustment of the Output Volume for the Chime and Announcement
-  Dispatcher Mode: Auto-load all available Stations
-  Dispatcher Mode: Automatic detection of the trains in the station
-  Dispatcher Mode: Automatic generation of the station announcement based on the timetable ("passing through", "stop", "train ends")
-  Dispatcher Mode: 10 buttons to generate a fast train passing announcement
-  Dispatcher Mode: Automatic mention of the delay if it is over 5 minutes
-  More features to come

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/XcZNswYxk8PgTnd?file=&fileId=1094001&x=1926&y=1056&a=true)

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/tZCD2s7BQxzZcTY?file=&fileId=1093590&x=1926&y=1056&a=true)

This mode is intended for the train driver to generate announcements for his train. The announcements are logically only for passenger trains. As soon as you have received a timetable in Train Driver 2, enter the train number at the top and click on "Load Schedule". The timetable will then be loaded. Note: The first and last stations are always loaded as well as all stops that are defined as PH in the timetable, all other entries in the timetable are ignored. To generate an announcement, select the stop for which you want to make an announcement.

There are now 3 options for the announcement: Exit right, Exit left and Next Stop Only. The first two options add the exit side to the announcement and Next Stop Only only mentions the next stop without mentioning an exit side. These 3 buttons also offer a hotkey function. More about this in the Hotkeys section. The announcements are always generated in the currently selected language. To change this, simply change the language in the selection menu.

There is also the option to play a chime before each announcement: To do this, press the "Select Gong" button and select the corresponding audio file.
The driver also has the option of generating special announcements. Buttons S1 to S5 are available for this purpose. The texts for these can be customized via config.cfg. Attention: Please make sure that the language selection corresponds to the text in the config.cfg.

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/CEnNpezKyjHGDzw?file=&fileId=1094002&x=1205&y=645&a=true)

This mode is for the dispatcher. The tool is designed to generate platform announcements. Audio announcements are generated and the announcement text is copied to the clipboard so that it can be pasted into the Train Driver 2 in-game chat. The tool automatically reads the train timetable and generates the announcements accordingly. Output is implemented in English, German, and Polish.

At the moment, the App generates the following Announcements fully automatically depending on the Timetable:  
  
**If a train has a PH in a Station and has no Delay, the Announcement looks like this:**  
> *STATION ANNOUNCEMENT* Attention at track 1, The pospieszny from Trzymałkowice to LIGOTA GRABOWSKA is arriving. The planned Departure is 12:05. *OGŁOSZENIE STACYJNE* Uwaga! Pociąg pospieszny ze stacji Trzymałkowice do stacji LIGOTA GRABOWSKA wjedzie na tor 1, Planowy odjazd pociągu o godzinie 12:05.

**If a train has a PH in a Station and has a Delay > 5 Minutes, the Announcement looks like this:**  
> *STATION ANNOUNCEMENT* The pospieszny from station CZERMIN to station ŻORY, scheduled arrival 12:02, will arrive approximately 9 minutes late at platform 1. The delay is subject to change. Please pay attention to announcements. *OGŁOSZENIE STACYJNE* Uwaga! Pociąg pospieszny ze stacji CZERMIN do stacji ŻORY wjedzie na tor 1, planowy przyjazd 12:02, przyjedzie z opóźnieniem około 9 minut. Opóźnienie może ulec zmianie. Prosimy o zwracanie uwagi na komunikaty.

**If a Train ends at the Station, the Announcement looks like this:**  
> *STATION ANNOUNCEMENT* Attention at track 1, the pospieszny from is arriving. This train ends here, please do not board the train. *OGŁOSZENIE STACYJNE* Uwaga na tor 1, przyjedzie Pociąg pospieszny ze stacji . Pociąg kończy bieg. Prosimy zachować ostrożność i nie zbliżać się do krawędzi peronu

  
**If a train has no PH, is passing through, or has no timetable, this announcement is generated**  
> *STATION ANNOUNCEMENT* Attention at track 1, A train is passing through. Please stand back. *OGŁOSZENIE STACYJNE* Uwaga! Na tor 1 wjedzie pociąg bez zatrzymania. Prosimy zachować ostrożność i nie zbliżać się do krawędzi peronu.

**How to use the Mode:**

1. Select the Station where you want to generate the Announcements  
2. In the language selection, select the language in which the announcement is to be generated. Attention: This selection also applies to the audio announcements.  
3. **Wait until the Train arrives at your Station**, click the Update Trains Button to Refresh the List of Trains
4. Select the Train for which you want to generate the Announcement  
5. Select the track for which the announcement is to be made.  
6. **OPTIONAL**: Do you want to hear the Announcement too? Then Select Play Audio. You can also choose a .wav File if you want the App to play a Gong before the Announcement  
7. Click the Button Generate. **It will now generate the Announcement and copies the Text into your Clipboard** so that you can easily paste it into the Chat of TD2 with STRG+V. There is also a Pop Up appearing where you  
can Check the generated Announcement.  
**Note: The announcements for a PH are generated only for the primary station, not for small stops.**

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/foi59jd93yBnbjs?file=&fileId=1093648&x=3844&y=1951&a=true)
The program offers the possibility to adapt the text for the voice output. This currently requires 2 files:
**Categories.cfg**

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/ZgD7mCs6mkfzaRA?file=&fileId=1093589&x=3844&y=1951&a=true)

This file is used to convert the train category from the shortcode to the long version for the announcements. This is currently only used for the special announcement at the departure station.
**config.cfg**

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/BDzFz79a8FCAN4q?file=&fileId=1093591&x=3844&y=1951&a=true)

This is the main file that is used for the announcements. From line 1 to 24 are the different text templates for English, German and Polish. These can be customized individually. Please note: The adjustment must be made before the program is started, otherwise the changes will be ignored. 
The announcements "Additional_Announcement_XX" are special announcements that are randomly added to the announcement.
$Hotkey_XY are used for the hotkey assignment for the exit right, left or the announcement without naming the exit.
$Special1-5 are for the buttons S1 to S5 which you can use for your own special announcements. German special announcements are currently defined there.

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/8S7Xini4WtQ4cmF?file=&fileId=1093668&x=3844&y=1951&a=true)

Hotkeys can be used for the Buttons "Exit Left, "Exit Right" and "Next Stop Only" The Hotkeys can be defined in the config.cfg (see above). Please note that the Hotkeys only work when the App is in Focus! You can use any Program to do that. In this Example, i show you how to do that with Streamdeck:

Ad Focus Windows by Process Name from the Windows Gizmos Library  and set "Driver PIS System" as the Process Name:

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/mJ4eeW4x49TsBws?file=&fileId=1093522&x=1926&y=1057&a=true)

Next add a Hotkey Function and klick on the little Arrow:

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/z8DPpMFe4gxHnWo?file=&fileId=1093523&x=1926&y=1057&a=true)

Then Select the F Keys -> F13, F14 or F15 depending on what you want:

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/GNnr3CpqbD78CDL?file=&fileId=1093521&x=1926&y=1057&a=true)

Thats it. You can now use the Hotkeys :) Ps: You can add a third step where the Focus goes back to TD2

![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/D5fi2oJJdH9yaHj?file=&fileId=1093667&x=3844&y=1951&a=true)

1. If you don't hear any Audio Announcements, Start the Internet Explorer once. This will fix the issue.
