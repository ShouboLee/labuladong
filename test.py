from sentseg import Passage
from sentseg.normal import get_sentences_speed
from sentseg import normal
import pandas as pd
import time


if __name__ == '__main__':
    data_path = 'data/一讯通模型_宏观新闻_20221010_1014_pred_宏观.tsv'
    data_path_2 = 'data/sample_0829.csv'
    df = pd.read_csv(data_path, sep='\t')
    # contents = df['正文']
    contents = df['content']
    start = time.perf_counter()
    for content in contents:
        Seg = Passage(content)
        Seg.sentences_speed
        # print(Seg.sentences_speed)
    end = time.perf_counter()
    print('sentence_speed:', end - start)

    start = time.perf_counter()
    for content in contents:
        Seg = Passage(content)
        print(Seg.sentences())
    end = time.perf_counter()
    print('sentence:', end - start)



