import base64, zlib, re

strLow = "abcdefghijklmnopqrstuvwxyz"
strCap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decrypt_shift(inp, shift):
    data = []
    for i in inp: 
        if i.strip() and i in strLow: 
            data.append(strLow[(strLow.index(i) - shift) % 26])
        elif i.strip() and i in strCap: 
            data.append(strCap[(strCap.index(i) - shift) % 26])
        else:
            data.append(i) 
    output = "".join(data)
    return output

def reverse_enc(script):
    try:
        return zlib.decompress(base64.b64decode(script[::-1]))
    except Exception as e:
        print(f"Error in reverse_enc: {e}")
        return b""

def reverse_multiEnc(i, a=97):
    if a == 0:
        return reverse_enc(i)
    return reverse_multiEnc(reverse_enc(i), a=a-1)

def extract_shift(script):
    match = re.search(r'strCap[(strCap.index(i) - (\d+)', script)
    if match:
        print(match.group(1))
        return int(match.group(1))
    raise ValueError("Shift value not found in the script")

def decrypt(script):
    try:
        # Extract the multi-layer encrypted script
        multiEncrypted = script.split('exec((_)(', 1)[1].rsplit('))', 1)[0]
        
        # Reverse the multi-layer encryption
        baseEnc = reverse_multiEnc(multiEncrypted)
        
        # Decode the base64 and zlib compression
        decoded_script = reverse_enc(baseEnc)
        
        return decoded_script.decode()
    except Exception as e:
        print(f"Error in decrypt: {e}")
        return ""

def main(fpath):
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Reverse the initial multi-layer encryption to get the script with shift
        partial_decoded_script = reverse_enc(content.split('exec((_)(', 1)[1].rsplit('))', 1)[0])
        
        if not partial_decoded_script:
            print("Error: Could not partially decode the script.")
            return
        
        shift_script = reverse_multiEnc(partial_decoded_script, a=96).decode()
        
        # Extract the shift value
        shift = extract_shift(shift_script)
        
        # Reverse the initial shift encoding
        shifted_content = decrypt_shift(content, shift)
        
        # Extract and decrypt the original script
        decrypted_content = decrypt(shifted_content)
        
        if decrypted_content:
            with open(fpath.replace("-encrypted", "-decrypted"), "w", encoding="utf-8") as f:
                f.write(decrypted_content)
            
            print("File saved to: " + fpath.replace("-encrypted", "-decrypted"))
        else:
            print("Decryption failed.")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Decrypt & deobfuscate a file's content")
    parser.add_argument("file_path", type=str, help="Path to the file to be decrypted")
    
    args = parser.parse_args()
    main(args.file_path)
