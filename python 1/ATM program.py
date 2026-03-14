 # ATM program 
us={'karthik':"#gkv@upi","kavitha": 123}
user ="karthik"
password="#gkv@upi"

B= '''
1.CREDIT
2.Debit
3.Ministatement
4.Exit
'''

user_name =input("Enter the Uername :")
Passwords =input("Enter the Password :")

Amount =1000

if user_name in us.keys() and Passwords in us.values():
    while True:
       print(B)
       option=int(input("Enete the option :"))
       if option==1 :
            Credit_amount=int(input("please enter the Amount:"))
            print("Total credit amount is :",Amount+Credit_amount)
       elif option==2:
            Debit_amount=int(input("please enter the Amount:"))
            print("Total credit amount is :",Amount+Debit_amount)
       elif option==3 :
           
            print("****Total  amount is**** :",Amount)
       else:
           break
else:
    print("User_name and password is inccoret please try again")