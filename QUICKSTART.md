# MoneyPrinter V2 - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

Before starting, make sure you have:
- Python 3.9 or higher installed
- Internet connection

## Installation (3 Steps)

### Step 1: Download the Code

```bash
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2
```

### Step 2: Run Automated Setup

```bash
python setup.py install
```

This will:
- ✅ Install all Python packages
- ✅ Check your system dependencies
- ✅ Create configuration files
- ✅ Set up directories

**Expected output:**
```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              MoneyPrinter V2 - Setup Script                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

✓ Python 3.9.x detected (meets requirement: 3.9+)
✓ Python packages installed successfully
✓ ImageMagick is installed
✓ Firefox is installed
✓ Created config.json from example
✓ Created directory: .mp
✓ Created directory: Songs

============================================================
✓ Installation completed successfully!
============================================================
```

### Step 3: Configure

```bash
python setup.py config
```

Or manually edit `config.json`:

```json
{
  "verbose": true,
  "headless": false,
  "firefox_profile": "/path/to/your/firefox/profile",
  "imagemagick_path": "/path/to/imagemagick"
}
```

**Finding Firefox Profile:**
- Open Firefox
- Type `about:profiles` in URL bar
- Copy "Root Directory" path

**Finding ImageMagick Path:**
```bash
# Windows
where magick

# Linux/Mac
which convert
```

## First Run

```bash
python src/main.py
```

You'll see:

```
============ OPTIONS ============
 1. YouTube Shorts Automation
 2. Twitter Bot
 3. Affiliate Marketing
 4. Outreach
 5. Quit
=================================

Select an option:
```

## Quick Test

### Test YouTube Automation

1. Select option `1` (YouTube Shorts)
2. Choose "Create new account"
3. Follow prompts:
   - Nickname: `Test Channel`
   - Firefox Profile: (paste your profile path)
   - Niche: `Technology`
   - Language: `English`
   - Image Gen: `1` (G4F)
4. Select `1` (Upload Short)
5. Wait for video generation (2-5 minutes)
6. Review generated video in `.mp/` folder

### Test Twitter Bot

1. Select option `2` (Twitter Bot)
2. Choose "Create new account"
3. Follow prompts:
   - Nickname: `Test Bot`
   - Firefox Profile: (paste your profile path)
   - Topic: `AI and Technology`
4. Select `1` (Post something)
5. Watch bot generate and post tweet

## Troubleshooting

### "ImageMagick not found"

**Windows:**
1. Download from [imagemagick.org](https://imagemagick.org/script/download.php)
2. Install with "Install legacy utilities" option
3. Add to PATH
4. Update `imagemagick_path` in config.json

**Linux:**
```bash
sudo apt install imagemagick
```

### "Firefox profile error"

1. Open Firefox
2. Go to `about:profiles`
3. Create a new profile named "MoneyPrinterBot"
4. Log into your social media accounts
5. Copy profile path to config.json

### "Python package errors"

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

## Next Steps

Once everything works:

1. **Read the full documentation:**
   - [INSTALLATION.md](docs/INSTALLATION.md) - Detailed setup
   - [USAGE.md](docs/USAGE.md) - Feature guides

2. **Run tests:**
   ```bash
   python tests/run_all_tests.py
   ```

3. **Set up automation:**
   - Use CRON jobs for scheduled posting
   - See docs/USAGE.md#cron-jobs-scheduling

4. **Optimize settings:**
   - Adjust `threads` in config.json for faster video processing
   - Choose different AI models
   - Customize content generation

## Support

Need help?

- 📖 **Documentation:** [docs/](docs/)
- 🐛 **Issues:** [GitHub Issues](https://github.com/FujiwaraChoki/MoneyPrinterV2/issues)
- 💬 **Community:** [Discord](https://dsc.gg/fuji-community)

## Quick Reference

**Verify Installation:**
```bash
python setup.py check
```

**Run Tests:**
```bash
python tests/run_all_tests.py
```

**Start Application:**
```bash
python src/main.py
```

**Configuration:**
```bash
python setup.py config
```

---

**You're all set!** 🚀 Start generating content and growing your online presence!
