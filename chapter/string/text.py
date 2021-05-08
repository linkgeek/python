import re

line = "tiny4k.melody.marks.naughty.school.girl[N1C]"
pattern = r"melody.marks"
m = re.search(pattern, line)
print(m, '\n')


pattern = r"Melody Marks"
m = re.search(pattern, line)
print(m, '\n')

patt = r'melody,marks'
pattern = re.compile(patt)
result = pattern.findall(line)
print(result, '\n')

# search_str = 'YMDD-199,HR-001,HR-002'
search_str = 'YMDD-199'
_title = 'YMDD-199 新村あかり'
if _title.find(search_str) >= 0:
    print('ok')
else:
    print('no')

# 替换关键字
def check_filter(keywords, text):
    return re.sub("|".join(keywords), "***", text)


keywords = ("暴力", "色情", "其他关键字", "YMDD", "Melody Marks")
text = "Y5MDD-199 这句话里不包含暴1力，也不包含色1情，但是可能包含其他关键6字Melodymelody marks"
#print(check_filter(keywords, text))
print(re.search("|".join(keywords), text, re.M|re.I), bool(re.search("|".join(keywords), text, re.M|re.I)))
