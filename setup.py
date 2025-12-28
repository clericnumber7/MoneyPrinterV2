"""
Automated Setup Script for MoneyPrinter V2

This script provides one-command installation and setup for MoneyPrinter V2.
It handles:
- Dependency checking
- Python package installation
- System dependency verification
- Configuration file setup
- Directory structure initialization

Usage:
    python setup.py install      # Install all dependencies
    python setup.py check        # Check system dependencies only
    python setup.py config       # Run configuration wizard

Author: MoneyPrinter V2 Team
License: AGPL-3.0
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_banner():
    """Print the setup script banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              MoneyPrinter V2 - Setup Script                  ║
║                                                              ║
║         Automated Installation & Configuration Tool          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)


def check_python_version():
    """Check if Python version meets requirements"""
    print(f"\n{Colors.BOLD}Checking Python version...{Colors.END}")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 9:
        print(f"{Colors.GREEN}✓ Python {version_str} detected (meets requirement: 3.9+){Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗ Python {version_str} detected{Colors.END}")
        print(f"{Colors.YELLOW}  Python 3.9 or higher is required{Colors.END}")
        return False


def install_python_packages():
    """Install required Python packages from requirements.txt"""
    print(f"\n{Colors.BOLD}Installing Python packages...{Colors.END}")

    requirements_file = Path(__file__).parent / "requirements.txt"

    if not requirements_file.exists():
        print(f"{Colors.RED}✗ requirements.txt not found{Colors.END}")
        return False

    try:
        print(f"{Colors.CYAN}  Running: pip install -r requirements.txt{Colors.END}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Python packages installed successfully{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}✗ Failed to install Python packages{Colors.END}")
            print(f"{Colors.YELLOW}{result.stderr}{Colors.END}")
            return False

    except Exception as e:
        print(f"{Colors.RED}✗ Error installing packages: {e}{Colors.END}")
        return False


def check_system_dependencies():
    """Check for required system dependencies"""
    print(f"\n{Colors.BOLD}Checking system dependencies...{Colors.END}\n")

    dependencies = {
        "imagemagick": {
            "command": "magick" if sys.platform == "win32" else "convert",
            "name": "ImageMagick",
            "required": True,
            "install_url": "https://imagemagick.org/script/download.php"
        },
        "firefox": {
            "command": "firefox",
            "name": "Firefox",
            "required": True,
            "install_url": "https://www.mozilla.org/firefox/"
        },
        "go": {
            "command": "go",
            "name": "Go",
            "required": False,
            "install_url": "https://golang.org/dl/",
            "note": "Only required for Outreach feature"
        }
    }

    all_required_met = True
    missing_deps = []

    for key, dep in dependencies.items():
        command_exists = shutil.which(dep["command"]) is not None

        if command_exists:
            print(f"{Colors.GREEN}✓ {dep['name']} is installed{Colors.END}")
        else:
            if dep["required"]:
                print(f"{Colors.RED}✗ {dep['name']} is NOT installed [REQUIRED]{Colors.END}")
                all_required_met = False
                missing_deps.append(dep)
            else:
                print(f"{Colors.YELLOW}⚠ {dep['name']} is NOT installed [OPTIONAL]{Colors.END}")
                if "note" in dep:
                    print(f"{Colors.CYAN}  Note: {dep['note']}{Colors.END}")

    if not all_required_met:
        print(f"\n{Colors.RED}{Colors.BOLD}Missing Required Dependencies:{Colors.END}")
        for dep in missing_deps:
            print(f"\n{Colors.YELLOW}  • {dep['name']}{Colors.END}")
            print(f"    Download from: {dep['install_url']}")

    return all_required_met


def setup_config_file():
    """Create config.json from config.example.json if it doesn't exist"""
    print(f"\n{Colors.BOLD}Setting up configuration file...{Colors.END}")

    project_root = Path(__file__).parent
    config_file = project_root / "config.json"
    example_file = project_root / "config.example.json"

    if config_file.exists():
        print(f"{Colors.YELLOW}⚠ config.json already exists, skipping{Colors.END}")
        return True

    if not example_file.exists():
        print(f"{Colors.RED}✗ config.example.json not found{Colors.END}")
        return False

    try:
        # Copy example to config
        shutil.copy(str(example_file), str(config_file))
        print(f"{Colors.GREEN}✓ Created config.json from example{Colors.END}")
        print(f"{Colors.CYAN}  Please edit config.json to add your settings{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to create config.json: {e}{Colors.END}")
        return False


def setup_directory_structure():
    """Create necessary directories"""
    print(f"\n{Colors.BOLD}Setting up directory structure...{Colors.END}")

    project_root = Path(__file__).parent
    directories = [
        project_root / ".mp",
        project_root / "Songs",
        project_root / "fonts"
    ]

    for directory in directories:
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"{Colors.GREEN}✓ Created directory: {directory.name}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}✗ Failed to create {directory.name}: {e}{Colors.END}")
                return False
        else:
            print(f"{Colors.CYAN}  Directory already exists: {directory.name}{Colors.END}")

    return True


def run_configuration_wizard():
    """Interactive configuration wizard"""
    print(f"\n{Colors.BOLD}Configuration Wizard{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

    project_root = Path(__file__).parent
    config_file = project_root / "config.json"

    if not config_file.exists():
        print(f"{Colors.RED}config.json not found. Running setup first...{Colors.END}")
        setup_config_file()

    # Load current config
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"{Colors.RED}Error loading config: {e}{Colors.END}")
        return False

    print(f"{Colors.YELLOW}Leave blank to keep current value{Colors.END}\n")

    # Basic settings
    verbose = input(f"Enable verbose logging? (true/false) [{config.get('verbose', 'true')}]: ").strip()
    if verbose:
        config['verbose'] = verbose.lower() == 'true'

    headless = input(f"Run browser in headless mode? (true/false) [{config.get('headless', 'false')}]: ").strip()
    if headless:
        config['headless'] = headless.lower() == 'true'

    # LLM settings
    print(f"\n{Colors.BOLD}LLM Model Selection:{Colors.END}")
    print("  Options: gpt4, gpt35_turbo, llama2_7b, llama2_13b, llama2_70b, mixtral_8x7b")
    llm = input(f"Main LLM model [{config.get('llm', 'gpt35_turbo')}]: ").strip()
    if llm:
        config['llm'] = llm

    # Image settings
    print(f"\n{Colors.BOLD}Image Model Selection:{Colors.END}")
    print("  Options: v1, v2, v3, lexica, prodia, simurg, animefy, raava, shonin")
    image_model = input(f"Image generation model [{config.get('image_model', 'prodia')}]: ").strip()
    if image_model:
        config['image_model'] = image_model

    # Save config
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n{Colors.GREEN}✓ Configuration saved successfully{Colors.END}")
        return True
    except Exception as e:
        print(f"\n{Colors.RED}✗ Failed to save configuration: {e}{Colors.END}")
        return False


def main():
    """Main setup function"""
    print_banner()

    if len(sys.argv) < 2:
        print(f"{Colors.YELLOW}Usage:{Colors.END}")
        print(f"  python setup.py install   - Full installation")
        print(f"  python setup.py check     - Check dependencies only")
        print(f"  python setup.py config    - Run configuration wizard")
        return

    command = sys.argv[1].lower()

    if command == "check":
        # Just check dependencies
        check_python_version()
        check_system_dependencies()

    elif command == "install":
        # Full installation
        print(f"{Colors.CYAN}Starting full installation...{Colors.END}")

        steps = [
            ("Checking Python version", check_python_version),
            ("Installing Python packages", install_python_packages),
            ("Checking system dependencies", check_system_dependencies),
            ("Setting up configuration", setup_config_file),
            ("Creating directories", setup_directory_structure)
        ]

        all_success = True
        for step_name, step_func in steps:
            if not step_func():
                all_success = False
                print(f"\n{Colors.RED}✗ Setup failed at: {step_name}{Colors.END}")
                break

        if all_success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}")
            print(f"{Colors.GREEN}{Colors.BOLD}✓ Installation completed successfully!{Colors.END}")
            print(f"{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}\n")
            print(f"{Colors.CYAN}Next steps:{Colors.END}")
            print(f"  1. Edit config.json with your settings")
            print(f"  2. Run: python src/main.py")
            print(f"\n{Colors.CYAN}Optional:{Colors.END}")
            print(f"  - Run 'python setup.py config' for interactive setup")
        else:
            print(f"\n{Colors.RED}Installation incomplete. Please fix errors and try again.{Colors.END}")

    elif command == "config":
        # Run configuration wizard
        run_configuration_wizard()

    else:
        print(f"{Colors.RED}Unknown command: {command}{Colors.END}")
        print(f"{Colors.YELLOW}Valid commands: install, check, config{Colors.END}")


if __name__ == "__main__":
    main()
