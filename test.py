import re
dob = input("Enter your Date of birth(dd/mm/yyyy): ")
while( re.match(r"^(([0]{1}[1-9]{1}[\/]{1})|([1-2]{1}\d{1}[\/]{1})|([3]{1}[0-1]{1}[\/]{1}))(([0]{1}[1-9]{1}[\/]{1})|([1]{1}[0-2]{1}[\/]{1}))([1-9]{1}\d{3})$",dob)==None):
    print("invalid")
    dob = input("Enter your Date of birth(dd/mm/yyyy): ")
    
print("done")

