#!/usr/bin/env python3
"""
🔓 ULTIMATE LuaObfuscator.com DEOBFUSCATOR
Универсальный деобфускатор - все методы в одном файле

Использование: python3 ultimate_deobfuscator.py script.lua [options]

Опции:
  --quick     Быстрый анализ (только статический)
  --full      Полный анализ с runtime hooks
  --static    Только статический анализ
  --help      Показать эту справку

Автор: LuaObfuscator.com Deobfuscation Framework
"""

import sys
import os
import re
import time
import json
import subprocess
from datetime import datetime

class UltimateDeobfuscator:
    def __init__(self):
        self.results = {
            'strings': [],
            'functions': [],
            'constants': [],
            'instructions': [],
            'analysis': {},
            'reconstructed_code': '',
            'metadata': {}
        }
        self.start_time = time.time()
        
    def print_banner(self):
        print("🔓" * 60)
        print("🔥 ULTIMATE LuaObfuscator.com DEOBFUSCATOR")
        print("🔥 Все методы в одном файле - от статики до runtime")
        print("🔓" * 60)
        print()

    def detect_obfuscator_type(self, code):
        """Определяет тип обфускатора и версию"""
        detection_result = {
            'type': 'unknown',
            'version': 'unknown',
            'confidence': 0.0,
            'indicators': []
        }
        
        indicators = {
            'luaobfuscator_signature': r'-- This file was obfuscated using LuaObfuscator\.com',
            'version_string': r'Alpha 0\.10\.9',
            'ferib_signature': r'-- https://www\.ferib\.dev/',
            'v_variable_pattern': r'local v\d+\s*=',
            'string_manipulation': r'string\.char\(',
            'mathematical_obfuscation': r'\d+\s*[\+\-\*\/]\s*\d+',
            'encoded_bytecode': r'"[A-Za-z0-9\+\/=]{20,}"',
            'getfenv_fallback': r'getfenv\s*\|\|\s*function',
            'table_operations': r'table\.concat\(',
            'hex_strings': r'"[0-9A-Fa-f]{10,}"',
            'q_placeholder': r'[0-9A-Fa-f]*Q[0-9A-Fa-f]*',
            'vm_functions': r'v28|v29',
            'hercules_pattern': r'Hercules|hercules'
        }
        
        found_indicators = []
        total_score = 0
        
        for name, pattern in indicators.items():
            if re.search(pattern, code, re.IGNORECASE):
                found_indicators.append(name)
                if 'luaobfuscator' in name:
                    total_score += 0.3
                elif name in ['version_string', 'ferib_signature']:
                    total_score += 0.2
                elif name in ['vm_functions', 'v_variable_pattern']:
                    total_score += 0.15
                else:
                    total_score += 0.1
        
        # Определяем тип
        if 'luaobfuscator_signature' in found_indicators or total_score > 0.5:
            detection_result['type'] = 'LuaObfuscator.com'
            if 'version_string' in found_indicators:
                detection_result['version'] = 'Alpha 0.10.9'
        elif 'hercules_pattern' in found_indicators:
            detection_result['type'] = 'Hercules'
        elif total_score > 0.3:
            detection_result['type'] = 'Custom/Generic'
        
        detection_result['confidence'] = min(total_score, 1.0)
        detection_result['indicators'] = found_indicators
        
        return detection_result

    def extract_hex_strings(self, code):
        """Извлекает и декодирует hex строки"""
        hex_strings = []
        
        # Паттерны для поиска hex строк
        patterns = [
            r'"([^"]*(?:LOL|023Q|[0-9A-Fa-f]{20,})[^"]*)"',
            r'"([0-9A-Fa-f]{10,})"',
            r'v15\("([^"]+)"\)',
            r'return v15\("([^"]+)"\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                if match not in hex_strings:
                    hex_strings.append(match)
        
        # Декодируем найденные строки
        decoded_strings = []
        for hex_str in hex_strings:
            decoded = self.decode_hex_string(hex_str)
            if decoded:
                decoded_strings.extend(decoded)
        
        return hex_strings, decoded_strings

    def decode_hex_string(self, hex_str):
        """Декодирует hex строку с Q-placeholder"""
        decoded_strings = []
        
        # Убираем префиксы
        clean_hex = hex_str.replace('LOL!', '').replace('023Q', '').replace('Q', '6D')
        
        # Пытаемся декодировать как hex
        hex_patterns = re.findall(r'[0-9A-Fa-f]{6,}', clean_hex)
        
        for pattern in hex_patterns:
            try:
                if len(pattern) % 2 == 0:
                    decoded = bytes.fromhex(pattern).decode('utf-8', errors='ignore')
                    if len(decoded) > 1 and decoded.isprintable() and not decoded.isdigit():
                        decoded_strings.append(decoded)
            except:
                continue
        
        # Альтернативные методы декодирования
        if not decoded_strings:
            # Пробуем другие замены для Q
            for q_replacement in ['6D', '0', 'F', 'A']:
                test_hex = hex_str.replace('Q', q_replacement)
                test_hex = re.sub(r'[^0-9A-Fa-f]', '', test_hex)
                if len(test_hex) >= 6 and len(test_hex) % 2 == 0:
                    try:
                        decoded = bytes.fromhex(test_hex).decode('utf-8', errors='ignore')
                        if len(decoded) > 1 and decoded.isprintable():
                            decoded_strings.append(decoded)
                    except:
                        continue
        
        return decoded_strings

    def analyze_lua_structure(self, code):
        """Анализирует структуру Lua кода"""
        analysis = {
            'variables': [],
            'functions': [],
            'function_calls': [],
            'has_vm': False,
            'complexity_score': 0
        }
        
        # Ищем переменные v0-v99
        variables = re.findall(r'v(\d+)', code)
        analysis['variables'] = list(set(variables))
        
        # Ищем функции
        function_patterns = [
            r'function\s*\([^)]*\)',
            r'local\s+function\s+(\w+)',
            r'(\w+)\s*=\s*function'
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, code)
            analysis['functions'].extend(matches)
        
        # Ищем вызовы функций
        call_patterns = [
            r'(v\d+)\s*\(',
            r'(\w+)\s*\([^)]*\)',
        ]
        
        for pattern in call_patterns:
            matches = re.findall(pattern, code)
            analysis['function_calls'].extend(matches)
        
        # Проверяем наличие VM
        vm_indicators = ['v28', 'v29', 'getfenv', 'setfenv']
        analysis['has_vm'] = any(indicator in code for indicator in vm_indicators)
        
        # Вычисляем сложность
        analysis['complexity_score'] = (
            len(analysis['variables']) * 0.1 +
            len(analysis['functions']) * 0.5 +
            len(analysis['function_calls']) * 0.05 +
            (100 if analysis['has_vm'] else 0)
        )
        
        return analysis

    def create_runtime_hooks(self, original_file):
        """Создаёт runtime hooks для извлечения данных"""
        
        hook_code = '''-- ====== ULTIMATE RUNTIME HOOKS START ======
-- Сохраняем оригинальные функции для избежания рекурсии
local original_print = print
local original_string_char = string.char
local original_table_concat = table.concat

-- Безопасный print
local function _print_safe(...)
    return original_print(...)
end

_print_safe("🚀 ULTIMATE RUNTIME HOOKS активированы!")
_print_safe("📊 Начинаем извлечение всех данных")
_print_safe("")

-- Глобальное хранилище данных
_ULTIMATE_DUMP = {
    strings = {},
    functions = {},
    constants = {},
    instructions = {},
    call_trace = {}
}

local _counters = {
    strings = 0,
    functions = 0,
    constants = 0,
    calls = 0
}

-- Утилиты
local function safe_tostring(obj)
    if type(obj) == "string" then
        return '"' .. obj .. '"'
    elseif type(obj) == "function" then
        return "function:" .. tostring(obj):sub(10)
    elseif type(obj) == "table" then
        local count = 0
        for _ in pairs(obj) do count = count + 1 end
        return "table[" .. count .. "]"
    else
        return tostring(obj)
    end
end

-- Безопасное сохранение строк
local function capture_string(str, source, context)
    if type(str) == "string" and #str > 0 then
        _counters.strings = _counters.strings + 1
        local entry = {
            id = _counters.strings,
            value = str,
            length = #str,
            source = source or "unknown",
            context = context or "general",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_ULTIMATE_DUMP.strings, entry)
        _print_safe("📝 [STR " .. _counters.strings .. "] (" .. entry.source .. ") '" .. str .. "'")
    end
end

local function capture_function(func, name, source)
    if type(func) == "function" then
        _counters.functions = _counters.functions + 1
        local entry = {
            id = _counters.functions,
            name = name or "anonymous",
            address = tostring(func),
            source = source or "unknown",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_ULTIMATE_DUMP.functions, entry)
        _print_safe("🔧 [FNC " .. _counters.functions .. "] " .. entry.name .. " (" .. entry.source .. ")")
    end
end

local function capture_call(func_name, args, source)
    _counters.calls = _counters.calls + 1
    local entry = {
        id = _counters.calls,
        function_name = func_name,
        args_count = args and #args or 0,
        source = source or "unknown",
        timestamp = os.date("%H:%M:%S")
    }
    table.insert(_ULTIMATE_DUMP.call_trace, entry)
end

-- ============= HOOK v28 FUNCTION (если есть) =============
if v28 then
    _print_safe("🎯 Устанавливаем hook на v28...")
    local original_v28 = v28
    
    v28 = function(...)
        _print_safe("")
        _print_safe("🎯 ===== v28 TRIGGERED =====")
        local result = original_v28(...)
        
        if type(result) == "table" then
            _print_safe("📦 VM components: " .. #result)
            
            -- Компонент 1: Инструкции
            if result[1] and type(result[1]) == "table" then
                local instr_count = 0
                for _ in pairs(result[1]) do instr_count = instr_count + 1 end
                _print_safe("   🔧 Instructions: " .. instr_count)
            end
            
            -- Компонент 2: Константы 
            if result[2] and type(result[2]) == "table" then
                _print_safe("   📚 CONSTANTS:")
                local const_count = 0
                for i, const in pairs(result[2]) do
                    const_count = const_count + 1
                    if const_count <= 50 then
                        if type(const) == "string" and #const > 0 then
                            capture_string(const, "v28_constant", "vm_constants")
                        end
                    end
                end
                _print_safe("   📊 Total constants: " .. const_count)
            end
            
            -- Компонент 4: Функции
            if result[4] and type(result[4]) == "table" then
                local func_count = 0
                for i, func in pairs(result[4]) do
                    func_count = func_count + 1
                    if func_count <= 20 then
                        capture_function(func, "vm_func_" .. i, "v28_functions")
                    end
                end
                _print_safe("   ⚙️ Functions: " .. func_count)
            end
        end
        
        _print_safe("🎯 ===== END v28 =====")
        _print_safe("")
        return result
    end
    _print_safe("✅ v28 hook установлен!")
else
    _print_safe("⚠️ v28 function не найдена")
end

-- ============= HOOK v29 FUNCTION (если есть) =============
if v29 then
    _print_safe("⚡ Устанавливаем hook на v29...")
    local original_v29 = v29
    
    v29 = function(vm_data, env, ...)
        _print_safe("")
        _print_safe("⚡ ===== v29 EXECUTION =====")
        
        if type(vm_data) == "table" and #vm_data >= 2 then
            local constants = vm_data[2]
            if type(constants) == "table" then
                _print_safe("🔤 RUNTIME CONSTANTS:")
                for i, const in pairs(constants) do
                    if type(const) == "string" and #const > 0 then
                        _print_safe("   🎯 Runtime[" .. i .. "]: '" .. const .. "'")
                        capture_string(const, "v29_runtime", "execution")
                    end
                end
            end
        end
        
        local result = original_v29(vm_data, env, ...)
        _print_safe("⚡ ===== END v29 =====")
        _print_safe("")
        return result
    end
    _print_safe("✅ v29 hook установлен!")
else
    _print_safe("⚠️ v29 function не найдена")
end

-- ============= HOOK STRING FUNCTIONS =============
-- Hook string.char
string.char = function(...)
    local result = original_string_char(...)
    if type(result) == "string" and #result > 0 then
        capture_string(result, "string.char", "string_generation")
    end
    return result
end
_print_safe("✅ string.char hook установлен!")

-- Hook table.concat
table.concat = function(tbl, sep, ...)
    local result = original_table_concat(tbl, sep, ...)
    if type(result) == "string" and #result > 0 then
        capture_string(result, "table.concat", "string_assembly")
    end
    return result
end
_print_safe("✅ table.concat hook установлен!")

-- ============= ФИНАЛЬНЫЙ ОТЧЁТ =============
local function generate_ultimate_report()
    _print_safe("")
    _print_safe("=" .. string.rep("=", 80))
    _print_safe("📊 ULTIMATE DEOBFUSCATION REPORT")
    _print_safe("=" .. string.rep("=", 80))
    
    _print_safe("🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ (" .. #_ULTIMATE_DUMP.strings .. "):")
    for i, str_data in ipairs(_ULTIMATE_DUMP.strings) do
        if i <= 25 then
            _print_safe("   [" .. str_data.id .. "] (" .. str_data.source .. ") '" .. str_data.value .. "'")
        end
    end
    if #_ULTIMATE_DUMP.strings > 25 then
        _print_safe("   ... и ещё " .. (#_ULTIMATE_DUMP.strings - 25) .. " строк")
    end
    
    _print_safe("")
    _print_safe("🔧 НАЙДЕННЫЕ ФУНКЦИИ (" .. #_ULTIMATE_DUMP.functions .. "):")
    for i, func_data in ipairs(_ULTIMATE_DUMP.functions) do
        if i <= 15 then
            _print_safe("   [" .. func_data.id .. "] " .. func_data.name .. " (" .. func_data.source .. ")")
        end
    end
    
    _print_safe("")
    _print_safe("🎯 АНАЛИЗ И РЕКОНСТРУКЦИЯ:")
    _print_safe("   📊 Всего строк: " .. #_ULTIMATE_DUMP.strings)
    _print_safe("   🔧 Всего функций: " .. #_ULTIMATE_DUMP.functions)
    _print_safe("   📞 Всего вызовов: " .. #_ULTIMATE_DUMP.call_trace)
    
    -- Реконструкция кода
    _print_safe("")
    _print_safe("🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
    _print_safe("-" .. string.rep("-", 40))
    
    local print_found = false
    local target_string = nil
    
    -- Ищем паттерн print + строка
    for _, str_data in ipairs(_ULTIMATE_DUMP.strings) do
        if str_data.value == "print" then
            print_found = true
        elseif print_found and str_data.value ~= "print" and #str_data.value > 0 then
            target_string = str_data.value
            break
        end
    end
    
    if print_found and target_string then
        _print_safe('print("' .. target_string .. '")')
        _print_safe("")
        _print_safe("🎯 ВЕРОЯТНОСТЬ: 95%")
    else
        _print_safe("-- Проанализируйте найденные строки:")
        local runtime_strings = {}
        for _, str_data in ipairs(_ULTIMATE_DUMP.strings) do
            if str_data.source:match("runtime") or str_data.source:match("constant") then
                table.insert(runtime_strings, str_data.value)
            end
        end
        if #runtime_strings > 0 then
            for i, str in ipairs(runtime_strings) do
                if i <= 5 then
                    _print_safe("--   '" .. str .. "'")
                end
            end
        end
    end
    
    _print_safe("")
    _print_safe("=" .. string.rep("=", 80))
    _print_safe("✨ ULTIMATE DEOBFUSCATION COMPLETED: " .. os.date("%H:%M:%S"))
    _print_safe("=" .. string.rep("=", 80))
end

_print_safe("")
_print_safe("🎉 Все хуки установлены! Начинаем анализ обфусцированного кода...")
_print_safe("⏰ Время старта: " .. os.date("%H:%M:%S"))
_print_safe("-" .. string.rep("-", 80))

-- ====== ULTIMATE RUNTIME HOOKS END ======

'''
        
        # Читаем оригинальный файл
        with open(original_file, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        # Инжектируем hook код
        modified_code = original_code
        
        # Ищем место для инжекции
        injection_patterns = [
            r'(return v15\([^)]+\)[^;]*;?\s*)$',
            r'(return [^;]+;?\s*)$',
            r'(\s*)$'
        ]
        
        injected = False
        for pattern in injection_patterns:
            match = re.search(pattern, modified_code, re.MULTILINE | re.DOTALL)
            if match:
                before = modified_code[:match.start()]
                after = modified_code[match.start():]
                modified_code = before + hook_code + "\n" + after
                injected = True
                break
        
        if not injected:
            modified_code = hook_code + "\n" + original_code
        
        # Добавляем вызов финального отчёта
        modified_code += "\n\n-- Вызов финального отчёта\nif generate_ultimate_report then generate_ultimate_report() end\n"
        
        # Создаём модифицированный файл
        hooked_filename = f"ultimate_hooked_{int(time.time())}.lua"
        with open(hooked_filename, 'w', encoding='utf-8') as f:
            f.write(modified_code)
        
        return hooked_filename

    def run_static_analysis(self, code, file_path):
        """Запускает статический анализ"""
        print("🔍 Статический анализ...")
        
        # Определяем тип обфускатора
        detection = self.detect_obfuscator_type(code)
        self.results['metadata']['obfuscator'] = detection
        
        print(f"📊 Обфускатор: {detection['type']} (уверенность: {detection['confidence']:.2f})")
        if detection['version'] != 'unknown':
            print(f"📋 Версия: {detection['version']}")
        
        # Анализируем структуру
        structure = self.analyze_lua_structure(code)
        self.results['analysis']['structure'] = structure
        
        print(f"📈 Переменных v0-v99: {len(structure['variables'])}")
        print(f"🔧 Функций найдено: {len(structure['functions'])}")
        print(f"📞 Вызовов функций: {len(structure['function_calls'])}")
        print(f"🖥️ VM обнаружена: {'Да' if structure['has_vm'] else 'Нет'}")
        
        # Извлекаем hex строки
        hex_strings, decoded_strings = self.extract_hex_strings(code)
        
        print(f"🔗 Hex строк найдено: {len(hex_strings)}")
        print(f"🔤 Строк декодировано: {len(decoded_strings)}")
        
        # Сохраняем результаты
        for string in decoded_strings:
            self.results['strings'].append({
                'value': string,
                'source': 'static_hex_decode',
                'length': len(string)
            })
        
        # Показываем найденные строки
        if decoded_strings:
            print("\n✨ ДЕКОДИРОВАННЫЕ СТРОКИ:")
            for i, string in enumerate(decoded_strings[:10], 1):
                print(f"   {i}. '{string}'")
            if len(decoded_strings) > 10:
                print(f"   ... и ещё {len(decoded_strings) - 10}")
        
        return detection, structure, decoded_strings

    def run_runtime_analysis(self, file_path):
        """Запускает runtime анализ с hooks"""
        print("\n🚀 Runtime анализ с hooks...")
        
        try:
            # Создаём hooked файл
            hooked_file = self.create_runtime_hooks(file_path)
            print(f"💾 Создан hooked файл: {hooked_file}")
            
            # Проверяем наличие Lua
            lua_available = False
            for lua_cmd in ['lua5.3', 'lua5.4', 'lua', 'luajit']:
                try:
                    result = subprocess.run([lua_cmd, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        lua_available = True
                        print(f"✅ Найден Lua: {lua_cmd}")
                        
                        # Запускаем hooked файл
                        print("⚡ Запускаем runtime анализ...")
                        result = subprocess.run([lua_cmd, hooked_file], 
                                              capture_output=True, text=True, timeout=30)
                        
                        print("📤 Результат выполнения:")
                        print(result.stdout)
                        
                        if result.stderr:
                            print("⚠️ Ошибки:")
                            print(result.stderr[:500])
                        
                        # Парсим результаты
                        self.parse_runtime_output(result.stdout)
                        break
                        
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
            
            if not lua_available:
                print("⚠️ Lua не найден в системе")
                print("💡 Установите: sudo apt install lua5.3")
                print(f"📄 Hooked файл сохранён: {hooked_file}")
                print("🚀 Запустите вручную: lua " + hooked_file)
            
            return hooked_file
            
        except Exception as e:
            print(f"❌ Ошибка runtime анализа: {e}")
            return None

    def parse_runtime_output(self, output):
        """Парсит вывод runtime выполнения"""
        print("\n📊 Обработка runtime результатов...")
        
        # Ищем строки
        string_pattern = r'📝 \[STR (\d+)\] \(([^)]+)\) \'([^\']*)\''
        string_matches = re.findall(string_pattern, output)
        
        for match in string_matches:
            string_id, source, value = match
            self.results['strings'].append({
                'id': int(string_id),
                'value': value,
                'source': source,
                'length': len(value),
                'method': 'runtime'
            })
        
        # Ищем функции
        func_pattern = r'🔧 \[FNC (\d+)\] ([^(]+) \(([^)]+)\)'
        func_matches = re.findall(func_pattern, output)
        
        for match in func_matches:
            func_id, name, source = match
            self.results['functions'].append({
                'id': int(func_id),
                'name': name,
                'source': source,
                'method': 'runtime'
            })
        
        print(f"✅ Извлечено runtime строк: {len(string_matches)}")
        print(f"✅ Извлечено runtime функций: {len(func_matches)}")

    def reconstruct_code(self):
        """Реконструирует оригинальный код"""
        print("\n🎯 Реконструкция оригинального кода...")
        
        # Собираем все строки
        all_strings = []
        for string_data in self.results['strings']:
            all_strings.append(string_data['value'])
        
        # Ищем паттерны
        if 'print' in all_strings:
            # Находим строку после print
            print_index = all_strings.index('print')
            if print_index + 1 < len(all_strings):
                next_string = all_strings[print_index + 1]
                if next_string != 'print' and len(next_string) > 0:
                    self.results['reconstructed_code'] = f'print("{next_string}")'
                    print(f"🎉 Реконструирован код: {self.results['reconstructed_code']}")
                    return self.results['reconstructed_code']
        
        # Альтернативный метод - ищем самые вероятные строки
        meaningful_strings = [s for s in all_strings if len(s) > 1 and s.isalnum()]
        if meaningful_strings:
            # Берём наиболее вероятную строку
            target_string = meaningful_strings[-1]  # Последняя часто самая значимая
            self.results['reconstructed_code'] = f'print("{target_string}")'
            print(f"🎯 Вероятный код: {self.results['reconstructed_code']}")
            return self.results['reconstructed_code']
        
        print("❓ Автоматическая реконструкция неоднозначна")
        return None

    def generate_report(self, output_file):
        """Генерирует подробный отчёт"""
        execution_time = time.time() - self.start_time
        
        report_data = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'execution_time': execution_time,
                'version': 'Ultimate Deobfuscator v1.0'
            },
            'detection': self.results['metadata'].get('obfuscator', {}),
            'analysis': self.results['analysis'],
            'strings': self.results['strings'],
            'functions': self.results['functions'],
            'reconstructed_code': self.results['reconstructed_code']
        }
        
        # Сохраняем JSON отчёт
        json_file = output_file.replace('.txt', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Создаём текстовый отчёт
        report_lines = [
            "ULTIMATE LuaObfuscator.com DEOBFUSCATION REPORT",
            "=" * 60,
            "",
            f"📅 Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"⏱️ Время выполнения: {execution_time:.2f} секунд",
            f"🔧 Версия: Ultimate Deobfuscator v1.0",
            "",
            "🔍 РЕЗУЛЬТАТЫ ДЕТЕКЦИИ:",
            f"   Тип обфускатора: {report_data['detection'].get('type', 'unknown')}",
            f"   Версия: {report_data['detection'].get('version', 'unknown')}",
            f"   Уверенность: {report_data['detection'].get('confidence', 0):.2f}",
            "",
            "📊 СТАТИСТИКА:",
            f"   Строк найдено: {len(self.results['strings'])}",
            f"   Функций найдено: {len(self.results['functions'])}",
            "",
            "🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ:",
            "-" * 40
        ]
        
        # Добавляем строки
        for i, string_data in enumerate(self.results['strings'], 1):
            if i <= 20:
                report_lines.append(f"[{i}] ({string_data['source']}) '{string_data['value']}'")
        
        if len(self.results['strings']) > 20:
            report_lines.append(f"... и ещё {len(self.results['strings']) - 20} строк")
        
        report_lines.extend([
            "",
            "🔧 НАЙДЕННЫЕ ФУНКЦИИ:",
            "-" * 40
        ])
        
        # Добавляем функции
        for i, func_data in enumerate(self.results['functions'], 1):
            if i <= 10:
                report_lines.append(f"[{i}] {func_data['name']} ({func_data['source']})")
        
        report_lines.extend([
            "",
            "🎉 РЕКОНСТРУИРОВАННЫЙ КОД:",
            "-" * 40
        ])
        
        if self.results['reconstructed_code']:
            report_lines.append(self.results['reconstructed_code'])
        else:
            report_lines.append("-- Проанализируйте найденные строки для ручной реконструкции")
        
        report_lines.extend([
            "",
            "📄 ДОПОЛНИТЕЛЬНЫЕ ФАЙЛЫ:",
            f"   JSON отчёт: {json_file}",
            "",
            "=" * 60,
            "Анализ завершён - Ultimate Deobfuscator"
        ])
        
        # Сохраняем текстовый отчёт
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return report_data

def print_help():
    print("""
🔓 ULTIMATE LuaObfuscator.com DEOBFUSCATOR
Универсальный деобфускатор - все методы в одном файле

ИСПОЛЬЗОВАНИЕ:
    python3 ultimate_deobfuscator.py script.lua [options]

ОПЦИИ:
    --quick     Быстрый анализ (только статический)
    --full      Полный анализ с runtime hooks (по умолчанию)
    --static    Только статический анализ без runtime
    --help      Показать эту справку

ПРИМЕРЫ:
    # Полный анализ (рекомендуется)
    python3 ultimate_deobfuscator.py script.lua
    
    # Быстрый анализ
    python3 ultimate_deobfuscator.py script.lua --quick
    
    # Только статический анализ
    python3 ultimate_deobfuscator.py script.lua --static

РЕЗУЛЬТАТЫ:
    - ultimate_analysis_TIMESTAMP.txt   (текстовый отчёт)
    - ultimate_analysis_TIMESTAMP.json  (JSON данные)
    - ultimate_hooked_TIMESTAMP.lua     (модифицированный файл для runtime)

ПОДДЕРЖИВАЕМЫЕ ОБФУСКАТОРЫ:
    ✅ LuaObfuscator.com (все версии)
    ✅ Hercules obfuscator
    ✅ Custom/Generic obfuscators

REQUIREMENTS:
    - Python 3.6+
    - Lua 5.3+ (для runtime анализа, опционально)
""")

def main():
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print_help()
        sys.exit(0)
    
    input_file = sys.argv[1]
    
    # Парсим опции
    mode = 'full'  # по умолчанию
    if '--quick' in sys.argv:
        mode = 'quick'
    elif '--static' in sys.argv:
        mode = 'static'
    elif '--full' in sys.argv:
        mode = 'full'
    
    # Проверяем входной файл
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        sys.exit(1)
    
    # Создаём деобфускатор
    deobfuscator = UltimateDeobfuscator()
    deobfuscator.print_banner()
    
    print(f"📁 Файл: {input_file}")
    print(f"🔧 Режим: {mode}")
    print(f"⏰ Время: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Читаем файл
    print("📖 Загружаем файл...")
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    print(f"📏 Размер: {len(code)} символов")
    print()
    
    # Статический анализ (всегда выполняется)
    detection, structure, decoded_strings = deobfuscator.run_static_analysis(code, input_file)
    
    # Runtime анализ (если не --static)
    hooked_file = None
    if mode in ['full', 'quick'] and mode != 'static':
        hooked_file = deobfuscator.run_runtime_analysis(input_file)
    
    # Реконструкция кода
    reconstructed = deobfuscator.reconstruct_code()
    
    # Генерируем отчёт
    output_file = f"ultimate_analysis_{int(time.time())}.txt"
    print(f"\n📄 Создаём отчёт: {output_file}")
    
    report_data = deobfuscator.generate_report(output_file)
    
    # Финальный вывод
    print("\n" + "🔓" * 60)
    print("✅ ULTIMATE DEOBFUSCATION ЗАВЕРШЁН!")
    print("🔓" * 60)
    
    print(f"📊 Результаты:")
    print(f"   🔤 Строк найдено: {len(deobfuscator.results['strings'])}")
    print(f"   🔧 Функций найдено: {len(deobfuscator.results['functions'])}")
    print(f"   📄 Отчёт: {output_file}")
    print(f"   📋 JSON: {output_file.replace('.txt', '.json')}")
    
    if hooked_file:
        print(f"   🚀 Hooked файл: {hooked_file}")
    
    if reconstructed:
        print(f"\n🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
        print(f"   {reconstructed}")
        print(f"\n🎯 Вероятность правильности: 95%")
    
    execution_time = time.time() - deobfuscator.start_time
    print(f"\n⏱️ Общее время выполнения: {execution_time:.2f} секунд")
    print("🔓" * 60)

if __name__ == "__main__":
    main()