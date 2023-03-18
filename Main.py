from AutoKRS import AutoKRS

title = "AUTO KRS SCHEDULER"
top_bottom_border = "#" * 50
spaces_needed = (50 - len(title)) // 2
title_card = ""
for i in range(7):
    if i == 0 or i == 7 - 1:
        title_card += "{}\n".format(top_bottom_border)
    elif i == 7 // 2:
        title_card += "#{}{}{}#\n".format(" " * spaces_needed, title, " " * (50 - spaces_needed - len(title) - 2))
    else:
        title_card += "#{}#\n".format(" " * (50 - 2))
        
# Print the title card
print(title_card)

krs_raw = {
'senin': [[''],[''],[''],['']],
'selasa':[[''],[''],[''],['']],
'rabu':[[''],[''],[''],['']],
'kamis':[[''],[''],[''],['']],
'jumat':[[''],[''],[''],['']]
    }


krs = AutoKRS(krs_raw)
wishing = ['KaKom','PrPROGWEB','PROGWEB','RPLBO-A','PrRPLBO-A','PP','EtProf','AI']
krs.krs_iterator('krs.json')
print("==================================")
krs.print_krs('krs.json',wishing)
