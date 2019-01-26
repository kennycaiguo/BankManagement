import cx_Oracle
import datetime
#import time;
class customer:
    def withdraw(self,acc_no):# make changes in customer,tranx table give type of tranx as well
        self.amount=int(input("Enter amount to be withdraw"))
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select cust_type,bal from customer where acc_no=:1",(acc_no,))
        self.temp=cur.fetchone()
        self.bal=int(self.temp[1])
        self.cust_type=self.temp[0]
        self.result_bal=self.bal-self.amount
        if self.result_bal>=500:
            if self.amount<=20000:
                cur.execute("update customer set bal=:1 where acc_no=:2",(self.result_bal,acc_no))
                conn.commit()
                now = datetime.datetime.now()
                now=now.strftime("%d-%b-%y")
                self.type='Db'
                cur.execute("insert into tranx values(:1,:2,:3,:4)",(acc_no,now,self.amount,self.type))
                conn.commit()
                print("Withdraw complete successfully")
            else:
                print("you can't withdraw more than 20000")
        else:
            print("Minimum balance in account, transaction cannot be completed")
            
        #conn.close()
    def deposit(self,acc_no): # make changes in customer, tranx table give type of tranx as well
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        self.deposit_amount=int(input("Enter the amount to be deposited"))
        cur.execute("select bal from customer where acc_no=:1",(acc_no,))
        self.temp=cur.fetchone()
        self.bal=int(self.temp[0])
        self.final_bal=self.bal+self.deposit_amount
        self.now = datetime.datetime.now()
        self.now=self.now.strftime("%d-%b-%y")
        cur.execute("update customer set bal=:1 where acc_no=:2",(self.final_bal,acc_no))
        self.type='Cr'
        cur.execute("insert into tranx values(:1,:2,:3,:4)",(acc_no,self.now,self.deposit_amount,self.type))
        conn.commit()
        #conn.close()
    def enquiry(self,acc_no): #balance enquiry from the customer table
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select * from customer where acc_no=:1",(acc_no,))
        self.details=cur.fetchone()
        for self.i in self.details:
            print(self.i,end=" ")
        #conn.close()
    def tranx_details(self,acc_no):
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select * from tranx where acc_no=:1",(acc_no,))
        self.details=cur.fetchall()
        for self.i in self.details:
            for self.j in self.i:
                print(self.j,end=" ")
            print()
        #conn.close()
    def id_gen(self,acc_type):
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select acc_no from customer")
        self.acc_no=cur.fetchall()
        #print(self.acc_no)
        for self.i in self.acc_no:
            for self.j in self.i:
                if self.j[0:1:]=='s' and acc_type=='S':
                    self.acc_no=self.j[1::]
                elif self.j[0:1:]=='c' and acc_type=='C':
                    self.acc_no=self.j[1::]  
        
        return self.acc_no
        #conn.close() 
    
class golden_cust(customer):
    
    def withdraw(self,acc_no):
        self.amount=input("Enter amount to be withdraw")
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select bal from customer where acc_no=:1",(acc_no,))
        self.temp=cur.fetchone()
        self.bal=self.temp[0]
        self.result_bal=self.bal-self.amount
        if self.result_bal>500:
            cur.execute("update table customer set bal=:1 where acc_no=:2",(self.result_bal,acc_no))
            self.now = datetime.datetime.now()
            self.now=self.now.strftime("%d-%b-%y")
            self.type='Db'
            cur.execute("insert into tranx values(:1,:2,:3,:4)",(acc_no,self.now,self.amount,self.type))
            conn.commit()
        #conn.close()


class Admin:
    RC=customer()
    def login(self):
        self.username=input("Enter username")
        self.password=input("Enter password")
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("select password from login where username=:1",(self.username,))
        self.temp=cur.fetchone()
        self.temp=self.temp[0]
        if self.password==self.temp:
            return True
        else:
            return False    
    #def control(self,username):
            
    def update_password(self,username):
        self.new_pass=input("Enter new password")
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("update login set password=:1 where username=:2",(self.new_pass,username))
        conn.commit()
        print("Successfully updated password")
        #conn.close()
    def add_customer(self):
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        self.acc_type=input("Enter account type(Saving/Current)")
        self.acc_no=RC.id_gen(self.acc_type)
        #print(self.acc_no)
        self.acc_no=int(self.acc_no)+1
        if self.acc_type=='S':
            self.acc_no='s'+str(self.acc_no)
            print()
        else:
            self.acc_no='c'+str(self.acc_no)
            
        self.name=input("Enter name")
        self.phone_no=input("Enter phone number")
        self.e_mail=input("Enter e-mail ID")
        self.address=input("Enter the address")
        self.cust_type=input("Enter account type(Regular(R)/Golden(G))")
        self.amount_dep=0
        self.flag=0
        #self.init_bal=0
        self.confirm=input("Submit nominal fee(Y/N)")
        if self.confirm=="Y":
            self.init_bal=int(input("Enter amount"))
            if self.cust_type=='G':
                #print("reached into if")
                while self.init_bal<10500:
                    print("You are a golden customer please please deposit more money")
                    print("Give "+(10500-self.init_bal)+" more")
                    self.init_bal=int(input("Enter amount"))
                self.amount_dep=(self.init_bal)-10000
                self.flag=1
                #cur.execute("insert into customer values(:1,:2,:3,:4,:5,:6,:7,10000)",(self.acc_no,self.name,self.phone_no,self.e_mail,self.address,self.cust_type,self.amount_dep))
            if self.flag==1:
                cur.execute("insert into customer values(:1,:2,:3,:4,:5,:6,:7,10000)",(self.acc_no,self.name,self.phone_no,self.e_mail,self.address,self.cust_type,self.amount_dep))
                conn.commit()
                self.now = datetime.datetime.now()
                self.now=self.now.strftime("%d-%b-%y")
                self.type='Cr'
                cur.execute("insert into tranx values(:1,:2,:3,:4)",(self.acc_no,self.now,self.amount_dep,self.type))
                conn.commit()
                print("Customer added successfully")
                
            elif self.init_bal>=500 and self.cust_type=='R':
                cur.execute("insert into customer values(:1,:2,:3,:4,:5,:6,:7,'')",(self.acc_no,self.name,self.phone_no,self.e_mail,self.address,self.cust_type,self.init_bal))
                conn.commit()
                self.now = datetime.datetime.now()
                self.now=self.now.strftime("%d-%b-%y")
                self.type='Cr'
                cur.execute("insert into tranx values(:1,:2,:3,:4)",(self.acc_no,self.now,self.init_bal,self.type))
                conn.commit()
                print("Customer added successfully")
                
    def remove_customer(self,acc_no):
        conn=cx_Oracle.connect("Bank/12345678")
        cur=conn.cursor()
        cur.execute("delete from customer where acc_no=:1",(acc_no,))
        conn.commit()
        conn.close()
    def forget_pass(self):
        self.username=input("Enter username")
        
        print("password changed succcessfully, restart your system")
        
if __name__ == "__main__":
    admin_obj=Admin()
    #admin_obj.login()
    again='Y'
    if admin_obj.login()==True:
        while again=='Y':
            GC=golden_cust()
            RC=customer()
            print("1.Add customer")
            print("2.Remove customer")
            print("3.Withdraw Money")
            print("4.Deposit Money")
            print("5.Mini Statement")
            print("6.Get details")
            print("7.Update password")
            print("8.exit")
            choice=int(input("Enter your choice"))
            if choice==1:
                admin_obj.add_customer()
            elif choice==2:
                acc_no=input("Enter customer account number")
                admin_obj.remove_customer(acc_no)
            elif choice==3:
                conn=cx_Oracle.connect("Bank/12345678")
                cur=conn.cursor()
                acc_no=input("Enter customer account number")
                cur.execute("select cust_type from customer where acc_no=:1",(acc_no,))
                temp=cur.fetchone()
                cust_type=temp[0]
                if cust_type=='G':
                    GC.withdraw(acc_no)
                else:
                    RC.withdraw(acc_no)
            elif choice==4:
                acc_no=input("Enter customer account number")
                RC.deposit(acc_no)
            elif choice==5:
                acc_no=input("Enter customer account number")
                RC.tranx_details(acc_no)
            elif choice==6:
                acc_no=input("Enter customer account number")
                RC.enquiry(acc_no)
            elif choice==7:
                username=input("Enter the username")
                password=input("Enter the password")
                if admin_obj.login==True:
                    admin_obj.update_password(username)
                else:
                    print("Wrong username or password")
                    print("security breach detected")
                    print("exiting system")
                    exit()
                #admin_obj.update_password(username)
            elif choice==8:
                exit()
            again=input("Do you want to continue (Y/N)")
    else:
        print("Wrong username or password")
        print("1.Forget password")
        choice=input("Enter your choice")
        if choice==1:
            admin_obj.forget_pass()
        #call the forget password module