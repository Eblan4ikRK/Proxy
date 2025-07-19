# Lua Deobfuscation Tools

This repository contains comprehensive tools for analyzing and deobfuscating Lua scripts, with specialized support for various obfuscation techniques including the Hercules obfuscator.

## Overview

The toolkit includes two main deobfuscators:

1. **`lua_deobfuscator.py`** - General-purpose Lua deobfuscator
2. **`hercules_deobfuscator.py`** - Specialized tool for Hercules obfuscated scripts

## Features

### General Lua Deobfuscator (`lua_deobfuscator.py`)

- **String Deobfuscation**: Reverses string encoding techniques including:
  - `string.char()` concatenation
  - Hex encoded strings (`\x` sequences)
  - Base64-like encodings
  - Table concatenation patterns

- **Variable Analysis**: 
  - Identifies obfuscated variable names
  - Simplifies overly complex identifiers
  - Maps variable usage patterns

- **Control Flow Analysis**:
  - Detects goto-based obfuscation
  - Identifies suspicious jump patterns
  - Analyzes label usage

- **Security Analysis**:
  - Identifies potential vulnerabilities
  - Detects dynamic code execution
  - Finds file/network access patterns
  - Warns about system command usage

- **Code Cleanup**:
  - Removes junk code patterns
  - Eliminates dead code branches
  - Formats output for readability

### Hercules Specialized Deobfuscator (`hercules_deobfuscator.py`)

- **Hercules Detection**: 
  - Identifies Hercules obfuscator signatures
  - Detects version information
  - Analyzes confidence levels

- **VM Analysis**:
  - Extracts virtual machine bytecode
  - Analyzes VM instruction patterns
  - Identifies custom instruction sets

- **String Extraction**:
  - Decodes Hercules custom string encoding
  - Extracts strings from VM bytecode
  - Handles advanced Caesar cipher variants

- **Anti-Tamper Detection**:
  - Identifies protection mechanisms
  - Analyzes integrity checks
  - Detects anti-debugging measures

## Installation

### Requirements

```bash
# Python 3.7 or higher
pip install argparse  # Usually included with Python
```

### Setup

1. Clone or download the repository
2. Ensure Python 3.7+ is installed
3. Make scripts executable:

```bash
chmod +x lua_deobfuscator.py
chmod +x hercules_deobfuscator.py
```

## Usage

### General Lua Deobfuscator

```bash
# Basic deobfuscation
python lua_deobfuscator.py obfuscated_script.lua

# Specify output file
python lua_deobfuscator.py obfuscated_script.lua -o clean_script.lua

# Analysis only (no deobfuscation)
python lua_deobfuscator.py obfuscated_script.lua -a

# Verbose output with detailed report
python lua_deobfuscator.py obfuscated_script.lua -v -r analysis_report.json
```

### Hercules Specialized Deobfuscator

```bash
# Analyze Hercules obfuscated script
python hercules_deobfuscator.py hercules_script.lua

# Full deobfuscation with custom output
python hercules_deobfuscator.py hercules_script.lua -o deobfuscated.lua

# Analysis only for Hercules detection
python hercules_deobfuscator.py hercules_script.lua -a -v

# Generate comprehensive report
python hercules_deobfuscator.py hercules_script.lua -r hercules_report.json
```

### Command Line Options

Both tools support the following options:

- `-o, --output`: Specify output file for deobfuscated code
- `-r, --report`: Generate JSON analysis report
- `-a, --analyze-only`: Only analyze, don't deobfuscate
- `-v, --verbose`: Enable verbose output
- `-h, --help`: Show help message

## Example Usage

### Analyzing Your Obfuscated File

```bash
# First, analyze the file to understand the obfuscation
python hercules_deobfuscator.py obf_USt8699Rq2bfiXQ93Za91xpB0A5QX61s671rNhAFv33NWZNz5E8OQL925279N3aQ.lua -a -v

# Then attempt deobfuscation
python hercules_deobfuscator.py obf_USt8699Rq2bfiXQ93Za91xpB0A5QX61s671rNhAFv33NWZNz5E8OQL925279N3aQ.lua -o deobfuscated.lua -r analysis.json
```

## Output Files

### Deobfuscated Code
- Cleaned and formatted Lua code
- Simplified variable names
- Decoded strings where possible
- Removed junk code

### Analysis Reports (JSON)
```json
{
  "obfuscation_analysis": {
    "obfuscation_detected": true,
    "techniques": ["string_encoding", "vm_execution", "variable_renaming"],
    "complexity": "high",
    "confidence": 0.95
  },
  "vulnerabilities": [
    {
      "type": "dynamic_code_execution",
      "description": "Uses loadstring() for dynamic code execution",
      "severity": "high"
    }
  ],
  "statistics": {
    "original_size": 45820,
    "deobfuscated_size": 2341,
    "obfuscation_ratio": 19.6
  }
}
```

## Supported Obfuscation Techniques

### String Obfuscation
- ✅ `string.char()` concatenation
- ✅ Hex encoding (`\x` sequences)
- ✅ Decimal encoding (`\123` sequences)
- ✅ Base64-like encodings
- ✅ Table concatenation
- ✅ Custom alphabet encoding (Hercules)

### Variable Obfuscation
- ✅ Random identifier renaming
- ✅ Hex-based variable names
- ✅ Overly long identifiers
- ⚠️ Semantic-preserving renaming (partial)

### Control Flow Obfuscation
- ✅ Goto-based control flow
- ✅ Dead code insertion
- ✅ Conditional junk code
- ⚠️ Complex state machines (limited)

### Advanced Techniques
- ✅ VM-based execution (Hercules)
- ✅ Bytecode manipulation
- ✅ Function inlining
- ✅ Anti-tamper checks
- ⚠️ Anti-debugging (detection only)

## Limitations

### General Limitations
1. **Dynamic Analysis**: These tools perform static analysis only. Some obfuscation techniques require runtime analysis.

2. **Complex VM**: Advanced virtual machines may require custom emulation.

3. **Encrypted Strings**: Cryptographically encrypted strings cannot be recovered without keys.

4. **Custom Encodings**: Novel encoding schemes may not be recognized.

### Hercules Specific Limitations
1. **VM Emulation**: Full deobfuscation requires executing the VM, which these tools don't do for security reasons.

2. **Bytecode Complexity**: The custom bytecode format may evolve between versions.

3. **Anti-Analysis**: Some Hercules versions include anti-analysis measures.

## Security Considerations

### Safe Analysis
- Tools perform static analysis only
- No code execution during analysis
- Safe to analyze malicious scripts

### Potential Risks
- Deobfuscated code may contain malicious functionality
- Always review deobfuscated output before execution
- Use sandboxed environments for testing

## Vulnerability Detection

The tools can identify several security concerns:

### High Risk
- Dynamic code execution (`loadstring`, `load`)
- System command execution (`os.execute`)
- File system access patterns
- Network communication attempts

### Medium Risk
- Environment manipulation (`_G`, `getfenv`)
- Debug interface usage
- Bytecode manipulation
- Anti-debugging measures

### Reporting
- Detailed vulnerability reports in JSON format
- Severity levels and descriptions
- Pattern matching locations

## Advanced Usage

### Custom Pattern Detection
You can extend the tools by modifying the pattern dictionaries in the source code:

```python
# Add custom patterns to lua_deobfuscator.py
'custom_pattern': re.compile(r'your_regex_here', re.IGNORECASE)
```

### Batch Processing
For multiple files:

```bash
# Bash script for batch processing
for file in *.lua; do
    python hercules_deobfuscator.py "$file" -o "clean_$file"
done
```

## Troubleshooting

### Common Issues

1. **"File not found"**
   - Ensure the file path is correct
   - Check file permissions

2. **"No obfuscation detected"**
   - File may use unknown obfuscation
   - Try the general deobfuscator instead

3. **"Partial deobfuscation only"**
   - Some techniques require dynamic analysis
   - Review the analysis report for details

### Getting Help

1. Check the verbose output (`-v` flag)
2. Review the analysis report (`-r` flag)
3. Try both deobfuscators on the same file
4. Examine the detected patterns and techniques

## Contributing

To contribute improvements:

1. Add new obfuscation pattern detection
2. Improve deobfuscation algorithms
3. Enhance vulnerability detection
4. Add support for new obfuscators

## Legal Notice

These tools are intended for:
- Security research
- Malware analysis
- Educational purposes
- Legitimate reverse engineering

Users are responsible for compliance with applicable laws and regulations.

## Version History

- **v1.0**: Initial release with basic deobfuscation
- **v1.1**: Added Hercules specialized support
- **v1.2**: Enhanced vulnerability detection
- **v1.3**: Improved string extraction and VM analysis

## Technical Details

### Hercules Obfuscator Analysis

Based on analysis of Hercules v1.6.2:

1. **VM Architecture**: Uses custom virtual machine with bytecode execution
2. **String Encoding**: Advanced Caesar cipher with custom alphabet
3. **Function Wrapping**: Multiple layers of function indirection
4. **Anti-Tamper**: Runtime integrity checks and protection mechanisms

### Detection Algorithms

The tools use multiple detection methods:
- Pattern matching for known signatures
- Statistical analysis of code structure
- Entropy analysis for encoded content
- Control flow graph analysis

This comprehensive toolkit provides powerful capabilities for analyzing and reversing Lua obfuscation while maintaining security and providing detailed insights into the protection mechanisms used.