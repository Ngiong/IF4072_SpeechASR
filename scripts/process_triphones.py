import os
import scripts.utils as utils
from scripts.consts import *

def make_triphone1():
	# creating mktri.led cofiguration file
	with open(MKTRI_FILE, 'w') as outfile:
		outfile.write("WB sp\n")
		outfile.write("WB sil\n")
		outfile.write("TC    ")

	# HLEd -n triphones1 -l '*' -i wintri.mlf mktri.led aligned.mlf
	cmd = "HLEd -A -D -T 1 -n %s -l * -i %s %s %s"
	args = (TRIPHONE1_FILE, WINTRI_MLF_FILE, MKTRI_FILE, ALIGNED_MLF_FILE)
	utils.run(cmd % args)

def make_mktriHED():
	cmd = "perl scripts/perl/maketrihed %s %s"
	args = (MONOPHONE1_FILE, TRIPHONE1_FILE)
	utils.run(cmd % args)

def train_hmm10_hmm12():
	for i in range (10, 13):
		hmm_dir = HMM_OUTPUT_DIR + 'hmm' + str(i)
		if not os.path.exists(hmm_dir):
			os.mkdir(hmm_dir)

	# HMM10
	# HHEd -A -D -T 1 -H hmm9/macros -H hmm9/hmmdefs -M hmm10 mktri.hed monophones1 
	cmd = "HHEd -A -D -T 1 -H hmm_result/hmm9/macros -H hmm_result/hmm9/hmmdefs -M hmm_result/hmm10 %s %s"
	args = (MKTRI_HED_FILE, MONOPHONE1_FILE)
	utils.run(cmd % args)

	# HMM11
	# HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm10/macros -H hmm10/hmmdefs -M hmm11 triphones1
	cmd = "HERest  -A -D -T 1 -C %s -I %s -t 250.0 150.0 3000.0 -S %s -H hmm_result/hmm10/macros -H hmm_result/hmm10/hmmdefs -M hmm_result/hmm11 %s"
	args = (HMM_CONF_FILE, WINTRI_MLF_FILE, MFCC_LIST_FILE, TRIPHONE1_FILE)
	utils.run(cmd % args)

	# HMM12
	# HERest  -A -D -T 1 -C config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm11/macros -H hmm11/hmmdefs -M hmm12 triphones1 
	cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 3000.0 -s hmm_result/hmm12/stats -S %s -H hmm_result/hmm11/macros -H hmm_result/hmm11/hmmdefs -M hmm_result/hmm12 %s "
	args = (HMM_CONF_FILE, WINTRI_MLF_FILE, MFCC_LIST_FILE, TRIPHONE1_FILE)
	utils.run(cmd % args)

def execute_triphones():
	make_triphone1()
	make_mktriHED()
	train_hmm10_hmm12()