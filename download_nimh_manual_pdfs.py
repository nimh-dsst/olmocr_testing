import boto3
import json
import os
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'nimh_pdf_download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def create_download_directory():
    """Create the download directory if it doesn't exist."""
    download_dir = Path('nimh_pdfs_2024')
    download_dir.mkdir(exist_ok=True)
    return download_dir

def load_pdf_filenames():
    """Load PDF filenames from the JSON file."""
    try:
        with open('nimh_manual_pdfs_2024.json', 'r') as f:
            data = json.load(f)
            return data.get('nimh manual 2024', [])
    except FileNotFoundError:
        logging.error("JSON file not found: nimh_manual_pdfs_2024.json")
        return []
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in nimh_manual_pdfs_2024.json")
        return []

def find_pdf_in_s3(s3_client, bucket, filename):
    """Search for a PDF file in the S3 bucket recursively."""
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        if 'Contents' not in page:
            continue
        for obj in page['Contents']:
            if obj['Key'].endswith(filename):
                return obj['Key']
    return None

def download_pdfs():
    """Main function to download PDFs from S3."""
    s3_client = boto3.client('s3')
    bucket = 'osm-pdf-uploads'
    download_dir = create_download_directory()
    pdf_filenames = load_pdf_filenames()
    
    if not pdf_filenames:
        logging.error("No PDF filenames found in the JSON file")
        return
    
    successful_downloads = []
    failed_downloads = []
    
    for filename in pdf_filenames:
        logging.info(f"Searching for {filename} in S3 bucket...")
        s3_key = find_pdf_in_s3(s3_client, bucket, filename)
        
        if s3_key:
            try:
                local_path = download_dir / filename
                s3_client.download_file(bucket, s3_key, str(local_path))
                logging.info(f"Successfully downloaded {filename}")
                successful_downloads.append(filename)
            except Exception as e:
                logging.error(f"Error downloading {filename}: {str(e)}")
                failed_downloads.append(filename)
        else:
            logging.warning(f"Could not find {filename} in S3 bucket")
            failed_downloads.append(filename)
    
    # Log summary
    logging.info("\nDownload Summary:")
    logging.info(f"Total PDFs processed: {len(pdf_filenames)}")
    logging.info(f"Successfully downloaded: {len(successful_downloads)}")
    logging.info(f"Failed to download: {len(failed_downloads)}")
    
    if failed_downloads:
        logging.info("\nFailed downloads:")
        for filename in failed_downloads:
            logging.info(f"- {filename}")

if __name__ == "__main__":
    download_pdfs()
