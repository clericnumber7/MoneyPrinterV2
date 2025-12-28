# MoneyPrinter V2 - Installation Guide

Complete installation instructions for Windows, Debian Linux, and Ubuntu.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Manual Installation](#manual-installation)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **Internet Connection**: Required for initial setup and operation

### Required Software

1. **Python 3.9+** - Core runtime
2. **ImageMagick** - Video processing (REQUIRED)
3. **Firefox** - Browser automation (REQUIRED)
4. **Go** - Google Maps scraper (OPTIONAL - only for Outreach feature)

---

## Quick Installation

The automated setup script handles everything for you:

```bash
# 1. Clone the repository
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2

# 2. Run automated setup
python setup.py install

# 3. Configure settings
python setup.py config

# 4. Run the application
python src/main.py
```

That's it! The setup script will:
- ✅ Check Python version
- ✅ Install all Python packages
- ✅ Verify system dependencies
- ✅ Create configuration files
- ✅ Set up directory structure

---

## Manual Installation

If you prefer manual installation or need more control:

### Step 1: Install Python

**Windows:**
1. Download Python 3.9+ from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify: `python --version`

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
python3 --version
```

### Step 2: Install System Dependencies

**ImageMagick (Required)**

*Windows:*
1. Download from [imagemagick.org](https://imagemagick.org/script/download.php#windows)
2. Run installer (choose "Install legacy utilities")
3. Add to PATH
4. Verify: `magick --version`

*Debian/Ubuntu:*
```bash
sudo apt update
sudo apt install imagemagick
convert --version
```

**Firefox (Required)**

*Windows:*
1. Download from [mozilla.org/firefox](https://www.mozilla.org/firefox/)
2. Run installer
3. Verify: `firefox --version`

*Debian/Ubuntu:*
```bash
sudo apt update
sudo apt install firefox
firefox --version
```

**Go (Optional - for Outreach feature only)**

*Windows:*
1. Download from [golang.org/dl](https://golang.org/dl/)
2. Run installer
3. Verify: `go version`

*Debian/Ubuntu:*
```bash
sudo apt update
sudo apt install golang
go version
```

### Step 3: Install Python Packages

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate

# Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configuration

```bash
# Copy example configuration
cp config.example.json config.json

# Edit configuration file
# Windows: notepad config.json
# Linux: nano config.json
```

**Required Configuration:**

```json
{
  "verbose": true,
  "headless": false,
  "firefox_profile": "",
  "twitter_language": "English",
  "llm": "gpt35_turbo",
  "image_model": "prodia",
  "threads": 2,
  "is_for_kids": false,
  "imagemagick_path": "REPLACE_WITH_YOUR_PATH",
  "font": "bold_font.ttf"
}
```

**Finding ImageMagick Path:**

*Windows:*
```bash
where magick
# Example: C:\Program Files\ImageMagick-7.1.0-Q16\magick.exe
```

*Linux:*
```bash
which convert
# Example: /usr/bin/convert
```

---

## Platform-Specific Instructions

### Windows 10/11

1. **Install Visual C++ Build Tools** (for TTS)
   - Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"

2. **Firefox Profile Path**
   ```
   Press Win+R, type: %APPDATA%\Mozilla\Firefox\Profiles\
   Copy your profile path
   ```

3. **Run PowerShell as Administrator** for initial setup

### Debian 11+

```bash
# Install all dependencies
sudo apt update
sudo apt install -y \
    python3.9 \
    python3-pip \
    python3-venv \
    firefox \
    imagemagick \
    build-essential

# If you need Go for Outreach:
sudo apt install golang

# Verify installations
python3 --version
firefox --version
convert --version
```

### Ubuntu 20.04+

```bash
# Add deadsnakes PPA for Python 3.9+ (if needed)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install dependencies
sudo apt install -y \
    python3.9 \
    python3-pip \
    python3.9-venv \
    firefox \
    imagemagick \
    build-essential

# Link python3.9 as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Verify
python3 --version
firefox --version
convert --version
```

---

## Verification

After installation, verify everything works:

```bash
# 1. Check dependencies
python setup.py check

# 2. Run unit tests
python tests/run_all_tests.py

# 3. Start the application
python src/main.py
```

**Expected Output:**
```
═══════════════════════════════════════════════════════════
             SYSTEM DEPENDENCY CHECK
═══════════════════════════════════════════════════════════

✓ PYTHON [CRITICAL]
   Version: 3.9.x

✓ IMAGEMAGICK [CRITICAL]
   Path: /usr/bin/convert

✓ FIREFOX [CRITICAL]
   Path: /usr/bin/firefox

⚠ GO [OPTIONAL]
   Required for: Outreach feature only

═══════════════════════════════════════════════════════════
✓ All critical dependencies are satisfied!
═══════════════════════════════════════════════════════════
```

---

## Troubleshooting

### Common Issues

**Issue: "Python not found"**
```bash
# Windows: Reinstall Python and check "Add to PATH"
# Linux: Install python3.9 or higher
```

**Issue: "ImageMagick not found"**
```bash
# Verify installation
magick --version  # Windows
convert --version  # Linux

# If installed but not found, update config.json with full path
```

**Issue: "Firefox profile error"**
- Create a new Firefox profile specifically for the bot
- In Firefox: Menu > Profiles > Create Profile
- Use absolute path in config.json

**Issue: "Permission denied" (Linux)**
```bash
# Give execute permissions
chmod +x setup.py
chmod +x src/main.py

# Or run with python explicitly
python3 setup.py install
```

**Issue: "ModuleNotFoundError"**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

**Issue: "ImageMagick policy error"**

This affects PDF/video operations. Edit ImageMagick policy:

*Linux:*
```bash
sudo nano /etc/ImageMagick-6/policy.xml
# Comment out or remove restrictive policies
```

*Windows:*
```
Edit: C:\Program Files\ImageMagick-X.X.X\policy.xml
Comment out PDF/video restrictions
```

### Getting Help

If you encounter issues:

1. **Check logs**: Enable `"verbose": true` in config.json
2. **Run tests**: `python tests/run_all_tests.py`
3. **Check dependencies**: `python setup.py check`
4. **GitHub Issues**: [Create an issue](https://github.com/FujiwaraChoki/MoneyPrinterV2/issues)
5. **Discord**: Join the community server

---

## Next Steps

After successful installation:

1. Read [USAGE.md](USAGE.md) for operational instructions
2. Configure your social media accounts
3. Set up Firefox profiles
4. Start generating content!

---

**Installation complete!** 🎉

You're ready to start using MoneyPrinter V2. See [USAGE.md](USAGE.md) for detailed instructions on running the application.
