import json 


def auto_complete(str_input): 
    with open('id_sentences.json') as json_file:
        id_sentences = json.load(json_file)
    str_input = str_input.lower()
    str_input = "".join([c for c in str_input if c.isalpha() or c == " "])
    str_input = " ".join(str_input.split())
    with open(f'abc_dicts/{str_input[0]}_dict.json') as json_file:
        data = json.load(json_file)
    if str_input not in data.keys():
        return
    five_sentences = data[str_input]
    five_sentences = sorted(five_sentences, reverse=True)
    print("Here " + f"{len(five_sentences)} " + "suggustion:\n")
    for index,sentence in enumerate(five_sentences):
        print(f"{index + 1}. " + id_sentences[str(sentence[0])])


def output_(text):#
    print(text)
def input_():
    text = input('The system is ready. Enter your text: \n')
    while True:
        auto_complete(text)
        if text.endswith("#"):
            break
        text += input(text)
    input_()
if __name__ == '__main__':
    input_()

