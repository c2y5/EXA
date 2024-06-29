import base64, zlib, string, random, argparse

strLow = "abcdefghijklmnopqrstuvwxyz"
strCap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
shift = random.randint(1, 20)

def generateJunkCode():
    jcode = ""
    for x in range(1, 100):
        jcode += ("".join(random.choices(string.ascii_letters, k=32))+f"={random.randint(1,100000)};")
    
    return jcode
        
def enc(inp):
    baseEnc = base64.b64encode(zlib.compress((inp).encode()))[::-1]
    multiEncrypted = base64.b64encode(zlib.compress(f"""exec((_)({multiEnc(baseEnc, a=0)}))""".encode()))[::-1]
    script=f"""_=lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));____=lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));exec((_)({multiEncrypted}))"""
        
    return script

def b16e(inp):
    return base64.b16encode(zlib.compress(f"""exec((____)({inp}))""".encode()))[::-1]

def multiEnc(i, a=0):
    if a == 100:
        return b16e(i)
        #return base64.b64encode(zlib.compress(f"""exec((_)({i}))""".encode()))[::-1]
    
    return multiEnc(base64.b64encode(zlib.compress(f"""exec((_)({i}))""".encode()))[::-1], a=a+1)

def shiftScript(inp):
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
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read().replace('"', '\\"').replace("'", "\\'")
        
    with open(fpath.replace(".py", "")+"-encrypted.py", "w", encoding="utf-8") as f:
        f.write(enc(decryptScript+shiftScript(content)))
        
    print("File saved to: " + fpath.replace(".py", "")+"-encrypted.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt & obfuscate a file's content")
    parser.add_argument("file_path", type=str, help="Path to the file to be encrypted")
    
    args = parser.parse_args()
    main(args.file_path)