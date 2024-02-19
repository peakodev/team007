import inquirer
from inquirer import prompt
from inquirer.themes import BlueComposure
from colorama import init
init()
from colorama import Fore, Back, Style

def check_input(msg_txt, type_mode):
    msg = Fore.RED + 'Щоб відмовитися, натисніть Enter\n' + \
          Fore.RESET + msg_txt + Style.BRIGHT + ' > ' + Style.RESET_ALL
    txt_add_user = input(msg)
    tuple_msg = tuple(filter(lambda x: x, txt_add_user.split(' ')))
    if len(tuple_msg) == 0:
        return '0'
    
    user = tuple_msg[0]
    
    '''--------- Додати користовача ---------'''
    if type_mode == 'AddUser':
        num_phone, birthday, txt = None, None, ''
        
        if len(tuple_msg) >= 2:
           num_phone = tuple_msg[1]
           txt = f' т. {num_phone}'
        
        if len(tuple_msg) == 3:
            birthday = tuple_msg[2]
            txt = txt + f' день народження: {birthday} '
    
        '''   Тут має бути виклик методу "Додати користовача"   '''
        return f'Користувач {user} доданий до адресної книги ' + txt
    
    '''--------- Додати/змінити інформацію ---------'''
    if type_mode == 'AddInfo':
        
        if len(tuple_msg) == 2:        # ----------- Видалити/Додати номер телефону
            type_job = tuple_msg[1][0]
            num_phone = tuple_msg[1][1:]
            if type_job == '-':                  # Видалити номер телефону
                '''   Тут має бути виклик методу "Видалити номер телефону"   '''
                return f'У користувача {user} видалено номер телефону {num_phone}'
            
            elif type_job == '+':                # Додати  номер телефону
                '''   Тут має бути виклик методу "Додати  номер телефону"   '''
                return f'Користувачу {user} додано номер телефону {num_phone}'
            
            else:
                return f'Помилка у типі операції {type_job}'
            
        elif len(tuple_msg) == 3:      # ----------- Замінити номер телефону
            old_phone = tuple_msg[1]
            new_phone = tuple_msg[2]
            '''   Тут має бути виклик методу "Замінити номер телефону"   '''
            return f'Користувачу {user} номер телефону {old_phone} замінено на {new_phone}'
        
        else:
            return 'Відсутня інформація необхідна для "Додавання/Видалення/Заміни"'
            

choice_main, choice_book = ['', '']

while choice_main != 'Закінчити роботу':
    
    print('\n\n\n')
    main_menu = [inquirer.List('MainMenu',
                 message = Fore.LIGHTWHITE_EX+Style.BRIGHT+'Выберите режим работы'+Style.RESET_ALL,
                 choices = ['Адресна книга',
                            'Блокнот',
                            'Сортування',
                            'Закінчити роботу'])]
    choice_main = prompt(main_menu, theme=BlueComposure())['MainMenu']
    
    while choice_main == 'Адресна книга' and \
          choice_book != 'Повернутись на режими роботи':
    
        book_menu = [inquirer.List('BookMenu',
                      message = Fore.LIGHTWHITE_EX+Style.BRIGHT+"Робота з адресною книгою"+Style.RESET_ALL,
                      choices = ['Додати нового користувача',
                                 'Додати/змінити інформацію',
                                 "Пошук на ім'я або номер телефону",
                                 'Отримати інформацію про користувачів', 
                                 'Повернутись на режими роботи',
                                 'Закінчити роботу'])]
        choice_book = prompt(book_menu, theme=BlueComposure())['BookMenu']

        if choice_book == 'Закінчити роботу': 
           choice_main = choice_book
           break
        
        while choice_book == 'Додати нового користувача':
            
            txt_msg = "Вкажіть ім'я користувача, телефон та (не обов'язково) дату народження"
            txt = check_input(txt_msg, 'AddUser')
            if txt == '0':
                break
            
            print('\n\n\n' + Fore.LIGHTWHITE_EX + Style.BRIGHT + txt + '\n\n' + \
                   Fore.WHITE + Style.RESET_ALL + f'Продовжуємо режим: "{choice_book}')
            
        while choice_book == 'Додати/змінити інформацію':
            
            txt_msg = Fore.LIGHTWHITE_EX + Style.BRIGHT + \
                "Вкажіть " + Fore.LIGHTBLUE_EX + '"ім''я користувача" ' + Fore.WHITE + \
                "та (через пропуск):\n" + Style.RESET_ALL + \
                '   для додавання номера телефону: ' + Fore.LIGHTBLUE_EX + '"+номер"\n' + Fore.WHITE + \
                '   для видалення номера телефону: ' + Fore.LIGHTBLUE_EX + '"-номер"\n' + Fore.WHITE + \
                '   для заміни номера телефону: '+ Fore.LIGHTBLUE_EX + '"старий номер" "новый номер"' + Fore.RESET
            
            txt = check_input(txt_msg, 'AddInfo')
            if txt == '0':
                break
            
            print('\n\n\n' + Fore.LIGHTWHITE_EX + Style.BRIGHT + txt + '\n\n' + \
                   Fore.WHITE + Style.RESET_ALL + f'Продовжуємо режим: "{choice_book}')
        
print('\n\n\n' + Style.BRIGHT + Fore.BLACK + Back.LIGHTCYAN_EX + 
      'Дякую що вибрали для роботи наш JAMESBOT' + Style.RESET_ALL + Fore.RESET + Back.RESET + ' \n\n')
