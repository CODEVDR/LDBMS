import os
import datetime
from mymodules import*

print("\t\t\t\t\tLibrary Database Management System")
print("connecting server..")
cs = connect_server()
while True:
    os.system('color 2')
    print("1. Storing Book Data.")
    print("2. Student borrowing a Book.")
    print("3. Book Damaged or book lost by student.")
    print("4. Update Book Name or Book Number.")
    print("5. To see Books borrowing history of Student.")
    print("6. Student Returned Book/Books.")
    n = input("Select and Enter : ")
    if n.isdigit():
        if int(n[0]) <= 6 and int(n[0]) > 0:
            n = n[0]
        else:
            print("Enter a valid option")
    else:
        print("Enter A valid option")
    if n == "1":  # Tested OK
        book_nm = input("Enter Book Name : ")
        book_no = int(input("Enter Book ID : "))
        book_p = float(input("Enter Book Price : "))
        qty = int(input("Enter Quantity Of Books : "))
        cnecn = connect_database(cs[1])
        # storing book data
        try:  # for creating Table in Sql
            q1 = f"""
            create table if not exists books(
                Book_Name varchar(50),
                Book_ID int(50) primary key,
                Book_Price float(50),
                qts int(25)
            );
            """
            execute_query(cnecn, q1)
        except:
            print("An Unexpected Error Ouccured...Please Try Again...")
        try:
            q0 = f"""use gnps;"""
            q2 = f"""insert into books values("{book_nm}",{book_no},{book_p},{qty});"""
            execute_query(cnecn, q0)
            execute_query(cnecn, q2)
        except:
            print("Somethhing Went Wrong Please try again..")
            pass
    elif n == "2":  # Tested OK
        # Student borrowing a Book.
        stud_nm = input("Enter Student Name : ").capitalize()
        admn_no = int(input(f"Enter Admission Number of {stud_nm} : "))
        book_id = int(input("Enter Book ID : "))
        cnecn = connect_database(cs[1])
        dt = datetime.datetime.now()
        try:  # for creating Table in Sql
            q1 = f"""
            create table if not exists borrow_bk(
                Student_Name varchar(50),
                Admission_Number int(50),
                Book_Id int(50),
                Book_Name varchar(50),
                Book_Price float(50),
                Date_Time varchar(150)
            );
            """
            execute_query(cnecn, q1)
        except:
            print("error")
        rq1 = f"""select * from books where Book_ID={book_id};"""
        rd = read_query(cnecn, rq1)
        tq1 = """select qts from books;"""
        rd1 = read_query(cnecn, tq1)
        rq1 = f"""select count(Book_Name) from borrow_bk where Student_Name="{stud_nm}" && Book_Id={book_id} && Admission_Number={admn_no};"""
        rdq1 = read_query(cnecn, rq1)
        if rdq1[0][0] == 0:
            if rd1[0][0] <= 10 and rd1[0][0] >= 1:
                try:
                    q0 = f"""use gnps;"""
                    q2 = f"""insert into borrow_bk values("{stud_nm}",{admn_no},{book_id},"{rd[0][0]}",{rd[0][2]},"{dt}");"""
                    tq1 = f"""update books set qts={rd1[0][0]}-1 where Book_ID={book_id}"""
                    execute_query(cnecn, q0)
                    execute_query(cnecn, q2)
                    execute_query(cnecn, tq1)

                except:
                    print(f"Something Went Wrong.Please Try Again.")
                    for i in range(2, 0, -1):
                        s = input("Read More [y/n] : ")
                        if s[0] == "Y" or s[0] == "y":
                            s = s[0]
                            break
                        elif s[0] == "n" or s[0] == "N":
                            break
                            pass
                        else:
                            print(f"select y/n.remainig times {i}")
                    if s in "yY":
                        with open("__pycache__/solution.txt", "r") as f:
                            data = f.read()
                            print(data)
            elif rd1[0][0] == 0:
                print("Sorry The Book Is Not Available in Library")
        else:
            print("Book Already Borrowed By Student.We Can't Issue Another Same Book..")
    elif n == "3":  # Tested Ok
        issue = input("Book Damaged or Book lost ??[D/L] : ")
        # Book Damaged or book lost by student.
        stud_nm = input("Enter Student Name : ").capitalize()
        admn_no = int(input(f"Enter  Admission Number of {stud_nm}: "))
        book_no = int(input("Enter Book Number : "))
        if issue in "Dd":
            fine = float(input("Enter Fine : "))
        cnecn = connect_database(cs[1])
        rq1 = f"""select * from books where Book_Number={book_no};"""
        rd = read_query(cnecn, rq1)
        if issue in "Ll":
            fine = float(rd[0][2])
        try:  # for creating Table in Sql
            q1 = f"""
            create table if not exists fine_studs(
                Student_Name varchar(50),
                Admission_Number int(50),
                Book_No int(50),
                Book_Name varchar(50),
                Book_Price float(50),
                fine float(50),
                reason varchar(100)
            );
            """
            execute_query(cnecn, q1)
        except:
            print("Something Went Wrong Please Try again")
        if issue in "Dd":
            issue = f"Book Damaged by {stud_nm}"
        elif issue in "Ll":
            issue = f"Book Lost by {stud_nm}"
        try:
            q0 = f"""use gnps;"""
            q2 = f"""insert into fine_studs values("{stud_nm}",{admn_no},{book_no},"{rd[0][0]}",{rd[0][2]},{fine},"{issue}");"""
            execute_query(cnecn, q0)
            execute_query(cnecn, q2)
        except:
            print("Something Went Wrong Please Try again..")
            pass
        n = input("Do you want to see total fine in rupees [y/n] : ")
        if n in "yY":
            rq1 = f"""select fine from fine{stud_nm};"""
            v = read_query(cnecn, rq1)
            sum = 0
            for i in v:
                l = list(i)
                sum += l[0]
            print(f"Fine to be paid by {stud_nm} is INR {sum}")
        else:
            pass
    elif n == "4":  # tested OK
        updt = input(
            "What Do You Want To Update\n[1.Book Name]\n[2.Book ID]\nSelect And Enter: ")
        # Update Book Name or Book Number
        if updt == "1":
            book_id = int(input("Enter Book ID: "))
            n_book_nm = input("Enter Updated Book Name : ")
            q0 = f"""use gnps;"""
            q1 = f"""update books set Book_Name="{n_book_nm}" where Book_Number={book_id};"""
            cnecn = connect_database(cs[1])
            execute_query(cnecn, q0)
            execute_query(cnecn, q1)
        elif updt == "2":
            book_no = int(input("Enter Book Number : "))
            n_book_id = int(input("Enter Updated Book ID : "))
            q0 = f = """use gnps;"""
            q1 = f"""update books set Book_Number="{n_book_id}" where Book_Number={book_id};"""
            cnecn = connect_database(cs[1])
            execute_query(cnecn, q0)
            execute_query(cnecn, q1)
        else:
            print("Select and Enter from [1/2]")
    elif n == "5":
        try:  # tested OK
            stud_nm = input("Enter Student Name : ").capitalize()
            stud_adno = int(input(f"Enter Admission Number of {stud_nm} : "))
            cnecn = connect_database(cs[1])
            rq1 = f"""select * from borrow_bk where Admission_Number={stud_adno} || Student_Name="{stud_nm}";"""
            rq = read_query(cnecn, rq1)
            if rq != []:
                print("Student_name \t\t", "Admission_No \t", "Book_Number \t\t",
                      "Book_Name \t\t\t\t", "Book_Price \t\t", "Date-Time")
                for i in rq:
                    v = i
                    print(v[0], "\t", v[1], "\t", v[2],
                          "\t", v[3], "\t", v[4], "\t", v[5])
            else:
                print("Student Haven't Borrowed Any Book")
        except:
            print("Something went wrong..Please Try Again..")
            pass
    elif n == "6":  # tested OK
        stud_nm = input("Enter Student Name : ")
        book_id = int(input("Enter Book ID : "))
        admn_no = int(input(f"Enter Admission Number of {stud_nm} : "))
        cnecn = connect_database(cs[1])
        tq1 = """select qts from books;"""
        rd1 = read_query(cnecn, tq1)
        if rd1[0][0] <= 10:
            q1 = f"""delete from borrow_bk where Book_Id={book_id} && Student_Name="{stud_nm}" && Admission_Number={admn_no};"""
            execute_query(cnecn, q1)
            tq = f"""update books set qts={rd1[0][0]}+1 where Book_ID={book_id}"""
            execute_query(cnecn, tq)
        else:
            print("All Books Are Returned..")
    s = input("Do You Want to Continue [Y/N] : ").upper()
    if s[0] == "Y":
        s = s[0]
    elif s[0] == "N":
        s = s[0]
    else:
        print("Select And Enter Y or N")
    if s == "N":
        break
