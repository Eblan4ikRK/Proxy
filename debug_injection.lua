-- Отладочный скрипт для извлечения данных из LuaObfuscator.com
-- Вставьте этот код ПЕРЕД строкой return v15("LOL!...", v9(), ...);

-- Сохраняем оригинальную функцию v28
local original_v28 = v28

-- Создаем отладочную версию v28
local function debug_v28()
    print("=== ОТЛАДКА V28 ФУНКЦИИ ===")
    
    -- Вызываем оригинальную функцию
    local v93, v94, v95, v96, v97, v98, v99, v100 = original_v28()
    
    -- Выводим все возвращаемые значения
    print("v93 (тип:", type(v93), ") =", v93)
    print("v94 (тип:", type(v94), ") =", v94)
    print("v95 (тип:", type(v95), ") =", v95)
    print("v96 (тип:", type(v96), ") =", v96)
    print("v97 (тип:", type(v97), ") =", v97)
    print("v98 (тип:", type(v98), ") =", v98)
    print("v99 (тип:", type(v99), ") =", v99)
    print("v100 (тип:", type(v100), ") =", v100)
    
    -- Дополнительный анализ для таблиц
    for i, val in ipairs({v93, v94, v95, v96, v97, v98, v99, v100}) do
        local var_name = "v" .. (92 + i)
        if type(val) == "table" then
            print(var_name .. " - таблица с", #val, "элементами:")
            for j = 1, math.min(#val, 5) do  -- показываем первые 5 элементов
                print("  [" .. j .. "] =", val[j])
            end
            if #val > 5 then
                print("  ... и еще", #val - 5, "элементов")
            end
        elseif type(val) == "function" then
            print(var_name .. " - функция")
            -- Пытаемся вызвать функцию без параметров (осторожно!)
            local success, result = pcall(val)
            if success then
                print("  Результат вызова:", result)
            else
                print("  Ошибка при вызове:", result)
            end
        elseif type(val) == "string" then
            print(var_name .. " - строка длиной", #val, "символов")
            if #val < 100 then
                print("  Содержимое:", repr(val))
            else
                print("  Начало:", repr(val:sub(1, 50)) .. "...")
            end
        end
    end
    
    print("=== КОНЕЦ ОТЛАДКИ V28 ===")
    
    -- Возвращаем те же значения
    return v93, v94, v95, v96, v97, v98, v99, v100
end

-- Заменяем v28 на отладочную версию
v28 = debug_v28

-- Дополнительно: отладка функции v29 если она используется
if v29 then
    local original_v29 = v29
    v29 = function(...)
        print("=== ОТЛАДКА V29 ВЫЗОВА ===")
        print("Аргументы v29:", ...)
        local result = original_v29(...)
        print("Результат v29:", result)
        print("=== КОНЕЦ ОТЛАДКИ V29 ===")
        return result
    end
end

-- Функция для безопасного представления значений
function repr(val)
    if type(val) == "string" then
        return '"' .. val:gsub('\\', '\\\\'):gsub('"', '\\"') .. '"'
    else
        return tostring(val)
    end
end

print("🔍 Отладочные хуки установлены! Запускаем оригинальный код...")

-- ЗДЕСЬ ИДЕТ ОРИГИНАЛЬНЫЙ КОД
-- return v15("LOL!...", v9(), ...);