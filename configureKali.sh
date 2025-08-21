#!/bin/bash

# Ideas:
# * auto customize user
# * custom background
# * fix terminal preferences

# Install bunch of custom tools and scripts

# Starttime & disksize
start=$(date +%s.%N)
TARGET="/"
USER="kali"
before_bytes=$(df "$TARGET" | awk 'NR==2 {print $3}')  # Used space

# Header
echo -e "***************************************************"
echo -e "*                                                 *"
echo -e "*              CUSTOMIZING KALI                   *"
echo -e "*                                                 *"
echo -e "***************************************************"

# Check the right priviledges
if [ "$(id -u)" -ne 0 ]; then
  echo "[!] This script needs to be ran as root, aborting"
  exit 1
fi

# Update to the latest version
sudo apt full-upgrade
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get update --fix-missing
echo -e "[x] Updated package manager to latest version"


# Remove unnecessary stuff
sudo apt remove gnome-games -y
sudo apt autoremove -y
echo -e "[x] Cleaned unnecessary packages"

# Install go-lang
sudo apt install -y golang-go


# Install additional software
sudo apt install bc
sudo apt install obsidian
sudo apt install -y nuclei
sudo apt install -y cloud-enum
sudo apt install -y seclists
sudo apt install -y pspy
sudo apt install -y \
    nodejs \
    npm \
    skipfish \
    whatweb \
    subfinder \
    dirsearch \
    ffuf \
    zaproxy \
    openvas \
    python3-fuzzywuzzy \
    hakrawler \
    hashid \
    notepadqq \
    bloodhound \
    bloodyad \
    trufflehog \
    chisel \
    httpx-toolkit \
    dirsearch \
    kerberoast \
    wafw00f \
    paramspider \
    xsser \
    cmseek \
    gobuster \
    testssl.sh \

    
sudo apt install -y libpcre3-dev 
echo -e "[x] Installed additional packages"

# Install custom scripts
cd /opt
sudo git clone https://github.com/vikas0vks/JSNinja.git
sudo git clone https://github.com/Ekultek/WhatWaf.git
sudo git clone https://github.com/sepehrdaddev/zap-scripts.git
sudo git clone https://github.com/carlospolop/PEASS-ng.git
sudo git clone https://github.com/PowerShellMafia/PowerSploit.git
sudo git clone https://github.com/devanshbatham/paramspider

# SCADA special
sudo git clone https://github.com/sourceperl/mbtget.git

echo -e "[x] Downloaded custom scripts in /opt"

# Install python modules
sudo -u "kali" pipx install uploadserver
sudo -u "kali" pipx install git-dumper
sudo -u "kali" pipx install xsstrike
sudo -u "kali" pipx install python-snap7
sudo -u "kali" pipx install scapy
sudo -u "kali" pipx install flask

cd /opt/WhatWaf
echo $USER | sudo python setup.py install
echo -e "[x] Installed additional python libaries and tools"

# Install perl modules
cd /opt/mbtget
sudo perl Makefile.PL
sudo make
sudo make install

# Ruby stuff
sudo apt upgrade -y ruby
sudo apt upgrade -y rails
sudo apt upgrade -y gem


# Install go-lang tools
go install github.com/0xTeles/jsleak/v2/jsleak@latest
go install github.com/ImAyrix/fallparams@latest
go install -v github.com/webklex/wappalyzer@main
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/rverton/webanalyze/cmd/webanalyze@latest
go install github.com/tomnomnom/waybackurls@latest
sudo cp ~/go/bin/jsleak /usr/local/bin
sudo cp ~/go/bin/fallparams /usr/local/bin
sudo cp ~/go/bin/wappalyzer /usr/local/bin
sudo cp ~/go/bin/httpx /usr/local/bin
sudo cp ~/go/bin/webanalyze /usr/local/bin
webanalyze -update
sudo cp ~/go/bin/waybackurls /usr/local/bin
echo -e "[x] Installed additional go-lang libaries and tools"


# Install firefox plugins
file=/usr/share/firefox-esr/distribution/policies.json
src=`head -n -3 $file`
ext='    },
    "Extensions": {
      "Install": [
        "https://addons.mozilla.org/firefox/downloads/file/3445870/tamper_data_for_ff_quantum-0.5.xpi",
        "https://addons.mozilla.org/firefox/downloads/file/3384326/http_header_live-0.6.5.2.xpi"
      ]
    }
  }
}'
output=`echo -e "$src\n$ext"`
echo -e "$[-] File backed-up: $file.bak"
if [ ! -f $file.bak ]; then
    sudo mv $file $file.bak
else
    echo -e "[!] Backup file already exists"
fi
echo -e "$output" > /tmp/policies.json
sudo mv /tmp/policies.json $file
sudo chown root:root $file
echo -e "[x] Added firefox plugins"

# Silence VM and make pentest less obvious (add network stuff later: https://hackmag.com/security/kali-hardening)
HOSTNAME="Actual-Intelligence"
sudo hostnamectl set-hostname $HOSTNAME
sudo systemctl stop systemd-timesyncd

LINE="127.0.1.1 $HOSTNAME"
if ! grep -q "$LINE" /etc/hosts; then
    echo "$LINE" | sudo tee -a /etc/hosts > /dev/null
else
    echo "[!] Hostname already present in /etc/hosts."
fi

# Configure and unpack some stuff
searchsploit -u
nuclei -update-templates
sudo msfdb init
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
sudo updatedb  #fix locate database, so we can find the installed stuff
echo -e "[x] Prepared, updated and initialized bunch of tools"

# Prepare staging area
cd /home/kali
mkdir staging
cd staging
cp /usr/share/pspy/* .


# Bonus nice IDE
echo "Download: https://code.visualstudio.com/download (deb file)"
echo "Execute: sudo apt install ./code_1.87.0-1709078641_amd64.deb"

# Goodbye
end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l)
runtime_minutes=$(echo "$runtime / 60" | bc -l)
after_bytes=$(df "$TARGET" | awk 'NR==2 {print $3}')
diff=$(( (after_bytes - before_bytes) / 1000 ))

echo "[x] Kali customization completed downloaded and installed  $diff MB in: $runtime_minutes minutes"
