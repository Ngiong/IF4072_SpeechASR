from collections import OrderedDict

file = open('combined.tsv', 'r')

def word2phonem(s):
	x = s.replace('-', '')
	return ' '.join(list(x))


word_dict = OrderedDict()

for line in file:
	xline = line.rstrip()
	split_line = xline.split('\t')
	# text = split_line[0]
	# transcript = split_line[1]

	split_text = list(filter(None, split_line[1].split(' ')))
	split_trans = list(filter(None, split_line[2].split(' ')))

	# print (line)
	# print (len(split_text), len(split_trans))
	
	if len(split_text) != len(split_trans):
		input("Press Enter to continue...")


	for idx, word in enumerate(split_text):
		trans = split_trans[idx]
		word_dict[word] = word2phonem(trans)

for key, value in sorted(word_dict.items()):
	print(key, ' ', value)