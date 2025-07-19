#!/usr/bin/env python3
"""
Hercules Deobfuscator - Specialized tool for reversing Hercules Lua obfuscator
Targets specific techniques used by Hercules v1.6.2:
- Advanced Caesar Cipher string encoding
- Virtual machine bytecode execution
- Custom instruction sets
- Function wrapping and inlining
- Anti-tamper protection
"""

import re
import base64
import string
import argparse
import sys
from typing import Dict, List, Set, Tuple, Optional, Any
import json

class HerculesDeobfuscator:
    def __init__(self):
        self.original_code = ""
        self.deobfuscated_code = ""
        self.vm_instructions = {}
        self.string_table = []
        self.function_table = []
        self.constant_table = []
        
    def load_file(self, filename: str) -> bool:
        """Load obfuscated Lua file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                self.original_code = f.read()
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def detect_hercules(self) -> Dict[str, Any]:
        """Detect if this is Hercules obfuscated code"""
        detection = {
            'is_hercules': False,
            'version': None,
            'confidence': 0.0,
            'indicators': []
        }
        
        code = self.original_code
        indicators = []
        
        # Check for Hercules signature
        if 'Hercules' in code and 'obfuscator' in code.lower():
            indicators.append('hercules_signature')
            
        # Check for version string
        version_match = re.search(r'Hercules.*?v?(\d+\.\d+(?:\.\d+)?)', code, re.IGNORECASE)
        if version_match:
            detection['version'] = version_match.group(1)
            indicators.append('version_string')
            
        # Check for VM bytecode patterns
        if re.search(r'return.*?function.*?local.*?while.*?alpha.*?do', code, re.DOTALL):
            indicators.append('vm_structure')
            
        # Check for string encoding patterns specific to Hercules
        if re.search(r'HuDWadUZyHyr\(.*?\)', code):
            indicators.append('string_decoder_function')
            
        # Check for bytecode conversion patterns
        if 'SVkOeWirtS' in code:
            indicators.append('bytecode_loader')
            
        # Check for VM execution patterns
        if 'iLkvhyKfZlmz' in code:
            indicators.append('vm_executor')
            
        # Check for function wrapping
        if 'oOctatkvH' in code:
            indicators.append('function_wrapper')
            
        # Check for anti-tamper patterns
        if re.search(r'cuCzEJpiRD.*?afToLAMJHixs.*?fTAKBayDIjj', code):
            indicators.append('anti_tamper')
            
        # Calculate confidence
        confidence = len(indicators) / 8.0  # 8 possible indicators
        
        detection['is_hercules'] = confidence > 0.3
        detection['confidence'] = confidence
        detection['indicators'] = indicators
        
        return detection
    
    def extract_vm_bytecode(self) -> Optional[str]:
        """Extract the VM bytecode string"""
        # Look for the main bytecode string
        bytecode_pattern = re.compile(r"HuDWadUZyHyr\('([^']+)'")
        match = bytecode_pattern.search(self.original_code)
        
        if match:
            return match.group(1)
        return None
    
    def decode_custom_encoding(self, encoded_str: str, alphabet: str) -> bytes:
        """Decode Hercules custom string encoding"""
        try:
            # Split by underscore delimiter
            parts = encoded_str.split('_')
            decoded_bytes = []
            
            alphabet_len = len(alphabet)
            char_to_value = {char: i for i, char in enumerate(alphabet)}
            
            for part in parts:
                if not part:
                    continue
                    
                # Convert from custom base to decimal
                value = 0
                for char in part:
                    if char in char_to_value:
                        value = value * alphabet_len + char_to_value[char]
                
                # Convert to byte if in valid range
                if 0 <= value <= 255:
                    decoded_bytes.append(value)
            
            return bytes(decoded_bytes)
        except:
            return b''
    
    def extract_strings_from_vm(self, bytecode: str) -> List[str]:
        """Extract strings from VM bytecode"""
        strings = []
        
        # The alphabet used in the encoding (based on the pattern observed)
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
        
        # Try to decode the bytecode
        decoded_bytes = self.decode_custom_encoding(bytecode, alphabet)
        
        if decoded_bytes:
            # Look for string patterns in the decoded bytes
            try:
                decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                strings.append(decoded_str)
            except:
                pass
        
        return strings
    
    def analyze_vm_structure(self) -> Dict[str, Any]:
        """Analyze the VM structure and instructions"""
        analysis = {
            'vm_detected': False,
            'instructions': [],
            'functions': [],
            'constants': []
        }
        
        code = self.original_code
        
        # Look for VM instruction patterns
        if 'while alpha do' in code:
            analysis['vm_detected'] = True
            
        # Extract function definitions
        func_pattern = re.compile(r'function\s+(\w+)\s*\([^)]*\)')
        functions = func_pattern.findall(code)
        analysis['functions'] = functions
        
        # Extract local variable assignments (potential constants)
        const_pattern = re.compile(r'local\s+(\w+)\s*=\s*([^;\n]+)')
        constants = const_pattern.findall(code)
        analysis['constants'] = constants[:20]  # Limit output
        
        return analysis
    
    def find_vulnerabilities(self) -> List[Dict[str, str]]:
        """Find potential security vulnerabilities"""
        vulnerabilities = []
        
        # Check for code execution functions
        if 'loadstring' in self.original_code.lower():
            vulnerabilities.append({
                'type': 'dynamic_code_execution',
                'description': 'Uses loadstring() for dynamic code execution',
                'severity': 'high',
                'line_pattern': 'loadstring'
            })
            
        # Check for bytecode loading
        if 'string.dump' in self.original_code:
            vulnerabilities.append({
                'type': 'bytecode_manipulation',
                'description': 'Manipulates Lua bytecode directly',
                'severity': 'medium',
                'line_pattern': 'string.dump'
            })
            
        # Check for anti-debugging measures
        if re.search(r'debug\.|getfenv|setfenv', self.original_code):
            vulnerabilities.append({
                'type': 'anti_debugging',
                'description': 'Contains anti-debugging measures',
                'severity': 'medium',
                'line_pattern': 'debug functions'
            })
            
        # Check for environment manipulation
        if '_G' in self.original_code:
            vulnerabilities.append({
                'type': 'environment_manipulation',
                'description': 'Manipulates global environment (_G)',
                'severity': 'medium',
                'line_pattern': '_G'
            })
            
        return vulnerabilities
    
    def extract_embedded_strings(self) -> List[str]:
        """Extract embedded strings from the obfuscated code"""
        strings = []
        
        # Look for string literals
        string_pattern = re.compile(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'')
        matches = string_pattern.findall(self.original_code)
        for match in matches:
            string_content = match[0] if match[0] else match[1]
            if len(string_content) > 3:  # Filter out short strings
                strings.append(string_content)
        
        return strings
    
    def deobfuscate_hercules(self) -> str:
        """Main deobfuscation method for Hercules"""
        print("Starting Hercules deobfuscation...")
        
        # Step 1: Detect Hercules
        detection = self.detect_hercules()
        if not detection['is_hercules']:
            print("Warning: This doesn't appear to be Hercules obfuscated code")
            return self.original_code
            
        print(f"Hercules detected (confidence: {detection['confidence']:.2f})")
        if detection['version']:
            print(f"Version: {detection['version']}")
        print(f"Indicators: {', '.join(detection['indicators'])}")
        
        # Step 2: Extract VM bytecode
        bytecode = self.extract_vm_bytecode()
        if bytecode:
            print(f"Extracted VM bytecode ({len(bytecode)} characters)")
            
            # Try to decode strings from bytecode
            strings = self.extract_strings_from_vm(bytecode)
            if strings:
                print(f"Extracted {len(strings)} strings from VM")
                self.string_table = strings
        
        # Step 3: Analyze VM structure
        vm_analysis = self.analyze_vm_structure()
        print(f"VM analysis: {vm_analysis['vm_detected']}")
        
        # Step 4: Extract readable content
        code = self._extract_readable_content()
        
        # Step 5: Clean up and format
        code = self._cleanup_code(code)
        
        self.deobfuscated_code = code
        return code
    
    def _extract_readable_content(self) -> str:
        """Extract readable content from the obfuscated code"""
        content_lines = []
        
        # Add extracted strings as comments
        if self.string_table:
            content_lines.append("-- Extracted strings from VM:")
            for i, string_val in enumerate(self.string_table[:10]):  # Limit to first 10
                content_lines.append(f"-- String {i+1}: {repr(string_val)}")
            content_lines.append("")
        
        # Look for the original script structure
        lines = self.original_code.split('\n')
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and very long obfuscated lines
            if not line or len(line) > 200:
                continue
                
            # Keep readable function definitions
            if re.match(r'function\s+\w+\s*\(', line):
                content_lines.append(line)
            elif re.match(r'local\s+\w+\s*=\s*function', line):
                content_lines.append(line)
            elif line.startswith('--') and len(line) < 100:
                content_lines.append(line)
                
        # If we couldn't extract much, provide a skeleton
        if len(content_lines) < 5:
            content_lines = [
                "-- Hercules obfuscated Lua script",
                "-- Original functionality is wrapped in VM bytecode",
                "",
                "-- Detected obfuscation techniques:",
                f"-- - VM-based execution",
                f"-- - String encoding",
                f"-- - Function wrapping",
                "",
                "-- To fully deobfuscate, the VM bytecode needs to be executed",
                "-- in a controlled environment to extract the original logic."
            ]
            
        return '\n'.join(content_lines)
    
    def _cleanup_code(self, code: str) -> str:
        """Clean up and format the extracted code"""
        lines = code.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                clean_lines.append(line)
                
        return '\n'.join(clean_lines)
    
    def generate_analysis_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        detection = self.detect_hercules()
        vulnerabilities = self.find_vulnerabilities()
        vm_analysis = self.analyze_vm_structure()
        embedded_strings = self.extract_embedded_strings()
        
        return {
            'hercules_detection': detection,
            'vm_analysis': vm_analysis,
            'vulnerabilities': vulnerabilities,
            'embedded_strings': embedded_strings[:20],  # Limit output
            'extracted_strings': self.string_table,
            'statistics': {
                'original_size': len(self.original_code),
                'deobfuscated_size': len(self.deobfuscated_code),
                'obfuscation_ratio': len(self.original_code) / max(1, len(self.deobfuscated_code)),
                'lines_original': len(self.original_code.split('\n')),
                'functions_found': len(vm_analysis.get('functions', [])),
                'constants_found': len(vm_analysis.get('constants', []))
            },
            'deobfuscation_notes': [
                "This script uses Hercules obfuscator with VM-based protection",
                "The original code is compiled to custom bytecode",
                "Full deobfuscation requires VM emulation or dynamic analysis",
                "Static analysis can extract some strings and structure"
            ]
        }
    
    def save_deobfuscated(self, filename: str) -> bool:
        """Save deobfuscated code to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.deobfuscated_code)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Hercules Deobfuscator - Specialized tool for Hercules obfuscated Lua')
    parser.add_argument('input_file', help='Input Hercules obfuscated Lua file')
    parser.add_argument('-o', '--output', help='Output file for deobfuscated code')
    parser.add_argument('-r', '--report', help='Output file for analysis report (JSON)')
    parser.add_argument('-a', '--analyze-only', action='store_true', help='Only analyze, don\'t deobfuscate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize deobfuscator
    deobfuscator = HerculesDeobfuscator()
    
    # Load file
    if not deobfuscator.load_file(args.input_file):
        print(f"Failed to load file: {args.input_file}")
        return 1
    
    print(f"Loaded file: {args.input_file}")
    print(f"File size: {len(deobfuscator.original_code)} bytes")
    
    if args.analyze_only:
        # Analysis only
        report = deobfuscator.generate_analysis_report()
        
        if args.verbose:
            print("\n=== HERCULES ANALYSIS REPORT ===")
            print(json.dumps(report, indent=2))
        else:
            detection = report['hercules_detection']
            print(f"\nHercules detected: {detection['is_hercules']}")
            print(f"Confidence: {detection['confidence']:.2f}")
            if detection['version']:
                print(f"Version: {detection['version']}")
            print(f"Indicators: {', '.join(detection['indicators'])}")
            print(f"Vulnerabilities found: {len(report['vulnerabilities'])}")
            print(f"VM detected: {report['vm_analysis']['vm_detected']}")
    else:
        # Full deobfuscation
        deobfuscated = deobfuscator.deobfuscate_hercules()
        
        # Save output
        output_file = args.output or args.input_file.replace('.lua', '_deobfuscated.lua')
        if deobfuscator.save_deobfuscated(output_file):
            print(f"Deobfuscated code saved to: {output_file}")
        
        # Generate and save report
        report = deobfuscator.generate_analysis_report()
        report_file = args.report or args.input_file.replace('.lua', '_hercules_analysis.json')
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Analysis report saved to: {report_file}")
        except Exception as e:
            print(f"Failed to save report: {e}")
        
        if args.verbose:
            stats = report['statistics']
            print(f"\nOriginal size: {stats['original_size']} bytes")
            print(f"Deobfuscated size: {stats['deobfuscated_size']} bytes")
            print(f"Obfuscation ratio: {stats['obfuscation_ratio']:.1f}x")
            print(f"Functions found: {stats['functions_found']}")
            print(f"Constants found: {stats['constants_found']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())