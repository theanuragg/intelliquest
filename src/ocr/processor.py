import os
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

import pytesseract
from PIL import Image
import re

from src.config import CACHE_DIR, TESSERACT_PATH
from src.utils.logger import get_logger

logger = get_logger("ocr_processor")

# Set tesseract path if available
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.pytesseract_cmd = TESSERACT_PATH


class OCRProcessor:
    """Handle document OCR and text extraction"""

    def __init__(self):
        self.cache_dir = CACHE_DIR / "ocr_cache"
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, filepath: str) -> str:
        """Generate cache key for OCR result"""
        file_hash = hashlib.md5(str(filepath).encode()).hexdigest()
        return file_hash

    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load OCR result from cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            with open(cache_file, "r") as f:
                logger.info(f"Loaded OCR from cache: {cache_key}")
                return json.load(f)
        return None

    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]):
        """Save OCR result to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Cached OCR result: {cache_key}")

    def extract_text_from_image(
        self, image_path: str, use_cache: bool = True
    ) -> Dict[str, Any]:
        """Extract text from image using Tesseract"""
        image_path = Path(image_path)

        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return {"status": "error", "error": "Image not found"}

        # Check cache
        cache_key = self._get_cache_key(str(image_path))
        if use_cache:
            cached_result = self._load_from_cache(cache_key)
            if cached_result:
                return cached_result

        try:
            img = Image.open(image_path)
            raw_text = pytesseract.image_to_string(img)

            result = {
                "status": "success",
                "source_file": str(image_path),
                "raw_ocr_text": raw_text,
                "confidence": self._estimate_confidence(raw_text),
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Save to cache
            self._save_to_cache(cache_key, result)

            logger.info(f"OCR extracted from {image_path.name}")
            return result

        except Exception as e:
            logger.error(f"OCR extraction failed for {image_path}: {str(e)}")
            return {
                "status": "error",
                "source_file": str(image_path),
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    def extract_text_from_pdf(
        self, pdf_path: str, use_cache: bool = True
    ) -> Dict[str, Any]:
        """Extract text from PDF by converting to images"""
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            logger.error(f"PDF not found: {pdf_path}")
            return {"status": "error", "error": "PDF not found"}

        # Check cache
        cache_key = self._get_cache_key(str(pdf_path))
        if use_cache:
            cached_result = self._load_from_cache(cache_key)
            if cached_result:
                return cached_result

        try:
            # Try to import pdf2image, fallback if not available
            try:
                from pdf2image import convert_from_path

                images = convert_from_path(str(pdf_path))
            except ImportError:
                logger.warning("pdf2image not installed, attempting alternative method")
                # Fallback: assume PDF might have been downloaded as image or use ImageMagick
                logger.error("pdf2image required for PDF processing")
                return {
                    "status": "error",
                    "error": "pdf2image not installed. Install with: pip install pdf2image",
                }

            all_text = []
            for page_num, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                all_text.append({"page": page_num + 1, "text": text})

            combined_text = "\n\n".join([p["text"] for p in all_text])

            result = {
                "status": "success",
                "source_file": str(pdf_path),
                "raw_ocr_text": combined_text,
                "pages": all_text,
                "total_pages": len(all_text),
                "confidence": self._estimate_confidence(combined_text),
                "timestamp": datetime.utcnow().isoformat(),
            }

            self._save_to_cache(cache_key, result)
            logger.info(f"OCR extracted from PDF {pdf_path.name} ({len(all_text)} pages)")
            return result

        except Exception as e:
            logger.error(f"PDF OCR extraction failed for {pdf_path}: {str(e)}")
            return {
                "status": "error",
                "source_file": str(pdf_path),
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _estimate_confidence(self, text: str) -> float:
        """Estimate OCR confidence based on text quality"""
        if not text:
            return 0.0

        # Simple heuristic: check for common OCR errors and word validity
        total_chars = len(text)
        suspicious_patterns = len(
            re.findall(r"[0O]{2,}|l{3,}|[!1]{2,}", text)
        )  # Common OCR mistakes
        suspicious_score = suspicious_patterns / (total_chars / 100) if total_chars > 0 else 0

        confidence = max(0.0, 1.0 - (suspicious_score / 10))
        return round(confidence, 3)

    def clean_ocr_text(self, raw_text: str) -> str:
        """Clean and normalize OCR text"""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", raw_text)

        # Fix common OCR mistakes
        replacements = {
            r"\b0(?=[A-Z])\b": "O",  # 0 -> O at word boundary
            r"(?<=[a-z])l(?=[a-z]{2,})": "i",  # l -> i in words
            r"rn\b": "m",  # rn -> m at end
        }

        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Normalize spacing around punctuation
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        text = re.sub(r"([.,!?;:])\s*(?=[A-Z])", r"\1 ", text)

        return text.strip()
