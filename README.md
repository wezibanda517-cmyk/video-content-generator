# Video Content Generator for Facebook

An intelligent, AI-powered video content generation platform that automatically creates, edits, and uploads professional video content to Facebook.

## 🎬 Features

✅ **Auto-Generate Video Scripts/Captions** - AI-powered script generation using OpenAI  
✅ **Combine Existing Video Clips** - Easy video composition and compilation  
✅ **Text-to-Video Generation** - Convert text prompts into engaging videos  
✅ **Effects, Transitions & Music** - Professional video editing capabilities  
✅ **Auto-Generated Subtitles** - Automatic caption generation with speech recognition  
✅ **Facebook Integration** - Direct posting to Facebook  
✅ **Web Dashboard** - User-friendly interface for content creation  
✅ **REST API** - Complete API for programmatic access  

## 📁 Project Structure

```
video-content-generator/
├── backend/
│   ├── script_generator.py      # AI script generation using OpenAI
│   ├── video_composer.py        # Combine and arrange video clips
│   ├── text_to_video.py         # Text-to-video conversion engine
│   ├── effects_handler.py       # Add effects, transitions, music
│   ├── subtitle_generator.py    # Auto-generate captions from audio
│   ├── facebook_uploader.py     # Facebook Graph API integration
│   ├── app.py                   # Main Flask application
│   └── config.py                # Configuration settings
├── frontend/
│   ├── index.html               # Web interface
│   ├── style.css                # Styling
│   └── script.js                # Frontend logic
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Facebook Developer Account
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wezibanda517-cmyk/video-content-generator.git
   cd video-content-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key from https://platform.openai.com
   - `FACEBOOK_ACCESS_TOKEN`: Your Facebook Graph API token
   - `FACEBOOK_PAGE_ID`: Your Facebook page ID

5. **Run the application**
   ```bash
   python backend/app.py
   ```
   The application will be available at `http://localhost:5000`

## 💻 Usage

### Web Dashboard

Navigate to `http://localhost:5000` and use the dashboard to:

1. **Generate Scripts** - Enter a topic, AI generates video scripts
2. **Upload Clips** - Upload existing video files
3. **Compose Video** - Arrange clips, add transitions and effects
4. **Add Effects & Music** - Apply professional filters and background audio
5. **Generate Subtitles** - Auto-generate captions from video audio
6. **Preview & Post** - Preview the final video and post directly to Facebook

### API Endpoints

#### 📝 Script Generation
```
POST /api/generate-script
Content-Type: application/json

{
  "topic": "How to make coffee",
  "duration": 60,
  "style": "engaging",
  "target_audience": "coffee enthusiasts"
}
```

#### 🎞️ Video Composition
```
POST /api/compose-video
Content-Type: application/json

{
  "clip_paths": ["/path/to/clip1.mp4", "/path/to/clip2.mp4"],
  "transition": "fade"
}
```

#### 📹 Text-to-Video
```
POST /api/text-to-video
Content-Type: application/json

{
  "text": "Welcome to my channel!",
  "duration": 5,
  "style": "default"
}
```

#### ✨ Add Effects
```
POST /api/add-effects
Content-Type: application/json

{
  "video_path": "/path/to/video.mp4",
  "effects": ["fade", "blur", "brightness"],
  "music": "background_music.mp3"
}
```

#### 📺 Generate Subtitles
```
POST /api/generate-subtitles
Content-Type: application/json

{
  "video_path": "/path/to/video.mp4",
  "language": "en"
}
```

#### 📤 Post to Facebook
```
POST /api/post-facebook
Content-Type: application/json

{
  "video_path": "/path/to/video.mp4",
  "title": "My Awesome Video",
  "description": "Check out this amazing content!"
}
```

## ⚙️ Configuration

Edit `backend/config.py` to customize:

- **Video Settings**: Resolution, framerate, codec, quality
- **Effects**: Available effects and transitions
- **Audio**: Music and sound effects paths
- **Facebook API**: Settings and rate limits
- **Subtitles**: Language, font size, color
- **Server**: Host, port, debug mode

## 🛠️ Technologies

- **Backend**: Python 3.8+, Flask 3.0
- **Video Processing**: MoviePy, OpenCV, Pillow
- **AI/ML**: OpenAI GPT-4 API, SpeechRecognition
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **APIs**: Facebook Graph API
- **Audio**: librosa, pydub
- **Database**: SQLite (optional)

## 📦 Dependencies

Key packages included:

- `moviepy` - Video processing and editing
- `opencv-python` - Computer vision operations
- `openai` - AI script and content generation
- `flask` - Web framework
- `pillow` - Image processing
- `librosa` - Audio analysis
- `pydub` - Audio manipulation
- `speechrecognition` - Audio-to-text conversion
- `requests` - HTTP client
- `python-dotenv` - Environment variables

See `requirements.txt` for complete list.

## 🔑 API Keys Setup

### OpenAI API Key
1. Sign up at https://platform.openai.com/signup
2. Go to API keys section
3. Create new API key
4. Copy and paste into `.env` as `OPENAI_API_KEY`

### Facebook API Credentials
1. Go to https://developers.facebook.com
2. Create a new app (select "Business" type)
3. Add Facebook Login product
4. Go to Settings > Basic to get App ID
5. Create Page Access Token
6. Copy credentials into `.env`

## 🐛 Troubleshooting

### FFmpeg Not Installed
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Module Not Found Errors
Ensure virtual environment is activated:
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### Video Processing Errors
- Ensure input videos are in supported formats: MP4, MOV, AVI, WebM
- Check file permissions
- Verify sufficient disk space for output videos

### API Rate Limiting
- Implement exponential backoff for retries
- Respect API rate limits (OpenAI: 3 requests/min free tier)
- Consider upgrading API plan for production use

## 📚 Usage Examples

### Generate Script and Create Video

```python
from backend.script_generator import ScriptGenerator
from backend.text_to_video import TextToVideo

# Generate script
script_gen = ScriptGenerator()
script_result = script_gen.generate_script(
    topic="Healthy breakfast recipes",
    duration=60,
    style="engaging"
)

# Create video from generated script
text_to_video = TextToVideo()
video_result = text_to_video.create_text_video(
    text=script_result['script'],
    duration=60,
    style="fade"
)
```

### Combine Video Clips

```python
from backend.video_composer import VideoComposer

composer = VideoComposer()
result = composer.combine_clips(
    clip_paths=["clip1.mp4", "clip2.mp4", "clip3.mp4"],
    transition="fade"
)
```

### Post to Facebook

```python
from backend.facebook_uploader import FacebookUploader

uploader = FacebookUploader()
result = uploader.upload_video(
    video_path="final_video.mp4",
    title="Amazing Content",
    description="Check this out!"
)
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, feature requests, or questions:
- Open a GitHub issue
- Check existing issues and discussions
- Review troubleshooting section above

## 🗺️ Roadmap

- [x] Core video composition engine
- [x] AI script generation
- [x] Text-to-video conversion
- [x] Effects and transitions
- [x] Subtitle generation
- [x] Facebook integration
- [ ] Web UI dashboard
- [ ] Stock footage integration
- [ ] Advanced AI customization
- [ ] Multi-language support
- [ ] Video analytics
- [ ] Scheduled posting
- [ ] Video templates library
- [ ] Instagram/TikTok export
- [ ] Mobile app
- [ ] Team collaboration

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star! ⭐

---

**Made with ❤️ for content creators**

For more information, visit: https://github.com/wezibanda517-cmyk/video-content-generator
