import re

with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all CMK ranges in the file
cmk_in_html = set(re.findall(r'makale-cmk-(\d+-\d+)\.html', content))

# All 48 CMK ranges that should be there
all_cmk = ['3-7', '8-11', '12-21', '22-32', '33-38', '39-42', '43-61', '62-73', '74-89', '90-99', 
           '100-108', '109-115', '116-134', '135-138', '139-140', '141-144', '145-146', '147-148', 
           '149-156', '157-159', '160-169', '170-171', '172-174', '175-181', '182-202', '203-205', 
           '206-218', '219-222', '223-225', '226-226', '227-232', '233-236', '237-243', '244-246', 
           '247-248', '249-249', '250-252', '253-255', '256-259', '260-266', '267-271', '272-285', 
           '286-307', '308-308', '309-310', '311-323', '324-330', '331-335']

missing = [r for r in all_cmk if r not in cmk_in_html]

print(f"CMK in HTML: {len(cmk_in_html)}")
print(f"Missing: {len(missing)}")
print("Missing ranges:", missing)
