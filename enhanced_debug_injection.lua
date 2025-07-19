-- Улучшенный отладочный код для извлечения данных из v28
-- Вставьте этот код ПЕРЕД строкой return v15(...)

-- Перехватываем v28
local original_v28 = v28
local function enhanced_debug_v28()
    print("=== РАСШИРЕННАЯ ОТЛАДКА V28 ===")
    
    -- Вызываем оригинальную функцию
    local result = original_v28()
    
    print("Тип результата v28:", type(result))
    
    if type(result) == "table" then
        print("Структура результата v28:")
        for i, component in ipairs(result) do
            print(f"  [{i}] тип:", type(component))
            
            if type(component) == "table" then
                print(f"    Размер таблицы: {#component}")
                -- Выводим первые несколько элементов
                for j = 1, math.min(#component, 3) do
                    local elem = component[j]
                    if type(elem) == "table" then
                        print(f"      [{j}] таблица размером {#elem}")
                        if #elem > 0 then
                            print(f"        Первый элемент: {elem[1]} (тип: {type(elem[1])})")
                        end
                    else
                        print(f"      [{j}] = {elem} (тип: {type(elem)})")
                    end
                end
                if #component > 3 then
                    print(f"    ... и ещё {#component - 3} элементов")
                end
            elseif type(component) == "function" then
                print("    Это функция - попробуем вызвать")
                local success, func_result = pcall(component)
                if success then
                    print(f"    Результат вызова: {func_result} (тип: {type(func_result)})")
                else
                    print(f"    Ошибка при вызове: {func_result}")
                end
            else
                print(f"    Значение: {component}")
            end
        end
    end
    
    print("=== КОНЕЦ РАСШИРЕННОЙ ОТЛАДКИ V28 ===")
    return result
end

-- Заменяем v28
v28 = enhanced_debug_v28

-- Дополнительно: отладка v29 для перехвата выполнения
local original_v29 = v29
v29 = function(vm_data, env, ...)
    print("=== ОТЛАДКА V29 (ВЫПОЛНЕНИЕ ВИРТУАЛЬНОЙ МАШИНЫ) ===")
    print("VM данные тип:", type(vm_data))
    
    if type(vm_data) == "table" and #vm_data >= 1 then
        local instructions = vm_data[1]  -- Обычно инструкции в первом элементе
        if type(instructions) == "table" then
            print("Количество инструкций:", #instructions)
            
            -- Анализируем первые несколько инструкций
            for i = 1, math.min(#instructions, 5) do
                local instr = instructions[i]
                if type(instr) == "table" then
                    print(f"Инструкция {i}: {table.concat(instr, ', ')}")
                else
                    print(f"Инструкция {i}: {instr}")
                end
            end
        end
        
        -- Проверяем таблицу констант (обычно во втором элементе)
        if #vm_data >= 2 then
            local constants = vm_data[2]
            if type(constants) == "table" then
                print("Количество констант:", #constants)
                for i = 1, math.min(#constants, 10) do
                    local const = constants[i]
                    print(f"Константа {i}: {const} (тип: {type(const)})")
                end
            end
        end
    end
    
    local result = original_v29(vm_data, env, ...)
    print("=== КОНЕЦ ОТЛАДКИ V29 ===")
    return result
end

print("🔧 Улучшенные отладочные хуки установлены!")

