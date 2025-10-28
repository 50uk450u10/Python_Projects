#!/usr/bin/env python3
"""
make_test_secret_shortpw.py

Creates secret.txt containing one Fernet-encrypted message produced with a short password
so the cracker above can be tested.

WARNING: for classroom/local testing ONLY. Do not use to store real secrets.
"""
import hashlib
import base64
from cryptography.fernet import Fernet

MSG = "This is a test message for cracker demo."
SHORT_PW = "cat"   # choose a short lowercase password (<=3) for assignment-style testing
OUT_FILE = "secret.txt"

def make_key_from_password(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def main():
    key = make_key_from_password(SHORT_PW)
    f = Fernet(key)
    encrypted = f.encrypt(MSG.encode())
    # write single entry (append format same as your script)
    with open(OUT_FILE, "wb") as fh:
        fh.write(encrypted + b"\n---END---\n")
    print(f"Wrote test secret to {OUT_FILE} using password '{SHORT_PW}' (for testing only).")

if __name__ == "__main__":
    main()
