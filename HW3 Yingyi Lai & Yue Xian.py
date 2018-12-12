from pygeodesy import ellipsoidalVincenty as ev
from datetime import datetime


def Imprt(path):
    Property_list = []
    detail=[]
    StormID = 'c'
    dict_p = {}
    dict_d = {}
    dict_r = {}
    radii = []
    with open(path, 'r') as f:
        for line in f:
            values_on_line = line.split(',')

            # when recognize the header
            if values_on_line[0][0].isalpha() == True:
                dict_p[StormID] = Property_list
                dict_d[StormID] = detail
                Property_list = []
                detail= []
                StormID = values_on_line[0]
                name = values_on_line[1].strip()
                recdlen = int(values_on_line[2])
                if name == 'UNNAMED':
                    name = ' '
                Property_list.append(name)

                # in  the cycle of records chunk
                for i in range(recdlen):
                    line = next(f)
                    values_on_line = line.split(',')
                    Date = values_on_line[0]
                    time = Date+values_on_line[1]

                    # output time and coordinate to a list
                    detail.append((time, values_on_line[4].strip(), values_on_line[5].strip()))

                    # initialize the value when read the first line of the record
                    if i == 0:
                        StDate = Date
                        maxdate = Date
                        Property_list.append(StDate)
                        t = []
                        knotmax = 0
                        radii=[]
                        # store the coordiante and time

                    # output the radii to a list
                    radius = [int(value.strip()) for value in values_on_line[8:19]]
                    if -999 not in radius and any(radius) != 0:
                        radii.append((values_on_line[4].strip(), values_on_line[5].strip(), radius))
                        dict_r[StormID] = radii

                    t.append(values_on_line[2].strip())
                    knot = int(values_on_line[6])
                    if knot > knotmax:
                        knotmax = knot
                        maxdate = Date

                    # when read the last line
                    if i == (recdlen - 1):
                        Enday = Date
                        Property_list.append(Enday)
                Property_list.append(knotmax)
                Property_list.append(maxdate)
                Property_list.append(t.count('L'))

    dict_p[StormID] = Property_list
    dict_d[StormID] = detail
    del dict_p['c']
    del dict_d['c']
    return dict_p, dict_d, dict_r


def hour_elapse(time1:str, time2: str):
    """
    It is a function to calculate the elapsed time between time1 and time2
    :param time1: first observed time
    :param time2: second observed time
    :return: elapsed time in hour
    """
    FMT='%Y%m%d %H%M'
    diff=datetime.strptime(time2, FMT) - datetime.strptime(time1, FMT)
    elapsed_hour = diff.seconds/3600
    return elapsed_hour


def dist(lat1:str, lon1:str, lat2:str, lon2:str):
    """
    It is a function to calculate the distance between two coordinate
    :param lat1: latitude of the first location
    :param lon1: longitude of the first location
    :param lat2: latitude of the second location
    :param lon2: longitude of the second location
    :return: distance in nautical miles
    """
    a = ev.LatLon(lat1, lon1)
    b = ev.LatLon(lat2, lon2)
    if a == b:
        return 0
    else:
        return a.distanceTo(b)/1852.0


def bear(lat1:str, lon1:str, lat2:str, lon2:str):
    a = ev.LatLon(lat1, lon1)
    b = ev.LatLon(lat2, lon2)
    if a == b:
        return 0
    else:
        return a.bearingTo(b)


def judge(degree) -> int:
    """
    judge the bearing belong to which quadrant
    :param degree: specific degree
    :return: corresponding quadrant
    """
    if degree > 360:
        degree=degree-360

    if 0 < degree < 90:
        quad = [1]
    if 90 < degree < 180:
        quad = [2]
    if 180 < degree < 270:
        quad = [3]
    if 270 < degree < 360:
        quad = [4]
    if degree==0 or degree == 360:
        quad =[1,4]
    if degree == 90:
        quad = [1,2]
    if degree == 180:
        quad = [2,3]
    if degree == 270:
        quad = [3,4]
    return quad


def dispeed(somedict:dict) -> dict:
    """
    This is a function reading the relevant location and observed time and ouput the sum of distance, maximum and
    average speed
    :param somedict: a dictionary with corresponding observed location and time
    :return: a dictionary whose key is the storm ID and its value is its corresponding sum of distance, maximum speed
    and average speed
    """
    speedict={}
    for id in somedict.keys():
        list=somedict[id]
        # speed=[] did not work
        if len(list)==1:
            speedict[id] = ('N/A','N/A', 'N/A')
        else:
            for i in range(len(list)-1):
                if i ==0 :
                    speed=[]
                    alldist=[]
                distance = dist(list[i][1],list[i][2], list[i+1][1], list[i+1][2])
                elap_time= hour_elapse(list[i][0],list[i+1][0])
                alldist.append(distance)
                speed.append(round(distance/elap_time,2))
            # ouput sum of distance, maximum speed and average speed per storm
            speedict[id]=(round(sum(alldist),2), max(speed), round(sum(speed)/len(speed),2))
    return speedict

def maxiquad (somelist:list):
    """
    This is function could figure out the quadrant of the strongest and longest non-zero radius of each sample data
    :param somelist: the list of the radii for each storm
    :return: give back the quadrant of strongest and longest non-zero radius
    """
    if any(somelist[-1:-5])!=0:
        maxr=max(somelist[-1:-5])
        ind = [i + 1 for i, j in enumerate(somelist[-1:-5]) if j == maxr]
    elif any(somelist[-5:-9])!=0:
        maxr=max(somelist[-5:-9])
        ind = [i + 1 for i, j in enumerate(somelist[-5:-9]) if j == maxr]
    else:
        maxr = max(somelist)
        ind = [i + 1 for i, j in enumerate(somelist) if j == maxr]
    return ind



def test(angle:int, radict: dict):
    """
    This is a function that input an angle and a dictionary whose key is storm id and values are the non zero radii
    :param angle: a specific angle that we'd like to test the hypothesis
    :param radict: a dictionary whose key is storm id and values are the non zero radii
    :return:  percentage of the evidents supporting the hpothesis
    """
    total = 0
    countrue = 0
    for id in radict.keys():
        radii4storm=radict[id]
        for j in range(len(radii4storm)-1):
            bearing = bear(radii4storm[j][0], radii4storm[j][1], radii4storm[j+1][0], radii4storm[j+1][1])
            quad_hypo = judge(bearing + angle)
            #print(bearing + angle)
            #print(quad_hypo)
            quad_fact = maxiquad(radii4storm[j+1][2])
            #print(quad_fact)
            if any(x in quad_fact for x in quad_hypo):
                countrue = countrue +1
            total=total+1
    return countrue/total

properti1, detail1, dict_r1 = Imprt('hurdat2-1851-2017-050118.txt')
properti2, detail2, dict_r2 = Imprt('hurdat2-nepac-1949-2017-050418.txt')



# question a and b
speedict1 = dispeed(detail1)
speedict2 = dispeed(detail2)


f = open('ouput.txt','w')

print("Detail for each storm on Atlantic Hurricanes:\n", file=f)
print("ID\tTotalDistance \t Max \t Mean", file=f)
for id in speedict1.keys():
     print("{}\t{}\t{}\t{}".format(id,speedict1[id][0],speedict1[id][1],speedict1[id][2]), file=f)
print("\nPercentage of evidence that support the hypothesis:\n", file=f)
print("Degree\tPercentage", file=f)
for i in range(70,111):
    print("{}\t{:.2%}".format(i,test(i, dict_r1)),file=f)

print("Detail for each storm on Pacific Hurricanes:\n", file=f)
print("ID\tTotalDistance \t Max \t Mean", file=f)
for id in speedict2.keys():
     print("{}\t{}\t{}\t{}".format(id,speedict2[id][0],speedict2[id][1],speedict2[id][2]), file=f)
print("\nPercentage of evidence that support the hypothesis:\n", file=f)
print("Degree\tPercentage", file=f)
for i in range(70,111):
    print("{}\t{:.2%}".format(i,test(i, dict_r2)),file=f)


f.close()
