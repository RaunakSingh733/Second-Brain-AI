"""
Batch upload service for handling multiple file uploads efficiently.
"""

import os
import logging
from typing import List, Dict, Any
from fastapi import UploadFile
from pathlib import Path

logger = logging.getLogger(__name__)


class BatchUploadService:
    """
    Service for handling batch file uploads and processing.
    
    Features:
    - Upload multiple files at once
    - Track progress for each file
    - Handle errors gracefully
    - Validate file types and sizes
    """

    def __init__(self):
        self.upload_dir = "./uploads"
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {'.pdf', '.txt', '.md', '.docx'}

    async def batch_upload(
        self,
        files: List[UploadFile],
        skip_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Upload multiple files at once.
        
        Args:
            files: List of uploaded files
            skip_existing: Skip if file already exists
            
        Returns:
            {
                'total': int,
                'successful': int,
                'failed': int,
                'results': List[upload result],
                'errors': List[error messages]
            }
        """
        results = {
            'total': len(files),
            'successful': 0,
            'failed': 0,
            'results': [],
            'errors': []
        }

        for idx, file in enumerate(files):
            try:
                result = await self._upload_single_file(file, skip_existing)
                if result['status'] == 'success':
                    results['successful'] += 1
                    results['results'].append(result)
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'file': file.filename,
                        'error': result.get('error', 'Unknown error')
                    })
            except Exception as e:
                logger.error(f"Error uploading file {file.filename}: {str(e)}")
                results['failed'] += 1
                results['errors'].append({
                    'file': file.filename,
                    'error': str(e)
                })

        logger.info(
            f"Batch upload complete: {results['successful']}/{results['total']} successful"
        )
        return results

    async def _upload_single_file(
        self,
        file: UploadFile,
        skip_existing: bool
    ) -> Dict[str, Any]:
        """
        Upload a single file with validation.
        """
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return {
                'status': 'error',
                'file': file.filename,
                'error': f'Invalid file type: {file_ext}. Allowed: {self.allowed_extensions}'
            }

        # Read file content to check size
        content = await file.read()
        if len(content) > self.max_file_size:
            return {
                'status': 'error',
                'file': file.filename,
                'error': f'File too large: {len(content)} bytes (max: {self.max_file_size})'
            }

        # Check if file already exists
        file_path = os.path.join(self.upload_dir, file.filename)
        if os.path.exists(file_path):
            if skip_existing:
                return {
                    'status': 'skipped',
                    'file': file.filename,
                    'message': 'File already exists'
                }

        # Save file
        try:
            os.makedirs(self.upload_dir, exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(content)

            return {
                'status': 'success',
                'file': file.filename,
                'size': len(content),
                'path': file_path
            }
        except Exception as e:
            return {
                'status': 'error',
                'file': file.filename,
                'error': f'Failed to save file: {str(e)}'
            }


# Singleton instance
batch_upload_service = BatchUploadService()
