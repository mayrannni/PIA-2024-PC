<#
.synopsis
This is the menu to manage custom modules.

.description
This menu asks for the path of each module in order to import them into the current session and manage them to display their content.

.parameter ModuleRequestApiHashBased
Enter the path to the module (example) >> C:\Program Files\WindowsPowerShell\Modules\ModuleRequestApiHashBased

.parameter ModuleShowHiddenFiles
Enter the path to the module (example) >> C:\Program Files\WindowsPowerShell\Modules\ModuleShowHiddenFiles

.parameter ModuleGetPCInformation
Enter the path to the module (example) >> C:\Program Files\WindowsPowerShell\Modules\ModuleGetPCInformation

.parameter ModuleShowLogsLogin
Enter the path to the module (example) >> C:\Program Files\WindowsPowerShell\Modules\ModuleShowLogsLogin

.example
PS C:\Users\PCName\here\is\the\menu> .\Menu

.notes
-Enter the abs path of each module with extension .psm1
Version 1.0
Authors: Estrella Díaz, Fernanda Romo
Created 12/09/2024
#>

param (
    [Parameter(Mandatory)][String]$ModuleRequestApiHashBased,
    [Parameter(Mandatory)][String]$ModuleShowHiddenFiles,
    [Parameter(Mandatory)][String]$ModuleGetPCInformation,
    [Parameter(Mandatory)][String]$ModuleShowLogsLogin
)

#save the paths in $modulesPath array
$modulesPath = @($ModuleRequestApiHashBased, $ModuleShowHiddenFiles, $ModuleGetPCInformation, $ModuleShowLogsLogin)
$badmodulesPath = @()

#validate that the path is not enclosed in quotation marks
foreach ($module in $modulesPath) {
    if ($module -like '*"*"*' -or $module -like "*'*'*") {
        Write-Host -ForegroundColor Red ">> Error: $module"
        $badmodulesPath += $module
    }
}

if ($badmodulesPath.Count -gt 0) {
    Write-Host -ForegroundColor DarkYellow  "(´。＿。｀) Avoid typing the path inside double or single quotes. Thank you."
    exit
}

#verify that it works in strict mode
Set-StrictMode -Version Latest

function Show-Menu {

    Write-Host -ForegroundColor Green "<-------------------------------------->"
        Write-Host "Main: You can review the following Cybersecurity activities."
        Write-Host "1. Query VT api based on file hashes"
        Write-Host "2. Show hidden files from a folder"
        Write-Host "3. Verify system resources"
        Write-Host "4. Review recent login logs"
        Write-Host "0. Exit"
        Write-Host -ForegroundColor Green "<-------------------------------------->"
}

try {

    do {

        #call function, displays the options
        Show-Menu
        $UserChoice = Read-Host "Select an option to show actions"
    
        switch ($UserChoice) {

            1 { 
                Write-Host -ForegroundColor DarkBlue ">> Module Request-ApiHashBased"
                Import-Module $ModuleRequestApiHashBased
                Request-ApiHashBased
            }

            2 { 
                Write-Host -ForegroundColor DarkBlue ">> Module Show-HiddenFiles"
                Import-Module $ModuleShowHiddenFiles
                Show-HiddenFiles
            }

            3 { 
                Write-Host -ForegroundColor DarkBlue ">> Module Get-PCInformation"
                Import-Module $ModuleGetPCInformation
                Get-PCInformation
            }

            4 { 
                Write-Host -ForegroundColor DarkBlue ">> Module Show-LogsLogin"
                Import-Module $ModuleShowLogsLogin
                Show-LogsLogin
            }

            0 {

                Write-Host "Closing..." -ForegroundColor Cyan
                break
            }

            default { Write-Host "Try again. Enter a valid option." -ForegroundColor Red }
        }

    } while ($userChoice -ne 0)

} catch {

    Write-Host -ForegroundColor Blue "We are sorry. Unexpected error: $($_.Exception.Message)"
}
