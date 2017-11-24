import os
import scripts.utils as utils
from scripts.consts import *

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

# NOTE: ini cuma run HMM0 - HMM3 karena HMM4 udah pakai monophones1 dan ada konfigurasi sendiri lagi
def run_hmm(n_epoch):
    for epoch in range(1, n_epoch + 1):
        # HERest -A -D -T 1 -C {hmm.conf} -I {phones.mlf} -t 250.0 150.0 1000.0 -S {mfcc_list.scp} -H {hmm/macros} -H {hmm/hmmdefs} -M {hmm_result/hmm} {monophones}
        cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 1000.0 -S %s -H hmm_result/hmm%d/macros -H hmm_result/hmm%d/hmmdefs -M hmm_result/hmm%d %s"
        args = (HMM_CONF_FILE, PHONES_MLF_FILE, MFCC_LIST_FILE, epoch-1, epoch-1, epoch, MONOPHONE0_FILE)
        utils.run(cmd % args)
