import os
import shutil
import zipfile
from xfiles_sorter import organize_files, remove_empty_folders, normalize_files, normalize


def handle_command(command):
    if command == "organize":
        # Здесь вы можете запросить у пользователя путь к папке или задать его заранее
        folder_path = input("Введите путь к папке для организации: ")
        organize_files(folder_path)
    elif command == "remove":
        folder_path = input("Введите путь к папке для очистки: ")
        remove_empty_folders(folder_path)
    elif command == "normalize":
        folder_path = input("Введите путь к папке для розшифроки: ")
        normalize_files(folder_path)
    elif command == "help":
        print("Доступные команды:\norganize - организовать файлы в указанной папке\nexit - выйти из программы\nremove - remove folder\nnormalize - translate")
    elif command == "exit":
        print("Выход из программы...")
        exit()
    else:
        print("Неизвестная команда. Введите 'help' для списка доступных команд.")

def main():
    print("Консольный бот для организации файлов. Введите 'help' для списка команд.")
    while True:
        command = input("Введите команду: ")
        handle_command(command)

if __name__ == "__main__":
    main()
