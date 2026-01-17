# Welcome to Karol-Oke 🎤

**Turn your computer into a karaoke machine in minutes!**

Karol-Oke is a simple, ready-to-use karaoke application that lets you play video karaoke files with synchronized lyrics. Perfect for parties, family gatherings, or just having fun at home!

---

## 🚀 Quick Start for End Users

### Step 1: Download Karol-Oke

Get the latest version for your operating system:

👉 **[Download from GitHub Releases](https://github.com/acsenrafilho/karoloke/releases/latest)**

Choose the file for your system:
- **Windows**: `karoloke-v*-windows.exe`
- **macOS**: `karoloke-v*-macos`
- **Linux**: `karoloke-v*-linux`

---

### Step 2: Prepare Your Karaoke Videos

> **⚠️ Important: Karol-Oke does NOT include karaoke songs!**
>
> You need to provide your own video karaoke files. The app supports:
> - **MP4** files (`.mp4`)
> - **WebM** files (`.webm`)
> - **OGG** files (`.ogg`)

**Where to get karaoke videos:**
- Purchase from legal karaoke video providers
- Use your existing karaoke DVD/CD collection (convert to digital format)
- Create your own videos with lyrics overlay
- Search for legal, free karaoke content online

**Organize your files:**
1. Create a folder on your computer (e.g., `C:\Karaoke` or `/home/user/karaoke`)
2. Place all your video files in this folder
3. Optionally, use subfolders to organize by artist, genre, etc.
4. Name files with song numbers for easy selection (e.g., `0001.mp4`, `0002.mp4`)

---

### Step 3: Run Karol-Oke

#### **Windows**

1. Double-click `karoloke-v*-windows.exe`
2. If Windows Defender shows a warning:
   - Click **"More info"**
   - Click **"Run anyway"**
3. The app will open in your default web browser automatically

#### **macOS**

1. Open Terminal and navigate to the download folder
2. Make the file executable:
   ```bash
   chmod +x karoloke-v*-macos
   ```
3. Run the application:
   ```bash
   ./karoloke-v*-macos
   ```
4. If macOS blocks it (unsigned app):
   - Right-click the file → **Open**
   - Click **"Open"** in the dialog
   - Or run: `xattr -d com.apple.quarantine karoloke-v*-macos`

#### **Linux**

1. Open Terminal and navigate to the download folder
2. Make the file executable:
   ```bash
   chmod +x karoloke-v*-linux
   ```
3. Run the application:
   ```bash
   ./karoloke-v*-linux
   ```

---

### Step 4: Configure Your Video Folder

When Karol-Oke opens in your browser:

1. Click the **⚙️ Settings** button (top-right corner)
2. Under **"Pasta de Vídeos"** (Video Folder), enter the full path to your karaoke folder:
   - **Windows**: `C:\Users\YourName\Videos\Karaoke`
   - **macOS**: `/Users/YourName/Videos/Karaoke`
   - **Linux**: `/home/yourname/Videos/karaoke`
3. Click **"Salvar Pasta"** (Save Folder)
4. Return to the main screen

---

### Step 5: Start Singing! 🎶

1. **Enter a song number** in the input field
2. Click **"Bota pra cantar!"** (Let's Sing!) or press Enter
3. The video will play with synchronized lyrics
4. Use the **Stop** button to end playback
5. Select your next song and repeat!

---

## 📱 Access from Other Devices

Share the karaoke with everyone at your party:

1. On the main screen, click the **QR Code** icon
2. Scan the QR code with your phone or tablet
3. Open the playlist page to browse and queue songs
4. Multiple people can add songs to the queue simultaneously!

**The playlist shows:**
- All available songs with title and artist
- Filter by song number, title, or artist
- Click **"+ Fila"** to add songs to the queue
- Real-time queue status

---

## 🎨 Customize Background Images

Make your karaoke more personal:

1. Click the **⚙️ Settings** button
2. Under **"Pasta de Backgrounds"**, select a theme folder
3. The app includes two default themes:
   - **default**: General karaoke backgrounds
   - **suelioke**: Custom themed backgrounds

**Add your own backgrounds:**
1. Navigate to the Karol-Oke installation folder
2. Go to `backgrounds/` directory
3. Create a new subfolder (e.g., `backgrounds/party/`)
4. Add your images (`.jpg`, `.png`, `.gif`, `.bmp`)
5. Select your folder from the Settings page

---

## 💡 Tips & Tricks

### Song Organization
- **Use numeric filenames**: `0001.mp4`, `0002.mp4`, etc.
- **Create a playlist database**: Use the included PDF playlist generator (see developer docs)
- **Backup your collection**: Keep copies of your video files

### Performance
- **Close other apps**: Free up system resources for smooth playback
- **Use local files**: Network/USB drives may cause lag
- **Check video quality**: Higher quality = smoother playback (but larger files)

### Party Mode
- **Queue multiple songs**: Let guests add their favorites to the queue
- **Use multiple devices**: Browse and queue from phones while playing on TV
- **Display QR code**: Print and place near the karaoke area for easy access

---

## 🆘 Troubleshooting

### "No video found" error
- ✅ Check that video files are in the configured folder
- ✅ Verify file extensions (`.mp4`, `.webm`, `.ogg`)
- ✅ Make sure filenames match the song numbers

### Videos won't play
- ✅ Check browser compatibility (Chrome, Firefox, Edge recommended)
- ✅ Verify video codec support (H.264 MP4 works best)
- ✅ Try a different video file to isolate the issue

### Slow performance
- ✅ Close browser tabs and other applications
- ✅ Use lower resolution videos if available
- ✅ Ensure videos are on a fast local drive (not USB 2.0 or network)

### Can't access from other devices
- ✅ Ensure all devices are on the same WiFi network
- ✅ Check firewall settings (allow port 5000)
- ✅ Try scanning the QR code again

---

## 📖 For Developers & Advanced Users

If you want to contribute to the project, customize features, or install from source:

- **Developer Documentation**: See [Getting Started](getting_started.md) guide
- **Source Code**: [GitHub Repository](https://github.com/acsenrafilho/karoloke)
- **API Reference**: Full documentation of the `karoloke` Python library
- **Contributing**: Read our [Contribution Guidelines](https://github.com/acsenrafilho/karoloke/blob/main/CONTRIBUTING.md)

### Installation from Source

```bash
# Install via pip
pip install karoloke

# Run the application
karoloke
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/acsenrafilho/karoloke.git
cd karoloke

# Install with poetry
poetry install

# Run tests
poetry run task test

# Start development server
poetry run karoloke
```

---

## 🤝 Support & Community

- **Report Issues**: [GitHub Issues](https://github.com/acsenrafilho/karoloke/issues)
- **Feature Requests**: Open a new issue with your suggestion
- **Sponsor the Project**: [GitHub Sponsors](https://github.com/sponsors/acsenrafilho)
- **Code of Conduct**: [Read here](https://github.com/acsenrafilho/karoloke/blob/main/CODE_OF_CONDUCT.md)

---

## 📜 License

Karol-Oke is open-source software licensed under the **MIT License**.

> **Note on Video Content**: Karol-Oke is only a player application. Users are responsible for ensuring they have the legal right to use any video content they play through the application. Always respect copyright laws and obtain proper licenses for commercial use.

---

**Enjoy your karaoke party! 🎉🎤**