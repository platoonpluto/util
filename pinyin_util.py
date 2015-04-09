# -*- coding: utf-8 -*-

pinyin_mapping = {}

def load_pinyin_dict(pinyin_dict_filename):
    pinyin_dict_file = open(pinyin_dict_filename)
    for line in pinyin_dict_file:
        columns = line.strip().decode('utf-8').split('=')
        if len(columns) != 2:
            continue
        pinyins = columns[1].split(',')
        pinyin_mapping[columns[0]] = pinyins
    pinyin_dict_file.close()

def get_single_pinyin(word):
    if word not in pinyin_mapping:
        return None
    return pinyin_mapping[word]

def next_permutation(upper_bound, current_index):
    idx = len(upper_bound) - 1
    while idx >= 0:
        if current_index[idx] + 1 < upper_bound[idx]:
            current_index[idx] += 1
            idx += 1
            while idx < len(upper_bound):
                current_index[idx] = 0
                idx += 1
            return True
        idx -= 1
    return False

def get_multiple_pinyin(words):
    results = []
    pinyin_vecs = []
    for word in words:
        if '0' <= word <= '9' or 'a' <= word <= 'z' or 'A' <= word <= 'Z':
            pinyin_vecs.append([word])
            continue
        tmp = get_single_pinyin(word)
        if tmp == None:
            pinyin_vecs.append([""])
        else:
            pinyin_vecs.append(tmp)
    upper_bound = []
    current_index = []
    for idx in xrange(0, len(words)):
        upper_bound.append(len(pinyin_vecs[idx]))
        current_index.append(0)
    while True:
        vec = []
        for idx in xrange(0, len(words)):
            vec.append(pinyin_vecs[idx][current_index[idx]])
        mapping = []
        for idx in xrange(0, len(words)):
            for ch in vec[idx]:
                mapping.append(idx)
        results.append(["".join(vec), mapping])
        if next_permutation(upper_bound, current_index) == False:
            break
    return results

def lcs(vec1, vec2):
    len1 = len(vec1)
    len2 = len(vec2)
    common = []
    dp = [[0 for idx2 in xrange(len2+1)] for idx1 in xrange(len1+1)]
    flags = [[0 for idx2 in xrange(len2+1)] for idx1 in xrange(len1+1)]
    for idx1 in xrange(1, idx1+1):
        for idx2 in xrange(1, idx2+1):
            if vec1[idx1-1] == vec2[idx2-1]:#左上角
                dp[idx1][idx2] = dp[idx1-1][idx2-1] + 1
                flags[idx1][idx2] = 1
            elif dp[idx1-1][idx2] > dp[idx1][idx2-1]:#上方
                dp[idx1][idx2] = dp[idx1-1][idx2]
                flags[idx1][idx2] = 2
            else:#左侧
                dp[idx1][idx2] = dp[idx1][idx2-1]
                flags[idx1][idx2] = 3
    idx1 = len1
    idx2 = len2
    #print vec1, vec2
    #for vec in dp:
    #    print vec
    while idx2 > 0 and dp[idx1][idx2] == dp[idx1][idx2-1]:
        idx2 -= 1
    while idx1 > 0 and idx2 > 0:
        if flags[idx1][idx2] == 1:
            common.append(idx2-1)
            idx1 -= 1
            idx2 -= 1
        elif flags[idx1][idx2] == 2:
            idx1 -= 1
        elif flags[idx1][idx2] == 3:
            idx2 -= 1
    common.reverse()
    return dp[len1][len2], common

def lcs_query(query1, query2, commons):
    pinyins1 = get_multiple_pinyin(query1)
    pinyins2 = get_multiple_pinyin(query2)
    for pinyin1 in pinyins1:
        for pinyin2 in pinyins2:
            lcs_number, vec = lcs(pinyin1[0], pinyin2[0])
            if lcs_number + 1 >= len(pinyin1[0]) and vec[-1]-vec[0] <= len(pinyin1[0]):
                #print lcs_number, vec
                positions = []
                for v in vec:
                    if pinyin2[1][v] not in positions:
                        positions.append(pinyin2[1][v])
                common = []
                for p in positions:
                    common.append(query2[p])
                common = ''.join(common)
                #print common
                if common not in commons:
                    commons[common] = 0
                commons[common] += 1
                break


load_pinyin_dict("../data/pinyin.txt")


if __name__ == "__main__":
    '''pinyins = get_multiple_pinyin(u"单机游戏")
    for p in pinyins:
        print p'''
    print lcs(u"123564", u"123456")
    commons = {}
    lcs_query(u"习伯伯", u"习伯小苹版", commons)
    for common in commons:
        print common

