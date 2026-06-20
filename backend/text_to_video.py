"""Text-to-video generation module"""

import os
from moviepy.editor import (
    TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
import logging
from typing import Dict, Tuple, Optional
from config import Config

logger = logging.getLogger(__name__)


class TextToVideo:
    """Convert text to video"""
    
    def __init__(self, output_folder: str = None):
        """Initialize text-to-video converter"""
        self.output_folder = output_folder or Config.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
    
    def create_text_video(self,
                         text: str,
                         duration: float = 5.0,
                         style: str = 'default',
                         background_color: Tuple[int, int, int] = (0, 0, 0),
                         text_color: Tuple[int, int, int] = (255, 255, 255),
                         font_size: int = 60,
                         output_path: str = None) -> Dict[str, any]:
        """Create a video from text
        
        Args:
            text: Text to display
            duration: Duration in seconds
            style: Style of the video (default, fade, slide, typewriter)
            background_color: RGB background color
            text_color: RGB text color
            font_size: Font size
            output_path: Path to save the video
            
        Returns:
            Dictionary with result
        """
        try:
            # Parse resolution
            res_str = Config.VIDEO_OUTPUT_RESOLUTION
            width, height = map(int, res_str.split('x'))
            fps = Config.VIDEO_FPS
            
            if style == 'default':
                video = self._create_default_text_video(
                    text, duration, width, height, fps,
                    background_color, text_color, font_size
                )
            elif style == 'fade':
                video = self._create_fade_text_video(
                    text, duration, width, height, fps,
                    background_color, text_color, font_size
                )
            elif style == 'slide':
                video = self._create_slide_text_video(
                    text, duration, width, height, fps,
                    background_color, text_color, font_size
                )
            elif style == 'typewriter':
                video = self._create_typewriter_video(
                    text, duration, width, height, fps,
                    background_color, text_color, font_size
                )
            else:
                return {'status': 'error', 'message': f'Unknown style: {style}'}
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'text_video.mp4')
            
            video.write_videofile(
                output_path,
                fps=fps,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            logger.info(f"Created text video: {style} style")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'duration': duration,
                'style': style,
                'resolution': f"{width}x{height}"
            }
            
        except Exception as e:
            logger.error(f"Error creating text video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _create_default_text_video(self, text, duration, width, height, fps,
                                   bg_color, text_color, font_size):
        """Create a simple text video with centered text"""
        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=font_size,
            color='white',
            bg=None,
            method='caption',
            size=(width - 100, None),
            font='Arial'
        )
        
        # Center text
        txt_clip = txt_clip.set_position('center').set_duration(duration)
        
        # Create background
        bg_clip = ColorClip(size=(width, height), color=bg_color).set_duration(duration)
        
        # Composite
        return CompositeVideoClip([bg_clip, txt_clip], size=(width, height))
    
    def _create_fade_text_video(self, text, duration, width, height, fps,
                               bg_color, text_color, font_size):
        """Create text video with fade in/out effect"""
        # Similar to default but with fade effects
        txt_clip = TextClip(
            text,
            fontsize=font_size,
            color='white',
            bg=None,
            method='caption',
            size=(width - 100, None),
            font='Arial'
        )
        
        # Add fade effect
        fade_duration = min(1.0, duration / 3)
        txt_clip = txt_clip.set_position('center').set_duration(duration)
        txt_clip = txt_clip.fadein(fade_duration).fadeout(fade_duration)
        
        bg_clip = ColorClip(size=(width, height), color=bg_color).set_duration(duration)
        
        return CompositeVideoClip([bg_clip, txt_clip], size=(width, height))
    
    def _create_slide_text_video(self, text, duration, width, height, fps,
                                bg_color, text_color, font_size):
        """Create text video with sliding effect"""
        txt_clip = TextClip(
            text,
            fontsize=font_size,
            color='white',
            bg=None,
            method='caption',
            size=(width - 100, None),
            font='Arial'
        ).set_duration(duration)
        
        # Slide from left to center
        def slide_position(t):
            progress = min(t / (duration * 0.5), 1)
            x = -width/2 + (width/2 * progress)
            return (x, 'center')
        
        txt_clip = txt_clip.set_position(slide_position)
        
        bg_clip = ColorClip(size=(width, height), color=bg_color).set_duration(duration)
        
        return CompositeVideoClip([bg_clip, txt_clip], size=(width, height))
    
    def _create_typewriter_video(self, text, duration, width, height, fps,
                                bg_color, text_color, font_size):
        """Create typewriter-style text video"""
        # Create frames for typewriter effect
        clips = []
        chars_per_frame = max(1, len(text) // int(fps * duration))
        
        for i in range(0, len(text), chars_per_frame):
            frame_text = text[:i]
            txt_clip = TextClip(
                frame_text,
                fontsize=font_size,
                color='white',
                bg=None,
                method='caption',
                size=(width - 100, None),
                font='Arial'
            ).set_position('center').set_duration(1/fps)
            
            bg_clip = ColorClip(size=(width, height), color=bg_color).set_duration(1/fps)
            frame = CompositeVideoClip([bg_clip, txt_clip], size=(width, height))
            clips.append(frame)
        
        return concatenate_videoclips(clips)