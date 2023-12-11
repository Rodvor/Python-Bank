import os, readline
from time import sleep

def loginView(): #Login View, allows user to login

    while True:

        clear()
        print('Python Bank - Login')
        print('-------------------')
        name = input('Name: ')

        if name.replace(' ','') == '': break #Exit program if name is empty

        password = input('Password: ')

        if loginRequest(name, password): 

            if name.lower() == "admin": adminView()
            else: accountView(name) 
        
        else:

            clear()
            print('Invalid Credentials!')
            sleep(1)
    
def accountView(name):
    
    leaveView = False

    account = Account(name)

    while not leaveView:
        
        #Draw main menu for user
        option = drawMenu(f'Python Bank - Account: {account.name}\nBalance: {account.balance:,} €', ['Transfer Money','Change Password','Exit'])

        clear()
        
        if option == 1:
            
            print('Python Bank - Transfer Money')
            print('----------------------------')
            print(f'Balance: {account.balance:,} €')
            print('----------------------------')
            receiver = input('Receiver: ')
            amount = input('Amount: ')

            result = account.transfer(receiver, amount)

            clear()
            print(result)
            sleep(1)


        elif option == 2:

            print('Python Bank - Change Password')
            print('-----------------------------')
            oldPass = input('Old Password: ')
            newPass = input('New Password: ')

            clear()

            if oldPass == account.password:

                account.password = newPass
                account.save()

                print('Password changed!')
            
            else:

                print('Incorrect Password!')
            
            sleep(1)


        elif option == 3:
            leaveView = True

        else:

            print("Invalid option!")
            sleep(1)

def adminView():

    leaveView = False

    while not leaveView:

        option = drawMenu(f'Python Bank - Admin Settings', ['Create Account','Delete Account','Exit'])
        
        clear()

        if option == 1:
            
            print('Python Bank - Create Account')
            print('----------------------------')
            name = input('Name: ')
            password = input('Password: ')

            clear()

            if Account(name).create(password):

                print('Account created!')

            else:

                print('Account already exists!')
            
            sleep(1)


        elif option == 2:
            pass

        elif option == 3:
            leaveView = True

        else:

            print("Invalid option!")
            sleep(1)


class Account:

    def __init__(self, name) -> None:
        
        self.name = name
        self.path = f'Accounts/{self.name}'
        self.exists = os.path.exists(self.path)

        if self.exists:
            
            file = readFile(self.path)
            data = file.split('\n') #Data is split in file at a certain order, separated by a backspace

            self.balance = int(data[0])
            self.password = data[1]
    
    def create(self, password) -> bool:

        if not self.exists:

            if self.name == 'Bank': self.balance = 1_000_000_000
            else: self.balance = 0

            self.password = password

            self.save()

            return True

        return False
    
    def transfer(self, receiver, amount) -> str:
        
        try: amount = int(amount)
        except: return 'Amount must be numerical!'

        receiver = Account(receiver)

        if not receiver.exists:

            return 'Receiver account does not exist!'

        if amount > self.balance:

            return 'Insufficient funds!'

        if amount < 0:

            return 'Amount must be positive!'
        
        self.balance -= amount
        receiver.balance += amount

        self.save()
        receiver.save()

        return f'Successfully transferred {amount}€ to {receiver.name}!'
    
    def save(self): #Save file ie. update account file

        text = f"{self.balance}\n{self.password}"
        writeFile(self.path, text)




def loginRequest(name, password) -> bool:

    account = Account(name)

    if not account.exists:
        return False
    
    if account.password != password:
        return False
    
    return True

def drawMenu(title, options) -> int: #Title, if multiple can be split by \n. options in string list

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
    
    

#Useful Functions

def clear(): #Clear screen
    os.system('clear')

def readFile(path) -> str:
    with open(path, mode='r') as file:
        return(file.read())
    
def writeFile(path, text):
    with open(path, mode='w') as file:
        file.write(text)



# Program Start

def main():

    if not os.path.exists('Accounts'): #Creates Accounts folder if it does not exist
        os.mkdir('Accounts')

    if not os.path.exists('Accounts/Admin'): #Creates Admin account with password 0000 if it does not exist
        Account('Admin').create('0000')

    if not os.path.exists('Accounts/Bank'): #Creates Bank account with password 0000 if it does not exist
        Account('Bank').create('0000')

    loginView()

if __name__ == '__main__':
    main()