import datetime
# importing "copy" for copy operations
import copy
import pandas as pd
import matplotlib.pyplot as plt
file_name = "out.csv"
users_fm = "users.csv"
category_fm = "category.csv"


class User:
    def __init__(self, fullname, points0):
        self.fullname = fullname
        # __myActions = []
        __myTransactionData = pd.read_csv(file_name)
        self.BudgetController = BudgetController(__myTransactionData, self.fullname)
        self.points = points0  # Reward points

    def add_RewardPoints(self, pnt):
        self.points = self.points + pnt

    def print_RewardPoints(self):
        print("The balance of your reward points are: " + str(self.points))

    def save_records(self):
        self.UserTransactions.to_csv(file_name, index=False)


class Transaction:
    def __init__(self, date, amount, description, details):
        self.amount = amount
        self.date = date
        self.description = description
        self.details = details

    def setAmount(self, amount):
        self.amount = amount

    def getAmount(self):
        return self.amount

    def setDate(self, date):
        self.date = date

    def getDate(self):
        return self.date

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description


######## BudgetController  ################
class BudgetController:
    def __init__(self, UserTransactionsPd, user_fullname):
        self.UserTransactions = UserTransactionsPd
        self.expenses_category = pd.read_csv(category_fm)
        self.user_fullname = user_fullname

    def createTransaction(self, trans_type, date1, amount1, description1, details1):
        transaction_c = Transaction(date1, amount1, description1, details1)
        if trans_type == 'income':
            self.addIncome(transaction_c)
        else:
            self.addExpense(transaction_c)
        mainUser.BudgetController.save_records()

    def category_list(self):
        exp_c = self.expenses_category
        print(exp_c)
        number_of_rows = len(exp_c.index)
        inx = int(input("   Chose Category number "))
        while inx < 0 or inx >= number_of_rows:
            print(" Out of bounds. Chose Category number between 0 to ", number_of_rows - 1)
            inx = int(input("   Chose Category number: "))
        print("you chose num: ", inx)
        x = exp_c.loc[inx]
        y = x.values.tolist()
        cat_name = y[0]
        return cat_name

    def inputTransaction(self, trans_type):
        print('Enter Date:')
        date1 = self.dateInput()
        amount1 = input('Enter Amount:')
        if trans_type == 'income':
            description1 = input('Enter Description:')
        else:
            description1 = self.category_list()
        details1 = input('Enter Details:')
        self.createTransaction(trans_type, date1, amount1, description1, details1)
        print("  The record was successfully received!")

    def addIncome(self, income):
        self.UserTransactions = self.UserTransactions.append(
            # {'Date': '12/05/2022', 'Amount': '-500', 'Description': 'Food', 'Details': 'Burger'}, ignore_index=True)
            {'Date': income.date, 'Amount': int(income.amount),
             'Description': income.description, 'Details': income.details}, ignore_index=True)

    def addExpense(self, expense):
        neg_expense = copy.deepcopy(expense)
        neg_expense.amount = int(neg_expense.amount) * -1
        self.UserTransactions = self.UserTransactions.append(
            {'Date': neg_expense.date, 'Amount': int(neg_expense.amount),
             'Description': neg_expense.description, 'Details': neg_expense.details}, ignore_index=True)

    def printTransactions(self):
        print(self.UserTransactions)

    def dateInput(self):
        year = int(input('Enter a year '))
        while year < 2021:
            print("Wrong year number. Insert big then 2020")
            year = int(input('Enter a year '))
        month = int(input('Enter a month '))
        while month < 1 or month > 12:
            print("Wrong month number. Insert between 1-12")
            month = int(input('Enter a month '))
        day = int(input('Enter a day '))
        while day < 1 or day > 31:
            print("Wrong day number. Insert between 1-31")
            day = int(input('Enter a day '))
        return datetime.date(year, month, day)

    def account_Balance(self):
        total = self.UserTransactions['Amount'].sum()
        return total

    def show_Balance(self):
        print("Your Account Balance is: ", self.account_Balance(), "$")

    def save_records(self):
        self.UserTransactions.to_csv(file_name, index=False)

    def expenses_PieChart(self):
        ut0 = self.UserTransactions
        exp_sum = ut0.groupby('Description').Amount.sum().reset_index()
        exp_sum = exp_sum[exp_sum.Amount < 0]
        exp_sum['Amount'] = exp_sum['Amount'].abs()
        print(exp_sum)
        # Plot
        plt.pie(exp_sum['Amount'], labels=exp_sum['Description'],
                autopct='%1.1f%%', shadow=True, startangle=50)
        plt.show()

    # לעשות השוואה של הוצאה בקטגוריה מסויימת, ואם הוא ירד מקבל נקודות
    def exp_by_months(self, month, year):
        df = self.UserTransactions
        df.Date = pd.to_datetime(df.Date)
        # Create new columns
        df['day'] = df['Date'].dt.day
        df['month'] = df['Date'].dt.month
        df['year'] = df['Date'].dt.year

        df = df[df.Amount < 0]
        # df['Amount'] = df['Amount'].abs()

        df = df[df.month == month]
        df = df[df.year == year]
        df = df.groupby('Description').Amount.sum().reset_index()
        print(df)
        return df

    def expenses_compere(self):
        print("\nExpense analysis:")
        year = int(input('Enter a year '))
        while year < 2021:
            print("Wrong year number. Insert big then 2020")
            year = int(input('Enter a year '))
        month = int(input('Enter a month '))
        while month < 1 or month > 12:
            print("Wrong month number. Insert between 1-12")
            month = int(input('Enter a month '))

        print("\nExpenses by Description\nFor: " + str(month) + "/" + str(year))
        curr = self.exp_by_months(month, year)
        print("\nExpenses by Description\nFor: " + str(month - 1) + "/" + str(year))
        last_month = self.exp_by_months(month - 1, year)
        print("\nExpenses by Description\nFor: " + str(month) + "/" + str(year - 1))
        last_year = self.exp_by_months(month, year - 1)

        print("\nExpenses by specific Description")
        description1 = self.category_list()
        curr = curr[curr.Description == description1]
        curr = curr['Amount'].sum()
        last_month = last_month[last_month.Description == description1]
        last_month = last_month['Amount'].sum()
        last_year = last_year[last_year.Description == description1]
        last_year = last_year['Amount'].sum()

        print("*********************")
        print("\nExpenses by specific Description")
        print("The financial expenses in the " + str(description1) + " category are:")
        print("Current year - " + str(month) + "/" + str(year) + ": " + str(curr) + "$")
        print("Last month   - " + str(month - 1) + "/" + str(year) + ": " + str(last_month) + "$")
        print("Last year    -" + str(month) + "/" + str(year - 1) + ": " + str(last_year) + "$")

        if curr > last_month:
            print("\nWell done " + self.user_fullname + "!")
            print("This month's expenses in the " + str(description1) + " category are declining.")
            print("Compared to the previous month.")
            print("\nYou got 20 reward points!\n*****")
            return 20
        elif curr > last_year:
            print("\nWell done " + self.user_fullname + "!")
            print("This month's expenses in the " + str(description1) + " category are declining.")
            print("Compared to the previous year.")
            print("\nYou got 10 reward points!\n*****")
            return 10
        else:
            print("\nDear " + self.user_fullname + "!")
            print("This month's expenses in the " + str(description1) + " category are on the rise,")
            print("you should get better next month.")
            return 0

    def expenses_vs_incomes_Chart(self):
        ut0 = self.UserTransactions
        exp_sum = ut0.groupby('Description').Amount.sum().reset_index()
        exp_sum = exp_sum[exp_sum.Amount < 0]
        exp_sum['Amount'] = exp_sum['Amount'].abs()
        exp_sum = exp_sum['Amount'].sum()

        inc_sum = ut0.groupby('Description').Amount.sum().reset_index()
        inc_sum = inc_sum[inc_sum.Amount > 0]
        inc_sum = inc_sum['Amount'].sum()

        print("Total Expenses:", exp_sum, "$")
        print("Total Incomes:", inc_sum, "$")
        x = ["Incomes", "Expenses"]
        y = [inc_sum, exp_sum]
        plt.bar(x, y)
        plt.show()


def loginCheck(username0, password0):
    tmp = users[users.userName == username0]
    if tmp.empty:
        return False
    pass_check = tmp.iloc[-1]['password']
    if int(pass_check) == int(password0):
        return True
    else:
        return False


# Login function


def login():
    print('\n** Welcome to finvalue **\n')
    flag = 0
    while flag == 0:
        print('Enter your username:')
        x = input()
        print('Enter your password:')
        y = input()
        flag = loginCheck(x, y)
        if not flag:
            print("Wrong username or password. Try again\n")
        else:
            return x


def load_users():
    return pd.read_csv(users_fm)

def getPoint(us):
    tmp = users[users.userName == us]
    pot = tmp.iloc[-1]['points']
    return pot


def getFullname(us):
    tmp = users[users.userName == us]
    return tmp.iloc[-1]['fullname']


def menu_print():
    print("\n*** FinValue - Menu ***")
    print(
        "Choose action:\n 1- Insert Income\n 2- Insert Expense\n 3-Expenses Pie Chart\n 4- Expenses vs. Income")
    print(" 5- Print Transactions\n 6- Expenses Compere\n 7- Calc Balnce\n 8- Reward Points\n 0-Save & Exit")

def points_record(user, add_pts, curr_points):
    users_file = pd.read_csv(users_fm)
    user_name = user
    users_file.loc[users_file.userName == user_name, "points"] = add_pts + curr_points
    users_file.to_csv(users_fm, index=False)

# #####    Main     #######

users = load_users()
print("For demo:\n", users)

us = login()
file_name = "out_" + us + ".csv"
points = getPoint(us)
full_name = getFullname(us)
# Create mainUser
mainUser = User(full_name, points)

chose = 1  # 0 for off menu
print("\n\nWelcome ", mainUser.fullname)
mainUser.BudgetController.show_Balance()
mainUser.print_RewardPoints()
while chose != 0:
    chose_menu = int(input("\n  Show menu? 1 for yes. Other for no"))
    if chose_menu == 1:
        menu_print()
    chose = int(input("\n  Enter chose form the menu "))
    if chose == 1:
        mainUser.BudgetController.inputTransaction('income')
    elif chose == 2:
        mainUser.BudgetController.inputTransaction('expense')
    elif chose == 3:
        mainUser.BudgetController.expenses_PieChart()
    elif chose == 4:
        mainUser.BudgetController.expenses_vs_incomes_Chart()
    elif chose == 5:
        mainUser.BudgetController.printTransactions()
    elif chose == 7:
        mainUser.BudgetController.show_Balance()
    elif chose == 8:
        mainUser.print_RewardPoints()
    elif chose == 6:
        pts = mainUser.BudgetController.expenses_compere()
        if pts > 0:
            mainUser.add_RewardPoints(pts)
            mainUser.print_RewardPoints()
            points_record(us, pts, getPoint(us))
    elif chose == 0:
        print("Bye Bye")
