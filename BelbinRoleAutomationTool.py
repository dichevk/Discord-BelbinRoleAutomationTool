from numpy import loadtxt
import numpy as np
import ast
from collections import ChainMap
import requests
import json
from itertools import combinations, starmap
import pandas as pd
import openpyxl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import Iterable
nltk.download('stopwords')
nltk.download('punkt')

all_names_identifiers = dict()
names_identifiers_map = dict()
big_dict = dict()
timestamp_dict = dict()
big_timestamp_dict = dict()
new_dict = dict()
avg_dict = dict()
implementers = ['EloWizard9000','Dimitrios Katsantonis','Doortje Dieleman','taybt','sososo1234','I make memes','Danish','Kąsnys','Suzanne','florian','David Galati','Larswijn','Jurre','Mette','Migush','Lys','An']
plants = ['Moose946','ciolos','Mariska','Jamie','🔥Dirk🔥','Everard de Vree','MichRacz00','ni3k','Demolator200','Hubix']
shapers = ['Abrahans','Silas','BrianPvanOers','StephanWithPH','Catgirl','AlexP','TomE','Andrea_01','Tim Klampe','JobvD','Deimon','TimKwink','Brianna','Cati','Murky','Cristian Zubcu','Nova Mane','Shasank','Barry','Ward']
monitorevaluators = ['Hein','Rocinante','CatBreakOut','Karsten','hayodehaai','coolajor']
resourceinvestigators =['takkie','Mathijs','Krzysztof','Cemill']
coordinators = ['Foubzi','teyim','TOMBONE','Niblet','kasteelharry','ScreamingKoala','Mohamed Waleed','Valerie Seinstra','Teodora','Dani Baba','reikal951','Liran Neta','AAndré','BasVreeman']
specialists = ['shadow_booster','Toghrul Garalov','minkaas','ardasatici','Miles','Vaseto108','daw10','Faidoo','Novojit','Tessa van Belois','SaDaT','Thomass','jasper','Denel','kaan900p']
teamworkers = ['Quirijn | Kroin','Byeonghun Park','Aleksandra Ignatovich','Jeongyeon','Ajydaar','Edina','VictorMelinceanu','Koen Rienstra','dianab','rusuandrei','MrJnl','Yifan','Ac3','Jelke']
completerfinishers=['GoodGuyEugene','Jelmer','Kristiyan','Kl4wS (Nick)','Victor Mintus','KrisVe','JyYoshi','timo','WillyWagen','Thomas1944567','Arsalaan Khan','Xander Heij','martpostma','BaraNn']
all_users_by_roles_arr = [implementers,plants,shapers,monitorevaluators,resourceinvestigators,coordinators,specialists,teamworkers,completerfinishers]
implementers_words = []
plants_words = []
shapers_words = []
monitorevaluators_words = []
resourceinvestigators_words = []
coordinators_words = []
specialists_words = []
teamworkers_words = []
completerfinishers_words = []
all_users_words = [implementers_words,plants_words,shapers_words,monitorevaluators_words,resourceinvestigators_words,coordinators_words,specialists_words,teamworkers_words,completerfinishers_words]
all_users_words_arr = []

'''
def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item
'''
def fill_the_words():
    for some,j in zip(all_users_by_roles_arr,all_users_words):
        for name in some:
            j.append(big_dict[name])
    return all_users_words_arr


headers = {
        "authorization": "MjE5MTcwNTU3MzE1MzgzMjk3.GF5jYI.8pkonmSAbCqcE9Bdzil5rzj1cnyvvjhlJSlp1w",


    }
def retrieve_names(chanelid):


    r = requests.get(f'https://discord.com/api/v9/channels/{chanelid}/messages', headers=headers)
    info_json = json.loads(r.text)
    #print(info_json)
    #f = open('messagescontent.txt', 'w', encoding="utf-8")
    for value in info_json:

        #print(value['author']['username'] + ':' + value['content'],'\n')
        if value['author']['username']!= 'Deleted User' and value['author']['username']!='Yeray':
            if value['author']['username'] not in names_identifiers_map:
                names_identifiers_map[value['author']['id']] = value['author']['username']


        #f.write(value['author']['username'] + ':' + value['content'] + '@#;')
        #f.write('\n')
    #f.close()
def retrieve_messages(chanelid):
    r = requests.get(f'https://discord.com/api/v9/channels/{chanelid}/messages', headers=headers)
    info_json = json.loads(r.text)
    for value in info_json:
        for username in big_dict.keys():
            if value['author']['username'] == username:
                big_dict[username].append(read_and_parse_string(value['content']))
        for userr in timestamp_dict.keys():
            if value['author']['username'] == userr:
                timestamp_dict[userr].append(format_timestamp(value['timestamp']))

    for key in list(timestamp_dict):
        if len(timestamp_dict.get(key)) == 0:
            timestamp_dict.pop(key)
    big_timestamp_dict.update(timestamp_dict)
    #print(big_dict)


    #print(timestamp_dict)
    #print(big_dict)
def read_and_parse_string(str):
    text_tokens = word_tokenize(str)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    return tokens_without_sw





def for_all_channels():
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    channels_storage = read_from_file('researchchannels.txt', ',')
    for channel in channels_storage:
        retrieve_names(channel)
    for user in names_identifiers_map.values():
        big_dict[user] = []
        timestamp_dict[user] = []

    for channel in channels_storage:
        retrieve_messages(channel)

    for key,value in big_timestamp_dict.items():
        new_dict[key] = []

        for i in range(len(value)-1):
            if len(value) >0:
                td = datetime.strptime(value[i],fmt) - datetime.strptime(value[i+1],fmt)


                new_dict.get(key).append(int(round(td.total_seconds()/60)))
    adj_weight = 1000
    for user,timedif in new_dict.items():
        for item in timedif:
            item+=1
            adj_weight -= 95
        if adj_weight<0:
            adj_weight = 1
        if len(timedif)!=0:
            avg_dict[user]=(sum(timedif)*adj_weight)/len(timedif)


    #df = pd.DataFrame(data=names_identifiers_map, index = [0])
    #df = (df.T)
    #df.to_excel('usernamessheet.xlsx')

char_arr = []
def init_characteristic(characteristic,traits_list):
    definition_dict = dict()
    traits_dict = dict()


    for i in range(len(traits_list)):
        traits_dict[traits_list[i]] = []


    definition_dict[characteristic] = traits_dict
    #print(definition_dict)
    return definition_dict

def read_from_file(file,delimiter):
    my_file = open(file, 'r')
    content = my_file.read()
    content_list = content.split(delimiter)
    my_file.close()
    #print(content_list)
    return content_list


def add_characteristic(arr,characteristic):
    arr.append(characteristic)



belbin_arr = ["Shaper", "Plant","Co-ordinator","Monitor-Evaluator","Resource-Investigator","Implementer","Teamworker","Completer-Finisher","Specialist"]

for role in belbin_arr:
    add_characteristic(char_arr,role)

Shaper_dict = init_characteristic(char_arr[0], read_from_file("shaper.txt",';'))
Plant_dict = init_characteristic(char_arr[1], read_from_file("plant.txt",';'))
Coordinator_dict = init_characteristic(char_arr[2], read_from_file("coordinator.txt",';'))
MonitorEvaluator_dict = init_characteristic(char_arr[3], read_from_file("monitorevaluator.txt",';'))
ResourceInvestigator_dict = init_characteristic(char_arr[4], read_from_file("resourceinvestigator.txt",';'))
Implementer_dict = init_characteristic(char_arr[5], read_from_file("implementer.txt",';'))
TeamWorker_dict = init_characteristic(char_arr[6], read_from_file("teamworker.txt",';'))
CompleterFinisher_dict = init_characteristic(char_arr[7], read_from_file("completerfinisher.txt",';'))
Specialist_dict = init_characteristic(char_arr[8], read_from_file("specialist.txt",';'))

all_virtues_dict = {**Shaper_dict,**Plant_dict,**Coordinator_dict,**MonitorEvaluator_dict,**ResourceInvestigator_dict,**Implementer_dict,**TeamWorker_dict,**CompleterFinisher_dict,**Specialist_dict}





#build_dict()
def format_timestamp(input_string):
    new_str = input_string.replace('T',' ').replace('+00:00','')
    return new_str



for_all_channels()

with open('messagecontent.txt','w',encoding='utf-8') as f:
    f.write(str(big_dict))
f.close()


MonitorEvaluator_dict['Monitor-Evaluator']['undecisive'].extend(['?','question','maybe','could','thought','think','probably','clarification','advise'])
MonitorEvaluator_dict['Monitor-Evaluator']['Analytical Thinking'].extend(['however','resolve','wondering','idea'])
MonitorEvaluator_dict['Monitor-Evaluator']['prudent'].extend(['Plan','practicing','upload','start','mandatory','submit','planning','version'])

Specialist_dict['Specialist']['technical expertise'].extend(['security','deployment','redeploy','redeployed','credentials','localhost','machine','server','problem','merge','merged','acces','ping','implementation','implemented','Azure','integration','nodejs','integrate','NDA','branch','requirements','master','readme','README','app','pwd','DB','pooling','commit','javascript','function','JSON','XPath','XML','.js','JSONPath','spring','frameworks','backend','XMLHttpRequest','frontend','code','callback','XMLHTTPREQUESTS','http','requests','JS','booleans','routing','complexity','dynamic','switches','react','GitHub','Pascal','Fortran','java'])
Specialist_dict['Specialist']['decision-making'].extend(['give','checked','mentioned','decided','nice-to-haves'])
Specialist_dict['Specialist']['very committed'].extend(['merge','merged','deployed','checked','redeployed','completed','finished','believe','medal','medals','structured','solid','progress','10/10','pass','everything'])
Specialist_dict['Specialist']['professionalism'].extend(['sorry','Sorry','alright',',','.','hour','correct','apologies','Apologies','pardon','Pardon','present','meaningful','Regarding','indication','approximate'
                                           ])
Plant_dict['Plant']['creativity'].extend(['try','LATIN1','ideas','case','curiosity'])
Plant_dict['Plant']['introverted'].extend(['🙂','still','?','propose','ask','proposal','assume','resent','wondering','Ah','aaah','aah','curiousity','maybe'])
Plant_dict['Plant']['unwelcoming to criticism'].extend(['hear/see','souls','vreugd','joy','betterbe','us','mistake','BetterBe'])
CompleterFinisher_dict['Completer-Finisher']['paying attention to detail'].extend(['Also','curiosity','unsure','specific','Overview','required'])
CompleterFinisher_dict['Completer-Finisher']['do not like delegating tasks'].extend(['redeployed','deployed','completed','finished','take','work','commiting','pushing','pushed','restoring','deploy','receive','checking','added','working'])
CompleterFinisher_dict['Completer-Finisher']['highly concentrated'].extend(['problem','stuck','expect'])
Shaper_dict['Shaper']['expressivness'].extend(['do😂','late😂','😂','!','Moreover','card'
])#associate it with emojis
Shaper_dict['Shaper']['patience'].extend(['tomorrow','wait','soon'])
Shaper_dict['Shaper']['motivation'].extend(['brb','ll','deadlines','corrrect','correct','correctly','campus','ready','forward','exactly','improve','final','deadline','grade','8/10'])
Shaper_dict['Shaper']['Networking skills'].extend(['Sorry','kind','everyone','clarify','members','team','guys','hello','Hey','Hello','Guest','We','Hence','behalf','🙏','miscommunication'])

ResourceInvestigator_dict['Resource-Investigator']['negotiating skills'].extend(['voice'])
ResourceInvestigator_dict['Resource-Investigator']['networking skills'].extend(['👍'])
ResourceInvestigator_dict['Resource-Investigator']['relaxed'].extend(['redeployed'])

Coordinator_dict['Co-ordinator']['leadership'].extend(['redeployed','questions','asked','Question','check','updates','cost','effort','charge','Our','concern','ensure','prevent','concerns','product','proposed','main','need','besides','np','meeting','start','progress'])
Coordinator_dict['Co-ordinator']['task division and assignment'].extend(['Dani','tennaz','Jan','Fokstra','issue','via','sent','invite','someone','Ivo','Stefano'])
Coordinator_dict['Co-ordinator']['confidence'].extend(['wdym','wearing','underwear','feeling','sick','shit','look','jcc','useless','stupid','bad'])
Implementer_dict['Implementer']['problem-solving skills'].extend(['mindhash','axis','map','server','working','complete','sense','resource','resources','directory','src/main/java/FileStructure/environments','variable','filehandler','databaseHandler','filehandler','handler','merge','conflicts','git','https','//git.snt.utwente.nl/di21-23/grybb','repository','Maven','pull','master','front-end','back-end','time-frame','finalized','React' ])
Implementer_dict['Implementer']['taking tasks'].extend(['sure','re-submission','trello','board','sprint','tasks','I','ll','add','added'])
Implementer_dict['Implementer']['well-organized'].extend(['meeting','10:30','Tuesday','trello','board','stand-up','4min','15min'])
Implementer_dict['Implementer']['reliable'].extend(['feedback','upload','review','log','Today','today','campus','improve'])
TeamWorker_dict['Teamworker']['supportive'].extend(['redeployed','try','🙂','please','divide','lets','accompanied','great','awesome','feedback','call','help'])
TeamWorker_dict['Teamworker']['diplomatic'].extend(['meeting','contribute','audience','contract','public','effective','dring','unanswered','reason','We','presume'])









sorted_avg_dict = dict(sorted(avg_dict.items(), key=lambda item: item[1]))
unique_words = dict()

def init_unique_words():
    for dictname in all_virtues_dict.keys():
        unique_words[dictname] = []
    for dictname,innerdict in all_virtues_dict.items():
        for trait,innerarr in innerdict.items():
            for value in innerarr:
                if any(value not in subinner for subinner in innerdict.values()):
                    unique_words.get(dictname).append(value)
init_unique_words()
#ako high average na messages -> increase plant
personal_roles_dict = dict()
def find_roles(username):
    personal_pie_chart_value_arr = []
    pie_chart_labels = []
    belbinroles_dict = {'Shaper': 0, 'Plant': 0, 'Co-ordinator': 0, 'Monitor-Evaluator': 0, 'Resource-Investigator': 0,
                        'Implementer': 0, 'Teamworker': 0, 'Completer-Finisher': 0, 'Specialist': 0}
    personal_roles_dict[username] = belbinroles_dict
    for dictname,innerdict in all_virtues_dict.items():
        for trait,innerarr in innerdict.items():
            for value in innerarr:
                for i in big_dict[username]:
                    for j in i:
                        if value == j:
                            personal_roles_dict[username][dictname]+=1

    print(personal_roles_dict)
    for x,y in personal_roles_dict[username].items():
        if y!= 0:
            pie_chart_labels.append(x)
            personal_pie_chart_value_arr.append(y)
    explode = ()
    for i in pie_chart_labels:
        explode = explode + (0.2,)
    #print(unique_words)
    personal_pie_chart_value_arr_np = np.array(personal_pie_chart_value_arr)
    percentage_format = "%1.1f%%"
    plt.pie(personal_pie_chart_value_arr_np,labels = pie_chart_labels,autopct=percentage_format,shadow = True,startangle=90, pctdistance=0.85,explode = explode)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.tight_layout()
    plt.title(username)
    #plt.legend(loc = 'upper right')

    plt.show()


def find_roles_for_all():
    for person in names_identifiers_map.values():
        find_roles(person)
        personal_roles_dict.clear()
'''
def find_roles_for_all():
    pltcounter =0
    for person in names_identifiers_map.values():
        if any(person in sublist for sublist in all_users_by_roles_arr):
            find_roles(person)
            pltcounter+=1
'''
find_roles_for_all()


#something()


# print(timestamp_dict)

#print(fill_the_words())





