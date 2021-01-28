import string
import numpy as np
from nltk.corpus import stopwords
from collections import OrderedDict
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

alpha = 0.001


def parse_data(filename):
    try:
        file_desc = open(filename, 'r')
        content = ""
        while chunk := file_desc.read(1024):
            content += chunk
        return content
    except IOError as exception:
        print(type(exception), str(exception))
        exit(1)


def preprocess_input(content):
    stopwords_set = set(stopwords.words('romanian'))
    input_data = list()
    sentences = content.split('.')
    for index in range(len(sentences)):
        sentences[index] = sentences[index].strip()
        sentence = sentences[index].split()
        words = [word.strip(string.punctuation).lower() for word in sentence if word not in stopwords_set]
        input_data.append(words)
    return input_data


def remove_duplicates(content):
    return list(OrderedDict.fromkeys(content))


def init_training_data(sentences, window_size):
    flattened_sentences = sum(sentences, [])
    unique_words = remove_duplicates(flattened_sentences)
    unique_count = len(unique_words)

    input_layer = list()
    hidden_layer = list()

    for sentence in sentences:
        for position, word in enumerate(sentence):
            target_word = [0 for x in range(unique_count)]
            target_word[unique_words.index(word)] = 1
            target_context = [0 for x in range(unique_count)]
            for offset in range(position - window_size, position + window_size):
                if position != offset and position >= 0 and offset < len(sentences):
                    target_context[unique_words.index(unique_words[offset])] = 1
            input_layer.append(target_word)
            hidden_layer.append(target_context)
    return input_layer, hidden_layer


def softmax(x):
    return np.exp(x) / sum(np.exp(x))


def propagate_forward(x, weights, weights_prime, n):
    h = np.dot(weights.T, x).reshape(n, 1)
    u = np.dot(weights_prime.T, h)
    y = softmax(u)

    return h, u, y


def propagate_backwards(x, t, v, weights, weights_prime, h, y):
    e = y - np.asarray(t).reshape(v, 1)
    w_prime_d = np.dot(h, e.T)
    w_d = np.dot(np.array(x).reshape(v, 1), np.dot(weights_prime, e).T)
    weights = weights - alpha * w_d
    weights_prime = weights_prime - alpha * w_prime_d
    return weights, weights_prime


def train_sg_model(context, neurons_count, epoch_count, window_size, target_words):
    flattened_sentences = sum(context, [])
    unique_words = remove_duplicates(flattened_sentences)
    unique_count = len(unique_words)
    input_layer, hidden_layer = init_training_data(context, window_size)

    weights = np.random.uniform(-0.8, 0.8, (unique_count, neurons_count))
    weights_prime = np.random.uniform(-0.8, 0.8, (neurons_count, unique_count))

    for epoch_index in range(epoch_count):
        loss_value = 0
        for instance_index in range(0, len(input_layer)):

            h, u, y = propagate_forward(input_layer[instance_index], weights, weights_prime, neurons_count)
            weights, weights_prime = propagate_backwards(input_layer[instance_index],
                                                         hidden_layer[instance_index], unique_count,
                                                         weights,
                                                         weights_prime, h, y)
            C = 0
            for index in range(unique_count):
                if hidden_layer[instance_index][index]:
                    loss_value += C * np.log(np.sum(np.exp(u)))
                    C = C + 1

        print(f'Epoch {epoch_index} done with loss:{loss_value}!')

    for word in target_words:
        if word in unique_words:
            index = unique_words.index(word)
            encoding = [0 for i in range(unique_count)]
            encoding[index] = 1
            probability = propagate_forward(encoding, weights, weights_prime, neurons_count)[2]
            output = {}
            for i in range(unique_count):
                output[probability[i][0]] = i
            if 0.0 in output.keys():
                del output[0.0]
            context_words = []
            for count, k in enumerate(sorted(output, reverse=True)):
                if count <= 6:
                    context_words.append(unique_words[output[k]])
                else:
                    break
            x_embedded_list = list()
            for item in context_words:
                encoding = [0 for i in range(len(unique_words))]
                encoding[unique_words.index(item)] = 1
                x_embedded_list.append(encoding)
            x_embedded_list.append(encoding)
            context_words.append(word)
            x_embedded = TSNE(n_components=2).fit_transform(x_embedded_list)
            plt.scatter([item[0] for item in x_embedded], [item[1] for item in x_embedded])
            for count, item in enumerate(x_embedded):
                plt.text(item[0], item[1], context_words[count])
            plt.show()


if __name__ == '__main__':
    data = preprocess_input(parse_data('stefan.in'))
    print(len(data[0]))
    # train_sg_model(data, 2, 15, 3, ['comfort'])
