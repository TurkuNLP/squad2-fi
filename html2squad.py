import bs4
from bs4 import BeautifulSoup

# colors from palette.txt for easier access
colors = ['#696969','#a9a9a9','#dcdcdc','#2f4f4f','#556b2f','#6b8e23','#a0522d','#228b22','#191970','#8b0000','#483d8b','#3cb371','#bc8f8f','#663399','#008080','#bdb76b','#4682b4','#d2691e','#9acd32','#cd5c5c','#00008b','#32cd32','#daa520','#7f007f','#8fbc8f','#b03060','#66cdaa','#9932cc','#ff4500','#00ced1','#ff8c00','#ffd700','#c71585','#0000cd','#deb887','#00ff00','#00ff7f','#4169e1','#e9967a','#dc143c','#00ffff','#00bfff','#f4a460','#9370db','#0000ff','#a020f0','#adff2f','#ff6347','#da70d6','#d8bfd8','#ff00ff','#db7093','#f0e68c','#ffff54','#6495ed','#dda0dd','#90ee90','#87ceeb','#ff1493','#afeeee','#7fffd4','#ff69b4','#ffe4c4','#ffb6c1']


def is_bu(elem): #is this a bold_underline?
    return len(list(elem.select("u > b")))>0 or len(list(elem.select("b > u")))>0

def is_b(elem): #is this bold?
    return len(list(elem.select("b")))>0

def is_tag(elem):
    return isinstance(elem,bs4.Tag)

with open('squad2-fi-raw/html/squad2_000 fi.html', 'r') as file:
    soup = BeautifulSoup(file,'html.parser')
    for elem in soup.body.children:
        if not is_tag(elem):
            continue
        
        # Get the document ID's
        if is_bu(elem):
            doc = elem.get_text()
            doc_id = ''.join([i for i in doc.split() if i.isdigit()])
            print('DOC_ID ' + doc_id)
            continue
        
        # Get the answers
        if is_b(elem) and "numero" in elem.get_text():
            para_id = elem.get_text()
            para_id = ''.join([i for i in para_id.split() if i.isdigit()])
            print('PARA_ID ' + para_id)
            para = elem.find_next("p")
            para_text = para.get_text() # paragraph plain text
            for tag in para.find_all("font"):
                if tag.get("color") is not None: # Skip tags with other attributes
                    ans = tag.get_text().replace("\n", " ")
                    color = tag['color']
                    color_idx = colors.index(color) # Matches the idx in meta.jsonl
                    print(color_idx, color, ans)
            continue
        
        # Get questions
        if is_b(elem) and "Kysymys" in elem.get_text():
            question = elem.find_next("p").get_text().replace("\n", " ")
            print(elem.getText(),question)
            continue

