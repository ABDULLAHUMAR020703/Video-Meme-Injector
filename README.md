# Video Memer - Black Frame Detector

A Python application that automatically detects black frames in videos and replaces them with random meme images from a selected folder.

## Features

- **Black Frame Detection**: Automatically scans videos for black or near-black frames
- **Meme Insertion**: Replaces black segments with random images from your meme folder
- **Customizable Settings**: Adjust image duration and black threshold sensitivity
- **Simple GUI**: User-friendly interface with file browsers and progress tracking
- **Multiple Video Formats**: Supports MP4, AVI, MOV, MKV, WMV and more
- **Multiple Image Formats**: Supports JPG, PNG, BMP, GIF, TIFF

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows 10/11 (tested on Windows)

### Setup Instructions

1. **Clone or download this project** to your local machine

2. **Open Command Prompt or PowerShell** in the project directory

3. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Activate the virtual environment** (if not already active):
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Run the application**:
   ```bash
   python video_memer.py
   ```

### Using the GUI

1. **Select Video File**: Click "Browse" next to "Video File" and choose your input video
2. **Select Meme Folder**: Click "Browse" next to "Meme Folder" and choose a folder containing your meme images
3. **Adjust Settings**:
   - **Image Duration**: How long each meme image should appear (default: 2 seconds)
   - **Black Threshold**: Sensitivity for detecting black frames (0-255, default: 30)
4. **Choose Output**: The output path is auto-generated, but you can change it using "Browse"
5. **Process**: Click "Process Video" and wait for completion

### Settings Explained

- **Image Duration**: The length of time each meme image will be displayed during black segments
- **Black Threshold**: 
  - Lower values (1-20): Only very dark frames are considered "black"
  - Higher values (30-100): More frames will be considered "black"
  - Default 30 works well for most videos

## How It Works

1. **Frame Analysis**: The app scans each frame of your video to detect black segments
2. **Segment Detection**: Identifies continuous sequences of black frames
3. **Meme Selection**: Randomly selects images from your meme folder
4. **Video Reconstruction**: Creates a new video by:
   - Keeping original non-black segments
   - Replacing black segments with meme images
   - Maintaining original video quality and audio

## Supported Formats

### Input Videos
- MP4, AVI, MOV, MKV, WMV, and other common formats

### Meme Images
- JPG, JPEG, PNG, BMP, GIF, TIFF

### Output
- MP4 format (recommended for compatibility)

## Troubleshooting

### Common Issues

1. **"Could not open video file"**
   - Ensure the video file isn't corrupted
   - Try a different video format (MP4 recommended)

2. **"No image files found in meme folder"**
   - Check that your meme folder contains image files
   - Supported formats: JPG, PNG, BMP, GIF, TIFF

3. **Processing is slow**
   - Larger videos take longer to process
   - The app shows progress updates during processing

4. **Black frames not detected**
   - Increase the "Black Threshold" value
   - Try values between 40-80 for more sensitive detection

### Performance Tips

- Use MP4 format for best compatibility and performance
- Keep meme images reasonably sized (under 5MB each)
- Close other applications during processing for better performance

## Creating an Executable (.exe)

If you want to create a standalone executable:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**:
   ```bash
   pyinstaller --onefile --windowed video_memer.py
   ```

3. **Find the executable** in the `dist` folder

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- MoviePy
- Pillow (PIL)
- NumPy

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application! 