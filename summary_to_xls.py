import collections
import os
from datetime import datetime
from pathlib import Path

import xlwt
from imutils import paths
from nltk import pos_tag, conlltags2tree, Tree


def stanford_tree(bio_tagged):
    tokens, ne_tags = zip(*bio_tagged)
    pos_tags = [pos for token, pos in pos_tag(tokens)]

    conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
    ne_tree = conlltags2tree(conlltags)
    return ne_tree


def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = "".join([token for token, pos in subtree.leaves()])
            # ne.append((ne_string, ne_label))
            ne.append((ne_label, ne_string))
    return ne


def stats(src,xlx_name):
    ai_tec = set()
    ai_product = set()
    ai_program = set()
    Org = set()
    # today = datetime.today().strftime('%Y%m%d')
    today='summary'
    for file in paths.list_files(src, validExts=('.anns',)):
        with open(file, encoding='utf-8') as f:
            bio_tagged = []
            for i, line in enumerate(f):
                tup = line.split()
                if len(tup) != 2: continue
                bio_tagged.append(tup)
            nes = structure_ne(stanford_tree(bio_tagged))

            # 统计每篇文档实体的字典
            entity_dic = collections.defaultdict(set)
            for label, entity in nes:
                entity_dic[label].add(entity)

            dst = os.path.sep.join([today, file.split(os.sep)[-2]])
            if not os.path.exists(dst):
                os.makedirs(dst)

            ai_tec.update(entity_dic['ai_tec'])
            ai_product.update(entity_dic['ai_product'])
            ai_program.update(entity_dic['ai_program'])
            Org.update(entity_dic['Org'])

            for key, items in entity_dic.items():
                path = Path(dst, f'{key}.txt')
                with open(path, 'w', encoding='utf-8') as fd:
                    for item in sorted(items):
                        fd.write(item)
                        fd.write('\n')

    with open(today + '/' + 'ai_tec.txt', 'w', encoding='utf-8') as f1:
        for item in sorted(ai_tec):
            f1.write(item)
            f1.write('\n')
    with open(today + '/' + 'ai_product.txt', 'w', encoding='utf-8') as f1:
        for item in sorted(ai_product):
            f1.write(item)
            f1.write('\n')
    with open(today + '/' + 'ai_program.txt', 'w', encoding='utf-8') as f1:
        for item in sorted(ai_program):
            f1.write(item)
            f1.write('\n')
    with open(today + '/' + 'Org.txt', 'w', encoding='utf-8') as f1:
        for item in sorted(Org):
            f1.write(item)
            f1.write('\n')

    row0 = ["ai_tec", "ai_product", "ai_program", "Org"]
    colum0 = [item for item in sorted(ai_tec)]
    colum1 = [item for item in sorted(ai_product)]
    colum2 = [item for item in sorted(ai_program)]
    colum3 = [item for item in sorted(Org)]

    f = xlwt.Workbook(encoding = 'utf-8')
    sheet1 = f.add_sheet(xlx_name, cell_overwrite_ok=True)
    # 写
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(colum0)):
        sheet1.write(i + 1, 0, colum0[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(colum1)):
        sheet1.write(i + 1, 1, colum1[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(colum2)):
        sheet1.write(i + 1, 2, colum2[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(colum3)):
        sheet1.write(i + 1, 3, colum3[i], set_style('Times New Roman', 220, True))
    f.save(f'{xlx_name}.xls')

    print(f'amount ai_tec = {len(ai_tec)}')
    print(f'amount ai_product = {len(ai_product)}')
    print(f'amount ai_program = {len(ai_program)}')
    print(f'amount Org = {len(Org)}')
    print(f'amount = {len(ai_tec) + len(ai_product) + len(ai_program) + len(Org)}')


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


if __name__ == '__main__':
    print('===========cntag=============')
    stats('./cntag','cntag')
    print('===========entag=============')
    stats('./entag','entag')
