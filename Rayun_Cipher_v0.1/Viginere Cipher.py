import random
import os
import subprocess
import sys
import string

os.chdir("C:\\Users\\Michelle\\OneDrive - DEPED REGION 5-2\\Documents\\Rajah\\Personal Projects\\Viginere Cipher")

"""def running():
    # This function returns True if the script is running in a Command Prompt window
    return os.name == 'nt' and 'PROMPT' in os.environ
if not running():
    # If the script is not running in a Command Prompt window, relaunch it in a new Command Prompt window
    subprocess.run(['start', 'cmd', '/k', 'python', __file__], shell=True)
    sys.exit()"""

def get_Row(*args):
    global Viginere_Table
    cipher_Txt = args[1];
    
    for k in range(len(Viginere_Table)):
        if Viginere_Table[k][args[0]] == cipher_Txt[args[2]]:
            return k;
def get_Column(*args):
    global Viginere_Table
    key = args[0];
    j = args[1] % len(key);
    column = Viginere_Table[0].index(key[j]);
    return column;
def generate_Viginere_Table(randomize_Amt, numbers_Query, symbols_Query, capitalization_Query, whitespace_Query):
    
    alphabet_Lowercase = list(string.ascii_lowercase)
    alphabet_Uppercase = list(string.ascii_uppercase)
    numbers = list(string.digits)
    symbols = list(string.punctuation)
    whitespace = list(string.whitespace)
    cipher_Elements = alphabet_Lowercase;
    if numbers_Query:
        cipher_Elements.extend(numbers);
    if symbols_Query:
        cipher_Elements.extend(symbols);
    if capitalization_Query:
        cipher_Elements.extend(alphabet_Uppercase);
    if whitespace_Query:
        cipher_Elements.append(' ')
    for i in range(random.randint(500, 1000) + abs(randomize_Amt)):
        letter_Index = cipher_Elements.index(random.choice(cipher_Elements));
        j = cipher_Elements[letter_Index];
        cipher_Elements.remove(j);
        cipher_Elements.insert(random.randint(0, len(cipher_Elements) - 1), j);
    
    f = open("Viginere table.txt", 'w');

    for x in range(len(cipher_Elements)):
        
        y = cipher_Elements[0];
        cipher_Elements.pop(0);
        cipher_Elements.append(y);
        for z in range(len(cipher_Elements)):
            f.write(cipher_Elements[z]);
        f.write("\n");
        print(cipher_Elements);
        print("-----------------------------------------------------");
    f.close;
    print("Viginere Table Generated");
def encrypt(plain_Txt, key):
    global Viginere_Table
    
    plain_Txt = list(plain_Txt)
    key = list(key)
    cipher_Txt = ""

    for i in range(len(plain_Txt)):
        try:
            row = Viginere_Table[0].index(plain_Txt[i]);
            j = i % len(key)
            column = Viginere_Table[0].index(key[j]);
            cipher_Txt += Viginere_Table[row][column];
        except:
            cipher_Txt += plain_Txt[i];   
    print(cipher_Txt);
    return cipher_Txt;
def decrypt(cipher_Txt, key):
    global Viginere_Table

    cipher_Txt = list(cipher_Txt)
    key = list(key)
    plain_Txt = ""

    for i in range(len(cipher_Txt)):
        try:
            column = get_Column(key, i)
            row = get_Row(column, cipher_Txt, i)
            plain_Txt += Viginere_Table[row][0];
        except:
            plain_Txt += Viginere_Table[row][0];
    print(plain_Txt);
    return(plain_Txt);
def line():
    print("[x----------------------------------------------------------------------x]")
def clear():
    os.system('cls');
def process_Input(user_Input, *args):
    global encrypt_Query, decrypt_Query, cipher_Txt, menu, run

    clear();

    if user_Input == 'e' or user_Input == 'E':
        encrypt_Query = True;
        decrypt_Query = False;
        menu = False;
    elif user_Input == 'd' or user_Input == 'D':
        decrypt_Query = True;
        encrypt_Query = False;
        menu = False;
    elif user_Input == 'g' or user_Input == 'G':
        randomize_Amt = int(input("Input an integer for randomization: "));
        clear();
        generate_Viginere_Table(randomize_Amt, True, True, True, True);
    elif user_Input == 'Y' or user_Input == 'y' and decrypt_Query:
        f = open("Decrypted Text.txt", 'a');
        f.write(args[0])
        f.write("\n[x------------------------------------------------------------------------------------------------------x]\n");
        f.close
    elif user_Input == 'Y' or user_Input == 'y' and encrypt_Query:
        f = open("Encrypted Text.txt", 'a');
        f.write(args[0] + "\nEncryption key: %s" % args[1]);
        f.write("\n[x------------------------------------------------------------------------------------------------------x]\n");
        f.close
    elif user_Input == 'm' or user_Input == 'M':
        menu = True;
        encrypt_Query = False;
        decrypt_Query = False;
    elif user_Input == 'q' or user_Input == 'Q':
        menu = False;
        run = False;

run = True;
menu = True;
encrypt_Query = False;
decrypt_Query = False;

f = open("Viginere table.txt", 'r');
cipher_Key = f.readlines();
Viginere_Table = [];

for i in range(len(cipher_Key)):
    current_Line = cipher_Key[i][:-1];
    Viginere_Table.append(list(current_Line));

while run:
    while (menu):
        print("E: Encrypt");
        print("D: Decrypt");
        print("G: Generate Viginere Table");
        print("L: Load Viginere Table [Not supported]");
        print("Q: Quit");
        query = input("> ")
        process_Input(query);
    clear();
    while (encrypt_Query):
        plain_Txt = input("Please enter your Plain Text:\n")
        if plain_Txt == 'm' or plain_Txt == 'M':
            process_Input('m');
            continue;
        key = input("Please enter encryption key:\n");
        if key == 'm' or key == 'M':
            process_Input('m');
            continue;
        line();
        cipher_Txt = encrypt(plain_Txt, key);
        line();
        save_Query = input("Would you like to save it to the .txt file? [Y/N]: ");
        process_Input(save_Query, cipher_Txt, key);
        clear();
    clear();
    while (decrypt_Query):
        cipher_Txt = input("Please enter your Cipher Text:\n");
        if cipher_Txt == 'm' or cipher_Txt == 'M':
            process_Input('m');
            continue;
        key = input("Please enter encryption key:\n");
        if key == 'm' or key == 'M':
            process_Input('m');
            continue;
        line();
        plain_Txt = decrypt(cipher_Txt, key);
        line();
        save_Query = input("Would you like to save it to the .txt file? [Y/N]: ");
        process_Input(save_Query, plain_Txt);
        clear();
quit();