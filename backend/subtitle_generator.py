"""Subtitle and caption generation module"""

import os
import logging
from typing import Dict, List, Optional
from config import Config

try:
    import speech_recognition as sr
    from pydub import AudioSegment
except ImportError:
    sr = None
    AudioSegment = None

logger = logging.getLogger(__name__)


class SubtitleGenerator:
    """Generate subtitles from video audio"""
    
    def __init__(self, output_folder: str = None):
        """Initialize subtitle generator"""
        self.output_folder = output_folder or Config.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
    
    def generate_subtitles(self,
                          video_path: str,
                          language: str = 'en',
                          output_format: str = 'srt') -> Dict[str, any]:
        """Generate subtitles from video audio
        
        Args:
            video_path: Path to video file
            language: Language for recognition
            output_format: Output format (srt, vtt)
            
        Returns:
            Dictionary with subtitle data
        """
        try:
            if sr is None:
                return {
                    'status': 'error',
                    'message': 'speech_recognition not installed'
                }
            
            # Extract audio from video
            from moviepy.editor import VideoFileClip
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                return {'status': 'error', 'message': 'Video has no audio'}
            
            # Export audio to temporary file
            temp_audio = os.path.join(self.output_folder, 'temp_audio.wav')
            audio.write_audiofile(temp_audio, verbose=False, logger=None)
            
            # Recognize speech
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_audio) as source:
                audio_data = recognizer.record(source)
            
            try:
                transcript = recognizer.recognize_google(audio_data, language=language)
                logger.info(f"Generated transcript: {len(transcript)} characters")
                
                # Create subtitle data
                subtitles = self._create_subtitles(transcript, language)
                
                # Save subtitles
                output_path = os.path.join(
                    self.output_folder,
                    f'subtitles.{output_format}'
                )
                self._save_subtitles(subtitles, output_path, output_format)
                
                # Clean up temp file
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
                
                return {
                    'status': 'success',
                    'output_path': output_path,
                    'transcript': transcript,
                    'subtitles': subtitles,
                    'language': language,
                    'format': output_format
                }
                
            except sr.UnknownValueError:
                return {'status': 'error', 'message': 'Could not understand audio'}
            
        except Exception as e:
            logger.error(f"Error generating subtitles: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def add_subtitles_to_video(self,
                              video_path: str,
                              subtitles: List[Dict],
                              font_size: int = None,
                              font_color: str = None,
                              output_path: str = None) -> Dict[str, any]:
        """Add subtitle text to video
        
        Args:
            video_path: Path to video file
            subtitles: List of subtitle dictionaries with start, end, text
            font_size: Font size for subtitles
            font_color: Color of subtitle text
            output_path: Path to save the video
            
        Returns:
            Dictionary with result
        """
        try:
            from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
            
            font_size = font_size or Config.SUBTITLE_FONT_SIZE
            font_color = font_color or Config.SUBTITLE_COLOR
            
            video = VideoFileClip(video_path)
            clips = [video]
            
            # Add text clips for each subtitle
            for subtitle in subtitles:
                txt_clip = TextClip(
                    subtitle.get('text', ''),
                    fontsize=font_size,
                    color=font_color,
                    bg=Config.SUBTITLE_BACKGROUND,
                    method='caption',
                    size=(video.w - 100, None),
                    font='Arial'
                )
                
                txt_clip = txt_clip.set_position('bottom').set_duration(
                    subtitle.get('end', 0) - subtitle.get('start', 0)
                ).set_start(subtitle.get('start', 0))
                
                clips.append(txt_clip)
            
            final_video = CompositeVideoClip(clips, size=video.size)
            
            if not output_path:
                output_path = os.path.join(self.output_folder, 'with_subtitles.mp4')
            
            final_video.write_videofile(
                output_path,
                codec=Config.VIDEO_CODEC,
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            logger.info(f"Added {len(subtitles)} subtitles to video")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'subtitles_count': len(subtitles)
            }
            
        except Exception as e:
            logger.error(f"Error adding subtitles: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def _create_subtitles(transcript: str, language: str) -> List[Dict]:
        """Create subtitle objects from transcript
        
        Args:
            transcript: Full text transcript
            language: Language code
            
        Returns:
            List of subtitle dictionaries
        """
        subtitles = []
        words = transcript.split()
        words_per_subtitle = 10  # Approx 2-3 seconds per subtitle
        
        for i in range(0, len(words), words_per_subtitle):
            subtitle_text = ' '.join(words[i:i+words_per_subtitle])
            subtitle = {
                'start': (i * 0.5),  # Approximate timing
                'end': ((i + words_per_subtitle) * 0.5),
                'text': subtitle_text
            }
            subtitles.append(subtitle)
        
        return subtitles
    
    @staticmethod
    def _save_subtitles(subtitles: List[Dict], output_path: str, format: str) -> None:
        """Save subtitles to file
        
        Args:
            subtitles: List of subtitle dictionaries
            output_path: Path to save the file
            format: Output format (srt, vtt)
        """
        if format == 'srt':
            content = SubtitleGenerator._subtitles_to_srt(subtitles)
        elif format == 'vtt':
            content = SubtitleGenerator._subtitles_to_vtt(subtitles)
        else:
            raise ValueError(f'Unsupported format: {format}')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def _subtitles_to_srt(subtitles: List[Dict]) -> str:
        """Convert subtitles to SRT format"""
        lines = []
        for i, subtitle in enumerate(subtitles, 1):
            lines.append(str(i))
            start = SubtitleGenerator._format_time_srt(subtitle['start'])
            end = SubtitleGenerator._format_time_srt(subtitle['end'])
            lines.append(f"{start} --> {end}")
            lines.append(subtitle['text'])
            lines.append('')
        return '\n'.join(lines)
    
    @staticmethod
    def _subtitles_to_vtt(subtitles: List[Dict]) -> str:
        """Convert subtitles to VTT format"""
        lines = ['WEBVTT', '']
        for subtitle in subtitles:
            start = SubtitleGenerator._format_time_vtt(subtitle['start'])
            end = SubtitleGenerator._format_time_vtt(subtitle['end'])
            lines.append(f"{start} --> {end}")
            lines.append(subtitle['text'])
            lines.append('')
        return '\n'.join(lines)
    
    @staticmethod
    def _format_time_srt(seconds: float) -> str:
        """Format time for SRT format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    @staticmethod
    def _format_time_vtt(seconds: float) -> str:
        """Format time for VTT format (HH:MM:SS.mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"