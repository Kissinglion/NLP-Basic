import io
import os

import MeCab
import re
mecab_tagger= MeCab.Tagger()

def mecablist(inputs):
    r=[ (x.split('\t')[0],x.split('\t')[1].split(',')[0]) for x in inputs.split('\n')[:-2] ]
    return r
def mecabsplit(inputs, pos):
    r=[]
    inputs = mecab_tagger.parse(inputs)
    t = inputs.split('\n')[:-2]
    for i in t:
        field = i.split('\t')
        if field[1].split(',')[-1] is not '*':
            r.extend( [ (x.split('/')[0],x.split('/')[1]) for x in field[1].split(',')[-1].split('+') ] )
        else:
            r.append( (field[0],field[1].split(',')[0]) )
    if pos:
        return r
    else:
        return [ x[0] for x in r ]
    return r


class pattern_var():
    def __init__(self):
        #의도
        self.intent=''
        #패턴
        self.pat=[]
        
    def addpattern(self, pat,intent):
        self.pat = pat
        self.intent=intent
        #self.varpoint.append(varpoint)


class sentence_matching():
    def __init__(self,pattern_file):
        intent = ''
        self.pattern=[]
        for i,line in enumerate(open(pattern_file,'r',encoding='utf-8')):
            line=line.strip()
            if line == '':
                intent=''
                continue
            if intent == '':
                intent=line
            else:
                item = line.split('\t')
                t=pattern_var()
                t.addpattern(item[0].split(' '),intent)
                
                self.pattern.append(t)


    def input_sent(self,sentence):
        self.sentence= mecabsplit(sentence,False)
        self.sentence_pos = mecabsplit(sentence ,True)
        self.sentence_intent={}
        print ('형태소 분석 결과' + str(self.sentence_pos))
    def matches(self):

        sent,sent_pos,intent = self.matching_varpat(self.pattern)

        return sent,sent_pos,intent

    def matching_varpat(self,pat):

        for pattern_it in pat:
            result = self.matching(pattern_it.pat,self.sentence_pos)

            if result is not None:
                temp={}
                temp['intent']=pattern_it.intent
                self.sentence_intent= temp
                print(pattern_it.pat)
                break
        return self.sentence,self.sentence_pos, self.sentence_intent


    def get_next_pattern_token(self,pat):
        t = next(pat, None)
        if t == None:
            return None, None
        t1 = t.split('/')
        return t1[0], t1[1]

        t = next(pat, None)
        return t

    def matching(self,pattern, input_text):
        result = []
        pattern_iter = iter(pattern)
        txt,pos = self.get_next_pattern_token(pattern_iter)
        matched_first = False

        for tok in input_text:
            # 패턴토큰이 끝까지 갔다면 종료
            if txt == None:
                break
            # 패턴이 매칭되면 결과에 추가
            if re.findall(txt, tok[0]) != [] and tok[1] == pos:
                result.append(tok[0])
                txt,pos = self.get_next_pattern_token(pattern_iter)

        # 패턴이 끝까지 매칭된경우 종료
        # 끝까지 매칭되지 않았으면 다음패턴
        if txt == None:
            return result
        return None


