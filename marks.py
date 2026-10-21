m1= int(input("enter marks for subject 1:"))
m2= int(input("enter marks for subject 2:"))
m3= int(input("enter marks for subject 3:"))
m4= int(input("enter marks for subject 4:")) 
m5= int(input("enter marks for subject 5:"))
print("*********************")
total= m1+m2+m3+m4+m5
percentage=total/5
print("total marks=",total)
print("percentage=",percentage)
if percentage>=75:
    print("pass with distinction")
elif percentage>=60:
    print("pass with first class")
elif percentage>=40:
    print("pass")
else:
    print("fail")