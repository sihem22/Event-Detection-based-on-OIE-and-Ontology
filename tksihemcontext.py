from tkinter import *
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import spacy
from spacy import displacy
from tabulate import tabulate

tabulate.PRESERVE_WHITESPACE = True
from table_tkinter import *

main = Tk()
main.geometry("600x400+350+400")
main.title('Ontologie')


def get_context_formel():
    stop = set(stopwords.words('english'))
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(salut.get())
    _tokens = []
    cc = str(doc)

    verb = cc.split(';')[1].split(';')[0]
    ents = []
    for token in doc:
        if token.lemma_ not in stop:
            _tokens.append(token.lemma_)
    orgs = [ent.label_ for ent in doc.ents]

    PERSON = []
    ORG = []
    coming_stat = 0
    if 'PERSON' in orgs or 'ORG' in orgs:
        if 'appoint' in _tokens:
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    PERSON.append(str(ent))
                    ents.append({'start': ent.start_char,
                                 'end': ent.end_char,
                                 'label': 'COMING PERSON'})
                if ent.label_ == 'ORG':
                    ORG.append(str(ent))
                    ents.append({'start': ent.start_char,
                                 'end': ent.end_char,
                                 'label': 'ORG IN'})
                    coming_stat = 1

        if 'resign' in _tokens:
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    ents.append({'start': ent.start_char,
                                 'end': ent.end_char,
                                 'label': 'LEAVING Person'})
                if ent.label_ == 'ORG':
                    ents.append({'start': ent.start_char,
                                 'end': ent.end_char,
                                 'label': 'ORG OUT'})
                    coming_stat = 0
    _dict = {
        'text': cc,
        'ents': ents,
        'title': None
    }
    print(cc)
    BR = ''
    # --l'affichage de tableau--
    p = "  |"  # la premiere ligne du tableau
    j = 0
    # for ent in doc.ents:
    #     p=p+ent.label_+"|"
    # print(p)
    # BR=p +'\n'

    # for w in doc.ents:
    #     espace = " "*(len(w)-1)
    # m = person + '|' + 'X | |\n'

    # m += str(token)+"|"   
    # if token.ent_type_ == ent.label_:

    #             m=m+"X"+espace+"|"
    # else:
    #             m=m+" "+espace+"|"
    # print(m)
    table = [['  X  ', 'Person', 'ORG', 'Coming', 'Leaving']]
    for person in PERSON:
        if coming_stat:
            table.append([person, '  X  ', ' ', '  X ', ' '])
        else:
            table.append([person, '  X ', ' ', ' ', '  X '])
    for org in ORG:
        table.append([org, ' ', '  X', ' ', ' '])

    print(tabulate(table, tablefmt="grid"))
    _table = Table(main, table[0], column_minwidths=[None, None, None, None, None])
    _table.pack(padx=10, pady=10)
    _table.set_data(table[1:])


salut = StringVar()
texte = Entry(main, textvariable=salut, width=60).pack()
bouton1 = Button(main, command=get_context_formel)
bouton1['text'] = 'Context Formel'
bouton1.place(x='200', y='250', )

main.mainloop()
