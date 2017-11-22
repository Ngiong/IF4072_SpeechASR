import os

data_directory = ['set_1', 'set_2', 'set_3', 'set_4', 'set_5']
files = os.listdir('./Dataset/')
f = open('codetrain_gen.scp', 'w')

os.mkdir('./Dataset_MFCC/')
for file in files:
	if file in data_directory:
		os.mkdir('./Dataset_MFCC/' + file + '/')
		print 'Entering ', file
		subfiles = os.listdir('./Dataset/' + file)
		for subfile in subfiles :
			os.mkdir('./Dataset_MFCC/' + file + '/' + subfile)
			subsubfiles = os.listdir('./Dataset/' + file + '/' + subfile)
			for subsubfile in subsubfiles:
				subsubfile_temp = subsubfile.replace(".wav", ".mfc")
				result_range = './Dataset_MFCC' + '/' + file + '/' + subfile + '/' + subsubfile_temp
				result_domain = './Dataset/' + file + '/' + subfile + '/' + subsubfile + ' ' + result_range
				f.write(result_domain + '\n')
f.close()