import customtkinter as ctk
import random
import csv

class ErrorWindow:
  def __init__(self, root2, title, message):
    self.window = ctk.CTkToplevel(root2)
    self.window.title(title)
    self.window.geometry("500x200")

    self.window.lift()
    self.window.focus_force()

    self.title_label = ctk.CTkLabel(self.window, text=title, font=("Arial", 16))
    self.title_label.pack(pady=20)

    self.message_label = ctk.CTkLabel(self.window, text=message, font=("Arial", 12))
    self.message_label.pack(pady=10)

    self.ok_button = ctk.CTkButton(self.window, text="OK", command=self.window.destroy)
    self.ok_button.pack(pady=20)

class Account:
  def __init__(self, account_number, balance=0, cust_name='', filename="Cust_info.csv", root2=None):
    self.account_number = int(account_number)
    self.balance = float(balance)
    self.cust_name = cust_name
    self.filename = filename
    self.root2 = root2

  def deposit(self, dep_amount, root=None):
    try:
      if dep_amount >= 1000000:
        print(f"root is: {self.root}")
        ErrorWindow(self.root2, "Deposit Error","Maximum amount you can deposit via\nthe counter is a million for a single transaction.")
      elif dep_amount < 0:
        ErrorWindow(self.root2, "Deosit Error","You cannot deposit a negative amount.")
      else:
        self.balance += dep_amount
        ErrorWindow(self.root2, "Deposit Completed Successfully",f"Ksh. {dep_amount} deposited succesfully. New balance is Ksh. {self.balance}")
        self.update_balance()
    except ValueError:
      print("Please enter a valid figure.")

  def withdraw(self, draw_amount):
    trans_cost = 115
    withdrawable_amount = self.balance - 115
    if draw_amount > self.balance:
      ErrorWindow(self.root2, "Withdrawal Error","Withdrawal amount cannot be greater than the account balance.")
    elif draw_amount > 1000000:
      ErrorWindow(self.root2, "Withdrawal Error","Maximum amount you can withdraw via\nthe counter is a million for a single transaction.")
    elif draw_amount > withdrawable_amount:
      ErrorWindow(self.root2, "Withdrawal Error","You cannot withdraw more than your withdrawal limit.")
    else:
      self.balance -= (draw_amount + trans_cost)
      ErrorWindow(self.root2, "Withdrawal Completed Successfully",f"Ksh.{draw_amount} withdrawn succesfully. Tracsaction cost = {trans_cost}. New balance is Ksh.{self.balance}")
      self.update_balance()
  
  def update_balance(self):
    try:
      with open(self.filename) as file:
        reader = csv.reader(file)
        rows = list(reader)

      for row in rows:
        if row and int(row[2]) == self.account_number:
          row[4] = str(self.balance)
          break
      
      with open(self.filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
      print("Account balance Updated successfully.")
    except FileNotFoundError:
      ErrorWindow(self.root2, "File Error","Customer  file not found.")
    except Exception as e:
      ErrorWindow(self.root2, "Error",f"Error updating file: {e}")

  def show_balance(self):
    return f"Your current account balance is Ksh.{self.balance}"
  
  def check_acc_no(self):
    return f"Your account number is{self.account_number}"

class Customer(Account):
  def __init__(self, filename, balance=0):
    super().__init__(0, balance)
    self.balance = balance
    self.cust_info = []
    self.filename = filename
    self.load_current_cust()

  def get_acc_number(self, id_no):
    for line in self.cust_info:
      if int(line['id_no']) == id_no:
        print(f"Your Account number is:{line['acc_number']}".strip())
        return line['acc_number']
    ErrorWindow(self.root2,f"Customer with ID number{id_no} was not found.\nCheck the ID number then try again.")

  def add_new_cust(self, id_no, cust_name, pass_wd, first_deposit=0):
    try:
      if len(str(id_no)) < 8 or len(str(id_no)) > 9:
            ErrorWindow(self.root2, "ID Error","Please enter a valid Id number.")
            return
      
      self.load_current_cust()

      for customer in self.cust_info:
          if int(customer['id_no']) == id_no:
            ErrorWindow(self.root2, "ID Error","A customer with the provided ID number already exists in our database.\nKindly check your ID number then try again.")
            return

      acc_number = random.randint(14618500000, 14618599999)
      while acc_number in self.cust_info:
        acc_number = random.randint(14618500000, 14618599999)

      with open(self.filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_no, cust_name, acc_number, pass_wd, first_deposit])
      self.load_current_cust()
      ErrorWindow(self.root2, "Account Created",f"Congratulations {cust_name}!!\nYou are now a member of TrustWell Bank.\nYour new account number is{acc_number}")
      return

    except ValueError:
      ErrorWindow(self.root2, "Input Error","Invalid input. Kindly try again.")
    except Exception as e:
      ErrorWindow(self.root2, "Error", f"Error in creating account: {e}")

  def load_current_cust(self):
    self.cust_info = []
    try:
      with open(self.filename, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
          if len(line) < 5:
            continue
          id_no, cust_name, acc_number, pass_wd, self.balance = line
          self.cust_info.append({"id_no": id_no, "cust_name": cust_name, "acc_number": acc_number,
          "pass_wd": pass_wd, "acc_balance": self.balance})
      
    except FileNotFoundError:
      ErrorWindow(self.root2, "File Error","Customer file not found.")
    except Exception as e:
      ErrorWindow(self.root2, "Error", f"Error loading customer file: {e}")
  
  def find_customer(self, id_no, pass_wd):
    for cust in self.cust_info:
      if int(cust['id_no']) == id_no and cust['pass_wd'] == pass_wd:
        return cust
    return None

class BankGUI:
  def __init__(self, root):
    self.root = root
    self.root2 = root2
    self.root.title("TrustWell Bank Management System.")
    self.root.geometry("550x500")

    self.valid_cust = Customer("Cust_info.csv", balance=0)
    self.account = None #Holds  account object one customer logs in
    self.create_widgets()
  
  def create_widgets(self):
    self.label = ctk.CTkLabel(self.root, text="Welcome to TrustWell Bank", font=("Arial", 30))
    self.label2 = ctk.CTkLabel(self.root, text="Are you a/an", font=("Arial", 22))
    self.label.pack(pady=15)
    self.label2.pack(pady=15)

    self.new_customer_button = ctk.CTkButton(self.root, text="New Customer", command=self.new_customer, width=80, height=50, corner_radius=30, hover_color="green")
    self.new_customer_button.pack(pady=20)

    self.existing_cust_button = ctk.CTkButton(self.root, text="Existing Customer", command=self.existing_customer, width=100, height=50, corner_radius=30, hover_color="green")
    self.existing_cust_button.pack(pady=20)

  def new_customer(self):
    self.clear_widgets()

    self.new_cust_frame = ctk.CTkScrollableFrame(root, width=230, height=250, label_text="Customer Onboarding")
    self.new_cust_frame.pack(pady=20)

    self.label = ctk.CTkLabel(self.new_cust_frame, text="Enter your National ID No:", font=("Arial", 12))
    self.label.pack(pady=5)

    self.id_entry = ctk.CTkEntry(self.new_cust_frame)
    self.id_entry.pack(pady=5)

    self.name_label = ctk.CTkLabel(self.new_cust_frame, text="Enter your Name:", font=("Arial", 12))
    self.name_label.pack(pady=5)

    self.name_entry = ctk.CTkEntry(self.new_cust_frame)
    self.name_entry.pack(pady=5)

    self.pass_wd_label = ctk.CTkLabel(self.new_cust_frame, text="Create a password.", font=("Arial", 12))
    self.pass_wd_label.pack(pady=5)

    self.pass_wd_entry = ctk.CTkEntry(self.new_cust_frame)
    self.pass_wd_entry.pack(pady=5)

    self.deposit_label = ctk.CTkLabel(self.new_cust_frame, text="Enter First deposit (Ksh):", font=("Arial", 12))
    self.deposit_label.pack(pady=5)

    self.deposit_entry = ctk.CTkEntry(self.new_cust_frame)
    self.deposit_entry.pack(pady=5)

    self.submit_button = ctk.CTkButton(self.root, text="Create Account", command=self.create_account)
    self.submit_button.pack(pady=15)

    self.back_btn = ctk.CTkButton(self.root, text="Back", command=self.go_back_to_main_menu)
    self.back_btn.pack(pady=22)

  def create_account(self):
    id_no = int(self.id_entry.get())
    cust_name = self.name_entry.get().strip()
    pass_wd = self.pass_wd_entry.get().strip()
    first_deposit = float(self.deposit_entry.get() or 0)

    if cust_name:
      self.valid_cust.add_new_cust(id_no, cust_name, pass_wd, first_deposit)
      self.go_to_login()
    else:
      ErrorWindow(self.root, "Input Error", "Please provide your name.\nIt is a mandatory requirement to open an account.")

  def existing_customer(self):
    self.clear_widgets()

    self.label = ctk.CTkLabel(self.root, text="Enter your National ID No:", font=("Arial", 12))
    self.label.pack(pady=5)

    self.id_entry = ctk.CTkEntry(self.root)
    self.id_entry.pack(pady=5)

    self.label2 = ctk.CTkLabel(self.root, text="Enter your Password:", font=("Arial", 12))
    self.label2.pack(pady=5)

    self.pass_wd_entry = ctk.CTkEntry(self.root, show="*")
    self.pass_wd_entry.pack(pady=5)

    self.submit_button = ctk.CTkButton(self.root, text="Log in", command=self.login_customer)
    self.submit_button.pack(pady=20)

    self.back_btn = ctk.CTkButton(self.root, text="Back", command=self.go_back_to_main_menu)
    self.back_btn.pack(pady=30)

  def login_customer(self):
    try:
      id_no = int(self.id_entry.get())
      pass_wd = self.pass_wd_entry.get()
      customer = self.valid_cust.find_customer(id_no, pass_wd)
      if customer:
        self.account = Account(customer['acc_number'], float(customer['acc_balance']), customer['cust_name'], root2=self.root2)
        self.customer_dashboard(customer['cust_name'])
      else:
        ErrorWindow(self.root, "Login Error", "Invalid ID No or Password")
    except ValueError:
      ErrorWindow(self.root, "Value Error", "The ID No Field can only accomodate numerical Digits.")
  
  def customer_dashboard(self, name):
    self.clear_widgets()

    if self.account is None:
      ErrorWindow(self.root, "Account Error", "No Account loded.\nKindly sign in again")
      return

    self.label = ctk.CTkLabel(self.root, text=f"Welcome back, {name}!", font=("Arial", 25))
    self.label.pack(pady=15)

    self.account_number_label = ctk.CTkLabel(self.root, text=f"Account Number\n {self.account.account_number}", font=("Britanic Bold", 23))
    self.account_number_label.pack(pady=15)

    self.label2 = ctk.CTkLabel(self.root, text=f"What would you like to do Today?", font=("Arial", 18))
    self.label2.pack(pady=15)

    self.deposit_button = ctk.CTkButton(self.root, text="Deposit", command=self.deposit, width=20)
    self.deposit_button.pack(pady=10)

    self.withdraw_button = ctk.CTkButton(self.root, text="Withdraw", command=self.withdraw, width=20)
    self.withdraw_button.pack(pady=10)

    self.balance_button = ctk.CTkButton(self.root, text="Check my Account Blance", command=self.check_balance, width=20)
    self.balance_button.pack(pady=10)

    self.logout_button = ctk.CTkButton(self.root, text="Logout", command=self.go_back_to_main_menu, width=20)
    self.logout_button.pack(pady=10)

  def deposit(self):
    self.clear_widgets()

    self.label = ctk.CTkLabel(self.root, text="Enter the amount you would like to dwposit:", font=("Arial", 12))
    self.label.pack(pady=5)

    self.deposit_entry = ctk.CTkEntry(self.root)
    self.deposit_entry.pack(pady=5)

    self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.submit_deposit)
    self.submit_button.pack(pady=15)

    self.back_btn = ctk.CTkButton(self.root, text="Back", command=self.back_to_customer_dashboard)
    self.back_btn.pack(pady=20)

  def submit_deposit(self):
    dep_amount = float(self.deposit_entry.get())
    self.account.deposit(dep_amount, self.root)
    self.back_to_customer_dashboard()
  
  def withdraw(self):
    self.clear_widgets()

    self.label = ctk.CTkLabel(self.root, text="Enter the amount you would like to withdraw:", font=("Arial", 12))
    self.label.pack(pady=5)

    self.withdraw_entry = ctk.CTkEntry(self.root)
    self.withdraw_entry.pack(pady=5)

    self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.submit_withdraw)
    self.submit_button.pack(pady=15)

    self.back_btn = ctk.CTkButton(self.root, text="Back", command=self.back_to_customer_dashboard)
    self.back_btn.pack(pady=20)

  def submit_withdraw(self):
    draw_amount = float(self.withdraw_entry.get())
    self.account.withdraw(draw_amount)
    self.back_to_customer_dashboard()

  def check_balance(self):
    balance_info = self.account.show_balance()
    ErrorWindow(self.root, "Account Balance", balance_info)
  
  def check_acc_number(self):
    acc_info = self.account.check_acc_no()
    ErrorWindow(self.root, "Account Number", acc_info)

  def go_to_login(self):
    self.clear_widgets()
    self.existing_customer()

  def back_to_customer_dashboard(self):
    self.clear_widgets()
    if self.account:
      customer_name = self.account.cust_name
      self.customer_dashboard(customer_name)

  def go_back_to_main_menu(self):
    self.clear_widgets()
    self.create_widgets()
    
  def clear_widgets(self):
    for widget in self.root.winfo_children():
      widget.destroy()

if __name__ == "__main__":
  root2 = ctk.CTk()
  root = ctk.CTk()
  bank_gui = BankGUI(root)
  root.mainloop()