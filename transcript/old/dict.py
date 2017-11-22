from collections import OrderedDict

file = open('wlist', 'r')

def word2phonem(s):
	return '-'.join(list(trans))


word_dict = OrderedDict()

for line in file:
	xline = line.rstrip()
	split_line = xline.split('\t')
	# text = split_line[0]
	# transcript = split_line[1]

	split_text = list(filter(None, split_line[0].split(' ')))
	split_trans = list(filter(None, split_line[1].split(' ')))

	# print (line)
	# print (len(split_text), len(split_trans))

	for idx, word in enumerate(split_text):
		trans = split_trans[idx]
		if '-' not in trans:
			trans = word2phonem(trans)

		# if word in word_dict.keys():
		# 	if word_dict[word] != trans:
		# 		print ('[CONFLICT]', word, ' -> ', 'before: ', word_dict[word], '; new: ', trans)
		# 		input("Press Enter to continue...")
		# else:
		word_dict[word] = trans


		# print('[', word, ', ', split_trans[idx], ']')

for key, value in word_dict.items():
	print(key, '\t\t', value.replace('-', ' '))