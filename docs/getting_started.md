# Getting Started with Karoloke

Karoloke is a simple music player for your karaoke parties. Choose between using the pre-built executable or running from source.

## **Quick Start with Executable (Recommended)**

### Download
1. Go to the [Releases page](https://github.com/acsenrafilho/karoloke/releases)
2. Download the latest version for your operating system:
   - **Linux:** `karoloke-v*-linux`
   - **macOS:** `karoloke-v*-macos`  
   - **Windows:** `karoloke-v*-windows.exe`

### Run

**Linux/macOS:**
```bash
chmod +x karoloke-v*-linux  # or karoloke-v*-macos
./karoloke-v*-linux         # or ./karoloke-v*-macos
```

**Windows:**
- Double-click the `.exe` file
- If Windows Defender shows a warning, click "More info" → "Run anyway"

The application will automatically open in your default web browser at `http://localhost:5000`.

## **Running from Source**

### Prerequisites
- Python 3.9 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Installation
```bash
# Clone the repository
git clone https://github.com/acsenrafilho/karoloke.git
cd karoloke

# Install dependencies
poetry install

# Run the application
poetry run karoloke
```

Or install via pip:
```bash
pip install karoloke
karoloke
```

## **Using the Application**

### Initial Setup
1. When the application starts, it will open in your browser
2. Click the **settings button** (⚙️) in the top-right corner
3. Enter the **full path** to your video files directory
4. Click "Save"

### Playing Music
1. Enter the **song number** in the input field
2. Press **Enter** or click "Bota pra cantar!"
3. When the video loads, you'll see "Preparado? Aperte Enter!"
4. Press **Enter** to start playback
5. After the song ends, enjoy the fun score animation!

### Accessing the Playlist
- Scan the **QR code** (bottom-left) with your phone
- Or click the playlist link to see all available songs

## **Supported Video Formats**
- `.mp4` (recommended)
- `.webm`
- `.ogg`

## **Score Panel and Internet Requirement**
- After a video finishes, a fun score panel is displayed
- **Note:** The score panel requires an internet connection to fetch GIF animations
- The rest of the application works completely offline

## **Music/Video Files**
- The project does **not** include any music or video files
- You must provide your own compatible video files
- Organize them in a folder with numbered filenames (e.g., `001.mp4`, `002.mp4`)

## **Browser Compatibility**
- Tested on Chrome, Firefox, Microsoft Edge, and Safari
- Responsive design works on all screen sizes
- Video player adapts to your display automatically

For more details, see the [README.md](../README.md) and [CONTRIBUTING.md](../CONTRIBUTING.md).
