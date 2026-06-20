"""Script generation module using OpenAI API"""

import openai
from typing import Dict, List, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)

class ScriptGenerator:
    """Generate video scripts using OpenAI"""
    
    def __init__(self, api_key: str = None):
        """Initialize the script generator"""
        self.api_key = api_key or Config.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.model = Config.OPENAI_MODEL
    
    def generate_script(self, 
                       topic: str,
                       duration: int = 60,
                       style: str = 'engaging',
                       target_audience: str = 'general',
                       language: str = 'en') -> Dict[str, any]:
        """Generate a video script based on topic
        
        Args:
            topic: The topic of the video
            duration: Desired video duration in seconds
            style: Script style (engaging, educational, promotional, entertaining)
            target_audience: Target audience for the content
            language: Language for the script
            
        Returns:
            Dictionary containing script and metadata
        """
        try:
            # Calculate approximate word count (average: 130 words per minute)
            minutes = duration / 60
            target_words = int(minutes * 130)
            
            prompt = f"""Create a {style} video script for Facebook about '{topic}'.
            
Requirements:
- Target audience: {target_audience}
- Approximate length: {target_words} words ({duration} seconds)
- Tone: {style}
- Language: {language}
- Include hooks to grab attention in the first 3 seconds
- Make it suitable for mobile viewing
- Include [VISUAL] and [AUDIO] cues
- Add timing markers in brackets

Format the response as:
HOOK: [Opening line]
SCRIPT: [Main content]
CALL TO ACTION: [Final message]
VISUAL NOTES: [Visual directions]
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert video script writer for social media content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            script_content = response['choices'][0]['message']['content']
            
            logger.info(f"Generated script for topic: {topic}")
            
            return {
                'status': 'success',
                'script': script_content,
                'topic': topic,
                'duration': duration,
                'style': style,
                'target_audience': target_audience,
                'language': language,
                'word_count': len(script_content.split()),
                'tokens_used': response['usage']['total_tokens']
            }
            
        except openai.error.AuthenticationError:
            logger.error("OpenAI authentication failed")
            return {'status': 'error', 'message': 'Authentication failed'}
        except openai.error.RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            return {'status': 'error', 'message': 'Rate limit exceeded'}
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def generate_multiple_scripts(self,
                                 topic: str,
                                 num_scripts: int = 3,
                                 **kwargs) -> Dict[str, any]:
        """Generate multiple script variations
        
        Args:
            topic: The topic of the video
            num_scripts: Number of variations to generate
            **kwargs: Additional arguments to pass to generate_script
            
        Returns:
            Dictionary containing multiple scripts
        """
        scripts = []
        
        for i in range(num_scripts):
            script = self.generate_script(topic, **kwargs)
            if script['status'] == 'success':
                scripts.append(script)
        
        return {
            'status': 'success' if scripts else 'error',
            'scripts': scripts,
            'topic': topic,
            'count': len(scripts)
        }
    
    def enhance_script(self, script: str, enhancement: str = 'seo') -> Dict[str, any]:
        """Enhance an existing script
        
        Args:
            script: Original script text
            enhancement: Type of enhancement (seo, engagement, accessibility)
            
        Returns:
            Enhanced script
        """
        try:
            if enhancement == 'seo':
                prompt = f"""Enhance this video script for SEO without changing its meaning:
                
{script}

Add relevant keywords naturally and improve searchability."""
            
            elif enhancement == 'engagement':
                prompt = f"""Make this script more engaging and attention-grabbing:
                
{script}

Add more emotional appeal, questions, and interactive elements."""
            
            elif enhancement == 'accessibility':
                prompt = f"""Make this script more accessible for all audiences:
                
{script}

Simplify language, add descriptions, ensure clarity."""
            else:
                return {'status': 'error', 'message': 'Unknown enhancement type'}
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert script editor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            enhanced = response['choices'][0]['message']['content']
            
            logger.info(f"Enhanced script with {enhancement}")
            
            return {
                'status': 'success',
                'original': script,
                'enhanced': enhanced,
                'enhancement_type': enhancement
            }
            
        except Exception as e:
            logger.error(f"Error enhancing script: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def generate_captions(self, script: str, max_length: int = 280) -> Dict[str, any]:
        """Generate social media captions from script
        
        Args:
            script: Video script
            max_length: Maximum caption length
            
        Returns:
            Generated captions
        """
        try:
            prompt = f"""Create 3 different social media captions for this video script.
Each caption should be max {max_length} characters and include relevant hashtags.

Script:
{script}

Format as:
Caption 1: [text]
Caption 2: [text]
Caption 3: [text]"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            captions_text = response['choices'][0]['message']['content']
            captions = self._parse_captions(captions_text)
            
            logger.info("Generated captions")
            
            return {
                'status': 'success',
                'captions': captions
            }
            
        except Exception as e:
            logger.error(f"Error generating captions: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def _parse_captions(text: str) -> List[str]:
        """Parse caption text into list"""
        captions = []
        for line in text.split('\n'):
            if line.startswith('Caption'):
                caption = line.split(': ', 1)[1] if ': ' in line else line
                captions.append(caption)
        return captions