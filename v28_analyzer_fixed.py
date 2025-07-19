#!/usr/bin/env python3
"""
Исправленный специализированный анализатор функции v28
"""

import re
import json

class V28AnalyzerFixed:
    def __init__(self, lua_code):
        self.lua_code = lua_code
        self.v28_body = self.extract_v28_body()
        
    def extract_v28_body(self):
        """Извлекает тело функции v28 правильно"""
        # Ищем от 'local function v28()' до 'end' перед 'local function v29'
        pattern = r'local function v28\(\)(.*?)(?=\n\s*end\s*\n\s*local function v29)'
        match = re.search(pattern, self.lua_code, re.DOTALL)
        
        if match:
            body = match.group(1)
            print(f"✅ Извлечено тело v28: {len(body)} символов")
            return body
        
        # Альтернативный поиск
        pattern2 = r'local function v28\(\)(.*?)return v59;'
        match2 = re.search(pattern2, self.lua_code, re.DOTALL)
        
        if match2:
            body = match2.group(1) + "return v59;"
            print(f"✅ Извлечено тело v28 (альтернативный способ): {len(body)} символов")
            return body
            
        print("❌ Не удалось извлечь тело функции v28")
        return None
    
    def find_return_statement(self):
        """Ищет return statement в функции v28"""
        if not self.v28_body:
            return None
            
        # Ищем 'return v59' в конце функции
        return_pattern = r'return\s+(v\d+);?\s*$'
        match = re.search(return_pattern, self.v28_body, re.MULTILINE)
        
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
            
        # Ищем определение v59 с правильным паттерном
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
        """Ищет и анализирует функцию v54 с переменными v93-v100"""
        if not self.v28_body:
            return None
            
        # Ищем функцию v54 с параметрами v93, v94, v95, v96, v97, v98, v99, v100
        v54_pattern = r'local (v\d+) = \(function\(\)\s*return function\((v\d+, v\d+, v\d+, v\d+, v\d+, v\d+, v\d+, v\d+)\)(.*?)return (v\d+, v\d+, v\d+, v\d+, v\d+, v\d+, v\d+, v\d+);'
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
            param_vars = [var.strip() for var in params.split(',')]
            
            return {
                'variable': var_name,
                'parameters': param_vars,
                'return_variables': return_vars,
                'body': body
            }
        
        print("❌ Функция v54 с v93-v100 не найдена")
        return None
    
    def find_v93_v100_assignments(self):
        """Ищет присваивания переменных v93-v100 внутри функции v54"""
        if not self.v28_body:
            return {}
            
        assignments = {}
        
        # Ищем присваивания типа 'local v93 = ...'
        for i in range(93, 101):  # v93 to v100
            var_name = f"v{i}"
            pattern = rf'local {var_name} = \(function\(\)\s*return ([^;]+);\s*end\)\(\);'
            match = re.search(pattern, self.v28_body)
            
            if match:
                value = match.group(1)
                assignments[var_name] = value
                print(f"✅ Найдено присваивание: {var_name} = {value}")
        
        print(f"📝 Всего найдено {len(assignments)} присваиваний v93-v100")
        return assignments
    
    def find_loops_and_operations(self):
        """Ищет циклы for и операции внутри v28"""
        if not self.v28_body:
            return []
            
        operations = []
        
        # Ищем циклы for
        for_pattern = r'for (v\d+) = ([^,]+), (v\d+) do(.*?)end'
        matches = re.findall(for_pattern, self.v28_body, re.DOTALL)
        
        for loop_var, start_val, end_var, loop_body in matches:
            operations.append({
                'type': 'for_loop',
                'variable': loop_var,
                'start': start_val,
                'end': end_var,
                'body': loop_body.strip()
            })
            print(f"✅ Найден цикл for: {loop_var} от {start_val} до {end_var}")
        
        return operations
    
    def extract_constant_table_operations(self):
        """Извлекает операции с таблицей констант (v61)"""
        if not self.v28_body:
            return []
            
        constants = []
        
        # Ищем операции v61[index] = value
        v61_pattern = r'v61\[([^\]]+)\] = \(function\(\)\s*return ([^;]+);\s*end\)\(\);'
        matches = re.findall(v61_pattern, self.v28_body)
        
        for index, value in matches:
            constants.append({
                'index': index,
                'value': value,
                'type': 'constant_assignment'
            })
            print(f"✅ Константа v61[{index}] = {value}")
        
        print(f"📋 Найдено {len(constants)} констант")
        return constants
    
    def generate_runtime_extraction_script(self):
        """Генерирует скрипт для извлечения данных во время выполнения"""
        
        script = '''-- RUNTIME EXTRACTION SCRIPT для LuaObfuscator.com
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
print("\\n📊 СОБРАННЫЕ ДАННЫЕ:")
for i, data in ipairs(extracted_data) do
    if data.type == "string_constant" then
        print(f"  Строка {data.index}: '{data.value}'")
    end
end

print("\\n🚀 Запускаем обфусцированный код с отладкой...")
'''
        
        return script
    
    def full_analysis(self):
        """Полный анализ функции v28"""
        print("🚀 Запуск ИСПРАВЛЕННОГО анализа функции v28...")
        
        if not self.v28_body:
            print("❌ Функция v28 не найдена")
            return None
        
        print(f"📏 Размер тела функции v28: {len(self.v28_body)} символов")
        
        # Трассировка компонентов
        print("\n🔍 Анализ компонентов v28:")
        
        # 1. Найти v54 (функция с v93-v100)
        v54_info = self.find_v54_function()
        
        # 2. Найти присваивания v93-v100
        v93_v100_assignments = self.find_v93_v100_assignments()
        
        # 3. Найти v59 (возвращаемая структура)
        v59_info = self.analyze_v59_structure()
        
        # 4. Найти return statement
        return_var = self.find_return_statement()
        
        # 5. Найти циклы и операции
        operations = self.find_loops_and_operations()
        
        # 6. Найти операции с константами
        constants = self.extract_constant_table_operations()
        
        # 7. Генерация скрипта извлечения
        extraction_script = self.generate_runtime_extraction_script()
        
        result = {
            'v28_found': True,
            'v28_body_size': len(self.v28_body),
            'v54_function': v54_info,
            'v93_v100_assignments': v93_v100_assignments,
            'v59_structure': v59_info,
            'return_variable': return_var,
            'operations': operations,
            'constants': constants,
            'extraction_script': extraction_script,
            'analysis_summary': {
                'has_v54_function': v54_info is not None,
                'has_v59_structure': v59_info is not None,
                'has_return_statement': return_var is not None,
                'v93_v100_count': len(v93_v100_assignments),
                'operations_count': len(operations),
                'constants_count': len(constants)
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
    analyzer = V28AnalyzerFixed(lua_code)
    result = analyzer.full_analysis()
    
    if result:
        # Сохраняем результат
        with open('v28_fixed_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Сохраняем скрипт извлечения
        with open('runtime_extraction_script.lua', 'w', encoding='utf-8') as f:
            f.write(result['extraction_script'])
        
        print("\n" + "="*70)
        print("📊 РЕЗУЛЬТАТЫ ИСПРАВЛЕННОГО АНАЛИЗА V28")
        print("="*70)
        
        summary = result['analysis_summary']
        print(f"✅ Функция v28 найдена и проанализирована")
        print(f"📏 Размер тела функции: {result['v28_body_size']} символов")
        print(f"🔧 Функция v54: {'✅' if summary['has_v54_function'] else '❌'}")
        print(f"📊 Структура v59: {'✅' if summary['has_v59_structure'] else '❌'}")
        print(f"↩️  Return statement: {'✅' if summary['has_return_statement'] else '❌'}")
        print(f"🔢 Переменные v93-v100: {summary['v93_v100_count']}")
        print(f"🔄 Операции/циклы: {summary['operations_count']}")
        print(f"📋 Константы: {summary['constants_count']}")
        
        if result['v93_v100_assignments']:
            print(f"\n🔢 Найденные присваивания v93-v100:")
            for var, value in result['v93_v100_assignments'].items():
                print(f"  {var} = {value}")
        
        if result['v59_structure']:
            v59 = result['v59_structure']
            print(f"\n📊 Структура {v59['variable']}: {{{v59['structure']}}}")
            print(f"  Компоненты: {', '.join(v59['components'])}")
        
        print(f"\n📄 Файлы созданы:")
        print(f"  • v28_fixed_analysis.json - подробный анализ")
        print(f"  • runtime_extraction_script.lua - скрипт для извлечения данных")
        
        print(f"\n💡 Рекомендации по деобфускации:")
        print(f"  1. Вставьте код из runtime_extraction_script.lua в начало вашего скрипта")
        print(f"  2. Запустите модифицированный скрипт в Lua интерпретаторе")
        print(f"  3. Анализируйте вывод для получения:")
        print(f"     • Строковых констант")
        print(f"     • Инструкций виртуальной машины")
        print(f"     • Структуры данных")
        print(f"  4. Используйте извлеченные данные для реконструкции оригинального кода")

if __name__ == "__main__":
    main()