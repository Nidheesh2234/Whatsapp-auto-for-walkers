"""
Batch Splitter - Split 700 QR codes into smaller batches
Useful for safer sending in multiple sessions
"""

import os
import shutil

SOURCE_FOLDER = "qr_codes"
BATCH_SIZE = 100  # Files per batch folder

print("📦 QR Code Batch Splitter\n")

if not os.path.exists(SOURCE_FOLDER):
    print(f"❌ Error: '{SOURCE_FOLDER}' folder not found!")
    exit(1)

# Get all QR files
qr_files = [f for f in os.listdir(SOURCE_FOLDER) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

total_files = len(qr_files)
if total_files == 0:
    print(f"❌ No QR images found in '{SOURCE_FOLDER}'!")
    exit(1)

num_batches = (total_files + BATCH_SIZE - 1) // BATCH_SIZE

print(f"📊 Total files: {total_files}")
print(f"📦 Batch size: {BATCH_SIZE}")
print(f"📁 Will create: {num_batches} batch folders\n")

response = input("Continue? (yes/no): ").strip().lower()
if response != 'yes':
    print("❌ Cancelled")
    exit(0)

# Create batch folders and copy files
for batch_num in range(num_batches):
    batch_folder = f"qr_codes_batch{batch_num + 1}"
    os.makedirs(batch_folder, exist_ok=True)
    
    start_idx = batch_num * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, total_files)
    batch_files = qr_files[start_idx:end_idx]
    
    for filename in batch_files:
        src = os.path.join(SOURCE_FOLDER, filename)
        dst = os.path.join(batch_folder, filename)
        shutil.copy2(src, dst)
    
    print(f"✅ Created {batch_folder}/ with {len(batch_files)} files")

print(f"\n✅ Done! Created {num_batches} batch folders")
print(f"\n📝 To send each batch:")
print(f"   1. Edit whatsapp.py and change: QR_FOLDER = 'qr_codes_batch1'")
print(f"   2. Run: python3 whatsapp.py")
print(f"   3. Repeat for batch2, batch3, etc.")
print(f"\n💡 Tip: Wait 1-2 hours between batches for maximum safety!")
