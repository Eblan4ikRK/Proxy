#!/usr/bin/env python3
"""
🔓 ONE-CLICK LuaObfuscator.com DEOBFUSCATOR
Быстрая деобфускация в одну команду

Использование: python3 deobfuscate.py script.lua
"""

import sys
import os
import re
import time
import subprocess
from datetime import datetime

def print_header():
    print("🔓" * 50)
    print("🔥 ONE-CLICK LuaObfuscator.com DEOBFUSCATOR")
    print("🔓" * 50)
    print()

def extract_strings_from_hex(hex_string):
    """Быстрое извлечение строк из hex payload"""
    strings = []
    
    # Ищем паттерны строк в hex
    hex_patterns = re.findall(r'[0-9A-Fa-f]{6,}', hex_string)
    
    for pattern in hex_patterns:
        try:
            # Пытаемся декодировать как hex
            if len(pattern) % 2 == 0:
                decoded = bytes.fromhex(pattern).decode('utf-8', errors='ignore')
                # Фильтруем читаемые строки
                if len(decoded) > 1 and decoded.isprintable() and not decoded.isdigit():
                    strings.append(decoded)
        except:
            continue
    
    return strings

def analyze_lua_structure(code):
    """Быстрый анализ структуры Lua кода"""
    results = {
        'variables': [],
        'functions': [],
        'hex_payloads': [],
        'strings': []
    }
    
    # Ищем переменные v0-v99
    variables = re.findall(r'v(\d+)', code)
    results['variables'] = list(set(variables))
    
    # Ищем hex строки
    hex_matches = re.findall(r'"([^"]*(?:LOL|023Q|[0-9A-Fa-f]{20,})[^"]*)"', code)
    results['hex_payloads'] = hex_matches
    
    # Извлекаем строки из hex
    for hex_payload in hex_matches:
        extracted_strings = extract_strings_from_hex(hex_payload)
        results['strings'].extend(extracted_strings)
    
    # Ищем функции
    function_matches = re.findall(r'function\s*\([^)]*\)|local\s+function\s+(\w+)', code)
    results['functions'] = function_matches
    
    return results

def create_injection_script(original_file):
    """Создаёт простой injection скрипт"""
    injection_code = '''-- SIMPLE DEOBFUSCATION INJECTION
print("🚀 Deobfuscation injection активирован!")

-- Hook для v28
if v28 then
    local original_v28 = v28
    v28 = function(...)
        print("🎯 v28 вызвана!")
        local result = original_v28(...)
        if type(result) == "table" and #result >= 2 then
            local constants = result[2]
            if type(constants) == "table" then
                print("📝 Найденные строки:")
                for i, const in pairs(constants) do
                    if type(const) == "string" and #const > 0 then
                        print("  [" .. i .. "] '" .. const .. "'")
                    end
                end
            end
        end
        return result
    end
end

-- Hook для v29
if v29 then
    local original_v29 = v29
    v29 = function(vm_data, env, ...)
        print("⚡ v29 выполняется!")
        if type(vm_data) == "table" and #vm_data >= 2 then
            local constants = vm_data[2]
            if type(constants) == "table" then
                print("🔤 Runtime строки:")
                for i, const in pairs(constants) do
                    if type(const) == "string" and #const > 0 then
                        print("  Runtime[" .. i .. "]: '" .. const .. "'")
                    end
                end
            end
        end
        return original_v29(vm_data, env, ...)
    end
end

print("✅ Injection готов, запускаем оригинальный код...")
print("-" * 50)

'''
    
    # Читаем оригинальный файл
    with open(original_file, 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    # Создаём модифицированный файл
    modified_file = f"injected_{int(time.time())}.lua"
    with open(modified_file, 'w', encoding='utf-8') as f:
        f.write(injection_code + original_code)
    
    return modified_file

def main():
    if len(sys.argv) < 2:
        print("❌ Использование: python3 deobfuscate.py script.lua")
        print("   script.lua - обфусцированный LuaObfuscator.com файл")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        sys.exit(1)
    
    print_header()
    print(f"📁 Файл: {input_file}")
    print(f"⏰ Время: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Читаем файл
    print("📖 Читаем файл...")
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    file_size = len(code)
    print(f"📏 Размер: {file_size} символов")
    
    # Быстрый анализ
    print("\n🔍 Быстрый анализ структуры...")
    analysis = analyze_lua_structure(code)
    
    print(f"📊 Найдено переменных v0-v99: {len(analysis['variables'])}")
    print(f"🔧 Найдено функций: {len(analysis['functions'])}")
    print(f"📦 Найдено hex payload: {len(analysis['hex_payloads'])}")
    print(f"🔤 Извлечено строк из hex: {len(analysis['strings'])}")
    
    # Показываем найденные строки
    if analysis['strings']:
        print("\n✨ НАЙДЕННЫЕ СТРОКИ:")
        for i, string in enumerate(analysis['strings'][:10], 1):
            print(f"   {i}. '{string}'")
        if len(analysis['strings']) > 10:
            print(f"   ... и ещё {len(analysis['strings']) - 10}")
    
    # Проверяем наличие ключевых функций
    has_v28 = 'v28' in code
    has_v29 = 'v29' in code
    
    print(f"\n🎯 Ключевые функции:")
    print(f"   v28: {'✅ Найдена' if has_v28 else '❌ Не найдена'}")
    print(f"   v29: {'✅ Найдена' if has_v29 else '❌ Не найдена'}")
    
    # Пытаемся реконструировать код
    print("\n🎉 ПОПЫТКА РЕКОНСТРУКЦИИ:")
    
    if 'print' in analysis['strings']:
        other_strings = [s for s in analysis['strings'] if s != 'print' and len(s) > 0]
        if other_strings:
            reconstructed = f'print("{other_strings[0]}")'
            print(f"🎯 Вероятный оригинальный код: {reconstructed}")
        else:
            print("🎯 Найдена функция print, но строка для вывода не определена")
    else:
        print("📋 Реконструкция неоднозначна, анализируйте найденные строки")
    
    # Создаём injection если возможно
    if has_v28 or has_v29:
        print(f"\n🚀 Создание injection скрипта...")
        try:
            injected_file = create_injection_script(input_file)
            print(f"✅ Создан: {injected_file}")
            print("\n📋 Для полного анализа выполните:")
            print(f"   1. Установите Lua: sudo apt install lua5.3")
            print(f"   2. Запустите: lua {injected_file}")
            print(f"   3. Анализируйте вывод для полной деобфускации")
        except Exception as e:
            print(f"❌ Ошибка создания injection: {e}")
    
    # Сохраняем краткий отчёт
    report_file = f"quick_analysis_{int(time.time())}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("ONE-CLICK DEOBFUSCATION REPORT\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Файл: {input_file}\n")
        f.write(f"Размер: {file_size} символов\n")
        f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("СТАТИСТИКА:\n")
        f.write(f"  Переменных: {len(analysis['variables'])}\n")
        f.write(f"  Функций: {len(analysis['functions'])}\n")
        f.write(f"  Hex payload: {len(analysis['hex_payloads'])}\n")
        f.write(f"  Строк извлечено: {len(analysis['strings'])}\n\n")
        
        f.write("НАЙДЕННЫЕ СТРОКИ:\n")
        for i, string in enumerate(analysis['strings'], 1):
            f.write(f"  {i}. '{string}'\n")
        
        if 'print' in analysis['strings']:
            other_strings = [s for s in analysis['strings'] if s != 'print']
            if other_strings:
                f.write(f"\nВЕРОЯТНЫЙ КОД:\nprint(\"{other_strings[0]}\")\n")
    
    print(f"\n📄 Краткий отчёт сохранён: {report_file}")
    
    print("\n" + "🔓" * 50)
    print("✅ ONE-CLICK DEOBFUSCATION ЗАВЕРШЁН!")
    
    if analysis['strings']:
        print(f"🎯 Найдено {len(analysis['strings'])} строк!")
        if 'print' in analysis['strings']:
            print("🎉 Обнаружен print statement!")
    
    print("🔓" * 50)

if __name__ == "__main__":
    main()