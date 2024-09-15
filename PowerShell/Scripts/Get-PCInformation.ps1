#==================================================
#function to check the use of computer resources :D
#==================================================

function Get-PCInformation {

    <#

    .synopsis
    Script to check detailed information about the use of computer resources.

    .description
    This script gives you a review about the usage of differents resources such as Memory, Disk, CPU and Network.
    With this script you can monitor the use of your computer in different aspects.

    .example
    PS C:\Users\PCName> Get-PCInformation
    With this example you can access the module.

    .inputs
    This script contains a function that does not require input parameters.
    Just select an option from menu!

    .outputs
    This script shows you in terminal any results before execute it.

    .notes
    Version 1.0
    Authors: Estrella Díaz, Fernanda Romo
    Created 07/09/2024

    #>

    Write-Host "Hi! there is a function to check the use of computer resources."
    do {

        Write-Host -ForegroundColor Magenta "--------------------------------------"
        Write-Host "Select a computer resource"
        Write-Host "1. Memory"
        Write-Host "2. Disk"
        Write-Host "3. CPU"
        Write-Host "4. Network"
        Write-Host "0. Exit"
        Write-Host -ForegroundColor Magenta "--------------------------------------"

        $userChoice = Read-Host ">> Your choice"

        switch ($userChoice) {
            1 {
                Write-Host -ForegroundColor Green "Memory usage"

                #returns the info in bytes, converts to mb
                Write-Host "> Process memory usage"
                Get-Process | Sort-Object WorkingSet -Descending | Select-Object @{Name = "Process"; Expression = {$_.Name}}, `
                @{Name = "Memory (MB)"; Expression = {[math]::round($_.WorkingSet / 1MB, 1)}} | Format-Table -AutoSize

                #Common Information Model (kilobytes), converts to gb
                $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
                $totalMem = [math]::round(($osInfo.TotalVisibleMemorySize / 1MB), 2)
                $freeMem = [math]::round(($osInfo.FreePhysicalMemory / 1MB), 2)
                $usedMem = ($totalMem - $freeMem)

                Write-Host "> System memory details"
                Write-Host "Total memory system: $totalMem GB"
                Write-Host "Free memory system: $freeMem GB"
                Write-Host "Total used memory system: $usedMem GB"
            }

            2 {
                Write-Host -ForegroundColor Green "Disk usage"
                Write-Host "> System disk details"
                Get-CimInstance -ClassName Win32_LogicalDisk | Select-Object @{Name = "Disk drive"; Expression = {$_.DeviceID}}, `
                @{Name = "Size (GB)";Expression = {[math]::round($_.Size/1GB, 2)}}, @{Name = "FreeSpace (GB)"; `
                Expression={[math]::round($_.FreeSpace/1GB, 2)}} | Format-Table -AutoSize
            }

            3 {
                Write-Host -ForegroundColor Green "CPU usage"
                Write-Host "> System processor usage (total)"
                Get-CimInstance -ClassName Win32_Processor | Select-Object @{Name = "Processor Name"; Expression = {$_.Name}}, `
                @{Name = "CPU usage (%)"; Expression={[math]::round($_.LoadPercentage, 2)}} | Format-Table -Autosize

                Write-Host "> CPU uptime per process"
                #'CPU' property: cpu time consumed by each process in seconds
                Get-Process | Select-Object @{Name = "Process"; Expression = {$_.Name}}, @{Name="CPU Time (sec)"; Expression={[math]::round($_.CPU, 2)}} `
                | Format-Table -Autosize
            }

            4 {
                Write-Host -ForegroundColor Green "Network usage"
                Write-Host "> Received and sent bytes per net adapter"
                Get-NetAdapterStatistics | Select-Object @{Name = "NetAdapter"; Expression = {$_.Name}}, ReceivedBytes, SentBytes `
                | Format-Table -Autosize

                Write-Host "> Detailed info about net adapters"
                Get-NetAdapter | Select-Object @{Name = "NetAdapter"; Expression = {$_.Name}}, DriverName, DriverDescription, Status, `
                @{Name = "DataTransfer Speed"; Expression = {$_.LinkSpeed}} | Format-Table -AutoSize
            }

            0 {
                Write-Host -ForegroundColor DarkCyan "Finishing checking your pc resources..."
                return
            }

            default {
                Write-Host -ForegroundColor Red "Sorry you must select one of the options indicated."
            }
        }
    
    } while ($userChoice -ne 0)
}

#call function
Get-PCInformation
