#!/usr/bin/env bash
# ------------------------------------------------------------------------
# PhoneStalker :: Automated Installer
# Supports: Termux (Android) and generic Linux (Debian/Ubuntu/Arch/Fedora)
# ------------------------------------------------------------------------

set -e

GOLD='\033[38;5;221m'
GREEN='\033[38;5;114m'
RED='\033[38;5;203m'
RESET='\033[0m'

echo -e "${GOLD}==============================================${RESET}"
echo -e "${GOLD}   PhoneStalker :: Installer${RESET}"
echo -e "${GOLD}==============================================${RESET}"

# --- Detect environment ---------------------------------------------------
if command -v pkg >/dev/null 2>&1; then
    ENV_TYPE="termux"
elif command -v apt >/dev/null 2>&1; then
    ENV_TYPE="debian"
elif command -v pacman >/dev/null 2>&1; then
    ENV_TYPE="arch"
elif command -v dnf >/dev/null 2>&1; then
    ENV_TYPE="fedora"
else
    ENV_TYPE="unknown"
fi

echo -e "${GREEN}[*] Detected environment: ${ENV_TYPE}${RESET}"

# --- Update & install system packages --------------------------------------
case "$ENV_TYPE" in
    termux)
        echo -e "${GREEN}[*] Updating Termux packages...${RESET}"
        pkg update -y && pkg upgrade -y
        echo -e "${GREEN}[*] Installing python & git...${RESET}"
        pkg install -y python git
        ;;
    debian)
        echo -e "${GREEN}[*] Updating apt packages...${RESET}"
        sudo apt update -y && sudo apt upgrade -y
        echo -e "${GREEN}[*] Installing python3, pip & git...${RESET}"
        sudo apt install -y python3 python3-pip git
        ;;
    arch)
        echo -e "${GREEN}[*] Updating pacman packages...${RESET}"
        sudo pacman -Syu --noconfirm
        echo -e "${GREEN}[*] Installing python & git...${RESET}"
        sudo pacman -S --noconfirm python python-pip git
        ;;
    fedora)
        echo -e "${GREEN}[*] Updating dnf packages...${RESET}"
        sudo dnf upgrade -y
        echo -e "${GREEN}[*] Installing python3, pip & git...${RESET}"
        sudo dnf install -y python3 python3-pip git
        ;;
    *)
        echo -e "${RED}[!] Unrecognized package manager.${RESET}"
        echo -e "${RED}    Please ensure python3 and pip are installed manually.${RESET}"
        ;;
esac

# --- Python dependencies -----------------------------------------------
echo -e "${GREEN}[*] Upgrading pip...${RESET}"
if command -v pip3 >/dev/null 2>&1; then
    PIP_BIN="pip3"
else
    PIP_BIN="pip"
fi

$PIP_BIN install --upgrade pip

echo -e "${GREEN}[*] Installing Python dependencies (phonenumbers, colorama)...${RESET}"
$PIP_BIN install phonenumbers colorama

# --- Permissions ---------------------------------------------------------
if [ -f "phonestalker.py" ]; then
    chmod +x phonestalker.py
    echo -e "${GREEN}[*] Set executable permission on phonestalker.py${RESET}"
else
    echo -e "${RED}[!] phonestalker.py not found in current directory.${RESET}"
    echo -e "${RED}    Run this script from inside the cloned repository.${RESET}"
fi

echo -e "${GOLD}==============================================${RESET}"
echo -e "${GREEN}[✔] Installation complete!${RESET}"
echo -e "${GOLD}Run the tool with:${RESET} python3 phonestalker.py"
echo -e "${GOLD}==============================================${RESET}"
