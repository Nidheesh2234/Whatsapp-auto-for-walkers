"""
WhatsApp QR Sender - WORKING VERSION with Selenium
Reliably sends QR codes via WhatsApp Web
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random

# ===== CONFIGURATION =====
QR_FOLDER = "qr_codes"
MIN_DELAY = 4
MAX_DELAY = 7
BATCH_SIZE = 100

CAPTION_MESSAGE = """🌟 Welcome to all Walkers International, Walkers Club Visakhapatnam (Dist 101) Members! 👣💫

📱✨ A new QR-based attendance system is introduced to make our meetings paperless and technology-friendly for all members.

🧾🔍 The QR code contains your basic member information for attendance marking at every regular meeting.

💾📲 Please download or save your individual QR code in your respective folders for convenient access.

📍🖱️ Scan your QR code at the reception desk upon arrival for each club meeting to mark your attendance.

✅📊 This process ensures accurate attendance tracking and keeps event management smooth and efficient.

💻👨‍💻 The QR application was developed by Master Nidheesh from Hasini Informatics Pvt Ltd, as part of our ongoing commitment to adopting modern solutions.

🎉🚶‍♂️ We look forward to a seamless and enjoyable experience for everyone — Happy Walking! 😄👟"""

print("🚀 WhatsApp QR Code Sender\n")

# Check folder
if not os.path.exists(QR_FOLDER):
    print(f"❌ Folder '{QR_FOLDER}' not found!")
    exit(1)

qr_files = [f for f in os.listdir(QR_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
total = len(qr_files)

if total == 0:
    print(f"❌ No QR images found in '{QR_FOLDER}'!")
    exit(1)

print(f"📊 Found {total} QR images")
print(f"⏱️  Estimated time: {(total * 5.5) / 60:.1f} minutes\n")

# Setup Chrome
print("🌐 Opening WhatsApp Web...")
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={os.path.abspath('./whatsapp_session')}")  # Save login session
options.add_argument("--remote-debugging-port=9222") # Fix for DevToolsActivePort error
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")

print("\n⏳ Waiting for WhatsApp to load...")
time.sleep(5)  # Quick wait since already logged in
print("✅ Starting to send messages...")

success = 0
failed = 0
failed_list = []

print(f"\n{'='*60}")
print("🚀 STARTING TO SEND")
print(f"{'='*60}\n")

for i, filename in enumerate(qr_files, 1):
    mobile = filename.rsplit('.', 1)[0]
    
    # Sanitize number: remove underscores, spaces, hyphens
    mobile = mobile.replace('_', '').replace(' ', '').replace('-', '')
    
    # Add country code if needed
    if not mobile.startswith('91') and not mobile.startswith('+'):
        mobile = f"91{mobile}"
    
    img_path = os.path.abspath(os.path.join(QR_FOLDER, filename))
    
    try:
        # Open new chat
        driver.get(f"https://web.whatsapp.com/send?phone={mobile}")
        time.sleep(6)
        
        # Step 1: Click attach button (paperclip/plus icon)
        attach_btn = None
        try:
            # Method 1: Find by aria-label
            attach_btn = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Attach"]')
            attach_btn.click()
        except:
            try:
                # Method 2: Find by title
                attach_btn = driver.find_element(By.XPATH, '//div[@title="Attach"]')
                attach_btn.click()
            except:
                try:
                    # Method 3: Find the plus icon parent
                    attach_btn = driver.find_element(By.XPATH, '//span[@data-icon="plus-rounded"]/../..')
                    attach_btn.click()
                except:
                    # Method 4: Find by role button with Attach
                    attach_btn = driver.find_element(By.XPATH, '//div[@role="button"][@aria-label="Attach"]')
                    attach_btn.click()
        
        time.sleep(2)
        
        # Step 2: Click "Photos & videos" menu item
        try:
            # Find the Photos & videos button by its icon
            photos_btn = driver.find_element(By.XPATH, '//span[@data-icon="media-filled-refreshed"]/..')
            photos_btn.click()
            time.sleep(1)
        except:
            try:
                # Alternative: find by text
                photos_btn = driver.find_element(By.XPATH, '//span[contains(text(), "Photos & videos")]/..')
                photos_btn.click()
                time.sleep(1)
            except:
                pass
        
        # Step 3: Find the file input for photos and upload
        try:
            # Find the input that accepts images
            photo_input = driver.find_element(By.CSS_SELECTOR, 'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            photo_input.send_keys(img_path)
        except:
            # Fallback: use any file input
            file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_input.send_keys(img_path)
        
        time.sleep(4)
        
        # Step 4: Add caption message
        try:
            print("   📝 Adding caption...")
            time.sleep(2) # Wait for image preview to load fully
            
            caption_box = None
            try:
                # Try finding the caption box
                caption_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Add a caption"]'))
                )
            except:
                # Fallback to active element as image upload usually focuses it
                caption_box = driver.switch_to.active_element
            
            if caption_box:
                # Click using JS to avoid interception
                try:
                    driver.execute_script("arguments[0].click();", caption_box)
                except:
                    pass
                
                time.sleep(0.5)
                
                # Send multi-line message
                # Copy paste method is often more reliable for large text, but we'll stick to send_keys for now
                # with a small delay between chunks if needed for stability
                
                time.sleep(0.5)
                
                # Send multi-line message using JS to support Emojis
                try:
                    for line in CAPTION_MESSAGE.split('\n'):
                        if line.strip():
                            # Use execCommand which handles emojis and contenteditable correctly
                            driver.execute_script("""
                                var elm = arguments[0], txt = arguments[1];
                                elm.focus();
                                document.execCommand('insertText', false, txt);
                            """, caption_box, line)
                        
                        # Use Selenium for reliable layout (Shift+Enter)
                        caption_box.send_keys(Keys.SHIFT, Keys.ENTER)
                        time.sleep(0.1)
                        
                except Exception as e:
                    print(f"   ⚠️ JS Text Error: {e}")
                    # Fallback
                    caption_box.send_keys(CAPTION_MESSAGE)
                
                time.sleep(1)
            else:
                print("   ⚠️ Could not find caption box!")
        except Exception as e:
            print(f"   ⚠️ Caption error: {str(e)}")
            
        # Step 5: Send the image

        # Press Enter key to send
        try:
            driver.switch_to.active_element.send_keys(Keys.ENTER)
        except:
             # Fallback click the send button if Enter fails
            try:
                send_btn = driver.find_element(By.XPATH, '//span[@data-icon="send"]/..')
                send_btn.click()
            except:
                pass
                
        time.sleep(2)
        
        success += 1
        print(f"✅ [{i}/{total}] Sent to +{mobile}")
        
        # Batch pause
        if i % BATCH_SIZE == 0 and i < total:
            pause = random.randint(60, 90)
            print(f"\n⏸️  Batch {i//BATCH_SIZE} done. Pausing {pause}s...\n")
            time.sleep(pause)
        else:
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            
    except Exception as e:
        failed += 1
        failed_list.append(mobile)
        print(f"❌ [{i}/{total}] Failed: +{mobile}")
        print(f"   Error: {str(e)}")
        time.sleep(3)

# Summary
print(f"\n{'='*60}")
print(f"✅ COMPLETED")
print(f"{'='*60}")
print(f"✅ Success: {success}/{total}")
print(f"❌ Failed: {failed}/{total}")

if failed_list:
    with open("failed_numbers.txt", "w") as f:
        f.write("\n".join(failed_list))
    print(f"\n💾 Failed numbers saved to 'failed_numbers.txt'")

print("\n🎉 Done! Closing browser in 5 seconds...")
time.sleep(5)
driver.quit()
