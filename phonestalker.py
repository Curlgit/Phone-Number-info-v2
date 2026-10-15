#!/usr/bin/env python3
"""
PhoneStalker :: OSINT Phone Number Intelligence Toolkit
--------------------------------------------------------
Offline phone-number reconnaissance tool built on Google's `phonenumbers`
(libphonenumber) library. Extracts numbering-plan metadata only:
validity, formatting, line type, assigned carrier range, geographic
region tied to the number prefix, and associated timezone(s).

This tool does NOT perform live geolocation, does NOT reveal a
subscriber's name/address, and does NOT query any external API or
network service. All data is derived from bundled, publicly published
numbering-plan metadata inside the `phonenumbers` library.

For authorized security auditing, OSINT training, and educational use
only. See DISCLAIMER.md.

Author: (add your name here)
License: MIT
"""

import sys
import time
import signal

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier as pn_carrier, timezone as pn_timezone
except ImportError:
    print("\n[!] Missing dependency: 'phonenumbers'")
    print("    Install it with: pip install phonenumbers colorama\n")
    sys.exit(1)

try:
    import colorama
    colorama.init(autoreset=False)
except ImportError:
    pass  # colorama is optional on Linux/Termux; ANSI codes work natively there


# ----------------------------------------------------------------------------
# COLOR PALETTE :: Light Gold + Green
# ----------------------------------------------------------------------------
RESET      = "\033[0m"
BOLD       = "\033[1m"
DIM        = "\033[2m"
GOLD       = "\033[38;5;221m"
GOLD_DIM   = "\033[38;5;179m"
GREEN      = "\033[38;5;114m"
GREEN_BOLD = "\033[1;38;5;82m"
RED        = "\033[38;5;203m"
GREY       = "\033[38;5;245m"
WHITE      = "\033[38;5;255m"

TERM_WIDTH = 64


# ----------------------------------------------------------------------------
# COUNTRY DATABASE :: Flag + Name + Calling Code
# ----------------------------------------------------------------------------
COUNTRIES = [
    ("🇮🇳", "India",          "+91"),
    ("🇧🇩", "Bangladesh",     "+880"),
    ("🇵🇰", "Pakistan",       "+92"),
    ("🇺🇸", "USA",            "+1"),
    ("🇬🇧", "United Kingdom", "+44"),
    ("🇨🇦", "Canada",         "+1"),
    ("🇦🇺", "Australia",      "+61"),
    ("🇩🇪", "Germany",        "+49"),
    ("🇫🇷", "France",         "+33"),
    ("🇧🇷", "Brazil",         "+55"),
    ("🇳🇬", "Nigeria",        "+234"),
    ("🇿🇦", "South Africa",   "+27"),
    ("🇨🇳", "China",          "+86"),
    ("🇯🇵", "Japan",          "+81"),
    ("🇷🇺", "Russia",         "+7"),
    ("🇮🇩", "Indonesia",      "+62"),
    ("🇲🇽", "Mexico",         "+52"),
    ("🇮🇹", "Italy",          "+39"),
    ("🇪🇸", "Spain",          "+34"),
    ("🇸🇦", "Saudi Arabia",   "+966"),
    ("🇦🇪", "UAE",            "+971"),
    ("🇪🇬", "Egypt",          "+20"),
    ("🇰🇪", "Kenya",          "+254"),
    ("🇵🇭", "Philippines",    "+63"),
    ("🇱🇰", "Sri Lanka",      "+94"),
    ("🇳🇵", "Nepal",          "+977"),
    ("🇹🇷", "Turkey",         "+90"),
    ("🇰🇷", "South Korea",    "+82"),
]

LINE_TYPE_LABELS = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line / Landline",
    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
    phonenumbers.PhoneNumberType.VOIP: "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    phonenumbers.PhoneNumberType.PAGER: "Pager",
    phonenumbers.PhoneNumberType.UAN: "UAN (Universal Access Number)",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
}


# ----------------------------------------------------------------------------
# UI HELPERS
# ----------------------------------------------------------------------------
def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def divider(char="─", color=GOLD_DIM):
    print(f"{color}{char * TERM_WIDTH}{RESET}")


def banner():
    art = f"""
{GOLD}{BOLD}   ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗
{GOLD}{BOLD}   ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝
{GOLD}{BOLD}   ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗
{GOLD}{BOLD}   ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝
{GOLD}{BOLD}   ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗
{GOLD}{BOLD}   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
{GREEN}{BOLD}        S T A L K E R   ::  OSINT Number Intel
{RESET}"""
    print(art)
    divider("═", GREEN)
    print(f"{GREY}  Offline numbering-plan intelligence · phonenumbers engine{RESET}")
    print(f"{GREY}  For authorized OSINT, research & security-audit use only{RESET}")
    divider("═", GREEN)


def main_menu():
    print()
    print(f"{GREEN_BOLD}  [1]{RESET} {WHITE}Phone Number Extract{RESET}")
    print(f"{GREEN_BOLD}  [2]{RESET} {WHITE}Exit{RESET}")
    print()
    divider()
    return input(f"{GOLD}  ➤ Select an option: {RESET}").strip()


def print_country_list():
    print()
    divider()
    print(f"{GOLD}{BOLD}  SELECT TARGET COUNTRY{RESET}")
    divider()
    cols = 1
    for idx, (flag, name, code) in enumerate(COUNTRIES, start=1):
        line = f"  {GREEN_BOLD}[{idx:>2}]{RESET} {flag}  {WHITE}{name:<18}{GOLD_DIM}{code}{RESET}"
        print(line)
    divider()


def loading_animation(stages, delay=0.35):
    """Multi-stage spinner used while 'processing' the number."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for stage in stages:
        steps = 10
        for i in range(steps):
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{GREEN}{frame}{RESET} {GOLD_DIM}{stage}{RESET}" + " " * 10)
            sys.stdout.flush()
            time.sleep(delay / steps)
        sys.stdout.write(f"\r{GREEN}✔{RESET} {GREEN}{stage}{RESET}" + " " * 12 + "\n")
        sys.stdout.flush()


PROCESS_STAGES = [
    "Initializing lookup engine",
    "Validating number structure",
    "Cross-referencing numbering plan database",
    "Resolving carrier assignment range",
    "Resolving geographic region",
    "Resolving timezone metadata",
    "Compiling intelligence report",
]


# ----------------------------------------------------------------------------
# CORE LOOKUP LOGIC
# ----------------------------------------------------------------------------
def run_lookup():
    print_country_list()
    choice = input(f"{GOLD}  ➤ Enter country number: {RESET}").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(COUNTRIES)):
        print(f"{RED}  [!] Invalid selection. Returning to main menu.{RESET}")
        time.sleep(1.2)
        return

    flag, country_name, calling_code = COUNTRIES[int(choice) - 1]

    print()
    print(f"{GREEN}  Selected: {flag} {country_name} ({calling_code}){RESET}")
    print(f"{GREY}  Enter ONLY the national number — no '+' and no country code.{RESET}")
    national_number = input(f"{GOLD}  ➤ National number: {RESET}").strip()

    # --- Input sanitation -----------------------------------------------
    cleaned = national_number.replace(" ", "").replace("-", "")
    if cleaned.startswith("+"):
        print(f"{RED}  [!] Do not include '+' or the country code — only digits.{RESET}")
        time.sleep(1.5)
        return
    if not cleaned.isdigit():
        print(f"{RED}  [!] Invalid input: only digits are allowed.{RESET}")
        time.sleep(1.5)
        return
    if not (4 <= len(cleaned) <= 14):
        print(f"{RED}  [!] Invalid length for a national number.{RESET}")
        time.sleep(1.5)
        return

    full_number = f"{calling_code}{cleaned}"

    print()
    loading_animation(PROCESS_STAGES)

    try:
        parsed = phonenumbers.parse(full_number, None)

        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)

        line_type_raw = phonenumbers.number_type(parsed)
        line_type = LINE_TYPE_LABELS.get(line_type_raw, "Unknown")

        carrier_name = pn_carrier.name_for_number(parsed, "en") or "Not available in database"
        region_desc = geocoder.description_for_number(parsed, "en") or "Not available in database"
        tzones = pn_timezone.time_zones_for_number(parsed)
        tz_str = ", ".join(tzones) if tzones else "Not available"

        display_report(
            flag, country_name, is_valid, is_possible, e164, intl,
            national, line_type, carrier_name, region_desc, tz_str
        )

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"{RED}  [!] Could not parse number: {e}{RESET}")
    except Exception as e:
        print(f"{RED}  [!] Unexpected error during analysis: {e}{RESET}")

    print()
    input(f"{GREY}  Press ENTER to return to the main menu...{RESET}")


def display_report(flag, country_name, is_valid, is_possible, e164, intl,
                    national, line_type, carrier_name, region_desc, tz_str):
    print()
    divider("═", GREEN)
    print(f"{GREEN_BOLD}  📋 INTELLIGENCE REPORT{RESET}")
    divider("═", GREEN)

    validity_color = GREEN if is_valid else RED
    validity_label = "VALID" if is_valid else "INVALID"

    rows = [
        ("Country",           f"{flag} {country_name}"),
        ("Validity",          f"{validity_color}{validity_label}{RESET}"),
        ("Possible Format",   "Yes" if is_possible else "No"),
        ("E.164 Format",      e164),
        ("International",     intl),
        ("National",          national),
        ("Line Type",         line_type),
        ("Carrier / Operator", carrier_name),
        ("Region / City",     region_desc),
        ("Timezone(s)",       tz_str),
    ]

    label_width = 20
    for label, value in rows:
        print(f"  {GOLD_DIM}{label:<{label_width}}{RESET} {WHITE}{value}{RESET}")

    divider("═", GREEN)
    print(f"{GREY}  Note: data reflects publicly assigned numbering-plan{RESET}")
    print(f"{GREY}  ranges only — not a live subscriber lookup.{RESET}")
    divider("═", GREEN)


# ----------------------------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------------------------
def handle_sigint(sig, frame):
    print(f"\n\n{RED}[!] Interrupted by user. Exiting PhoneStalker safely.{RESET}\n")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, handle_sigint)

    while True:
        try:
            clear_screen()
            banner()
            choice = main_menu()

            if choice == "1":
                run_lookup()
            elif choice == "2":
                print(f"\n{GREEN}  Goodbye. Stay ethical. 👋{RESET}\n")
                break
            else:
                print(f"{RED}  [!] Invalid option. Choose 1 or 2.{RESET}")
                time.sleep(1)

        except KeyboardInterrupt:
            handle_sigint(None, None)
        except Exception as e:
            print(f"\n{RED}[!] Unexpected error: {e}{RESET}")
            time.sleep(1.5)


if __name__ == "__main__":
    main()
