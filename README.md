# Serverless Image Processing Application

## Quick Start

1. **Prerequisites**: Ensure AWS CLI, SAM CLI, and Docker are installed
2. **Deploy Infrastructure**: 
   ```bash
   sam build --use-container
   sam deploy --guided
   ```
3. **Deploy UI**: Follow instructions in `deploy-ui.md`
4. **Test**: Upload images via web interface

## Architecture

Browser → S3 (source) → Lambda (Pillow) → S3 (thumbnails)

## Files Structure

```
├── template.yaml          # SAM template
├── src/
│   ├── handler.py         # Lambda function
│   └── requirements.txt   # Python dependencies
├── ui/
│   └── index.html        # Web interface
├── events/
│   └── s3-event.json     # Test event
└── deploy-ui.md          # UI deployment guide
```

## Cost Estimate (Free Tier)

- S3: Free for 5GB storage, 20K GET, 2K PUT requests/month
- Lambda: Free for 1M requests, 400K GB-seconds/month
- CloudWatch: Basic monitoring included
- **Total**: $0/month within free tier limits

## Security Features

- IAM least privilege permissions
- CORS configuration for browser uploads
- File type and size validation
- Structured logging for monitoring