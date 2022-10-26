# -*- coding: utf-8 -*-
# 文本处理类的设计
from __future__ import unicode_literals
from . import normal
from . import utils


class Passage(object):
    '''
    主要是初始化Passage对象，调用不同的断句方法
    :param sentences: 返回功能较强的断句结果，可以对整篇文档进行分句
    :param sentences_speed: 能处理普通公告等不包含复杂标点的文本，主要用
    :param sentences_grammar: 根据中文语法进行断句（忽略逗号、分号等处）
    :param sentences_ellipsis: 考虑标点不规范的文本，包括省略号
    :param sentences_en: 英文断句，目前暂未完善
    :return 断句后的list

    :param clean_text: 辅助函数，进行各种文本清洗操作（有些不清洗的文本断句容易出错），如微博中的特殊格式，网址，email，html代码，等等
        :param remove_url: （默认使用）是否去除网址
        :param email: （默认使用）是否去除email
        :param weibo_at: （默认使用）是否去除微博的\@相关文本
        :param stop_terms: 去除文本中的一些特定词语，默认参数为("转发微博",)
        :param emoji: （默认使用）去除\[\]包围的文本，一般是表情符号
        :param weibo_topic: （默认不使用）去除##包围的文本，一般是微博话题
        :param deduplicate_space: （默认使用）合并文本中间的多个空格为一个
        :param norm_url: （默认不使用）还原URL中的特殊字符为普通格式，如(%20转为空格)
        :param norm_html: （默认不使用）还原HTML中的特殊字符为普通格式，如(\&nbsp;转为空格)
        :param to_url: （默认不使用）将普通格式的字符转为还原URL中的特殊字符，用于请求，如(空格转为%20)
        :param remove_puncts: （默认不使用）移除所有标点符号
        :param remove_tags: （默认使用）移除所有html块
        :param t2s: （默认不使用）繁体字转中文
        :param expression_len: 假设表情的表情长度范围，不在范围内的文本认为不是表情，不加以清洗，如[加上特别番外荞麦花开时共五册]。设置为None则没有限制
        :param linesep2space: （默认不使用）把换行符转换成空格
        :return: 清洗后的文本
    '''

    def __init__(self, doc):
        self.doc = doc

    def sentences(self, grammar=True):
        return normal.SentenceSplitter().cut(self.doc, grammar=grammar)

    @property
    def sentences_speed(self):
        return normal.get_sentences_speed(self.doc)

    @property
    def sentences_grammar(self):
        return normal.get_sentences_grammar(self.doc)

    @property
    def sentences_ellipsis(self):
        return normal.get_sentences_ellipsis(self.doc)

    @property
    def sentences_en(self):
        return normal.get_sentences_en(self.doc)

    def clean_text(self, remove_url=True, email=True, weibo_at=True, stop_terms=("转发微博",),
                   emoji=True, weibo_topic=False, deduplicate_space=True,
                   norm_url=False, norm_html=False, to_url=False,
                   remove_puncts=False, remove_tags=True, t2s=False,
                   expression_len=(1, 6), linesep2space=False):
        return utils.clean_text(self.doc, remove_url, email, weibo_at, stop_terms,
                                emoji, weibo_topic, deduplicate_space,
                                norm_url, norm_html, to_url,
                                remove_puncts, remove_tags, t2s,
                                expression_len, linesep2space)
