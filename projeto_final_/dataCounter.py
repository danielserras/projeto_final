import json

numBedrooms = []
maxCapacity = []
listingType = []

#Reading file 
with open("data2.json") as myfile:
        data=myfile.read()
obj = json.loads(data)

#Get file data
for line in obj:
    if line['model'] == "mainApp.property":
        numBedrooms.append(line["fields"]["bedrooms_num"])
    if line['model'] == "mainApp.listing":
        maxCapacity.append(line["fields"]["max_occupancy"])
        listingType.append(line["fields"]["listing_type"])

print("-= Tipo de alojamento =-")
print("Apartment -> " + str(listingType.count("Apartment")))
print("House -> " + str(listingType.count("House")))
print("Studio -> " + str(listingType.count("Studio")))
print("Bedroom -> " + str(listingType.count("Bedroom")))
print("-= Quartos =-")
print("1 bedroom -> " + str(numBedrooms.count(1)))
print("2 bedroom -> " + str(numBedrooms.count(2)))
print("3 bedroom -> " + str(numBedrooms.count(3)))
print("4 bedroom -> " + str(numBedrooms.count(4)))
print("5 bedroom -> " + str(numBedrooms.count(5)))
print("-= Capacidade =-")
print("1 max -> " + str(maxCapacity.count(1)))
print("2 max -> " + str(maxCapacity.count(2)))
print("3 max -> " + str(maxCapacity.count(3)))
print("4 max -> " + str(maxCapacity.count(4)))
print("5 max -> " + str(maxCapacity.count(5)))