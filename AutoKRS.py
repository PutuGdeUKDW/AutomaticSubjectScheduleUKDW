import json

class AutoKRS:
    def __init__(self, krs_raw):
        self.krs_raw = krs_raw
        self.krs = self.combinator(self.krs_raw)
    
    def generate_combinations(self, lst, current=[], index=0):
        if index == len(lst):
            yield current
        else:
            for element in lst[index]:
                new_current = current + [element]
                yield from self.generate_combinations(lst, new_current, index+1)

    def combinator(self,krs):
        kombinasi_krs = []

        for day in krs:
            combos = []
            for l in self.generate_combinations(krs[day]):
                combos.append(list(l))
            kombinasi_krs.append(combos)
        return kombinasi_krs

    def krs_iterator(self, filename):
        counter = 1
        krs_data=[]
        for i in self.generate_combinations(self.krs):
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

            #if len(lister) == 9 and len(inval) == 0 and len(kelas) == 10:
            if len(inval) == 0 :
                krs_item = {}
                krs_item['counter'] = counter
                krs_item['schedule'] = lister
                krs_item['class_tot'] = len(kelas)
                krs_item['day_schedule'] = []
                count = 0
                day = ['Senin','Selasa','Rabu','Kamis','Jumat']
                for jadi in i:
                    day_schedule = {}
                    day_schedule['day'] = day[count]
                    day_schedule['sesi_1'] = jadi[0]
                    day_schedule['sesi_2'] = jadi[1]
                    day_schedule['sesi_3'] = jadi[2]
                    day_schedule['sesi_4'] = jadi[3]
                    krs_item['day_schedule'].append(day_schedule)
                    count +=1
                krs_data.append(krs_item)
                counter +=1

        with open(filename, 'w') as file:
            json.dump(krs_data, file)

    def load_krs(self,filename):
        with open(filename, 'r') as file:
            krs_data = json.load(file)
        return krs_data
    
    def print_krs(self,json_location):
        krs_data = self.load_krs(json_location)
        counter = 1

        for krs_schedule in krs_data:
            
            if len(krs_schedule['schedule']) == 9 and krs_schedule['class_tot'] == 10:
                print(str(counter)+'. KRS Schedule #{}'.format(krs_schedule['counter']))
                print('------------------------')
                for day_schedule in krs_schedule['day_schedule']:
                    print('{}:'.format(day_schedule['day']))
                    print('  Sesi 1: {}'.format(day_schedule['sesi_1']))
                    print('  Sesi 2: {}'.format(day_schedule['sesi_2']))
                    print('  Sesi 3: {}'.format(day_schedule['sesi_3']))
                    print('  Sesi 4: {}'.format(day_schedule['sesi_4']))
                print('------------------------\n')
                counter +=1

krs_raw = {
'senin': [[''],[''],[''],['']],
'selasa':[[''],[''],[''],['']],
'rabu':[[''],[''],[''],['']],
'kamis':[[''],[''],[''],['']],
'jumat':[[''],[''],[''],['']]
    }

krs = AutoKRS(krs_raw)
krs.krs_iterator('krs.json')
krs.print_krs('krs.json')
