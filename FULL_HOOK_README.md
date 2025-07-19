# 🔥 FULL HOOK DUMPER для LuaObfuscator.com

**Автоматический полный дамп всех строк, функций и VM инструкций из обфусцированных LuaObfuscator.com скриптов**

## 🚀 Использование

```bash
lua full_hook.lua input.lua output.txt
```

### Параметры:
- `input.lua` - ваш обфусцированный файл LuaObfuscator.com
- `output.txt` - файл для сохранения полного отчёта

## 🎯 Пример использования

```bash
# Анализируем ваш скрипт
lua full_hook.lua your_original_script.lua analysis_report.txt

# Результат будет сохранён в analysis_report.txt
```

## ✨ Что извлекает скрипт

### 🔤 Строки:
- ✅ Константы из VM (v28 extraction)
- ✅ Runtime строки (v29 execution)
- ✅ string.char генерации
- ✅ table.concat сборки
- ✅ print выводы

### 🔧 Функции:
- ✅ VM функции из таблицы функций
- ✅ Обфусцированные функции v0-v99
- ✅ Внутренние функции обработки

### ⚡ VM Инструкции:
- ✅ Opcodes виртуальной машины
- ✅ Инструкции выполнения
- ✅ Структура данных VM

### 📊 Константы:
- ✅ Все типы констант
- ✅ Числовые значения
- ✅ Таблицы данных

## 🔍 Технические детали

### Хукинг происходит на уровне:
1. **Функция v28** - извлечение структуры VM
2. **Функция v29** - перехват выполнения
3. **string.char** - генерация символов
4. **table.concat** - сборка строк
5. **print** - вывод результатов

### Безопасность:
- ✅ Безопасное выполнение (только логирование)
- ✅ Автоматическая очистка временных файлов
- ✅ Защита от зависания и ошибок

## 📋 Пример вывода

```
🔍 FULL HOOK DUMPER для LuaObfuscator.com
📁 Входной файл: script.lua
📄 Выходной файл: report.txt

🚀 Хуки активированы! Начинаем полный дамп...
✅ v28 function hooked!
✅ v29 function hooked!
✅ string.char hooked!
✅ table.concat hooked!
✅ print function hooked!

🎯 === HOOKING v28 FUNCTION ===
📊 VM Structure type: table
📋 VM Components count: 4
🔹 Component[1] type: table
   📦 Table size: 5
   🔧 VM INSTRUCTIONS:
      [1] 0 0 1 3
      [2] 1 2 0 0
      [3] 2 0 1 0

🔹 Component[2] type: table
   📦 Table size: 4
   📚 CONSTANTS TABLE:
      [1] nil: nil
      [2] string: print
      [3] string: hmmmm

📝 STRING[1] (vm_constant): 'print'
📝 STRING[2] (vm_constant): 'hmmmm'

⚡ === HOOKING v29 EXECUTION ===
🔤 RUNTIME STRINGS EXTRACTION:
   🎯 Runtime[2]: 'print'
   🎯 Runtime[3]: 'hmmmm'
📊 Total runtime strings found: 2

🎉 FULL HOOK DUMPER завершён успешно!
📊 Результаты:
   • Строк извлечено: 4
   • Функций найдено: 2
   • Отчёт сохранён в: report.txt

🔍 Найденные строки:
   1. 'print' (vm_constant)
   2. 'hmmmm' (vm_constant)
   3. 'print' (runtime)
   4. 'hmmmm' (runtime)
```

## 📄 Структура отчёта

Отчёт содержит:

### 1. Заголовок с метаданными
```
FULL HOOK DUMPER - Полный отчёт деобфускации
=============================================================
📁 Входной файл: script.lua
📅 Дата анализа: 2024-01-15 14:30:25
⏱️  Время выполнения: 2 секунд
```

### 2. Извлечённые строки
```
🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ:
----------------------------------------
[1] (vm_constant) Length:5 - 'print'
[2] (vm_constant) Length:5 - 'hmmmm'
[runtime_2] (runtime) Length:5 - 'print'
[runtime_3] (runtime) Length:5 - 'hmmmm'
```

### 3. Найденные функции
```
🔧 НАЙДЕННЫЕ ФУНКЦИИ:
----------------------------------------
[1] vm_function_1 (vm_functions) - function: 0x559ABC123
[2] anonymous (string.char) - function: 0x559ABC456
```

### 4. Полный вывод выполнения
```
📋 ПОЛНЫЙ ВЫВОД ВЫПОЛНЕНИЯ:
------------------------------------------------------------
[весь лог выполнения с хуками]
```

### 5. Реконструированный код
```
🎉 РЕКОНСТРУИРОВАННЫЙ КОД:
----------------------------------------
print("hmmmm")
```

## 🛠️ Устранение неполадок

### Ошибка "файл не найден"
```bash
❌ Ошибка: Файл script.lua не найден!
```
**Решение**: Проверьте путь к файлу

### Ошибка "не удалось запустить код"
```bash
❌ Не удалось запустить код!
```
**Решение**: Убедитесь что Lua установлен: `lua -v`

### Пустой вывод
**Возможные причины**:
- Файл не является LuaObfuscator.com скриптом
- Версия обфускатора не поддерживается
- Скрипт повреждён

## 🎯 Для вашего случая

На основе ваших данных:
```
1    3    print   function: 009DC990   function: 009DCB20   function: 009D13A8   table: 009D5CA0 1
1    3    hmmmm   function: 009DC990   function: 009DCB20   function: 009D13A8   table: 009D5CA0 2
```

Скрипт должен выдать:
```bash
🔍 Найденные строки:
   1. 'print' (vm_constant)
   2. 'hmmmm' (vm_constant)

🎉 РЕКОНСТРУИРОВАННЫЙ КОД:
print("hmmmm")
```

## 🚀 Запуск на вашем файле

```bash
# Скопируйте ваш обфусцированный код в файл
cp your_obfuscated_script.lua input.lua

# Запустите full_hook
lua full_hook.lua input.lua full_analysis.txt

# Посмотрите результаты
cat full_analysis.txt
```

**Результат**: Полный дамп всех строк, функций и инструкций + автоматическая реконструкция оригинального кода!

---

**💡 Совет**: Этот скрипт автоматизирует весь процесс, который мы делали вручную, и даёт полный отчёт за один запуск.