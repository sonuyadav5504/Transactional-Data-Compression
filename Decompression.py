import json
import sys

m=sys.argv[1]
m1=sys.argv[2]
########## decompression
compressed_data = []  #reading compressed dataset
mapping={}  #reading the mapping table or dictionary table
with open(m, "r") as file:
    for line in file:
        if '#' not in line:
            items = line.strip().split()  # Split items within the transaction
            compressed_data.append(items)
        else:
            json_data = file.read()
            # Parse the JSON data to get the dictionary
            mapping = json.loads(json_data)

#decompression logic        
asu1=[]
for aa in compressed_data:
    #print(type(aa))
    aa1=set(aa)
    aa2 = {int(item) for item in aa1}
    for i in mapping:
        q=int(i)
        qq={q}
        #print(type(z))
        if qq.issubset(aa2):
            #print(z)
            pq=int(qq.pop())
            aa2.discard(pq)
            x=mapping[i].split(',')
            z=[int(p) for p in x]
            y=set(z)
            for j in y:
                aa2.add(int(j))   
    asu1.append(aa2) 
    
#saving the decompressed dataset into the file 
with open(m1, "w") as file:
    for line1 in asu1:
        int_str1 = ','.join(map(str, line1))
        decompressed_items=int_str1.replace(',',' ')
        file.write(decompressed_items + "\n")
