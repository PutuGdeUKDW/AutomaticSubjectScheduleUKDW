from itertools import product

krs = {
'senin': [['KaKom-C',''],['JARNIR-A'],['PROGWEB-C','PROGWEB-D',''],['']],
'selasa':[['AI-C','AI-D',''],['RPLBO-C','RPLBO-D','AI-A','AI-B',''],['PROGWEB-A','PROGWEB-B','EtProf-C','EtProf-D',''],['']],
'rabu':[['PrRPLBO-C1','PrRPLBO-D1','KaKom-B',''],['PrPROGWEB-A','PrPROGWEB-B',''],['PP-H','PP-I','PrPROGWEB-C','PrPROGWEB-D',''],['']],
'kamis':[['KaKom-A','KaKom-D',''],[''],['PP-J','PP-K','EtProf-B',''],['']],
'jumat':[['PrRPLBO-C2','PrRPLBO-D2',''],[''],[''],['']]
    }

kombinasi_krs = [[],[],[],[],[]]
hari = ['senin','selasa','rabu','kamis','jumat']

for l in product(*krs['senin']):
    kombinasi_krs[0].append(list(l))

for l in product(*krs['selasa']):
    kombinasi_krs[1].append(list(l))

for l in product(*krs['rabu']):
    kombinasi_krs[2].append(list(l))

for l in product(*krs['kamis']):
    kombinasi_krs[3].append(list(l))

for l in product(*krs['jumat']):
    kombinasi_krs[4].append(list(l))

counter = 1
limit = 0

for i in product(*kombinasi_krs):
    i = list(i)
    lister = {}
    inval = []
    kelas = []
    for j in range(len(list(i))):
        for m in i[j]:
            if m != '':
                k = m.split('-')
                if k[0] not in lister:
                    lister[k[0]] = [k[1]]
                    kelas.append(m)
                else:
                    if k[1] not in lister[k[0]]:
                        lister[k[0]].append(k[1])
                        kelas.append(m) 
                    else:
                        inval.append(k[0])

    if len(lister) == 9 and len(inval) == 0 and counter != 50:
        print(lister)
        print(kelas)
        count = 0
        for jadi in i:
            print(hari[count])
            print('Sesi 1: '+jadi[0])
            print('Sesi 2: '+jadi[1])
            print('Sesi 3: '+jadi[2])
            print('Sesi 4: '+jadi[3])
            count +=1
        counter +=1
        print('\n')

