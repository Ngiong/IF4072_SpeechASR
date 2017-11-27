import os
from scripts.consts import *
from pprint import pprint

ROOT_DIR = 'Dataset_MFCC/'
DATA_DIR = ['set_1','set_2','set_3','set_4','set_5']

def load_full_transcript():
    transcript = {}

    with open(PROMPTS_FILE, 'r') as fin:
        for line in fin:
            l = line.split(' ')
            transcript[l[0]] = ' '.join(l[1:])

    # pprint(transcript)
    return transcript

def generate_transcript():
    transcript = load_full_transcript()

    if not os.path.exists("cross_validation"):
        os.mkdir("cross_validation")

    # LIST FILE yang ada di directory
    file_list = {}
    for directory in DATA_DIR:
        file_list[directory] = []
        for subdir in os.listdir(ROOT_DIR + directory):
             file_list[directory] += sorted(os.listdir(ROOT_DIR + directory + '/' + subdir))

    for directory in DATA_DIR:
        prompt_dir = "cross_validation/test_" + directory

        if not os.path.exists(prompt_dir):
            os.mkdir(prompt_dir)
        pprint(sorted(file_list[directory])[:5]);
        with open(prompt_dir + '/prompts.tsv', 'w') as fout, open(prompt_dir + '/answer.tsv', 'w') as answer_out:
            for k in sorted(transcript.keys()):
                if k[2:] + '.mfc' not in file_list[directory]:
                    fout.write(k + ' ' + transcript[k])
                else:
                    answer_out.write(k + ' ' + transcript[k])

        data = open(MFCC_LIST_FILE, 'r').readlines()
        gen_scp(file_list, directory, sorted(data))

def gen_scp(file_list, directory, data):
    print(directory)
    train_scp_file = 'cross_validation/test_' + directory + '/train_list.scp'
    test_scp_file = 'cross_validation/test_' + directory + '/answer_list.scp'

    with open(train_scp_file, 'w') as answerfout, open(test_scp_file, 'w') as trainfout:
        for mfc in data:
            if directory not in mfc:
                # print("'"+mfc[26:len(mfc)-1]+"'")
                answerfout.write(mfc)
            else:
                trainfout.write(mfc)
