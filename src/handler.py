import json
import boto3
import os
import logging
from urllib.parse import unquote_plus
from PIL import Image
import io

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

# Environment variables
DEST_BUCKET = os.environ['DEST_BUCKET']
THUMBNAIL_SIZE = tuple(map(int, os.environ.get('THUMBNAIL_SIZE', '256x256').split('x')))

# Allowed image formats
ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}

def lambda_handler(event, context):
    """
    Lambda function to process S3 image uploads and create thumbnails
    """
    try:
        # Process each record in the event
        for record in event['Records']:
            # Extract S3 bucket and object key
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            
            logger.info(f"Processing image: {key} from bucket: {bucket}")
            
            # Download image from S3
            try:
                response = s3_client.get_object(Bucket=bucket, Key=key)
                image_content = response['Body'].read()
            except Exception as e:
                logger.error(f"Error downloading image {key}: {str(e)}")
                continue
            
            # Process image with Pillow
            try:
                # Open image
                image = Image.open(io.BytesIO(image_content))
                
                # Validate format
                if image.format not in ALLOWED_FORMATS:
                    logger.warning(f"Unsupported format {image.format} for {key}")
                    continue
                
                # Create thumbnail maintaining aspect ratio
                image.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                
                # Convert to RGB if necessary (for JPEG)
                if image.mode in ('RGBA', 'P'):
                    image = image.convert('RGB')
                
                # Save thumbnail to bytes
                thumbnail_buffer = io.BytesIO()
                image.save(thumbnail_buffer, format='JPEG', quality=85, optimize=True)
                thumbnail_buffer.seek(0)
                
                # Generate thumbnail key
                file_name = os.path.splitext(os.path.basename(key))[0]
                thumbnail_key = f"thumbnails/{file_name}_thumb.jpg"
                
                # Upload thumbnail to destination bucket
                s3_client.put_object(
                    Bucket=DEST_BUCKET,
                    Key=thumbnail_key,
                    Body=thumbnail_buffer.getvalue(),
                    ContentType='image/jpeg',
                    Metadata={
                        'original-key': key,
                        'original-size': f"{image_content.__len__()}",
                        'thumbnail-size': f"{len(thumbnail_buffer.getvalue())}"
                    }
                )
                
                logger.info(f"Thumbnail created: {thumbnail_key}")
                
            except Exception as e:
                logger.error(f"Error processing image {key}: {str(e)}")
                continue
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Images processed successfully',
                'processed_count': len(event['Records'])
            })
        }
        
    except Exception as e:
        logger.error(f"Lambda execution error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }
