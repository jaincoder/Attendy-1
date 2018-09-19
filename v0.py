#!/usr/bin/python3
import time, datetime, random, string, csv, fileinput#, replit

def export(username, email, id, status):
    with open('attendance.csv', 'wt', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Name", "Email", "SID"])
    r = csv.reader(open('attendance.csv')) # Here your csv file
    lines = list(r)
    for l in lines:
        if l[0] == username:
            l.append(status)
    writer = csv.writer(open('attendance.csv', 'wt', newline=''))
    writer.writerows(lines)


def admin(n=3):
    prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
    return prefix

n_admin = 2

# 1 = absent, 2 = present, 3 = restart
def code_generator(length):
    original = admin(n_admin) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length-n_admin))
    restart = admin(n_admin) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length-n_admin))
    return [original, restart]

def check1(n, k, input, c_orig):
    now = time.time()
    code = code_generator(n)
    print (code)
    ''' check_code = input("What is the code on the screen? ") '''
    def compare(c_generated, c_input, length):
        matching = 0
        for i in range(len(c_generated)):
            if c_generated[i].lower() == c_input[i].lower():
                matching += 1
        return matching >= length - 2
    if check_code.lower() == code.lower():
        end = time.time()
        if round(end-now) < k:
            print ("Success! You have been marked as present.")
            #export(username, email, id, "Present")
            return 2
        else:
            print ("The attendance window for", str(datetime.datetime.now().strftime("%x")), "has already closed. It will open next on", future_date(7))
            #export(username, email, id, "Absent")
            return 1
    elif not compare(code, input, n):
        return 1
    else:
        return 3


def check2(n, k, input, c_orig):
        print ("Incorrect Code.")
        if compare(code, check_code, n) and not attempt:
            ''' check_code = input("What were the first and last digit of the code? ") '''
            if input.lower() == code[0].lower() + code[-1].lower():
                print ("Verified. Generating new code and restarting attendance tracker.")
                return True
            else:
                print ("Too many failed attempts. You have been marked absent.")
                #export(username, email, id, "Absent")
                return False
        else:
            print ("Too many failed attempts. You have been marked absent.")
            #export(username, email, id, "Absent")
            return False

def check3(n, k, input, c_restart):
    now = time.time()
    code = code_generator(n)
    print (code)
    ''' check_code = input("What is the code on the screen? ") '''
    def compare(c_generated, c_input, length):
        matching = 0
        for i in range(len(c_generated)):
            if c_generated[i].lower() == c_input[i].lower():
                matching += 1
        return matching >= length - 2
    if check_code.lower() == code.lower():
        end = time.time()
        if round(end-now) < k:
            print ("Success! You have been marked as present.")
            #export(username, email, id, "Present")
            return True
        else:
            print ("The attendance window for", str(datetime.datetime.now().strftime("%x")), "has already closed. It will open next on", future_date(7))
            #export(username, email, id, "Absent")
            return False
    else:
        return False


def future_date(p):
    today = datetime.datetime.now()
    diff = datetime.timedelta(days=p)
    future = today + diff
    return future.strftime("%m/%d/%Y")































'''

from tkinter import *
fields = ('Annual Rate', 'Number of Payments', 'Loan Principle', 'Monthly Payment', 'Remaining Loan')

def monthly_payment(entries):
   # period rate:
   r = (float(entries['Annual Rate'].get()) / 100) / 12
   print("r", r)
   # principal loan:
   loan = float(entries['Loan Principle'].get())
   n =  float(entries['Number of Payments'].get())
   remaining_loan = float(entries['Remaining Loan'].get())
   q = (1 + r)** n
   monthly = r * ( (q * loan - remaining_loan) / ( q - 1 ))
   monthly = ("%8.2f" % monthly).strip()
   entries['Monthly Payment'].delete(0,END)
   entries['Monthly Payment'].insert(0, monthly )
   print("Monthly Payment: %f" % float(monthly))

def final_balance(entries):
   # period rate:
   r = (float(entries['Annual Rate'].get()) / 100) / 12
   print("r", r)
   # principal loan:
   loan = float(entries['Loan Principle'].get())
   n =  float(entries['Number of Payments'].get())
   q = (1 + r)** n
   monthly = float(entries['Monthly Payment'].get())
   q = (1 + r)** n
   remaining = q * loan  - ( (q - 1) / r) * monthly
   remaining = ("%8.2f" % remaining).strip()
   entries['Remaining Loan'].delete(0,END)
   entries['Remaining Loan'].insert(0, remaining )
   print("Remaining Loan: %f" % float(remaining))

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1 = Button(root, text='Final Balance',
          command=(lambda e=ents: final_balance(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Monthly Payment',
          command=(lambda e=ents: monthly_payment(e)))
   b2.pack(side=LEFT, padx=5, pady=5)
   b3 = Button(root, text='Quit', command=root.quit)
   b3.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()
'''
