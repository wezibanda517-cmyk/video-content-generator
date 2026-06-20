"""Facebook API integration module"""

import os
import requests
import logging
from typing import Dict, Optional
from config import Config

logger = logging.getLogger(__name__)


class FacebookUploader:
    """Handle Facebook video uploads and posts"""
    
    def __init__(self, access_token: str = None, page_id: str = None):
        """Initialize Facebook uploader
        
        Args:
            access_token: Facebook page access token
            page_id: Facebook page ID
        """
        self.access_token = access_token or Config.FACEBOOK_ACCESS_TOKEN
        self.page_id = page_id or Config.FACEBOOK_PAGE_ID
        self.api_version = Config.FACEBOOK_API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def upload_video(self,
                    video_path: str,
                    title: str,
                    description: str = '',
                    thumbnail_path: str = None) -> Dict[str, any]:
        """Upload video to Facebook
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            thumbnail_path: Path to custom thumbnail
            
        Returns:
            Dictionary with upload result
        """
        try:
            if not os.path.exists(video_path):
                return {'status': 'error', 'message': 'Video file not found'}
            
            file_size = os.path.getsize(video_path)
            logger.info(f"Uploading video: {title} (Size: {file_size} bytes)")
            
            # Prepare upload URL
            upload_url = f"{self.base_url}/{self.page_id}/videos"
            
            # Prepare files
            with open(video_path, 'rb') as video_file:
                files = {
                    'source': video_file,
                }
                
                data = {
                    'title': title,
                    'description': description,
                    'access_token': self.access_token,
                    'published': False  # Save as draft first
                }
                
                # If thumbnail provided, use it
                if thumbnail_path and os.path.exists(thumbnail_path):
                    with open(thumbnail_path, 'rb') as thumb_file:
                        files['thumb'] = thumb_file
                        response = requests.post(upload_url, files=files, data=data)
                else:
                    response = requests.post(upload_url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                video_id = result.get('id')
                
                logger.info(f"Video uploaded successfully: {video_id}")
                
                return {
                    'status': 'success',
                    'video_id': video_id,
                    'message': 'Video uploaded as draft. Review and publish on Facebook.',
                    'facebook_url': f"https://www.facebook.com/{self.page_id}/videos/{video_id}"
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Upload failed: {error_msg}")
                
                return {
                    'status': 'error',
                    'message': f'Upload failed: {error_msg}'
                }
        
        except Exception as e:
            logger.error(f"Error uploading video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def publish_video(self,
                     video_id: str,
                     caption: str = '',
                     scheduled_publish_time: int = None) -> Dict[str, any]:
        """Publish a video to Facebook timeline
        
        Args:
            video_id: Facebook video ID
            caption: Post caption
            scheduled_publish_time: Unix timestamp for scheduled posting
            
        Returns:
            Dictionary with publish result
        """
        try:
            url = f"{self.base_url}/{video_id}"
            
            data = {
                'access_token': self.access_token,
                'published': True,
                'message': caption
            }
            
            if scheduled_publish_time:
                data['scheduled_publish_time'] = scheduled_publish_time
                data['published'] = False
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                logger.info(f"Video published successfully: {video_id}")
                return {
                    'status': 'success',
                    'video_id': video_id,
                    'message': 'Video published successfully'
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Publish failed: {error_msg}")
                
                return {
                    'status': 'error',
                    'message': f'Publish failed: {error_msg}'
                }
        
        except Exception as e:
            logger.error(f"Error publishing video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def get_video_insights(self, video_id: str) -> Dict[str, any]:
        """Get video analytics and insights
        
        Args:
            video_id: Facebook video ID
            
        Returns:
            Dictionary with video insights
        """
        try:
            url = f"{self.base_url}/{video_id}/insights"
            
            params = {
                'access_token': self.access_token,
                'metric': 'post_video_views,post_video_complete_views,post_video_complete_rate'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                insights = response.json().get('data', [])
                
                logger.info(f"Retrieved insights for video: {video_id}")
                
                return {
                    'status': 'success',
                    'insights': insights
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                
                return {
                    'status': 'error',
                    'message': f'Failed to get insights: {error_msg}'
                }
        
        except Exception as e:
            logger.error(f"Error getting insights: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def delete_video(self, video_id: str) -> Dict[str, any]:
        """Delete a video from Facebook
        
        Args:
            video_id: Facebook video ID
            
        Returns:
            Dictionary with deletion result
        """
        try:
            url = f"{self.base_url}/{video_id}"
            
            params = {'access_token': self.access_token}
            
            response = requests.delete(url, params=params)
            
            if response.status_code == 200:
                logger.info(f"Video deleted successfully: {video_id}")
                return {
                    'status': 'success',
                    'message': 'Video deleted successfully'
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                
                return {
                    'status': 'error',
                    'message': f'Deletion failed: {error_msg}'
                }
        
        except Exception as e:
            logger.error(f"Error deleting video: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def validate_credentials(self) -> Dict[str, any]:
        """Validate Facebook credentials
        
        Returns:
            Dictionary with validation result
        """
        try:
            url = f"{self.base_url}/me"
            
            params = {'access_token': self.access_token}
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Credentials validated for account: {data.get('name')}")
                
                return {
                    'status': 'success',
                    'message': 'Credentials are valid',
                    'account': data
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Invalid credentials'
                }
        
        except Exception as e:
            logger.error(f"Error validating credentials: {str(e)}")
            return {'status': 'error', 'message': str(e)}