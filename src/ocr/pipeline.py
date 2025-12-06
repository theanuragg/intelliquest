from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from src.ocr.processor import OCRProcessor
from src.config import DOWNLOADS_DIR, CACHE_DIR
from src.utils.logger import get_logger

logger = get_logger("document_pipeline")


class DocumentPipeline:
    """End-to-end document processing pipeline"""

    def __init__(self):
        self.ocr_processor = OCRProcessor()
        self.metadata_dir = CACHE_DIR / "document_metadata"
        self.metadata_dir.mkdir(exist_ok=True)

    def process_document(
        self, filepath: str, extract_text: bool = True
    ) -> Dict[str, Any]:
        """Process a single document through the entire pipeline"""
        filepath = Path(filepath)

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return {"status": "error", "error": "File not found"}

        file_type = filepath.suffix.lower()
        logger.info(f"Processing document: {filepath.name} ({file_type})")

        # Extract OCR text
        ocr_result = None
        cleaned_text = None

        if extract_text:
            if file_type in [".pdf"]:
                ocr_result = self.ocr_processor.extract_text_from_pdf(str(filepath))
            elif file_type in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
                ocr_result = self.ocr_processor.extract_text_from_image(str(filepath))
            else:
                logger.warning(f"Unsupported file type: {file_type}")
                ocr_result = {"status": "error", "error": f"Unsupported file type: {file_type}"}

            if ocr_result.get("status") == "success":
                raw_text = ocr_result.get("raw_ocr_text", "")
                cleaned_text = self.ocr_processor.clean_ocr_text(raw_text)

        # Compile document metadata
        document_result = {
            "status": "success",
            "filename": filepath.name,
            "filepath": str(filepath),
            "file_type": file_type,
            "file_size": filepath.stat().st_size,
            "processed_at": datetime.utcnow().isoformat(),
            "ocr_result": ocr_result,
            "cleaned_text": cleaned_text,
        }

        # Save metadata
        self._save_document_metadata(filepath.name, document_result)

        logger.info(f"Document processed successfully: {filepath.name}")
        return document_result

    def _save_document_metadata(self, filename: str, metadata: Dict[str, Any]):
        """Save document processing metadata"""
        metadata_file = self.metadata_dir / f"{filename}.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def get_document_metadata(self, filename: str) -> Optional[Dict[str, Any]]:
        """Retrieve saved document metadata"""
        metadata_file = self.metadata_dir / f"{filename}.json"
        if metadata_file.exists():
            with open(metadata_file, "r") as f:
                return json.load(f)
        return None
