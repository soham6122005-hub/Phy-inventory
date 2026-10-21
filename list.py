Students =["soham","dipak","rohit","shivam","ram"]
print(Students)
print(Students[0])
print(Students[1])
print(Students[2])
print(Students[3])
print(Students[4])

for student in Students:
    print(f"hello {student}! welcome to the class")
    
marks_list=[85,90,78,92,88]

for mark in marks_list:
    if mark>=90:
        print(f"mark: {mark} - grade: A")
    elif mark>=80:
        print(f"mark: {mark} - grade: B")
    elif mark>=70:
        print(f"mark: {mark} - grade: C")