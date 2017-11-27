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
	cmd = "HERest -A -D -T 1 -C %s -I %s -t 250.0 150.0 3000.0 -s %s -S %s -H hmm_result/hmm11/macros -H hmm_result/hmm11/hmmdefs -M hmm_result/hmm12 %s "
	args = (HMM_CONF_FILE, WINTRI_MLF_FILE, STAT_FILE, MFCC_LIST_FILE, TRIPHONE1_FILE)
	utils.run(cmd % args)

def create_maketriphonesded():
	with open(MAKETRIPHONESDED_FILE, 'w') as outfile:
		outfile.write("AS sp\nMP sil sil sp\nTC   ")

def create_fulllist():
	create_maketriphonesded()
	# HDMan -A -D -T 1 -b sp -n fulllist0 -g maketriphones.ded -l flog dict-tri ../lexicon/VoxForgeDict.txt
	cmd = "HDMan -A -D -T 1 -b sp -n %s -g %s -l flog %s %s"
	args = (FULLLIST0_FILE, MAKETRIPHONESDED_FILE, DICT_TRI_FILE, MY_DICT_FILE)
	utils.run(cmd % args)

	# using julia
	# julia ../bin/fixfulllist.jl fulllist0 monophones0 fulllist
	cmd = "julia scripts/julia/fixfulllist.jl %s %s %s"
	args = (FULLLIST0_FILE, MONOPHONE0_FILE, FULLLIST_FILE)
	utils.run(cmd % args)

def create_treeHED():
	fout = open(TREE_HED_FILE, 'w')
	with open('scripts/files/triphones/tree1.hed') as infile:
		for line in infile:
			fout.write(line)
	fout.close()

	# using julia
	# julia ../bin/mkclscript.jl monophones0 tree.hed
	cmd = "julia scripts/julia/mkclscript.jl %s %s"
	args = (MONOPHONE0_FILE, TREE_HED_FILE)
	utils.run(cmd % args)

def train_hmm13_hmm15():
	for i in range (13, 16):
		hmm_dir = HMM_OUTPUT_DIR + 'hmm' + str(i)
		if not os.path.exists(hmm_dir):
			os.mkdir(hmm_dir)

	# HMM 13
	# HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1
	cmd = "HHEd -A -D -T 1 -H hmm_result/hmm12/macros -H hmm_result/hmm12/hmmdefs -M hmm_result/hmm13 %s %s"
	args = (TREE_HED_FILE, TRIPHONE1_FILE)
	utils.run(cmd % args)

	#TODO: masih error ini
	'''#HMM 14
	# HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist
	cmd = "HERest -A -D -T 1 -T 1 -C %s -I %s  -t 250.0 150.0 3000.0 -S %s -H hmm_result/hmm13/macros -H hmm_result/hmm13/hmmdefs -M hmm_result/hmm14 tiedlist"
	args = (HMM_CONF_FILE, WINTRI_MLF_FILE, MFCC_LIST_FILE)
	utils.run(cmd % args)

	#HMM 15
	# HERest -A -D -T 1 -T 1 -C config -I wintri.mlf  -t 250.0 150.0 3000.0 -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist
	cmd = "HERest -A -D -T 1 -T 1 -C %s -I %s  -t 250.0 150.0 3000.0 -S %s -H hmm_result/hmm14/macros -H hmm_result/hmm14/hmmdefs -M hmm_result/hmm15 tiedlist"
	args = (HMM_CONF_FILE, WINTRI_MLF_FILE, MFCC_LIST_FILE)
	utils.run(cmd % args)'''

def execute_triphones():
	#make_triphone1()
	#make_mktriHED()
	#train_hmm10_hmm12()
	create_fulllist()
	create_treeHED()
	#train_hmm13_hmm15()
