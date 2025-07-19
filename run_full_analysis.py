#!/usr/bin/env python3
"""
UNIVERSAL DEOBFUSCATION RUNNER
Запускает все доступные инструменты для полной деобфускации LuaObfuscator.com

Использование: python3 run_full_analysis.py input.lua
"""

import sys
import os
import subprocess
import time
import json
from datetime import datetime

def print_banner():
    print("🔓" * 60)
    print("🔥 UNIVERSAL LuaObfuscator.com DEOBFUSCATION SUITE")
    print("🔓" * 60)
    print("")

def check_file_exists(filename):
    """Проверяет существование файла"""
    return os.path.exists(filename)

def run_tool(tool_name, command, description):
    """Запускает инструмент и возвращает результат"""
    print(f"🔧 Запускаем: {tool_name}")
    print(f"📝 Описание: {description}")
    print(f"⚡ Команда: {' '.join(command)}")
    print("-" * 50)
    
    start_time = time.time()
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        execution_time = time.time() - start_time
        
        status = "✅ Успешно" if result.returncode == 0 else "❌ Ошибка"
        print(f"{status} ({execution_time:.2f}s)")
        
        if result.stdout:
            print("📤 Вывод:")
            print(result.stdout[:500] + ("..." if len(result.stdout) > 500 else ""))
        
        if result.stderr and result.returncode != 0:
            print("⚠️ Ошибки:")
            print(result.stderr[:300])
        
        return {
            'tool': tool_name,
            'status': 'success' if result.returncode == 0 else 'error',
            'execution_time': execution_time,
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        }
    
    except subprocess.TimeoutExpired:
        print("⏰ Таймаут (120s)")
        return {
            'tool': tool_name,
            'status': 'timeout',
            'execution_time': 120,
            'output': '',
            'error': 'Timeout after 120 seconds',
            'return_code': -1
        }
    except Exception as e:
        print(f"💥 Исключение: {e}")
        return {
            'tool': tool_name,
            'status': 'exception',
            'execution_time': 0,
            'output': '',
            'error': str(e),
            'return_code': -2
        }
    
    print("")

def main():
    if len(sys.argv) < 2:
        print("❌ Использование: python3 run_full_analysis.py input.lua")
        print("   input.lua - обфусцированный файл для анализа")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Проверяем входной файл
    if not check_file_exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        sys.exit(1)
    
    print_banner()
    print(f"📁 Анализируемый файл: {input_file}")
    print(f"📅 Дата запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Создаём папку для результатов
    results_dir = f"analysis_results_{int(time.time())}"
    os.makedirs(results_dir, exist_ok=True)
    print(f"📂 Результаты будут сохранены в: {results_dir}/")
    print("")
    
    results = []
    
    # Список инструментов для запуска
    tools = [
        {
            'name': 'FULL HOOK DUMPER (Python)',
            'command': ['python3', 'full_hook.py', input_file, f'{results_dir}/full_hook_report.txt'],
            'description': 'Автоматическая инъекция хуков и извлечение всех данных',
            'required_files': ['full_hook.py']
        },
        {
            'name': 'V28 Analyzer (Fixed)',
            'command': ['python3', 'v28_analyzer_fixed.py'],
            'description': 'Детальный анализ функции v28 и VM структуры',
            'required_files': ['v28_analyzer_fixed.py']
        },
        {
            'name': 'LuaObfuscator.com Deobfuscator',
            'command': ['python3', 'luaobfuscator_com_deobfuscator.py', input_file, '-v'],
            'description': 'Статический анализ с обнаружением паттернов',
            'required_files': ['luaobfuscator_com_deobfuscator.py']
        },
        {
            'name': 'Hex Decoder',
            'command': ['python3', 'hex_decoder.py'],
            'description': 'Декодирование hex payload из обфусцированного кода',
            'required_files': ['hex_decoder.py']
        },
        {
            'name': 'LuaObfuscator Decoder',
            'command': ['python3', 'luaobfuscator_decoder.py'],
            'description': 'Специализированный анализ кодировки Q-placeholder',
            'required_files': ['luaobfuscator_decoder.py']
        },
        {
            'name': 'Advanced LuaObfuscator Deobfuscator',
            'command': ['python3', 'advanced_luaobfuscator_deobfuscator.py'],
            'description': 'Расширенный анализ с ML подходами',
            'required_files': ['advanced_luaobfuscator_deobfuscator.py']
        }
    ]
    
    # Запускаем доступные инструменты
    print("🚀 Начинаем полный анализ...")
    print("=" * 60)
    
    available_tools = 0
    successful_tools = 0
    
    for tool in tools:
        # Проверяем доступность всех необходимых файлов
        missing_files = [f for f in tool['required_files'] if not check_file_exists(f)]
        
        if missing_files:
            print(f"⚠️ Пропускаем {tool['name']}: отсутствуют файлы {missing_files}")
            results.append({
                'tool': tool['name'],
                'status': 'missing_files',
                'execution_time': 0,
                'output': '',
                'error': f"Missing files: {missing_files}",
                'return_code': -3
            })
            continue
        
        available_tools += 1
        
        # Запускаем инструмент
        result = run_tool(tool['name'], tool['command'], tool['description'])
        results.append(result)
        
        if result['status'] == 'success':
            successful_tools += 1
    
    # Создаём итоговый отчёт
    print("=" * 60)
    print("📊 СОЗДАНИЕ ИТОГОВОГО ОТЧЁТА")
    print("=" * 60)
    
    report = {
        'analysis_info': {
            'input_file': input_file,
            'analysis_date': datetime.now().isoformat(),
            'results_directory': results_dir,
            'total_tools': len(tools),
            'available_tools': available_tools,
            'successful_tools': successful_tools
        },
        'tool_results': results
    }
    
    # Сохраняем JSON отчёт
    json_report_path = f'{results_dir}/complete_analysis_report.json'
    with open(json_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Создаём текстовый отчёт
    text_report_path = f'{results_dir}/analysis_summary.txt'
    with open(text_report_path, 'w', encoding='utf-8') as f:
        f.write("UNIVERSAL DEOBFUSCATION ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"📁 Файл: {input_file}\n")
        f.write(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"📂 Результаты: {results_dir}/\n\n")
        
        f.write("📊 СТАТИСТИКА:\n")
        f.write(f"   Всего инструментов: {len(tools)}\n")
        f.write(f"   Доступно: {available_tools}\n")
        f.write(f"   Успешно выполнено: {successful_tools}\n")
        f.write(f"   Процент успеха: {(successful_tools/available_tools*100) if available_tools > 0 else 0:.1f}%\n\n")
        
        f.write("🔧 РЕЗУЛЬТАТЫ ПО ИНСТРУМЕНТАМ:\n")
        f.write("-" * 40 + "\n")
        
        for result in results:
            status_emoji = {
                'success': '✅',
                'error': '❌', 
                'timeout': '⏰',
                'exception': '💥',
                'missing_files': '⚠️'
            }.get(result['status'], '❓')
            
            f.write(f"{status_emoji} {result['tool']}\n")
            f.write(f"   Статус: {result['status']}\n")
            f.write(f"   Время: {result['execution_time']:.2f}s\n")
            
            if result['status'] == 'success' and result['output']:
                preview = result['output'][:200].replace('\n', ' ')
                f.write(f"   Вывод: {preview}...\n")
            elif result['error']:
                f.write(f"   Ошибка: {result['error'][:100]}...\n")
            f.write("\n")
        
        # Рекомендации
        f.write("🎯 РЕКОМЕНДАЦИИ:\n")
        f.write("-" * 40 + "\n")
        
        if successful_tools == 0:
            f.write("❌ Ни один инструмент не отработал успешно.\n")
            f.write("   Проверьте:\n")
            f.write("   - Корректность входного файла\n")
            f.write("   - Наличие необходимых зависимостей\n")
            f.write("   - Права на запись в текущую папку\n")
        elif successful_tools < available_tools // 2:
            f.write("⚠️ Частичный успех. Рекомендуется:\n")
            f.write("   - Проверить логи ошибок\n")
            f.write("   - Запустить успешные инструменты повторно\n")
            f.write("   - Проанализировать созданные отчёты\n")
        else:
            f.write("✅ Анализ прошёл успешно!\n")
            f.write("   - Изучите созданные отчёты\n")
            f.write("   - Обратите внимание на FULL HOOK результаты\n")
            f.write("   - Проверьте JSON файлы с детальными данными\n")
        
        f.write(f"\n📄 Полный JSON отчёт: {json_report_path}\n")
    
    # Финальный вывод
    print(f"✅ Анализ завершён!")
    print(f"📊 Статистика: {successful_tools}/{available_tools} инструментов успешно")
    print(f"📂 Результаты сохранены в: {results_dir}/")
    print(f"📄 Итоговый отчёт: {text_report_path}")
    print(f"📋 JSON данные: {json_report_path}")
    print("")
    
    # Показываем краткие результаты
    if successful_tools > 0:
        print("🎉 УСПЕШНЫЕ ИНСТРУМЕНТЫ:")
        for result in results:
            if result['status'] == 'success':
                print(f"   ✅ {result['tool']} ({result['execution_time']:.1f}s)")
        print("")
    
    if successful_tools < available_tools:
        print("⚠️ ПРОБЛЕМНЫЕ ИНСТРУМЕНТЫ:")
        for result in results:
            if result['status'] != 'success':
                print(f"   ❌ {result['tool']}: {result['status']}")
        print("")
    
    # Специальные инструкции для FULL HOOK
    full_hook_result = next((r for r in results if 'FULL HOOK' in r['tool']), None)
    if full_hook_result and full_hook_result['status'] == 'success':
        print("🚀 СЛЕДУЮЩИЕ ШАГИ для FULL HOOK:")
        print("   1. Найдите созданный hooked_*.lua файл")
        print("   2. Установите Lua: sudo apt install lua5.3")
        print("   3. Запустите: lua hooked_*.lua")
        print("   4. Анализируйте полный дамп данных!")
        print("")
    
    print("🎯 Для получения оригинального кода изучите отчёты!")
    print("🔓" * 60)

if __name__ == "__main__":
    main()