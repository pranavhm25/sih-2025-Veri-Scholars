from PIL import Image, ImageDraw, ImageFont
import os

# Predefined successful certificate details
certs = [
    {
        "certificate_id": "JHK-2025-CS-042",
        "name": "Aditi Sharma",
        "institution": "Birla Institute of Technology, Mesra",
        "course": "B.Tech Computer Science",
        "year": "2025"
    },
    {
        "certificate_id": "JHK-2024-ME-109",
        "name": "Rohan Das",
        "institution": "NIT Jamshedpur",
        "course": "B.Tech Mechanical Engineering",
        "year": "2024"
    },
    {
        "certificate_id": "JHK-2025-EE-201",
        "name": "Priya Patel",
        "institution": "IIT (ISM) Dhanbad",
        "course": "B.Tech Electrical Engineering",
        "year": "2025"
    },
    {
        "certificate_id": "JHK-2023-EC-304",
        "name": "Vikram Singh",
        "institution": "Ranchi University",
        "course": "B.Sc Electronics",
        "year": "2023"
    }
]

output_dir = "demo_certificates"
os.makedirs(output_dir, exist_ok=True)

# Try loading a standard font from Windows, otherwise use fallback default
try:
    font_path_title = "C:\\Windows\\Fonts\\georgiab.ttf" # Georgia Bold for elegant heading
    font_path_text = "C:\\Windows\\Fonts\\arial.ttf"    # Arial for clean OCR readability
    
    font_title = ImageFont.truetype(font_path_title, 40)
    font_subtitle = ImageFont.truetype(font_path_text, 20)
    font_label = ImageFont.truetype(font_path_text, 24)
    font_val = ImageFont.truetype(font_path_title, 26)
    font_id = ImageFont.truetype(font_path_text, 20)
except Exception:
    # Fallback to default PIL font if standard fonts aren't accessible
    font_title = font_subtitle = font_label = font_val = font_id = ImageFont.load_default()

for c in certs:
    # Create a blank high-resolution certificate canvas (1200x800, soft cream background)
    img = Image.new('RGB', (1200, 800), color='#FDFBF7')
    draw = ImageDraw.Draw(img)
    
    # 1. Draw elegant double borders
    draw.rectangle([20, 20, 1180, 780], outline='#D4AF37', width=5)  # Gold border
    draw.rectangle([30, 30, 1170, 770], outline='#1E293B', width=2)  # Charcoal inner border
    
    # Draw simple gold corners
    draw.rectangle([15, 15, 45, 45], fill='#D4AF37')
    draw.rectangle([1155, 15, 1185, 45], fill='#D4AF37')
    draw.rectangle([15, 755, 45, 785], fill='#D4AF37')
    draw.rectangle([1155, 755, 1185, 785], fill='#D4AF37')

    # 2. Draw Headers
    draw.text((600, 100), "BOARD OF HIGHER EDUCATION", fill='#1E293B', font=font_subtitle, anchor="mm")
    draw.text((600, 160), "CERTIFICATE OF ACHIEVEMENT", fill='#9A7B1C', font=font_title, anchor="mm")
    draw.text((600, 220), "This is proudly presented to verify the institutional credentials of", fill='#475569', font=font_subtitle, anchor="mm")

    # 3. Draw Main Fields (OCR-friendly key-value formatting)
    # Name
    draw.text((600, 280), "NAME", fill='#64748B', font=font_label, anchor="mm")
    draw.text((600, 320), c["name"], fill='#1E293B', font=font_val, anchor="mm")
    draw.line([400, 340, 800, 340], fill='#9A7B1C', width=1)

    # Details text
    details_text = f"who has completed the prescribed graduation requirements and is declared qualified for the award of"
    draw.text((600, 390), details_text, fill='#475569', font=font_subtitle, anchor="mm")

    # Course
    draw.text((600, 440), c["course"], fill='#1E293B', font=font_val, anchor="mm")
    
    # Institution / University
    draw.text((600, 500), "INSTITUTION", fill='#64748B', font=font_label, anchor="mm")
    draw.text((600, 545), c["institution"], fill='#1E293B', font=font_val, anchor="mm")
    
    # Year
    draw.text((600, 600), f"Graduation Year: {c['year']}", fill='#475569', font=font_val, anchor="mm")

    # 4. Draw Unique Secure Identifiers (ID and simulated security hash)
    draw.text((150, 710), f"CERTIFICATE ID: {c['certificate_id']}", fill='#1E293B', font=font_id)
    
    # Compute standard HMAC signature for display
    import hmac
    import hashlib
    mac = hmac.new(b"veri-scholars-dev-key-change-in-production", digestmod=hashlib.sha256)
    # Feed some structured data to get a stable deterministic hash matching our default seed
    mac.update(f"{c['certificate_id']}|{c['name']}|{c['institution']}".encode('utf-8'))
    secure_sig = mac.hexdigest()[:32] # display half of it as a seal hash
    
    draw.text((800, 710), f"SECURE SEAL HASH: {secure_sig}", fill='#64748B', font=font_id)

    # Save image
    file_name = f"{c['certificate_id']}.png"
    img.save(os.path.join(output_dir, file_name))
    print(f"Generated {file_name}")
