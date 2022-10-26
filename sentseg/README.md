# SentSeg
提供用于中文断句的工具（0.0.1）。
## Quickstart
### 安装
`pip install sentseg # 安装sentseg`
### 使用
```python
from sentseg import Passage

para = '公司（恒安，下同）市场份额扩大。公司推出了安全运营平台，扎实开展“转作风、树形象，保要素、促发展”活动。'
s = Passage(para)   # initialize Passage

sentence = s.sentences()    # 采用精确断句，默认按照中文语法规则。
# OUTPUT: ['公司（恒安，下同）市场份额扩大。', '公司推出了安全运营平台，扎实开展“转作风、树形象，保要素、促发展”活动。']

sentence = s.sentences(grammar=False)    # 采用精确断句，细粒度切分，不按照中文语法规则。
# OUTPUT: ['公司（恒安，下同）市场份额扩大。', '公司推出了安全运营平台，', '扎实开展“转作风、树形象，保要素、促发展”活动。']

sentence = s.sentences_speed   # 采用快速断句，细粒度切分。
# OUTPUT: ['公司（恒安', '下同）市场份额扩大', '公司推出了安全运营平台', '扎实开展“转作风、树形象', '保要素、促发展”活动']

s.sentences_grammar # 采用快速切分，按照中文语法规则。
# OUTPUT: ['公司（恒安，下同）市场份额扩大', '公司推出了安全运营平台，扎实开展“转作风、树形象，保要素、促发展”活动']

# clean_text: 辅助函数，进行各种文本清洗操作（有些不清洗的文本断句容易出错），如微博中的特殊格式，网址，email，html代码，等等
para2 = "【#恒安#：正筹备下一个项目 但不是地产行业....https://www.langboat.com"
s2 = Passage(para2)
s.clean_text(remove_url=True)
# (清洗网址URL)OUTPUT: 
#   原： 【#恒安#：正筹备下一个项目 但不是地产行业....https://www.langboat.com
#   清洗后： 【#恒安#：正筹备下一个项目 但不是地产行业....
```