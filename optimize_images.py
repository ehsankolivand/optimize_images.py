import os
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import io
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analyze_image_quality(original_data: bytes, webp_data: bytes) -> float:
    """
    Compare original and WebP image quality using structural analysis.
    Returns a similarity score between 0 and 1.
    """
    try:
        with Image.open(io.BytesIO(original_data)) as img1, \
             Image.open(io.BytesIO(webp_data)) as img2:
            # Convert both images to RGB mode for consistent comparison
            img1 = img1.convert('RGB')
            img2 = img2.convert('RGB')
            
            # Ensure same size for comparison
            if img1.size != img2.size:
                img2 = img2.resize(img1.size)
            
            # Compare images pixel by pixel
            diff = 0
            pixels1 = img1.getdata()
            pixels2 = img2.getdata()
            
            for p1, p2 in zip(pixels1, pixels2):
                diff += sum((a - b) ** 2 for a, b in zip(p1, p2))
            
            # Normalize difference score
            max_diff = float(len(pixels1) * 3 * (255 ** 2))
            similarity = 1 - (diff / max_diff)
            
            return similarity
    except Exception as e:
        logger.error(f"Error analyzing image quality: {e}")
        return 0.0

def convert_to_webp(image_path: Path) -> Optional[Tuple[bool, str]]:
    """
    Convert image to WebP format if beneficial.
    Returns (success, message) tuple or None if conversion should be skipped.
    """
    try:
        # Read original image and get its size
        with open(image_path, 'rb') as f:
            original_data = f.read()
        original_size = len(original_data)
        
        # Open and convert image to WebP
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                alpha = img.getchannel('A')
                # Use lossless for images with transparency
                webp_buffer = io.BytesIO()
                img.save(webp_buffer, 'WEBP', lossless=True, quality=90)
                webp_data = webp_buffer.getvalue()
            else:
                img = img.convert('RGB')
                # Try different quality settings
                best_size = original_size
                best_quality = 90
                best_data = None
                
                for quality in [90, 85, 80]:
                    webp_buffer = io.BytesIO()
                    img.save(webp_buffer, 'WEBP', quality=quality)
                    webp_data = webp_buffer.getvalue()
                    
                    if len(webp_data) < best_size:
                        similarity = analyze_image_quality(original_data, webp_data)
                        if similarity >= 0.95:  # 95% similarity threshold
                            best_size = len(webp_data)
                            best_quality = quality
                            best_data = webp_data
                
                if best_data is None:
                    return None  # Skip conversion
                webp_data = best_data

        # Check if conversion is beneficial
        webp_size = len(webp_data)
        if webp_size >= original_size:
            return None  # Skip conversion
        
        # Save WebP version
        webp_path = image_path.with_suffix('.webp')
        with open(webp_path, 'wb') as f:
            f.write(webp_data)
        
        # Delete original only after successful WebP creation
        os.remove(image_path)
        
        savings = (original_size - webp_size) / original_size * 100
        return True, f"Converted {image_path.name}: {savings:.1f}% smaller"
        
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")
        return False, f"Failed to convert {image_path.name}: {str(e)}"

def process_directory(directory: Path) -> Tuple[int, int, int]:
    """
    Process all images in directory and subdirectories.
    Returns (success_count, skip_count, error_count) tuple.
    """
    success_count = 0
    skip_count = 0
    error_count = 0
    
    # Find all supported image files
    image_files = []
    for ext in ('.jpg', '.jpeg', '.png'):
        image_files.extend(directory.rglob(f"*{ext}"))
    
    total_files = len(image_files)
    logger.info(f"Found {total_files} images to process")
    
    # Process images in parallel
    with ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(convert_to_webp, image_files), 1):
            if result is None:
                skip_count += 1
                logger.info(f"[{i}/{total_files}] Skipped conversion (not beneficial)")
            else:
                success, message = result
                if success:
                    success_count += 1
                else:
                    error_count += 1
                logger.info(f"[{i}/{total_files}] {message}")
    
    return success_count, skip_count, error_count

def main():
    """Main entry point for the script."""
    try:
        directory = Path.cwd()
        logger.info(f"Starting image optimization in: {directory}")
        
        success, skipped, errors = process_directory(directory)
        
        logger.info("\nOptimization Complete!")
        logger.info(f"Successfully converted: {success}")
        logger.info(f"Skipped (not beneficial): {skipped}")
        logger.info(f"Errors: {errors}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()