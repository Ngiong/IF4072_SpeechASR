#!/usr/bin/python3
from scripts import prepare_mfcc as mfcc, prepare_mlf as mlf, process_hmm as hmm, process_triphones as triphones

if __name__ == '__main__':
    # mfcc.gen_scp()
    # mfcc.gen_mfcc()
    # mlf.create_wlist()
    # mlf.create_htk_dict()
    # mlf.create_mlf_word()
    # mlf.create_mlf_phone()

    # generate files for hmm0
    # hmm.prepare_hmm()

    # run hmm for n epoch
    # hmm.run_hmm(7)
    
    # make triphones
    triphones.execute_triphones()