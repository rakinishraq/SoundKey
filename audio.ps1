param (
    [string]$index = ""
)

# Check if we are running as an administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    # We are not running "as Administrator" - so relaunch as administrator

    # Create a new process object that starts PowerShell
    $newProcess = new-object System.Diagnostics.ProcessStartInfo "PowerShell";

    # Specify the current script path and name as a parameter with the index argument
    $newProcess.Arguments = "& '" + $script:MyInvocation.MyCommand.Path + "'"
    if ($index -ne "") {
        $newProcess.Arguments += " -index " + $index
    }

    # Indicate that the process should be elevated
    $newProcess.Verb = "runas";

    # Start the new process
    [System.Diagnostics.Process]::Start($newProcess);

    # Exit from the current, unelevated, process
    exit
}

# Install AudioDeviceCmdlets if not installed
if (-not (Get-Module -ListAvailable -Name AudioDeviceCmdlets)) {
    Install-Module -Name AudioDeviceCmdlets
}
Import-Module -Name AudioDeviceCmdlets

# If index is a number, set the audio device, otherwise list the available audio devices
if ($index -eq "" -or -not ($index -match "^\d+$")) {
    Get-AudioDevice -List
} else {
    Set-AudioDevice -Index $index
}