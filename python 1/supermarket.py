# super market Bill geneation 

from datetime import datetime

name = input("eneter you name :")

lists = '''

    "Rice"                        ₹300 / 5 kg
    "Wheat Flour (Atta)"          ₹250 / 5 kg
    "Toor Dal":              ₹280 / 2 kg
    "Sugar":                   ₹90 / 2 kg
    "Salt":                  ₹20 / 1 kg
    "Cooking Oil"           ₹150 / 1 L
    "Milk":                   ₹120 / 2 L
    "Tea Powder":            ₹200 / 0.5 kg → ₹400/kg
    "Turmeric Powder":       ₹30 / 0.1 kg → ₹300/kg
    "Red Chili Powder":      ₹60 / 0.2 kg → ₹300/kg
    "Onion":                   ₹50 / 2 kg
    "Potato":                  ₹40 / 2 kg
    "Tomato":                  ₹45 / 1.5 kg
    "Green Chilies":           ₹15 / 0.25 kg
    "Soap (Bath)":            ₹80 / 4 pcs
    "Detergent Powder":         ₹60 / 1 kg

'''


 # declaration 

grocery_Items = {
    "Rice": 60,                  # ₹300 / 5 kg
    "Wheat Flour (Atta)": 50,    # ₹250 / 5 kg
    "Toor Dal": 140,             # ₹280 / 2 kg
    "Sugar": 45,                 # ₹90 / 2 kg
    "Salt": 20,                  # ₹20 / 1 kg
    "Cooking Oil": 150,          # ₹150 / 1 L
    "Milk": 60,                  # ₹120 / 2 L
    "Tea Powder": 400,           # ₹200 / 0.5 kg → ₹400/kg
    "Turmeric Powder": 300,      # ₹30 / 0.1 kg → ₹300/kg
    "Red Chili Powder": 300,     # ₹60 / 0.2 kg → ₹300/kg
    "Onion": 25,                 # ₹50 / 2 kg
    "Potato": 20,                # ₹40 / 2 kg
    "Tomato": 30,                # ₹45 / 1.5 kg
    "Green Chilies": 60,         # ₹15 / 0.25 kg
    "Soap (Bath)": 20,           # ₹80 / 4 pcs
    "Detergent Powder": 60       # ₹60 / 1 kg
}

price=0
price_list=[]
Total_price =0
final_price=0
plist=[]
ilist=[]
qlist=[]
option =int(input("Enter of items enter 1 "))
if option == 1:
  print(lists)
  for i in range(len(grocery_Items)):
     inp1=int(input("If you wnat to buy press 1 or 2 for exit  "))
     if inp1==2:
        break
     elif inp1==1:
        item=input("enetr your item in list: ")
        quantity = int(input("enetr the Quantity "))
        if item in grocery_Items.keys():
            price=quantity*(grocery_Items[item])
            price_list.append(item,quantity,price)
            Total_price+=price
            ilist.append(item)
            qlist.append(quantity)
            plist.append(price)
            gst=(Total_price*5)/100
            final_price=Total_price+gst
        else:
            print("currently item is not avialable :")
     else:
        print("you enter wrong number ")
  inp=intput("can i generted the bill or not")
  if inp=="yes" :
     pass
     if final_price !=0:
        for i in range(price_list):
           print(i,ilist[i],plist[i],qlist[i])
      
        


 

