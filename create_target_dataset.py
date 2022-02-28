from underthesea import pos_tag as pos
from underthesea import word_tokenize as tokenizer
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

# Preprocessing the text
def preprocessing(has_accents_content):
    content = []
    for text in has_accents_content:
        text = text.replace('vn','VN').replace('cs','CS').replace('nsut','NSUT').replace('gt','GT')
        text = text.replace('\n','').replace('@','').strip()
        content.append(text)
    return content

# Search the entities in a relation
def search_entities(pos_t, i):
    ent1 = ""
    ent2 = ""
    relation = pos_t[i][0]
    k = i
    if (i == len(pos_t)-1):
        return None, None
    while (pos_t[i+1][1] == "V"):
        i += 1
        relation += ' ' + pos_t[i][0]
        if (i == len(pos_t)-1):
            return None, None
    if (i+3 > len(pos_t)):
        m = len(pos_t)
    else:
        m = i + 3
    j = i+1
    while (j < m):
        if (pos_t[j][1] == "N" or pos_t[j][1] == "Np" or pos_t[j][1] == "M"):
          ent2 += pos_t[j][0] + " "
        else:
          break
        j += 1
    t = k-1
    if (k == 0):
        ent1 = ""
    else:
        while (pos_t[k-1][1] == "P" or pos_t[k-1][1] == "N" or pos_t[k-1][1] == "Np"):
            ent1 = pos_t[k-1][0] + ' ' + ent1
            k -= 1
    if (ent1 and ent2 and (ent1.strip() != ent2.strip())):
        return [ent1.strip(), relation, ent2.strip()], [k,t,i+1,j-1]
    else:
        return None, None

# Extract the relation in a text from file's text
def extract_relation(content, debug = True):
    kg = []
    index = []
    count = 0
    if (debug):
        n_loop = 500
    else:
        n_loop = len(content)
    for text in content[:n_loop]:
        count += 1
        pos_t = list(pos(text))
        check = False
        id = False
        for i in range(len(pos_t)):
            if (pos_t[i][1] == "V"):
                check, id = search_entities(pos_t, i)
            if (check):
                t = ['', '', '']
                if (len(kg) != 0):
                    t = kg[-1]
                if (check[1] not in t[1]):
                    kg.append(check)
                    index.append([count, id])
                check = False
    return kg, index

# Create content of target dataset
def create_content(content, index):
    target_content = []
    count = -1
    for item in index:
        count += 1
        dic = {}
        text = tokenizer(content[item[0]])
        text.insert(item[1][3] + 1, "]]")
        text.insert(item[1][2], "[[")
        text.insert(item[1][1] + 1, ">>")
        if (item[1][0] == -1):
            text.insert(0, "<<")
        else:
            text.insert(item[1][0], "<<")
        dic['text'] = ' '.join(text)
        dic['id'] = count
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

# Read file's content
has_accents_content = read_content('file path + file name')

# Preprocessing
start = timeit.default_timer()
content = preprocessing(has_accents_content)
stop = timeit.default_timer()
print_runtime('Preprocessing runtime: ', start, stop)

'''
If you just wanna test the program whether it can run good or not:
- If yes: set the debug is True
- If no: set the debug is False
'''
start_kg = timeit.default_timer()
kg, index = extract_relation(content, debug = True)
stop_kg = timeit.default_timer()
print_runtime('Extract relation runtime: ', start_kg, stop_kg)

target_content = create_content(content, index)
stop = timeit.default_timer()
print_runtime('Full runtime: ', start, stop)

# Export the knowledge graph to txt file
with open('output_filename', 'w') as f:
    f.write('[entity 1, relation, entity 2]\n')
    for item in kg:
        f.write(str(item)+'\n')

# THE END
