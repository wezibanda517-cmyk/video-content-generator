"""Video composition and clip combination module"""

import os
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips, CompositeVideoClip,
    AudioFileClip, concatenate_audioclips, CompositeAudioClip
)
from moviepy.video.fx.all import resize
import logging
from typing import List, Dict, Optional, Tuple
from config import Config

logger = logging.getLogger(__name__)


class VideoComposer:
    """Compose and combine video clips"""
    
    def __init__(self, output_folder: str = None):
        """Initialize video composer"""
        self.output_folder = output_folder or Config.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
    
    def combine_clips(self,
                     clip_paths: List[str],
                     transition: str = 'fade',
                     transition_duration: float = 1.0,
                     output_path: str = None) -> Dict[str, any]:
        """Combine multiple video clips into one
        
        Args:
            clip_paths: List of paths to video files
            transition: Type of transition between clips
            transition_duration: Duration of transition in seconds
            output_path: Path to save the combined video
            
        Returns:
            Dictionary with composition result
        """
        try:
            clips = []
            
            # Load all clips
            for clip_path in clip_paths:
                if not os.path.exists(clip_path):
                    logger.warning(f"Clip not found: {clip_path}")
                    continue
                
                clip = VideoFileClip(clip_path)
                clips.append(clip)
            
            if not clips:
                return {'status': 'error', 'message': 'No valid clips found'}
            
            # Concatenate clips
            if transition == 'fade':
                final_clip = concatenate_videoclips(clips, method="chain")
            else:
                final_clip = concatenate_videoclips(clips, method="chain")
            
            # Generate output path
            if not output_path:
                output_path = os.path.join(self.output_folder, 'combined_video.mp4')
            
            # Write the video file
            final_clip.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            logger.info(f"Combined {len(clips)} clips into {output_path}")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'duration': final_clip.duration,
                'fps': final_clip.fps,
                'clips_combined': len(clips)
            }
            
        except Exception as e:
            logger.error(f"Error combining clips: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def resize_video(self,
                     input_path: str,
                     target_resolution: Tuple[int, int] = None,
                     output_path: str = None) -> Dict[str, any]:
        """Resize video to target resolution
        
        Args:
            input_path: Path to input video
            target_resolution: Target resolution as (width, height)
            output_path: Path to save resized video
            
        Returns:
            Dictionary with resize result
        """
        try:
            if not target_resolution:
                # Parse from config
                res_str = Config.VIDEO_OUTPUT_RESOLUTION
                w, h = map(int, res_str.split('x'))
                target_resolution = (w, h)
            
            clip = VideoFileClip(input_path)
            resized_clip = resize(clip, newsize=(target_resolution[0], target_resolution[1]))
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'resized_video.mp4')
            
            resized_clip.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                verbose=False,
                logger=None
            )
            
            logger.info(f"Resized video to {target_resolution}")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'resolution': target_resolution
            }
            
        except Exception as e:
            logger.error(f"Error resizing video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def crop_video(self,
                   input_path: str,
                   start_time: float,
                   end_time: float,
                   output_path: str = None) -> Dict[str, any]:
        """Crop a video to specific time range
        
        Args:
            input_path: Path to input video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Path to save cropped video
            
        Returns:
            Dictionary with crop result
        """
        try:
            clip = VideoFileClip(input_path)
            cropped_clip = clip.subclipped(start_time, end_time)
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'cropped_video.mp4')
            
            cropped_clip.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                verbose=False,
                logger=None
            )
            
            logger.info(f"Cropped video from {start_time}s to {end_time}s")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'duration': cropped_clip.duration
            }
            
        except Exception as e:
            logger.error(f"Error cropping video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def adjust_speed(self,
                     input_path: str,
                     speed_factor: float,
                     output_path: str = None) -> Dict[str, any]:
        """Adjust video playback speed
        
        Args:
            input_path: Path to input video
            speed_factor: Speed multiplier (e.g., 1.5 for 1.5x speed)
            output_path: Path to save speed-adjusted video
            
        Returns:
            Dictionary with result
        """
        try:
            clip = VideoFileClip(input_path)
            adjusted_clip = clip.speedx(speed_factor)
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'speed_adjusted_video.mp4')
            
            adjusted_clip.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                verbose=False,
                logger=None
            )
            
            logger.info(f"Adjusted video speed by {speed_factor}x")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'speed_factor': speed_factor,
                'new_duration': adjusted_clip.duration
            }
            
        except Exception as e:
            logger.error(f"Error adjusting speed: {str(e)}")
            return {'status': 'error', 'message': str(e)}