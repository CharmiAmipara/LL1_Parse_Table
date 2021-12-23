def findfirst(variable):
    
    if variable in dfirst:
        return first[variable]
    
    rhs=[]
    eps=0  # There is no Epsilon
    
    for i in productions:
        if i[0]==variable:
            rhs.append(i[3:])
    
    first[variable]=[]
    for i in rhs:
        first_letter = True   
        
        for letter in i:
            if letter==variable and first_letter:
                first_letter = False
            
            elif (letter!=variable) and (letter in variables) and (first_letter or eps==1):
                
                temp=findfirst(letter)
                if "@" not in temp:
                    eps=0
                
                for each in temp:
                    if each=='@':
                        eps=1
                    else:
                        first[variable].append(each)
                first_letter=False
            
            elif (letter in terminals) and (first_letter or eps==1):
                first[variable].append(letter)
                eps=0
                first_letter=False
            
            elif letter=='/':
                first_letter=True
                if eps==1:
                    first[variable].append('@')
                    eps=0
        if eps==1:
            first[variable].append('@')
    
    dfirst.append(variable)
    return first[variable]


 
def findfollow(variable):
    
    if variable in dfollow:
        return follow[variable]
    
    follow[variable]=[]
    
    if variable==productions[0][0]:
        follow[variable].append('$')
        
    for i in productions:
        rhs = i[3:]
        eps=0
        
        if variable in rhs:
            for letter in rhs:
                if letter==variable and eps==0:
                    eps=1
                
                elif (letter in variables) and eps==1:
                    
                    temp=findfirst(letter)
                    for each in temp:
                        if each!='@':
                            follow[variable].append(each)
                    if '@' not in temp:
                        eps=0
                
                elif (letter in terminals) and eps==1:
                    follow[variable].append(letter)
                    eps=0
                
                elif letter=='/' and eps==1:
                    if variable != i[0]:
                        temp = findfollow(i[0])
                        for each in temp:
                            follow[variable].append(each)
                    eps=0
        if eps==1:
            if variable != i[0]:
                temp = findfollow(i[0])
                for each in temp:
                    follow[variable].append(each)
    
    dfollow.append(variable)
    return follow[variable]



ptable = {}
def parse(variable):
    
    prod=[]
    table={}
    print()
    print(variable+"\t", end="")
    for i in productions:
        if i[0]==variable:
            temp=i[3:]
            ll=temp.split('/')
            for each in ll:
                prod.append(each)
    
    for i in prod:
        first=True
        for letter in i:
            if (letter in variables) and first:
                temp=findfirst(letter)
                if '@' not in temp:
                    first=False
                else:
                    temp=list(set(temp))
                    temp.remove('@')
                for each in set(temp):
                    if each not in table.keys():
                        table[each]=[i]
                    else:
                        table[each].append(i)
            elif letter=='@':
                first = False
                temp=findfollow(variable)
                for each in set(temp):
                    if each not in table.keys():
                        table[each]=[i]
                    else:
                        table[each].append(i)
            elif (letter in terminals) and first:
                if letter not in table.keys():
                    table[letter]=[i]
                else:
                    table[letter].append(i)
                first=False
            
        if first:
            if '$' not in table.keys():
                table['$']=[i]
            else:
                table['$'].append(i)
    
    
    # general parse table to validate string
    llist = list(table.keys())
    for each in llist:
        tp = []
        if each not in ptable.keys():
            for i in table[each]:
                tp.append(variable + "->" + i)
            ptable[each] = tp
        else:
            for i in table[each]:
                ptable[each].append(variable + "->" + i)
        
    
    # To print the parsing table
    for terminal in terminals:
        if terminal=='@':
            terminal='$'
        if terminal in table.keys():
            temp=set(table[terminal])
            if len(temp)==1:
                for each in temp:
                    print((variable+"->"+each).ljust(20), end="")
            else:
                print((variable+"->"+str(temp)).ljust(20), end="")
        else:
            print("".ljust(20), end="")



def validate(input_string):
     
    flag = 0   # string is valid
    input_string += "$"
    
    stack = []
    start_symbol = productions[0][0]
    
    stack.append("$")
    stack.append(start_symbol)
    
    pointer = 0
    
    while len(stack)>0:
        top = stack[len(stack)-1]
        cur_input = input_string[pointer]
        
        if top == cur_input:
            stack.pop()
            pointer += 1
            
        else:
            ll = []
            for prod in ptable[cur_input]:
                ll.append(prod[0])
            
            if top not in ll:
                flag = 1
                break
            
            for prod in ptable[cur_input]:
                if prod[0] == top:
                    rhs = prod[3:]
                    if rhs == "@":
                        stack.pop()
                    else:   
                        stack.pop()
                        for j in range(len(rhs)-1 , -1, -1):
                            stack.append(rhs[j])
                      
    
    if flag == 1:
        print("String is Not Accepted")
    else:
        print("String is Accepted")
                        



#main class
file = open("grammar.txt","r")

productions=[]
while True:
    ll = file.readline().strip()
    if ll=="":
        break
    productions.append(ll)
print("\n",productions)

variables =[]
for i in productions:
    variables.append(i[0])

terminals = []
for i in productions:
    i = i[3:]
    for j in i:
        if j not in variables and j!="/":
            terminals.append(j)
terminals = list(set(terminals))

    
first={}
follow={}
dfirst=[]
dfollow=[]

print()
print("First and Follow \n")
print("Terminal".ljust(13), "First".ljust(25), "Follow".ljust(25))

for v in variables:
    print(v.ljust(13), str(set(findfirst(v))).ljust(25), str(set(findfollow(v))).ljust(25))

print()
print("Parsing Table :")
print("\t", end="")

for terminal in terminals:
    if terminal=='@':
        terminal='$'
    print(terminal.ljust(20), end="")

if "@" not in terminals:
    terminal = '$'
    print(terminal.ljust(20), end="")

for v in variables:
    parse(v)
    
print("\n")    

string = input("Enter String : ")
validate(string)