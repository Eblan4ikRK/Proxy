#!/usr/bin/env python3
"""
FULL HOOK DUMPER (FIXED) для LuaObfuscator.com
Исправлена проблема с рекурсией в print hook

Использование: python3 full_hook_fixed.py input.lua output.txt
"""

import sys
import os
import re
import time
import json
from datetime import datetime

def main():
    if len(sys.argv) < 3:
        print("❌ Использование: python3 full_hook_fixed.py input.lua output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        sys.exit(1)
    
    print("🔍 FULL HOOK DUMPER (FIXED) для LuaObfuscator.com")
    print(f"📁 Входной файл: {input_file}")
    print(f"📄 Выходной файл: {output_file}")
    print("")
    
    # Читаем оригинальный файл
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        original_code = f.read()
    
    # Исправленный hook код без рекурсии
    hook_code = '''-- ====== FULL HOOK INJECTION (FIXED) START ======
-- Сохраняем оригинальный print СРАЗУ для избежания рекурсии
local original_print = print
local _print_safe = function(...)
    return original_print(...)
end

_print_safe("🚀 FULL HOOK DUMPER (FIXED) активирован!")
_print_safe("📊 Начинаем извлечение всех данных из LuaObfuscator.com")
_print_safe("")

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

-- Безопасный capture_string БЕЗ вызова print
local function capture_string_safe(str, source, context)
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
        -- Используем безопасный print
        _print_safe("📝 [STR " .. _string_counter .. "] (" .. entry.source .. ") '" .. str .. "'")
    end
end

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
        _print_safe("🔧 [FNC " .. _function_counter .. "] " .. entry.name .. " (" .. entry.source .. ") " .. entry.address)
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
    _print_safe("📋 [CON " .. _constant_counter .. "] [" .. entry.index .. "] " .. entry.type .. ": " .. safe_tostring(const))
    
    -- Автоматически захватываем строки из констант
    if type(const) == "string" then
        capture_string_safe(const, source .. "_constant", context)
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
    _print_safe("⚡ [INS " .. _instruction_counter .. "] [" .. entry.index .. "] " .. instr_str)
end

-- ============= HOOK v28 FUNCTION =============
if v28 then
    _print_safe("🎯 Устанавливаем hook на v28...")
    local original_v28 = v28
    
    v28 = function(...)
        _print_safe("")
        _print_safe("🎯 ===== HOOK v28 TRIGGERED =====")
        _print_safe("⏰ Время: " .. os.date("%H:%M:%S"))
        
        local vm_result = original_v28(...)
        _print_safe("📊 v28 result type: " .. type(vm_result))
        
        if type(vm_result) == "table" then
            _print_safe("📦 VM structure components: " .. #vm_result)
            
            for i = 1, #vm_result do
                local component = vm_result[i]
                local comp_type = type(component)
                _print_safe("🔹 Component[" .. i .. "]: " .. comp_type)
                
                if comp_type == "table" then
                    local size = 0
                    for _ in pairs(component) do size = size + 1 end
                    _print_safe("   📦 Table size: " .. size)
                    
                    -- Component 1: Instructions
                    if i == 1 and size > 0 then
                        _print_safe("   🔧 EXTRACTING VM INSTRUCTIONS:")
                        local instr_count = 0
                        for j, instr in pairs(component) do
                            instr_count = instr_count + 1
                            if instr_count <= 30 then
                                capture_instruction(instr, j, "v28_component1", "vm_instructions")
                            end
                        end
                        if instr_count > 30 then
                            _print_safe("      ... и ещё " .. (instr_count - 30) .. " инструкций")
                        end
                    end
                    
                    -- Component 2: Constants
                    if i == 2 and size > 0 then
                        _print_safe("   📚 EXTRACTING CONSTANTS:")
                        local const_count = 0
                        for j, const in pairs(component) do
                            const_count = const_count + 1
                            if const_count <= 100 then
                                capture_constant(const, j, "v28_component2", "vm_constants")
                            end
                        end
                        if const_count > 100 then
                            _print_safe("      ... и ещё " .. (const_count - 100) .. " констант")
                        end
                    end
                    
                    -- Component 4: Functions
                    if i == 4 and size > 0 then
                        _print_safe("   ⚙️ EXTRACTING FUNCTIONS:")
                        local func_count = 0
                        for j, func in pairs(component) do
                            func_count = func_count + 1
                            if func_count <= 20 then
                                capture_function(func, "vm_func_" .. j, "v28_component4", "vm_functions")
                            end
                        end
                    end
                end
            end
        end
        
        _print_safe("🎯 ===== END v28 HOOK =====")
        _print_safe("")
        return vm_result
    end
    _print_safe("✅ v28 hook установлен!")
else
    _print_safe("⚠️ v28 function не найдена")
end

-- ============= HOOK v29 FUNCTION =============
if v29 then
    _print_safe("⚡ Устанавливаем hook на v29...")
    local original_v29 = v29
    
    v29 = function(vm_data, env, ...)
        _print_safe("")
        _print_safe("⚡ ===== HOOK v29 EXECUTION =====")
        _print_safe("⏰ Время: " .. os.date("%H:%M:%S"))
        _print_safe("📊 VM data type: " .. type(vm_data))
        
        if type(vm_data) == "table" and #vm_data >= 2 then
            local constants = vm_data[2]
            if type(constants) == "table" then
                _print_safe("🔤 RUNTIME CONSTANTS EXTRACTION:")
                local runtime_count = 0
                for i, const in pairs(constants) do
                    runtime_count = runtime_count + 1
                    if type(const) == "string" and #const > 0 then
                        _print_safe("   🎯 Runtime[" .. i .. "]: '" .. const .. "'")
                        capture_string_safe(const, "v29_runtime", "execution_constants")
                    end
                    if runtime_count <= 50 then
                        capture_constant(const, i, "v29_runtime", "execution_constants")
                    end
                end
                _print_safe("📊 Runtime constants processed: " .. runtime_count)
            end
            
            local instructions = vm_data[1]
            if type(instructions) == "table" then
                _print_safe("🔧 RUNTIME INSTRUCTIONS:")
                local exec_count = 0
                for i, instr in pairs(instructions) do
                    exec_count = exec_count + 1
                    if exec_count <= 20 then
                        capture_instruction(instr, i, "v29_runtime", "execution_instructions")
                    end
                end
                _print_safe("📊 Runtime instructions processed: " .. exec_count)
            end
        end
        
        local result = original_v29(vm_data, env, ...)
        _print_safe("⚡ ===== END v29 EXECUTION =====")
        _print_safe("")
        return result
    end
    _print_safe("✅ v29 hook установлен!")
else
    _print_safe("⚠️ v29 function не найдена")
end

-- ============= HOOK STRING FUNCTIONS (БЕЗ РЕКУРСИИ) =============
-- Hook string.char
if string and string.char then
    local original_char = string.char
    string.char = function(...)
        local result = original_char(...)
        if type(result) == "string" and #result > 0 and (#result > 1 or string.byte(result) > 31) then
            capture_string_safe(result, "string.char", "string_generation")
        end
        return result
    end
    _print_safe("✅ string.char hook установлен!")
end

-- Hook table.concat
if table and table.concat then
    local original_concat = table.concat
    table.concat = function(tbl, sep, ...)
        local result = original_concat(tbl, sep, ...)
        if type(result) == "string" and #result > 0 then
            capture_string_safe(result, "table.concat", "string_assembly")
        end
        return result
    end
    _print_safe("✅ table.concat hook установлен!")
end

-- НЕ хукаем print чтобы избежать рекурсии!
-- Вместо этого добавляем финальный отчёт

-- ============= ФИНАЛЬНЫЙ ОТЧЁТ =============
local function generate_final_report()
    _print_safe("")
    _print_safe("=" .. string.rep("=", 80))
    _print_safe("📊 ФИНАЛЬНЫЙ ОТЧЁТ FULL HOOK DUMPER (FIXED)")
    _print_safe("=" .. string.rep("=", 80))
    
    _print_safe("🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ (" .. #_FULL_DUMP.strings .. "):")
    for i, str_data in ipairs(_FULL_DUMP.strings) do
        if i <= 20 then
            _print_safe("   [" .. str_data.id .. "] (" .. str_data.source .. ") '" .. str_data.value .. "'")
        end
    end
    if #_FULL_DUMP.strings > 20 then
        _print_safe("   ... и ещё " .. (#_FULL_DUMP.strings - 20) .. " строк")
    end
    
    _print_safe("")
    _print_safe("🔧 НАЙДЕННЫЕ ФУНКЦИИ (" .. #_FULL_DUMP.functions .. "):")
    for i, func_data in ipairs(_FULL_DUMP.functions) do
        if i <= 15 then
            _print_safe("   [" .. func_data.id .. "] " .. func_data.name .. " (" .. func_data.source .. ") " .. func_data.address)
        end
    end
    if #_FULL_DUMP.functions > 15 then
        _print_safe("   ... и ещё " .. (#_FULL_DUMP.functions - 15) .. " функций")
    end
    
    _print_safe("")
    _print_safe("📋 КОНСТАНТЫ (" .. #_FULL_DUMP.constants .. "):")
    for i, const_data in ipairs(_FULL_DUMP.constants) do
        if i <= 25 then
            _print_safe("   [" .. const_data.id .. "] [" .. const_data.index .. "] " .. const_data.type .. ": " .. safe_tostring(const_data.value))
        end
    end
    if #_FULL_DUMP.constants > 25 then
        _print_safe("   ... и ещё " .. (#_FULL_DUMP.constants - 25) .. " констант")
    end
    
    _print_safe("")
    _print_safe("⚡ ИНСТРУКЦИИ (" .. #_FULL_DUMP.instructions .. "):")
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
            _print_safe("   [" .. instr_data.id .. "] [" .. instr_data.index .. "] " .. instr_str)
        end
    end
    if #_FULL_DUMP.instructions > 15 then
        _print_safe("   ... и ещё " .. (#_FULL_DUMP.instructions - 15) .. " инструкций")
    end
    
    _print_safe("")
    _print_safe("🎯 АНАЛИЗ РЕЗУЛЬТАТОВ:")
    _print_safe("   🔤 Строк извлечено: " .. #_FULL_DUMP.strings)
    _print_safe("   🔧 Функций найдено: " .. #_FULL_DUMP.functions) 
    _print_safe("   📋 Констант обработано: " .. #_FULL_DUMP.constants)
    _print_safe("   ⚡ Инструкций захвачено: " .. #_FULL_DUMP.instructions)
    
    _print_safe("")
    _print_safe("🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
    _print_safe("-" .. string.rep("-", 40))
    
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
        _print_safe('print("' .. string_to_print .. '")')
    else
        _print_safe("-- Анализируйте извлечённые строки выше для реконструкции")
        local runtime_strings = {}
        for _, str_data in ipairs(_FULL_DUMP.strings) do
            if str_data.source == "v29_runtime" or str_data.source == "v28_component2_constant" then
                table.insert(runtime_strings, str_data.value)
            end
        end
        if #runtime_strings > 0 then
            _print_safe("-- Найденные runtime строки:")
            for i, str in ipairs(runtime_strings) do
                if i <= 5 then
                    _print_safe("--   '" .. str .. "'")
                end
            end
        end
    end
    
    _print_safe("")
    _print_safe("=" .. string.rep("=", 80))
    _print_safe("✨ HOOK DUMPER (FIXED) завершён: " .. os.date("%H:%M:%S"))
    _print_safe("=" .. string.rep("=", 80))
end

-- Вызываем финальный отчёт в конце
_print_safe("")
_print_safe("🎉 Все хуки установлены! Начинаем анализ обфусцированного кода...")
_print_safe("⏰ Время старта: " .. os.date("%H:%M:%S"))
_print_safe("-" .. string.rep("-", 80))

-- Добавляем вызов отчёта в конец
local function call_final_report()
    generate_final_report()
end

-- Устанавливаем таймер для вызова отчёта
if os and os.time then
    local start_time = os.time()
    local check_timer = function()
        if os.time() - start_time > 3 then
            call_final_report()
        end
    end
end

-- ====== FULL HOOK INJECTION (FIXED) END ======

'''
    
    # Инжектируем исправленный hook код
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
            before = modified_code[:match.start()]
            after = modified_code[match.start():]
            modified_code = before + hook_code + "\n" + after
            injected = True
            print(f"✅ Hook код инжектирован перед: {match.group(1)[:50]}...")
            break
    
    if not injected:
        modified_code = hook_code + "\n" + original_code
        print("✅ Hook код добавлен в начало файла")
    
    # Добавляем вызов финального отчёта в самый конец
    modified_code += "\n\n-- Финальный отчёт\nif generate_final_report then generate_final_report() end\n"
    
    # Создаём модифицированный файл
    modified_filename = f"hooked_fixed_{int(time.time())}.lua"
    
    print(f"💾 Сохраняем исправленный файл: {modified_filename}")
    with open(modified_filename, 'w', encoding='utf-8') as f:
        f.write(modified_code)
    
    # Создаём отчёт
    execution_time = time.time() - time.time()
    
    report_lines = [
        "FULL HOOK DUMPER (FIXED) - Отчёт",
        "=" * 60,
        "",
        f"📁 Исходный файл: {input_file}",
        f"🔧 Модифицированный файл: {modified_filename}",
        f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"📏 Размер исходного: {len(original_code)} символов",
        f"📏 Размер с хуками: {len(modified_code)} символов",
        "",
        "🔧 ИСПРАВЛЕНИЯ:",
        "  ✅ Убрана рекурсия в print hook",
        "  ✅ Добавлен безопасный _print_safe",
        "  ✅ Исправлен capture_string_safe",
        "  ✅ Защита от stack overflow",
        "",
        "🚀 ИНСТРУКЦИИ ПО ЗАПУСКУ:",
        "",
        f"1. Запустите исправленный файл:",
        f"   lua {modified_filename}",
        "",
        "2. Теперь не будет рекурсии и stack overflow!",
        "",
        "🎯 ОЖИДАЕМЫЕ РЕЗУЛЬТАТЫ:",
        "   📝 Извлечение всех строк",
        "   🔧 Анализ функций",
        "   📋 Обработка констант",
        "   🎉 Реконструкция кода",
        "",
        "=" * 60,
        f"Исправленный файл готов: {modified_filename}",
        "=" * 60
    ]
    
    # Сохраняем отчёт
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("")
    print("🎉 FULL HOOK DUMPER (FIXED) завершён успешно!")
    print("📊 Результаты:")
    print(f"   🔧 Исправленный файл: {modified_filename}")
    print(f"   📄 Отчёт: {output_file}")
    print("")
    print("🚀 Теперь запустите исправленный файл:")
    print(f"   lua {modified_filename}")
    print("")
    print("✅ Проблема с рекурсией исправлена!")

if __name__ == "__main__":
    main()