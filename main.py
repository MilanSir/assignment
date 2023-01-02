import argparse

def csvtodic(filename):
    with open(filename) as f:
        csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]
        (_, *header), *data = csv_list
        csv_dict = {}
        for row in data:
            key, *values = row   
            csv_dict[key] = {key: value for key, value in zip(header, values)}
    return csv_dict

def toppereachsubject(dic):
    for k in ["Maths","Biology","English","Physics","Chemistry","Hindi"]:
        Marks = []
        for i,j in dic.items():
            Marks.append(int(j[k]))
        indices = []
        for idx,value in enumerate(Marks):
            if value == max(Marks):
                indices.append(idx)
        for l in indices:
            print(f"Topper in {k} is {list(dic)[l]}")

def allovertopper(csv_dict):
    Marks = []
    for i,j in csv_dict.items():
        Marks.append(sum(int(x) for x in j.values()))
    kr = Marks
    print(f"Best students in the class are ({list(csv_dict)[Marks.index(sorted(kr,reverse=1)[0])]} first rank, {list(csv_dict)[Marks.index(sorted(kr,reverse=1)[1])]} second rank,{list(csv_dict)[Marks.index(sorted(kr,reverse=1)[2])]} third rank)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-file',type=str, default='Student_marks_list (1).csv')
    opt = parser.parse_args()
    csvdict = csvtodic(opt.file)
    toppereachsubject(csvdict)
    allovertopper(csvdict)
