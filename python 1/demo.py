print("this is my code ")

grocery_Items = [
    {"S.No": 1, "Item Name": "Rice", "Price (₹)": 300},
    {"S.No": 2, "Item Name": "Wheat Flour (Atta)", "Price (₹)": 250},
    {"S.No": 3, "Item Name": "Toor Dal", "Price (₹)": 280},
    {"S.No": 4, "Item Name": "Sugar", "Price (₹)": 90},
    {"S.No": 5, "Item Name": "Salt", "Price (₹)": 20},
    {"S.No": 6, "Item Name": "Cooking Oil", "Price (₹)": 150},
    {"S.No": 7, "Item Name": "Milk", "Price (₹)": 120},
    {"S.No": 8, "Item Name": "Tea Powder", "Price (₹)": 200},
    {"S.No": 9, "Item Name": "Turmeric Powder", "Price (₹)": 30},
    {"S.No": 10, "Item Name": "Red Chili Powder", "Price (₹)": 60},
    {"S.No": 11, "Item Name": "Onion", "Price (₹)": 50},
    {"S.No": 12, "Item Name": "Potato", "Price (₹)": 40},
    {"S.No": 13, "Item Name": "Tomato", "Price (₹)": 45},
    {"S.No": 14, "Item Name": "Green Chilies", "Price (₹)": 15},
    {"S.No": 15, "Item Name": "Soap (Bath)", "Price (₹)": 80},
    {"S.No": 16, "Item Name": "Detergent Powder", "Price (₹)": 60}
]

# for i in grocery_Items:
#             for k,v in i.items():
#                if v==item:
#                 price=quantity*(v[item])

for i in grocery_Items:
    #print(i)
    for k ,v in i.items():
        print(v)