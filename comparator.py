import itertools
import os
import subprocess
import operator
import time
import substr


def getSum(score):
    sum = { 'length': 0, 'src1_lineNum': 0, 'src2_lineNum': 0 }
    if score == []:
        return {}
    else:
        for i in range(len(score)):
            sum['length'] += score[i]['length']
            sum['src1_lineNum'] += (score[i]['src1_lineEnd'] - score[i]['src1_lineStart'])
            sum['src2_lineNum'] += (score[i]['src2_lineEnd'] - score[i]['src2_lineStart'])
        return sum


'''
<< getResult >>

src1 : path of src1
src2 : path of src2
tokenizerOption : exact or rough, dafault is exact.
criterion : number of criterion whether it is code clone or not. default is 20.
'''
def getResult(src1, src2, lang='C/C++', tokenizerOption='exact', criterion=20):      
    start_time = time.time() 
    src1_list = []
    src2_list = []
    src1_totalLineNumber = 0
    src2_totalLineNumber = 0
    src1_tokens = {}
    src2_tokens = {}
    src1_result = {}
    src2_result = {}
    result = {}
    tokenizer = ''

    ### determine tokenizer
    if lang == 'c':
        if tokenizerOption == 'exact':
            tokenizer = "c_tokenizer_exact.py"
        else:
            tokenizer = "c_tokenizer_rough.py"
    elif lang == 'python':
        tokenizer = "py_tokenizer.py"
    else:
        tokenizer = "java_tokenizer.py"

    ### get list of file path
    if lang == 'c':   
        for (path, dir, files) in os.walk(src1):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if((ext == '.c') or (ext == '.cpp')):
                    src1_list.append(path + '/' + filename)
        for (path, dir, files) in os.walk(src2):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ((ext == '.c') or (ext == '.cpp')):
                    src2_list.append(path + '/' + filename)
    elif lang == 'python':
        for (path, dir, files) in os.walk(src1):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if(ext == '.py'):
                    src1_list.append(path + '/' + filename)
        for (path, dir, files) in os.walk(src2):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if (ext == '.py'):
                    src2_list.append(path + '/' + filename)
    elif lang == 'java':
        for (path, dir, files) in os.walk(src1):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if(ext == '.java'):
                    src1_list.append(path + '/' + filename)
        for (path, dir, files) in os.walk(src2):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if (ext == '.java'):
                    src2_list.append(path + '/' + filename)

    result['fileNum'] = { 'src1': len(src1_list), 'src2': len(src1_list) }


    ### get line number of each file
    result['lineNum'] = { 'src1': {}, 'src2': {} }
    for path in src1_list:
        f = open(path, 'r')
        n = len(f.readlines())
        result['lineNum']['src1'][path] = n
        src1_totalLineNumber = src1_totalLineNumber + n
        f.close()

    for path in src2_list:
        f = open(path, 'r')
        n = len(f.readlines())
        result['lineNum']['src2'][path] = n
        src2_totalLineNumber = src2_totalLineNumber + n
        f.close()

    result['lineNum']['src1']['totalLineNum'] = src1_totalLineNumber
    result['lineNum']['src2']['totalLineNum'] = src2_totalLineNumber
    print('src1 totalLineNumber : ', result['lineNum']['src1']['totalLineNum'])
    print('src2 totalLineNumber : ', result['lineNum']['src2']['totalLineNum'])


    ### get token sequence of each file
    print('start getting tokens...')
    for path in src1_list:
        print(path)
        tokenSequence = subprocess.check_output(["python", tokenizer, path])
        src1_tokens[path] = tokenSequence

    for path in src2_list:
        print(path)
        tokenSequence = subprocess.check_output(["python", tokenizer, path])
        src2_tokens[path] = tokenSequence


    ### get score of each file combinations
    print('start getting score...')
    result['score'] = {}
    result['sum'] = {}
    for i in src1_list:
        result['score'][i] = {}
        result['sum'][i] = {}
        for j in src2_list:
            tokenSequence_1 = src1_tokens[i]
            tokenSequence_2 = src2_tokens[j]
            score = substr.getLCS(tokenSequence_1, tokenSequence_2, criterion)
            result['score'][i][j] = score
            result['sum'][i][j] = getSum(score)



    print("--- %s seconds ---" %(time.time() - start_time))
    return result



















