import subprocess
import ctypes
import sys
import re

VERSION = "1.0"


# -----------------------------
# Admin check
# -----------------------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# -----------------------------
# Command runner
# -----------------------------

def run(cmd, desc):

    print(f"\n[+] {desc}")

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("[OK]")
        if result.stdout.strip():
            print(result.stdout.strip())
    else:
        print("[ERROR]")
        print(result.stderr)


# -----------------------------
# Detect active network adapter
# -----------------------------

def get_active_adapter():

    result = subprocess.run(
        "netsh interface show interface",
        shell=True,
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():

        if "Connected" in line and ("Dedicated" in line or "Ethernet" in line):

            parts = re.split(r"\s{2,}", line.strip())

            if len(parts) >= 4:
                return parts[-1]

    return None


# -----------------------------
# Configure Cloudflare DNS
# -----------------------------

def configure_dns(adapter):

    run(
        f'netsh interface ipv4 set dnsservers name="{adapter}" static 1.1.1.1',
        "Setting Cloudflare primary DNS"
    )

    run(
        f'netsh interface ipv4 add dnsservers name="{adapter}" 1.0.0.1 index=2',
        "Setting Cloudflare secondary DNS"
    )


def configure_ipv6_dns(adapter):

    run(
        f'netsh interface ipv6 set dnsservers "{adapter}" static 2606:4700:4700::1111',
        "Setting Cloudflare IPv6 DNS"
    )

    run(
        f'netsh interface ipv6 add dnsservers "{adapter}" 2606:4700:4700::1001 index=2',
        "Setting secondary IPv6 DNS"
    )


# -----------------------------
# Enable DNS over HTTPS
# -----------------------------

def enable_doh():

    run(
        'netsh dns add encryption server=1.1.1.1 dohtemplate=https://cloudflare-dns.com/dns-query autoupgrade=yes',
        "Enabling DoH for 1.1.1.1"
    )

    run(
        'netsh dns add encryption server=1.0.0.1 dohtemplate=https://cloudflare-dns.com/dns-query autoupgrade=yes',
        "Enabling DoH for 1.0.0.1"
    )

    run(
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters" /v EnableAutoDoh /t REG_DWORD /d 2 /f',
        "Enabling automatic DoH upgrade"
    )


# -----------------------------
# Disable insecure protocols
# -----------------------------

def disable_netbios():

    run(
        'powershell -Command "Get-WmiObject Win32_NetworkAdapterConfiguration | Where {$_.IPEnabled -eq $true} | ForEach {$_.SetTcpipNetbios(2)}"',
        "Disabling NetBIOS"
    )


def disable_llmnr():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f',
        "Disabling LLMNR"
    )


def disable_mdns():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v EnableMDNS /t REG_DWORD /d 0 /f',
        "Disabling mDNS"
    )


def disable_smart_dns():

    run(
        'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows NT\\DNSClient" /v DisableSmartNameResolution /t REG_DWORD /d 1 /f',
        "Disabling Smart Multi-Homed Name Resolution"
    )


def disable_suffix_devolution():

    run(
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters" /v UseDomainNameDevolution /t REG_DWORD /d 0 /f',
        "Disabling DNS suffix devolution"
    )


# -----------------------------
# Refresh network
# -----------------------------

def refresh_network():

    run("ipconfig /flushdns", "Flushing DNS cache")
    run("ipconfig /renew", "Renewing DHCP lease")


# -----------------------------
# Security report
# -----------------------------

def report():

    print("\n===== DNSentinel Security Report =====")

    subprocess.run("ipconfig /all", shell=True)
    subprocess.run("netsh dns show encryption", shell=True)

    print("\nTest DNS manually with:")
    print("nslookup google.com.")

    print("\nOnline DNS leak test:")
    print("https://dnsleaktest.com")

    print("\n=====================================")


# -----------------------------
# Restore defaults
# -----------------------------

def restore(adapter):

    run(
        f'netsh interface ipv4 set dnsservers name="{adapter}" source=dhcp',
        "Restoring default DNS settings"
    )

    print("\nDefault DNS restored.")


# -----------------------------
# Main
# -----------------------------

def main():

    print(f"\nDNSentinel v{VERSION}")
    print("Windows DNS Privacy Hardening Tool\n")

    if not is_admin():
        print("Please run DNSentinel as Administrator.")
        input("Press Enter to exit...")
        sys.exit()

    adapter = get_active_adapter()

    if not adapter:
        print("Could not detect active network adapter.")
        input("Press Enter to exit...")
        sys.exit()

    print(f"Detected network adapter: {adapter}")

    print("\n1) Harden DNS configuration")
    print("2) Restore default DNS")
    print("3) Exit")

    choice = input("\nSelect option: ")

    if choice == "1":

        print("\nDNSentinel will apply the following changes:")
        print("- Cloudflare DNS (1.1.1.1 / 1.0.0.1)")
        print("- Cloudflare IPv6 DNS")
        print("- DNS over HTTPS")
        print("- Disable NetBIOS")
        print("- Disable LLMNR")
        print("- Disable mDNS")
        print("- Disable Smart DNS fallback")

        confirm = input("\nContinue? (y/n): ")

        if confirm.lower() != "y":
            sys.exit()

        configure_dns(adapter)
        configure_ipv6_dns(adapter)

        enable_doh()

        disable_netbios()
        disable_llmnr()
        disable_mdns()
        disable_smart_dns()
        disable_suffix_devolution()

        refresh_network()

        report()

    elif choice == "2":

        restore(adapter)

    else:
        sys.exit()

    print("\nDNSentinel completed.")


if __name__ == "__main__":
    main()
