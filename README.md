
![enter image description here]((https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/W9ejkj84sYZSnAy?file=&fileId=1093913&x=1926&y=1056&a=true))
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

You can either use the hotkeys defined in config.cfg or press the buttons manually. "Next Stop only" only announces the next stop without mentioning an exit side. Occasionally there is an additional announcement.
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
