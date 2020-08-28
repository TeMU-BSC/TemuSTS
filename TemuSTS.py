#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:40:44 2020

@author: crodri

Version 2.0

"""
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import spacy
modelo="es_core_news_md"
import wmd
nlp = spacy.load(modelo)#
import os,sys,pickle,numpy, time
from rapidfuzz import process



from optparse import OptionParser
def generateSentences(dirin):
    if dirin[-1] != os.path.sep:
        dirin = dirin+os.path.sep
    filesin = os.listdir(dirin)
    parrafos = {}
    all_sents = 0
    all_toks = 0
    doc_number = len(filesin)
    from collections import OrderedDict
    for x in filesin:
        print(dirin+x)
        txt = open(dirin+x).read().strip()
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        y = nlp(txt)
        number_sentences = len([x for x in y.sents])
        number_toks = len([x for x in y])
        all_sents  = all_sents + number_sentences
        all_toks  = all_toks + number_toks
        statsdoc = (doc_number,all_sents,all_toks)
        w = 0
        for s in y.sents:
            parrafos[x+"_"+str(number_sentences)+"-"+str(w)] = s.text#s.lower_#" ".join([z.lower_ for z in s])
            w += 1
    return parrafos, statsdoc

def generateSourceSentences(dirin):
    if dirin[-1] != os.path.sep:
        dirin = dirin+os.path.sep
    filesin = os.listdir(dirin)
    parrafos = {}
    all_sents = 0
    all_toks = 0
    doc_number = len(filesin)
    #from collections import OrderedDict
    for x in filesin:
        print(dirin+x)
        txt = open(dirin+x).read().strip()
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        txt = txt.replace("\n\n", "\n")
        y = nlp(txt)
        number_sentences = len([x for x in y.sents])
        number_toks = len([x for x in y])
        all_sents  = all_sents + number_sentences
        all_toks  = all_toks + number_toks
        statsdoc = (doc_number,all_sents,all_toks)
        w = 0
        for s in y.sents:
            parrafos[s.text] =  x+"_"+str(number_sentences)+"-"+str(w)#s.lower_#" ".join([z.lower_ for z in s])
            w += 1
    return parrafos, statsdoc


#Jaccard similarity
def get_jaccard_sim(str1, str2): 
    a = set(str1.lower().split()) 
    b = set(str2.lower().split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))



def fuzzy(allterms,sentence,cutoff=93):
    highest = process.extractOne(sentence,allterms,processor=None, score_cutoff=cutoff)
    if highest:
        return highest
    else:
        return None

def similitud(parrafos,sentence):
    #from operator import itemgetter
    sim = {}
    for k in parrafos.keys():
        source = parrafos[k]
        s = get_jaccard_sim(source,sentence)
        if s == 0.0:
            pass
        else:
            sim[k] = s
    sortedic = sorted(sim.items(), key=lambda x: x[1],reverse=True)
    try:
        return sortedic[0]
    except IndexError:
        return None


def compareAndWrite(parrafos1,parrafos2,umbral,method,redact=None):
    similares = []
    allterms = [x for x in parrafos1.keys()] 
    for eachone in parrafos2.keys():
        sentence = parrafos2[eachone]
        if method == 'fuzzy':
            top = fuzzy(allterms,sentence,93)
        elif method == 'jaccard':
            top = similitud(parrafos1,sentence)
        if top:
            if top[-1] > umbral:
                if redact:
                    similares.append([top[0],parrafos1[top[0]],top[-1],"--XXXXXXX--",eachone])
                    #similares.append([eachone,sentence,top[-1],"--XXXXXXX--",top[0]])
                else:
                    similares.append([top[0],parrafos1[top[0]],top[-1],sentence,eachone])
    return similares

    
def writeOut(targetdir,similares,statstarget,method,fileout):
    import csv
    fo= open(fileout,"w")
    w = csv.writer(fo, dialect="excel", delimiter="\t")
    w.writerow(["Target directory:"+targetdir,' # of Documents'+ str(statstarget[0]),"<=====>", '# of sentences '+str(statstarget[1]), '# of tokens '+str(statstarget[-1]),'Method:'+method])
    w.writerow(['source_id', 'source_sentence', "score", 'target_sentence', 'target_id','method'])
    w.writerows(similares)
    fo.close()

def main(argv=None):
    parser = OptionParser()
    parser.add_option("-s", "--source", dest="source",
                    help="source directory")
    parser.add_option("-o", "--fileout", dest="fileout", help="output file, tab-separated values extension (.tsv)",default="compared.tsv")
    parser.add_option("-m", "--method", dest="method", help="Comparison method (jaccard, fuzzy [default]) Fuzzy is way faster",default="fuzzy")
    parser.add_option("-t", "--target", dest="target", help="target directory")
    parser.add_option("-u", "--umbral", dest="umbral", help="similarity threshold (default 93, for jaccard use 0.3 or higher)",type="float", default=93)
    parser.add_option("-r", "--redact", dest="redact", help="do not write target sentences", default=None)
    (options, args) = parser.parse_args(argv)
    
    import time
    t1 = time.time()
    #print("*",type(options.cluster_num))
    if options.source:
        if options.method == 'fuzzy':
            parrafos1, statssource = generateSourceSentences(options.source)
        else:
            parrafos1, statssource = generateSentences(options.source)
        parrafos2, statstarget = generateSentences(options.target)
        print("Initiating Comparison ...")
        if options.redact:
            similares = compareAndWrite(parrafos1,parrafos2,options.umbral,options.method,options.redact)
        else:
            similares = compareAndWrite(parrafos1,parrafos2,options.umbral,options.method)
        if options.fileout:
            writeOut(options.target,similares,statstarget,options.method,options.fileout)
        else:
            writeOut(options.target,similares,statstarget,options.method,"compared.tsv")
    else:
        print("Initiating Comparison ...")
        if not options.target:
            print("Need arguments. use python similituds_cc.py --help")
        else:
            print("No Source Directory ... Comparing against a reference corpus")
            parrafos1 = pickle.load(open("corpus.bin","rb"))
            parrafos2,statstarget = generateSentences(options.target)
            if options.redact:
                similares = compareAndWrite(parrafos1,parrafos2,options.umbral,options.method,options.redact)
            else:
                similares = compareAndWrite(parrafos1,parrafos2,options.umbral,options.method)
            if options.fileout:
                writeOut(options.target,similares,statstarget,options.method,options.fileout)
            else:
                writeOut(options.target,similares,statstarget,options.method,"compared.tsv")
    t2 = time.time()
    print("processed  in "+str((t2-t1))+" seconds "+str((t2-t1)/60)+" minutes or "+str(((t2-t1)/60)/60)+" hours using "+options.method)

if __name__ == "__main__":
  sys.exit(main())