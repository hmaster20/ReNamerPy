#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для копирования файлов из одной директории в другую с переименованием
и добавлением расширения .txt
"""

import os
import shutil
import argparse
import sys
from pathlib import Path

# Переменные по умолчанию
DEFAULT_SOURCE_DIR = r"D:\Repo"  # Исходная директория по умолчанию
DEFAULT_FILE_FORMATS = ['.php', '.js', '.py', '.html', '.css', '.txt']  # Форматы файлов для поиска
DEFAULT_DESTINATION_DIR = os.path.join(os.getcwd(), 'destination')  # Директория назначения

def create_destination_dir(dest_path):
    """
    Создает директорию назначения, если она не существует
    
    Args:
        dest_path (str): Путь к директории назначения
    """
    try:
        os.makedirs(dest_path, exist_ok=True)
        print(f"Директория назначения создана/проверена: {dest_path}")
    except Exception as e:
        print(f"Ошибка при создании директории {dest_path}: {e}")
        sys.exit(1)

def find_files_by_format(source_dir, file_formats):
    """
    Ищет файлы в исходной директории по заданным форматам
    
    Args:
        source_dir (str): Исходная директория для поиска
        file_formats (list): Список расширений файлов для поиска
        
    Returns:
        list: Список найденных файлов
    """
    found_files = []
    
    if not os.path.exists(source_dir):
        print(f"Ошибка: Исходная директория не существует: {source_dir}")
        return found_files
    
    print(f"Поиск файлов в директории: {source_dir}")
    print(f"Искомые форматы: {', '.join(file_formats)}")
    
    # Рекурсивный поиск файлов
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in file_formats:
                file_path = os.path.join(root, file)
                found_files.append(file_path)
                
    print(f"Найдено файлов: {len(found_files)}")
    return found_files

def copy_and_rename_files(files_list, destination_dir):
    """
    Копирует файлы в директорию назначения и переименовывает их, добавляя .txt
    
    Args:
        files_list (list): Список файлов для копирования
        destination_dir (str): Директория назначения
    """
    if not files_list:
        print("Нет файлов для копирования")
        return
    
    copied_count = 0
    error_count = 0
    
    for file_path in files_list:
        try:
            # Получаем имя файла без пути
            file_name = os.path.basename(file_path)
            
            # Создаем новое имя файла с добавлением .txt
            new_file_name = file_name + '.txt'
            
            # Полный путь к файлу назначения
            dest_file_path = os.path.join(destination_dir, new_file_name)
            
            # Если файл с таким именем уже существует, добавляем номер
            counter = 1
            while os.path.exists(dest_file_path):
                name_without_ext = os.path.splitext(file_name)[0]
                ext = os.path.splitext(file_name)[1]
                new_file_name = f"{name_without_ext}_{counter}{ext}.txt"
                dest_file_path = os.path.join(destination_dir, new_file_name)
                counter += 1
            
            # Копируем файл
            shutil.copy2(file_path, dest_file_path)
            print(f"Скопирован: {file_name} -> {new_file_name}")
            copied_count += 1
            
        except Exception as e:
            print(f"Ошибка при копировании {file_path}: {e}")
            error_count += 1
    
    print(f"\nРезультат копирования:")
    print(f"Успешно скопировано: {copied_count} файлов")
    print(f"Ошибок: {error_count}")

def parse_file_formats(formats_str):
    """
    Парсит строку с форматами файлов и возвращает список
    
    Args:
        formats_str (str): Строка с форматами через запятую
        
    Returns:
        list: Список форматов файлов
    """
    formats = [f.strip() for f in formats_str.split(',')]
    # Добавляем точку в начале, если её нет
    formats = [f if f.startswith('.') else '.' + f for f in formats]
    return formats

def main():
    """
    Основная функция программы
    """
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description='Копирование файлов с переименованием и добавлением расширения .txt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python renamer.py
  python renamer.py -s "C:\\MyFiles" -d "C:\\Output"
  python renamer.py --source "D:\\Projects" --formats "php,js,html"
  python renamer.py -s "E:\\Code" -d "E:\\Backup" -f "py,txt,md"
        """
    )
    
    parser.add_argument('-s', '--source', 
                       default=DEFAULT_SOURCE_DIR,
                       help=f'Исходная директория (по умолчанию: {DEFAULT_SOURCE_DIR})')
    
    parser.add_argument('-d', '--destination',
                       default=DEFAULT_DESTINATION_DIR,
                       help=f'Директория назначения (по умолчанию: {DEFAULT_DESTINATION_DIR})')
    
    parser.add_argument('-f', '--formats',
                       default=','.join(DEFAULT_FILE_FORMATS),
                       help=f'Форматы файлов через запятую (по умолчанию: {",".join(DEFAULT_FILE_FORMATS)})')
    
    # Парсим аргументы
    args = parser.parse_args()
    
    # Получаем значения из аргументов или используем значения по умолчанию
    source_directory = args.source
    destination_directory = args.destination
    file_formats = parse_file_formats(args.formats)
    
    # Выводим информацию о настройках
    print("=" * 60)
    print("СКРИПТ КОПИРОВАНИЯ ФАЙЛОВ С ПЕРЕИМЕНОВАНИЕМ")
    print("=" * 60)
    print(f"Исходная директория: {source_directory}")
    print(f"Директория назначения: {destination_directory}")
    print(f"Форматы файлов: {', '.join(file_formats)}")
    print("=" * 60)
    
    # Создаем директорию назначения
    create_destination_dir(destination_directory)
    
    # Ищем файлы
    files_to_copy = find_files_by_format(source_directory, file_formats)
    
    # Копируем и переименовываем файлы
    copy_and_rename_files(files_to_copy, destination_directory)
    
    print("\nСкрипт завершен!")

if __name__ == "__main__":
    main()