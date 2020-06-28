import requests
from bs4 import BeautifulSoup

import json
import sys
from multiprocessing import Pool

from pprint import pprint
import config as cfg

bad_spells = ['trap-the-soul']
def main():
    #in spell list but the spell page is broken

    result = [] 
    spells = getSpellList()

    if (len(sys.argv) < 2):
        print("invalid input, allowed options:\nlist\njson")
        sys.exit(1)
 
    if (sys.argv[1] == 'list'):
        for spell in spells:
            print(spell)

    elif(sys.argv[1] == 'json'):
        p = Pool(processes=cfg.NUM_PROC)
        result = p.map(parseSpell, spells)
        p.close()
        p.join()
        with open(cfg.ASSETS+"spells.json", "w+") as out:
            out.write(json.dumps(result, indent=4, sort_keys=True))

    elif(sys.argv[1] == "spell" and sys.argv[2]):
        pprint(parseSpell(sys.argv[2]))

    else:
        print("invalid input, allowed options:\nlist\njson")
        sys.exit(1)
        


def getSpellList():
    # general rule:
    # 'Name of Spell' -> 'name-of-spell'

    data = requests.get('https://www.dnd-spells.com/spells')
    soup = BeautifulSoup(data.text, 'html.parser')

    spells = []

    for tr in soup.find_all('tr'):
        spell = [" ".join(td.text.split()) for td in tr.find_all('td') if td.text.split() != '']
        if(spell):
            # isolate spell name
            spell = spell[1]
            spell = spell.replace(' (Open in new window)','')
            # replace spaces with - and remove ignored characters
            spell = spell.replace(u'\u2019', "") \
                         .replace(u'\u2013', "") \
                         .replace(' ', '-') \
                         .replace("'", '') \
                         .replace('/', '')

            if ("(Ritual)" in spell):
                spell = spell.replace("(Ritual)","ritual")

            spell = spell.lower()
            
            # for some reason this spell does not follow the ritual api rule
            if ("detect-poison" in spell):
                spell = spell.replace("-ritual","")

            if (spell not in bad_spells):
                spells.append(spell)

    return spells

def parseSpell(name):
    url = 'https://www.dnd-spells.com/spell/'+ name.strip()
    data = requests.get(url)

    # parse html for text, split into lines, remove irrelevant lines
    soup = BeautifulSoup(data.text, 'html.parser')
    text = soup.text.split('\n')

    # remove extra text
    start = text.index('Remove the adds')
    end = text.index(' Create and save your own spellbooks, sign up now!')
    text = text[start + 1:end]

    # parse
    text = [" ".join(line.split()) for line in text] # remove whitespace
    text = [line for line in text if line != ''] # remove empyt lines
    
    spell = {}

    spell['Name'] = text.pop(0).replace(u'\u2019', "'")
    spell['School'] = text.pop(0)
    spell['Level'] = text.pop(0).split(": ")[1]
    spell['Casting time'] = text.pop(0).split(": ")[1]
    spell['Range'] = text.pop(0).split(": ")[1]
    spell['Components'] = text.pop(0).split(": ")[1] \
                                     .replace(u'\u2019', "'") \
                                     .replace(u'\u2013', "'") \
                                     .replace(u'\u2014', "-")
    spell['Duration'] = text.pop(0).split(": ")[1]

    spell['Class'] = []
    while True:
        line = text.pop()
        if line == "A":
            break
        if line != 'spell':
            spell['Class'].append(line)

    spell['Page'] = text.pop().split(": ")[1]

    # The leftover lines are the spell blurb
    # Join and replace unwanted unicode
    spell['Text'] = [line.replace(u'\u2019', "'")
                         .replace(u'\u2018', "'")
                         .replace(u'\u2022', "'")
                         .replace(u'\u2014', "-")
                         .replace(u'\ufffc', "")
                         .replace(u'\u00d7', "*")
                         .replace(u'\u201c', "\"")
                         .replace(u'\u201d', "\"")
                         .replace(u'\u0093', "\"")
                         .replace(u'\u0094', "\"")
                         .replace(u'\u2013 \u0097', "-")
                         .replace(u'\u0097', "-")
                         .replace(u'\u2013', "-")
                         for line in text]

    return spell

if __name__ == "__main__":
    main()
