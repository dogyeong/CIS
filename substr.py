import sys

 
def getLCS(tokenSequence1 , tokenSequence2, criterion):
    # Get List of token using given parameter
    X = tokenSequence1.split('#')[1:]
    Y = tokenSequence2.split('#')[1:]

    for i in range(len(X)):
        temp_list = X[i].split(',')
        X[i] = { 'token': temp_list[0], 'line': temp_list[1] }
    for i in range(len(Y)):
        temp_list = Y[i].split(',')
        Y[i] = { 'token': temp_list[0], 'line': temp_list[1] }

    # Initialize variables
    lcs = [[0]*(len(Y)+1) for i in range((len(X)+1))]
    result = []

    # get LCS array
    for i in range(len(X)+1):
        for j in range(len(Y)+1):
            if (i==0 or j==0):
                lcs[i][j] = 0;
            elif (X[i-1]['token'] == Y[j-1]['token']):
                lcs[i][j] = lcs[i-1][j-1] + 1
                #length = max(length, lcs[i][j])
    
    '''            
    for i in range(len(X)+1):
        print(lcs[i])
    '''

    # Find common token sequences (diagonal)
    i = len(X)
    j = len(Y)
    nextI = i
    while (i>=0 and j>=0):
        if(lcs[i][j] > criterion):
            temp_dict = {
                'src1_lineEnd': int(X[i-1]['line']),
                'src2_lineEnd': int(Y[j-1]['line']),
                'length': lcs[i][j]
                }
            temp_len = lcs[i][j]
            i = i-temp_len
            j = j-temp_len
            nextI = i
            temp_dict['src1_lineStart'] = int(X[i]['line'])
            temp_dict['src2_lineStart'] = int(Y[j]['line'])
            print("--------------- Find Code Clone. ---------------")
            print(temp_dict)
            result.append(temp_dict)
        else:
            if (i != 0):
                i = i-1
            else:
                i = nextI
                j = j-1
       

    return result	    
