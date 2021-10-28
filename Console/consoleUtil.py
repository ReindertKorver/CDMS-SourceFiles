import glob, os, sys
from typing import Callable
class ConsoleUtility:
    @staticmethod
    def showFuncDict(dict):
        for i, (k,v) in enumerate(dict.items()):
            print(k+":\t"+v.__name__)
    @staticmethod
    def clear_console() :
        print_str = '\n'*30
        print_str += '\033[H'
        print_str += '\033[J'
        print(print_str,end='')
        return print_str
    @staticmethod
    def rewriteLastLine(input):
       print (str(input)+"...",end="\r")
        

    @staticmethod
    def remove_row() :
        print_str = '\033[F'
        print_str += '\033[K'
        print(print_str,end='')
        return print_str

    @staticmethod
    def show_header(title) :
        ConsoleUtility.clear_console()
        line = ('*' * (len(title) + 9)) + '\n'
        title_row = '*   ' + title + '    *\n'
        print_str = line + title_row + line
        print(print_str)
        return print_str

    @staticmethod
    def input_number(text='Number: ', error='Invalid number!') :
        input_str = ConsoleUtility.is_int(input(text))

        if input_str == False :
            print(error)
            return ConsoleUtility.input_number(text,error)
        else :
            return input_str

    @staticmethod
    def input_not_empty(text, error='Empty input!') :
        input_str = input(text)
        if input_str == '' :
            print(error)
            return ConsoleUtility.input_not_empty(text, error)
        else :
            return input_str


    @staticmethod
    def input_numbers(text='Number(s): ', error='Invalid number(s)!') :
        input_str = input(text)
        
        numbers = []

        if(input_str.count('-') == 1) :
            filtered_input = ''.join([c for c in input_str if c.isdigit() or c == '-'])
            splitted = filtered_input.split('-')
            if len(splitted) == 2 :
                if splitted[0].isdigit() and splitted[1].isdigit() :
                    return list(range(int(splitted[0]), int(splitted[1])+1))


        seperated = True
        for i,c in enumerate(input_str) :
            if (c == ',' or  c == ';') and i+1 != len(input_str) :
                seperated = True
            elif c.isdigit() and seperated:
                numbers.append(int(c))
                seperated = False
            elif c.isdigit() :
                numbers[len(numbers)-1] = int(numbers[-1]) * 10 + int(c)

        if len(numbers) < 1 :
            print(error)
            return ConsoleUtility.input_numbers(text,error)
        else :
            return numbers
            
    @staticmethod
    def validate_input(validator:Callable[[str], str] ,text='Type something: '):
        val =input(text)
        valResult = validator(val)
        if valResult==None:
            return val
        else:
            print("❌ "+valResult)
            return ConsoleUtility.validate_input(validator,text)

    @staticmethod
    def select_option(options, text='Select option: ', select_text='Option: ', error='Invalid option!') :
        selected_options = ConsoleUtility.select_options(options, text, select_text, error)
        if len(selected_options) > 0 :
            selected_option = selected_options[0][1]
            if len(selected_options) > 1 :
                ConsoleUtility.remove_row()
                print('To many options\n')
            elif(selected_option < len(options) and selected_option >= 0) :
                return (options[selected_option], selected_option)

        return ConsoleUtility.select_option(options, text, select_text, error)

    @staticmethod
    def select_options(options, text='Select option(s): ', select_text='Option(s): ', error='Invalid option(s)!') :
        print(text)
        for i, option in enumerate(options) :
            print(f'  {str(i+1)}. {option}')

        selected_nums = ConsoleUtility.input_numbers(select_text, error+'\n')
        selected_options = []
        for selected_num in selected_nums :
            index = selected_num - 1
            if(index < len(options) and index >= 0) :
                selected_options.append((options[index], index))
        
        if len(selected_options) > 0 :
            print()
            return selected_options
        else :
            print(error+'\n')
            return ConsoleUtility.select_options(options, text, select_text, error)

    @staticmethod       
    def search_option(options, display_order, search_order, col_width, sort_key, text='Option: ', search_text='Search term: ', before_table='', error='Invalid option!') :
        """
        Returns False when the cancel option is selected
        """
        has_to_many = False
        while(True) :
            if has_to_many :
                custom_before_table = before_table+'To many options'
            else :
                custom_before_table = before_table

            res = ConsoleUtility.search_options(options, display_order, search_order, col_width, text, sort_key, search_text, custom_before_table, error, False)
            if res == False :
                return res
            elif len(res) > 1 :
                has_to_many = True
            else :
                return res

    
    @staticmethod
    def select_file(path='', question='', file_extension='',return_no_file=False) :
        if question == '' :
            question = 'Filename or path: '
        if file_extension != '' and not '.' in file_extension:
            file_extension = '.' + file_extension

        if path.startswith('& \'') and path.endswith('\'') : 
            path = path[2:]
        if (path.strip(' ').startswith('\'') and path.strip(' ').endswith('\'') or
            path.strip(' ').startswith('"') and path.strip(' ').endswith('"')) :
            path = path.strip(' ')[1:-1]
        if path == '/' or path == '\\' :
            path = './'
            
        if os.path.isfile(path) :
            return path
        else :
            if not path.endswith('/') and not path.endswith('\\') :
                path = path + '/'
            if not path.endswith('*') :
                path = path + '*' + file_extension
            else :
                path = path + file_extension

            options = glob.glob(path)
            if (len(options) < 1) :
                if return_no_file:
                    return False
                else:
                    print('\nNo file(s) Found, try again with a different filename or path')
                    return ConsoleUtility.select_file('./', question, file_extension,return_no_file)
            else :
                options.append('Other filename or path')
                options.append('Go back')
                selected_option = ConsoleUtility.select_option(options, question)

                if(selected_option[1] == len(options)-2) :
                    return ConsoleUtility.select_file(input(question), question, file_extension,return_no_file)
                if(selected_option[1] == len(options)-1) :
                    return None
                else :
                    return selected_option[0]

    @staticmethod
    def select_bool(question, options=['Yes', 'No'], text='Option: ', error='Invalid Option!') :
        return ConsoleUtility.select_option(options[:2], question, text, error)[1] < 1

    @staticmethod
    def enter_to_continue():
        input('Press enter to continue...')

    @staticmethod
    def input_string_contains(contains, text='Number: ', error='Invalid number!') :
        input_str = input(text)
        isValid = True

        for char in contains :
            if char in input_str and isValid :
                isValid = True
            else :
                isValid = False
                
        if isValid :
            return input_str
        else :
            print(error)
            return ConsoleUtility.input_string_contains(contains, text, error)

    @staticmethod
    def input_string_num(text ='Number: ', error='Invalid number!', min_amount = 1, max_amount = 0, check_letter = False) :
        input_str = input(text)

        numberCount = 0
        for char in input_str :
            if char.isdigit() :
                numberCount += 1

        check_amount = max_amount == 0 and numberCount >= min_amount or (numberCount <= max_amount and numberCount >= min_amount)
        check_contains_letter = check_letter == False or ConsoleUtility.string_contains_letter(input_str) 
                
        if check_amount and check_contains_letter :
            return input_str
        else :
            print(error)
            return ConsoleUtility.input_string_num(text, error, min_amount, max_amount)

    @staticmethod
    def string_contains_letter(input_str, error='Not a letter in input!') :
        for char in input_str :
            if char.isalpha():
                return True

        return False

    @staticmethod
    def is_int(input_str) :
        try:
            return int(input_str)
        except :
            return False