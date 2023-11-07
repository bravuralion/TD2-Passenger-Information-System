Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$currentVersion = '0.3'

#File Location für Audio Announcement
$filename = "$env:APPDATA\TD2-AN.wav"

#Settings for Azure Voice
$resourceRegion = "westeurope"
$apiKey = "1234"
$ttsUrl = "https://$resourceRegion.tts.speech.microsoft.com/cognitiveservices/v1"

function Check-For-Update {
    $user = 'bravuralion'
    $repo = 'TD2-Driver-PIS-SYSTEM'
    $apiUrl = "https://api.github.com/repos/$user/$repo/releases/latest"


    $latestRelease = Invoke-RestMethod -Uri $apiUrl
    $latestVersion = $latestRelease.tag_name
    $downloadUrl = $latestRelease.assets[0].browser_download_url

    if ($currentVersion -ne $latestVersion) {
        $message = "Eine neue Version ($latestVersion) ist verfügbar. Möchten Sie das Update jetzt herunterladen?"
        $title = "Update verfügbar"   

        $result = [System.Windows.Forms.MessageBox]::Show($message, $title, [System.Windows.Forms.MessageBoxButtons]::YesNo)

        if ($result -eq 'Yes') {
            Start-Process $downloadUrl 
        } 
    } 
}
Check-For-Update
function Get-WavDuration {
    param (
        [string]$wavPath
    )

    $fileStream = [System.IO.File]::OpenRead($wavPath)
    $binaryReader = New-Object System.IO.BinaryReader($fileStream)

    # Skip the first 22 bytes of the WAV header
    $binaryReader.BaseStream.Position = 22

    # Read the number of channels (2 bytes)
    $channels = $binaryReader.ReadUInt16()

    # Read the sample rate (4 bytes)
    $sampleRate = $binaryReader.ReadUInt32()

    # Skip the next 6 bytes
    $binaryReader.BaseStream.Position += 6

    # Read the block align (2 bytes)
    $blockAlign = $binaryReader.ReadUInt16()

    # Skip to byte 40 to get the data size (4 bytes)
    $binaryReader.BaseStream.Position = 40
    $dataSize = $binaryReader.ReadUInt32()

    $binaryReader.Close()
    $fileStream.Close()

    # Calculate the duration in seconds
    $durationInSeconds = $dataSize / ($sampleRate * $channels * $blockAlign / 8)
    return $durationInSeconds
}

function ConvertTextToSpeech {
    param (
        [Parameter(Mandatory=$true)]
        [string]$text,
        [Parameter(Mandatory=$true)]
        [string]$language
    )
    $Song = New-Object System.Media.SoundPlayer
    if ($script:gongSoundPath) {
        $timeout = Get-WavDuration -wavPath $gongSoundPath
        if ($timeout -lt 10)
        {
            $Song.SoundLocation = $gongSoundPath
            $Song.Play()
            Start-Sleep -Seconds $timeout
        }
    }
    if ($language -eq "German" -and $text -match '(\d{2}:\d{2})') {
        $text = $text -replace '(\d{2}:\d{2})', (ConvertTimeForAudio -time (Get-Date $matches[1]))
    }
    # Header für die Anfrage
    $headers = @{
        "Ocp-Apim-Subscription-Key" = $apiKey
        "Content-Type" = "application/ssml+xml"
        "X-Microsoft-OutputFormat" = "riff-16khz-16bit-mono-pcm"
        "User-Agent" = "PowerShell"
    }

    # SSML-Body für die Anfrage basierend auf der gewählten Sprache
    switch ($language) {
        "English" {
            $voiceName = "en-US-JessaNeural"
            $lang = "en-US"
        }
        "Polish" {
            $voiceName = "pl-PL-AgnieszkaNeural"
            $lang = "pl-PL"
        }
        "German" {
            $voiceName = "de-DE-KatjaNeural"
            $lang = "de-DE"
        }
    }

    $bodyString = @"
<speak version='1.0' xml:lang='$lang'>
    <voice xml:lang='$lang' xml:gender='Female' name='$voiceName'>
        $text
    </voice>
</speak>
"@

    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyString)
    $response = Invoke-WebRequest -Uri $ttsUrl -Method Post -Headers $headers -Body $bodyBytes
    [System.IO.File]::WriteAllBytes($filename, $response.Content)

    $Song = New-Object System.Media.SoundPlayer
    $Song.SoundLocation = $filename
    $Song.Play()
    $timeout = Get-WavDuration -wavPath $filename
    Start-Sleep -Seconds $timeout
}


$form = New-Object System.Windows.Forms.Form
$form.Text = 'Driver PIS System'
$form.Size = New-Object System.Drawing.Size(500, 430)

$trainNumberTextbox = New-Object System.Windows.Forms.TextBox
$trainNumberTextbox.Location = New-Object System.Drawing.Point(10, 10)
$trainNumberTextbox.Size = New-Object System.Drawing.Size(460, 20)
$form.Controls.Add($trainNumberTextbox)

$loadScheduleButton = New-Object System.Windows.Forms.Button
$loadScheduleButton.Location = New-Object System.Drawing.Point(10, 40)
$loadScheduleButton.Size = New-Object System.Drawing.Size(460, 30)
$loadScheduleButton.Text = 'Load Schedule'
$form.Controls.Add($loadScheduleButton)

$stationsListbox = New-Object System.Windows.Forms.ListBox
$stationsListbox.Location = New-Object System.Drawing.Point(10, 80)
$stationsListbox.Size = New-Object System.Drawing.Size(460, 160)
$form.Controls.Add($stationsListbox)

$exitRightButton = New-Object System.Windows.Forms.Button
$exitRightButton.Location = New-Object System.Drawing.Point(170, 250)
$exitRightButton.Size = New-Object System.Drawing.Size(150, 40)
$exitRightButton.Text = 'Exit to the right'
$form.Controls.Add($exitRightButton)

$exitLeftButton = New-Object System.Windows.Forms.Button
$exitLeftButton.Location = New-Object System.Drawing.Point(10, 250)
$exitLeftButton.Size = New-Object System.Drawing.Size(150, 40)
$exitLeftButton.Text = 'Exit to the left'
$form.Controls.Add($exitLeftButton)

$exitNoneButton = New-Object System.Windows.Forms.Button
$exitNoneButton.Location = New-Object System.Drawing.Point(330, 250)
$exitNoneButton.Size = New-Object System.Drawing.Size(140, 40)
$exitNoneButton.Text = 'Next Stop'
$form.Controls.Add($exitNoneButton)

$gongButton_Click = {
    $openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $openFileDialog.Filter = "WAV Files (*.wav)|*.wav"
    $openFileDialog.Title = "Select a WAV File"
    if ($openFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $script:gongSoundPath = $openFileDialog.FileName
    }
}

$gongButton = New-Object System.Windows.Forms.Button
$gongButton.Location = New-Object System.Drawing.Point(10, 300)
$gongButton.Size = New-Object System.Drawing.Size(460, 20)
$gongButton.Text = 'Select Gong Sound'
$gongButton.Add_Click($gongButton_Click)
$form.Controls.Add($gongButton)

$languageComboBox = New-Object System.Windows.Forms.ComboBox
$languageComboBox.Location = New-Object System.Drawing.Point(10,330)
$languageComboBox.Size = New-Object System.Drawing.Size(460, 20)
$languageComboBox.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList
$languageComboBox.Items.Add("Deutsch")
$languageComboBox.Items.Add("English")
$languageComboBox.SelectedItem = "Deutsch"
$form.Controls.Add($languageComboBox)

$loadScheduleButton.Add_Click({
    $trainsResponse = Invoke-RestMethod -Uri "https://stacjownik.spythere.pl/api/getActiveTrainList"
    $selectedTrainNo = $trainNumberTextbox.Text
    $selectedTrain = $trainsResponse | Where-Object { $_.trainNo -eq $selectedTrainNo }
    $stationsListbox.Items.Clear()
    foreach ($stop in $selectedTrain.timetable.stopList) {
        if ($stop.stopType -eq 'PH' -or $stop -eq $selectedTrain.timetable.stopList[-1]) {
            $stationsListbox.Items.Add($stop.stopNameRAW)
        }
    }
})

$announceExit = {
    param([string]$exitSide)
    
    $selectedLanguage = $languageComboBox.SelectedItem.ToString()
    $languageCode = if ($selectedLanguage -eq 'Deutsch') { 'german' } else { 'english' }

    if ($stationsListbox.SelectedItem) {
        $currentIndex = $stationsListbox.SelectedIndex
        $isLastStation = $currentIndex -eq $stationsListbox.Items.Count - 1
        $stationName = $stationsListbox.SelectedItem -replace 'po\.$', ''

        $baseAnnouncement = ""
        $exitAnnouncement = ""
        $additionalAnnouncement = ""
        
        switch ($selectedLanguage) {
            'Deutsch' {
                $baseAnnouncement = "Nächster Halt: $($stationName)"
                if ($exitSide -eq "links") { $exitAnnouncement = ", Ausstieg in Fahrtrichtung Links" }
                if ($exitSide -eq "rechts") { $exitAnnouncement = ", Ausstieg in Fahrtrichtung Rechts" }
                if (-not $isLastStation) {
                    $random = Get-Random -Minimum 1 -Maximum 6
                    if ($random -le 2) {
                        $additionalAnnouncement = ". Für Ihre Anschlüsse beachten Sie bitte die Lautsprecherdurchsagen und weitere Informationen am Bahnsteig"
                    }
                }
            }
            'English' {
                $baseAnnouncement = "Next stop: $($stationName)"
                if ($exitSide -eq "links") { $exitAnnouncement = ", Exit on the left" }
                if ($exitSide -eq "rechts") { $exitAnnouncement = ", Exit on the right" }
                if (-not $isLastStation) {
                    $random = Get-Random -Minimum 1 -Maximum 6
                    if ($random -le 2) {
                        $additionalAnnouncement = ". For your connections, please pay attention to the announcements and further information on the platform"
                    }
                }
            }
        }

        $finalAnnouncement = "$baseAnnouncement$exitAnnouncement$additionalAnnouncement"        
        if ($isLastStation) {
            if ($selectedLanguage -eq 'Deutsch') {
                $finalAnnouncement += ", Dieser Zug endet hier. Bitte alle aussteigen."
            } elseif ($selectedLanguage -eq 'English') {
                $finalAnnouncement += ", This train terminates here. All passengers must disembark."
            }
        }

        ConvertTextToSpeech -text $finalAnnouncement -language $languageCode

        if (-not $isLastStation) {
            $stationsListbox.SelectedIndex = $currentIndex + 1
        }
    }
}




$exitRightButton.Add_Click({ $announceExit.Invoke('rechts') })
$exitLeftButton.Add_Click({ $announceExit.Invoke('links') })
$exitNoneButton.Add_Click({ $announceExit.Invoke('none') })

$form.KeyPreview = $true
$form.Add_KeyDown({
    switch ($_.KeyCode) {
        'F13' {
            $announceExit.Invoke('rechts')
        }
        'F14' {
            $announceExit.Invoke('links')
        }
        'F15' {
            $announceExit.Invoke('none')
        }
    }
})
$form.ShowDialog()

