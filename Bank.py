import os, readline
from time import sleep

def loginView():

    leaveView = False

    while not leaveView:

        clear()
        print('Python Bank - Login')
        print('-------------------')
        name = input('Name: ')
        password = input('Password: ')

        if loginRequest(name, password):

            accountView(name)
        
        else:

            clear()
            print('Invalid Credentials!')
            sleep(1)
    
def accountView(name):
    
    leaveView = False

    account = Account(name)

    while not leaveView:

        option = drawScreen(f'Python Bank - Account: {account.name}\nBalance: {account.balance} €', ['Transfer Money','Change Password','Exit'])

        clear()

        
        if option == 1:
            pass 

        elif option == 2:
            pass

        elif option == 3:
            leaveView = True

        else:

            print("Invalid option!")
            sleep(1)



class Account:

    def __init__(self, name):
        
        self.name = name
        self.path = f'Accounts/{self.name}'
        self.exists = os.path.exists(self.path)

        if self.exists:
            
            file = readFile(self.path)
            data = file.split('\n')

            self.balance = int(data[0])
            self.password = data[1]
    
    def create(self, password):

        if not self.exists:

            self.balance = 0
            self.password = password

            self.save()

            return True

        return False
    
    def save(self):

        text = f"{self.balance}\n{self.password}"
        writeFile(self.path, text)

def loginRequest(name, password):

    account = Account(name)

    if not account.exists:
        return False
    
    if account.password != password:
        return False
    
    return True

def drawScreen(title, options):

    clear()

    titles = title.split('\n')
    length = len(max(titles, key=len))

    for i in titles:
        print(i)
        print('-' * length)

    for n, i in enumerate(options,1):
        print(f"[{n}] {i}")
    
    print('-' * length)
    option = input("> ")

    try:

        option = int(option)

        if option <= len(options):
            return option
    
    except:
        pass

    return 0
    
    



def clear():
    os.system('clear')


def readFile(path):
    with open(path, mode='r') as file:
        return(file.read())
    
def writeFile(path, text):
    with open(path, mode='w') as file:
        file.write(text)

if not os.path.exists('Accounts'):
    os.mkdir('Accounts')

loginView()