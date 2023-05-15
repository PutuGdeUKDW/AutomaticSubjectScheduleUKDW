import json
from tqdm import tqdm
import PyPDF2
import os
import tabula
import csv
import re

class AutoKRS:
    def __init__(self, krs_raw):
        """
        Initializes the object.

        Parameters:
        krs_raw {dict}: Dictionary of the form {day: [list of classes]}
        that contain the available classes for each days.

        Returns:
        None
        """

        self.krs_raw = krs_raw
        self.krs = self.combinator(self.krs_raw)

    def generate_combinations(self, lst, current=[], index=0):
        """
        Generate all possible combinations of the classes

        Parameters:
        lst [list]: Lists inside of a list that contain all available classes for each day.
        current [list]: Empty by default. List of classes that have been generated so far.
        index (int): 0 by default. The current index in the lst that is being iterated.

        Returns:
        Generator that yields all possible combinations of classes for the day.
        """

        if index == len(lst):
            yield current
        else:
            for element in lst[index]:
                new_current = current + [element]
                yield from self.generate_combinations(lst, new_current, index+1)

    def combinator(self, krs):
        """
        Generates all possible schedules from the available classes for each day.

        Parameters:
        krs {dict}: Dictionary of the form {day: [list of classes]}
        that contain the available classes for each days.

        Returns:
        All possible schedules inside a list.

        """

        kombinasi_krs = []
        for day in krs:
            combos = []
            for l in self.generate_combinations(krs[day]):
                combos.append(list(l))
            kombinasi_krs.append(combos)
        return kombinasi_krs

    def krs_iterator(self, filename, subjects_count):
        """
        Iterates over all possible schedules and saves it to a JSON file.

        Parameters:
        filename (string): The name of the JSON file for saving the generated schedules.

        Returns:
        None
        """

        counter = 1
        krs_data = []
        for i in tqdm(self.generate_combinations(self.krs)):
            i = list(i)
            lister = {}
            kelas = []
            inval = False
            for j in range(len(list(i))):
                for m in i[j]:
                    if m != '':
                        k = m.split('-')
                        if any(ava == k[0] for ava in lister) == False:
                            lister[k[0]] = k[1][0]
                            kelas.append(m)
                        else:
                            if lister[k[0]] != k[1][0]:
                                inval = True
                                break
                            else:
                                kelas.append(m)
                if inval:
                    break
            if inval:
                continue

            if len(kelas) >= subjects_count:
                krs_item = {}
                krs_item['counter'] = counter
                krs_item['schedule'] = lister
                krs_item['class_tot'] = len(kelas)
                krs_item['day_schedule'] = []
                count = 0
                day = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
                for jadi in i:
                    day_schedule = {}
                    day_schedule['day'] = day[count]
                    day_schedule['sesi_1'] = jadi[0]
                    day_schedule['sesi_2'] = jadi[1]
                    day_schedule['sesi_3'] = jadi[2]
                    day_schedule['sesi_4'] = jadi[3]
                    krs_item['day_schedule'].append(day_schedule)
                    count += 1
                krs_data.append(krs_item)
                counter += 1

        print("SAVING SCHEDULES ITERATIONS")
        with open(filename, 'w') as file:
            json.dump(krs_data, file)
        print("COMPLETE")

    def load_krs(self, filename):
        """
        Loads the schedules from the save files that are a JSON format.

        Parameters:
        filename (string): The name of the JSON file to load the schedule from.

        Returns:
        A list of schedules.

        """

        with open(filename, 'r') as file:
            krs_data = json.load(file)
        return krs_data

    def hitung_pertemuan(self, kelas):
        """
        Count the total number of meetings from the given list of classes.

        Parameters:
        kelas [list]: A list of the desired classes.

        Returns:
        The total number of meetings.
        """

        jumlah = len(kelas)
        for i in kelas:
            if i[:2] == 'Pr':
                while True:
                    tempe = str(
                        input(f"Apakah {i} ada 2(dua) pertemuan perminggu (y/n)? "))
                    if tempe == 'y':
                        jumlah += 1
                        break
                    elif tempe == 'n':
                        break
        return jumlah

    def print_krs(self, json_location, wishlist):
        """
        Filter and prints the schedules that meet the criteria specified in the wishlist.

        Parameters:
        json_location (string): The name of the JSON file containing the schedules.
        wishlist [list]: A list of classes that must be in the schedule.

        Returns:
        None
        """
        krs_data = self.load_krs(json_location)
        counter = 1
        jumlah_kel = self.hitung_pertemuan(wishlist)
        for krs_schedule in krs_data:
            mek = len(wishlist)
            for i in wishlist:
                j = i.split('-')
                if j[-1] == j[0]:
                    if j[0] in krs_schedule['schedule']:
                        mek -= 1
                else:
                    if j[0] in krs_schedule['schedule']:
                        if krs_schedule['schedule'][j[0]] == j[1][0]:
                            mek -= 1
            if len(krs_schedule['schedule']) == len(wishlist) and krs_schedule['class_tot'] == jumlah_kel and mek == 0:
                print(str(counter) +
                      '. KRS Schedule #{}'.format(krs_schedule['counter']))
                print('------------------------')
                for day_schedule in krs_schedule['day_schedule']:
                    print('{}:'.format(day_schedule['day']))
                    print('  Sesi 1: {}'.format(day_schedule['sesi_1']))
                    print('  Sesi 2: {}'.format(day_schedule['sesi_2']))
                    print('  Sesi 3: {}'.format(day_schedule['sesi_3']))
                    print('  Sesi 4: {}'.format(day_schedule['sesi_4']))
                print('------------------------\n')
                counter += 1
        if counter == 1:
            print('\n===Kelas Tidak Ditemukan, coba ganti kelas===')


class UserProfile:
    def __init__(self):
        self.usr_profile = []
        self.usr_grades = {"MPBP": {}, "MPWP": {}, "WAJIB": {}}
        self.usr_GPAinfo = {"Tot_SKS": 0, "Tot_AK": 0.0,
                            "Tot_IPK": 0.0, "IPS_Terakhir": 0.00}
        self.usr_AS = AcademicSubjects(self)

    def getUsrSKSTempuh(self):
        return self.usr_GPAinfo["Tot_SKS"]

    def getUsrAngkaKualitas(self):
        return self.usr_GPAinfo["Tot_AK"]

    def getUsrIPK(self):
        return self.usr_GPAinfo["Tot_IPK"]

    def getUsrIPS(self):
        return self.usr_GPAinfo["IPS_Terakhir"]

    def getUsrProfile(self):
        return self.usr_profile
    
    def getUsrGrades(self):
        return self.usr_grades

    def readGradeTranscript(self, pdfName):
        if not os.path.exists(pdfName):
            print(f"File '{pdfName}' not found.")
            return

        with open(pdfName, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page_obj = pdf_reader.pages[page_num]
                page_text = page_obj.extract_text()
                lines = page_text.splitlines()
                grade_check = False

                counter = 0
                profile = ""
                for line in lines:
                    # print(line)
                    if len(self.usr_profile) < 4:
                        line = line.split(":")

                        if 'No. Mahasiswa' in line[0]:
                            self.usr_profile.append(line[1])
                        elif 'Nama' in line[0]:
                            self.usr_profile.append(line[1][:-10])
                            self.usr_profile.append(line[2])
                        elif 'Program' in line[0]:
                            self.usr_profile.append(line[1])
                        counter += 1
                        continue
                    if "Matakuliah Wajib" in line:
                        profile = "WAJIB"
                        grade_check = True
                        counter += 1
                        continue
                    elif "Matakuliah Pilihan Bebas Prodi" in line:
                        profile = "MPBP"
                        grade_check = True
                        counter += 1
                        continue

                    elif "Matakuliah Pilihan Wajib Profil" in line:
                        profile = "MPWP"
                        grade_check = True
                        counter += 1
                        continue

                    if "Total SKS" in line:
                        sks = line.split(":")
                        self.usr_GPAinfo["Tot_SKS"] = int(sks[-1])
                        grade_check = False
                        continue
                    elif "Total Angka Kualitas" in line:
                        sks = line.split(":")
                        self.usr_GPAinfo["Tot_AK"] = float(sks[-1])
                    elif "IP Kumulatif" in line:
                        sks = line.split(":")
                        self.usr_GPAinfo["Tot_IPK"] = float(sks[-1])

                    if grade_check == True:
                        if "Matakuliah Wajib" in line or "Matakuliah Pilihan Bebas Prodi" in line or " Matakuliah Pilihan Wajib Profil" in line:
                            counter += 1
                            continue

                        subject = line.split(" ")
                        if len(subject[-1]) > 2:
                            if subject[-1] == "SKSNILAI":
                                subject_name = " ".join(subject[1:-3])
                                jum_sks = subject[-3][0]
                                grade = subject[-3][1]+subject[-3][2]
                            else:
                                subject_name = " ".join(subject[1:-1])
                                jum_sks = subject[-1][0]
                                grade = subject[-1][1]+subject[-1][2]

                        else:
                            subject_name = " ".join(subject[1:-1])
                            jum_sks = subject[-1][0]
                            grade = subject[-1][1]

                        if not jum_sks.isdigit():
                            next_line = lines[counter+1]
                            if next_line[-1] == "-" or next_line[-1] == "+":
                                jum_sks = next_line[-3]
                                grade = next_line[-2]+next_line[-1]
                                subject_name = subject_name+" "+next_line[0:-3]
                            else:
                                jum_sks = next_line[-2]
                                grade = next_line[-1]
                                subject_name = subject_name+" " + \
                                    subject[-1]+" "+next_line[0:-2]

                        if subject[0][0:2].isdigit():
                            self.usr_grades[profile][subject[0][2::]] = [
                                subject_name, int(jum_sks), grade]
                        elif subject[0][0:1].isdigit():
                            self.usr_grades[profile][subject[0][1::]] = [
                                subject_name, int(jum_sks), grade]
                        elif subject[0][0].isdigit():
                            self.usr_grades[profile][subject[0][0::]] = [
                                subject_name, int(jum_sks), grade]
                    counter += 1

    def readKHSTransript(self, pdfName):
        if not os.path.exists(pdfName):
            print(f"File '{pdfName}' not found.")
            return False

        with open(pdfName, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page_obj = pdf_reader.pages[page_num]
                page_text = page_obj.extract_text()
                lines = page_text.splitlines()

                for line in lines:
                    # print(line)
                    if "IP Semester" in line:
                        SGPa = line.split(" ")
                        self.usr_GPAinfo["IPS_Terakhir"] = float(SGPa[-3])


class AcademicSubjects:
    def __init__(self, profile):
        self.usr_profile = profile
        self.usr_maksSKS = 24
        self.jadwal = None

    def getMaksSKS(self):
        IPK_usr = self.getTableAddress(self.usr_profile.getUsrIPK())
        IPS_usr = self.getTableAddress(self.usr_profile.getUsrIPS())

        sks_maks = min(24, 15+IPK_usr+IPS_usr)
        self.usr_maksSKS = sks_maks
        return sks_maks

    def getTableAddress(self, input):
        index_adress = [(3.7, 9), (3.3, 8), (3.0, 7), (2.7, 6), (2.3, 5), (2.0, 4), 
                        (1.7, 3), (1.3, 2), (1.0, 1), (0.0, 0)]
        for ipk_ips, adress in index_adress:
            if input >= ipk_ips:
                return adress
        return 0

    def readSchedule(self,pdf_path,csv_path):
        tabula.convert_into(pdf_path, csv_path, output_format="csv", pages="all")
        Jadwal = []
        with open(csv_path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                Jadwal.append(row)

        JSeninSelasa = []
        JRabuKamis = []
        JJumat = []
        A = 1
        B = 0
        JadwalAwal = []
        AkhirSesi = 0
        Indek = 0
        for i in Jadwal :
            if len(JSeninSelasa) > 0 :
                Indek += 1
            if i[0] == "08:30" or "07:30" :
            
                if A == 1 :
                    if len(JSeninSelasa) > 1 :
                        if i[0] == '07:30' :
                            B += 1
                            A += 1 
                            JRabuKamis.append(i)
                            continue
                        elif i[0] == '08:30':
                            B += 1
                            A += 1 
                            JRabuKamis.append(i)
                            continue

                    JSeninSelasa.append(i)
                elif A == 2 :
                    if len(JRabuKamis) > 1 :
                        if i[0] == '07:30' :
                            
                            B += 1
                            A += 1 
                            continue
                        elif i[0] == '08:30':
                            B += 1
                            A += 1 
                            continue
                    JRabuKamis.append(i)
                elif A == 3 :
                    if i[0] != '07:30' :
                        continue
                    else : 
                        A += 1
                if A == 4 :
                    if len(JJumat) > 1 :
                        if i[0] == "16:30" :
                            AkhirSesi += 1
                        if AkhirSesi == 1 and i[0] == "Smstr_X" :
                            JJumat.append(i)
                            JJumat.append(Jadwal[Indek+1])
                            break      
                    JJumat.append(i)


        JadwalAwal.append(JSeninSelasa)
        JadwalAwal.append(JRabuKamis)

        JadwalMingguan = []
        for daftar in JadwalAwal :
            if len(daftar[0]) == 12 :
                hari1 = []
                hari2 = []
                sementaraHari1 = []
                sementaraHari2 = []
                for i in daftar :
                    a = 0
                    if len(sementaraHari1) == 6 :
                        hari1.append(sementaraHari1)
                        hari2.append(sementaraHari2)

                    for j in i :
                        if len(sementaraHari2) == 6 :
                            sementaraHari1 = []
                            sementaraHari2 = []
                        if a <= 5 :
                            if j.isdigit() : 
                                sementaraHari1.append("")
                            else :
                                sementaraHari1.append(j)
                            a = a + 1
                        elif a >= 6 :
                            if j.isdigit() :
                                sementaraHari2.append("")
                            else :
                                sementaraHari2.append(j)
                            a = a + 1
                        
                a = []
                for i in range(6,12) :
                    a.append(daftar[-1][i])
                hari2.append(a)
                a = []
                for i in range(0,6) :
                    a.append(daftar[-1][i])
                hari1.append(a)
                JadwalMingguan.append(hari1)
                JadwalMingguan.append(hari2)

        JadwalAkhir = {}
        IndekHari = 1
        for hari in JadwalMingguan :
            hasil = []
            Sesi = {}
            smt = 0
            semester = []   
            while len(hasil) != 4 :  
                for i in range(len(hari)) :
                    if len(hasil) == 4 :
                        break
                    if hari[smt][0] != "Smstr_X" :
                        semester.append(hari[smt])
                        smt += 1
                    else :
                        semester.append(hari[smt])
                        if (smt+1) < len(hari) :
                            if hari[smt+1][0] == '' :
                                semester.append(hari[smt+1])
                                hari.remove(hari[smt+1])
                                smt += 1
                                hasil.append(semester)
                                semester = []
                        if semester != [] :
                            if semester[-1] == semester[-2] :
                                del semester[-1]
                                hasil.append(semester)
                                semester = []   
                                break   
            for i in hasil :
                Sesi[i[0][0]] = {}
                if len(i) == 13 :
                    Sesi[i[0][0]] = {}
                    sems1or2 = [[i[1][1],  i[3][1]],  [i[1][2],i[3][2]],   [i[1][3],i[3][3]],   [i[1][4],i[3][4]],    [i[1][5],  i[3][5]]]
                    sems3or4 = [[i[4][1],  i[6][1]],  [i[4][2],i[6][2]],   [i[4][3],i[6][3]],   [i[4][4],i[6][4]],    [i[4][5],  i[6][5]]]
                    sems5or6 = [[i[7][1],  i[9][1]],  [i[7][2],i[9][2]],   [i[7][3],i[9][3]],   [i[7][4], i[9][4]],   [i[7][5],  i[9][5]]]
                    semsx    = [[i[10][1], i[12][1]], [i[10][2],i[12][2]], [i[10][3],i[12][3]], [i[10][4], i[12][4]], [i[10][5], i[12][5]]] 
                    Sesi[i[0][0]][i[2][0]]  = sems1or2
                    Sesi[i[0][0]][i[5][0]]  = sems3or4
                    Sesi[i[0][0]][i[8][0]]  = sems5or6
                    Sesi[i[0][0]][i[11][0]] = semsx
                elif len(i) == 11 :
                    if i[2][0] != "Smstr_2" :
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems3or4 = [[i[2][1],  i[4][1]],  [i[2][2],i[4][2]],   [i[2][3],i[4][3]],   [i[2][4], i[4][4]],  [i[2][5], i[4][5]]]
                        sems5or6 = [[i[5][1],  i[7][1]],  [i[5][2],i[7][2]],   [i[5][3],i[7][3]],   [i[5][4], i[7][4]],  [i[5][5], i[7][5]]]
                        semsx    = [[i[8][1], i[10][1]],  [i[8][1],i[10][1]],  [i[8][1],i[10][1]],  [i[8][1], i[10][1]], [i[8][5], i[10][5]]] 
                        Sesi[i[0][0]][i[1][0]]  = dumy
                        Sesi[i[0][0]][i[3][0]]  = sems3or4
                        Sesi[i[0][0]][i[6][0]]  = sems5or6
                        Sesi[i[0][0]][i[9][0]] = semsx
                    elif i[5][0] != "Smstr_4" :
                        Sesi[i[0][0]] = {}
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems1or2 = [[i[1][1],  i[3][1]],  [i[1][2],i[3][2]],   [i[1][3],i[3][3]],   [i[1][4], i[3][4]],  [i[1][5],i[3][5]]]
                        sems5or6 = [[i[5][1],  i[7][1]],  [i[5][2],i[7][2]],   [i[5][3],i[7][3]],   [i[5][4], i[7][4]],  [i[5][5], i[7][5]]]
                        semsx    = [[i[8][1],  i[10][1]], [i[8][2],i[10][2]],  [i[8][3],i[10][3]],  [i[8][4], i[10][4]], [i[8][5], i[10][5]]] 
                        Sesi[i[0][0]][i[2][0]]  = sems1or2
                        Sesi[i[0][0]][i[5][0]]  = dumy
                        Sesi[i[0][0]][i[8][0]]  = sems5or6
                        Sesi[i[0][0]][i[11][0]] = semsx
                    elif i[8][0] != "Smstr_6" :
                        Sesi[i[0][0]] = {}
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems1or2 = [[i[1][1],  i[3][1]],  [i[1][2],i[3][2]],   [i[1][3],i[3][3]],   [i[1][4],i[3][4]],  [i[1][5],i[3][5]]]
                        sems3or4 = [[i[4][1],  i[6][1]],  [i[4][2],i[6][2]],   [i[4][3],i[6][3]],   [i[4][4],i[6][4]],  [i[4][5],i[6][5]]]
                        semsx    = [[i[8][1],  i[10][1]], [i[8][2],i[10][2]],  [i[8][3],i[10][3]],  [i[8][4],i[10][4]], [i[8][5],i[10][5]]] 
                        Sesi[i[0][0]][i[2][0]]  = sems1or2
                        Sesi[i[0][0]][i[5][0]]  = sems3or4
                        Sesi[i[0][0]][i[7][0]]  = dumy
                        Sesi[i[0][0]][i[9][0]] = semsx
                    elif i[11][0] !=  "Smstr_X" :
                        Sesi[i[0][0]] = {}
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems1or2 = [[i[1][1],  i[3][1]],  [i[1][2],i[3][2]],   [i[1][3],i[3][3]],   [i[1][4],i[3][4]], [i[1][5],i[3][5]]]
                        sems3or4 = [[i[4][1],  i[6][1]],  [i[4][2],i[6][2]],   [i[4][3],i[6][3]],   [i[4][4],i[6][4]], [i[4][5],i[6][5]]]
                        sems5or6 = [[i[7][1],  i[9][1]],  [i[7][2],i[9][2]],   [i[7][3],i[9][3]],   [i[7][4],i[9][4]], [i[7][5],i[9][5]]]
                        Sesi[i[0][0]][i[2][0]]  = sems1or2
                        Sesi[i[0][0]][i[5][0]]  = sems3or4
                        Sesi[i[0][0]][i[8][0]]  = sems5or6
                        Sesi[i[0][0]][i[11][0]] = dumy
                elif len(i) == 9 :
                    if i[2][0] != "Smstr_2" :
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        Sesi[i[0][0]][i[1][0]]  = dumy
                        if i[3][0] != "Smstr_4" :
                            sems5or6 = [[i[3][1], i[5][1]],  [i[3][2],i[5][2]],   [i[3][3],i[5][3]],   [i[3][4], i[5][4]], [i[3][5], i[5][5]]]
                            semsx    = [[i[6][1], i[8][1]],  [i[6][2],i[8][2]],   [i[6][3],i[8][3]],   [i[6][4], i[8][4]], [i[6][5], i[8][5]]]
                            Sesi[i[0][0]][i[2][0]]  = dumy
                            Sesi[i[0][0]][i[4][0]]  = sems5or6
                            Sesi[i[0][0]][i[7][0]] = semsx
                        if i[6][0] != "Smstr_6" :   
                            sems3or4 = [[i[2][1], i[4][1]],  [i[2][2],i[4][2]],   [i[2][3],i[4][3]],   [i[2][4], i[4][4]], [i[2][5],i[4][5]]] 
                            semsx    = [[i[6][1], i[8][1]],  [i[6][2],i[8][2]],   [i[6][3],i[8][3]],   [i[6][4], i[8][4]], [i[6][5],i[8][5]]]  
                            Sesi[i[0][0]][i[3][0]]  = sems3or4
                            Sesi[i[0][0]][i[5][0]]  = dumy
                            Sesi[i[0][0]][i[7][0]] = semsx
                        if i[9][0] != "Smstr_X" :
                            sems3or4 = [[i[2][1], i[4][1]],  [i[2][2],i[4][2]],   [i[2][3],i[4][3]],   [i[2][4],i[4][4]], [i[2][5],i[4][5]]]
                            sems5or6 = [[i[5][1], i[7][1]],  [i[5][2],i[7][2]],   [i[5][3],i[7][3]],   [i[5][4],i[7][4]], [i[5][5],i[7][5]]]
                            Sesi[i[0][0]][i[3][0]]  = sems3or4
                            Sesi[i[0][0]][i[6][0]]  = sems5or6
                            Sesi[i[0][0]][i[9][0]] = semsx
                    elif i[5][0] != "Smstr_4" :
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems1or2 = [[i[1][1],i[3][1]],[i[1][2],i[3][2]],[i[1][3],i[3][3]],[i[1][4],i[3][4]]]
                        Sesi[i[0][0]][i[4][0]] = dumy
                        Sesi[i[0][0]][i[2][0]] = sems1or2
                        if i[6][0] != "Smstr_6" :
                            semsx    = [[i[6][1], i[8][1]],  [i[6][2],i[8][2]],   [i[6][3],i[8][3]],   [i[6][4], i[8][4]], [i[6][5], i[8][5]]]  
                            Sesi[i[0][0]][i[5][0]]  = dumy 
                            Sesi[i[0][0]][i[7][0]] = semsx
                        if i[8][0] == "Smstr_X" :
                            sems5or6 = [[i[5][1], i[7][1]],  [i[5][2],i[7][2]],   [i[5][3],i[7][3]],   [i[5][4],i[7][4]], [i[5][5],i[7][5]]]
                            Sesi[i[0][0]][i[6][0]]  = sems5or6
                            Sesi[i[0][0]][i[8][0]] = dumy
                    elif i[7][0] == "Smstr_6" :
                        dumy = [["",""],["",""],["",""],["",""],["",""]]
                        sems1or2 = [[i[1][1],i[3][1]],  [i[1][2],i[3][2]], [i[1][3],i[3][3]], [i[1][4],i[3][4]], [i[1][5],i[3][5]]]
                        sems3or4 = [[i[4][1],i[6][1]],  [i[4][2],i[6][2]], [i[4][3],i[6][3]], [i[4][4],i[6][4]], [i[4][5],i[6][5]]]
                        Sesi[i[0][0]][i[2][0]] = sems1or2
                        Sesi[i[0][0]][i[5][0]] = sems3or4
                        Sesi[i[0][0]][i[7][0]] = dumy
                        Sesi[i[0][0]][i[8][0]] = dumy
                elif len(i) == 7 :
                    Sesi[i[0][0]] = {}
                    dumy = [["",""],["",""],["",""],["",""],["",""]]
                    if i[1][0] == "Smstr_2" :
                        Sesi[i[0][0]][i[1][0]] = dumy	
                        if i[2][0] == "Smstr_4" :
                            Sesi[i[0][0]][i[2][0]] = dumy
                            if i[3][0] == "Smstr_6" :
                                Sesi[i[0][0]][i[3][0]] = dumy
                                Sesi[i[0][0]][i[5][0]] = [[i[4][1],i[6][1]],  [i[4][2],i[6][2]], [i[4][3],i[6][3]], [i[4][4],i[6][4]], [i[4][5],i[6][5]]]
                            else : 
                                Sesi[i[0][0]][i[6][0]] = dumy
                                Sesi[i[0][0]][i[4][0]] = [[i[3][1], i[5][1]],  [i[3][2],i[5][2]],   [i[3][3],i[5][3]],   [i[3][4], i[5][4]], [i[3][5], i[5][5]]]
                        else :
                            Sesi[i[0][0]][i[5][0]] = dumy
                            Sesi[i[0][0]][i[6][0]] = dumy
                            Sesi[i[0][0]][i[3][0]] = [[i[2][1], i[4][1]],  [i[2][2],i[4][2]],   [i[2][3],i[4][3]],   [i[2][4],i[4][4]], [i[2][5],i[4][5]]]
                    else : 
                        Sesi[i[0][0]][i[2][0]] = [[i[1][1],  i[3][1]],  [i[1][2],i[3][2]],   [i[1][3],i[3][3]],   [i[1][4],i[3][4]], [i[1][5],i[3][5]]] 
                        Sesi[i[0][0]][i[4][0]] = dumy
                        Sesi[i[0][0]][i[5][0]] = dumy
                        Sesi[i[0][0]][i[6][0]] = dumy
                elif len(i) == 5 :
                    Sesi[i[0][0]][i[1][0]] = dumy
                    Sesi[i[0][0]][i[2][0]] = dumy
                    Sesi[i[0][0]][i[3][0]] = dumy
                    Sesi[i[0][0]][i[4][0]] = dumy
            if IndekHari == 1 :      
                JadwalAkhir["Senin"] = Sesi
                IndekHari += 1
            elif IndekHari == 2 :
                JadwalAkhir["Selasa"] = Sesi
                IndekHari += 1
            elif IndekHari == 3 :
                JadwalAkhir["Rabu"] = Sesi
                IndekHari += 1
            elif IndekHari == 4 :
                JadwalAkhir["Kamis"] = Sesi
                IndekHari += 1
            

        sementaraHari3 = []
        JumatNih = []
        for z in JJumat :
            for x in z :
                if x.isdigit() : 
                    sementaraHari3.append("")
                else :
                    sementaraHari3.append(x)
            JumatNih.append(sementaraHari3)

        hari = JJumat
        smt = 0
        hasil = []
        semester = []   
        while len(hasil) != 4 :  
            for i in range(len(hari)) :
                if len(hasil) == 4 :
                    break
                if hari[smt][0] != "Smstr_X" :
                    semester.append(hari[smt])
                    smt += 1
                else :
                    semester.append(hari[smt])
                    if (smt+1) < len(hari) :
                        if hari[smt+1][0] == '' :
                            semester.append(hari[smt+1])
                            hari.remove(hari[smt+1])
                            smt += 1
                            hasil.append(semester)
                            semester = []
                    if semester != [] :
                        if semester[-1] == semester[-2] :
                            del semester[-1]
                            hasil.append(semester)
                            semester = []
                            smt +=1    
                            break 
        tampung = []
        dumy = [["",""],["",""],["",""],["",""],["",""]]
        sems = "Smstr_"
        Jumatan = []
        for hari in hasil :
            for i in range(1,len(hari)) :
                if i == len(hari)-1 :
                    if re.search(sems, hari[i][0]) :
                        tampung.append([hari[i],dumy])
                        continue
                if re.search(sems, hari[i][0]) and re.search(sems, hari[i+1][0]):
                    tampung.append([hari[i],dumy])
                    continue
                else :
                    if i%2 == 0 :
                        continue
                    else :
                        oke = [[hari[i][1],hari[i+1][1]],[hari[i][2],hari[i+1][2]], [hari[i][3],hari[i+1][3]],[hari[i][4],hari[i+1][4]],[hari[i][5],hari[i+1][5]]]
                        tampung.append(oke)
            Jumatan.append(tampung)
            tampung = []
        #print(1)
        Sesi = {}
        waktu = ["07:30","10:30","13:30","16:30"]

        b = 0
        for z in range(0,4) :
            Sesi[waktu[z]] = {}
            for i in Jumatan[z] :
                if b == 0 :
                    Sesi[waktu[z]]["Smstr_2"] = i
                    b += 1
                elif b == 1 :
                    Sesi[waktu[z]]["Smstr_4"] = i
                    b += 1
                elif b == 2 :
                    Sesi[waktu[z]]["Smstr_6"] = i
                    b += 1
                elif b == 3 :
                    Sesi[waktu[z]]["Smstr_X"] = i
                    b = 0
        JadwalAkhir["Jumat"] = Sesi
        self.jadwal = JadwalAkhir
        #print(1)
        
    def printSchedule(self):
        for hari in self.jadwal:
            print(hari)
            for sesi in self.jadwal[hari]:
                print(sesi)
                for semester in self.jadwal[hari][sesi]:
                    print (semester)
                    for matkul in self.jadwal[hari][sesi][semester]:
                        print(matkul,end=" ")
                    print()

    def readSubjects(self, csv_Subjects_List):
        with open(csv_Subjects_List, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row['Kode'], row['Singkatan'], row['SKS'], row['Harga'])
    

    def checkAvailableSubject(self):
        grade = self.usr_profile.getUsrGrades()

        for hari in self.jadwal:
            print(hari)
            for sesi in self.jadwal[hari]:
                print(sesi)
                for semester in self.jadwal[hari][sesi]:
                    print (semester)
                    for matkul in self.jadwal[hari][sesi][semester]:

                        if matkul in grade["MPBP"] or matkul in grade["MPWP"]:
                            pass #{"MPBP": {}, "MPWP": {}, "WAJIB": {}}
                        print(matkul,end=" ")
                    print()

    




pdf_path = "04_JadwalKuliah_2022_2023_2Genap_toStudent_230116_01.pdf"
csv_path = "ile.csv"

# guh = AcademicSubjects()
# guh.readSchedule(pdf_path,csv_path)

user = UserProfile()
user.readGradeTranscript("daftarnilai71210816.pdf")
user.readKHSTransript("khs71210816.pdf")
user.usr_AS.readSchedule(pdf_path,csv_path)
user.usr_AS.printSchedule()


print()
print(user.usr_profile, "\n")

for i in user.usr_grades:
    print(i)
    for j in user.usr_grades[i]:
        print(j, user.usr_grades[i][j])

print(user.getUsrIPK(), user.getUsrIPS())



sksAmbil = user.usr_AS.getMaksSKS()
print(f"Maksimal SKS yang boleh diambil adalah {sksAmbil} SKS")

user.usr_AS.readSubjects("Subjects.csv")
