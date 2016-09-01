from sys import argv
from collections import Counter
import copy
import glob
import os
import math

def generate_ngram(content, n):
    content = content.split()
    ngrams = []
    for i in range(len(content) - n + 1):
        ngrams.append(content[i:i + n])
    return [' '.join(x) for x in ngrams]


def populateDict(ref_path,n):
    #returns a list which contains num_ref_files dictionaries having count for specified 'n'-gram
    dictlist=[]
    
    if not os.path.isdir(ref_path):
        dictionary = {}
        # print 'inside if'
        # raw_input()
        content = open(ref_path, 'r').read().strip('\r\n')
        content_by_line = content.split('\n')
        for index, line in enumerate(content_by_line):
            # call generate_ngram
            dictionary[index] = Counter(generate_ngram(line, n))
        dictlist.append(dictionary)
        return dictlist
    
    for name in glob.glob(ref_path+'/*.txt'):
        dictionary = {}
        content=open(name,'r').read()
        content_by_line=content.split('\n')
        for index,line in enumerate(content_by_line):
            # call generate_ngram
            dictionary[index]=Counter(generate_ngram(line.strip(),n))
        dictlist.append(dictionary)
    
    return dictlist


def main():
    # script,candidate_path,ref_path=argv
    candidate_path='candidate-3.txt'
    ref_path='reference-3.txt'  #'reference-3.txt'
    candidate_file=open(candidate_path,'r')
    candidate_content=candidate_file.read().strip('\r\n')
    candidate_list_of_lines=candidate_content.split('\n')
    count=0
    
    for line in candidate_list_of_lines:
        count+= sum(Counter(line.strip().split()).values())
    
    c=count
    
    # best match length
    r=0 
    
    #generating unigrams, bi-grams, tri-grams, 4-grams
    n=4
    wn=float(1/4)
    
    # need to calc r,c from unigram data use if i==1
    clipped_counts_by_line={}
    candidate_dict={}
    total_ngram_count_by_line={}
    total_ngrams={}
    clipped_ngrams={}
    modified_precision={}
    best_match_lengths=0
    
    for i in range(n):
        print 'ngram no n=',i+1
        dictlist = populateDict(ref_path,i+1)
        candidate_dict[i] = {} 
        clipped_counts_by_line[i] = {}
        total_ngram_count_by_line[i] = {}
        total_ngrams[i] = {}
        clipped_ngrams[i] = {}
        
        for index,line in enumerate(candidate_list_of_lines):
            candidate_dict[i][index] = {}
            candidate_dict[i][index] = Counter(generate_ngram(line,i+1))
        
        if i == 0:
            candidate_unigram_count_by_line=candidate_dict[0]
            print candidate_unigram_count_by_line
            
            for line_number in range(len(candidate_unigram_count_by_line)):
                candidate_line_count = sum(candidate_unigram_count_by_line[line_number].values())
                print line_number,' candidate line count: ',candidate_line_count
                ref={}
                
                for dict_num in range(len(dictlist)):
                    ref[dict_num] = {}
                    diction = dictlist[dict_num]
                    ref_line_count = sum(diction[line_number].values())
                    print ' ref:',ref_line_count
                    ref[dict_num] = ref_line_count
                minimum = min(ref.itervalues())
                best_match_lengths += minimum

        #combine all reference dictionaries into one
        combined_ref_dict = {}
        
        for line_num in range(len(candidate_dict[i])):
            temp_dict = {}
            clipped_counts_by_line[i][line_num] = 0
            total_ngram_count_by_line[i][line_num] = 0
            num_dict = len(dictlist)
            max_count = 0
            
            for k2,v2 in candidate_dict[i][line_num].iteritems():
                total_ngram_count_by_line[i][line_num] += v2
            total_ngrams[i] = sum(total_ngram_count_by_line[i].values())
            
            for dict_num in range(num_dict):
                line = dictlist[dict_num][line_num]
                
                for k,v in line.iteritems():
                    
                    if k not in temp_dict:
                        temp_dict[k] = v
                    else:
                        if v>temp_dict[k]:
                            temp_dict[k] = v
            combined_ref_dict[line_num] = temp_dict
            
            for k1,v1 in candidate_dict[i][line_num].iteritems():
                if k1 in combined_ref_dict[line_num]:
                    if v1>=combined_ref_dict[line_num][k1]:
                        clipped_counts_by_line[i][line_num] += combined_ref_dict[line_num][k1] #i is unigram number
                    elif v1<combined_ref_dict[line_num][k1]:
                        clipped_counts_by_line[i][line_num] += v1
            clipped_ngrams[i] = sum(clipped_counts_by_line[i].values())
    
    for k3 in clipped_ngrams:
        if clipped_ngrams[k3] == 0 or total_ngrams[k3]==0:
            modified_precision[k3] = 0
        else:
            modified_precision[k3] = math.log(float(clipped_ngrams[k3])/total_ngrams[k3])
    
    #brevity penalty
    BP = 0
    r = best_match_lengths
    print r,',',c
    if r<c:
        BP = 1
    else:
        BP = math.exp(1-(float(r)/c))

    output = open('bleu_out.txt','r+')
    BLEU = BP*(math.exp(sum(modified_precision.values())*0.25))
    output.write(str(BLEU))

if __name__ == '__main__':
    main()
