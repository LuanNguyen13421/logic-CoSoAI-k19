import os

# Kiểm tra 2 literal có đối không
def IsOppositeLiteral(a, b):
    if len(a) == len(b):
        return False
    else:
        if len(a) == 2:
            return a[1] == b[0]
        else:
            return a[0] == b[1]

# Kiểm tra 2 câu có phần đối nhau không
def IsOppositeSentence(a, b):
    first_sentence = a.split(" OR ")
    second_sentence = b.split(" OR ")
    for i in first_sentence:
        for j in second_sentence:
            if IsOppositeLiteral(i, j):
                return True
    return False

# Sắp xếp các literals theo thứ tự
def Sort(sen):
    for i in range(0, len(sen)):
        for j in range(i+1, len(sen)):
            first = sen[i]
            second = sen[j]
            if first[0] == '-':
                first = first[1]
            if second[0] == '-':
                second = second[1]
            if first > second:
                sen[i], sen[j] = sen[j], sen[i]
    return sen

# Nghịch đảo literal
def NegativeLiteral(literal):
    if len(literal) == 1:
        return "-" + literal
    else:
        return literal[1]

# Nghịch đảo keyword
def NegativeKeyword(keyword):
    if keyword == "OR":
        return "AND"
    else:
        return "OR"

# Nghịch đảo câu bao gồm cả literal và keyword
def NegativeSentence(sen):
    parts = sen.split(' ')
    for i in range(0, len(parts)):
        if i % 2 == 0:
            parts[i] = NegativeLiteral(parts[i])
        else:
            parts[i] = NegativeKeyword(parts[i])
    return (' ').join(parts)

# Hợp giải hai câu có literal đối nhau
def CombineSentence(first_sentence, second_sentence):
    first_literals = first_sentence.split(" OR ")
    second_literals = second_sentence.split(" OR ")
    first_opposite_pos = []
    second_opposite_pos = []
    for i in range(0, len(first_literals)):
        for j in range(0, len(second_literals)):
            if IsOppositeLiteral(first_literals[i], second_literals[j]):
                first_opposite_pos.append(i)
                second_opposite_pos.append(j)
    
    # Hợp giải khi 2 câu chỉ có 1 cặp literal đối nhau
    if len(first_opposite_pos) == 1 and len(second_opposite_pos) == 1:
        first_literals.remove(first_literals[first_opposite_pos[0]])
        second_literals.remove(second_literals[second_opposite_pos[0]])
        result = first_literals + second_literals
        result = list(set(result))
        result = Sort(result)
        if len(result) == 0:
            return "{}"
        else:
            return " OR ".join(result)
    else:
        return "null"

# Đọc file input, chuẩn hoá về 1 chuỗi
def ReadInputFile(file):
    fstream = open(file, "r")
    result = []

    # Đọc alpha và chuẩn hoá alpha
    alpha = fstream.readline()
    alpha = alpha.rstrip()
    if len(alpha) <= 2:
        alpha = NegativeLiteral(alpha)
        result.append(alpha)
    else:
        alpha = NegativeSentence(alpha)
        alpha = alpha.split(" AND ")
        for i in alpha:
            result.append(i)
    
    # Đọc KB
    n = int(fstream.readline())
    for i in range(0, n):
        sentence = fstream.readline()
        sentence = sentence.rstrip()
        result.append(sentence)

    fstream.close()
    result = list(set(result))
    return result

# Ghi file output
def WriteOutputFile(file, sentence):
    fstream = open(file, "w")
    for i in sentence:
        fstream.writelines(i)
    fstream.close()

def PL_RESOLUTION(sentence):
    result = []
    loop_result = []
    checked_pos = 1
    while True:
        loop_result.clear()
        for i in range(0, len(sentence) - 1):
            for j in range(checked_pos, len(sentence)):
                if i < j:
                    if IsOppositeSentence(sentence[i], sentence[j]):
                        temp = CombineSentence(sentence[i], sentence[j])
                        if temp != "null":
                            loop_result.append(temp)
        checked_pos = len(sentence)
        
        # Kết thúc nếu không có mệnh đề mới phát sinh
        if len(loop_result) == 0:
            result.append("0\n")
            result.append("NO")
            break
        
        # Loại những mệnh đề trùng có trong loop_result và thêm những mệnh đề mới vào KB
        loop_result = list(set(loop_result).difference(sentence))
        loop_result = Sort(loop_result)
        sentence.extend(loop_result)

        # Ghi những mệnh đề mới vào kết quả
        if len(loop_result) != 0:
            result.append(str(len(loop_result)) + '\n')
            for e in loop_result:
                result.append(e)
                result.append('\n')
                sentence.append(e)

        # Kết thúc nếu KB đã hết mệnh đề
        if '{}' in sentence:
            result.append("YES")
            break
    return result

# Main
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_INPUT = ROOT_DIR + '/input'
ROOT_OUTPUT=ROOT_DIR + '/output'

for file in os.listdir(ROOT_INPUT):
    file_input = ROOT_INPUT + '/' + file
    file_output = ROOT_OUTPUT + '/' + 'output' + file[file.find('_'):]
    sentence = ReadInputFile(file_input)
    result = PL_RESOLUTION(sentence)
    WriteOutputFile(file_output, result)