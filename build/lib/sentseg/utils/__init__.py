# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import w3lib.html
import urllib
import html
from opencc import OpenCC


def clean_text(text, remove_url=True, email=True, weibo_at=True, stop_terms=("转发微博",),
               emoji=True, weibo_topic=False, deduplicate_space=True,
               norm_url=False, norm_html=False, to_url=False,
               remove_puncts=False, remove_tags=True, t2s=False,
               expression_len=(1, 6), linesep2space=False):
    # unicode不可见字符
    # 未转义
    text = re.sub(r"[\u200b-\u200d]", "", text)
    # 已转义
    text = re.sub(r"(\\u200b|\\u200c|\\u200d)", "", text)
    # 反向的矛盾设置
    if norm_url and to_url:
        raise Exception("norm_url和to_url是矛盾的设置")
    if norm_html:
        text = html.unescape(text)
    if to_url:
        text = urllib.parse.quote(text)
    if remove_tags:
        text = w3lib.html.remove_tags(text)
    if remove_url:
        try:
            URL_REGEX = re.compile(
                r'(?i)http[s]?://(?:[a-zA-Z]|[0-9]|[#$%*-;=?&@~.&+]|[!*,])+',
                re.IGNORECASE)
            text = re.sub(URL_REGEX, "", text)
        except:
            # sometimes lead to "catastrophic backtracking"
            zh_puncts1 = "，；、。！？（）《》【】"
            URL_REGEX = re.compile(
                r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
                re.IGNORECASE)
            text = re.sub(URL_REGEX, "", text)
    if norm_url:
        text = urllib.parse.unquote(text)
    if email:
        EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
        text = re.sub(EMAIL_REGEX, "", text)
    if weibo_at:
        text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    if emoji:
        # 去除括号包围的表情符号
        # ? lazy match避免把两个表情中间的部分去除掉
        if type(expression_len) in {tuple, list} and len(expression_len) == 2:
            # 设置长度范围避免误伤人用的中括号内容，如[加上特别番外荞麦花开时共五册]
            lb, rb = expression_len
            text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
        else:
            text = re.sub(r"\[\S+?\]", "", text)
        # text = re.sub(r"\[\S+\]", "", text)
        # 去除真,图标式emoji
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
    if weibo_topic:
        text = re.sub(r"#\S+#", "", text)  # 去除话题内容
    if linesep2space:
        text = text.replace("\n", " ")  # 不需要换行的时候变成1行
    if deduplicate_space:
        text = re.sub(r"(\s)+", r"\1", text)  # 合并正文中过多的空格
    if t2s:
        cc = OpenCC('t2s')
        text = cc.convert(text)
    assert hasattr(stop_terms, "__iter__"), Exception("去除的词语必须是一个可迭代对象")
    if type(stop_terms) == str:
        text = text.replace(stop_terms, "")
    else:
        for x in stop_terms:
            text = text.replace(x, "")
    if remove_puncts:
        allpuncs = re.compile(
            r"[，\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
        text = re.sub(allpuncs, "", text)

    return text.strip()
