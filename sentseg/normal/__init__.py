# -*- coding: utf-8 -*-
# 各种断句算法的实现
from __future__ import unicode_literals

import re


def get_sentences_speed(doc):
    # 简单快速，基本可用
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[，。？！；!?…~]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


def get_sentences_grammar(doc):
    # 按照中文语法切分
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[。？！?!]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


def get_sentences_ellipsis(para):
    # 考虑省略号
    para = re.sub('([，；。！？\?\!])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


def get_sentences_en(doc):
    # 英文断句，不完善
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[。？！?!.,]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences


# 功能全面的断句方法
# 考虑各类括号、省略号等影响断句的标点
class SentenceSplitter(object):
    def __init__(self):
        self.text = None
        self.end_operator = ["。", "？", "……", "…", "~", "！"]

    # 处理括号问题
    def process_bracket(self, end_operator_index):
        couple_operator = [['(', ')'], ['（', '）'], ['[', ']'], ['《', '》'], ['【', '】'], ['<', '>']]
        left_bracket_index = -1

        for op in couple_operator:
            temp = self.text[:end_operator_index].find(op[0])
            if temp > left_bracket_index:
                left_bracket_index = temp
                coup_op = op

        if left_bracket_index != -1:
            right_bracket_index = self.text[end_operator_index + 1:].find(coup_op[1]) + end_operator_index
            if right_bracket_index != -1:
                # 防止(xxx(x),xx。xxxx(xx))错误
                if self.text[left_bracket_index + 1:right_bracket_index].find(coup_op[0]) == -1 and \
                        self.text[left_bracket_index + 1:right_bracket_index].find(coup_op[1]) == -1:
                    end_operator = re.search("|".join(self.end_operator), self.text[right_bracket_index:])
                    end_operator_index = self.text[right_bracket_index:].index(
                        end_operator.group()) + right_bracket_index

        return end_operator_index

    def cut(self, text, grammar=True):
        if not grammar:
            # 判断是不是语法格式切分，主要针对"，"和"；"
            self.end_operator.append("，")
            self.end_operator.append("；")
            self.end_operator.append(";")
        sentence_set = [sentence.strip() for sentence in text.split("\n") if sentence.strip()]
        # print(sentence_set)
        res = []

        for sentence in sentence_set:
            try:
                for s in self.rules(sentence, []):
                    res.append(s)
            except Exception as e:
                res.append(sentence)
                print(e)
                print(sentence)

        return res

    def rules(self, sentence, cut_list):
        self.text = sentence
        if not self.text:
            return cut_list

        # 如果为对话 则切分 “xxx。xxx”
        if self.text[0] == "“":
            couple_index = self.text.find("”")
            # 如果匹配到
            if couple_index != -1:
                if self.text[couple_index - 1] in self.end_operator:
                    cut_list.append(self.text[:couple_index + 1])
                    # 继续切分余下的句子
                    text = self.text[couple_index + 1:]
                    return self.rules(text, cut_list)
                else:
                    end_operator = re.search("|".join(self.end_operator), self.text)
                    if end_operator:
                        end_operator_index = self.text.index(end_operator.group())
                        if "“" not in self.text[couple_index:end_operator_index]:
                            cut_list.append(self.text[:end_operator_index + 1])
                            # 继续切分余下的句子
                            text = self.text[end_operator_index + 1:]
                            return self.rules(text, cut_list)
                        else:
                            couple_index_2 = self.text[couple_index + 1:].find("”")
                            if couple_index_2 != -1:
                                couple_index_2 = couple_index_2 + couple_index + 1
                                if couple_index_2 == len(self.text) - 1:
                                    cut_list.append(self.text)
                                    return cut_list
                                elif self.text[couple_index_2 - 1] in self.end_operator:
                                    cut_list.append(self.text[:couple_index_2 + 1])
                                    # 继续切分余下的句子
                                    text = self.text[couple_index_2 + 1:]
                                    return self.rules(text, cut_list)
                                elif self.text[couple_index_2 + 1] in self.end_operator:
                                    cut_list.append(self.text[:couple_index_2 + 2])
                                    # 继续切分余下的句子
                                    text = self.text[couple_index_2 + 2:]
                                    return self.rules(text, cut_list)
                                else:
                                    cut_list.append(self.text)
                                    return cut_list
                    else:
                        cut_list.append(self.text)
                        return cut_list
            # 错误符号用法直接返回该句子
            else:
                # cut_list.append(self.text)
                return self.rules(self.text[1:], cut_list)

        else:
            end_operator = re.search("|".join(self.end_operator), self.text)
            if end_operator:
                end_operator_index = self.text.index(end_operator.group())
                # xxxxxxx。类型
                if "“" not in self.text[:end_operator_index] and "”" not in self.text[:end_operator_index]:
                    if end_operator.group() == "……":
                        end_operator_index += 1
                    # 处理括号问题
                    end_operator_index = self.process_bracket(end_operator_index)
                    cut_list.append(self.text[:end_operator_index + 1])
                    text = self.text[end_operator_index+1:]
                    return self.rules(text, cut_list)
                # xxx"xxx"xx。
                elif "“" in self.text[:end_operator_index] and "”" in self.text[:end_operator_index]:
                    if end_operator.group() == "……":
                        end_operator_index += 1
                    # 处理括号问题
                    end_operator_index = self.process_bracket(end_operator_index)
                    cut_list.append(self.text[:end_operator_index + 1])
                    text = self.text[end_operator_index+1:]
                    return self.rules(text, cut_list)

                if "“" not in self.text[:end_operator_index] or \
                        ("“" in self.text[:end_operator_index] and "”" in self.text[:end_operator_index]):
                    if end_operator.group() == "……":
                        end_operator_index += 1

                    if "”" in self.text[end_operator_index + 1:]:
                        couple_index = self.text[end_operator_index + 1:].find("”") + end_operator_index + 1
                        if couple_index == len(self.text) - 1:
                            cut_list.append(self.text)
                            return cut_list
                        elif self.text[couple_index - 1] in self.end_operator:
                            cut_list.append(self.text[:couple_index + 1])
                            text = self.text[couple_index + 1:]
                            return self.rules(text, cut_list)
                        else:
                            cut_list.append(self.text[:end_operator_index + 1])
                            # 继续切分余下的句子
                            text = self.text[end_operator_index + 1:]
                            return self.rules(text, cut_list)
                    else:
                        # 处理括号问题
                        end_operator_index = self.process_bracket(end_operator_index)
                        cut_list.append(self.text[:end_operator_index + 1])
                        # 继续切分余下的句子
                        text = self.text[end_operator_index + 1:]
                        return self.rules(text, cut_list)
                # “xxxxxx。xxxx”类型
                else:
                    couple_index = self.text.find("”")
                    # 如果引号在句子末尾直接返回， 不再切割
                    if couple_index == len(self.text) - 1:
                        cut_list.append(self.text)
                        return cut_list
                    elif couple_index != -1:
                        # 如果引号在之前是断号
                        if self.text[couple_index - 1] in self.end_operator:
                            cut_list.append(self.text[:couple_index + 1])
                            # 继续切分余下的句子
                            text = self.text[couple_index + 1:]
                            return self.rules(text, cut_list)
                        # elif self.text[couple_index + 1] in self.end_operator:
                        #     cut_list.append(self.text[:couple_index + 2])
                        #     # 继续切分余下的句子
                        #     text = self.text[couple_index + 2:]
                        #     return self.rules(text, cut_list)
                        # else:
                        #     # cut_list.append(self.text)
                        #     # 继续切分余下的句子
                        #     cut_list.append(self.text[:end_operator_index+1])
                        #     text = self.text[end_operator_index + 1:]
                        #     return self.rules(text, cut_list)
                        else:
                            # "xxx,xxx。"xx（xxx，xx）xx。xxx
                            next_end_operator = re.search("|".join(self.end_operator), self.text[couple_index:])
                            next_end_index = self.text[couple_index:].index(next_end_operator.group()) + couple_index
                            # # 处理括号问题
                            next_end_index = self.process_bracket(next_end_index)
                            cut_list.append(self.text[:next_end_index + 1])
                            # 继续切分余下句子
                            text = self.text[next_end_index + 1:]
                            return self.rules(text, cut_list)
                    else:
                        cut_list.append(self.text)
                        return cut_list
            else:
                cut_list.append(self.text)
                return cut_list
