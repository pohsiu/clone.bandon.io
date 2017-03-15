import numpy as np
import jieba
import sys
import os
from word2vec import Word2Vec, Sent2Vec, LineSentence
reload(sys)
sys.setdefaultencoding('utf-8')
sent_file = 'output'

with open('haha.sentvec', 'r') as myfile:
    data=myfile.readlines()
with open('haha', 'r') as myfile:
    sentence = myfile.readlines()
for i in sentence:
    i = i.replace(' ', "").replace('\n', "")

sent_bank = []
for i in range(len(data)):
    sent_bank.append(np.array(data[i].replace('\n','').split(' ')[1:], dtype=np.float32))

while True:
    input = raw_input("\nUser: ")
    seg = jieba.cut(input, cut_all=True)
    seg2 = " ".join(seg)
    output = open("output",'w')
    output.write(seg2.encode('utf8'))
    output.close()
    model = Sent2Vec(LineSentence(sent_file), model_file='data_seg' + '.model')
    model.save_sent2vec_format(sent_file + '.sentvec')
   
    
    with open('output.sentvec', 'r') as myfile:
        mysent = myfile.read().replace('\n', "")
    myfile.close()
    mysent_vec = np.array(mysent.split(' ')[2:], dtype=np.float32)
    if mysent_vec.shape[0] == 0:
        print "Your inputs are invalid, please try again."
        continue
    
    max = 0
    answer_sent = ""
    print answer_sent
    
    for i in range(len(sent_bank)):
        score = np.dot(mysent_vec,sent_bank[i])/(np.linalg.norm(mysent_vec)*np.linalg.norm(sent_bank[i]))
        if score >= max and input != sentence[i].replace(' ', "").replace('\n' ,""):
            max = score
            answer_sent = sentence[i]
    
    print "\033[1;33mReply: ", answer_sent.replace(' ', "").replace('\n' ,""), "\033[m"
    os.remove('output')
    os.remove('output.sentvec')
