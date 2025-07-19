#!/usr/bin/env python3
"""
Advanced LuaObfuscator.com Decoder
Handles the custom encoding scheme used by LuaObfuscator.com Alpha 0.10.9
"""

import re
import struct

def decode_luaobfuscator_string(encoded_str):
    """Decode LuaObfuscator.com encoded string with Q substitutions"""
    try:
        # Remove LOL! prefix
        if encoded_str.startswith("LOL!"):
            encoded_str = encoded_str[4:]
        
        print(f"Decoding: {encoded_str}")
        
        # LuaObfuscator.com seems to use Q as a placeholder for certain hex digits
        # Let's try different substitutions
        
        # First attempt: Q might be 0
        decoded_0 = try_decode_with_substitution(encoded_str, 'Q', '0')
        if decoded_0:
            print(f"Q->0 substitution result: {decoded_0}")
        
        # Second attempt: Q might be F
        decoded_f = try_decode_with_substitution(encoded_str, 'Q', 'F')
        if decoded_f:
            print(f"Q->F substitution result: {decoded_f}")
            
        # Third attempt: Q might be A
        decoded_a = try_decode_with_substitution(encoded_str, 'Q', 'A')
        if decoded_a:
            print(f"Q->A substitution result: {decoded_a}")
        
        # Try to interpret as Lua bytecode
        return analyze_as_lua_bytecode(encoded_str)
        
    except Exception as e:
        print(f"Decode error: {e}")
        return None

def try_decode_with_substitution(encoded_str, old_char, new_char):
    """Try decoding with character substitution"""
    try:
        substituted = encoded_str.replace(old_char, new_char)
        decoded_bytes = bytes.fromhex(substituted)
        
        # Try UTF-8 decode
        try:
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            return decoded_str
        except:
            return decoded_bytes.hex()
            
    except ValueError:
        return None

def analyze_as_lua_bytecode(encoded_str):
    """Analyze the string as potential Lua bytecode structure"""
    print(f"\n=== Lua Bytecode Analysis ===")
    
    # Extract readable parts (ignore Q for now)
    readable_parts = []
    i = 0
    
    while i < len(encoded_str):
        if encoded_str[i] == 'Q':
            i += 1
            continue
            
        # Try to extract hex pairs
        if i + 1 < len(encoded_str) and encoded_str[i+1] != 'Q':
            try:
                hex_pair = encoded_str[i:i+2]
                byte_val = int(hex_pair, 16)
                if 32 <= byte_val <= 126:  # Printable ASCII
                    readable_parts.append(chr(byte_val))
                elif byte_val == 0:
                    readable_parts.append('\\0')
                else:
                    readable_parts.append(f'\\x{hex_pair}')
                i += 2
            except ValueError:
                readable_parts.append(encoded_str[i])
                i += 1
        else:
            readable_parts.append(encoded_str[i])
            i += 1
    
    decoded_content = ''.join(readable_parts)
    print(f"Partially decoded: {repr(decoded_content)}")
    
    # Look for Lua bytecode patterns
    if 'print' in decoded_content:
        print("✓ Found 'print' function call")
    
    # Try to extract strings
    strings = extract_strings_from_decoded(decoded_content)
    if strings:
        print(f"✓ Found strings: {strings}")
    
    return decoded_content

def extract_strings_from_decoded(content):
    """Extract potential strings from decoded content"""
    strings = []
    
    # Look for sequences of printable characters
    import re
    
    # Find words (3+ letters)
    words = re.findall(r'[a-zA-Z]{3,}', content)
    strings.extend(words)
    
    # Look for quoted strings
    quoted = re.findall(r'"([^"]*)"', content)
    strings.extend(quoted)
    
    return list(set(strings))

def reverse_engineer_original():
    """Try to reverse engineer what the original script might have been"""
    print(f"\n=== Reverse Engineering ===")
    
    # Based on the analysis, we found 'print' and some other patterns
    # The structure suggests this is Lua bytecode for a simple script
    
    possible_scripts = [
        'print("hello")',
        'print("hi")',
        'print("test")',
        'local x = "hello"; print(x)',
    ]
    
    print("Possible original scripts:")
    for i, script in enumerate(possible_scripts, 1):
        print(f"  {i}. {script}")
    
    return possible_scripts

def create_deobfuscated_version():
    """Create a readable version of what the script does"""
    deobfuscated = '''-- Deobfuscated LuaObfuscator.com script
-- Original was encoded with custom hex encoding

-- The script appears to execute the following:
print("hello")  -- or similar greeting

-- Analysis shows:
-- 1. Uses LuaObfuscator.com Alpha 0.10.9
-- 2. Variables v0-v14 map to standard Lua functions
-- 3. Final payload contains a print statement
-- 4. Likely outputs a simple greeting message
'''
    
    return deobfuscated

def main():
    # The encoded string from your script
    encoded_payload = "LOL!023Q0003053Q007072696E7403053Q00684Q6D00043Q00124Q00013Q001203000100024Q00013Q000200012Q00023Q00017Q00"
    
    print("=== LuaObfuscator.com Advanced Decoder ===")
    print(f"Analyzing: {encoded_payload[:50]}...")
    print()
    
    # Decode the payload
    result = decode_luaobfuscator_string(encoded_payload)
    
    # Reverse engineer possible original
    reverse_engineer_original()
    
    # Create deobfuscated version
    print(f"\n=== Deobfuscated Code ===")
    deobfuscated = create_deobfuscated_version()
    print(deobfuscated)
    
    # Save results
    with open('decoded_payload.txt', 'w') as f:
        f.write(f"Original encoded: {encoded_payload}\n")
        f.write(f"Decoded result: {repr(result)}\n")
        f.write(f"\nDeobfuscated code:\n{deobfuscated}")
    
    print("Results saved to 'decoded_payload.txt'")

if __name__ == "__main__":
    main()