-- RUNTIME EXTRACTION SCRIPT для LuaObfuscator.com
-- Вставьте этот код ПЕРЕД последней строкой return v15(...)

print("🔍 Начинаем извлечение данных из обфусцированного скрипта...")

-- Перехватываем функцию v28
local original_v28 = v28
local extracted_data = {}

local function debug_v28()
    print("=== ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ V28 ===")
    
    -- Вызываем оригинальную функцию
    local vm_structure = original_v28()
    
    print("Тип результата v28:", type(vm_structure))
    
    if type(vm_structure) == "table" then
        print("Компоненты VM структуры:")
        
        for i = 1, #vm_structure do
            local component = vm_structure[i]
            print(f"  Компонент [{i}]: {type(component)}")
            
            if type(component) == "table" then
                print(f"    Размер таблицы: {#component}")
                
                -- Если это таблица инструкций
                if i == 1 and #component > 0 then
                    print("    ИНСТРУКЦИИ ВИРТУАЛЬНОЙ МАШИНЫ:")
                    for j = 1, math.min(#component, 10) do
                        local instr = component[j]
                        if type(instr) == "table" then
                            local instr_str = ""
                            for k = 1, #instr do
                                instr_str = instr_str .. tostring(instr[k]) .. " "
                            end
                            print(f"      Инструкция {j}: {instr_str}")
                        else
                            print(f"      Инструкция {j}: {instr}")
                        end
                    end
                    if #component > 10 then
                        print(f"      ... ещё {#component - 10} инструкций")
                    end
                end
                
                -- Если это таблица констант  
                if i == 2 and #component > 0 then
                    print("    КОНСТАНТЫ:")
                    for j = 1, math.min(#component, 20) do
                        local const = component[j]
                        print(f"      Константа {j}: {const} (тип: {type(const)})")
                        
                        -- Сохраняем строковые константы
                        if type(const) == "string" then
                            table.insert(extracted_data, {
                                type = "string_constant",
                                index = j,
                                value = const
                            })
                        end
                    end
                    if #component > 20 then
                        print(f"      ... ещё {#component - 20} констант")
                    end
                end
                
                -- Если это таблица функций
                if i == 4 and #component > 0 then
                    print("    ФУНКЦИИ:")
                    for j = 1, math.min(#component, 5) do
                        local func = component[j]
                        print(f"      Функция {j}: {type(func)}")
                    end
                end
            end
        end
    end
    
    print("=== КОНЕЦ ИЗВЛЕЧЕНИЯ ИЗ V28 ===")
    return vm_structure
end

-- Заменяем v28
v28 = debug_v28

-- Перехватываем v29 для анализа выполнения
local original_v29 = v29
v29 = function(vm_data, env, ...)
    print("=== ВЫПОЛНЕНИЕ ВИРТУАЛЬНОЙ МАШИНЫ ===")
    
    -- Показываем данные перед выполнением
    if type(vm_data) == "table" and #vm_data >= 2 then
        local constants = vm_data[2]
        if type(constants) == "table" then
            print("СТРОКОВЫЕ КОНСТАНТЫ НАЙДЕНЫ:")
            for i = 1, #constants do
                local const = constants[i]
                if type(const) == "string" and #const > 0 then
                    print(f"  [{i}] '{const}'")
                end
            end
        end
    end
    
    -- Выполняем оригинальный код
    local result = original_v29(vm_data, env, ...)
    
    print("=== ВИРТУАЛЬНАЯ МАШИНА ЗАВЕРШЕНА ===")
    return result
end

-- Выводим собранные данные
print("\n📊 СОБРАННЫЕ ДАННЫЕ:")
for i, data in ipairs(extracted_data) do
    if data.type == "string_constant" then
        print(f"  Строка {data.index}: '{data.value}'")
    end
end

print("\n🚀 Запускаем обфусцированный код с отладкой...")
