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
