import hashlib #Generates secure cryptographic hashes
import base64 #Encodes binary data into base64 for key handling
from cryptography.fernet import Fernet #Fernet is a symmetric encryption system
import re #Regular expressions tools for pattern checks

def MakeKey(password):
    #.sha256() takes the input and converts to a fixed 256-bit hash
    #.encode() converts a string into bytes
    #.digest() returns binary bytes of the hash, required for Fernet keys which have to be byte-encoded
    hashed = hashlib.sha256(password.encode()).digest()

    #.urlsafe_b64encode() converts binary hash to a safe string capable of being used in URLs or File Names, required for Fernet
    #This is the encryption key
    return base64.urlsafe_b64encode(hashed)

def PassStrengthCheck(password):
    if len(password) < 8:
        print("Password too short. Must be at least 8 characters.\n")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter.\n")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter.\n")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one number.\n")
        return False
    if not re.search(r"[\W_]", password):
        print("Password must contain at least one special character (e.g., !@#$%).\n")
        return False
    print("Password accepted.\n")
    return True

def Encrypt(message, password=None):
    #Run strength check before encryption
    while True:
        if password is None or not PassStrengthCheck(password):
            password = input("Please enter a strong password for this message:\n")
            continue
        else:
            break
    
    key = MakeKey(password) #Make a key that Fernet can use with the password
    fernet = Fernet(key) #Fernet object performs a symmetric encryption so the same key is used for encryption and decrypting
    encrypted = fernet.encrypt(message.encode()) #Encrypt message to bytes
    with open("secret.txt", "ab") as f: #Write encryption to file, creates a file if one does not exist in the location
        f.write(encrypted + b"\n---END---\n") #Appends message with separator for multiple encryptions

def Decrypt(password):
    try: #Try/Catch for file not found
        with open("secret.txt", "rb") as f: #Read encrypted data from the file
            data = f.read()
    except FileNotFoundError:
        print("No encrypted message found.\n")
        return

    #Generate the same key from the provided password and 
    entries = data.split(b"\n---END---\n") #Divides the data pulled
    key = MakeKey(password)
    fernet = Fernet(key)

    found = False
    for entry in entries:
        if not entry.strip(): #Safeguard to remove any extra whitespace
            continue
        try: #Try/Catch for incorrect password or corrupt data
            #.decrypt() returns bytes of the message as plain text
            #.decode() converts decrypted bytes into a readable string
            decrypted = fernet.decrypt(entry).decode()
            print("\nDecrypted message: ")
            print(decrypted)
            found = True
        except:
            continue
    
    if not found:
        print("Incorrect password or file corrupted.\n")

userSelect = int(input("1. Encrypt a New Message\n2. Decrypt an Existing Message\n"))

match userSelect:
    case 1:
        message = input("Please enter the message you would like to encrypt.\n")
        Encrypt(message)
    case 2:
        password = input("Enter the password key to decrypt a stored message.\n")
        Decrypt(password)
    case _:
        print("Invalid option, enter 1 or 2.")