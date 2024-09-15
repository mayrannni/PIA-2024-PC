#======================================
#function that displays hidden files :D
#======================================

function Show-HiddenFiles {

    <#

    .synopsis
    Script that displays a list of hidden files.

    .description
    This script shows you all existing hidden files in a given folder path.
    Use a function called Show-HiddenFiles.

    .parameter FolderPath
    This is the path to the folder (it contains hidden files).

    .example
    PS C:\Users\PCName> Show-HiddenFiles -FolderPath "C:\this\is\the\folder\path"
    With this example you can access the module.

    .inputs
    This script requires the $FolderPath parameter to show the information.

    .outputs
    This script shows you in terminal any results before execute it.

    .notes
    Version 1.0
    Authors: Estrella Díaz, Fernanda Romo
    Created 07/09/2024

    #>

    param (
        [Parameter(Mandatory)][string]$FolderPath
    )
    
    try {
        
        if (-Not(Test-Path -Path $FolderPath)) {
            Write-Host "The folder path $FolderPath cannot be found."
        }
        
        #check the hidden files and save them in $HiddenFiles
        $HiddenFiles = Get-ChildItem -Path $FolderPath -Hidden -Recurse

        if ($HiddenFiles.Count -eq 0){
            #validates that the folder contains hidden files
            Write-Host "There are no hidden files in $FolderPath."
        } else {
            #obtains the info from hidden files
            Write-Host -ForegroundColor Green "> Information about hidden files"
            $HiddenFiles | Select-Object -Property @{Name = "HiddenFile"; Expression = {$_.Name}}, LastAccessTime, LastWriteTime, `
            @{Name = "Length (Bytes)"; Expression = {$_.Length}}, Mode, IsReadOnly | Format-Table -AutoSize
        }

    } catch {
        #catch any unexpected errors
        Write-Host -ForegroundColor Red "Something went wrong..." $($_.Exception.Message)
    }
}

#call the function
Show-HiddenFiles
