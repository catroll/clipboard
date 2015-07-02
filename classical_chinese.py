#!/usr/bin/python
# -*- coding: utf-8 -*-

src = u"""
季逑足下：日来用力何似？亮吉三千里外，每有造述，手未握管，心县此人。虽才分素定，亦契慕有独至也！
吾辈好尚既符，嗜欲又寡。幼不随搔首弄姿、顾影促步之客，以求一时之怜；长实思研精蓄神、忘寝与食，以希一得之获。惟吾年差长，忧患频集，坐此不逮足下耳。然犬马之齿，三十有四，距强仁之日，尚复六年。上亦冀展尺寸之效，竭志力以报先人；下庶几垂竹帛之声，传姓名以无惭生我。每览子桓之论：＂日月逝于上，体貌衰于下，忽然与万物迁化。＂及长沙所述：＂佚游荒醉，生无益于时，死无闻于后，是自弃也。＂感此数语，掩卷而悲，并日而学。又佣力之暇，余晷尚富，疏野之质，本乏知交，鸡胶胶则随暗影以披衣，烛就跋则携素册以到枕。衣上落虱，多而不嫌；凝尘浮寇，日以积寸。非门外入刺，巷侧过车，不知所处在京邑之内，所居界公卿之间也。
夫人之智力有限，今世之士，或县心于贵势，或役志于高名，在人者款来，在已者已失。又或放情于博奕之趣，毕命于花鸟之研，劳瘁既同，岁月共尽。若此，皆巧者之失也。间常自思，使扬子云移研经之术以媚世，未必胜汉廷诸人，而坐废深沉之思。韦宏嗣舍著史之长以事棋，未必充吴国上选，而并忘渐渍之效。二子者，专其所独至，而弃其所不能，为足妒耳。每以自慰，亦惟敢告足下也。
"""
DEBUG = True
NUMBERS = u'１２３４５６７８９０'


class ParameterError(Exception):
    pass


class NotSupported(Exception):
    pass


def classical_chinese(text, word_num=None, line_num=None, whitespace=False, reverse=False):
    """ 古文-style 竖排输出

    现在的问题就是如果提供了 line_num 和 whitespace 两个参数就不行。

    :param text:       文言文
    :param word_num:   每列字数
    :param line_num:   列数
    :param whitespace: 是否允许换行
    :param reverse:    是否从左向右输出
    :return:           竖排输出的字符串
    """
    if word_num is None and line_num is None:
        raise ParameterError('Need one of word_num and line_num')

    if line_num is not None and whitespace:
        raise NotSupported('Not support whitespace parameter when use line_num mode')

    lines = []
    if whitespace:
        seq = [(i + u'　' * (word_num - len(i) % word_num)) for i in text.strip().split('\n')]
        seq = [j for i in seq for j in i]
    else:
        seq = [i for i in text if i.strip()]

    char_num = len(seq)
    if word_num is None:
        word_num = int(float(char_num) / float(line_num) + 0.5)

    for i in range(word_num):
        line = [seq[j] for j in range(i, char_num, word_num)]
        if reverse:
            line.reverse()
        lines.append(line)

    if DEBUG:
        lines.insert(0, [NUMBERS[i % 10] for i in range(len(lines[0]))])

    return '\n'.join([u'｜'.join(i) for i in lines])


classical_chinese(src)
try:
    classical_chinese(src)
except Exception as e:
    print e

# print classical_chinese(src, 15, whitespace=True, reverse=True)
# print classical_chinese(src, line_num=35, whitespace=True)
