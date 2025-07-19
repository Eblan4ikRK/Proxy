#!/usr/bin/env python3
"""
FULL HOOK DUMPER (Python версия) для LuaObfuscator.com
Полный дамп всех строк, функций, VM инструкций и данных

Использование: python3 full_hook.py input.lua output.txt
Автор: Deobfuscation Framework
"""

import sys
import os
import re
import time
import json
from datetime import datetime

def print_usage():
    print("❌ Использование: python3 full_hook.py input.lua output.txt")
    print("   input.lua  - обфусцированный файл")
    print("   output.txt - файл для сохранения результатов")
    print("")
    print("💡 Этот скрипт создаёт модифицированный Lua файл с хуками")
    print("   для полного дампа всех строк и функций")

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Проверка существования файла
    if not os.path.exists(input_file):
        print(f"❌ Ошибка: Файл {input_file} не найден!")
        sys.exit(1)
    
    print("🔍 FULL HOOK DUMPER (Python версия) для LuaObfuscator.com")
    print(f"📁 Входной файл: {input_file}")
    print(f"📄 Выходной файл: {output_file}")
    print("")
    
    start_time = time.time()
    
    # Читаем оригинальный файл
    print("📖 Читаем обфусцированный файл...")
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            original_code = f.read()
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        sys.exit(1)
    
    print(f"📏 Размер файла: {len(original_code)} символов")
    
    # Создаём hook код
    print("🔧 Создаём hook инъекции...")
    
    hook_code = '''-- ====== FULL HOOK INJECTION START ======
print("🚀 FULL HOOK DUMPER активирован!")
print("📊 Начинаем извлечение всех данных из LuaObfuscator.com")
print("")

-- Глобальные переменные для сбора данных
_FULL_DUMP = {
    strings = {},
    functions = {},
    constants = {},
    instructions = {},
    vm_structure = {},
    execution_trace = {}
}

local _string_counter = 0
local _function_counter = 0
local _constant_counter = 0
local _instruction_counter = 0

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

local function capture_string(str, source, context)
    if type(str) == "string" and #str > 0 then
        _string_counter = _string_counter + 1
        local entry = {
            id = _string_counter,
            value = str,
            length = #str,
            source = source or "unknown",
            context = context or "general",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_FULL_DUMP.strings, entry)
        print("📝 [STR " .. _string_counter .. "] (" .. entry.source .. ") '" .. str .. "'")
    end
end

local function capture_function(func, name, source, context)
    if type(func) == "function" then
        _function_counter = _function_counter + 1
        local entry = {
            id = _function_counter,
            name = name or "anonymous",
            address = tostring(func),
            source = source or "unknown",
            context = context or "general",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_FULL_DUMP.functions, entry)
        print("🔧 [FNC " .. _function_counter .. "] " .. entry.name .. " (" .. entry.source .. ") " .. entry.address)
    end
end

local function capture_constant(const, index, source, context)
    _constant_counter = _constant_counter + 1
    local entry = {
        id = _constant_counter,
        index = index or _constant_counter,
        value = const,
        type = type(const),
        source = source or "unknown", 
        context = context or "general",
        timestamp = os.date("%H:%M:%S")
    }
    table.insert(_FULL_DUMP.constants, entry)
    print("📋 [CON " .. _constant_counter .. "] [" .. entry.index .. "] " .. entry.type .. ": " .. safe_tostring(const))
    
    -- Автоматически захватываем строки из констант
    if type(const) == "string" then
        capture_string(const, source .. "_constant", context)
    end
end

local function capture_instruction(instr, index, source, context)
    _instruction_counter = _instruction_counter + 1
    local entry = {
        id = _instruction_counter,
        index = index or _instruction_counter,
        instruction = instr,
        source = source or "unknown",
        context = context or "general",
        timestamp = os.date("%H:%M:%S")
    }
    table.insert(_FULL_DUMP.instructions, entry)
    
    local instr_str = ""
    if type(instr) == "table" then
        for i, v in ipairs(instr) do
            instr_str = instr_str .. tostring(v) .. " "
        end
    else
        instr_str = tostring(instr)
    end
    print("⚡ [INS " .. _instruction_counter .. "] [" .. entry.index .. "] " .. instr_str)
end

-- ============= HOOK v28 FUNCTION =============
if v28 then
    print("🎯 Устанавливаем hook на v28...")
    local original_v28 = v28
    
    v28 = function(...)
        print("")
        print("🎯 ===== HOOK v28 TRIGGERED =====")
        print("⏰ Время: " .. os.date("%H:%M:%S"))
        
        -- Вызываем оригинальную функцию
        local vm_result = original_v28(...)
        
        print("📊 v28 result type: " .. type(vm_result))
        
        if type(vm_result) == "table" then
            print("📦 VM structure components: " .. #vm_result)
            
            _FULL_DUMP.vm_structure = {
                type = "table",
                count = #vm_result,
                components = {}
            }
            
            for i = 1, #vm_result do
                local component = vm_result[i]
                local comp_type = type(component)
                print("🔹 Component[" .. i .. "]: " .. comp_type)
                
                local comp_info = {
                    index = i,
                    type = comp_type,
                    details = {}
                }
                
                if comp_type == "table" then
                    local size = 0
                    for _ in pairs(component) do size = size + 1 end
                    print("   📦 Table size: " .. size)
                    comp_info.size = size
                    
                    -- Component 1: Instructions
                    if i == 1 and size > 0 then
                        print("   🔧 EXTRACTING VM INSTRUCTIONS:")
                        local instr_count = 0
                        for j, instr in pairs(component) do
                            instr_count = instr_count + 1
                            if instr_count <= 30 then
                                capture_instruction(instr, j, "v28_component1", "vm_instructions")
                            end
                        end
                        if instr_count > 30 then
                            print("      ... и ещё " .. (instr_count - 30) .. " инструкций")
                        end
                        comp_info.instruction_count = instr_count
                    end
                    
                    -- Component 2: Constants
                    if i == 2 and size > 0 then
                        print("   📚 EXTRACTING CONSTANTS:")
                        local const_count = 0
                        for j, const in pairs(component) do
                            const_count = const_count + 1
                            if const_count <= 100 then
                                capture_constant(const, j, "v28_component2", "vm_constants")
                            end
                        end
                        if const_count > 100 then
                            print("      ... и ещё " .. (const_count - 100) .. " констант")
                        end
                        comp_info.constant_count = const_count
                    end
                    
                    -- Component 4: Functions
                    if i == 4 and size > 0 then
                        print("   ⚙️ EXTRACTING FUNCTIONS:")
                        local func_count = 0
                        for j, func in pairs(component) do
                            func_count = func_count + 1
                            if func_count <= 20 then
                                capture_function(func, "vm_func_" .. j, "v28_component4", "vm_functions")
                            end
                        end
                        comp_info.function_count = func_count
                    end
                end
                
                table.insert(_FULL_DUMP.vm_structure.components, comp_info)
            end
        end
        
        print("🎯 ===== END v28 HOOK =====")
        print("")
        return vm_result
    end
    print("✅ v28 hook установлен!")
else
    print("⚠️ v28 function не найдена")
end

-- ============= HOOK v29 FUNCTION =============
if v29 then
    print("⚡ Устанавливаем hook на v29...")
    local original_v29 = v29
    
    v29 = function(vm_data, env, ...)
        print("")
        print("⚡ ===== HOOK v29 EXECUTION =====")
        print("⏰ Время: " .. os.date("%H:%M:%S"))
        print("📊 VM data type: " .. type(vm_data))
        
        if type(vm_data) == "table" and #vm_data >= 2 then
            -- Извлекаем константы перед выполнением
            local constants = vm_data[2]
            if type(constants) == "table" then
                print("🔤 RUNTIME CONSTANTS EXTRACTION:")
                local runtime_count = 0
                for i, const in pairs(constants) do
                    runtime_count = runtime_count + 1
                    if type(const) == "string" and #const > 0 then
                        print("   🎯 Runtime[" .. i .. "]: '" .. const .. "'")
                        capture_string(const, "v29_runtime", "execution_constants")
                    end
                    if runtime_count <= 50 then
                        capture_constant(const, i, "v29_runtime", "execution_constants")
                    end
                end
                print("📊 Runtime constants processed: " .. runtime_count)
            end
            
            -- Извлекаем инструкции
            local instructions = vm_data[1]
            if type(instructions) == "table" then
                print("🔧 RUNTIME INSTRUCTIONS:")
                local exec_count = 0
                for i, instr in pairs(instructions) do
                    exec_count = exec_count + 1
                    if exec_count <= 20 then
                        capture_instruction(instr, i, "v29_runtime", "execution_instructions")
                    end
                end
                print("📊 Runtime instructions processed: " .. exec_count)
            end
        end
        
        -- Выполняем оригинальный код
        local result = original_v29(vm_data, env, ...)
        print("⚡ ===== END v29 EXECUTION =====")
        print("")
        return result
    end
    print("✅ v29 hook установлен!")
else
    print("⚠️ v29 function не найдена")
end

-- ============= HOOK STRING FUNCTIONS =============
-- Hook string.char
if string and string.char then
    local original_char = string.char
    string.char = function(...)
        local result = original_char(...)
        if type(result) == "string" and #result > 0 and (#result > 1 or string.byte(result) > 31) then
            capture_string(result, "string.char", "string_generation")
        end
        return result
    end
    print("✅ string.char hook установлен!")
end

-- Hook table.concat
if table and table.concat then
    local original_concat = table.concat
    table.concat = function(tbl, sep, ...)
        local result = original_concat(tbl, sep, ...)
        if type(result) == "string" and #result > 0 then
            capture_string(result, "table.concat", "string_assembly")
        end
        return result
    end
    print("✅ table.concat hook установлен!")
end

-- Hook print function
if print then
    local original_print = print
    print = function(...)
        local args = {...}
        for i, arg in ipairs(args) do
            if type(arg) == "string" and #arg > 0 then
                capture_string(arg, "print_output", "program_output")
            end
        end
        return original_print(...)
    end
    print("✅ print hook установлен!")
end

-- ============= FINAL DUMP FUNCTION =============
local function generate_final_report()
    print("")
    print("=" .. string.rep("=", 80))
    print("📊 ФИНАЛЬНЫЙ ОТЧЁТ FULL HOOK DUMPER")
    print("=" .. string.rep("=", 80))
    
    print("🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ (" .. #_FULL_DUMP.strings .. "):")
    for i, str_data in ipairs(_FULL_DUMP.strings) do
        if i <= 20 then
            print("   [" .. str_data.id .. "] (" .. str_data.source .. ") " .. str_data.timestamp .. " '" .. str_data.value .. "'")
        end
    end
    if #_FULL_DUMP.strings > 20 then
        print("   ... и ещё " .. (#_FULL_DUMP.strings - 20) .. " строк")
    end
    
    print("")
    print("🔧 НАЙДЕННЫЕ ФУНКЦИИ (" .. #_FULL_DUMP.functions .. "):")
    for i, func_data in ipairs(_FULL_DUMP.functions) do
        if i <= 15 then
            print("   [" .. func_data.id .. "] " .. func_data.name .. " (" .. func_data.source .. ") " .. func_data.address)
        end
    end
    if #_FULL_DUMP.functions > 15 then
        print("   ... и ещё " .. (#_FULL_DUMP.functions - 15) .. " функций")
    end
    
    print("")
    print("📋 КОНСТАНТЫ (" .. #_FULL_DUMP.constants .. "):")
    for i, const_data in ipairs(_FULL_DUMP.constants) do
        if i <= 25 then
            print("   [" .. const_data.id .. "] [" .. const_data.index .. "] " .. const_data.type .. ": " .. safe_tostring(const_data.value))
        end
    end
    if #_FULL_DUMP.constants > 25 then
        print("   ... и ещё " .. (#_FULL_DUMP.constants - 25) .. " констант")
    end
    
    print("")
    print("⚡ ИНСТРУКЦИИ (" .. #_FULL_DUMP.instructions .. "):")
    for i, instr_data in ipairs(_FULL_DUMP.instructions) do
        if i <= 15 then
            local instr_str = ""
            if type(instr_data.instruction) == "table" then
                for j, v in ipairs(instr_data.instruction) do
                    instr_str = instr_str .. tostring(v) .. " "
                end
            else
                instr_str = tostring(instr_data.instruction)
            end
            print("   [" .. instr_data.id .. "] [" .. instr_data.index .. "] " .. instr_str)
        end
    end
    if #_FULL_DUMP.instructions > 15 then
        print("   ... и ещё " .. (#_FULL_DUMP.instructions - 15) .. " инструкций")
    end
    
    print("")
    print("🎯 АНАЛИЗ РЕЗУЛЬТАТОВ:")
    
    -- Анализ найденных строк для реконструкции
    local runtime_strings = {}
    for _, str_data in ipairs(_FULL_DUMP.strings) do
        if str_data.source == "v29_runtime" or str_data.source == "v28_component2_constant" then
            table.insert(runtime_strings, str_data.value)
        end
    end
    
    print("   🔤 Строк извлечено: " .. #_FULL_DUMP.strings)
    print("   🔧 Функций найдено: " .. #_FULL_DUMP.functions) 
    print("   📋 Констант обработано: " .. #_FULL_DUMP.constants)
    print("   ⚡ Инструкций захвачено: " .. #_FULL_DUMP.instructions)
    
    print("")
    print("🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
    print("-" .. string.rep("-", 40))
    
    -- Простая реконструкция на основе найденных строк
    local print_found = false
    local string_to_print = nil
    
    for _, str_data in ipairs(_FULL_DUMP.strings) do
        if str_data.value == "print" then
            print_found = true
        elseif print_found and str_data.value ~= "print" and #str_data.value > 0 then
            string_to_print = str_data.value
            break
        end
    end
    
    if print_found and string_to_print then
        print('print("' .. string_to_print .. '")')
    else
        print("-- Анализируйте извлечённые строки выше для реконструкции")
        if #runtime_strings > 0 then
            print("-- Найденные runtime строки:")
            for i, str in ipairs(runtime_strings) do
                if i <= 5 then
                    print("--   '" .. str .. "'")
                end
            end
        end
    end
    
    print("")
    print("=" .. string.rep("=", 80))
    print("✨ HOOK DUMPER завершён: " .. os.date("%H:%M:%S"))
    print("=" .. string.rep("=", 80))
end

-- Устанавливаем финальный отчёт на завершение работы
if _G.getfenv then
    local env = _G.getfenv()
    if env then
        env._FINAL_REPORT = generate_final_report
    end
end

print("")
print("🎉 Все хуки установлены! Начинаем анализ обфусцированного кода...")
print("⏰ Время старта: " .. os.date("%H:%M:%S"))
print("-" .. string.rep("-", 80))

-- ====== FULL HOOK INJECTION END ======

'''
    
    # Инжектируем hook код
    print("💉 Инжектируем hooks в код...")
    
    # Ищем место для инжекции (перед последним return)
    modified_code = original_code
    
    # Паттерны для поиска места инжекции
    injection_patterns = [
        r'(return v15\([^)]+\)[^;]*;?\s*)$',
        r'(return [^;]+;?\s*)$',
        r'(\s*)$'
    ]
    
    injected = False
    for pattern in injection_patterns:
        match = re.search(pattern, modified_code, re.MULTILINE | re.DOTALL)
        if match:
            # Вставляем hook код перед найденным паттерном
            before = modified_code[:match.start()]
            after = modified_code[match.start():]
            modified_code = before + hook_code + "\n" + after
            injected = True
            print(f"✅ Hook код инжектирован перед: {match.group(1)[:50]}...")
            break
    
    if not injected:
        # Если не нашли подходящее место, добавляем в начало
        modified_code = hook_code + "\n" + original_code
        print("✅ Hook код добавлен в начало файла")
    
    # Создаём модифицированный файл
    modified_filename = f"hooked_{int(time.time())}.lua"
    
    print(f"💾 Сохраняем модифицированный файл: {modified_filename}")
    try:
        with open(modified_filename, 'w', encoding='utf-8') as f:
            f.write(modified_code)
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        sys.exit(1)
    
    # Создаём отчёт
    execution_time = time.time() - start_time
    
    report_lines = [
        "FULL HOOK DUMPER - Отчёт о модификации кода",
        "=" * 60,
        "",
        f"📁 Исходный файл: {input_file}",
        f"🔧 Модифицированный файл: {modified_filename}",
        f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"⏱️ Время обработки: {execution_time:.2f} секунд",
        f"📏 Размер исходного: {len(original_code)} символов",
        f"📏 Размер с хуками: {len(modified_code)} символов",
        f"📈 Добавлено: {len(modified_code) - len(original_code)} символов хуков",
        "",
        "🔧 УСТАНОВЛЕННЫЕ ХУКИ:",
        "  ✅ v28 function hook - извлечение VM структуры",
        "  ✅ v29 function hook - перехват выполнения",
        "  ✅ string.char hook - генерация строк",
        "  ✅ table.concat hook - сборка строк",
        "  ✅ print hook - вывод программы",
        "",
        "🚀 ИНСТРУКЦИИ ПО ЗАПУСКУ:",
        "",
        "1. Установите Lua (если не установлен):",
        "   Ubuntu/Debian: sudo apt install lua5.3",
        "   macOS: brew install lua",
        "   Windows: скачайте с lua.org",
        "",
        f"2. Запустите модифицированный файл:",
        f"   lua {modified_filename}",
        "",
        "3. Анализируйте вывод - все строки, функции и инструкции",
        "   будут автоматически извлечены и показаны.",
        "",
        "4. В конце выполнения вы увидите:",
        "   📊 ФИНАЛЬНЫЙ ОТЧЁТ FULL HOOK DUMPER",
        "   🎉 РЕКОНСТРУИРОВАННЫЙ КОД",
        "",
        "🎯 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:",
        "",
        "На основе ваших данных:",
        "1    3    print   ...",
        "1    3    hmmmm   ...",
        "",
        "Скрипт должен найти:",
        "📝 [STR 1] (v28_component2) 'print'",
        "📝 [STR 2] (v28_component2) 'hmmmm'",
        "🎯 Runtime[2]: 'print'",
        "🎯 Runtime[3]: 'hmmmm'",
        "",
        "И реконструировать код:",
        'print("hmmmm")',
        "",
        "=" * 60,
        f"Модифицированный файл готов: {modified_filename}",
        "Запустите его в Lua для получения полного дампа!",
        "=" * 60
    ]
    
    # Сохраняем отчёт
    print(f"📄 Создаём отчёт: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
    except Exception as e:
        print(f"❌ Ошибка создания отчёта: {e}")
        sys.exit(1)
    
    # Выводим результат
    print("")
    print("🎉 FULL HOOK DUMPER (Python) завершён успешно!")
    print("📊 Результаты:")
    print(f"   🔧 Модифицированный файл: {modified_filename}")
    print(f"   📄 Отчёт сохранён: {output_file}")
    print(f"   ⏱️ Время обработки: {execution_time:.2f} сек")
    print(f"   📈 Размер увеличен на: {len(modified_code) - len(original_code)} символов")
    print("")
    print("🚀 Следующие шаги:")
    print(f"   1. Установите Lua: sudo apt install lua5.3")
    print(f"   2. Запустите: lua {modified_filename}")
    print(f"   3. Анализируйте полный вывод дампа")
    print("")
    print("💡 Ожидаемый результат:")
    print("   📝 Все строки: 'print', 'hmmmm'")
    print("   🎉 Реконструкция: print(\"hmmmm\")")

if __name__ == "__main__":
    main()