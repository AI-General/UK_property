import ast
file_path = 'total_lists.txt'  

# Open and read the file  
with open(file_path, 'r') as file:  
    content = file.read()  

# Safely evaluate the content to convert it into a Python list  
all_lists = ast.literal_eval(content)
print("number of unique properties: ",len(all_lists))
# Split the list into two parts  
list1 = all_lists[:100000] 
with open("list1.txt", "w") as f:
    f.write(str(list1))
list2 = all_lists[100000:200000]  
with open("list2.txt", "w") as f:
    f.write(str(list2))
list3 = all_lists[200000:300000]  
with open("list3.txt", "w") as f:
    f.write(str(list3))
list4 = all_lists[300000:400000] 
with open("list4.txt", "w") as f:
    f.write(str(list4))
list5 = all_lists[400000:] 
with open("list5.txt", "w") as f:
    f.write(str(list5))

print(len(list1))
print(len(list2))
print(len(list3))    
print(len(list4))
print(len(list5))