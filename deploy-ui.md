# UI Deployment Options

## Option A: S3 Static Website + CloudFront

### Step 1: Create S3 Bucket for Website
```bash
aws s3 mb s3://my-image-processor-ui-{{AWS_ACCOUNT_ID}}
```

### Step 2: Enable Static Website Hosting
```bash
aws s3 website s3://my-image-processor-ui-{{AWS_ACCOUNT_ID}} --index-document index.html
```

### Step 3: Upload UI Files
```bash
aws s3 cp ui/index.html s3://my-image-processor-ui-{{AWS_ACCOUNT_ID}}/
```

### Step 4: Set Bucket Policy (Public Read)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-image-processor-ui-{{AWS_ACCOUNT_ID}}/*"
        }
    ]
}
```

### Step 5: Access Website
URL: `http://my-image-processor-ui-{{AWS_ACCOUNT_ID}}.s3-website-{{AWS_REGION}}.amazonaws.com`

## Option B: AWS Amplify Hosting

### Console Steps:
1. Go to AWS Amplify Console
2. Click "Host your web app"
3. Choose "Deploy without Git provider"
4. Upload `ui` folder as ZIP
5. App will be deployed automatically

### Benefits:
- HTTPS by default
- Global CDN
