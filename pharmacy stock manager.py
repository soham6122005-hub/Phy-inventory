medicines = ["paracetamol", "metformin", "amlodipine" , "salbutamol"]
expiry_date =[ "1-1-2026", "2-3-2026", "4-5-2026", "3-5-2026"]
quantity = [10, 9, 45, 30]
 

for i in range(len(medicines)):
    print(f"medicine: {medicines[i]} - expiry date: {expiry_date[i]} - quantity: {quantity[i]}")    
 
if quantity[0] < 20:
    print(f"medicine: {medicines[0]} is running low. Please restock.")
    
if quantity[1] < 20:
    print(f"medicine: {medicines[1]} is running low. Please restock.")  
    
if quantity[2] < 20:
    print(f"medicine: {medicines[2]} is running low. Please restock.") 
     
if quantity[3] < 20:
    print(f"medicine: {medicines[3]} is running low. Please restock.")    