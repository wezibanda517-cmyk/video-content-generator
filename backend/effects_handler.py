"""Effects and transitions handler module"""

import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.all import speedx, resize
import logging
from typing import Dict, List, Optional
from config import Config
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)


class EffectsHandler:
    """Handle video effects and transitions"""
    
    def __init__(self, output_folder: str = None):
        """Initialize effects handler"""
        self.output_folder = output_folder or Config.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
    
    def apply_effects(self,
                     video_path: str,
                     effects: List[str],
                     output_path: str = None) -> Dict[str, any]:
        """Apply multiple effects to a video
        
        Args:
            video_path: Path to input video
            effects: List of effects to apply
            output_path: Path to save the video
            
        Returns:
            Dictionary with result
        """
        try:
            clip = VideoFileClip(video_path)
            
            # Apply effects in sequence
            for effect in effects:
                if effect == 'fade':
                    clip = self._apply_fade(clip)
                elif effect == 'blur':
                    clip = self._apply_blur(clip)
                elif effect == 'brightness':
                    clip = self._apply_brightness(clip)
                elif effect == 'contrast':
                    clip = self._apply_contrast(clip)
                elif effect == 'sepia':
                    clip = self._apply_sepia(clip)
                elif effect == 'grayscale':
                    clip = self._apply_grayscale(clip)
                elif effect == 'zoom':
                    clip = self._apply_zoom(clip)
                elif effect == 'pan':
                    clip = self._apply_pan(clip)
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'effects_video.mp4')
            
            clip.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            logger.info(f"Applied {len(effects)} effects to video")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'effects_applied': effects
            }
            
        except Exception as e:
            logger.error(f"Error applying effects: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def add_transition(self,
                      video1_path: str,
                      video2_path: str,
                      transition_type: str = 'fade',
                      duration: float = 1.0,
                      output_path: str = None) -> Dict[str, any]:
        """Add transition between two videos
        
        Args:
            video1_path: Path to first video
            video2_path: Path to second video
            transition_type: Type of transition (fade, wipe, dissolve, slide)
            duration: Duration of transition in seconds
            output_path: Path to save the video
            
        Returns:
            Dictionary with result
        """
        try:
            clip1 = VideoFileClip(video1_path)
            clip2 = VideoFileClip(video2_path)
            
            if transition_type == 'fade':
                # Fade transition
                clip1_trimmed = clip1.subclipped(0, clip1.duration - duration/2)
                clip2_trimmed = clip2.subclipped(duration/2, clip2.duration)
                
                result = [clip1_trimmed, clip2_trimmed]
                
            elif transition_type == 'dissolve':
                # Dissolve effect
                result = [clip1, clip2]
            
            else:
                result = [clip1, clip2]
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'transitioned_video.mp4')
            
            logger.info(f"Added {transition_type} transition")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'transition_type': transition_type
            }
            
        except Exception as e:
            logger.error(f"Error adding transition: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def add_background_music(self,
                            video_path: str,
                            music_path: str,
                            music_volume: float = 0.3,
                            output_path: str = None) -> Dict[str, any]:
        """Add background music to video
        
        Args:
            video_path: Path to video file
            music_path: Path to audio file
            music_volume: Volume of music (0-1)
            output_path: Path to save the video
            
        Returns:
            Dictionary with result
        """
        try:
            from moviepy.editor import AudioFileClip, CompositeAudioClip
            
            video_clip = VideoFileClip(video_path)
            music_clip = AudioFileClip(music_path)
            
            # Loop music if needed
            if music_clip.duration < video_clip.duration:
                music_loop_times = int(video_clip.duration / music_clip.duration) + 1
                music_clip = music_clip.loop(n=music_loop_times)
            
            # Trim music to video length
            music_clip = music_clip.subclipped(0, video_clip.duration)
            
            # Set volumes
            original_audio = video_clip.audio.volumex(0.7) if video_clip.audio else None
            music_audio = music_clip.volumex(music_volume)
            
            # Composite audio
            if original_audio:
                final_audio = CompositeAudioClip([original_audio, music_audio])
            else:
                final_audio = music_audio
            
            final_video = video_clip.set_audio(final_audio)
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'with_music.mp4')
            
            final_video.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            logger.info(f"Added background music to video")
            
            return {
                'status': 'success',
                'output_path': output_path
            }
            
        except Exception as e:
            logger.error(f"Error adding music: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    # Effect implementation methods
    
    @staticmethod
    def _apply_fade(clip):
        """Apply fade in/out effect"""
        fade_duration = min(1.0, clip.duration / 3)
        return clip.fadein(fade_duration).fadeout(fade_duration)
    
    @staticmethod
    def _apply_blur(clip):
        """Apply blur effect"""
        from scipy.ndimage import gaussian_filter
        
        def blurred_frame(get_frame, t):
            frame = get_frame(t)
            return gaussian_filter(frame, sigma=2)
        
        return clip.fl(blurred_frame)
    
    @staticmethod
    def _apply_brightness(clip, factor=1.2):
        """Increase brightness"""
        return clip.fx(lambda f: np.clip(f * factor, 0, 255))
    
    @staticmethod
    def _apply_contrast(clip, factor=1.2):
        """Increase contrast"""
        def adjust_contrast(frame):
            return np.clip((frame - 128) * factor + 128, 0, 255)
        
        return clip.fl(adjust_contrast)
    
    @staticmethod
    def _apply_sepia(clip):
        """Apply sepia tone effect"""
        def sepia_frame(frame):
            sepia_matrix = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            return np.dot(frame[..., :3], sepia_matrix.T)
        
        return clip.fl(sepia_frame)
    
    @staticmethod
    def _apply_grayscale(clip):
        """Convert to grayscale"""
        def gray_frame(frame):
            return np.dot(frame[..., :3], [0.299, 0.587, 0.114])
        
        return clip.fl(gray_frame)
    
    @staticmethod
    def _apply_zoom(clip):
        """Apply zoom effect"""
        return clip.resize(lambda t: 1 + 0.5 * (t / clip.duration))
    
    @staticmethod
    def _apply_pan(clip):
        """Apply pan effect"""
        def make_frame(t):
            progress = t / clip.duration
            return clip.get_frame(t)
        
        return clip.fl(make_frame)