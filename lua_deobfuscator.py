#!/usr/bin/env python3
"""
Lua Deobfuscator - A comprehensive tool for analyzing and deobfuscating Lua scripts
Supports various obfuscation techniques including:
- String encoding/encryption
- Variable renaming
- Control flow obfuscation
- Bytecode encoding
- Function inlining
- Garbage code insertion
"""

import re
import base64
import string
import ast
import argparse
import sys
from typing import Dict, List, Set, Tuple, Optional, Any
import json

class LuaDeobfuscator:
    def __init__(self):
        self.original_code = ""
        self.deobfuscated_code = ""
        self.patterns = self._load_patterns()
        self.string_mappings = {}
        self.variable_mappings = {}
        self.function_mappings = {}
        
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        """Load common obfuscation patterns"""
        return {
            # String encoding patterns
            'string_concat': re.compile(r'string\.char\([^)]+\)', re.IGNORECASE),
            'string_format': re.compile(r'string\.format\([^)]+\)', re.IGNORECASE),
            'table_concat': re.compile(r'table\.concat\([^)]+\)', re.IGNORECASE),
            
            # Variable obfuscation patterns
            'random_vars': re.compile(r'\b[a-zA-Z][a-zA-Z0-9_]{10,}\b'),
            'hex_vars': re.compile(r'\b[a-fA-F0-9]{8,}\b'),
            
            # Function obfuscation patterns
            'loadstring': re.compile(r'loadstring\([^)]+\)', re.IGNORECASE),
            'load': re.compile(r'\bload\([^)]+\)', re.IGNORECASE),
            
            # Bytecode patterns
            'bytecode_dump': re.compile(r'string\.dump\([^)]+\)', re.IGNORECASE),
            
            # Control flow patterns
            'goto_labels': re.compile(r'::[a-zA-Z_][a-zA-Z0-9_]*::', re.IGNORECASE),
            'goto_jumps': re.compile(r'goto\s+[a-zA-Z_][a-zA-Z0-9_]*', re.IGNORECASE),
            
            # Encoded strings
            'base64_like': re.compile(r'[A-Za-z0-9+/]{20,}={0,2}'),
            'hex_encoded': re.compile(r'\\x[0-9a-fA-F]{2}'),
            'decimal_encoded': re.compile(r'\\[0-9]{1,3}'),
        }
    
    def load_file(self, filename: str) -> bool:
        """Load obfuscated Lua file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                self.original_code = f.read()
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def analyze_obfuscation(self) -> Dict[str, Any]:
        """Analyze the type and level of obfuscation"""
        analysis = {
            'obfuscation_detected': False,
            'techniques': [],
            'complexity': 'low',
            'confidence': 0.0
        }
        
        code = self.original_code
        techniques_found = []
        
        # Check for string obfuscation
        if self.patterns['string_concat'].search(code):
            techniques_found.append('string_concatenation')
        if self.patterns['string_format'].search(code):
            techniques_found.append('string_formatting')
        if self.patterns['table_concat'].search(code):
            techniques_found.append('table_concatenation')
            
        # Check for variable obfuscation
        random_vars = len(self.patterns['random_vars'].findall(code))
        if random_vars > 10:
            techniques_found.append('variable_renaming')
            
        # Check for loadstring/eval obfuscation
        if self.patterns['loadstring'].search(code):
            techniques_found.append('dynamic_code_execution')
            
        # Check for bytecode obfuscation
        if self.patterns['bytecode_dump'].search(code):
            techniques_found.append('bytecode_encoding')
            
        # Check for control flow obfuscation
        if self.patterns['goto_labels'].search(code) or self.patterns['goto_jumps'].search(code):
            techniques_found.append('control_flow_obfuscation')
            
        # Check for encoded strings
        if self.patterns['base64_like'].search(code):
            techniques_found.append('base64_encoding')
        if self.patterns['hex_encoded'].search(code):
            techniques_found.append('hex_encoding')
        if self.patterns['decimal_encoded'].search(code):
            techniques_found.append('decimal_encoding')
            
        # Determine complexity
        complexity_score = len(techniques_found)
        if complexity_score == 0:
            analysis['complexity'] = 'none'
        elif complexity_score <= 2:
            analysis['complexity'] = 'low'
        elif complexity_score <= 5:
            analysis['complexity'] = 'medium'
        else:
            analysis['complexity'] = 'high'
            
        analysis['obfuscation_detected'] = complexity_score > 0
        analysis['techniques'] = techniques_found
        analysis['confidence'] = min(1.0, complexity_score / 10.0)
        
        return analysis
    
    def extract_strings(self) -> List[str]:
        """Extract potentially obfuscated strings"""
        strings = []
        
        # Find string.char patterns
        char_matches = self.patterns['string_concat'].findall(self.original_code)
        for match in char_matches:
            try:
                # Extract numbers from string.char(num1, num2, ...)
                numbers = re.findall(r'\d+', match)
                if numbers:
                    decoded = ''.join(chr(int(num)) for num in numbers if 0 <= int(num) <= 255)
                    strings.append(decoded)
            except:
                pass
                
        # Find base64-like strings
        b64_matches = self.patterns['base64_like'].findall(self.original_code)
        for match in b64_matches:
            try:
                decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
                if decoded.isprintable():
                    strings.append(decoded)
            except:
                pass
                
        return strings
    
    def deobfuscate_strings(self) -> str:
        """Deobfuscate string encodings"""
        code = self.original_code
        
        # Deobfuscate string.char() calls
        def replace_string_char(match):
            try:
                numbers = re.findall(r'\d+', match.group(0))
                if numbers:
                    decoded = ''.join(chr(int(num)) for num in numbers if 0 <= int(num) <= 255)
                    return f'"{decoded}"'
            except:
                pass
            return match.group(0)
            
        code = self.patterns['string_concat'].sub(replace_string_char, code)
        
        # Deobfuscate hex encoded strings
        def replace_hex_strings(match):
            try:
                hex_str = match.group(0)
                decoded = bytes.fromhex(hex_str.replace('\\x', '')).decode('utf-8', errors='ignore')
                return f'"{decoded}"'
            except:
                return match.group(0)
                
        code = self.patterns['hex_encoded'].sub(replace_hex_strings, code)
        
        return code
    
    def analyze_control_flow(self) -> Dict[str, List[str]]:
        """Analyze control flow obfuscation"""
        analysis = {
            'labels': [],
            'jumps': [],
            'suspicious_patterns': []
        }
        
        # Find goto labels
        labels = self.patterns['goto_labels'].findall(self.original_code)
        analysis['labels'] = [label.strip('::') for label in labels]
        
        # Find goto jumps
        jumps = self.patterns['goto_jumps'].findall(self.original_code)
        analysis['jumps'] = [jump.replace('goto ', '').strip() for jump in jumps]
        
        # Look for suspicious patterns
        if len(analysis['labels']) > 5:
            analysis['suspicious_patterns'].append('excessive_goto_usage')
        if len(analysis['jumps']) > len(analysis['labels']):
            analysis['suspicious_patterns'].append('more_jumps_than_labels')
            
        return analysis
    
    def find_vulnerabilities(self) -> List[Dict[str, str]]:
        """Find potential security vulnerabilities in the obfuscated code"""
        vulnerabilities = []
        
        # Check for eval-like functions
        if 'loadstring' in self.original_code.lower():
            vulnerabilities.append({
                'type': 'code_injection',
                'description': 'Uses loadstring() which can execute arbitrary code',
                'severity': 'high'
            })
            
        if 'load(' in self.original_code:
            vulnerabilities.append({
                'type': 'code_injection', 
                'description': 'Uses load() which can execute arbitrary code',
                'severity': 'high'
            })
            
        # Check for file operations
        if 'io.open' in self.original_code:
            vulnerabilities.append({
                'type': 'file_access',
                'description': 'May access files on the system',
                'severity': 'medium'
            })
            
        # Check for network operations
        if 'socket' in self.original_code.lower():
            vulnerabilities.append({
                'type': 'network_access',
                'description': 'May perform network operations',
                'severity': 'medium'
            })
            
        # Check for system commands
        if 'os.execute' in self.original_code:
            vulnerabilities.append({
                'type': 'command_execution',
                'description': 'May execute system commands',
                'severity': 'critical'
            })
            
        return vulnerabilities
    
    def extract_constants(self) -> Dict[str, List[str]]:
        """Extract constants and potential configuration values"""
        constants = {
            'strings': [],
            'numbers': [],
            'tables': [],
            'functions': []
        }
        
        # Extract string literals
        string_pattern = re.compile(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'')
        constants['strings'] = string_pattern.findall(self.original_code)
        
        # Extract numeric constants
        number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        constants['numbers'] = list(set(number_pattern.findall(self.original_code)))
        
        return constants
    
    def deobfuscate(self) -> str:
        """Main deobfuscation method"""
        print("Starting deobfuscation process...")
        
        # Step 1: Analyze obfuscation
        analysis = self.analyze_obfuscation()
        print(f"Obfuscation analysis: {analysis}")
        
        # Step 2: Deobfuscate strings
        code = self.deobfuscate_strings()
        print("String deobfuscation completed")
        
        # Step 3: Simplify variable names (basic approach)
        code = self._simplify_variables(code)
        print("Variable simplification completed")
        
        # Step 4: Remove junk code
        code = self._remove_junk_code(code)
        print("Junk code removal completed")
        
        # Step 5: Format code
        code = self._format_code(code)
        print("Code formatting completed")
        
        self.deobfuscated_code = code
        return code
    
    def _simplify_variables(self, code: str) -> str:
        """Simplify variable names"""
        # Find all variable-like identifiers
        var_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        variables = set(var_pattern.findall(code))
        
        # Filter out Lua keywords and built-in functions
        lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while', 'goto',
            'print', 'type', 'pairs', 'ipairs', 'next', 'tonumber', 'tostring',
            'string', 'table', 'math', 'io', 'os', 'debug', 'coroutine'
        }
        
        obfuscated_vars = [var for var in variables if len(var) > 8 and var not in lua_keywords]
        
        # Create simplified mappings
        for i, var in enumerate(sorted(obfuscated_vars)[:50]):  # Limit to first 50
            if len(var) > 10:  # Only rename very long variables
                simple_name = f"var_{i+1}"
                code = re.sub(r'\b' + re.escape(var) + r'\b', simple_name, code)
                
        return code
    
    def _remove_junk_code(self, code: str) -> str:
        """Remove obvious junk code"""
        lines = code.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('--'):
                continue
                
            # Skip obvious junk patterns
            if re.match(r'^local \w+\s*=\s*\d+$', line):  # local var = number
                continue
            if re.match(r'^if false then', line):  # if false blocks
                continue
            if re.match(r'^while false do', line):  # while false blocks
                continue
                
            clean_lines.append(line)
            
        return '\n'.join(clean_lines)
    
    def _format_code(self, code: str) -> str:
        """Basic code formatting"""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Decrease indent for end statements
            if re.match(r'^(end|else|elseif|until)', line):
                indent_level = max(0, indent_level - 1)
                
            formatted_lines.append('  ' * indent_level + line)
            
            # Increase indent for block statements
            if re.match(r'.*(then|do|else|function.*\)|repeat)$', line):
                indent_level += 1
                
        return '\n'.join(formatted_lines)
    
    def save_deobfuscated(self, filename: str) -> bool:
        """Save deobfuscated code to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.deobfuscated_code)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        analysis = self.analyze_obfuscation()
        vulnerabilities = self.find_vulnerabilities()
        control_flow = self.analyze_control_flow()
        constants = self.extract_constants()
        strings = self.extract_strings()
        
        return {
            'obfuscation_analysis': analysis,
            'vulnerabilities': vulnerabilities,
            'control_flow': control_flow,
            'extracted_constants': constants,
            'extracted_strings': strings[:50],  # Limit output
            'statistics': {
                'original_size': len(self.original_code),
                'deobfuscated_size': len(self.deobfuscated_code),
                'lines_original': len(self.original_code.split('\n')),
                'lines_deobfuscated': len(self.deobfuscated_code.split('\n')),
            }
        }

def main():
    parser = argparse.ArgumentParser(description='Lua Deobfuscator - Analyze and deobfuscate Lua scripts')
    parser.add_argument('input_file', help='Input obfuscated Lua file')
    parser.add_argument('-o', '--output', help='Output file for deobfuscated code')
    parser.add_argument('-r', '--report', help='Output file for analysis report (JSON)')
    parser.add_argument('-a', '--analyze-only', action='store_true', help='Only analyze, don\'t deobfuscate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize deobfuscator
    deobfuscator = LuaDeobfuscator()
    
    # Load file
    if not deobfuscator.load_file(args.input_file):
        print(f"Failed to load file: {args.input_file}")
        return 1
    
    print(f"Loaded file: {args.input_file}")
    print(f"File size: {len(deobfuscator.original_code)} bytes")
    
    if args.analyze_only:
        # Analysis only
        report = deobfuscator.generate_report()
        
        if args.verbose:
            print("\n=== ANALYSIS REPORT ===")
            print(json.dumps(report, indent=2))
        else:
            print(f"\nObfuscation detected: {report['obfuscation_analysis']['obfuscation_detected']}")
            print(f"Techniques found: {', '.join(report['obfuscation_analysis']['techniques'])}")
            print(f"Complexity: {report['obfuscation_analysis']['complexity']}")
            print(f"Vulnerabilities found: {len(report['vulnerabilities'])}")
    else:
        # Full deobfuscation
        deobfuscated = deobfuscator.deobfuscate()
        
        # Save output
        output_file = args.output or args.input_file.replace('.lua', '_deobfuscated.lua')
        if deobfuscator.save_deobfuscated(output_file):
            print(f"Deobfuscated code saved to: {output_file}")
        
        # Generate and save report
        report = deobfuscator.generate_report()
        report_file = args.report or args.input_file.replace('.lua', '_analysis.json')
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Analysis report saved to: {report_file}")
        except Exception as e:
            print(f"Failed to save report: {e}")
        
        if args.verbose:
            print(f"\nOriginal size: {report['statistics']['original_size']} bytes")
            print(f"Deobfuscated size: {report['statistics']['deobfuscated_size']} bytes")
            print(f"Reduction: {((report['statistics']['original_size'] - report['statistics']['deobfuscated_size']) / report['statistics']['original_size'] * 100):.1f}%")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())