from PIL import Image
import json
import os
import random
import sys



path = "/input/"
dirname = os.path.dirname(__file__)
#sorted from bottom to top
sorted_layers = ["Backgrounds", "Skin", "Clothing", "Mouth", "Eyes", "Head"]
#pre-condition these two arrays have the same length
categories = ["/Legendary/", "/SuperRare/", "/Rare/", "/Standard/"] 
chances = [0.01, 0.09, 0.2, 0.7] #chance of getting above category
real_chances = {}
editions = sys.argv[1]



def generate_image(edition):
    generated_image = Image.open(dirname + path + "base.png")
    attributes = []
    metadata = {"description": "8,765 mutated twitter eggs living on the Ethereum blockchain. Each egg is unique and a composition of hundreds of attributes, your Default Egg's chance of being generated is one in 2.5 quadrillion",
                "external_url": "www.defaulteggs.com",
                "name": "Default Egg #"+edition}

    for layer in sorted_layers:
        rarity = ""
        rand = random.uniform(0, 1)

        for index, chance in enumerate(real_chances[layer]):
            if rand < chance : 
                rarity = categories[index]
                break

        folder = dirname + path + layer + rarity
        file_name = random.choice(os.listdir(folder))
        addative_image = Image.open(folder + file_name)
        generated_image.paste(addative_image, (0, 0), addative_image)
        addative_image.close()
        
        attributes.append({"trait_type": layer,"value":file_name[0:-4]})

    generated_image.save("output/images/"+edition+".png")
    metadata["attributes"] = attributes

    with open("output/metadata/"+edition, 'w') as outfile:
        json.dump(metadata, outfile, indent=4)

    generated_image.close()
    outfile.close()
        
                
            
#re-weighs the percentage to amt of files
def calculateChances():
    new_chances = []
    for layer in sorted_layers:
        for index1, chance in enumerate(chances):
            DIR = dirname + path + layer + categories[index1]
            file_count = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
            new_chances.append(chance * file_count)
        
        array_sum = sum(new_chances)
        new_chances[:] = [chance / array_sum for chance in new_chances]

        for index2, new_chance in enumerate(new_chances):
            if index2 > 0 : new_chances[index2] += new_chances[index2-1]

        real_chances[layer] = new_chances
        new_chances = []




def updateCID(cid):
    directory = dirname + "/output/metadata/"

    for file_name in os.listdir(directory):
        a_file = open(directory+file_name, "r")
        json_object = json.load(a_file)
        a_file.close()

        json_object["image"] = "ipfs://"+cid+"/"+file_name+".png"

        a_file = open(directory+file_name, "w")
        json.dump(json_object, a_file, indent=4)
        a_file.close()


#=======================================================


calculateChances()

for edition in range(int(editions)+1):
    print("Creating edition: " + str(edition))
    generate_image(str(edition))

cid = input("Enter CID: ")
updateCID(cid)