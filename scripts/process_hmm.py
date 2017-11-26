import os
import scripts.utils as utils
from scripts.consts import *
from shutil import copyfile

def prepare_hmm():
    output_dir = HMM_OUTPUT_DIR + "hmm0"

    for i in range (4):
        hmm_dir = HMM_OUTPUT_DIR + "hmm" + str(i)
        if not os.path.exists(hmm_dir):
            os.mkdir(hmm_dir)

    # HCompV -A -D -T 1 -C {config} -f 0.01 -m -S {mfcc_list.scp} -M {output_dir} {proto}
    cmd = "HCompV -A -D -T 1 -C %s -f 0.01 -m -S %s -M %s %s"
    args = (HMM_CONF_FILE, MFCC_LIST_FILE, output_dir, HMM_PROTO_FILE)
    utils.run(cmd % args)

    generated_proto = HMM_OUTPUT_DIR + "hmm0/" + "proto"
    with open(generated_proto, 'r') as fin:
        proto_data = list(fin)
    proto_top = ''.join(proto_data[:3])
    proto_bottom = ''.join(proto_data[4:])

    template = "~h \"%s\"\n" + proto_bottom
    gen_hmmdefs(output_dir, template)
    gen_macros(output_dir, proto_top)

def add_sil_to_monophones():
    if 'sil' not in open(MONOPHONE0_FILE).read():
        with open(MONOPHONE0_FILE, 'a') as fout:
            fout.write('sil\n')

def gen_hmmdefs(path, template):
    add_sil_to_monophones()

    print(template)
    with open(MONOPHONE0_FILE, 'r') as fin:
        phones = [line.strip('\n') for line in fin]

    hmmdefs_file = path + '/hmmdefs'
    with open(hmmdefs_file, 'w') as fout:
        for phone in phones:
            fout.write(template % (phone))

def gen_macros(path, proto_top):
    generated_vfloors = path + "/vFloors"
    with open(generated_vfloors, 'r') as fin:
        vfloors_data = fin.read()

    macros_file = path + "/macros"
    with open(macros_file, 'w') as fout:
        fout.write(proto_top)
        fout.write(vfloors_data)

def prepare_silence_model():
    # copy the content of hmm3 to hmm4
    files = os.listdir(HMM_OUTPUT_DIR + 'hmm3')
    for file in files:
        copyfile(HMM_OUTPUT_DIR + 'hmm3/' + file, HMM_OUTPUT_DIR + 'hmm4/' + file)

    # sp model
    sp_model = []
    with open(HMM_OUTPUT_DIR + 'hmm4/hmmdefs','r') as infile:
        for i, line in enumerate(infile):
            if("sil" in line):
                line_sil = i

    with open(HMM_OUTPUT_DIR + 'hmm4/hmmdefs','r') as infile:
        for i, line in enumerate(infile):
            if(i >= line_sil and i <= line_sil + 14):
                sp_model.append(line)

    sp_model = sp_model[:3] + sp_model[9:]
    sp_model[0] = sp_model[0].replace('sil', 'sp')
    sp_model[2] = sp_model[2].replace('5','3')
    sp_model[3] = sp_model[3].replace('3', '2')

    sp_model.append('<TRANSP> 3\n')
    sp_model.append('0.0 1.0 0.0\n')
    sp_model.append('0.0 0.9 0.1\n')
    sp_model.append('0.0 0.0 0.0\n')
    sp_model.append('<ENDHMM>\n')

    with open(HMM_OUTPUT_DIR + 'hmm4/hmmdefs', 'a+') as fout:
        for item in sp_model:
            fout.write(item)

def prepare_realigning_data():
    # HVite -A -D -T 1 -l * -o SWT -b SENT-END -C config -H hmm7/macros -H hmm7/hmmdefs -i aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I words.mlf -S train.scp dict monophones1> HVite_log
    cmd = "HVite -A -D -T 1 -l * -o SWT -b SENT-END -C %s -H hmm_result/hmm7/macros -H hmm_result/hmm7/hmmdefs -i %s -m -t 250.0 150.0 1000.0 -y lab -a -I %s -S %s %s %s> %s"
    args = (HMM_CONF_FILE, ALIGNED_MLF_FILE, WORDS_MLF_FILE, MFCC_LIST_FILE, HTK_DICT_FILE, MONOPHONE1_FILE, HVITE_LOG)
    utils.run(cmd % args)

def run_hmm(n_epoch):
    # make all directory for HMM
    for i in range (10):
        hmm_dir = HMM_OUTPUT_DIR + 'hmm' + str(i)
        if not os.path.exists(hmm_dir):
            os.mkdir(hmm_dir)

    for epoch in range(3):
        # HERest -A -D -T 1 -C {hmm.conf} -I {phones.mlf} -t 250.0 150.0 1000.0 -S {mfcc_list.scp} -H {hmm/macros} -H {hmm/hmmdefs} -M {hmm_result/hmm} {monophones}
        cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 1000.0 -S %s -H hmm_result/hmm%d/macros -H hmm_result/hmm%d/hmmdefs -M hmm_result/hmm%d %s"
        args = (HMM_CONF_FILE, PHONES0_MLF_FILE, MFCC_LIST_FILE, epoch, epoch, epoch+1, MONOPHONE0_FILE)
        utils.run(cmd % args)

    prepare_silence_model()
    for i in range(4, 7):
        if(i == 4):
            # HHEd -A -D -T 1 -H hmm4/macros -H hmm4/hmmdefs -M hmm5 sil.hed monophones1
            cmd = "HHEd -A -D -T 1 -H hmm_result/hmm%d/macros -H hmm_result/hmm%d/hmmdefs -M hmm_result/hmm%d %s %s"
            args = (i, i, i+1, SILENCE_CONF_FILE, MONOPHONE1_FILE)
            utils.run(cmd % args)
        else:
            # HERest -A -D -T 1 -C config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm5/macros -H  hmm5/hmmdefs -M hmm6 monophones1
            cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 3000.0 -S %s -H hmm_result/hmm%d/macros -H hmm_result/hmm%d/hmmdefs -M hmm_result/hmm%d %s"
            args = (HMM_CONF_FILE, PHONES1_MLF_FILE, MFCC_LIST_FILE, i, i, i+1, MONOPHONE1_FILE)
            utils.run(cmd % args)

    prepare_realigning_data()
    for i in range(7, 9):
        #HERest -A -D -T 1 -C config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm7/macros -H hmm7/hmmdefs -M hmm8 monophones1 
        cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 3000.0 -S %s -H hmm_result/hmm%d/macros -H hmm_result/hmm%d/hmmdefs -M hmm_result/hmm%d %s"
        args = (HMM_CONF_FILE, ALIGNED_MLF_FILE, MFCC_LIST_FILE, i, i, i+1, MONOPHONE1_FILE)
        utils.run(cmd % args)