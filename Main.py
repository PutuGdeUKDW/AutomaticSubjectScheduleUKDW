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
'senin': [['KaKom-C',''],['RPLBO-A','RPLBO-B',''],['PROGWEB-C','PROGWEB-D',''],['']],
'selasa':[['PrRPLBO-A1','PrRPLBO-B1','AI-C','AI-D',''],['RPLBO-C','RPLBO-D','AI-A','AI-B',''],['PROGWEB-A','PROGWEB-B','EtProf-C','EtProf-D',''],['']],
'rabu':[['PrRPLBO-C1','PrRPLBO-D1','KaKom-B',''],['PrPROGWEB-A','PrPROGWEB-B',''],['PP-H','PP-I','PrPROGWEB-C','PrPROGWEB-D',''],['']],
'kamis':[['KaKom-A','KaKom-D',''],['PrRPLBO-A2','PrRPLBO-B2',''],['PP-J','PP-K','EtProf-B',''],['']],
'jumat':[['PrRPLBO-C2','PrRPLBO-D2',''],[''],[''],['']]
    }


krs = AutoKRS(krs_raw)
wishing = ['KaKom','PrPROGWEB','PROGWEB','RPLBO-A','PrRPLBO-A','PP','EtProf','AI']
krs.krs_iterator('krs.json')
print("==================================")
krs.print_krs('krs.json',wishing)