def LZ77decode(code):
    decode = ''
    for c in code:
        if c[0] == '_':
            decode += c[2]
        else:
            for k in range(c[1]):
                mx_char = len(decode)
                decode += decode[mx_char-c[0]]
            decode += c[2]
    return decode

def update_workspace(present,d_size,b_size,text_to_list):
    workspace = [0]*(d_size + b_size)
    workspace[-b_size-present::] = text_to_list[0:b_size+present]
    true_workspace = workspace[-(d_size + b_size)::]
    return true_workspace

def num_of_sol(list,target):
    count = 0
    for c in list:
        if c == target:
            count += 1
    return count

def find_best_sol(best_sol):
    repeat_list = []
    for e in best_sol:
        repeat_list.append(e[1])
    repeat_max = max(repeat_list)
    wanted_index = []
    for e in best_sol:
        if e[1] == repeat_max:
            wanted_index.append(e[0])
    wanted_LZ77_index = min(wanted_index)
    for e in best_sol:
        if e[0] == min(wanted_index) and e[1] == repeat_max:
            next_char_index = e[2]
    return (wanted_LZ77_index, repeat_max, next_char_index) 

def LZ77encode(text,d_size,b_size): # '_' is a stop marker.
    text_adjust = text + '_'*b_size
    text_to_list = [c for c in text_adjust]
    present = 0
    code = []
    w = update_workspace(present,d_size,b_size,text_to_list)
    while w[d_size] != '_':
        n = num_of_sol(w[0:d_size],w[d_size])
        sol = 0
        if n > 0:
            lz77i = 0
            best_sol = []
            while sol != n:
                bwi = w[0:d_size][::-1].index(w[d_size],lz77i)
                lz77i = bwi + 1
                ttli = present - lz77i
                count = 0
                for i in range(ttli,len(text)-lz77i+1):
                    if text_to_list[i] == text_to_list[i+lz77i]:
                        count += 1
                        next_char_index = i+lz77i
                    else: break
                best_sol.append([lz77i,count,next_char_index+1])
                sol += 1
            [a,b,c] = find_best_sol(best_sol)
            code.append([a,b,text_to_list[c]])
            present = present + b + 1
            w = update_workspace(present,d_size,b_size,text_to_list)
        else:
            code.append(['_',0,w[d_size]])
            present = present + 1
            w = update_workspace(present,d_size,b_size,text_to_list)
    return code

text1 = 'AAABCADEFAABCDCDCDGGGGGH' # d_size = 8, b_size = 5 
code1 = [['_', 0, 'A'], [1, 2, 'B'], ['_', 0, 'C'], [3, 1, 'D'], ['_', 0, 'E'], ['_', 0, 'F'], [8, 4, 'D'], [2, 4, 'G'], [1, 4, 'H']]
text2 = 'AACAACABCABAAAC' # d_size = 6, b_size = 4
code2 = [['_', 0, 'A'], [1, 1, 'C'], [3, 4, 'B'], [3, 3, 'A'], [1, 2, 'C']]

print(LZ77encode(text1,8,5))
print(LZ77encode(text2,6,4))

print(LZ77decode(code1))
print(LZ77decode(code2))

