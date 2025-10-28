README.txt
========================================

Title: Brute Force Cracker

Files submitted:
- BruteForce_Cracker.py       # brute-force cracker (fernet / sha256 modes)
- PasswordEncryption.py       # messsage encrypter/decrypter (creates secret.txt using Fernet)
- ShortPassTest.py # small code that writes secret.txt using password "cat"
- README.txt                  # this file
- secret.txt                  # example encrypted output

Overview
--------
This repository provides a local, offline brute-force cracker and helpers for classroom testing.
Use it only on files you created or have explicit permission to test.  The cracker supports two modes:
- **fernet**: attempts to decrypt Fernet tokens in `secret.txt`
- **sha256**: compares SHA-256 hex digests from `target.txt`

Requirements
------------
- Python 3.8+ (3.13 tested)
- `cryptography` package (only required for `fernet` mode)

Install dependency (Windows example):
```
py -3 -m pip install --upgrade pip
py -3 -m pip install cryptography
```

How to run (quick)
------------------
1. Open a terminal in the project folder (example path shown).
```
cd /d "C:\Users\<yourname>\Desktop\Python_Projects"
```

2. Create a quick test secret (fast; uses password "cat"):
```
py -3 ShortPassTest.py
```

3. Run the cracker (FERNET mode, small demo):
```
py -3 BruteForce_Cracker.py --mode fernet --secret secret.txt --charset "abcdefghijklmnopqrstuvwxyz" --min-len 1 --max-len 3 --workers 2 --progress-interval 100
```

4. Run SHA-256 mode (if you have target.txt with hex digests):
```
py -3 BruteForce_Cracker.py --mode sha256 --target-file target.txt --charset "abcdefghijklmnopqrstuvwxyz" --min-len 1 --max-len 5
```

Can I run with only `--mode`?
-----------------------------
Yes — the script has sensible defaults. If you run with only the `--mode` flag, it will use default values for other parameters:
- default `secret` file: `secret.txt`
- default `target-file`: `target.txt`
- default `charset`: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:',.<>?/\\|
- default `min-len`: 1
- default `max-len`: 6
- default `workers`: cpu_count() - 1 (at least 1)
- default `progress-interval`: 1000
- default `prefix-depth`: 1

So this command will work without specifying more and will run a conservative search (may be slow if max length large):
```
py -3 BruteForce_Cracker.py --mode fernet
```
However:
- If you expect to crack a password that follows a stricter policy (e.g., requires uppercase, digits, specials, or length ≥ 8), you should set `--charset`, `--min-len`, `--max-len`, and policy flags accordingly.
- For classroom demos, use small charsets and small `--max-len` so the run finishes quickly.

Common command examples
-----------------------
Quick demo (fast):
```
py -3 BruteForce_Cracker.py --mode fernet --min-len 1 --max-len 3 --charset "abcdefghijklmnopqrstuvwxyz"
```

Policy-mode example (requires upper/lower/digit/special and min length >= required classes):
```
py -3 BruteForce_Cracker.py --mode fernet --charset "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$" --min-len 8 --max-len 10 --policy strong
```

Notes on outputs (sample)
-------------------------
- After running `ShortPassTest.py`:
```
Wrote test secret to secret.txt using password 'cat' (for testing only).
```

- Example cracker run output (small test):
```
Loaded 1 encrypted entries from secret.txt.
[progress] approx attempts=100 elapsed=0.34s
=== FOUND ===
Password: cat
Attempts (approx): 312
Elapsed: 0.42s
Decrypted plaintext:
This is a test message for cracker demo.
```

Ethics & notes
--------------
- Only attack hashes or encrypted files you created or have explicit permission to test.
- Large charsets and long max lengths produce infeasible search spaces (combinatorial explosion).
- Use `--workers 1` for easier interrupting during tests; increase workers for speed when necessary.
- The script saves an approximate `progress.json` checkpoint on exit or interrupt; for robust resume support, request per-prefix offsets or a stronger checkpoint system.

Optional improvements (ideas)
----------------------------
- Implement a combinatorial generator that constructs only policy-satisfying candidates (faster than filtering).
- Add mask/pattern support (e.g., `?u?l?d?s`) for targeted attacks.
- Precise per-prefix offset checkpointing for perfect resume behavior on very large jobs.
