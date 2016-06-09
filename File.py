from pathlib import Path
import os
import os.path
import shutil


def perform_action(third_step:str, interesting_files:'list of interesting files')-> None:
    '''This function decides what action to perform on interesting files'''
    
    if third_step == 'P':
        print(*interesting_files,sep='\n')
    elif third_step == 'F':
        for x in interesting_files:
            open_file = x.open()
            print(x)
            print(open_file.readline().rstrip())
    elif third_step == 'D':
        for x in interesting_files:
            a=shutil.copy2(str(x),str(x)+'.dup')
            print(x)
    elif third_step == 'T':
        for x in interesting_files:
            os.utime(str(x))
            print(x)
    else:
        print("ERROR")
        letter = input(' ')
        perform_action(letter, interesting_files)
        
    

def subdir_search(user_input:'directory that user inputs')->['list of files in directory']:
    '''searches through directories and checks if they contain subdirectories, calls itself until reaches file'''
    list_of_files = []
    for x in user_input.iterdir():
        if x.is_dir():
            subdir_search(x)
        elif x.is_file():
            list_of_files.append(x)
    return list_of_files


def search_by_filename(file_name:str, file_dir:'directory that user inputs') ->['list of files that match input filename']:
    '''Searches through given directory for files that match filename input by user'''
    list_of_files = []
    try:
        files_in_dir = subdir_search(file_dir)
        for files in files_in_dir:
            if os.path.basename(str(files)) == file_name:
                list_of_files.append(files)

        return list_of_files

    except:
        print("ERROR")
        letter = input('Enter Letter: ')
        search_by_letter(letter, file_dir)

def search_by_extension(file_ext:str,file_dir:'directory that user inputs') ->['list of files that match input extension']:
    '''Searches through given directory for files that match extension input by user'''
    list_of_files = []
    try:
        files_in_dir = subdir_search(file_dir)
        if file_ext[0] != ".":
            file_ext = "." + file_ext
        for files in files_in_dir:
            name, ext = os.path.splitext(str(files)) 
            if ext == file_ext:
                list_of_files.append(files)
                
        return list_of_files

    except:
        print("ERROR")
        letter = input('Enter Extension: ')
        search_by_letter(letter, file_dir)
        

def search_by_bytes(file_size:str, file_dir:'directory that user inputs')->['list of files of bytes greater than input size']:
    '''Searches through given directory for files greater than the amount of bytes input by user'''
    list_of_files = []
    try:
        files_in_dir = subdir_search(file_dir)
        for files in files_in_dir:
            if int(os.path.getsize(str(files))) > int(file_size):
                list_of_files.append(files)
                
        return list_of_files

    except:
        print("ERROR")
        letter = input('Enter Bytes: ')
        search_by_letter(letter, file_dir)
        

def search_by_letter(second_step:str, user_input:'directory that user inputs')->['list of interesting files']:
    '''Takes in second input by user and calls appropriate function depending on letter'''
    split_list = second_step.split(' ', maxsplit=1)
    if len(split_list) == 2:

        if split_list[0]=='N':
            interesting_files = search_by_filename(split_list[1],user_input)
            return interesting_files
       
        elif split_list[0]=='E':
            interesting_files = search_by_extension(split_list[1],user_input)
            return interesting_files
        
                
        elif split_list[0]=='S':
            interesting_files = search_by_bytes(split_list[1],user_input)
            return interesting_files


        
    
def main_function():
    user_input = Path(input('Enter Path: '))
    if user_input.exists() and user_input.is_dir():
            second_step = input('N: Search For Name, E: Search by extension or S: Search by bytes: ')
            interesting_files = search_by_letter(second_step, user_input)
            while interesting_files == None:
                print('ERROR')
                second_step = input('N: Search For Name, E: Search by extension or S: Search by bytes: ')
                interesting_files = search_by_letter(second_step, user_input)
            third_step = input('P: Prints Path to console or F: Reads First Line of File or D: Makes Duplicate copy of the File or T: Modifies the timestamp:  ')
            perform_action(third_step, interesting_files)
                
    else:
        print("ERROR")
        main_function()

if __name__ =='__main__':
    main_function()
