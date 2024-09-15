#=============================================
#function to show info about latest logins :D
#=============================================

function Show-LogsLogin {

    <#
    .synopsis
    Script that checks if logins on a device were successful.

    .description
    The script lists the logins depending on the number of sessions given by the user.
    The admin permissions are required in order to get results.

    .example
    PS C:\Users\PCName> Get-PCInformation -numLogins 3
    With this example the function shows you the information about 3 recents access sessions.

    .inputs
    TThis script requires the $numLogins parameter to know how many recent logins to display.

    .outputs
    This script shows you in terminal any results before execute it.

    .notes
    Version 1.0
    Authors: Estrella Díaz, Fernanda Romo
    Created 07/09/2024
    - Lines 28 to 39 based on https://github.com/Bert-JanP/Incident-Response-Powershell/blob/3d91389447d02b481e65675daeb5f49a1f1393e6/Scripts/LastLogons.ps1
    #>

    param(
        [Parameter(Mandatory)][int]$numLogins
    )

    try {
        #get $numLogins of security logs and filter them by ID
        $AccessSessions = Get-WinEvent -LogName 'Security' -FilterXPath "*[System[EventID = 4624 or EventID = 4648]]" `
        | Select-Object -First $numLogins

        #extract the info for earch login and prints it
        foreach ($session in $AccessSessions) {
            $date = $session.TimeCreated
            $message = $session.Message
            $SessionType = if ($session.Id -eq 4648) {"Explicit"} else {"Interactive"}

            Write-Host -ForegroundColor Yellow ">> Date (Time created): $date"
            Write-Host -ForegroundColor Cyan ">> Session Type: $SessionType"
            Write-Host -ForegroundColor DarkGreen ">> Message."
            Write-Host $message
        }

    } catch {
        #checks for administrator permissions by identify the users role
        if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::`
        GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
            Write-Host -ForegroundColor Green "Enables administrator permissions."
        }
    }
}

Export-ModuleMember -Function Show-LogsLogin
