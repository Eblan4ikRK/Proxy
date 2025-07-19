#!/usr/bin/env python3
"""
Advanced Code Reconstructor for Deobfuscated Lua Scripts
Enhanced version that better identifies final output strings
"""

import re
import sys
from typing import List, Dict, Set, Tuple, Optional

class AdvancedLuaReconstructor:
    def __init__(self):
        self.all_entries = []
        self.final_strings = []
        self.readable_strings = []
        
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
                    
                    self.all_entries.append(entry)
                    
                    # Check if this is a readable string that could be output
                    if self._is_final_output_string(data_type):
                        self.final_strings.append(entry)
                    elif self._is_readable_string(data_type):
                        self.readable_strings.append(entry)
                            
                except (ValueError, IndexError):
                    continue
    
    def _is_final_output_string(self, text: str) -> bool:
        """Check if text looks like a final output string"""
        if not text:
            return False
            
        # Look for simple readable strings without function references
        if (len(text) < 50 and 
            text.isascii() and 
            text.isprintable() and
            not re.search(r'function:|0x[0-9A-Fa-f]+|table:', text) and
            not text.isdigit()):
            return True
        
        return False
    
    def _is_readable_string(self, text: str) -> bool:
        """Check if text contains readable ASCII characters"""
        if not text or len(text) < 2:
            return False
            
        # Count readable characters
        readable_chars = sum(1 for c in text if c.isprintable() and ord(c) < 128)
        total_chars = len(text)
        
        if total_chars == 0:
            return False
            
        # At least 70% readable characters and not all digits
        return (readable_chars / total_chars) >= 0.7 and not text.isdigit()
    
    def find_key_strings(self) -> List[str]:
        """Find the most likely original strings from the runtime data"""
        candidates = []
        
        # First priority: Look for the final strings (like "hmmmm")
        print("🔍 Analyzing final strings...")
        for entry in self.final_strings:
            content = entry['type']  # The type field contains the actual string
            print(f"   Found final string: '{content}'")
            candidates.append(f'print("{content}")')
        
        # Second priority: Look for readable strings in the data
        print("🔍 Analyzing readable strings...")
        for entry in self.readable_strings:
            content = entry['type']
            if len(content) > 1 and content not in ['string', 'char', 'byte', 'sub', 'table', 'concat', 'insert']:
                print(f"   Found readable string: '{content}'")
                candidates.append(f'print("{content}")')
        
        # Third priority: Look in content field for short readable strings
        print("🔍 Scanning content fields...")
        for entry in self.all_entries:
            content_parts = entry['content'].split()
            for part in content_parts:
                if (self._is_final_output_string(part) and 
                    len(part) > 2 and 
                    part not in ['function', 'table']):
                    print(f"   Found content string: '{part}'")
                    candidates.append(f'print("{part}")')
        
        return candidates
    
    def analyze_execution_flow(self) -> List[str]:
        """Analyze the execution flow to find the final output"""
        print("🔍 Analyzing execution flow...")
        
        # Sort by depth and level to follow execution order
        sorted_entries = sorted(self.all_entries, key=lambda x: (x['depth'], x['level']))
        
        # Look for the last meaningful string operations
        final_candidates = []
        
        # Check the last few entries for final output
        for entry in sorted_entries[-10:]:  # Last 10 entries
            content = entry['type']
            if self._is_final_output_string(content):
                print(f"   Final execution string: '{content}'")
                final_candidates.append(f'print("{content}")')
        
        return final_candidates
    
    def reconstruct_code(self, output_file: str = None) -> str:
        """Main reconstruction method"""
        print("🔧 Starting advanced code reconstruction...")
        
        # Find key strings using different methods
        key_strings = self.find_key_strings()
        execution_flow = self.analyze_execution_flow()
        
        # Combine and deduplicate
        all_candidates = key_strings + execution_flow
        unique_candidates = list(dict.fromkeys(all_candidates))  # Remove duplicates while preserving order
        
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
        report.append("🔬 ADVANCED LUA CODE RECONSTRUCTION REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("📊 ANALYSIS SUMMARY:")
        report.append(f"   • Total entries parsed: {len(self.all_entries)}")
        report.append(f"   • Final output strings: {len(self.final_strings)}")
        report.append(f"   • Readable strings: {len(self.readable_strings)}")
        report.append("")
        
        if self.final_strings:
            report.append("🎯 DETECTED FINAL OUTPUT STRINGS:")
            report.append("-" * 40)
            for i, entry in enumerate(self.final_strings, 1):
                report.append(f"{i:2d}. '{entry['type']}'")
            report.append("")
        
        if candidates:
            report.append("🏆 RECONSTRUCTED LUA CODE:")
            report.append("-" * 40)
            
            # Find the best candidate (likely the original code)
            best_candidate = self._find_best_candidate(candidates)
            if best_candidate:
                report.append(f">>> {best_candidate}")
                report.append("")
                
            report.append("All candidates:")
            for i, candidate in enumerate(candidates, 1):
                marker = "★" if candidate == best_candidate else " "
                report.append(f"{marker} {i:2d}. {candidate}")
            report.append("")
        
        # Show some raw data for debugging
        report.append("🔍 RAW EXECUTION TRACE (last 10 entries):")
        report.append("-" * 40)
        for entry in self.all_entries[-10:]:
            report.append(f"  {entry['depth']}-{entry['level']}: {entry['type']} | {entry['content'][:50]}...")
        
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
            
            # Extract the string content from print("...")
            match = re.search(r'print\("([^"]+)"\)', candidate)
            if match:
                content = match.group(1)
                
                # Prefer simple, short strings
                if len(content) < 20:
                    score += 10
                
                # Prefer lowercase alphabetic strings
                if content.islower() and content.isalpha():
                    score += 15
                
                # Prefer strings that look like words
                if re.match(r'^[a-z]+$', content):
                    score += 20
                
                # Special bonus for "hmmmm" pattern
                if re.match(r'^h+m+$', content):
                    score += 50
                
            scored_candidates.append((score, candidate))
        
        # Return the highest scored candidate
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return scored_candidates[0][1] if scored_candidates else None


def main():
    if len(sys.argv) < 2:
        print("Usage: python advanced_reconstructor.py <runtime_output_file> [output_file]")
        print("Example: python advanced_reconstructor.py runtime_output.txt final_code.lua")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Read the runtime output
        with open(input_file, 'r', encoding='utf-8') as f:
            runtime_output = f.read()
        
        # Create reconstructor and analyze
        reconstructor = AdvancedLuaReconstructor()
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