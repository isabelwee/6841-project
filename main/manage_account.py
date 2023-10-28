from connect_db import connect_to_db
from getpass import getpass
from bcrypt import hashpw, checkpw, gensalt
from main.manage_passwords import get_db_masterpwd
import sql_queries, sys


# Checks if user has a password vault
def account_exists():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(sql_queries.db_get_row(), ['~'])
    account = cur.fetchall()

    return False if not account else True

# Prompts user to create a new vault account
def create_account():
    print("It seems you don't have an account. Let's begin the registration process :)")
    print("---------------------------------------------------------------------------")

    print("Register an email: ")
    email = register_email()

    print("Create a master password. must include at least one capital letter, one number and one special character: ")
    hashed_password = register_password()

    db_create_account(email, hashed_password)
    print("Account successfully created!")
    print("---------------------------------------------------------------------------")

# Prompts user to register a valid email
def register_email():
    while True:
        email = input()
        # TODO: RESTORE AFTER TESTING!!!
        # if not re.search(r'@[a-z]+\.com', email):
        #     print("Incorrect email format, try again")
        # else:
        return email

# Prompts user to register a valid master password
def register_password():
    while True:
        password = getpass()
        # TODO: RESTORE AFTWR TESTING!!!
        # if len(password) < 8:
        #     print("Make sure your password is at least 8 letters")
        # elif re.search('[0-9]',password) is None:
        #     print("Make sure your password has a number in it")
        # elif re.search('[A-Z]',password) is None: 
        #     print("Make sure your password has a capital letter in it")
        # elif re.search('[!@#$%^&*()]',password) is None: 
        #     print("Make sure your password has a special character in it")
        # else:
        #     print("Re-enter password: ")
        #     password_validate = getpass()
        #     if (password != password_validate):
        #         print("Passwords do not match. Retry a new password:")
        #         break
        break

    return hashpw(password, gensalt())

# Creates an admin account in the database
def db_create_account(email, password):
    db = connect_to_db()
    cur = db.cursor()

    cur.execute(sql_queries.db_insert_row(), ['~', email, email, password])
    db.commit()

    cur.close()


# Checks if input is same as password stored in the database 
def login():
    # verify password
    input = getpass("Enter master password: ").encode()
    if not checkpw(input, get_db_masterpwd()):
        print("Incorrect password. Run the program again.")
        sys.exit(0)
    else:
        print("\033[1m================ Successfully logged in to the Vault ================\033[0m")
        print("Enter 'help' to view command options")