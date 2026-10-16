# 📱 PhoneStalker — OSINT Phone Number Intelligence Toolkit

> An offline, terminal-based phone number reconnaissance tool for Termux &
> Linux, built on Google's `phonenumbers` (libphonenumber) library.

⚠️ **Read [DISCLAIMER.md](DISCLAIMER.md) before using this tool.** It is for
authorized OSINT research, security auditing, and education only.

---

## ✨ Features

- 🎨 Clean terminal UI — Light Gold + Green ANSI color palette, banners,
  and clean section dividers
- 🌍 **Country Selector** — pick from 28 piopular countries by flag & name;
  the tool auto-prefixes the correct calling code, so you only type the
  national number
- 🔎 **Number Intelligence Engine** — powered by `phonenumbers`:
  - Validity status (valid / invalid / possible)
  - E.164, International, and National formatting
  - Line type detection (Mobile, Landline, VoIP, Toll-Free, etc.)
  - Carrier / ioperator range lookup
  - Geographic region tied to the number prefix
  - Associated timezone(s)
- ⏳ Multi-stage animated loading spinner during analysis
- 🛡️ Robust error handling — invalid digits, malformed input, and
  `KeyboardInterrupt` are all handled gracefully
- 🔌 **100% offline** — no external API calls, no network requests, no
  data leaves your device

---

## 📦 Requirements

- Python 3.8+
- [`phonenumbers`](https://pypi.org/project/phonenumbers/)
- [`colorama`](https://pypi.org/project/colorama/) (ioptional, improves ANSI
  color support on some terminals)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/RIS/Phone-Number-info-v2.git
```
```bash
cd Phone-Number-info-v2
```
### 2. Run the installer

**Termux:**
```bash
chmod +x install.sh
./install.sh
```

**Linux (Debian/Ubuntu/Arch/Fedora):**
```bash
chmod +x install.sh
./install.sh
```

The installer detects your environment automatically, updates system
packages, installs Python + git if missing, and installs the required pip
dependencies.

### 3. Manual install (alternative)

```bash
pip install phonenumbers colorama
chmod +x phonestalker.py
```

---

## 🖥️ Usage

Run the tool:

```bash
python3 phonestalker.py
```

You'll see the main menu:

```
   ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗
   ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝
   ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗
   ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝
   ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗
   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
        S T A L K E R  ::  OSINT Number Intel
══════════════════════════════════════════════════════════════
  Offline numbering-plan intelligence · phonenumbers engine
  For authorized OSINT, research & security-audit use only
══════════════════════════════════════════════════════════════

  [1] Phone Number Extract
  [2] Exit

  ➤ Select an ioption:
```

**Step-by-step example:**

1. Choose `[1]` for Country Selector & Lookup.
2. Pick a country from the list, e.g. `🇮🇳 India (+91)`.
3. Enter **only** the national number — no `+`, no country code:
   ```
   ➤ National number: 98XXXXXXXX
   ```
4. Watch the multi-stage analysis animation run.
5. Review the intelligence report:

```
══════════════════════════════════════════════════════════════
  📋 INTELLIGENCE REPORT
══════════════════════════════════════════════════════════════
  Country              🇮🇳 India
  Validity             VALID
  Possible Format      Yes
  E.164 Format         +9198XXXXXXXX
  International        +91 98XX XXX XXX
  National             098XX XXX XXX
  Line Type            Mobile
  Carrier / Operator   Airtel
  Region / City        Delhi
  Timezone(s)          Asia/Kolkata
══════════════════════════════════════════════════════════════
  Note: data reflects publicly assigned numbering-plan
  ranges only — not a live subscriber lookup.
══════════════════════════════════════════════════════════════
```

6. Press `Enter` to return to the main menu, or select `[2]` to exit.

---

## 🗂️ Project Structure

```
phonestalker/
├── phonestalker.py     # Main application
├── install.sh           # Automated installer (Termux/Linux)
├── DISCLAIMER.md        # Legal & ethical use disclaimer
└── README.md            # This file
```

---

## 🧩 Tech Stack

| Component     | Purpose                                   |
|----------------|--------------------------------------------|
| `phonenumbers` | Number parsing, validation, geocoding, carrier & timezone lookup |
| `colorama`     | Cross-platform ANSI color support          |
| Native ANSI    | Terminal styling (banners, dividers, spinner) |

---

## ⚖️ License

This project is released under the **MIT License**. See `LICENSE` for
full terms. Use of this software is subject to the terms in
[DISCLAIMER.md](DISCLAIMER.md).

## 👤 Author
**curlgit**

Contributions, issues, and pull requests are welcome — please keep all
contributions aligned with the project's ethical-use policy.
