
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/tZCD2s7BQxzZcTY?file=&fileId=1093590&x=3844&y=1951&a=true)
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/a7Xkk97Ys8wALPi?file=&fileId=1093616&x=3844&y=1951&a=true)
As you may know, I have already written a tool for the dispatcher where you can make station announcements: https://td2.info.pl/english-boards/simple-text-announcement-generator/

I have written a simple tool in Powershell that the train driver can use to generate announcements for his passengers. The program is designed to be as simple as possible. The timetable is loaded automatically and the announcements are generated with Microsoft Azure Voice. There is also the option of making special announcements. Hotkeys for the most important functions are supported and the voice output can be customized via a configuration file. (Tutorial in this article below). The program is constantly being expanded with new features, so check this post regularly :)
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/R7CXwYWC3wfx3wo?file=&fileId=1093632&x=3844&y=1951&a=true)

-   Automatic determination of the timetable
-   Custom Announcement for the Starting Station
-   Custom Announcement for the Last Station
-   Announcement option for exiting right or left, alternatively only the announcement of the next stop.
-   Next Station is
-   5 Buttons for Special Announcements
-   Option to use a chime that is played before each announcement.
-   The next station is selected automatically
-   Auto Update: If a new version is detected, you can download the new version via the app
-   Support for EN,DE, PL
-   All Audio Announcements can be customized
-   All Hotkeys can be customized via config.cfg
- More features to come

More features to come :)

**IMPORTANT: It can happen that the Antivirus blocks the Exe as it detects that it runs a Powershell Script. You may have to whitelist the exe to be able to run it. This is a known issue but im on it to improve on that matter so that the executable will be signed in the future. https://github.com/MScholtes/Win-PS2EXE/issues/4**

Extract the content of the zip where you want. Be sure that the .cfg files are next to the exe file. Run the Program and enter your Train number. After that, load the schedule and select the first station of which you want to make an announcement. Make sure that you have selected the correct language in which you want the voice output.

You can either use the hotkeys defined in config.cfg or press the buttons manually. "Next Stop only" only announces the next stop without mentioning an exit side. Occasionally there is an additional announcement.
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/foi59jd93yBnbjs?file=&fileId=1093648&x=3844&y=1951&a=true)
The program offers the possibility to adapt the text for the voice output. This currently requires 2 files:
**Categories.cfg**
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/ZgD7mCs6mkfzaRA?file=&fileId=1093589&x=3844&y=1951&a=true)

This file is used to convert the train category from the short code to the long version for the announcements. This is currently only used for the special announcement at the departure station.
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
Thats it. You can now use the Hotkeys :) Ps: You can add a third step where the Focus goes back to TD2[/list]
![enter image description here](https://cloud.furry.fm/index.php/apps/files_sharing/publicpreview/D5fi2oJJdH9yaHj?file=&fileId=1093667&x=3844&y=1951&a=true)
1. If you don't hear any Audio Announcements, Start the Internet Explorer once. This will fix the issue.
