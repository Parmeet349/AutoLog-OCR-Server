from PIL import Image, ImageFilter, ImageOps

def preprocess_pil(pil_img: Image.Image) -> Image.Image:
    # Convert to grayscale
    img = pil_img.convert("L")
    
    # Increase contrast
    img = ImageOps.autocontrast(img, cutoff=2)
    
    # Slight sharpening
    img = img.filter(ImageFilter.SHARPEN)
    
    # Optional: resize small images to improve OCR
    base_width = 800
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    
    return img
