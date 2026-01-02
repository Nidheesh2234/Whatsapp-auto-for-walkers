# WhatsApp QR Code Bulk Sender 📱

Safely send 700+ QR codes to WhatsApp contacts using your personal account - **completely free**.

## ⚠️ Safety Features

- **Anti-spam delays**: 3-6 seconds between messages
- **Batch processing**: Pauses after every 100 messages
- **Random variations**: Prevents identical message patterns
- **Error handling**: Continues even if some messages fail
- **Failed number tracking**: Saves failed numbers for retry

## 🚀 Quick Start

### 1. Setup Your Files

Create a folder structure like this:
```
your-project/
├── whatsapp.py          (the script - already created!)
├── qr_codes/            (create this folder)
│   ├── 919876543210.png
│   ├── 919812345678.png
│   └── ...
└── contacts.xlsx        (optional - for custom messages)
```

### 2. Name Your QR Images

**Important**: Name each QR image with the mobile number (with country code):
- ✅ `919876543210.png` (India)
- ✅ `14155552671.jpg` (USA)
- ✅ `447700900123.png` (UK)

### 3. Optional: Custom Messages

Create `contacts.xlsx` with two columns:

| mobile        | message                           |
|---------------|-----------------------------------|
| 919876543210  | Hi Rohit, here's your QR code!   |
| 919812345678  | Hello! Your access code is ready |

### 4. Run the Script

```bash
python3 whatsapp.py
```

**What happens:**
1. Script shows summary of files found
2. Asks for confirmation
3. Opens WhatsApp Web (scan QR if needed)
4. Starts sending with safe delays
5. Shows progress in real-time
6. Saves failed numbers to `failed_numbers.txt`

## 📊 Expected Timeline

- **700 messages** with 3-6 second delays = ~50-70 minutes
- Includes automatic batch pauses every 100 messages
- Keep your computer awake and connected

## 🛡️ Avoiding WhatsApp Bans

✅ **Do:**
- Keep delays at 3-6 seconds minimum
- Run in batches (100-150 at a time)
- Use slightly different messages
- Keep WhatsApp Web open and stable

❌ **Don't:**
- Send identical messages to everyone
- Send more than 100-150 per hour
- Close WhatsApp Web during sending
- Use on multiple devices simultaneously

## 🔧 Troubleshooting

**"WhatsApp Web not opening"**
- Make sure Chrome/Firefox is installed
- Close other WhatsApp Web tabs first

**"Image not found"**
- Check QR images are in `qr_codes/` folder
- Verify filenames match mobile numbers exactly

**"Message failed to send"**
- Check internet connection
- Verify mobile number format (with country code)
- Failed numbers are saved to retry later

## 📝 Configuration

Edit these variables in `whatsapp.py`:

```python
QR_FOLDER = "qr_codes"      # Your QR images folder
BATCH_SIZE = 100            # Messages per batch
MIN_DELAY = 3               # Minimum seconds between sends
MAX_DELAY = 6               # Maximum seconds between sends
WAIT_TIME = 15              # Seconds for WhatsApp Web to load
```

## 🎯 Tips for Success

1. **Test first**: Try with 5-10 numbers before full run
2. **Stay connected**: Keep laptop plugged in and online
3. **Monitor progress**: Watch the console for any errors
4. **Retry failed**: Use `failed_numbers.txt` to retry later
5. **Split batches**: For 700 contacts, consider 7 batches of 100

## 📞 Need Help?

Common issues:
- Script opens browser but doesn't send → Increase `WAIT_TIME` to 20-30
- Too many failures → Check mobile number format
- WhatsApp blocks → Reduce `BATCH_SIZE` to 50 and increase delays

---

**Ready to send?** Just run `python3 whatsapp.py` and follow the prompts! 🚀
