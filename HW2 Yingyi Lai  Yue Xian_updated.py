## Team member: Yingyi Lai & Yue Xian

## We worked together all the question and code.

# global parameters
Dict={}
list = []
StormID='c'

# read the first dataset

with open('1.txt','r') as f:
    for line in f:
        values_on_line =line.split(',')
        if values_on_line[0][0].isalpha()==True:
            Dict[StormID]=list
            list = []
            knotmax = 0
            StormID=values_on_line[0]
            name=values_on_line[1].strip()
            recdlen=int(values_on_line[2])
            if name =='UNNAMED':
                 name=' '
            list.append(name)
            for i in range(recdlen):
                line = next(f)
                maxdate = ' '
                values_on_line = line.split(',')
                Date=values_on_line[0]
                if i==0:
                    StDate = Date
                    list.append(StDate)
                    t=[]
                t.append(values_on_line[2].strip())
                knot = int(values_on_line[6])
                if knot > knotmax:
                    knotmax=knot
                    maxdate=Date
                if i ==(recdlen - 1):
                    Enday=Date
                    list.append(Enday)
            list.append(knotmax)
            list.append(maxdate)
            list.append(t.count('L'))

# read the second dataset

with open("2.txt",'r') as f:
    for line in f:
        values_on_line =line.split(',')
        if values_on_line[0][0].isalpha()==True:
            Dict[StormID]=list
            list = []
            knotmax = 0
            StormID=values_on_line[0]
            name=values_on_line[1].strip()
            recdlen=int(values_on_line[2])
            if name =='UNNAMED':
                 name=' '
            list.append(name)
            for i in range(recdlen):
                line = next(f)
                maxdate = ' '
                values_on_line = line.split(',')
                Date = values_on_line[0]
                if i==0:
                    StDate = Date
                    list.append(StDate)
                    t=[]
                t.append(values_on_line[2].strip())
                knot=int(values_on_line[6])
                if knot > knotmax:
                    knotmax = knot
                    maxdate = Date
                if i == recdlen-1:
                    Enday = Date
                    list.append(Enday)
            list.append(knotmax)
            list.append(maxdate)
            list.append(t.count('L'))




del Dict['c']
Dict[StormID] = list

# print(Dict)

Year={}
Agg=[]

for ID in Dict.keys():
    allvar = Dict[ID]
    print(allvar)
    year=int(allvar[1][:4])
    Year[ID] = year
    if int(allvar[3]) >= 64:
        ans='Hurricane!'
    else:
        ans='Not Hurricane'
    Agg.append([ID,year, ans])
print(Agg)
# # define Count function : it first flipped the dictionary and then count the number of values, and print out

def Count (Dict):
    flipped = {}
    new=[]
    for k in Dict.keys():
        v = Dict[k]
        if v not in flipped:
            flipped[v] = [k]
        else:
            flipped[v].append(k)
    # print(flipped)
    for x in flipped.keys():
         new.append([x, len(flipped[x])])
    return new

Year1=Count(Year)

# Count the number of Hurricane per year

Hurr={}
for info in Agg:
    if info[2]=='Hurricane!':
        Hurr[info[0]]=info[1]
# print(Hurr)
Year2=Count(Hurr)  # print the number of Hurricane each year


# ouput
file = open('Result.txt', 'w')

#
file.write("Output Data: \n")
for ID in Dict.keys():
    file.write('StormID : {:10}'.format(str(ID)) + '\tStorm Name : {:15}'.format(str(Dict[ID][0]))+ '\tDate range is : {} - {} \t'.format(str(Dict[ID][1]), str(Dict[ID][2])) +
            'Highest Maximum Knots are : {:4}'.format(str(Dict[ID][3])) + '\tDate :{:10}'.format(str(Dict[ID][4])) +'\tTime of Landfall are :{:3}'.format(str(Dict[ID][5])) + '\n')

file.write("\nTotal number of Storm each year :\n")
for i in range(len(Year1)):
     file.write('Year : {:6}\t Total number of Storm : {}\n'.format(str(Year1[i][0]),str(Year1[i][1])))

file.write("\nTotal Number of Hurricane each year:\n")
for i in range(len(Year2)):
     file.write('Year : {:6}\t Total number of hurricane : {}\n'.format(str(Year2[i][0]),str(Year2[i][1])))


file.close
