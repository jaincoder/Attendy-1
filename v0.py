#!/usr/bin/python3
import time, datetime, random, string, csv, fileinput#, replit

def initialize_csv(username, email, id):
    with open('attendance.csv', 'wt', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["Name", "Email", "SID"])
        filewriter.writerow([username, email, id])
    r = csv.reader(open('attendance.csv')) # Here your csv file
    lines = list(r)
    for day in range(1, 20):
            lines[0].append("Week   " + str(day))
    writer = csv.writer(open('attendance.csv', 'wt', newline=''))
    writer.writerows(lines)

def export(username, status):
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

def code_generator(length, n_admin):
    original = admin(n_admin) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length-n_admin))
    restart = admin(n_admin) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length-n_admin))
    return [original, restart]

# 1 = absent, 2 = present, 3 = restart [logic for functions compare, check1, check2, check3]
def compare(c_orig, c_input, length):
    matching = 0
    if len(c_orig) == len(c_input):
        for i in range(len(c_orig)):
            if c_orig[i].lower() == c_input[i].lower():
                matching += 1
    else:
        return 100
    return matching >= length - 2

def check1(n, k, input, c_orig):
    now = time.time()
    input, c_orig = str(input), str(c_orig)
    if input.lower() == c_orig.lower():
        end = time.time()
        if round(end-now) < k:
            return 2
        else:
            return 1
    elif not compare(c_orig, input, n) or compare(c_orig, input, n) == 100:
        return 1
    else:
        return 3

def check2(n, k, input, c_orig):
    input, c_orig = str(input), str(c_orig)
    if compare(c_orig, input, n):
        if input.lower() == c_orig[0].lower() + c_orig[-1].lower():
            return True
        else:
            return False
    else:
        return False

def check3(n, k, input, c_restart):
    now = time.time()
    input, c_restart = str(input), str(c_restart)
    if input.lower() == c_restart.lower():
        end = time.time()
        if round(end-now) < k:
            return True
        else:
            return False
    else:
        return False

def future_date(p):
    today = datetime.datetime.now()
    diff = datetime.timedelta(days=p)
    future = today + diff
    return future.strftime("%m/%d/%Y")


print (check1(6, 5, "fqewrs", "fqewrs"))
