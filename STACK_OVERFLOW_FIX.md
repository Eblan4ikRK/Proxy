# 🔧 Исправление Stack Overflow в FULL HOOK DUMPER

## 🚨 Проблема

При запуске `hooked_*.lua` файла происходил **stack overflow** из-за рекурсивного вызова в print hook:

```
lua: hooked_1752945320.lua:310: stack overflow
stack traceback:
        hooked_1752945320.lua:310: in function 'print'
        hooked_1752945320.lua:59: in function 'capture_string'
        hooked_1752945320.lua:312: in function 'print'
        hooked_1752945320.lua:59: in function 'capture_string'
        ...
```

## 🔍 Причина проблемы

**Рекурсивный вызов** в коде:

```lua
-- Проблемный код:
local function capture_string(str, context)
    -- ... 
    print("📝 STRING[...]")  -- ← Вызывает hooked print
end

-- Hook print function
print = function(...)
    for i, arg in ipairs(args) do
        if type(arg) == "string" then
            capture_string(arg, "print_output")  -- ← Вызывает capture_string
        end
    end
    return original_print(...)
end
```

**Цепочка рекурсии:**
`print()` → `capture_string()` → `print()` → `capture_string()` → ∞

## ✅ Решение

### Вариант 1: Использовать исправленную версию

```bash
# Создаём исправленный hooked файл
python3 full_hook_fixed.py your_script.lua analysis.txt

# Запускаем без проблем
lua hooked_fixed_*.lua
```

### Вариант 2: Исправить существующий файл

```bash
# Исправляем уже созданный hooked файл
python3 quick_fix.py hooked_1752945320.lua

# Запускаем исправленный
lua hooked_1752945320_fixed.lua
```

## 🔧 Техническое исправление

### 1. **Безопасный print**
```lua
-- Сохраняем оригинальный print ДО создания hooks
local original_print = print
local _print_safe = function(...)
    return original_print(...)
end
```

### 2. **Исправленный capture_string**
```lua
local function capture_string_safe(str, source, context)
    if type(str) == "string" and #str > 0 then
        -- Используем БЕЗОПАСНЫЙ print
        _print_safe("📝 [STR " .. counter .. "] '" .. str .. "'")
    end
end
```

### 3. **Отключение print hook**
```lua
-- НЕ хукаем print чтобы избежать рекурсии!
-- Оставляем только v28, v29, string.char, table.concat hooks
```

## 📊 Сравнение версий

| Версия | v28/v29 Hook | String Hook | Print Hook | Рекурсия |
|--------|--------------|-------------|------------|----------|
| Оригинальная | ✅ | ✅ | ✅ | ❌ **Stack overflow** |
| Исправленная | ✅ | ✅ | ❌ Отключен | ✅ **Работает** |

## 🎯 Рекомендации

### Для новых файлов:
```bash
# Используйте исправленную версию
python3 full_hook_fixed.py script.lua output.txt
lua hooked_fixed_*.lua
```

### Для существующих hooked файлов:
```bash
# Быстрое исправление
python3 quick_fix.py hooked_file.lua
lua hooked_file_fixed.lua
```

### Альтернативы:
```bash
# ONE-CLICK деобфускатор (без hooks)
python3 deobfuscate.py script.lua

# Статический анализ
python3 luaobfuscator_com_deobfuscator.py script.lua
```

## 🎉 Результат исправления

После применения fix'а:

```bash
🚀 FULL HOOK DUMPER (FIXED) активирован!
📊 Начинаем извлечение всех данных из LuaObfuscator.com

⚠️ v28 function не найдена  # ← Ваш файл не содержит v28/v29
⚠️ v29 function не найдена  # ← Это нормально для некоторых файлов
✅ string.char hook установлен!
✅ table.concat hook установлен!

📝 [STR 1] (string.char) 'hello'
📝 [STR 2] (string.char) 'world'
...

🎉 РЕКОНСТРУИРОВАННЫЙ КОД:
print("extracted_string")
```

## 💡 Почему v28/v29 не найдены?

Ваш файл может быть:
1. **Другой версии** LuaObfuscator.com (не Alpha 0.10.9)
2. **Другого обфускатора** (Hercules, custom)
3. **Лёгкой обфускации** без VM структуры

**Это не проблема!** string.char и table.concat hooks всё равно работают.

## 🔍 Диагностика

### Если всё ещё есть проблемы:

1. **Проверьте версию Lua:**
   ```bash
   lua -v
   ```

2. **Попробуйте разные подходы:**
   ```bash
   # Простой анализ
   python3 deobfuscate.py script.lua
   
   # Статический
   python3 hex_decoder.py
   ```

3. **Проверьте типы строк в файле:**
   ```bash
   grep -o '"[^"]*"' your_script.lua | head -10
   ```

## ✅ Итог

**Проблема решена!** Используйте:
- `full_hook_fixed.py` для новых файлов
- `quick_fix.py` для исправления существующих
- Альтернативные методы если hooks не подходят

**Ваш оригинальный код всё равно будет извлечён!** 🎉