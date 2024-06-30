import base64, zlib, random, argparse

strLow = "abcdefghijklmnopqrstuvwxyz"
strCap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
shift = random.randint(1, 20)
        
def enc(inp):
    """
    Encrypts the provided input string using multiple layers of compression and encoding.
    
    Args:
        inp (str): The input string to be encrypted.
    
    Returns:
        str: The encrypted script that can be executed to decrypt the original input.
    """
    
    baseEnc = base64.b64encode(zlib.compress((inp).encode()))[::-1]
    multiEncrypted = base64.b64encode(zlib.compress(f"""____=lambda __:__import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));_____=lambda __:__import__('zlib').decompress(__import__('base64').b85decode(__[::-1]));______=lambda __:__import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));exec((_)({multiEnc(baseEnc, a=0)}))""".encode()))[::-1]
    script=f"""_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({multiEncrypted}))"""

    return script

def b16e(inp, a):
        return base64.b16encode(zlib.compress(f"""exec(({'_'*a})({inp}))""".encode()))[::-1]

def b85e(inp, a):
    return base64.b85encode(zlib.compress(f"""exec(({'_'*a})({inp}))""".encode()))[::-1]

def b32e(inp, a):
    return base64.b32encode(zlib.compress(f"""exec(({'_'*a})({inp}))""".encode()))[::-1]

def b64e(inp, a):
    return base64.b64encode(zlib.compress(f"""exec(({'_'*a})({inp}))""".encode()))[::-1]

def multiEnc(i, a=0, p=1):
    """
    Recursively applies multiple layers of compression and encoding to the provided input.
    
    Args:
        i (str): The input string to be encrypted.
        a (int): The current recursion depth. Defaults to 0.
        p (int): The current encoding type. Defaults to 1.
    
    Returns:
        str: The encrypted input string.
    """
    if a == 9:
        #print(f"{str(a)} - b64")
        return b64e(i, p)
    
    r = random.randint(1,4)
    if r == 1:
        #print(f"{str(a)} - b16")
        return multiEnc(b16e(i, p), a=a+1, p=4)
    elif r == 2:
        #print(f"{str(a)} - b85")
        return multiEnc(b85e(i, p), a=a+1, p=5)
    elif r == 3:
        #print(f"{str(a)} - b32")
        return multiEnc(b32e(i, p), a=a+1, p=6)
    
    #print(f"{str(a)} - b64")
    return multiEnc(b64e(i, p), a=a+1,p=1)

def shiftScript(inp):
    """
    Shifts the characters in the provided input string by the specified shift value.
    
    Args:
        inp (str): The input string to be shifted.
    
    Returns:
        str: The shifted output string.
    """
    data = []
    for i in inp: 
        if i.strip() and i in strLow: 
            data.append(strLow[(strLow.index(i) + shift) % 26])
        elif i.strip() and i in strCap: 
            data.append(strCap[(strCap.index(i) + shift) % 26])
        else:
            data.append(i) 
    output = "".join(data)
    return output+'"""))'

decryptScript = f"""
def decrypt(inp):
    strLow = "abcdefghijklmnopqrstuvwxyz"
    strCap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    data = []
    for i in inp: 
        if i.strip() and i in strLow: 
            data.append(strLow[(strLow.index(i) - {shift}) % 26])
        elif i.strip() and i in strCap: 
            data.append(strCap[(strCap.index(i) - {shift}) % 26])
        else:
            data.append(i) 
    output = "".join(data)
    return output

exec(decrypt("""+'"""'

def main(fpath):
    """
    Encrypts the content of the specified file and saves the encrypted content to a new file.
    
    Args:
        fpath (str): The path to the file to be encrypted.
    
    Returns:
        None
    """
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read().replace('"', '\\"').replace("'", "\\'")
        
    with open(fpath.replace(".py", "")+"-encrypted.py", "w", encoding="utf-8") as f:
        f.write(enc(decryptScript+shiftScript(content)))
        
    print("File saved to: " + fpath.replace(".py", "")+"-encrypted.py")

if __name__ == "__main__":
    """
    Parses command line arguments for the file encryption script.
    
    Args:
        file_path (str): The path to the file to be encrypted.
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Encrypt & obfuscate a file's content")
    parser.add_argument("file_path", type=str, help="Path to the file to be encrypted")
    
    args = parser.parse_args()
    main(args.file_path)