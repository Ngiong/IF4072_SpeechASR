import os
import scripts.utils as utils
from scripts.consts import *

def gen_scp():
	data_directory = ['set_1', 'set_2', 'set_3', 'set_4', 'set_5']
	files = os.listdir('./Dataset/')
	f = open(SCP_FILE, 'w')
	if not os.path.exists('./Dataset_MFCC/'):
		os.mkdir('./Dataset_MFCC/')
	for file in files:
		if file in data_directory:
			if not os.path.exists('./Dataset_MFCC/' + file + '/'):
				os.mkdir('./Dataset_MFCC/' + file + '/')
			print('Entering ', file)
			subfiles = os.listdir('./Dataset/' + file)
			for subfile in subfiles :
				if not os.path.exists('./Dataset_MFCC/' + file + '/' + subfile):
					os.mkdir('./Dataset_MFCC/' + file + '/' + subfile)
				subsubfiles = os.listdir('./Dataset/' + file + '/' + subfile)
				for subsubfile in subsubfiles:
					# rename the mfcc file
					subsubfile_temp = subsubfile.replace(".wav", ".mfc")
					filename = subsubfile_temp[-8:]
					num = ord(filename[0]) - 64
					filename = filename.replace(filename[0], str(num)+'_')
					print('Processing %s into %s' % (subsubfile, filename))

					result_range = './Dataset_MFCC' + '/' + file + '/' + subfile + '/' + filename
					result_domain = './Dataset/' + file + '/' + subfile + '/' + subsubfile + ' ' + result_range
					f.write(result_domain + '\n')
	f.close()

def gen_mfcc():
	# HCopy -A -D -T 1 -C <wav_config_file> -S <wav_config_file>
	cmd = "HCopy -A -D -T 1 -C %s -S %s "
	args = (WAV_CONF, SCP_FILE)
	utils.run(cmd % args)
