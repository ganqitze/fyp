from collections import Counter

token_file = "C://Users/User/Desktop/fyp/English/process/lda2vec/tokens/topic_20.txt"
new_file = "C://Users/User/Desktop/New folder/opdr_lda2vec_20.txt"


with open(token_file) as f:
    c = Counter(x.strip() for x in f)

print c


for x in c:
    if c[x] > 100:
    	c[x] = int(c[x]*0.01)


tokens = ''
for x in c:
	for i in range(0, c[x]):
		tokens += x + ' '

print c
with open(new_file, "wb") as f:
    f.write(tokens)

# print tokens