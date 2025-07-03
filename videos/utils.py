"""
Video processing utilities for background tasks
"""
import os
import ffmpeg
from datetime import timedelta
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Video, VideoFile


def get_video_duration(file_path):
    """
    Get video duration using ffmpeg
    """
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['streams'][0]['duration'])
        return timedelta(seconds=duration)
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return timedelta(0)


def generate_thumbnail(video_file_path, output_path, timestamp='00:00:01'):
    """
    Generate thumbnail from video at specific timestamp
    """
    try:
        (
            ffmpeg
            .input(video_file_path, ss=timestamp)
            .output(output_path, vframes=1, format='image2', vcodec='png')
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return False


def convert_video_quality(input_path, output_path, quality):
    """
    Convert video to specific quality using ffmpeg
    """
    quality_settings = {
        '120p': {'width': 160, 'height': 120, 'bitrate': '96k'},
        '360p': {'width': 640, 'height': 360, 'bitrate': '800k'},
        '720p': {'width': 1280, 'height': 720, 'bitrate': '2500k'},
        '1080p': {'width': 1920, 'height': 1080, 'bitrate': '5000k'},
    }
    
    if quality not in quality_settings:
        raise ValueError(f"Unsupported quality: {quality}")
    
    settings_dict = quality_settings[quality]
    
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='libx264',
                acodec='aac',
                vf=f"scale={settings_dict['width']}:{settings_dict['height']}",
                video_bitrate=settings_dict['bitrate'],
                audio_bitrate='128k',
                format='mp4'
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except Exception as e:
        print(f"Error converting video to {quality}: {e}")
        return False


def process_video_upload(video_id):
    """
    Background task to process uploaded video
    """
    try:
        video = Video.objects.get(id=video_id)
        
        # Find the original uploaded file
        original_file = video.video_files.filter(is_processed=False).first()
        if not original_file:
            print(f"No unprocessed file found for video {video_id}")
            return
        
        original_path = original_file.file.path
        
        # Get video duration
        duration = get_video_duration(original_path)
        video.duration = duration
        video.save()
        
        # Generate thumbnail
        thumbnail_filename = f"thumb_{video.id}_{video.title[:20]}.png"
        thumbnail_path = os.path.join(
            settings.MEDIA_ROOT, 
            'video_thumbnails', 
            thumbnail_filename
        )
        
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        
        if generate_thumbnail(original_path, thumbnail_path):
            with open(thumbnail_path, 'rb') as thumb_file:
                video.thumbnail.save(
                    thumbnail_filename,
                    ContentFile(thumb_file.read()),
                    save=True
                )
        
        # Convert to different qualities
        qualities_to_generate = ['120p', '360p', '720p', '1080p']
        
        for quality in qualities_to_generate:
            output_filename = f"{video.id}_{quality}.mp4"
            output_path = os.path.join(
                settings.MEDIA_ROOT,
                'videos',
                output_filename
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if convert_video_quality(original_path, output_path, quality):
                # Create VideoFile record
                with open(output_path, 'rb') as video_file:
                    file_size = os.path.getsize(output_path)
                    
                    video_file_obj = VideoFile.objects.create(
                        video=video,
                        quality=quality,
                        file_size=file_size,
                        is_processed=True
                    )
                    
                    video_file_obj.file.save(
                        output_filename,
                        ContentFile(video_file.read()),
                        save=True
                    )
        
        # Mark original file as processed
        original_file.is_processed = True
        original_file.save()
        
        print(f"Video {video_id} processed successfully")
        
    except Video.DoesNotExist:
        print(f"Video with id {video_id} not found")
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")


def cleanup_temp_files(video_id):
    """
    Clean up temporary files after processing
    """
    try:
        # This would clean up any temporary files created during processing
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp', str(video_id))
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error cleaning up temp files for video {video_id}: {e}")


def get_video_quality_recommendations(user_agent=None):
    """
    Recommend video quality based on user agent or device
    """
    # Simple quality recommendation logic
    # In a real application, this could be more sophisticated
    if user_agent:
        if 'Mobile' in user_agent:
            return '360p'
        elif 'Tablet' in user_agent:
            return '720p'
    
    return '720p'  # Default quality


def format_duration(duration):
    """
    Format duration timedelta object to readable string
    """
    if not duration:
        return "00:00"
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def format_file_size(size_bytes):
    """
    Format file size in bytes to readable string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_bytes = float(size_bytes)
    i = 0
    
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
