# 🔐 Android PIN Brute-Force Script (ADB + Logcat)

This script performs automated PIN brute-forcing on Android devices (tested and optimized for **Samsung Galaxy XCover Pro**, and works on most Samsung devices).
It uses **ADB**, **logcat**, and **Android input events** to:

* Wake & unlock the screen (swipe-up)
* Enter PIN digits automatically
* Detect lockout countdown from system logs
* Wait exactly until lockout ends
* Continue trying next PIN
* Detect success when the device reaches the home screen

No root access required.
No HID required.
Pure ADB.

---

## 🚀 Features

### Load PIN list from `passlist.txt`

Each line = one PIN to test.

### Lockout detection via **adb logcat**

Samsung logs messages like:

```
KeyguardSecIndicationController: CountdownTimer - Try again in 5 minutes
```

The script extracts the remaining time and waits automatically.

### Automated screen unlock sequence

Uses ADB:

```
adb shell input swipe
adb shell input keyevent
```

### Detects successful unlock

Reads:

```
adb shell dumpsys window
```

If `mShowingLockscreen=true` disappears → device is unlocked.

### Samsung-optimized

Verified on:

* Galaxy XCover Pro
* Galaxy A-series
* Galaxy S / Note devices
* Tab Active series

---

## 📁 File Structure

```
main.py
passlist.txt
README.md
```

---

## 📌 Requirements

### 1. Enable Developer Mode

`Settings` → `About phone` → `Software information` → Tap **Build number** 7 times.

### 2. Enable USB Debugging

`Settings` → `Developer options` → **USB debugging**

### 3. Install ADB

Ubuntu / Debian:

```
sudo apt install adb
```

Windows:
Install **Android Platform Tools** from Google.

---

## PIN List Format (`passlist.txt`)

Each PIN on its own line:

```
0000
1111
1234
123456
987654
```

---

## Running the Script

```
python3 main.py <file>
```

When the correct PIN is found, output:

```
========================
  SUCCESS: PIN = 123456
========================
```

---

## 🧠 How It Works

1. Reads the latest logcat output
2. Detects lockout message and extracts remaining time
3. Waits automatically
4. Wakes screen
5. Swipes up
6. Enters PIN (digit by digit)
7. Presses Enter
8. Checks if lockscreen disappeared
9. If not → tries the next PIN

---

## ⚠️ Notes

* Works when the device is on the **PIN lockscreen**.
* Some Samsung devices require a slightly longer delay after entering PIN.
* Intended for **security research and device recovery** only.

---

## Disclaimer

This project is for:

* Security research
* Forensic analysis
* Recovering your own device
* Studying Android lockout behavior

**Do NOT use this tool for unauthorized access.
You are fully responsible for how you use it.**