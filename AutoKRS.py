from itertools import product



krs = {
'senin': [['',''],[''],[''],['']],
'selasa':[[''],[''],[''],['']],
'rabu':[[''],[''],[''],['']],
'kamis':[[''],[''],[''],['']],
'jumat':[[''],[''],[''],['']]
    }

kombinasi_krs = []
hari = {'senin': 0, 'selasa': 1, 'rabu': 2, 'kamis': 3, 'jumat': 4}

for day in krs:
    combos = []
    for l in product(*krs[day]):
        combos.append(list(l))
    kombinasi_krs.append(combos)


counter = 1
for i in product(*kombinasi_krs):
    i = list(i)
    lister = {}
    inval = []
    kelas = []
    for j in range(len(list(i))):
        for m in i[j]:
            if m != '':
                k = m.split('-')
                if any(ava == k[0] for ava in lister) == False:
                    lister[k[0]] = k[1][0]
                    kelas.append(m)
                else:
                    if lister[k[0]] != k[1][0]:
                        inval.append(k[0])
                    else:
                        kelas.append(m)
                        
    if len(lister) == 9 and len(inval) == 0 and counter != 50 and len(kelas) == 10:
        print(lister)
        #print(kelas)
        count = 0
        for jadi in i:
            print(list(krs.keys())[count])
            print('Sesi 1: '+jadi[0])
            print('Sesi 2: '+jadi[1])
            print('Sesi 3: '+jadi[2])
            print('Sesi 4: '+jadi[3])
            count +=1
        counter +=1
        print('\n')
