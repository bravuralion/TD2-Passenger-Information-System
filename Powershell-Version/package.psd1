@{
    Root = 'C:\Users\bravura\Documents\GitHub\TD2-Driver-PIS-SYSTEM-2\Driver PIS System.ps1'
    OutputPath = 'C:\Users\bravura\Documents\GitHub\TD2-Driver-PIS-SYSTEM-2\out'
    Package = @{
        Enabled = $true
        Obfuscate = $true
        HideConsoleWindow = $true
        DotNetVersion = 'v4.6.2'
        FileVersion = '0.0.4'
        FileDescription = ''
        ProductName = 'TD2 Driver PIS System'
        ProductVersion = '0.0.4'
        Copyright = 'Bravura Lion'
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
        