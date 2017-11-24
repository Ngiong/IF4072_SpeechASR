import scripts.utils as utils
from scripts.consts import *

def create_wlist():
    # perl prompts2wlist {prompts.tsv} {wordlist}
    cmd = "perl scripts/perl/prompts2wlist %s %s"
    args = (PROMPTS_FILE, WORDLIST_FILE)
    utils.run(cmd % args)

def create_htk_dict():
    # HDMan -m -g {global.ded} -w {wlist} -n {monophones1} -i -l {dlog} {output_dict} {selfmade-dict.txt}
    cmd = "HDMan -m -g %s -w %s -n %s -i -l %s %s %s"
    args = (GLOBALDED_FILE, WORDLIST_FILE, MONOPHONE_FILE, DLOG_FILE, HTK_DICT_FILE, MY_DICT_FILE)
    utils.run(cmd % args)

def create_mlf_word():
    # perl scripts/prompts2mlf {word-level.mlf} prompts.tsv
    cmd = "perl scripts/perl/prompts2mlf %s %s"
    args = (WORDS_MLF_FILE, PROMPTS_FILE)
    utils.run(cmd % args)

def create_mlf_phone():
    # HLEd -A -D -T 1 -l '*' -d {dict} -i {phones.mlf} {mkphones0.led} {word-level.mlf}
    cmd = "HLEd -A -D -T 1 -l '*' -d %s -i %s %s %s"
    args = (HTK_DICT_FILE, PHONES_MLF_FILE, MKPHONES_FILE, WORDS_MLF_FILE)
    utils.run(cmd % args)
