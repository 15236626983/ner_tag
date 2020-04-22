import json
import os

from imutils import paths


# 将tmp.txt中文章中内容写入到文本
def tmp_to_file_part(file_num, part_num):
    content = ""
    with open("./tmp.txt", "r", encoding="utf-8") as f:
        list = f.readlines()
        content = "".join(list).replace("\n", "")
        print(content)
    if not os.path.exists(f"{file_num}"):
        os.makedirs(f"{file_num}")
    with open(f"./{file_num}/part_{part_num}.txt", "w", encoding="utf-8") as f:
        f.write(content)


# 获取以标注的文章标题，并写入tagged.txt
def get_all_tagged_tittle():
    with open(f'tagged.txt', 'w', encoding="utf-8") as f:
        for file in paths.list_files('.', validExts=('.json',)):
            j = json.load(open(file, 'r', encoding='utf-8'))
            f.write(j['name'] + '\n')
    pass


# 检测标题是否冗余,冗余返回false
def get_tagged_tittle():
    with open(f'tagged.txt', 'r', encoding="utf-8") as f:
        lines=f.readlines()
        lines = [i.strip() for i in lines]
        return lines


if __name__ == '__main__':
    get_all_tagged_tittle()
    _id = 2016 # 文章id
    part_num = 1  # 文章部分号
    tmp_to_file_part(_id, part_num)
    if (part_num == 1):
        name = '人工智能如何影响军事发展？'  # 标题
        lines=get_tagged_tittle()
        if name in lines:
            exit(0) #重复直接退出，不会生成json文件
        publisher = '每日军榜'
        url = 'https://new.qq.com/omn/20180421/20180421G04MSM.html'
        keywords = ''
        date = '20180421'  # 日期
        country = '中国'  # 国家
        data = {
            'id': _id,
            'name': name,
            'src': {'publisher': publisher,
                    'url': url},
            'date': date,
            "country": country,
            "field": "Military AI",
            'keywords': keywords
        }
        with open(f'{_id}/{_id}.json', 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

