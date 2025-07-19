#!/usr/bin/env python3
"""
Специализированный анализатор функции v28 для LuaObfuscator.com
Ищет точный паттерн возврата значений и анализирует структуру данных
"""

import re
import json

class V28Analyzer:
    def __init__(self, lua_code):
        self.lua_code = lua_code
        self.v28_body = self.extract_v28_body()
        
    def extract_v28_body(self):
        """Извлекает тело функции v28"""
        # Ищем функцию v28 с учетом вложенности
        pattern = r'local function v28\(\)(.*?)(?=\n\s*local function|\n\s*return|\Z)'
        match = re.search(pattern, self.lua_code, re.DOTALL)
        
        if match:
            return match.group(1)
        return None
    
    def find_return_statement(self):
        """Ищет return statement в функции v28"""
        if not self.v28_body:
            return None
            
        # v28 возвращает v59, поэтому ищем return v59
        return_pattern = r'return\s+(v\d+);?'
        match = re.search(return_pattern, self.v28_body)
        
        if match:
            return_var = match.group(1)
            print(f"✅ Найден return statement: return {return_var}")
            return return_var
        
        print("❌ Return statement не найден в v28")
        return None
    
    def analyze_v59_structure(self):
        """Анализирует структуру v59 = {v56,v57,nil,v58}"""
        if not self.v28_body:
            return None
            
        # Ищем определение v59
        v59_pattern = r'local (v\d+) = \(function\(\)\s*return \{([^}]+)\};\s*end\)\(\);'
        match = re.search(v59_pattern, self.v28_body)
        
        if match:
            var_name = match.group(1)
            structure = match.group(2)
            print(f"✅ Найдена структура {var_name}: {{{structure}}}")
            
            # Разбираем компоненты структуры
            components = [comp.strip() for comp in structure.split(',')]
            return {
                'variable': var_name,
                'components': components,
                'structure': structure
            }
        
        print("❌ Структура v59 не найдена")
        return None
    
    def find_v54_function(self):
        """Ищет и анализирует функцию v54"""
        if not self.v28_body:
            return None
            
        # Ищем определение v54 (это функция, которая возвращает v93-v100)
        v54_pattern = r'local (v\d+) = \(function\(\)\s*return function\(([^)]+)\)(.*?)return ([^;]+);'
        match = re.search(v54_pattern, self.v28_body, re.DOTALL)
        
        if match:
            var_name = match.group(1)
            params = match.group(2)
            body = match.group(3)
            return_stmt = match.group(4)
            
            print(f"✅ Найдена функция {var_name}")
            print(f"   Параметры: {params}")
            print(f"   Return: {return_stmt}")
            
            # Извлекаем возвращаемые переменные
            return_vars = [var.strip() for var in return_stmt.split(',')]
            
            return {
                'variable': var_name,
                'parameters': params.split(','),
                'return_variables': return_vars,
                'body': body
            }
        
        print("❌ Функция v54 не найдена")
        return None
    
    def trace_data_flow(self):
        """Отслеживает поток данных в v28"""
        print("\n🔍 Трассировка потока данных в v28:")
        
        # 1. Найти v54 (функция с v93-v100)
        v54_info = self.find_v54_function()
        
        # 2. Найти v59 (возвращаемая структура)
        v59_info = self.analyze_v59_structure()
        
        # 3. Найти return statement
        return_var = self.find_return_statement()
        
        # 4. Найти использование v54 в цикле
        v54_usage = self.find_v54_usage()
        
        return {
            'v54_function': v54_info,
            'v59_structure': v59_info,
            'return_variable': return_var,
            'v54_usage': v54_usage
        }
    
    def find_v54_usage(self):
        """Ищет использование функции v54 в цикле"""
        if not self.v28_body:
            return None
            
        # Ищем вызов v54 в цикле for
        usage_pattern = r'for\s+(v\d+)\s*=\s*[^,]+,\s*(v\d+)\s+do.*?=\s*\(function\(\)\s*return\s+(v\d+)\([^)]+\);.*?end\)\(\);'
        match = re.search(usage_pattern, self.v28_body, re.DOTALL)
        
        if match:
            loop_var = match.group(1)
            limit_var = match.group(2)
            func_call = match.group(3)
            
            print(f"✅ Найдено использование в цикле:")
            print(f"   Переменная цикла: {loop_var}")
            print(f"   Лимит цикла: {limit_var}")
            print(f"   Вызываемая функция: {func_call}")
            
            return {
                'loop_variable': loop_var,
                'limit_variable': limit_var,
                'function_call': func_call
            }
        
        print("❌ Использование v54 в цикле не найдено")
        return None
    
    def extract_string_table_operations(self):
        """Извлекает операции с таблицей строк"""
        if not self.v28_body:
            return []
            
        # Ищем операции с v61 (таблица констант)
        string_ops = []
        
        # Поиск операций типа v61[...] = ...
        v61_pattern = r'v61\[([^\]]+)\]\s*=\s*([^;]+);'
        matches = re.findall(v61_pattern, self.v28_body)
        
        for index, value in matches:
            string_ops.append({
                'index': index,
                'value': value,
                'type': 'assignment'
            })
        
        print(f"✅ Найдено {len(string_ops)} операций с таблицей строк")
        return string_ops
    
    def generate_debug_extraction_code(self, analysis_result):
        """Генерирует код для извлечения данных во время выполнения"""
        
        debug_code = '''-- Улучшенный отладочный код для извлечения данных из v28
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

'''
        
        return debug_code
    
    def full_analysis(self):
        """Полный анализ функции v28"""
        print("🚀 Запуск полного анализа функции v28...")
        
        if not self.v28_body:
            print("❌ Функция v28 не найдена")
            return None
        
        print(f"📏 Размер тела функции v28: {len(self.v28_body)} символов")
        
        # Трассировка потока данных
        data_flow = self.trace_data_flow()
        
        # Извлечение операций со строками
        string_ops = self.extract_string_table_operations()
        
        # Генерация отладочного кода
        debug_code = self.generate_debug_extraction_code(data_flow)
        
        result = {
            'v28_found': True,
            'v28_body_size': len(self.v28_body),
            'data_flow_analysis': data_flow,
            'string_operations': string_ops,
            'debug_extraction_code': debug_code,
            'analysis_summary': {
                'has_v54_function': data_flow['v54_function'] is not None,
                'has_v59_structure': data_flow['v59_structure'] is not None,
                'has_return_statement': data_flow['return_variable'] is not None,
                'string_operations_count': len(string_ops)
            }
        }
        
        return result

def main():
    # Читаем файл
    try:
        with open('your_original_script.lua', 'r', encoding='utf-8') as f:
            lua_code = f.read()
    except FileNotFoundError:
        print("❌ Файл your_original_script.lua не найден")
        return
    
    # Анализируем
    analyzer = V28Analyzer(lua_code)
    result = analyzer.full_analysis()
    
    if result:
        # Сохраняем результат
        with open('v28_detailed_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Сохраняем отладочный код
        with open('enhanced_debug_injection.lua', 'w', encoding='utf-8') as f:
            f.write(result['debug_extraction_code'])
        
        print("\n" + "="*60)
        print("📊 РЕЗУЛЬТАТЫ ДЕТАЛЬНОГО АНАЛИЗА V28")
        print("="*60)
        
        summary = result['analysis_summary']
        print(f"Функция v54 найдена: {'✅' if summary['has_v54_function'] else '❌'}")
        print(f"Структура v59 найдена: {'✅' if summary['has_v59_structure'] else '❌'}")
        print(f"Return statement найден: {'✅' if summary['has_return_statement'] else '❌'}")
        print(f"Операции со строками: {summary['string_operations_count']}")
        
        print(f"\n📄 Файлы созданы:")
        print(f"  • v28_detailed_analysis.json - детальный анализ")
        print(f"  • enhanced_debug_injection.lua - улучшенный отладочный код")
        
        if result['data_flow_analysis']['v54_function']:
            v54 = result['data_flow_analysis']['v54_function']
            print(f"\n🔧 Найдена ключевая функция {v54['variable']}:")
            print(f"  Возвращает: {', '.join(v54['return_variables'])}")
            
            print(f"\n💡 Для извлечения данных:")
            print(f"  1. Вставьте код из enhanced_debug_injection.lua в начало скрипта")
            print(f"  2. Запустите модифицированный скрипт")
            print(f"  3. Анализируйте вывод отладочной информации")

if __name__ == "__main__":
    main()