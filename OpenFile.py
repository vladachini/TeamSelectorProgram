import csv
import hashlib
from faker import Faker

def csvOpener(filename)->dict:
    players = []
    main_dict = {}
    with open(filename, encoding='utf-8-sig') as File:
        reader = csv.DictReader(File)
        for row in reader:
            players += [row]
    for player in players:
        f_name = player.get('First_name')
        l_name = player.get('Last_name')
        dob = player.get('DOB') #MIGHT NEED TO CHANGE TO DATE TYPE
        combine = f_name+l_name+dob
        id = hashlib.sha1(str.encode(combine)).hexdigest()[0:8] #id is a string type
        main_dict[id] = player
    return main_dict

def generate(filename, entries:int):
    faker = Faker()
    with open(filename, mode='a') as player_file:
        writer = csv.writer(player_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,entries) :
            writer.writerow([str(faker.first_name()), str(faker.last_name()), str(faker.date_of_birth()),
                             int(faker.random_int(155, 195)),faker.random_int(1, 5),faker.random_int(1, 5),
                             faker.random_int(1, 5),faker.random_int(1, 5)])


def generate10(filename, entries:int):
    faker = Faker()
    with open(filename, mode='a') as player_file:
        writer = csv.writer(player_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,entries) :
            writer.writerow([str(faker.first_name()), str(faker.last_name()), str(faker.date_of_birth()),
                             int(faker.random_int(155, 195)),faker.random_int(1, 10),faker.random_int(1, 10),
                             faker.random_int(1, 10),faker.random_int(1, 10)])

