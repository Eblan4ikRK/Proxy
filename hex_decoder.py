#!/usr/bin/env python3
"""
Simple hex decoder for LuaObfuscator.com encoded strings
"""

def decode_luaobfuscator_hex(hex_string):
    """Decode LuaObfuscator.com hex encoded string"""
    try:
        # Remove LOL! prefix
        if hex_string.startswith("LOL!"):
            hex_string = hex_string[4:]
        
        print(f"Hex to decode: {hex_string}")
        
        # Try direct hex decode
        try:
            decoded_bytes = bytes.fromhex(hex_string)
            print(f"Raw bytes: {decoded_bytes}")
            
            # Try as UTF-8
            try:
                decoded_str = decoded_bytes.decode('utf-8')
                print(f"UTF-8 decode: {repr(decoded_str)}")
                return decoded_str
            except UnicodeDecodeError:
                print("Not valid UTF-8")
        except ValueError as e:
            print(f"Hex decode error: {e}")
        
        # Try interpreting as custom encoding
        # LuaObfuscator might use custom character mapping
        result = ""
        i = 0
        while i < len(hex_string):
            if i + 1 < len(hex_string):
                char_code = hex_string[i:i+2]
                try:
                    byte_val = int(char_code, 16)
                    if 32 <= byte_val <= 126:  # Printable ASCII
                        result += chr(byte_val)
                    else:
                        result += f"\\x{char_code}"
                except ValueError:
                    result += char_code
                i += 2
            else:
                result += hex_string[i]
                i += 1
        
        print(f"Character interpretation: {repr(result)}")
        return result
        
    except Exception as e:
        print(f"Decode error: {e}")
        return None

def analyze_hex_pattern(hex_string):
    """Analyze the hex string pattern"""
    if hex_string.startswith("LOL!"):
        hex_string = hex_string[4:]
    
    print(f"\nAnalyzing hex pattern:")
    print(f"Length: {len(hex_string)} characters")
    print(f"Hex pairs: {len(hex_string) // 2} bytes")
    
    # Show hex in groups
    print("Hex groups:")
    for i in range(0, len(hex_string), 16):
        chunk = hex_string[i:i+16]
        print(f"  {i//2:04x}: {chunk}")
    
    # Look for patterns
    print("\nPattern analysis:")
    
    # Count character frequency
    char_freq = {}
    for char in hex_string:
        char_freq[char] = char_freq.get(char, 0) + 1
    
    print("Character frequency:")
    for char, count in sorted(char_freq.items()):
        print(f"  {char}: {count}")

if __name__ == "__main__":
    # Test with the provided string
    test_string = "LOL!023Q0003053Q007072696E7403053Q00684Q6D00043Q00124Q00013Q001203000100024Q00013Q000200012Q00023Q00017Q00"
    
    print("=== LuaObfuscator.com Hex Decoder ===")
    print(f"Input: {test_string}")
    print()
    
    analyze_hex_pattern(test_string)
    print()
    
    result = decode_luaobfuscator_hex(test_string)
    
    if result:
        print(f"\nFinal result: {repr(result)}")
        
        # Try to interpret as Lua bytecode structure
        print("\n=== Potential Lua Analysis ===")
        if "print" in result.lower():
            print("Contains 'print' - likely a print statement")
        if result.count('\x00') > 5:
            print("Many null bytes - likely binary/bytecode data")
        
        # Look for string patterns
        import re
        strings = re.findall(r'[a-zA-Z]{3,}', result)
        if strings:
            print(f"Found potential strings: {strings}")