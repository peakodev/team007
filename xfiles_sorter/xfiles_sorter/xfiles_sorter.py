import os
import shutil
import zipfile
import logging


def normalize(file_name):
    translit_table = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
        'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'iu', 'я': 'ia'
    }

    result = ''
    base_name, extension = os.path.splitext(file_name)
    for char in base_name:
        result += translit_table.get(char, char) if char not in ['/', '\\'] else char
    return result + extension


def remove_empty_folders(folder_path):
    folder_removed = False
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            current_folder = os.path.join(root, directory)
            try:
                os.rmdir(current_folder)
                print(f"Folder Purged of Contents: {current_folder}")
                folder_removed = True
            except OSError as e:
                # Error message printing removed to not display non-empty folder errors
                pass
    if not folder_removed:
        print("No Confidential Folders Detected.")


# def organize_files(folder_path):
#     folders_to_ignore = ['archived intel', 'classified footage', 'covert audio', 'top-secret documents', 'sensitive imager', 'miscellaneous classified data']
#     files_moved_count = {
#         'sensitive imager': 0,
#         'top-secret documents': 0,
#         'covert audio': 0,
#         'classified footage': 0,
#         'archived intel': 0,
#         'miscellaneous classified data': 0
#     }

#     for folder in folders_to_ignore:
#         if not os.path.exists(os.path.join(folder_path, folder)):
#             os.makedirs(os.path.join(folder_path, folder))

#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)

#             if any(folder in file_path.split(os.path.sep) for folder in folders_to_ignore):
#                 continue

#             if file_name.startswith('.') or os.path.isdir(file_path) or file_name in folders_to_ignore:
#                 continue

#             normalized_name = normalize(file_name)

#             file_extension = os.path.splitext(file_name)[1][1:].lower()

#             if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
#                 shutil.move(file_path, os.path.join(folder_path, 'sensitive imager', normalized_name))
#                 files_moved_count['sensitive imager'] += 1
#             elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
#                 shutil.move(file_path, os.path.join(folder_path, 'top-secret documents', normalized_name))
#                 files_moved_count['top-secret documents'] += 1
#             elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
#                 shutil.move(file_path, os.path.join(folder_path, 'covert audio', normalized_name))
#                 files_moved_count['covert audio'] += 1
#             elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
#                 shutil.move(file_path, os.path.join(folder_path, 'classified footage', normalized_name))
#                 files_moved_count['classified footage'] += 1
#             elif file_extension in ['zip', 'gz', 'tar']:
#                 try:
#                     if os.path.exists(file_path):
#                         with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                             zip_ref.extractall(os.path.join(folder_path, 'archived intel', normalized_name))
#                         os.remove(file_path)
#                         files_moved_count['archived intel'] += 1
#                         continue
#                     else:
#                         print(f"Classified Document Unavailable: {file_path}")
#                 except zipfile.BadZipFile:
#                     os.remove(file_path)
#             else:
#                 shutil.move(file_path, os.path.join(folder_path, 'miscellaneous classified data', normalized_name))
#                 files_moved_count['miscellaneous classified data'] += 1
        

def organize_files(folder_path, target_folder_path):
    logging.basicConfig(filename='organize_files.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    if target_folder_path is None:
        target_folder_path = folder_path
    
    folders_to_ignore = ['archived intel', 'classified footage', 'covert audio', 'top-secret documents', 'sensitive imager', 'miscellaneous classified data']
    files_moved_count = {category: 0 for category in folders_to_ignore}


    for folder in folders_to_ignore:
        target_path = os.path.join(target_folder_path, folder)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)


            if any(folder in file_path.replace(folder_path, target_folder_path).split(os.path.sep) for folder in folders_to_ignore):
                continue


            if file_name.startswith('.') or os.path.isdir(file_path) or file_name in folders_to_ignore:
                continue
             
            normalized_name = normalize(file_name)
            file_extension = os.path.splitext(file_name)[1][1:].lower()


            if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
                try:
                    shutil.move(file_path, os.path.join(target_folder_path, 'sensitive imager', normalized_name))
                    files_moved_count['sensitive imager'] += 1
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {file_path} в 'sensitive imager': {e}")
            elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
                try:
                    shutil.move(file_path, os.path.join(target_folder_path, 'top-secret documents', normalized_name))
                    files_moved_count['top-secret documents'] += 1
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {file_path} в 'stop-secret documents': {e}")
            elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
                try:
                    shutil.move(file_path, os.path.join(target_folder_path, 'covert audio', normalized_name))
                    files_moved_count['covert audio'] += 1
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {file_path} в 'covert audio': {e}")
            elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
                try:
                    shutil.move(file_path, os.path.join(target_folder_path, 'classified footage', normalized_name))
                    files_moved_count['classified footage'] += 1
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {file_path} в 'classified footage': {e}")
            elif file_extension in ['zip', 'gz', 'tar']:
                archive_target_folder = os.path.join(target_folder_path, 'archived intel', normalized_name.replace('.' + file_extension, ''))
                if not os.path.exists(archive_target_folder):
                    os.makedirs(archive_target_folder)
                # try:
                if os.path.exists(file_path):
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(archive_target_folder)
                        os.remove(file_path)
                        files_moved_count['archived intel'] += 1
                    except zipfile.BadZipFile:
                        logging.error(f"Ошибка: файл {file_path} поврежден и не может быть распакован.")
                        os.remove(file_path)
                    except Exception as e:
                        logging.error(f"Ошибка при обработке архива {file_path}: {e}")
            else:
                try:
                    shutil.move(file_path, os.path.join(folder_path, 'miscellaneous classified data', normalized_name))
                    files_moved_count['miscellaneous classified data'] += 1
                except Exception as e:
                    logging.error(f"Ошибка при перемещении файла {file_path} в 'miscellaneous classified data': {e}")


    remove_empty_folders(folder_path)
    print("Secure Directory Organization Complete.")
    for category, count in files_moved_count.items():
        print(f"{count} files moved to {category}.")
