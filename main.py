# 引入随机数模块
import random
import os
import json


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        return False


words_file_name = "words/datalib.txt"
english_file_name = "words/english.txt"
chinese_file_name = "words/chinese.txt"
base_dir = "data"
always_trace_file_name = base_dir + '/' + 'progress.txt'
trace_file_name = base_dir + '/' + "trace.txt"
correct_file_name = base_dir + '/' + "correct.txt"
mistake_1_file_name = base_dir + '/' + "mistake 1.txt"
mistake_2_file_name = base_dir + '/' + "mistake 2.txt"
mistake_3_file_name = base_dir + '/' + "mistake 3.txt"
finish_words_file_name = base_dir + '/' + "finish.txt"
progress_words_file_name = base_dir + '/' + "middles.dat"
remain_words_number = 12

mkdir(base_dir)

words = open(words_file_name, mode='r', encoding='UTF-8')
english_f = open(english_file_name, mode='w', encoding="UTF-8")
chinese_f = open(chinese_file_name, mode='w', encoding="UTF-8")
content = words.readlines()
content_lines = len(content)
for line in range(content_lines):
    if line % 2 == 0:
        english_f.write(content[line].strip() + '\n')
        english_f.flush()
    else:
        chinese_f.write(content[line].strip() + '\n')
        chinese_f.flush()
words.close()
english_f.close()
chinese_f.close()

f_english = open(english_file_name, mode='r', encoding='UTF-8')
f_chinese = open(chinese_file_name, mode='r', encoding='UTF-8')
eng_words = f_english.readlines()
ch_words = f_chinese.readlines()
f_english.close()
f_chinese.close()
words_trace = {}
words_history = []

if os.path.exists(progress_words_file_name):
    f = open(progress_words_file_name, mode='r+', encoding='UTF-8')
    dict_str = f.read()
    words_trace = json.loads(dict_str)
else:
    for word in eng_words:
        words_trace[word.strip()] = {"index": eng_words.index(word),
                                     "translation": ch_words[eng_words.index(word)],
                                     "remain count": 3,
                                     "correct count": 0,
                                     "mistake count": 0}

if os.path.exists(finish_words_file_name):
    f = open(finish_words_file_name, encoding='UTF-8', mode='a+')
    finish_words = f.readlines()
    for word in finish_words:
        word = word.strip()
        if word in eng_words:
            eng_words.remove(word)

print("\n开始背单词了，不要偷懒哟，生活会看着你的，加油！-_- \n\n")

while len(eng_words) > remain_words_number:
    word_index = random.randint(0, len(eng_words) - 1)
    word = eng_words[word_index].strip()

    if word in words_history:
        continue
    if len(words_history) >= 10:
        words_history = words_history[1:]
    words_history.append(word)

    total_eng_size = random.randint(3, 6)
    total_ch_size = random.randint(6, 10)
    correct_eng_index = random.randint(0, total_eng_size - 1)
    correct_ch_index = random.randint(0, total_ch_size - 1)
    words_array = []
    translation_array = []
    for w_index in range(total_eng_size):
        if w_index == correct_eng_index:
            words_array.append(word)
        else:
            append_word = eng_words[random.randint(0, len(eng_words) - 1)]
            while append_word in words_array:
                append_word = eng_words[random.randint(0, len(eng_words) - 1)]
            words_array.append(append_word)

    for w_index in range(total_ch_size):
        if w_index == correct_ch_index:
            translation_array.append(words_trace[word]["translation"])
        else:
            append_word = ch_words[random.randint(0, len(ch_words) - 1)]
            while append_word in words_array:
                append_word = ch_words[random.randint(0, len(ch_words) - 1)]
            translation_array.append(append_word)

    for index in range(total_ch_size):
        if index < len(words_array):
            print(str(index) + '、 ' + words_array[index].strip())
        print("                 " + str(index) + '、 ' + translation_array[index].strip())

    # print("请输入答案:")
    input_str = input("\n请输入答案:  ")
    input_str = input_str.strip()
    if not len(input_str) == 2 \
            or not 0 <= int(input_str[0]) < total_eng_size \
            or not 0 <= int(input_str[1]) < total_ch_size:
        input_str = input_str.split()
        while len(input_str) != 2 \
                or not 0 <= int(input_str[0].strip()) < total_eng_size \
                or not 0 <= int(input_str[1].strip()) < total_ch_size:
            # print("请输入正确的选择: ")
            input_str = input("请输入正确的选择:  ")
            input_str = input_str.strip()
            if len(input_str) == 2 \
                    and 0 <= int(input_str[0]) < total_eng_size \
                    and 0 <= int(input_str[1]) < total_ch_size:
                break
            input_str = input_str.split()
    word_correct_index = int(input_str[0].strip())
    chinese_correct_index = int(input_str[1].strip())

    words_trace[word]["remain count"] = words_trace[word]["remain count"] - 1
    if word_correct_index == correct_eng_index and chinese_correct_index == correct_ch_index:
        words_trace[word]["correct count"] = words_trace[word]["correct count"] + 1
        print("答对了，加油喔")
        print("***强化一下记忆中的它***\n     " + word + "    " + words_trace[word]["translation"] + '\n')
    else:
        words_trace[word]["mistake count"] = words_trace[word]["mistake count"] + 1
        print("很遗憾，你还没有记住它，想想你未来的家，努力吧\n")
        print("@@@@@这个单词必须记住，相信自己@@@@@\n     " + word + "    " + words_trace[word]["translation"] + '\n')

    f = open(always_trace_file_name, mode='a+', encoding='UTF-8')
    f.write(word + "\n" + words_trace[word]["translation"] + '\n')
    f.flush()
    f.close()

    f = open(progress_words_file_name, mode='w', encoding='UTF-8')
    dict_str = json.dumps(words_trace)
    f.write(dict_str)
    f.flush()
    f.close()

    if words_trace[word]["remain count"] < 1:
        f_trace = open(trace_file_name, mode='a+', encoding='UTF-8')
        f_trace.write(word + "    " + words_trace[word]["translation"]
                      + "    正确:" + str(words_trace[word]["correct count"])
                      + "次\n    错误:" + str(words_trace[word]["mistake count"] + "次\n"))
        f_trace.flush()
        eng_words.remove(word)
        f = open(finish_words_file_name, mode='a+', encoding='UTF-8')
        f.write(word + '\n')
        f.flush()
        f.close()
        if words_trace[word]["mistake count"] == 0:
            f_trace.write("        请继续加油哟，为了小可爱，为了美好的生活\n\n")
            f_trace.flush()
            f = open(correct_file_name, mode='a+', encoding='UTF-8')
            f.write(word + "    " + words_trace[word]["translation"])
            f.flush()
            f.close()
        elif words_trace[word]["mistake count"] == 1:
            f_trace.write("--------这个单词需要注意哟----------\n\n")
            f_trace.flush()
            f = open(mistake_1_file_name, mode='a+', encoding='UTF-8')
            f.write(word + "    " + words_trace[word]["translation"])
            f.flush()
            f.close()
        elif words_trace[word]["mistake count"] == 2:
            f_trace.write("=======必须留心了，不要放弃=========\n\n")
            f_trace.flush()
            f = open(mistake_2_file_name, mode='a+', encoding='UTF-8')
            f.write(word + "    " + words_trace[word]["translation"])
            f.flush()
            f.close()
        elif words_trace[word]["mistake count"] == 3:
            f_trace.write("#######警告，快点把他记下来#########\n\n")
            f_trace.flush()
            f = open(mistake_3_file_name, mode='a+', encoding='UTF-8')
            f.write(word + "    " + words_trace[word]["translation"])
            f.flush()
            f.close()
        f_trace.close()
print("很难得，终于到这一天了，剩下" + str(remain_words_number) + "个单词，要继续加油呀，\n这里就直接告诉你答案吧" \
      + '请努力记住：')
f = open(always_trace_file_name, mode='a+', encoding='UTF-8')
f.write('\n\n终于来到了这一天，让我们一起迈向明天\n               感到自己\n')
f.flush()
for word in eng_words:
    print(word + "     " + words_trace[word]["translation"])
    f.write(word + "     " + words_trace[word]["translation"] + '\n')
    f.flush()
f.close()
print("记住单词后按下任意键结束学习，感动自己才能感动他人，让世界为自己喝彩，加油，相信自己！")
input()
