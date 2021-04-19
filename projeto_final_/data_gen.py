import numpy as np
import random
import sys
import json

common_fields = ["model", "pk", "fields"]
user_models = ["mainApp.landlord", "auth.user", "mainApp.app_user"]
listing_models = [("mainApp.imagealbum",(("name", 10),)), ("mainApp.image", (("name", 10), ("is_cover", 0), ("image", 14), ("album", 3))), ("mainApp.property",(("landlord", 15),("address", 13), ("floor_area", 2), ("garden", 0), ("garage", 0), ("street_parking", 0), ("internet", 0), ("electricity", 0), ("water", 0), ("gas", 0), ("pets", 0), ("overnight_visits", 0), ("cleaning_services", 0), ("smoke", 0), ("latitude", 6), ("longitude", 7), ("bedrooms_num", 1))), ("mainApp.bathroom",(("associated_property", 3), ("toilet", 0), ("sink", 0), ("shower", 0), ("b_window", 0), ("bathtub", 0), ("bidet", 0))), ("mainApp.bedroom", (("associated_property", 3), ("be_chairs", 0), ("be_sofa", 0), ("be_sofa_bed", 0), ("be_window", 0), ("num_single_beds", 1), ("num_double_beds", 1), ("max_occupancy", 1), ("be_balcony", 0), ("wardrobe", 0), ("be_desk", 0), ("chest_of_drawers", 0), ("tv", 0), ("heater", 0), ("air_conditioning", 0), ("lock", 0), ("ensuite_bathroom", 0))), ("mainApp.kitchen", (("associated_property", 3), ("dish_washer", 0), ("k_window", 0), ("fridge", 0), ("freezer", 0), ("cooker", 0), ("dishes_cutlery", 0), ("pans_pots", 0), ("dishwasher_machine", 0), ("dryer", 0),("oven", 0), ("k_table", 0), ("laundering_machine", 0), ("k_chairs", 0), ("microwave", 0), ("k_balcony", 0))), ("mainApp.livingroom", (("associated_property", 3), ("l_chairs", 0), ("l_sofa", 0), ("l_sofa_bed", 0), ("l_window", 0), ("l_table", 0), ("l_balcony", 0), ("l_desk", 0))), ("mainApp.listing", (("allowed_gender", 8), ("monthly_payment", 2), ("availability_starts", 4), ("availability_ending", 5), ("title", 10), ("description", 9), ("security_deposit", 2), ("max_occupancy", 1), ("listing_type", 11),("is_active", 12), ("album", 3))), ("mainApp.property_listing", (("main_listing", 3), ("associated_property", 3)))]
listing_types = ["Apartment", "House", "Studio", "Bedroom"]

#Listing type and desc generator
adjectives = ["cosy", "big", "huge", "small", "homely", "tidy", "rustic", "modern", "luxury", "secluded", "comfortable", "nice", "pleasant", "pretty", "furnished"]
nouns = ["house", "apartment", "flat", "home"]
features = ["with netflix", "with free wi-fi", "near center", "with ocean view", "with moutain view", "near universities", "with great location", "close to metro"]
from shapely.geometry import Polygon, Point


poly = Polygon([(37.0781888, -8.3008575), (37.0946215, -8.1978607), (37.0694233, -8.1058502), (37.0354472, -8.0275726), (37.0102293, -7.9657745), (37.0431206, -7.7831268), (37.2172061, -7.46521), (38.0870132, -7.6409912), (39.3470425, -7.6959229), (40.709792, -7.3553467), (41.207589, -7.2454834), (41.4797758, -7.2674561), (41.463312, -8.7506104), (41.2747102, -8.7258911), (41.0917722, -8.6407471), (40.9155881, -8.6434937), (40.2040504, -8.8549805), (40.1715282, -8.881073), (40.141615, -8.8618469), (40.1074874, -8.8563538), (39.603572, -9.0444946), (39.3364218, -9.2697144), (38.7862045, -9.4235229), (38.7112325, -9.3218994), (38.6383273, -9.2120361), (38.4836948, -9.1516113), (38.4664928, -9.0582275), (38.50949, -8.9373779), (38.4191664, -8.8220215), (38.2899366, -8.7451172), (37.596824, -8.6791992), (37.0661359, -8.8027954), (37.0924307, -8.7327576), (37.0857209, -8.6846924), (37.1168, -8.6517334), (37.1241913, -8.5501099), (37.1198113, -8.4539795), (37.0781888, -8.3008575)])

def random_points_within(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)

    return points



def getRandom(dataType, iteration_counter = None):
    """
    Recebe uma representação numerica de um tipo de dados e deolve um 
    valor aleatorio apropiado para esse tipo
    0 -> bool
    1 -> numérico baixo (ex, num de quartos, ocupacao)
    2 -> numérico alto (ex, valor da renda, valor caucao)
    3 -> referencia a uma chave interna (ex associated_property)
    4 -> data menor
    5 -> data maior
    6 -> latitude
    7 -> longitude
    8 -> genero permitido
    9 -> descrição textual (ex descriçao)
    10 -> textual curto (ex titulo)
    11 -> listing type
    12 -> True, not random but usefull
    13 -> morada
    14 -> caminho de imagem
    """
    if dataType == 0:
        return bool(random.getrandbits(1))

    elif dataType == 1:
        return random.randint(1, 5)

    elif dataType == 2:
        return random.randint(200, 1000)

    elif dataType == 3:
        return iteration_counter
    elif dataType == 4:
        meses30 = [4,6,9,11]
        meses31 = [1,3,5,7,8,10,12]
        year = str(2020)
        month = random.randint(1, 12)
        if month in meses31:
            day = random.randint(1, 31)
        elif month in meses30:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)
        
        if month < 10:
            monthString = "0" + str(month)
        else:
            monthString = str(month)
        
        if day < 10:
            dayString = "0" + str(day)
        else:
            dayString = str(day)

        return year + "-" + monthString + "-" + dayString

    elif dataType == 5:
        meses30 = [4,6,9,11]
        meses31 = [1,3,5,7,8,10,12]
        year = str(2021)
        month = random.randint(1, 12)
        if month in meses31:
            day = random.randint(1, 31)
        elif month in meses30:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)
        
        if month < 10:
            monthString = "0" + str(month)
        else:
            monthString = str(month)
        
        if day < 10:
            dayString = "0" + str(day)
        else:
            dayString = str(day)

        return year + "-" + monthString + "-" + dayString

    elif dataType == 6:
        return str(random_points_within(poly,1)[0].x)
    elif dataType == 7:
        return str(random_points_within(poly,1)[0].y)
    elif dataType == 8:
        return "onlyWomens"
    elif dataType == 9:
        return adjectives[random.randint(0, len(adjectives)-1)] + " " + adjectives[random.randint(0, len(adjectives)-1)] + " " +  nouns[random.randint(0, len(nouns)-1)] + " " + features[random.randint(0, len(features)-1)]
    elif dataType == 10:
        return "Cosy little house"
    elif dataType == 11:
        return listing_types[random.randint(0, len(listing_types)-1)]
    elif dataType == 12:
        return True
    elif dataType == 13:
        return "Avenida da Republica 67 Lisboa"
    elif dataType == 14:
        return "mainApp/static/https://picsum.photos/300/200"
    elif dataType == 15:
        return 1


def dictMaker(iteration_counter):
    print(iteration_counter, "HERE")
    dictList = []
    for model in listing_models:
        fruitdict = {}
        for field in common_fields:
            if field == "model":
                fruitdict[field] = model[0]
            elif field == "fields":
                nested_dict = {}
                for field0 in model[1]:
                    nested_dict[field0[0]] = getRandom(field0[1], iteration_counter+1)
                fruitdict[field] = nested_dict
 
            else:
                fruitdict[field] = iteration_counter+1
        dictList.append(fruitdict)
    return dictList

def writeData(num_users, num_properties):
    data = []
    for i in range(num_properties):
        result = dictMaker(i+1)
        for table in result:
            data.append(table)

    with open("data2.json", "w") as write_file:
        json.dump(data, write_file, indent=4)



        

if __name__ == "__main__":
    print("Data Gen v Alpha 0.1, cria um ficheiro json com <num de users> e <num de propriedades>, pasados por linha de comandos")
    if(len(sys.argv) == 3):
        try:
            num_users = int(sys.argv[1])
            num_properties = int(sys.argv[2])            
        except:
            print("Os argumentos dados devem ser numeros inteiros")
            exit()
        writeData(num_users, num_properties)
    else:
        print("Numero Invalido de Argumentos, <num de users>, <num de propriedades>")