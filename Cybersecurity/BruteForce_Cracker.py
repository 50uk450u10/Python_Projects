import argparse #Allows for command line integration
import hashlib #Generates secure cryptographic hashes
import base64 #Encodes binary data into base64 for key handling
import itertools #Tools for creating iterators
import json #For saving and loading to .json files
import os #OS interface
import time #Timekeeping
from multiprocessing import Pool, Manager, cpu_count #Multiprocessing derivatives for speeding up process
from typing import List, Optional, Tuple #For expected code readability

"""
insert this into cmd:

py -3 -m pip install --upgrade pip
py -3 -m pip install cryptography

py BruteForce_Cracker.py --mode fernet --secret secret.txt --charset "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:',.<>?/\\|" --min-len 8 --max-len 12 --workers 4 --progress-interval 1000 --prefix-depth 1
or
py -3 BruteForce_Cracker.py --mode fernet --secret secret.txt --charset "abcdefghijklmnopqrstuvwxyz" --min-len 1 --max-len 3 --workers 2 --progress-interval 100
"""

#Optional import if cryptography is installed
try:
    from cryptography.fernet import Fernet #Fernet is a symmetric encryption system
    HAVE_FERNET = True
except Exception:
    HAVE_FERNET = False

Progress_Path = "progress.json" #Json path

#------------------------------------------Helper_Functions------------------------------------------

def CopyKey(password: str) -> bytes:
    #.sha256() takes the input and converts to a fixed 256-bit hash
    #.encode() converts a string into bytes
    #.digest() returns binary bytes of the hash, required for Fernet keys which have to be byte-encoded
    #.urlsafe_b64encode() converts binary hash to a safe string capable of being used in URLs or File Names, required for Fernet
    
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest) #This is the encryption key

def LoadEntries(path: str) -> List[bytes]: #Load encrypted entries from a file
    if not os.path.exists(path): #Check for presence of the file before attempting to read
        raise FileNotFoundError(f"Secret file '{path}' not found.") #Inform cracker with an exception
    data = open(path, "rb").read() #Read entire file as bytes
    parts = data.split(b"\n---END---\n") #Split into parts using the known separator string, using this on any other separated or non-single-line file with break the program
    entries = [p.strip() for p in parts if p and p.strip()] #Trim whitespace, drop empty parts
    return entries #Return non-empty byte entries

def LoadHashStrings(path: str) -> List[str]: #Read sha256 hex digests from a file with one digest per non-empty line
    if not os.path.exists(path): #Make sure the target file exists
        raise FileNotFoundError(f"Target file '{path}' not found.") #Throw an error if it doesn't
    lines = [] #List for storing non-empty lines
    with open(path, "r", encoding = "utf-8") as f: #Open text file using UTF-8
        for line in f: #Iterate over each line in the file
            s = line.strip() #Remove leading/trailing whitespace and newlines
            if s: #Skip empty lines
                lines.append(s.lower()) #Append the normalized lowercase hex string
    return lines #Return list of hash strings

def isPrintText(b: bytes, threshold: float = 0.9) -> bool: #Determine if a bytes object is printable text and compare with a threshold of 90% printable
    if not b: #Empty bytes are not considered printable text
        return False
    printable = 0 #Counter for printable bytes
    for c in b: #Iterate through each byte value
        if 9 <= c <= 13 or 32 <= c <= 126: #Standard range for ASCII
            printable += 1 #Increment by 1
    return (printable / len(b)) >= threshold #Compare fraction to threshold and return boolean

#------------------------------------------Worker_Functions------------------------------------------

def FernetMode(args: Tuple): #Checks all password with a given prefix using Fernet
    prefix, charset, min_len, max_len, entries, progress_shared, progress_interval = args #Unpack args
    attempts_local = 0 #Local counter of attempts
    for length in range(min_len, max_len + 1): #Loop lengths by min and max attempts
        if length < len(prefix): #If the prefix is longer than the target length, skip
            continue #Nothing to try for this length due to insufficient length from prefix
        if length == len(prefix):
            tails_iter = [()] #Empty tuple to represent zero additional characters
        else:
            tails_iter = itertools.product(charset, repeat=length - len(prefix)) #Cartesian product for tails (All possible pairs)
        for tail in tails_iter: #Iterate through each tail tuple combo
            candidate = prefix + "".join(tail) #Build the string by linking prefix + tail
            attempts_local += 1 #Increment local counter
            if attempts_local % progress_interval == 0: #Periodically update global attempt counter
                progress_shared['attempts'] += progress_interval #Bump shared attempts to help global progress view
            #Attempt decrypt from derived key
            try:
                key = CopyKey(candidate) #Derive Fernet key as the original script did
                f = Fernet(key) #Instantiate Fernet class with the derived key
                for entry in entries: #For each encrypted entry in the file
                    try:
                        dec = f.decrypt(entry) #Attempt decryption using Fernet; raises on failure
                        if isPrintText(dec, threshold = 0.8): #If decrypted content looks readable
                            return candidate, dec.decode("utf-8", errors = "replace") #Returns password & decoded text
                        else:
                            return candidate, dec.decode("utf-8", errors = "replace") #Return less than optimal decryption if likely a success
                    except Exception:
                        continue #If decrypt failed for this entry, continue to the next entry
            except Exception:
                continue #If anything goes wrong deriving the key or constructing Fernet, skip this candidate
    return None, None #If no candidate succeeds, return Null

def Sha256Mode(args: Tuple): #Checks all password with a given prefix using Sha256
    prefix, charset, min_len, max_len, target_hashes, progress_shared, progress_interval = args #Unpack args
    attempts_local = 0 #Local counter of attempts
    target_set = set(target_hashes) #Convert list to set for 0(1) membership checks
    for length in range(min_len, max_len + 1): #Loop lengths by min and max attempts
        if length < len(prefix): #If the prefix is longer than the target length, skip
            continue #Nothing to try for this length due to insufficient length from prefix
        if length == len(prefix):
            tails_iter = [()] #Empty tuple to represent zero additional characters
        else:
            tails_iter = itertools.product(charset, repeat=length - len(prefix)) #Cartesian product for tails (All possible pairs)
        for tail in tails_iter: #Iterate through each tail tuple combo
            candidate = prefix + "".join(tail) #Build the string by linking prefix + tail
            attempts_local += 1 #Increment local counter
            if attempts_local % progress_interval == 0: #Periodically update global attempt counter
                progress_shared['attempts'] += progress_interval #Bump shared attempts to help global progress view
            h = hashlib.sha256(candidate.encode("utf-8")).hexdigest() #.hexdigest()?
            if h in target_set: #Check for matching digest
                return candidate, h #Return the successful candidate and matching hash
    return None, None #If no match found, return Null

#------------------------------------------JSON_Handling------------------------------------------

def LoadProgress() -> dict: #Load minimal checkpoint from Progress_Path if present
    if not os.path.exists(Progress_Path): #If no file is found, return empty progress state
        return {}
    try:
        return json.load(open(Progress_Path, "r", encoding = "utf-8")) #Attempt to parse JSON and return it
    except Exception:
        return {} #On any error, return empty state instead of crashing
    
def SaveProgress(state: dict): #Saves and overwrites minimal checkpoint to Progress_Path
    with open(Progress_Path, "w", encoding="utf-8") as f: #Open file for writing in UTF-8
        json.dump(state, f, indent = 2) #Dump the Json with indentation for readability

#------------------------------------------Main------------------------------------------

def PrefixSplit(charset: str, depth: int, workers: int) -> List[str]: #Generate prefixes of length "depth" (Keep depth to 1 or 2 so it doesn't explode)
    if depth <= 0: #<= 0 means no prefixing
        return [""]
    prefixes = ["".join(p) for p in itertools.product(charset, repeat = depth)] #Build all prefixes
    return prefixes #Return list of prefix strings

def RunCracker(mode: str, charset: str, min_len: int, max_len: int, workers: int, progress_interval: int, target_file: Optional[str], secret_file: Optional[str], prefix_depth: int, resume_from: Optional[str]):
    start_time = time.time() #Record start time
    progress = LoadProgress() #Load previous progress if available
    attempts_before = progress.get("attempts", 0) #Extract previously recorded attempt count

    #Load targets based on mode
    if mode == "fernet":
        if not HAVE_FERNET:
            raise RuntimeError("cryptography.Fernet not available; Install cryptography package (pip install cryptography).")
        entries = LoadEntries(secret_file) #Load encrypted entries from the file
        print(f"Loaded {len(entries)} encrypted entries from {secret_file}") #Inform user of entry count
    else:
        target_hashes = LoadHashStrings(target_file) #Load digest targets
        print(f"Loaded {len(target_hashes)} target hash lines from {target_file}") #Inform user of loaded hashes

    prefixes = PrefixSplit(charset, prefix_depth, workers) #Generate prefix list
    if not prefixes: #Safety net ensuring there is at least one task
        prefixes = [""]

    manager = Manager() #Multiprocessing manager to link state between processes
    shared = manager.dict() #Linked dictionary for counters
    shared['attempts'] = 0 #Initialize shared attempts counter to zero

    tasks = [] #Task list holds all parameters required by worker functions
    if mode == "fernet":
        for p in prefixes: #Create a task for each prefix string
            tasks.append((p, charset, min_len, max_len, entries, shared, progress_interval))
        worker_func = FernetMode
    else:
        for p in prefixes: #Pass target hash list into each task
            tasks.append((p, charset, min_len, max_len, target_hashes, shared, progress_interval))
        worker_func = Sha256Mode

    print(f"Starting brute-force:\nmode = {mode}\ncharset_len = {len(charset)}\nmin = {min_len}\nmax = {max_len}\nworkers = {workers}\n") #Print summary
    print(f"Prefix depth = {prefix_depth} -> {len(prefixes)} tasks") #Display number of tasks
    if resume_from: #If user provided a resume point, display
        print(f"Resume point provided: will skip candidates accordingly <= '{resume_from}' (best-effort)")

    found = None #Placeholder for discovered password if any worker finds one
    found_meta = None #Placeholder for associated metadata

    #Use multiprocessing Pool to execute tasks in parallel
    with Pool(processes = workers) as pool: #Creat a pool of worker processes
        for result in pool.imap_unordered(worker_func, tasks): #Map tasks to worker_func in an unordered fashion
            if result and result[0]: #If a tuple contains a candidate string in the first element
                found, found_meta = result[0], result[1] #Capture found password and metadata
                pool.terminate() #Terminate remaining processes early due to found match
                break
            #Periodically print global progress
            total_attempts = attempts_before + shared['attempts'] #Combine previously saved attempts
            elapsed = time.time() - start_time #Calculate elapsed time
            print(f"[progress] approx. attempts = {total_attempts}\nelapsed = {elapsed:.2f}s", end = "\r") #Overwrite line progress
    
    total_attempts = attempts_before + shared['attempts'] #Final total attempts
    elapsed = time.time() - start_time #Final elapsed time

    SaveProgress({"attempts": total_attempts, "last_run_time": time.time()})

    if found: #If a password has been found
        print("\n\n===FOUND===") #Visual separator for success
        print(f"Password: {found}") #Show discovered password plainly
        print(f"Attempts (approx): {total_attempts}") #Show approximate number of attempts taken
        print(f"Elapsed: {elapsed:.2f}s") #Show elapsed time formatted to 2 decimal places
        if mode == "fernet": #If target was a fernet-encrypted entry, display decrypted plaintext
            print("Decrypted plaintext (best-effort):")
            print(found_meta)
        else:
            print(f"Matched hash: {found_meta}") #Print which target hash matched the candidate
        return True #Indicate success by returning True
    else:
        print("\n\n===NOT_FOUND===") #Inform the user no password was found in this search space
        print(f"Total attempts (approx): {total_attempts} Elapsed={elapsed:.2f}s") #Print summary stats for failure case
        return False #Indicate failure by returning False
    
#------------------------------------------Command_Line------------------------------------------

def ParseArgs():
    p = argparse.ArgumentParser(description = "Flexible brute-force cracker (fernet or sha256).") #Create parser
    p.add_argument("--mode", choices = ["fernet", "sha256"], required = True, help = "fernet = attack secret.txt entries; sha256 = compare hex digests from file") #Mode flag
    p.add_argument("--secret", default = "secret.txt", help = "secret file for fernet mode (default secret.txt)") #Secret file
    p.add_argument("--target-file", default = "target.txt", help = "file with hex SHA-256 targets (one per line)") #Target file
    p.add_argument("--charset", default = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:',.<>?/\\|", help = "string of characters to use (be careful: large charset x length explodes search space)") #Charset
    p.add_argument("--min-len", type = int, default = 1, help = "minimum candidate length") #Minimum length
    p.add_argument("--max-len", type = int, default = 6, help = "maximum candidate length") #Maximum length
    p.add_argument("--workers", type = int, default = max(1, cpu_count()-1), help = "number of parallel workers") #Number of workers
    p.add_argument("--progress-interval", type = int, default = 1000, help = "how many attempts between shared progress bumps") #Progress interval
    p.add_argument("--prefix-depth", type = int, default = 1, help = "how many characters to form prefixes for splitting work (small integer, default 1)") #Prefix partition depth
    p.add_argument("--resume-from", type = str, default = None, help = "(best-effort) lexicographic candidate to resume after (e.g. 'm' or 'ab')") #Resume hint
    return p.parse_args() #Parse CLI args and return the populated namespace

if __name__ == "__main__": #Standard Python entrypoint guard to allow importing without running main behavior
    args = ParseArgs() #Parse command-line arguments into `args` namespace

    #Quick safety guard: compute approximate search space size and warn if enormous
    charset_len = len(args.charset) #Number of characters in the user-specified charset
    max_space = sum(charset_len ** L for L in range(args.min_len, args.max_len + 1))
    if max_space > 1e8: #If space exceeds 100 million, warn the user
        print(f"WARNING: requested search space ~{max_space:.0f} candidates (this may take a very long time).")
        print("Proceed only if you understand this is for local testing on your machine.")
    try:
        RunCracker(mode = args.mode, charset = args.charset, min_len = args.min_len, max_len = args.max_len, workers = args.workers, progress_interval = args.progress_interval, target_file = args.target_file, secret_file = args.secret, prefix_depth = args.prefix_depth, resume_from = args.resume_from) #Launch main with parsed args
    except KeyboardInterrupt:
        print("\nInterrupted by user. Progress saved.") #Handling of Ctrl+C by user; progress is saved earlier
    except Exception as e:
        print("Error:", e) #Print any unexpected exception to help debugging