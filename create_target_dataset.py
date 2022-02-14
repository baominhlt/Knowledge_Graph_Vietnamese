from underthesea import pos_tag as pos
import pandas as pd
import timeit

# Functions list
#-------------------------------------------------------------------------------------------------------------------
# Read content of a text file
def read_content(filepath):
    f = open(filepath, encoding='utf-8')
    content = f.readlines()
    f.close()
    return content

# Search the entities in a relation
def search_entities(pos_t, i):
    ent1 = ""
    ent2 = ""
    if (i + 3 > len(pos_t)):
        m = len(pos_t)
    else:
        m = i + 3
    for j in range(i + 1, m):
        if (pos_t[j][1] == "N" or pos_t[j][1] == "Np"):
            ent2 += pos_t[j][0] + " "
        else:
            break
    if (i == 0):
        ent1 = ""
    else:
        if (pos_t[i - 1][1] == "P" or pos_t[i - 1][1] == "N" or pos_t[i - 1][1] == "Np"):
            ent1 = pos_t[i - 1][0]
    if (ent1 and ent2):
        return [ent1, pos_t[i][0], ent2.strip()]
    else:
        return None

# Extract the relation in a text from file's text
def extract_relation(content, relation_v, relation_c, debug = True):
    kg = []
    count = -1

    if (debug):
        n_loop = 500
    else:
        n_loop = len(content)
    for text in content[:n_loop]:
        count += 1
        pos_t = list(pos(text))
        check = False
        for i in range(len(pos_t)):
            if (pos_t[i][1] == "V" and pos_t[i][0] in relation_v):
                check = search_entities(pos_t, i)
            if (pos_t[i][1] == "C" and pos_t[i][0] in relation_c):
                check = search_entities(pos_t, i)
        if (check):
            kg.append([count, check])

    return kg

# Create content of target dataset
def create_content(kg, content):
    target_content = []
    id = -1

    for item in kg:
        id += 1
        dic = {}
        dic['id'] = id
        text = content[item[0]]
        text = text.replace(item[1][0], '<< ' + item[1][0] + ' >>', 1).replace(item[1][2], '[[ ' + item[1][2] + ' ]]',1)
        dic['text'] = text
        target_content.append(dic)

    return target_content

# Print the runtime by hours:minutes:seconds
def print_runtime(text, start, stop):
    runtime = stop - start
    h = int(runtime // 3600)
    m = int((runtime - h * 3600) // 60)
    s = int(runtime - h * 3600 - m * 60)
    print(text + str(h) + ':' + str(m) + ':' + str(s))

# Main program
#---------------------------------------------------------------------------------------------------------------------
start = timeit.default_timer()

# Initialize the relation
relation_v = "nói nghe là"
relation_c = "và hoặc"

# Read file's content
has_accents_content = read_content('file path + file name')

# Normalize many rules in Vietnamese
content = []
for text in has_accents_content:
  text = text.replace('vn','VN').replace('cs','CS').replace('nsut','NSUT').replace('gt','GT')
  content.append(text)

'''
If you just wanna test the program whether it can run good or not:
- If yes: set the debug is True
- If no: set the debug is False
'''
start_kg = timeit.default_timer()
kg = extract_relation(content, relation_v, relation_c, debug = True)
stop_kg = timeit.default_timer()
print_runtime('Extract relation runtime: ', start_kg, stop_kg)

target_content = create_content(kg, content)
stop = timeit.default_timer()
print_runtime('Full runtime: ', start, stop)

# Export the target dataset to csv file
df = pd.DataFrame(target_content)
df.to_csv('output_file_name')

# THE END