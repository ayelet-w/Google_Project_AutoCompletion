import json
from collections import defaultdict


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for letter in letters:
    letter_dict = {letter:[]}
    with open(f'{letter}_dict.json', 'w') as outfile:
        json.dump(letter_dict, outfile)