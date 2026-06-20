"""Flask application for video content generator"""

import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from config import get_config
from script_generator import ScriptGenerator
from video_composer import VideoComposer
from text_to_video import TextToVideo
from effects_handler import EffectsHandler
from subtitle_generator import SubtitleGenerator
from facebook_uploader import FacebookUploader
import traceback

load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
app.config.from_object(get_config())

# Enable CORS
CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))

# Set up logging
logging.basicConfig(
    level=app.config.get('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(app.config.get('LOG_FILE', 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize modules
script_gen = ScriptGenerator()
video_composer = VideoComposer()
text_to_video = TextToVideo()
effects_handler = EffectsHandler()
subtitle_gen = SubtitleGenerator()
facebook_uploader = FacebookUploader()


# Routes

@app.route('/', methods=['GET'])
def index():
    """Serve the web interface"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Video Content Generator API is running'
    })


# Script Generation Endpoints

@app.route('/api/generate-script', methods=['POST'])
def generate_script():
    """Generate a video script"""
    try:
        data = request.json
        topic = data.get('topic')
        duration = data.get('duration', 60)
        style = data.get('style', 'engaging')
        target_audience = data.get('target_audience', 'general')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        result = script_gen.generate_script(
            topic=topic,
            duration=duration,
            style=style,
            target_audience=target_audience
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in generate_script: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-captions', methods=['POST'])
def generate_captions():
    """Generate captions from script"""
    try:
        data = request.json
        script = data.get('script')
        
        if not script:
            return jsonify({'error': 'Script is required'}), 400
        
        result = script_gen.generate_captions(script)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in generate_captions: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Video Composition Endpoints

@app.route('/api/compose-video', methods=['POST'])
def compose_video():
    """Combine video clips"""
    try:
        data = request.json
        clip_paths = data.get('clip_paths', [])
        transition = data.get('transition', 'fade')
        
        if not clip_paths:
            return jsonify({'error': 'At least one clip is required'}), 400
        
        result = video_composer.combine_clips(
            clip_paths=clip_paths,
            transition=transition
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in compose_video: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Text-to-Video Endpoints

@app.route('/api/text-to-video', methods=['POST'])
def create_text_video():
    """Generate video from text"""
    try:
        data = request.json
        text = data.get('text')
        duration = data.get('duration', 5.0)
        style = data.get('style', 'default')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = text_to_video.create_text_video(
            text=text,
            duration=duration,
            style=style
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in create_text_video: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Effects Endpoints

@app.route('/api/add-effects', methods=['POST'])
def add_effects():
    """Add effects to video"""
    try:
        data = request.json
        video_path = data.get('video_path')
        effects = data.get('effects', [])
        
        if not video_path:
            return jsonify({'error': 'Video path is required'}), 400
        
        result = effects_handler.apply_effects(
            video_path=video_path,
            effects=effects
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in add_effects: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-music', methods=['POST'])
def add_music():
    """Add background music to video"""
    try:
        data = request.json
        video_path = data.get('video_path')
        music_path = data.get('music_path')
        music_volume = data.get('music_volume', 0.3)
        
        if not video_path or not music_path:
            return jsonify({'error': 'Video path and music path are required'}), 400
        
        result = effects_handler.add_background_music(
            video_path=video_path,
            music_path=music_path,
            music_volume=music_volume
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in add_music: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Subtitle Endpoints

@app.route('/api/generate-subtitles', methods=['POST'])
def generate_subtitles():
    """Generate subtitles for video"""
    try:
        data = request.json
        video_path = data.get('video_path')
        language = data.get('language', 'en')
        
        if not video_path:
            return jsonify({'error': 'Video path is required'}), 400
        
        result = subtitle_gen.generate_subtitles(
            video_path=video_path,
            language=language
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in generate_subtitles: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-subtitles', methods=['POST'])
def add_subtitles():
    """Add subtitles to video"""
    try:
        data = request.json
        video_path = data.get('video_path')
        subtitles = data.get('subtitles', [])
        
        if not video_path or not subtitles:
            return jsonify({'error': 'Video path and subtitles are required'}), 400
        
        result = subtitle_gen.add_subtitles_to_video(
            video_path=video_path,
            subtitles=subtitles
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in add_subtitles: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Facebook Integration Endpoints

@app.route('/api/post-facebook', methods=['POST'])
def post_facebook():
    """Upload video to Facebook"""
    try:
        data = request.json
        video_path = data.get('video_path')
        title = data.get('title')
        description = data.get('description', '')
        
        if not video_path or not title:
            return jsonify({'error': 'Video path and title are required'}), 400
        
        result = facebook_uploader.upload_video(
            video_path=video_path,
            title=title,
            description=description
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in post_facebook: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/publish-facebook/<video_id>', methods=['POST'])
def publish_facebook(video_id):
    """Publish video to Facebook"""
    try:
        data = request.json
        caption = data.get('caption', '')
        
        result = facebook_uploader.publish_video(
            video_id=video_id,
            caption=caption
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in publish_facebook: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-facebook', methods=['GET'])
def validate_facebook():
    """Validate Facebook credentials"""
    try:
        result = facebook_uploader.validate_credentials()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in validate_facebook: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Video Content Generator")
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )