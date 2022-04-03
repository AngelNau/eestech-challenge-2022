import math
import json

def createData(file_num):
    datoteka = open(f"unsupervised_dataset/scenario_week_example_{file_num}.csv")
    data = []
    for line in datoteka:
        curr = line.split(",")
        data.append(curr[3]) #3 je indeks za Turbine current

    data = data[1:]

    for i in range(len(data)):
        if data[i] == '':
            data[i] = data[i-1]
        data[i] = float(data[i])

    return data


#  FUNCTIONS FOR MAIN ALGORITHM

def back_climb(index):
    global end_periods
    global leakeges
    for i in range(index,0,-1):
        if heightDiffs[i] >= maxAvg - margin:
            max = 0
            new_index = 0
            for j in range((i-1)*diff,i*diff):
                if data[j] > max:
                    max = data[j] 
                    new_index = j

            end_periods.append(new_index * 10)
            leakeges.append(int(leakege))
            break

    return None


def front_climb(index):
    global end_periods
    global leakeges
    for i in range(index,len(data)):
        if heightDiffs[i] >= maxAvg - margin:
            max = 0
            new_index = 0
            for j in range((i-1)*diff,i*diff):
                if data[j] > max:
                    max = data[j]
                    new_index = j

            end_periods.append(new_index * 10)
            leakeges.append(int(leakege))
            break

    return None


def find_decline(index) -> bool:
    # global heightDiffs
    # global margin
    global game_over
    global leakege
    for i in range(index,len(heightDiffs)):
        if i + 1 >= len(heightDiffs):
            game_over = True
            leakege = True
            return i
        if abs(heightDiffs[i] - (minAvg + margin) ) < abs(heightDiffs[i] - (maxAvg - margin)) and \
           abs(heightDiffs[i+1] - (minAvg + margin)) < abs(heightDiffs[i+1] - (maxAvg - margin)):
            back_climb(i)
            break

    leakege = True
    return i

def find_incline(index):
    global game_over
    global leakege
    for i in range(index,len(heightDiffs)):
        if i + 1 >= len(heightDiffs):
            game_over = True
            leakege = False
            return i
        if abs(heightDiffs[i] - (minAvg + margin) ) > abs(heightDiffs[i] - (maxAvg - margin)) and \
           abs(heightDiffs[i+1] - (minAvg + margin)) > abs(heightDiffs[i+1] - (maxAvg - margin)):
            front_climb(i)
            break
    
    leakege = False
    return i

#  MAIN ALGORITHM 

all_end_perionds = []
all_leakages = []
jsonObject = []
temp = open("json_data.json","w")
temp.write('{\n\t"prediction_results": [\n\t{\n')

for k in range(100):

    data = createData(k)
    diff = 248
    margin = 0.06
    game_over = False
    end_periods = []
    leakeges = []


    avgValues2 = [] #avg values between 2 values next to each other
    heightDiffs = [] # height diffs between compared values


    for i in range(0,math.floor(len(data) - diff), diff):
        avgValues2.append(data[i] - data[i+diff])
        heightDiffs.append((data[i] + data[i + diff]) / 2)



    maxAvg = max(heightDiffs) # maximal average height value 
    minAvg = min(heightDiffs) # minimal average height value 



    # START POSITION CHECKING

    if abs(sum(data[:20]) / 20 - maxAvg) < abs(sum(data[:20]) / 20 - minAvg):
        leakege = False
    else:
        leakege = True

    if maxAvg - minAvg < margin:
        end_periods = [604800]
        leakeges = [0]
    else:
        znj = 0
        while znj < len(heightDiffs):
        # for znj in range(len(heightDiffs)):
            if game_over:
                break
            if not leakege:
                znj = find_decline(znj) + 1
            else:
                znj = find_incline(znj) + 1

    all_end_perionds.append(end_periods)
    all_leakages.append(leakeges)
    end_periods = []
    leakeges = []
    all_end_perionds[k].sort()
    if k != 0:
        temp.write("\t{\n")
    temp.write(f'\t\t\t"file_name" : "scenario_week_example_{k}.csv",\n')
    temp.write(f'\t\t\t"end_periods": {all_end_perionds[k]},\n')
    temp.write(f'\t\t\t"leakages": {all_leakages[k]}\n')
    if k == 99:
        temp.write("\t\t}\n")
    else:
        temp.write("\t\t},\n")
    
temp.write("\t]\n")
temp.write("}\n")
# temp.write("}")
# jsonObject[0]["file_name"].append(1)
print(jsonObject)
# with open('json_data.json', 'w') as outfile:
#     outfile.write(json.dumps(jsonObject).replace('\\', ''))