from PIL import Image
import json
import os
import random
import sys

#=======================================================
# CHANGE THE FOLLOWING PARAMS TO YOUR NEED
#=======================================================

# Collection information:
description = "Example description"
url = "www.example_url.com"
name = "Example Name"

# Layer information:
sorted_layers = ["Backgrounds", "Skin", "Clothing", "Mouth", "Eyes", "Head"]
categories = ["/Legendary/", "/SuperRare/", "/Rare/", "/Standard/"] 
chances = [0.075, 0.125, 0.25, 0.55] # odds of getting above category

#=======================================================


# Global variables:
path = "/input/"
dirname = os.path.dirname(os.path.abspath(__file__))
real_chances = {}
editions = sys.argv[1]

def generate_image(edition):
    generated_image = Image.open(dirname + path + "base.png")
    attributes = []
    metadata = {"description": description,
                "external_url": url,
                "name": name+ "#" + edition}

    for layer in sorted_layers:
        rarity = ""
        rand = random.uniform(0, 1)

        for index, chance in enumerate(real_chances[layer]):
            if rand < chance : 
                rarity = categories[index]
                break

        folder = dirname + path + layer + rarity
        file_name = random.choice(list(set(os.listdir(folder)) - {".DS_Store"}))
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
    assert len(categories) == len(chances)

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
        
def main():
    os.makedirs("output/metadata", exist_ok=True)
    os.makedirs("output/images", exist_ok=True)

    calculateChances()

    for edition in range(int(editions)+1):
        print("Creating edition: " + str(edition))
        generate_image(str(edition))

    cid = input("Enter CID: ")
    updateCID(cid)

main()