#!/usr/bin/env lua
--[[
FULL HOOK DUMPER для LuaObfuscator.com
Полный дамп всех строк, функций, VM инструкций и данных

Использование: lua full_hook.lua input.lua output.txt
Автор: Deobfuscation Framework
]]--

-- Проверка аргументов командной строки
if #arg < 2 then
    print("❌ Использование: lua full_hook.lua input.lua output.txt")
    print("   input.lua  - обфусцированный файл")
    print("   output.txt - файл для сохранения результатов")
    os.exit(1)
end

local input_file = arg[1]
local output_file = arg[2]

-- Проверка существования входного файла
local file = io.open(input_file, "r")
if not file then
    print("❌ Ошибка: Файл " .. input_file .. " не найден!")
    os.exit(1)
end
file:close()

print("🔍 FULL HOOK DUMPER для LuaObfuscator.com")
print("📁 Входной файл: " .. input_file)
print("📄 Выходной файл: " .. output_file)
print("")

-- Глобальные переменные для сбора данных
local dump_data = {
    strings = {},
    functions = {},
    vm_instructions = {},
    constants = {},
    opcodes = {},
    call_stack = {},
    variable_assignments = {},
    function_calls = {},
    start_time = os.time()
}

-- Счетчики
local counters = {
    strings_found = 0,
    functions_hooked = 0,
    instructions_captured = 0,
    calls_traced = 0
}

-- Утилиты для логирования
local function log(message)
    table.insert(dump_data.call_stack, os.date("%H:%M:%S") .. " | " .. tostring(message))
    print("🔍 " .. message)
end

local function dump_table_safe(tbl, max_depth, current_depth)
    current_depth = current_depth or 0
    max_depth = max_depth or 3
    
    if current_depth > max_depth then
        return "[MAX_DEPTH_REACHED]"
    end
    
    if type(tbl) ~= "table" then
        return tostring(tbl)
    end
    
    local result = "{"
    local count = 0
    for k, v in pairs(tbl) do
        count = count + 1
        if count > 10 then
            result = result .. ", ..."
            break
        end
        
        local key_str = tostring(k)
        local val_str
        
        if type(v) == "table" then
            val_str = dump_table_safe(v, max_depth, current_depth + 1)
        elseif type(v) == "string" then
            val_str = '"' .. v .. '"'
        elseif type(v) == "function" then
            val_str = "function"
        else
            val_str = tostring(v)
        end
        
        result = result .. key_str .. "=" .. val_str
        if count > 1 then result = "," .. result end
    end
    result = result .. "}"
    return result
end

local function save_string(str, context)
    if type(str) == "string" and #str > 0 then
        counters.strings_found = counters.strings_found + 1
        table.insert(dump_data.strings, {
            id = counters.strings_found,
            value = str,
            length = #str,
            context = context,
            timestamp = os.date("%H:%M:%S")
        })
        log("STRING [" .. counters.strings_found .. "] (" .. context .. "): '" .. str .. "'")
    end
end

local function save_function_info(func, name, context)
    if type(func) == "function" then
        counters.functions_hooked = counters.functions_hooked + 1
        table.insert(dump_data.functions, {
            id = counters.functions_hooked,
            name = name or "anonymous",
            address = tostring(func),
            context = context,
            timestamp = os.date("%H:%M:%S")
        })
        log("FUNCTION [" .. counters.functions_hooked .. "] " .. (name or "anonymous") .. " (" .. context .. "): " .. tostring(func))
    end
end

-- Читаем оригинальный файл
log("Читаем обфусцированный файл...")
local original_code = ""
local file = io.open(input_file, "r")
if file then
    original_code = file:read("*all")
    file:close()
else
    print("❌ Не удалось прочитать файл!")
    os.exit(1)
end

-- Инжектируем хуки в код
log("Инжектируем хуки для полного дампа...")

local hook_code = [[
-- FULL HOOK INJECTION START
print("🚀 Хуки активированы! Начинаем полный дамп...")

-- Глобальные переменные для дампа
_DUMP_STRINGS = {}
_DUMP_FUNCTIONS = {}
_DUMP_CONSTANTS = {}
_DUMP_INSTRUCTIONS = {}
_STRING_COUNTER = 0
_FUNC_COUNTER = 0

-- Функция для безопасного дампа таблиц
local function safe_dump(obj, max_depth, current_depth)
    current_depth = current_depth or 0
    max_depth = max_depth or 2
    
    if current_depth > max_depth then return "[DEEP]" end
    if type(obj) ~= "table" then return tostring(obj) end
    
    local result = "{"
    local count = 0
    for k, v in pairs(obj) do
        count = count + 1
        if count > 5 then result = result .. ",..."; break end
        if count > 1 then result = result .. "," end
        result = result .. tostring(k) .. "="
        if type(v) == "table" then
            result = result .. safe_dump(v, max_depth, current_depth + 1)
        elseif type(v) == "string" then
            result = result .. '"' .. v .. '"'
        else
            result = result .. tostring(v)
        end
    end
    return result .. "}"
end

-- Функция для сохранения строк
local function capture_string(str, context)
    if type(str) == "string" and #str > 0 then
        _STRING_COUNTER = _STRING_COUNTER + 1
        _DUMP_STRINGS[_STRING_COUNTER] = {str, context, os.date("%H:%M:%S")}
        print("📝 STRING[" .. _STRING_COUNTER .. "] (" .. (context or "unknown") .. "): '" .. str .. "'")
    end
end

-- Функция для сохранения функций
local function capture_function(func, name, context)
    if type(func) == "function" then
        _FUNC_COUNTER = _FUNC_COUNTER + 1
        _DUMP_FUNCTIONS[_FUNC_COUNTER] = {tostring(func), name or "anonymous", context or "unknown", os.date("%H:%M:%S")}
        print("🔧 FUNCTION[" .. _FUNC_COUNTER .. "] " .. (name or "anonymous") .. " (" .. (context or "unknown") .. "): " .. tostring(func))
    end
end

-- ========== ХУКИНГ v28 ФУНКЦИИ ==========
if v28 then
    local original_v28 = v28
    v28 = function(...)
        print("🎯 === HOOKING v28 FUNCTION ===")
        local vm_structure = original_v28(...)
        
        print("📊 VM Structure type:", type(vm_structure))
        
        if type(vm_structure) == "table" then
            print("📋 VM Components count:", #vm_structure)
            
            for i = 1, #vm_structure do
                local component = vm_structure[i]
                print("🔹 Component[" .. i .. "] type: " .. type(component))
                
                if type(component) == "table" then
                    local comp_size = 0
                    for _ in pairs(component) do comp_size = comp_size + 1 end
                    print("   📦 Table size: " .. comp_size)
                    
                    -- Инструкции VM (обычно первый компонент)
                    if i == 1 and comp_size > 0 then
                        print("   🔧 VM INSTRUCTIONS:")
                        local instr_count = 0
                        for j, instr in pairs(component) do
                            instr_count = instr_count + 1
                            if instr_count <= 20 then  -- Показываем первые 20 инструкций
                                if type(instr) == "table" then
                                    local instr_str = ""
                                    for k, v in ipairs(instr) do
                                        instr_str = instr_str .. tostring(v) .. " "
                                    end
                                    print("      [" .. j .. "] " .. instr_str:trim())
                                    _DUMP_INSTRUCTIONS[#_DUMP_INSTRUCTIONS + 1] = {j, instr_str:trim(), "vm_instruction"}
                                else
                                    print("      [" .. j .. "] " .. tostring(instr))
                                    _DUMP_INSTRUCTIONS[#_DUMP_INSTRUCTIONS + 1] = {j, tostring(instr), "vm_single"}
                                end
                            end
                        end
                        if instr_count > 20 then
                            print("      ... и ещё " .. (instr_count - 20) .. " инструкций")
                        end
                    end
                    
                    -- Константы (обычно второй компонент)
                    if i == 2 and comp_size > 0 then
                        print("   📚 CONSTANTS TABLE:")
                        local const_count = 0
                        for j, const in pairs(component) do
                            const_count = const_count + 1
                            if const_count <= 50 then  -- Показываем первые 50 констант
                                local const_type = type(const)
                                print("      [" .. j .. "] " .. const_type .. ": " .. tostring(const))
                                
                                -- Сохраняем строковые константы
                                if const_type == "string" then
                                    capture_string(const, "vm_constant")
                                end
                                
                                _DUMP_CONSTANTS[#_DUMP_CONSTANTS + 1] = {j, const, const_type, "vm_constant"}
                            end
                        end
                        if const_count > 50 then
                            print("      ... и ещё " .. (const_count - 50) .. " констант")
                        end
                    end
                    
                    -- Функции (обычно четвертый компонент)
                    if i == 4 and comp_size > 0 then
                        print("   ⚙️  FUNCTIONS TABLE:")
                        local func_count = 0
                        for j, func in pairs(component) do
                            func_count = func_count + 1
                            if func_count <= 10 then
                                capture_function(func, "vm_function_" .. j, "vm_functions")
                            end
                        end
                    end
                end
            end
        end
        
        print("🎯 === END v28 HOOK ===")
        return vm_structure
    end
    print("✅ v28 function hooked!")
end

-- ========== ХУКИНГ v29 ФУНКЦИИ ==========
if v29 then
    local original_v29 = v29
    v29 = function(vm_data, env, ...)
        print("⚡ === HOOKING v29 EXECUTION ===")
        print("📊 VM Data type:", type(vm_data))
        
        if type(vm_data) == "table" and #vm_data >= 2 then
            local constants = vm_data[2]
            if type(constants) == "table" then
                print("🔤 RUNTIME STRINGS EXTRACTION:")
                local string_count = 0
                for i, const in pairs(constants) do
                    if type(const) == "string" and #const > 0 then
                        string_count = string_count + 1
                        print("   🎯 Runtime[" .. i .. "]: '" .. const .. "'")
                        capture_string(const, "runtime_execution")
                    end
                end
                print("📊 Total runtime strings found: " .. string_count)
            end
            
            -- Дампим инструкции перед выполнением
            local instructions = vm_data[1]
            if type(instructions) == "table" then
                print("🔧 EXECUTION INSTRUCTIONS:")
                local exec_count = 0
                for i, instr in pairs(instructions) do
                    exec_count = exec_count + 1
                    if exec_count <= 10 then
                        if type(instr) == "table" then
                            local instr_dump = safe_dump(instr)
                            print("   ⚡ Exec[" .. i .. "]: " .. instr_dump)
                        end
                    end
                end
            end
        end
        
        local result = original_v29(vm_data, env, ...)
        print("⚡ === END v29 EXECUTION ===")
        return result
    end
    print("✅ v29 function hooked!")
end

-- ========== ХУКИНГ СТРОКОВЫХ ФУНКЦИЙ ==========
-- Хук string.char для отслеживания генерации строк
if string and string.char then
    local original_char = string.char
    string.char = function(...)
        local args = {...}
        local result = original_char(...)
        if #result > 0 and (#result > 1 or string.byte(result) > 31) then
            capture_string(result, "string.char")
        end
        return result
    end
    print("✅ string.char hooked!")
end

-- Хук table.concat для отслеживания сборки строк
if table and table.concat then
    local original_concat = table.concat
    table.concat = function(tbl, sep, ...)
        local result = original_concat(tbl, sep, ...)
        if type(result) == "string" and #result > 0 then
            capture_string(result, "table.concat")
        end
        return result
    end
    print("✅ table.concat hooked!")
end

-- Хук print для отслеживания вывода
if print then
    local original_print = print
    print = function(...)
        local args = {...}
        for i, arg in ipairs(args) do
            if type(arg) == "string" then
                capture_string(arg, "print_output")
            end
        end
        return original_print(...)
    end
    print("✅ print function hooked!")
end

-- ========== ФИНАЛЬНЫЙ ДАМП ==========
local function final_dump()
    print("\n" .. "="*80)
    print("📊 ФИНАЛЬНЫЙ ОТЧЁТ FULL HOOK DUMPER")
    print("="*80)
    
    print("🔤 НАЙДЕНО СТРОК: " .. #_DUMP_STRINGS)
    for i, str_data in ipairs(_DUMP_STRINGS) do
        print("   [" .. i .. "] (" .. str_data[2] .. ") " .. str_data[3] .. ": '" .. str_data[1] .. "'")
    end
    
    print("\n🔧 НАЙДЕНО ФУНКЦИЙ: " .. #_DUMP_FUNCTIONS)
    for i, func_data in ipairs(_DUMP_FUNCTIONS) do
        print("   [" .. i .. "] " .. func_data[2] .. " (" .. func_data[3] .. ") " .. func_data[4] .. ": " .. func_data[1])
    end
    
    print("\n📋 НАЙДЕНО КОНСТАНТ: " .. #_DUMP_CONSTANTS)
    for i, const_data in ipairs(_DUMP_CONSTANTS) do
        if i <= 20 then  -- Показываем первые 20
            print("   [" .. const_data[1] .. "] " .. const_data[3] .. ": " .. tostring(const_data[2]))
        end
    end
    if #_DUMP_CONSTANTS > 20 then
        print("   ... и ещё " .. (#_DUMP_CONSTANTS - 20) .. " констант")
    end
    
    print("\n⚡ НАЙДЕНО ИНСТРУКЦИЙ: " .. #_DUMP_INSTRUCTIONS)
    for i, instr_data in ipairs(_DUMP_INSTRUCTIONS) do
        if i <= 15 then  -- Показываем первые 15
            print("   [" .. instr_data[1] .. "] " .. instr_data[2])
        end
    end
    if #_DUMP_INSTRUCTIONS > 15 then
        print("   ... и ещё " .. (#_DUMP_INSTRUCTIONS - 15) .. " инструкций")
    end
    
    print("\n🎯 РЕЗЮМЕ:")
    print("   Строк извлечено: " .. #_DUMP_STRINGS)
    print("   Функций найдено: " .. #_DUMP_FUNCTIONS)
    print("   Констант обработано: " .. #_DUMP_CONSTANTS)
    print("   Инструкций захвачено: " .. #_DUMP_INSTRUCTIONS)
    print("="*80)
end

-- Устанавливаем финальный дамп на завершение
if os and os.exit then
    local original_exit = os.exit
    os.exit = function(...)
        final_dump()
        return original_exit(...)
    end
end

print("🎉 Все хуки установлены! Запускаем обфусцированный код...")
print("-"*60)

-- FULL HOOK INJECTION END
]]

-- Добавляем hook_code перед последней строкой return
local modified_code = original_code:gsub("(return v15%([^)]+%)%;?)$", hook_code .. "\n%1")

-- Если паттерн не сработал, добавляем в конец
if modified_code == original_code then
    modified_code = hook_code .. "\n" .. original_code
end

-- Сохраняем модифицированный код во временный файл
local temp_file = "temp_hooked_" .. os.time() .. ".lua"
local file = io.open(temp_file, "w")
if file then
    file:write(modified_code)
    file:close()
    log("Модифицированный код сохранён в " .. temp_file)
else
    print("❌ Не удалось создать временный файл!")
    os.exit(1)
end

-- Выполняем модифицированный код и перехватываем вывод
log("Запускаем код с полными хуками...")

local handle = io.popen("lua " .. temp_file .. " 2>&1")
local execution_output = ""
if handle then
    execution_output = handle:read("*all")
    handle:close()
else
    print("❌ Не удалось запустить код!")
    os.exit(1)
end

-- Удаляем временный файл
os.remove(temp_file)

-- Обрабатываем вывод и извлекаем данные
log("Обрабатываем результаты выполнения...")

local strings_found = {}
local functions_found = {}
local constants_found = {}
local instructions_found = {}

-- Парсим вывод выполнения
for line in execution_output:gmatch("[^\r\n]+") do
    -- Ищем строки
    local str_match = line:match("📝 STRING%[(%d+)%] %(([^)]+)%): '([^']*)'")
    if str_match then
        local id, context, value = line:match("📝 STRING%[(%d+)%] %(([^)]+)%): '([^']*)'")
        if id and context and value then
            table.insert(strings_found, {
                id = tonumber(id),
                context = context,
                value = value,
                length = #value
            })
        end
    end
    
    -- Ищем функции
    local func_match = line:match("🔧 FUNCTION%[(%d+)%] ([^%(]+) %(([^)]+)%): (.*)")
    if func_match then
        local id, name, context, address = line:match("🔧 FUNCTION%[(%d+)%] ([^%(]+) %(([^)]+)%): (.*)")
        if id and name and context and address then
            table.insert(functions_found, {
                id = tonumber(id),
                name = name,
                context = context,
                address = address
            })
        end
    end
    
    -- Ищем runtime строки
    local runtime_match = line:match("🎯 Runtime%[(%d+)%]: '([^']*)'")
    if runtime_match then
        local id, value = line:match("🎯 Runtime%[(%d+)%]: '([^']*)'")
        if id and value then
            table.insert(strings_found, {
                id = "runtime_" .. id,
                context = "runtime",
                value = value,
                length = #value
            })
        end
    end
end

-- Формируем финальный отчёт
local report = {
    "FULL HOOK DUMPER - Полный отчёт деобфускации",
    "=" .. string.rep("=", 60),
    "",
    "📁 Входной файл: " .. input_file,
    "📅 Дата анализа: " .. os.date("%Y-%m-%d %H:%M:%S"),
    "⏱️  Время выполнения: " .. (os.time() - dump_data.start_time) .. " секунд",
    "",
    "🎯 РЕЗУЛЬТАТЫ ДЕОБФУСКАЦИИ:",
    "   • Строк найдено: " .. #strings_found,
    "   • Функций найдено: " .. #functions_found,
    "   • Констант обработано: " .. #constants_found,
    "",
    "🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ:",
    "-" .. string.rep("-", 40)
}

-- Добавляем найденные строки
for i, str_data in ipairs(strings_found) do
    table.insert(report, string.format("[%s] (%s) Length:%d - '%s'", 
        tostring(str_data.id), str_data.context, str_data.length, str_data.value))
end

table.insert(report, "")
table.insert(report, "🔧 НАЙДЕННЫЕ ФУНКЦИИ:")
table.insert(report, "-" .. string.rep("-", 40))

-- Добавляем найденные функции
for i, func_data in ipairs(functions_found) do
    table.insert(report, string.format("[%d] %s (%s) - %s", 
        func_data.id, func_data.name, func_data.context, func_data.address))
end

table.insert(report, "")
table.insert(report, "📋 ПОЛНЫЙ ВЫВОД ВЫПОЛНЕНИЯ:")
table.insert(report, "-" .. string.rep("-", 60))
table.insert(report, execution_output)

table.insert(report, "")
table.insert(report, "🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
table.insert(report, "-" .. string.rep("-", 40))

-- Пытаемся реконструировать оригинальный код
local reconstructed = {}
for i, str_data in ipairs(strings_found) do
    if str_data.context == "runtime" or str_data.context == "vm_constant" then
        if str_data.value == "print" then
            -- Находим следующую строку как аргумент
            for j, next_str in ipairs(strings_found) do
                if j > i and next_str.value ~= "print" and #next_str.value > 0 then
                    table.insert(reconstructed, 'print("' .. next_str.value .. '")')
                    break
                end
            end
        end
    end
end

if #reconstructed > 0 then
    for i, line in ipairs(reconstructed) do
        table.insert(report, line)
    end
else
    table.insert(report, "-- Не удалось автоматически реконструировать код")
    table.insert(report, "-- Проанализируйте извлечённые строки выше")
end

table.insert(report, "")
table.insert(report, "=" .. string.rep("=", 60))
table.insert(report, "Отчёт создан: " .. os.date("%Y-%m-%d %H:%M:%S"))

-- Сохраняем отчёт в файл
local output = io.open(output_file, "w")
if output then
    output:write(table.concat(report, "\n"))
    output:close()
    log("Отчёт сохранён в " .. output_file)
else
    print("❌ Не удалось сохранить отчёт!")
    os.exit(1)
end

-- Выводим краткий результат
print("")
print("🎉 FULL HOOK DUMPER завершён успешно!")
print("📊 Результаты:")
print("   • Строк извлечено: " .. #strings_found)
print("   • Функций найдено: " .. #functions_found)
print("   • Отчёт сохранён в: " .. output_file)

if #strings_found > 0 then
    print("")
    print("🔍 Найденные строки:")
    for i, str_data in ipairs(strings_found) do
        if i <= 5 then  -- Показываем первые 5
            print("   " .. i .. ". '" .. str_data.value .. "' (" .. str_data.context .. ")")
        end
    end
    if #strings_found > 5 then
        print("   ... и ещё " .. (#strings_found - 5) .. " строк (см. в отчёте)")
    end
end

print("")
print("📄 Полный отчёт смотрите в файле: " .. output_file)