import bs4
from bs4 import BeautifulSoup
import jsonlines
from pathlib import Path

# colors from palette.txt for easier access
colors = ['#696969','#a9a9a9','#dcdcdc','#2f4f4f','#556b2f','#6b8e23','#a0522d','#228b22','#191970','#8b0000','#483d8b','#3cb371','#bc8f8f','#663399','#008080','#bdb76b','#4682b4','#d2691e','#9acd32','#cd5c5c','#00008b','#32cd32','#daa520','#7f007f','#8fbc8f','#b03060','#66cdaa','#9932cc','#ff4500','#00ced1','#ff8c00','#ffd700','#c71585','#0000cd','#deb887','#00ff00','#00ff7f','#4169e1','#e9967a','#dc143c','#00ffff','#00bfff','#f4a460','#9370db','#0000ff','#a020f0','#adff2f','#ff6347','#da70d6','#d8bfd8','#ff00ff','#db7093','#f0e68c','#ffff54','#6495ed','#dda0dd','#90ee90','#87ceeb','#ff1493','#afeeee','#7fffd4','#ff69b4','#ffe4c4','#ffb6c1']


def is_bu(elem): #is this a bold_underline?
    return len(list(elem.select("u > b")))>0 or len(list(elem.select("b > u")))>0

def is_b(elem): #is this bold?
    return len(list(elem.select("b")))>0

def is_tag(elem):
    return isinstance(elem,bs4.Tag)

def get_answer(tag):
    ans = tag.get_text().replace("\n", " ")
    return ans

"""
Get location of each <font> tag in paragraph and then subtract index * 29 from
each (font tag has 29 characters in total) to fix the offset caused by the
tags themselves.
"""
def get_ans_pos(para, colors):
    positions = []
    para = str(para)
    # These all mess up the indexing
    para = para.replace("&amp;", " ").replace('&lt;', " ").replace('&gt;', " ")
    para = para.replace('<font face="ＭＳ 明朝">', "") # Chinese text tag
    para = para.replace('</font>', "") # Replace all closing font tags
    para = para.replace('<font face=""><span lang="ar-SA">', "").replace('</span>', "")
    para = para.replace('<br/>', "") # line break
    # print(para) # print the whole paragraph with tags to make sense of this all
    font_tag = 22 # Length of the opening font tag
    color_start = 13 # Length from the color to the start of the font tag
    p_tag = 33 # length of the p tag in the start of the string
    tags_len = color_start + p_tag
    for i,color in enumerate(colors):
        # Get the positions of the answers in plain text paragraphs
        index = para.find(color)-font_tag*i-tags_len
        para = para.replace(color,'#######',1)
        positions.append(index)
    return positions

json_ids = []
json_qas = []
counter = 0
with jsonlines.open('squad2-en/meta.jsonl', 'r') as squad:
    lines = [obj for obj in squad]
    for title in lines:
        for para in title["paragraphs"]:
            for question in para[2]:
                json_ids.append(question)

    for title in lines:
        for para in title["paragraphs"]:
            for id,color in para[1].items():
                if color == -1:
                    pass
                elif '+' in id:
                    id_list = id.split('+')
                    for id in id_list:
                        ques, ans = id.split('_')
                        json_qas.append([ques,int(ans),color])
                else:
                    ques, ans = id.split('_')
                    json_qas.append([ques,int(ans),color])


for file in sorted(Path('squad2-fi-raw/html/').glob('*.html')):
    with open(file, 'r') as file:
        soup = BeautifulSoup(file,'html.parser')
        questions = []

        for elem in soup.body.children:
            if not is_tag(elem):
                continue
            
            # Get the document ID's
            if is_bu(elem):
                doc_id = ''.join([i for i in elem.get_text().split() if i.isdigit()])
                continue
            
            # Get the answers
            if is_b(elem) and "numero" in elem.get_text():
                questions = []
                para_id = ''.join([i for i in elem.get_text().split() if i.isdigit()])
                print()
                print()
                para = elem.find_next("p")
                para_text = para.get_text().replace("\n", " ")
                ans_colors = []
                color_ids = []
                answers = []
                answer_pos = []
                for tag in para("font"):
                    # Replace non-answer font-tags with plain text
                    if tag.get("color") is None:
                        tag = tag.get_text()
                    else:
                        color = tag['color']
                        color_ids.append(colors.index(color)) # = color id in meta.jsonl
                        answers.append(get_answer(tag))
                        ans_colors.append(color)
                        answer_pos = get_ans_pos(para, ans_colors)
                print(doc_id,para_id,para_text)
                print(doc_id,para_id,ans_colors)
                print(doc_id,para_id,color_ids)
                print(doc_id,para_id,answer_pos)
                print(doc_id,para_id,answers)
                continue
            
            # Get questions
            if is_b(elem) and "Kysymys" in elem.get_text():
                answer = elem.find_next("p").get_text().replace("\n", " ")
                qa_pair = []
                for qa in json_qas:
                    if qa[0] == json_ids[counter]:
                        for i,color in enumerate(color_ids):
                            if qa[2] == color_ids[i]:
                                word = answers[i]
                                pos = answer_pos[i]
                                qa_pair.append([qa[1],pos, word])
                questions.append(elem.find_next("p").get_text().replace("\n", " "))
                print(doc_id,para_id,json_ids[counter],answer,sorted(qa_pair))
                counter += 1
