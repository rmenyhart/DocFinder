import string
from ctypes import windll
import os
import textract

def getDrives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def traverseDirectory(path, keywords, echo):
    found = []
    if (echo):
        print('\tSearching directory: ' + path)
    try:
        for file in os.listdir(path):
            try:
                if (echo):
                    print('\t\tFile: ' + file)
                d = os.path.join(path, file)
                if os.path.isdir(d) and os.access(d, os.R_OK):
                    found.extend(traverseDirectory(d, keywords, echo))
                else:
                    if (file.endswith('.xlsx') or file.endswith('.doc')):
                        text = textract.process(d);
                        text = text.decode("utf-8")
                        good = True
                        for keyword in keywords:
                            if not(keyword in text):
                                good = False
                                break
                        if (good):
                            found.append(d)
                    elif file.endswith('.pdf'):
                        os.system('pdf2text/pdf2text.exe -o ./pdfs ' + d + '> /dev/null 2>&1')
                        textfile = open('./pdfs/' + file[:-3] + 'txt', 'r')
                        text = textfile.read();
                        good = True
                        for keyword in keywords:
                            if not(keyword in text):
                                good = False
                                break
                        if (good):
                            found.append(d)            
            except Exception as e:
                #print(e)
                pass
    except Exception as e:
        #print(e)
        pass
    return found;
        
def main():
    foundFiles = []
    drives = getDrives()
    print('Please type the keywords separated by spaces:')
    keywords = input().split()
    print('Would you like to follow the traversal of the file system?[Y/N]')
    echo = False
    if (input().upper() == 'Y'):
        echo = True
    if (echo):
        print('Found drives: ' + str(drives))
    drives = ['P']
    for drive in drives:
        print('Searching drive ' + drive)
        foundFiles = traverseDirectory(drive + ':\\', keywords, echo)
        print('Found files:')
        for path in foundFiles:
            print(path)

if __name__ == '__main__':
    main()