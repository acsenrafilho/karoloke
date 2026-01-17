# Karol-Oke

![Project Logo](docs/assets/karoloke-logo.png)

[![CI for Develop Branch](https://github.com/acsenrafilho/karoloke/actions/workflows/ci_develop.yaml/badge.svg)](https://github.com/acsenrafilho/karoloke/actions/workflows/ci_develop.yaml)
[![CI for Production Branch](https://github.com/acsenrafilho/karoloke/actions/workflows/ci_main.yaml/badge.svg)](https://github.com/acsenrafilho/karoloke/actions/workflows/ci_main.yaml)
[![codecov](https://codecov.io/gh/acsenrafilho/karoloke/graph/badge.svg?token=1PL6N4BI2G)](https://codecov.io/gh/acsenrafilho/karoloke)
![Python Versions](https://img.shields.io/badge/python-3.9%20|+-blue)
![PyPI downloads](https://img.shields.io/pypi/dm/karoloke)
[![Issues](https://img.shields.io/github/issues/acsenrafilho/karoloke)](https://github.com/acsenrafilho/karoloke/issues)
![Contributors](https://img.shields.io/github/contributors/acsenrafilho/karoloke)
[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️%20acsenrafilho-orange?logo=github)](https://github.com/sponsors/acsenrafilho)

A simple and easy-to-use Music Player for your karaoke parties! Play videos with synchronized lyrics and have fun with your friends.

## Quick Start

### Download Pre-built Executable (Recommended)

Download the latest release for your platform from [GitHub Releases](https://github.com/acsenrafilho/karoloke/releases):

**Linux:**
```bash
chmod +x karoloke-v*-linux
./karoloke-v*-linux
```

**macOS:**
```bash
chmod +x karoloke-v*-macos
./karoloke-v*-macos
```

**Windows:**
Double-click `karoloke-v*-windows.exe` to run.

### Installation from Source

- Requires **Python 3.9+**
- Install via pip:
  ```bash
  pip install karoloke
  ```

## Usage

- Start the application:
  ```bash
  karoloke
  ```
- The server will start locally and open in your default browser
- Configure your video directory by clicking the settings button (top-right corner)
- Supported formats: `.mp4`, `.webm`, `.ogg`
- Select a song number and press Enter to start playing
- The video player is responsive and works on all screen sizes

## Troubleshooting

### Windows

**Antivirus False Positive:**
If Windows Defender or your antivirus flags the executable:
1. Click "More info" in the SmartScreen warning
2. Click "Run anyway"
3. Alternatively, add an exclusion for the karoloke executable in Windows Security

### macOS

**Gatekeeper Warning (Unsigned Executable):**
If you see "cannot be opened because the developer cannot be verified":
1. Right-click the executable file
2. Select "Open" from the context menu
3. Click "Open" in the dialog
4. The app will now be allowed to run

Alternatively, use Terminal:
```bash
xattr -d com.apple.quarantine karoloke-v*-macos
```

### Linux

**GLIBC Compatibility:**
The executable is built on Ubuntu and requires GLIBC 2.31+. If you encounter errors:
```bash
./karoloke-v*-linux: /lib/x86_64-linux-gnu/libc.so.6: version 'GLIBC_2.XX' not found
```
Solution: Install from source using pip or use a newer Linux distribution.

**Permission Denied:**
Make sure the file is executable:
```bash
chmod +x karoloke-v*-linux
```

## Documentation

Full documentation is available at [ReadTheDocs](https://karoloke.readthedocs.io).

## Contributors

Thank you all the special people that invested their time and knowledge to improve this project. 👏

![Contributors](https://contrib.rocks/image?repo=acsenrafilho/karoloke)
