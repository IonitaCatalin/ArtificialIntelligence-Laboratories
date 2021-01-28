import json
import re
import nltk
from nltk.corpus import stopwords


def remove_diacritics(content):
    return [substring.encode('ascii', 'ignore').decode() for substring in content]


def remove_stopwords(filename, output):
    romanian_stopwords = set(stopwords.words('romanian'))
    clean_stopwords = remove_diacritics(romanian_stopwords)

    descriptor = open(filename, 'r')
    new_file_desc = open(output + ".txt", 'w+')
    line = descriptor.read()
    words = line.split()
    for r in words:
        if r not in clean_stopwords:
            new_file_desc.write(" " + r)


def build_model(filename):
    descriptor = open(filename, 'r')
    content = descriptor.read()
    data = re.split(r"[ !?()\[\],\".:;]+", content)
    word_dictionary = dict()
    for word in data:
        if word in word_dictionary.keys():
            word_dictionary[word] = word_dictionary[word] + 1
        else:
            word_dictionary[word] = 1

    for key in word_dictionary.keys():
        word_dictionary[key] = word_dictionary[key] / len(data) * 1000000

    return word_dictionary


def export_model(model, model_name):
    json_dump = json.dumps(model)
    open(model_name + '.json', 'w').write(json_dump)


def compare_models(f_model, s_model):
    similitude = 0

    for key in s_model.keys():
        if key in f_model.keys():
            similitude += abs(f_model[key] - s_model[key])
        else:
            similitude += s_model[key]

    return similitude, similitude / len(s_model)


if __name__ == '__main__':
    nltk.download('stopwords')
    # remove_stopwords('eminescu.txt', 'eminescu_normalized')
    # first_model = build_model('eminescu_normalized.txt')
    # export_model(first_model, 'eminescu_model')
    # remove_stopwords('harapalb.txt', 'harapalb_normalized')
    # second_model = build_model('harapalb_normalized.txt')
    # export_model(second_model, 'harapalb_model')
    remove_stopwords('stefan.txt','stefan_normalized')
    stefan_model=build_model('stefan_normalized')
    print(stefan_model)

    print(compare_models(first_model, second_model))
