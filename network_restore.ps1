# ------------------------------
# AUTO ADMIN ELEVATION
# ------------------------------
if (-not ([Security.Principal.WindowsPrincipal] `
[Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
[Security.Principal.WindowsBuiltInRole]::Administrator))
{
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# ------------------------------
# REPORT FILE
# ------------------------------
$report = "$env:USERPROFILE\Desktop\network_restore_report.txt"

"===== NETWORK RESTORE REPORT =====" | Out-File $report
"Date: $(Get-Date)" | Out-File $report -Append
"" | Out-File $report -Append

Write-Host ""
Write-Host "=== NETWORK RESTORE TOOL ==="
Write-Host "Report file: $report"
Write-Host ""

# ------------------------------
# FUNCTION FOR COMMANDS
# ------------------------------
function Run-Step {

    param (
        [string]$desc,
        [scriptblock]$cmd
    )

    Write-Host "[RUN] $desc"

    try {

        $output = & $cmd 2>&1

        if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq $null) {

            Write-Host "[SUCCESS]"
            "[SUCCESS] $desc" | Out-File $report -Append

        } else {

            Write-Host "[FAILED]"
            "[FAILED] $desc" | Out-File $report -Append

        }

        if ($output) {
            $output | Out-File $report -Append
        }

    } catch {

        Write-Host "[FAILED]"
        "[FAILED] $desc" | Out-File $report -Append
        $_ | Out-File $report -Append
    }

    "" | Out-File $report -Append
}

# ------------------------------
# DNS RESET
# ------------------------------
Run-Step "Reset IPv4 DNS on active adapters" {
    Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object {
        Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses
    }
}

Run-Step "Reset IPv6 DNS" {
    Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object {
        netsh interface ipv6 set dnsservers name="$($_.Name)" source=dhcp
    }
}

# ------------------------------
# REMOVE DNS OVER HTTPS
# ------------------------------
Run-Step "Remove DoH config 1.1.1.1" {
    netsh dns delete encryption server=1.1.1.1
}

Run-Step "Remove DoH config 1.0.0.1" {
    netsh dns delete encryption server=1.0.0.1
}

Run-Step "Remove AutoDoH registry key" {
    reg delete "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v EnableAutoDoh /f
}

# ------------------------------
# RESTORE DNS POLICIES
# ------------------------------
Run-Step "Restore LLMNR policy" {
    reg delete "HKLM\Software\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /f
}

Run-Step "Restore mDNS policy" {
    reg delete "HKLM\Software\Policies\Microsoft\Windows NT\DNSClient" /v EnableMDNS /f
}

Run-Step "Restore SmartNameResolution policy" {
    reg delete "HKLM\Software\Policies\Microsoft\Windows NT\DNSClient" /v DisableSmartNameResolution /f
}

# ------------------------------
# RESTORE SUFFIX DEVOLUTION
# ------------------------------
Run-Step "Restore DNS suffix devolution" {
    reg delete "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v UseDomainNameDevolution /f
}

# ------------------------------
# RE-ENABLE NETBIOS
# ------------------------------
Run-Step "Re-enable NetBIOS" {
    wmic nicconfig where IPEnabled=true call SetTcpipNetbios 0
}

# ------------------------------
# NETWORK STACK RESET
# ------------------------------
Run-Step "Reset Winsock" {
    netsh winsock reset
}

Run-Step "Reset TCP/IP stack" {
    netsh int ip reset
}

# ------------------------------
# NETWORK REFRESH
# ------------------------------
Run-Step "Flush DNS cache" {
    ipconfig /flushdns
}

Run-Step "Release DHCP lease" {
    ipconfig /release
}

Run-Step "Renew DHCP lease" {
    ipconfig /renew
}

# ------------------------------
# DIAGNOSTIC REPORT
# ------------------------------
Run-Step "Collect ipconfig /all" {
    ipconfig /all
}

Run-Step "Collect DNS encryption status" {
    netsh dns show encryption
}

Run-Step "Collect network adapters" {
    Get-NetAdapter
}

Write-Host ""
Write-Host "=== SCRIPT COMPLETE ==="
Write-Host "Report saved to Desktop."
Write-Host "Restart the computer now."