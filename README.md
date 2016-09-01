# Bleu-Machine-Translation-Score

Source: http://ron.artstein.org/csci544-2016/homework-8/homework-8.html

calculatebleu.py: Python program takes two paths as parameters: the first parameter is the path to the candidate translation (a single file), and the second parameter is the path to the reference translations (either a single file, or a directory if there are multiple reference translations). The program writes an output file called bleu_out.txt which contains a single floating point number, representing the BLEU score of the candidate translation relative to the set of reference translations.

> python calculatebleu.py /path/to/candidate /path/to/reference

Tested program by running it on the following candidate and translation files, and comparing the result to the true BLEU score.

Language	    Candidate	      Reference	            BLEU score
German	    candidate-1.txt	  reference-1.txt	    0.151184476557
Greek	      candidate-2.txt	  reference-2.txt	    0.0976570839819
Portuguese	candidate-3.txt	  reference-3.txt	    0.227803041867
English	    candidate-4.txt	  reference-4a.txt    0.227894952018
                              reference-4b.txt    
The German, Greek and Portuguese reference translations above are excerpted from the common test set of the EUROPARL corpus; the candidate translations were obtained by taking the corresponding English sentences and running them through Google Translate. The English reference translations are from two alternative translations of the Passover Hagaddah; the candidate translation was obtained by running the original Hebrew text through Google translate.

Notes

The candidate and reference files will be in UTF-8 encoding.
You may assume a line-by-line correspondence of sentences between the candidate and reference translations.
