# MoneyPrinter V2

> ♥︎ **Sponsor**: The Best AI Chat App: [shiori.ai](https://www.shiori.ai)

---

> 𝕏 Also, follow me on X: [@DevBySami](https://x.com/DevBySami).

[![madewithlove](https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=orange)](https://github.com/FujiwaraChoki/MoneyPrinterV2)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-brightgreen?logo=buymeacoffee)](https://www.buymeacoffee.com/fujicodes)
[![GitHub license](https://img.shields.io/github/license/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/issues)
[![GitHub stars](https://img.shields.io/github/stars/FujiwaraChoki/MoneyPrinterV2?style=for-the-badge)](https://github.com/FujiwaraChoki/MoneyPrinterV2/stargazers)
[![Discord](https://img.shields.io/discord/1134848537704804432?style=for-the-badge)](https://dsc.gg/fuji-community)

An Application that automates the process of making money online.

MPV2 (MoneyPrinter Version 2) is, as the name suggests, the second version of the MoneyPrinter project. It is a complete rewrite of the original project, with a focus on a wider range of features and a more modular architecture.

> **Note:** MPV2 requires Python 3.9+ to function effectively.
> Watch the YouTube video [here](https://youtu.be/wAZ_ZSuIqfk)

## ✨ What's New in This Version

This is an **enterprise-grade refactored version** with significant improvements:

### 🔧 Fixed Issues
- ✅ Removed broken `selenium_firefox` dependencies
- ✅ Fixed subprocess command execution bugs
- ✅ Implemented proper CRON job scheduling
- ✅ Fixed cache management bugs
- ✅ Added proper error handling throughout
- ✅ Fixed platform-specific command issues
- ✅ Resolved recursive function call issues

### 🌍 Cross-Platform Support
- ✅ Full Windows 10/11 support
- ✅ Debian Linux compatibility
- ✅ Ubuntu compatibility (20.04+)
- ✅ Automatic platform detection
- ✅ Cross-platform process management

### 📚 Documentation & Testing
- ✅ Comprehensive installation guide
- ✅ Detailed usage instructions
- ✅ Unit tests for core functionality
- ✅ Enterprise-level code documentation
- ✅ Automated setup script

### 🚀 Developer Experience
- ✅ One-command installation: `python setup.py install`
- ✅ Dependency verification tool
- ✅ Configuration wizard
- ✅ Test suite included

## Features

- [x] Twitter Bot (with CRON Jobs => `scheduler`)
- [x] YouTube Shorts Automater (with CRON Jobs => `scheduler`)
- [x] Affiliate Marketing (Amazon + Twitter)
- [x] Find local businesses & cold outreach

## Quick Start

### One-Command Installation

```bash
# Clone the repository
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2

# Run automated setup
python setup.py install

# Configure your settings
python setup.py config

# Start the application
python src/main.py
```

That's it! The setup script handles everything automatically.

### What Gets Installed

The setup script will:
1. ✅ Verify Python 3.9+ is installed
2. ✅ Install all Python dependencies
3. ✅ Check for ImageMagick (required)
4. ✅ Check for Firefox (required)
5. ✅ Check for Go (optional, for Outreach)
6. ✅ Create configuration files
7. ✅ Set up directory structure

## System Requirements

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| Python | 3.9+ | Core runtime | [python.org](https://python.org) |
| ImageMagick | Latest | Video processing | [imagemagick.org](https://imagemagick.org) |
| Firefox | Latest | Browser automation | [mozilla.org/firefox](https://mozilla.org/firefox) |
| Go | Latest | Outreach (optional) | [golang.org](https://golang.org) |

### Minimum Hardware

- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Broadband connection

## Platform-Specific Installation

### Windows 10/11

```bash
# 1. Install Python 3.9+ from python.org (check "Add to PATH")
# 2. Install ImageMagick from imagemagick.org
# 3. Install Firefox from mozilla.org
# 4. Install Visual C++ Build Tools for TTS

# Then run setup
python setup.py install
```

### Debian/Ubuntu Linux

```bash
# Install dependencies
sudo apt update
sudo apt install -y python3.9 python3-pip python3-venv firefox imagemagick build-essential

# Clone and setup
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git
cd MoneyPrinterV2
python3 setup.py install
```

## Documentation

### 📖 Complete Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup for all platforms
- **[Usage Guide](docs/USAGE.md)** - How to use all features
- **[Configuration](docs/Configuration.md)** - All configuration options
- **[Roadmap](docs/Roadmap.md)** - Future features

### 🧪 Testing

Run the test suite to verify your installation:

```bash
python tests/run_all_tests.py
```

### 🔍 Dependency Check

Verify all dependencies are installed:

```bash
python setup.py check
```

## Usage

```bash
# Run the application
python src/main.py

# You'll see the main menu:
# 1. YouTube Shorts Automation
# 2. Twitter Bot
# 3. Affiliate Marketing
# 4. Outreach
# 5. Quit
```

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md).

## Configuration

The application uses `config.json` for configuration. On first run, it's created from `config.example.json`.

### Quick Configuration

```bash
# Interactive configuration wizard
python setup.py config
```

### Manual Configuration

Edit `config.json`:

```json
{
  "verbose": true,
  "headless": false,
  "firefox_profile": "/path/to/firefox/profile",
  "twitter_language": "English",
  "llm": "gpt35_turbo",
  "image_model": "prodia",
  "threads": 2,
  "imagemagick_path": "/usr/bin/convert"
}
```

See [docs/Configuration.md](docs/Configuration.md) for all options.

## Troubleshooting

### Common Issues

**"ImageMagick not found"**
```bash
# Verify installation
magick --version  # Windows
convert --version # Linux

# Install if missing
# Windows: Download from imagemagick.org
# Linux: sudo apt install imagemagick
```

**"Firefox profile error"**
- Create a dedicated Firefox profile
- In Firefox: `about:profiles` → Create New Profile
- Copy profile path to config.json

**"Permission denied" (Linux)**
```bash
chmod +x setup.py src/main.py
```

For more help, see [docs/INSTALLATION.md#troubleshooting](docs/INSTALLATION.md#troubleshooting).

## Development

### Project Structure

```
MoneyPrinterV2/
├── src/
│   ├── main.py              # Main application entry point
│   ├── platform_utils.py    # Cross-platform utilities (NEW)
│   ├── utils_fixed.py       # Fixed utilities (NEW)
│   ├── cache_fixed.py       # Fixed cache management (NEW)
│   └── classes/             # Feature implementations
├── tests/                   # Unit tests (NEW)
│   ├── test_platform_utils.py
│   ├── test_cache.py
│   └── run_all_tests.py
├── docs/                    # Documentation
│   ├── INSTALLATION.md      # Installation guide (NEW)
│   ├── USAGE.md            # Usage guide (NEW)
│   └── Configuration.md     # Config reference
├── setup.py                # Automated setup script (NEW)
└── config.json             # User configuration
```

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test file
python tests/test_platform_utils.py
python tests/test_cache.py
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. Check out [docs/Roadmap.md](docs/Roadmap.md) for a list of features that need to be implemented.

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versions

MoneyPrinter has different versions for multiple languages developed by the community for the community. Here are some known versions:

- Chinese: [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

If you would like to submit your own version/fork of MoneyPrinter, please open an issue describing the changes you made to the fork.

## License

MoneyPrinterV2 is licensed under `Affero General Public License v3.0`. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- [CoquiTTS](https://github.com/coqui-ai/TTS)
- [gpt4free](https://github.com/xtekky/gpt4free)
- All contributors who helped improve this version

## Disclaimer

This project is for educational purposes only. The author will not be responsible for any misuse of the information provided. All the information on this website is published in good faith and for general information purpose only. The author does not make any warranties about the completeness, reliability, and accuracy of this information. Any action you take upon the information you find on this website (FujiwaraChoki/MoneyPrinterV2), is strictly at your own risk. The author will not be liable for any losses and/or damages in connection with the use of our website.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/FujiwaraChoki/MoneyPrinterV2/issues)
- **Discord**: [Join our community](https://dsc.gg/fuji-community)
- **Sponsor**: [Buy me a coffee](https://www.buymeacoffee.com/fujicodes)

**Made with ❤️ by the MoneyPrinter V2 team**
