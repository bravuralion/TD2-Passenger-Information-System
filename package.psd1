@{
    Root = 'C:\Users\Mateusz\TD2-Driver-PIS-SYSTEM\Driver PIS System.ps1'
    OutputPath = 'C:\Users\Mateusz\TD2-Driver-PIS-SYSTEM\out'
    Package = @{
        Enabled = $true
        Obfuscate = $true
        HideConsoleWindow = $true
        DotNetVersion = 'v4.6.2'
        FileVersion = '0.3.1mt'
        FileDescription = ''
        ProductName = 'TD2 Driver PIS System (translated)'
        ProductVersion = '0.3.1mt'
        Copyright = 'Bravura Lion, Argeos'
        RequireElevation = $false
        ApplicationIconPath = ''
        PackageType = 'Console'
        Resources = [string[]]@()
    }
    Bundle = @{
        Enabled = $true
        Modules = $true
        # IgnoredModules = @()
    }
}
        