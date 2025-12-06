"""
Watermark utility for applying watermarks to images using Pillow.
Used to mark AI-generated recipe images with the Google AI logo.
"""
import io
from pathlib import Path

from PIL import Image


def apply_watermark(image_bytes: bytes, watermark_path: Path | None = None, opacity: float = 0.7) -> bytes:
    """
    Apply a watermark to an image in the lower right corner.
    
    Args:
        image_bytes: The original image as bytes
        watermark_path: Path to the watermark image. If None, uses default AI robot watermark
        opacity: Opacity of the watermark (0.0 to 1.0)
    
    Returns:
        The watermarked image as bytes
    """
    # Use default watermark if none provided
    if watermark_path is None:
        watermark_path = Path(__file__).parent / "ai-watermark.png"
    
    # Open the base image
    base_image = Image.open(io.BytesIO(image_bytes))
    
    # Ensure base image is in RGBA mode for transparency
    if base_image.mode != "RGBA":
        base_image = base_image.convert("RGBA")
    
    # Open and prepare the watermark
    watermark = Image.open(watermark_path)
    if watermark.mode != "RGBA":
        watermark = watermark.convert("RGBA")
    
    # Calculate watermark size (10% of image width, maintaining aspect ratio)
    base_width, base_height = base_image.size
    watermark_width = int(base_width * 0.15)  # 15% of image width
    aspect_ratio = watermark.size[1] / watermark.size[0]
    watermark_height = int(watermark_width * aspect_ratio)
    
    # Resize watermark
    watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
    
    # Adjust opacity
    if opacity < 1.0:
        # Create a new image with adjusted alpha channel
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        watermark.putalpha(alpha)
    
    # Calculate position (lower right corner with 20px padding)
    padding = 20
    position = (
        base_width - watermark_width - padding,
        base_height - watermark_height - padding
    )
    
    # Create a transparent layer for compositing
    transparent = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    transparent.paste(watermark, position, watermark)
    
    # Composite the watermark onto the base image
    watermarked = Image.alpha_composite(base_image, transparent)
    
    # Convert back to RGB if original was RGB
    if image_bytes[:4] == b'\xff\xd8\xff\xe0' or image_bytes[:4] == b'\xff\xd8\xff\xe1':  # JPEG magic bytes
        watermarked = watermarked.convert("RGB")
    
    # Save to bytes
    output = io.BytesIO()
    if watermarked.mode == "RGBA":
        watermarked.save(output, format="PNG")
    else:
        watermarked.save(output, format="JPEG", quality=95)
    
    return output.getvalue()
