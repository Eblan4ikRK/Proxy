#!/usr/bin/env python3
"""
Code Reconstructor for Deobfuscated Lua Scripts
Analyzes extracted runtime data and reconstructs original Lua code
"""

import re
import json
import sys
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Optional

class LuaCodeReconstructor:
    def __init__(self):
        self.strings = []
        self.function_calls = []
        self.constants = []
        self.vm_operations = []
        self.patterns = []
        
        # Common Lua patterns
        self.lua_keywords = {
            'print', 'function', 'end', 'if', 'then', 'else', 'elseif',
            'while', 'for', 'do', 'repeat', 'until', 'break', 'return',
            'local', 'and', 'or', 'not', 'true', 'false', 'nil'
        }
        
        # String operation patterns
        self.string_ops = {
            'char': 'string.char',
            'byte': 'string.byte', 
            'sub': 'string.sub',
            'concat': 'table.concat'
        }
        
    def parse_runtime_output(self, output_text: str) -> None:
        """Parse the runtime hook output and extract meaningful data"""
        lines = output_text.strip().split('\n')
        
        for line in lines:
            if not line.strip() or line.startswith('🚀') or line.startswith('🔍') or line.startswith('⚠️') or line.startswith('✅'):
                continue
                
            # Parse data lines with format: depth level type data...
            parts = line.split('\t')
            if len(parts) >= 3:
                try:
                    depth = int(parts[0])
                    level = int(parts[1]) 
                    data_type = parts[2]
                    content = '\t'.join(parts[3:]) if len(parts) > 3 else ''
                    
                    entry = {
                        'depth': depth,
                        'level': level,
                        'type': data_type,
                        'content': content,
                        'raw_line': line
                    }
                    
                    if data_type in self.string_ops:
                        self.strings.append(entry)
                    elif data_type.isdigit():
                        self.constants.append(entry)
                    elif 'function:' in content:
                        self.function_calls.append(entry)
                    else:
                        # Check if it's a readable string
                        if self._is_readable_string(content):
                            self.strings.append(entry)
                        else:
                            self.vm_operations.append(entry)
                            
                except (ValueError, IndexError):
                    continue
    
    def _is_readable_string(self, text: str) -> bool:
        """Check if a string contains readable ASCII characters"""
        if not text:
            return False
            
        # Count readable characters
        readable_chars = sum(1 for c in text if c.isprintable() and ord(c) < 128)
        total_chars = len(text)
        
        if total_chars == 0:
            return False
            
        # At least 60% readable characters
        return (readable_chars / total_chars) >= 0.6
    
    def extract_potential_code(self) -> List[str]:
        """Extract potential Lua code snippets from the data"""
        candidates = []
        
        # Look for print statements
        for entry in self.strings:
            content = entry['content']
            
            # Check for direct print calls
            if 'print' in content.lower():
                candidates.append(content)
            
            # Check for string literals that might be printed
            if self._looks_like_string_literal(content):
                candidates.append(f'print("{content}")')
        
        # Look for function patterns
        for entry in self.function_calls:
            content = entry['content']
            if 'function:' in content:
                # This might be a function call or definition
                candidates.append(f"-- Function call detected: {content}")
        
        # Look for common Lua patterns in VM operations
        for entry in self.vm_operations:
            content = entry['content']
            if any(keyword in content.lower() for keyword in self.lua_keywords):
                candidates.append(content)
        
        return candidates
    
    def _looks_like_string_literal(self, text: str) -> bool:
        """Check if text looks like a string literal that would be printed"""
        if not text or len(text) < 2:
            return False
            
        # Check for common printable patterns
        if re.match(r'^[a-zA-Z0-9\s\.\,\!\?\-\+\=\(\)]+$', text):
            return True
            
        return False
    
    def analyze_string_construction(self) -> List[str]:
        """Analyze string.char and table.concat operations to reconstruct strings"""
        reconstructed = []
        
        # Group operations by depth/level to find related operations
        groups = defaultdict(list)
        for entry in self.strings:
            key = f"{entry['depth']}_{entry['level']}"
            groups[key].append(entry)
        
        for group_key, entries in groups.items():
            # Look for char operations followed by concat
            char_ops = [e for e in entries if e['type'] == 'char']
            concat_ops = [e for e in entries if e['type'] == 'concat']
            
            if char_ops and concat_ops:
                # Try to reconstruct the string
                reconstructed_str = self._reconstruct_from_char_ops(char_ops)
                if reconstructed_str:
                    reconstructed.append(f'print("{reconstructed_str}")')
        
        return reconstructed
    
    def _reconstruct_from_char_ops(self, char_entries: List[Dict]) -> Optional[str]:
        """Attempt to reconstruct a string from char operations"""
        # This is a simplified reconstruction
        # In practice, you'd need to analyze the actual character codes
        
        result_chars = []
        for entry in char_entries:
            content = entry['content']
            # Look for readable parts
            readable_parts = re.findall(r'[a-zA-Z0-9\s\.\,\!\?]+', content)
            result_chars.extend(readable_parts)
        
        if result_chars:
            return ''.join(result_chars).strip()
        return None
    
    def find_main_execution_flow(self) -> List[str]:
        """Identify the main execution flow and reconstruct it"""
        flow = []
        
        # Sort entries by depth and level to follow execution order
        all_entries = self.strings + self.function_calls + self.vm_operations
        all_entries.sort(key=lambda x: (x['depth'], x['level']))
        
        # Look for the final output patterns
        for entry in all_entries:
            content = entry['content']
            
            # Check if this looks like a final string output
            if self._is_final_output(content):
                flow.append(f'print("{content}")')
        
        return flow
    
    def _is_final_output(self, content: str) -> bool:
        """Check if content looks like final program output"""
        if not content:
            return False
            
        # Simple heuristic: short, readable strings are likely output
        if len(content) < 50 and content.isascii() and content.isprintable():
            # Exclude function references and hex values
            if not re.search(r'function:|0x[0-9A-Fa-f]+|table:', content):
                return True
        
        return False
    
    def reconstruct_code(self, output_file: str = None) -> str:
        """Main reconstruction method"""
        print("🔧 Starting code reconstruction...")
        
        # Extract different types of potential code
        direct_candidates = self.extract_potential_code()
        string_constructions = self.analyze_string_construction()
        execution_flow = self.find_main_execution_flow()
        
        # Combine and deduplicate
        all_candidates = []
        all_candidates.extend(direct_candidates)
        all_candidates.extend(string_constructions)
        all_candidates.extend(execution_flow)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_candidates = []
        for candidate in all_candidates:
            if candidate not in seen:
                seen.add(candidate)
                unique_candidates.append(candidate)
        
        # Generate the reconstruction report
        report = self._generate_reconstruction_report(unique_candidates)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"💾 Reconstruction saved to {output_file}")
        
        return report
    
    def _generate_reconstruction_report(self, candidates: List[str]) -> str:
        """Generate a detailed reconstruction report"""
        report = []
        report.append("=" * 80)
        report.append("🔬 LUA CODE RECONSTRUCTION REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("📊 ANALYSIS SUMMARY:")
        report.append(f"   • Strings extracted: {len(self.strings)}")
        report.append(f"   • Function calls: {len(self.function_calls)}")
        report.append(f"   • Constants found: {len(self.constants)}")
        report.append(f"   • VM operations: {len(self.vm_operations)}")
        report.append("")
        
        if candidates:
            report.append("🎯 RECONSTRUCTED CODE CANDIDATES:")
            report.append("-" * 40)
            for i, candidate in enumerate(candidates, 1):
                report.append(f"{i:2d}. {candidate}")
            report.append("")
            
            # Try to identify the most likely original code
            best_candidate = self._find_best_candidate(candidates)
            if best_candidate:
                report.append("🏆 MOST LIKELY ORIGINAL CODE:")
                report.append("-" * 40)
                report.append(f">>> {best_candidate}")
                report.append("")
        
        report.append("🔍 RAW DATA ANALYSIS:")
        report.append("-" * 40)
        
        if self.strings:
            report.append("String Operations:")
            for entry in self.strings[:10]:  # Show first 10
                report.append(f"  {entry['type']}: {entry['content'][:100]}")
            if len(self.strings) > 10:
                report.append(f"  ... and {len(self.strings) - 10} more")
            report.append("")
        
        if self.constants:
            report.append("Constants:")
            for entry in self.constants[:5]:
                report.append(f"  {entry['content']}")
            if len(self.constants) > 5:
                report.append(f"  ... and {len(self.constants) - 5} more")
            report.append("")
        
        report.append("=" * 80)
        return '\n'.join(report)
    
    def _find_best_candidate(self, candidates: List[str]) -> Optional[str]:
        """Find the most likely original code from candidates"""
        if not candidates:
            return None
        
        # Score candidates based on various criteria
        scored_candidates = []
        
        for candidate in candidates:
            score = 0
            
            # Prefer print statements
            if candidate.startswith('print('):
                score += 10
            
            # Prefer simple, readable content
            if len(candidate) < 50:
                score += 5
            
            # Prefer ASCII content
            if candidate.isascii():
                score += 3
            
            # Avoid function references
            if 'function:' not in candidate and 'table:' not in candidate:
                score += 5
            
            scored_candidates.append((score, candidate))
        
        # Return the highest scored candidate
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates[0][1] if scored_candidates else None


def main():
    if len(sys.argv) < 2:
        print("Usage: python code_reconstructor.py <runtime_output_file> [output_file]")
        print("Example: python code_reconstructor.py runtime_output.txt reconstructed.lua")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Read the runtime output
        with open(input_file, 'r', encoding='utf-8') as f:
            runtime_output = f.read()
        
        # Create reconstructor and analyze
        reconstructor = LuaCodeReconstructor()
        reconstructor.parse_runtime_output(runtime_output)
        
        # Perform reconstruction
        result = reconstructor.reconstruct_code(output_file)
        
        # Print result to console
        print(result)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during reconstruction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()