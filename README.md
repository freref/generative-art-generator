# Generative Art Generator
Bare-bones layer based generative art generator for NFT's. Automatically generates accompanying metadata json.  
## Requirements
- python3
## Usage
### Populate input directory
The general structure is as follows:  
```
input/
├─ layer #1/
│  ├─ rarity #1
│  ├─ rarity #2
│  ├─ rarity #3
├─ layer #2/
├─ layer #3/
```
### Parameters
Change parameters in ```main.py``` for your collection:
```python
# Collection information:
description = "Example description"
url = "www.example_url.com"
name = "Example Name"

# Layer information:
sorted_layers = ["layer #1", "layer #2", "layer #3", "layer #4", "layer #5", "layer #6"]
categories = ["/rarity #1/", "/rarity #2/", "/rarity #3/", "/rarity #4/"]
chances = [0.075, 0.125, 0.25, 0.55] # odds of getting above category
```
### Run
```
python main.py [# generated images]
```
