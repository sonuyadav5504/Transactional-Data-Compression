import json
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import sys

n=sys.argv[1]
n1=sys.argv[2]
#finding the support
count1 = open(n, "r")
data = count1.read()
nnn = len(data)

count2 = open(n, "r")
nn = sum(1 for line in count2)
                        
sup_th=nnn/nn


if sup_th>=190:
    sup=0.2   
elif 170<=sup_th<190:
    sup=0.09
elif 150<=sup_th<170:
    sup=0.009
elif 140<=sup_th<150:
    sup=0.01
elif 130<=sup_th<140:
    sup=0.05
elif 120<=sup_th<130:
    sup=0.1    
elif 90<=sup_th<120:
    sup=0.8
elif 75<=sup_th<90:
    sup=0.4
elif 60<=sup_th<75:
    sup=0.2
elif 50<=sup_th<60:
    sup=0.1    
elif 20<=sup_th<50:
    sup=0.01
else:
    sup=0.009    


if sup_th>0.5:
    size=9
elif 0.1<sup_th<=0.5:
    size=5
else:
    size=4    
    
# Read the transaction data from the .dat file
transaction_data = []
with open(n, "r") as file:
    for line in file:
        items = line.strip().split()  # Split items within the transaction
        transaction_data.append(items)

# Convert the list of items into a binary matrix using TransactionEncoder
encoder = TransactionEncoder()
one_hot_encoded = encoder.fit_transform(transaction_data)
df = pd.DataFrame(one_hot_encoded, columns=encoder.columns_)

# Apply the FP-Growth algorithm
frequent_itemsets = fpgrowth(df, min_support=sup, use_colnames=True)
filtered_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x)) >=size]

#for compression dictionary creating
count=-1
dictionary={}
for i in filtered_itemsets['itemsets']:
    temp={count:i}
    dictionary.update(temp)
    count-=1
      
    
# Convert dictionary list values to strings
for key, value in dictionary.items():
    dictionary[key] = ','.join(map(str, value))

# convert int key into string key
monu = {str(key): value for key, value in dictionary.items()}
# sort the dictionary value a/c to length of value
monus = dict(sorted(monu.items(), key=lambda item: len(item[1]), reverse=True))

##########compression logic
asu=[]
for a in transaction_data:
    a1=set(a)
    a2 = {int(item) for item in a1}
    #print(a2)
    for i in monus:
        x=monus[i].split(',')
        z=[int(p) for p in x]
        y=set(z)
        if y.issubset(a2):
            for j in y:
                a2.discard(j)
            a2.add(int(i))    
            
    asu.append(a2) 

#saving the dictinary & compressed data in the compressed data file
with open(n1, "w") as file:

    for line in asu:
        int_str = ','.join(map(str, line))
        compressed_items=int_str.replace(',',' ')
        file.write(compressed_items + "\n")

    content = "#"
    file.write(content)
    file.write("\n")
  # Serialize dictionary to JSON
    json_data = json.dumps(monus)
  # Write JSON data to a .dat file
    file.write(json_data)