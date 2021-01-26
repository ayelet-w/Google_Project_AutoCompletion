from collections import defaultdict
import json
from matching_letters import matching_letters


def id_sentences(file_path):
    id_sentence = 0
    sentences = open(file_path,"r")
    dict_id_sentences = dict()
    for sentence in sentences:
        if sentence != "" and sentence != "\n":
            dict_id_sentences[id_sentence] = sentence.replace('\n','')
            id_sentence += 1
    with open('id_sentences.json', 'w') as outfile:
        json.dump(dict_id_sentences, outfile)


def get_add_and_delete_score(txt, offset):
    reduce = 2
    if offset < 4:
        reduce = 10 - 2 * offset
    return 2 * len(txt) - reduce

def get_replace_score(txt, offset):
    reduce = 1
    if offset < 4:
        reduce = 5 - offset
    return 2 * (len(txt) - 1) - reduce


def choose_best_five_sentences(sentences): # {(id_s,offset,score)....}
    if len(sentences) < 6:
        return
    lowest_score = 1000
    sentence_delete = tuple()
    for sentence in sentences:
        if len(sentence) and sentence[2] < lowest_score:
            lowest_score = sentence[2]
            sentence_delete = sentence
    sentences.remove(sentence_delete)


def create_list_auto_copmlete_data(id_sentence, offset, user_input, sentence, del_or_irrel, clean_key = None):
    if del_or_irrel == 0: #original
        score = len(user_input) * 2
    if del_or_irrel == 1: #replace
        score = get_replace_score(user_input, offset)
    if del_or_irrel == 2 and clean_key == None: #delete
        score = get_add_and_delete_score(user_input, offset)
    if del_or_irrel == 2 and clean_key: # insert
        score = get_add_and_delete_score(clean_key, offset)
    tuple_auto_copmlete_data = (id_sentence,offset, score)
    return tuple_auto_copmlete_data


def check_double_ids(set_sentences, new_sentence): #(id, offset, score)
    swap_sentence = tuple()
    for sentence in set_sentences:
        if len(sentence):
            if sentence[0] == new_sentence[0]:
                swap_sentence = sentence
    if len(swap_sentence) == 0:
        set_sentences.append(new_sentence)
        return
    if swap_sentence[2] >= new_sentence[2]:
        return
    if swap_sentence[2] < new_sentence[2]:
        set_sentences.remove(swap_sentence)
        set_sentences.append(new_sentence) 


def swap_one_letter(clean_key, id_sentence, offset,sentence, curr_letter, letter_dict):
    for index,letter in enumerate(clean_key):
        swaped_key = clean_key 
        if letter != ' ':
            for swaped_letter in matching_letters[letter]:
                swaped_key = swaped_key[:index] + swaped_letter + swaped_key[index + 1:]
                if len(swaped_key) and swaped_key[0] == curr_letter:
                    list_auto_copmlete_data = create_list_auto_copmlete_data(id_sentence, offset, swaped_key, sentence, 1)
                    if swaped_key not in letter_dict.keys():
                        letter_dict[swaped_key] = []
                    check_double_ids(letter_dict[swaped_key], list_auto_copmlete_data)
                    choose_best_five_sentences(letter_dict[swaped_key])


def insert_one_letter(clean_key, id_sentence, offset,sentence, curr_letter, letter_dict):
    for index,letter in enumerate(clean_key):
        inserted_key = clean_key 
        if letter != ' ':
            for inserted_letter in matching_letters[letter]:
                if index == 0:
                    inserted_key = inserted_letter + inserted_key[index:]
                else:
                    inserted_key = inserted_key[:index] + inserted_letter + inserted_key[index:]
                inserted_key = clean_key 
                if len(inserted_key) and inserted_key[0] == curr_letter:
                    list_auto_copmlete_data = create_list_auto_copmlete_data(id_sentence, offset, inserted_key, sentence, 2 , clean_key)
                    if inserted_key not in letter_dict.keys():
                        letter_dict[inserted_key] = []
                    check_double_ids(letter_dict[inserted_key], list_auto_copmlete_data)
                    choose_best_five_sentences(letter_dict[inserted_key])

                inserted_key = inserted_key[:index+1] + inserted_letter + inserted_key[index+1:]
                if len(inserted_key) and inserted_key[0] == curr_letter:
                    list_auto_copmlete_data = create_list_auto_copmlete_data(id_sentence, offset, inserted_key, sentence, 2, clean_key)
                    if inserted_key not in letter_dict.keys():
                        letter_dict[inserted_key] = []
                    check_double_ids(letter_dict[inserted_key], list_auto_copmlete_data)
                    choose_best_five_sentences(letter_dict[inserted_key])


def delete_one_letter(clean_key, id_sentence, offset,sentence, curr_letter, letter_dict):
    for index,letter in enumerate(clean_key):
        deleted_key = clean_key 
        if letter != ' ':
            deleted_key = deleted_key[0:index] + deleted_key[index + 1:]
            list_auto_copmlete_data = create_list_auto_copmlete_data(id_sentence, offset, deleted_key, sentence, 2)
            if len(deleted_key) and deleted_key[0] == curr_letter:  
                if deleted_key not in letter_dict.keys():
                    letter_dict[deleted_key] = []
                check_double_ids(letter_dict[deleted_key], list_auto_copmlete_data)
                choose_best_five_sentences(letter_dict[deleted_key])
                


def clean_str(str_input): 
    str_input = str_input.lower()
    str_input = "".join([c for c in str_input if c.isalpha() or c == " "])
    str_input = " ".join(str_input.split())
    str_input = str_input.replace('\n','')
    return str_input 


def letter_dict_init(file_path, curr_letter):
    letter_dict = defaultdict(set)
    with open(f'{curr_letter}_dict.json','r') as json_file:
        letter_dict = json.load(json_file)
    sentences = open(file_path,"r")
    id_sentence = 0
    for sentence in sentences:
        print(sentence) 
        if sentence == '\n' or sentence == "":
            id_sentence -= 1
        for i in range(len(sentence)):
            for j in range(i,len(sentence)):
                clean_key = clean_str(sentence[i: j + 1])
                if len(clean_key) <= 15:
                    if len(clean_key) > 0 and clean_key[0] == curr_letter:
                        list_auto_copmlete_data = create_list_auto_copmlete_data(id_sentence, i, clean_key, sentence, 0)
                        if clean_key not in letter_dict.keys():
                            letter_dict[clean_key] = []
                        check_double_ids(letter_dict[clean_key], list_auto_copmlete_data)
                        choose_best_five_sentences(letter_dict[clean_key])
                    #swap one letter:
                    swap_one_letter(clean_key, id_sentence, i,sentence, curr_letter, letter_dict)
                    #insert one letter:
                    insert_one_letter(clean_key, id_sentence, i,sentence, curr_letter, letter_dict)
                    #delete one letter:
                    delete_one_letter(clean_key, id_sentence, i,sentence, curr_letter, letter_dict)
        id_sentence += 1

        with open(f'{curr_letter}_dict.json', 'w') as outfile:
            json.dump(letter_dict, outfile)


#id_sentences('rfc8496.txt')
# letters = ['a','b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
# for letter in letters:
#     letter_dict_init("rfc8496.txt", letter)


