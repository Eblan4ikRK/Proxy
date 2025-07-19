#!/usr/bin/env python3
"""
🔧 QUICK FIX для проблемы рекурсии в hooked файлах
Исправляет stack overflow в print hook

Использование: python3 quick_fix.py hooked_file.lua
"""

import sys
import os
import re

def main():
    if len(sys.argv) < 2:
        print("❌ Использование: python3 quick_fix.py hooked_file.lua")
        print("   hooked_file.lua - файл с проблемой рекурсии")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        sys.exit(1)
    
    print("🔧 QUICK FIX для исправления рекурсии в print hook")
    print(f"📁 Исправляемый файл: {input_file}")
    print("")
    
    # Читаем файл
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("🔍 Анализируем проблему...")
    
    # Проверяем наличие проблемного print hook
    if 'print = function' in code and 'capture_string' in code:
        print("✅ Найдена проблема с print hook рекурсией")
        
        # Исправляем код
        print("🔧 Применяем исправления...")
        
        # 1. Добавляем безопасный print в начало
        safe_print_code = '''
-- QUICK FIX: Безопасный print для избежания рекурсии
local original_print = print
local _print_safe = function(...)
    return original_print(...)
end

'''
        
        # 2. Заменяем все вызовы print в capture_string на _print_safe
        fixed_code = code.replace(
            'print("📝 STRING[" .. _string_counter .. "] (" .. (context or "unknown") .. "): \'" .. str .. "\'")',
            '_print_safe("📝 STRING[" .. _string_counter .. "] (" .. (context or "unknown") .. "): \'" .. str .. "\'")'
        )
        
        # 3. Убираем проблемный print hook
        fixed_code = re.sub(
            r'-- Hook print for отслеживания вывода.*?print = function\(.*?\n.*?end.*?\n.*?print\(".*?print function hooked!"\)',
            '-- Print hook DISABLED to prevent recursion\n_print_safe("⚠️ Print hook disabled to prevent stack overflow")',
            fixed_code,
            flags=re.DOTALL
        )
        
        # 4. Заменяем все оставшиеся print на _print_safe в hook коде
        fixed_code = re.sub(
            r'(\s+)print\("([^"]*)"',
            r'\1_print_safe("\2"',
            fixed_code
        )
        
        # 5. Добавляем safe_print в начало файла
        if '-- FULL HOOK INJECTION START' in fixed_code:
            fixed_code = fixed_code.replace(
                '-- FULL HOOK INJECTION START',
                safe_print_code + '-- FULL HOOK INJECTION START (FIXED)'
            )
        else:
            fixed_code = safe_print_code + fixed_code
        
        # Создаём исправленный файл
        fixed_filename = input_file.replace('.lua', '_fixed.lua')
        
        print(f"💾 Сохраняем исправленный файл: {fixed_filename}")
        with open(fixed_filename, 'w', encoding='utf-8') as f:
            f.write(fixed_code)
        
        print("")
        print("✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ:")
        print("   🔧 Добавлен безопасный _print_safe")
        print("   🔧 Заменены проблемные вызовы print")
        print("   🔧 Отключен рекурсивный print hook")
        print("   🔧 Исправлены capture функции")
        print("")
        print("🚀 Теперь запустите исправленный файл:")
        print(f"   lua {fixed_filename}")
        print("")
        print("✅ Проблема с stack overflow должна быть решена!")
        
    else:
        print("⚠️ Проблемы с print hook не обнаружено")
        print("   Возможно файл уже исправлен или проблема в другом месте")

if __name__ == "__main__":
    main()