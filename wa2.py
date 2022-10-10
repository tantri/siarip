from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import requests
import time
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta #tambahan
from time import sleep
from time import gmtime, strftime
from pytz import timezone
import pytz
import urllib
import urllib.parse
from urllib.parse import quote
import mysql.connector
import re
import locale
import socket
import urllib.request
import pymysql #tambahan

options = Options()
ua = UserAgent()
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"


# VARIBLE  UNTUK OTOMATISASI JAWABAN DAN KONFIGURASI
codeurl = 'https://raw.githubusercontent.com/brekertabumi/kelas_wa/main/class_wa_bot.py'
variabel = urllib.request.urlopen(codeurl)
datavariabel = variabel.read()
exec(datavariabel)

kodePa = "PA.Pas"
namapa = "Pengadilan Agama Pasuruan"
mulai = date(2020, 9, 1)
jarak = "3";
namadatabaselocal = "wa"
namaakunparkircursor = "Papas"
_NAMASINGKATANAPLIKASI_ = "SIARIP"
_PERKALIAN_BIAYA_P_ = 3
_PERKALIAN_BIAYA_T_ = 4
print(_UNREAD_)
print(_NAMAKONTAK_)
print(_TEXTBOX_)


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        return False


is_connected()


def koneksisipp():
    dbsipp = mysql.connector.connect(host="127.0.0.1", user="root", passwd="papas123*", database="sipp")
    return dbsipp


def koneksilocal():
    dblocal = mysql.connector.connect(host="127.0.0.1", user="root", passwd="papas123*", database="wa")
    return dblocal


koneksipp = koneksisipp()
if koneksipp.is_connected():
    print("Koneksi", "Koneksi ke SIPP Berhasil")
    koneksipp.close()
else:
    print("Koneksi", "Koneksi ke SIPP Gagal")

koneklocal = koneksilocal()
if koneklocal.is_connected():
    print("Koneksi", "Koneksi ke DB Local Berhasil")
    koneklocal.close()
else:
    print("Koneksi", "Koneksi DB Local Gagal")

browser = webdriver.Chrome(options=options, executable_path="/usr/bin/chromedriver")
browser.get('https://web.whatsapp.com')
sleep(20)


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(browser, time).until(element_present)


def send_whatsapp_msg(no_wa, jawaban):
    browser.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(no_wa))
    try:
        WebDriverWait(browser, 5).until(EC.alert_is_present(), )
        browser.switch_to.alert.accept()
    except TimeoutException:
        pass

    try:
        #XPATH BARU
        element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]', 40)
        #XPATH LAMA
        #element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 10)
        #txt_box = browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        text_box = browser.find_element_by_class_name(_TEXTBOX_)
        text_box.click()
        text_box.send_keys(jawaban)
        text_box.send_keys("\n")

    except Exception as e:
        print(e)
        print("Nomor HP tidak terdaftar di Whatsapp")
        pass


def number_format(num, places=0):
    return locale.format_string("%.*f", (places, num), True)


def cek_notif_outbox():
    print("Notif Outbox")
    try:
        koneklocal = koneksilocal()
        cursor_local_outbox = koneklocal.cursor()
        sql_local_outbox = "select `id`, `no_wa`, `isi_pesan`, `tgl_input`, `status`, `tgl_kirim` from outbox where status ='false' "
        cursor_local_outbox.execute(sql_local_outbox)
        results_outbox = cursor_local_outbox.fetchall()
        jumrowoutbox = cursor_local_outbox.rowcount
        # print(str(jumrowoutbox))
        if jumrowoutbox == 0:
            pass
        else:
            global data_outbox
            for data_outbox in results_outbox:
                id_outbox = data_outbox[0]
                no_wa = data_outbox[1]
                isi_pesan = data_outbox[2]
                tgl_input = data_outbox[3]
                # status = data_outbox[4]
                # tgl_kirim = data_outbox[5]
                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)
                jawaban = isi_pesan + " \n"
                print("Kirim Notif Outbox ke : " + no_wa)
                send_whatsapp_msg(no_wa, jawaban)
                sql_update_outbox = "update outbox set status ='true' , tgl_kirim =%s where id=%s "
                cursor_local_outbox.execute(sql_update_outbox, (tanggalkirim, id_outbox,))
                koneklocal.commit()
                sleep(3)

    finally:
        koneklocal.close()


def cek_notif_outbox_group():
    print("Notif Outbox_group")
    try:
        koneklocal = koneksilocal()
        cursor_local_outbox_group = koneklocal.cursor()
        sql_local_outbox_group = "select `id`, `nama_group`, `isi_pesan`, `tgl_input`, `status`, `tgl_kirim` from outbox_group where status ='false' "
        cursor_local_outbox_group.execute(sql_local_outbox_group)
        results_outbox_group = cursor_local_outbox_group.fetchall()
        jumrowoutbox_group = cursor_local_outbox_group.rowcount
        # print(str(jumrowoutbox))
        if jumrowoutbox_group == 0:
            pass
        else:
            global data_outbox_group
            for data_outbox_group in results_outbox_group:
                id_group = data_outbox_group[0]
                nama_group = data_outbox_group[1]
                isi_pesan = data_outbox_group[2]
                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim_group = datetime.now(jkt)
                jawaban = isi_pesan + " \n"
                print("Kirim Notif Outbox ke Group : " + nama_group)
                namagroups = [nama_group]
                for name in namagroups:
                    kontak = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                    kontak.click()
                    sleep(1)
                    text_box = browser.find_element_by_class_name(_TEXTBOX_)
                    text_box.click()
                    ganti = jawaban.replace("|", "~")
                    for part in ganti.split('~'):
                        text_box.send_keys(part)
                        action = webdriver.common.action_chains.ActionChains(browser)
                        action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()

                text_box.send_keys(" \n")

                sql_update_outbox_group = "update outbox_group set status ='true' , tgl_kirim =%s where id=%s "
                cursor_local_outbox_group.execute(sql_update_outbox_group, (tanggalkirim_group, id_group,))
                koneklocal.commit()
                sleep(3)

    finally:
        koneklocal.close()

#############################################################################
def notif_sidang_jsp():
    print("Notif Sidang JSP")
    try:
        koneksipp = koneksisipp()
        koneklocal2 = koneksilocal()
        cursorjsp = koneksipp.cursor()
        cursorjspnotif = koneksipp.cursor()
        cursorcek = koneklocal2.cursor()
        
        #Inisialisasi tanggal untuk kirim WA        
        date_now = datetime. now()
        date = datetime.strptime(date_now.strftime("%Y-%m-%d"), "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        tanggal_besok = modified_date.strftime("%Y-%m-%d")
        #tanggal_besok = "2021-04-08"

        sql2 = "SELECT id, nama FROM jurusita WHERE aktif LIKE 'Y' ORDER BY id ASC"
        cursorjsp.execute(sql2)
        resultsjsp = cursorjsp.fetchall()
        
        #perulangan TOTAL JSP        
        for data in resultsjsp:
            print(data[0], data[1])
            id_jurusita = data[0]
            
            #cari nomor hp untuk reminder siang dan sore hari
            sql4 = "SELECT b.jurusita_nama, b.hp_jsp, a.tanggal_sidang, a.status, a.jurusita_id FROM sidang_jsp AS a JOIN kontak_jsp AS b ON a.jurusita_id = b.jurusita_id WHERE a.tanggal_sidang = %s AND a.jurusita_id = %s"
            cursorcek.execute(sql4, (tanggal_besok, id_jurusita))
            resultsjspnotif2 = cursorcek.fetchall()
            jumlahrow_cek = cursorcek.rowcount
                  
            print('Cek apakah hari ini sudah kirim notif WA '+str(jumlahrow_cek))
            
            #Cek apakah JSP sudah dikirimi notifikasi hari ini? jika sudah maka kirimi peringatan     
            if jumlahrow_cek > 0: 
              print("Sudah Kirim Notifikasi Sidang \n")
              
            ############################### END FUNGSI KIRIM PERINGATAN UNTUK JSP ##################
              koneklocal_jam2 = koneksilocal()
              cursor_jam2 = koneklocal_jam2.cursor()

              #cari nomor hp untuk reminder siang dan sore hari
              cursor_jam2.execute("SELECT * FROM setting_notif_jsp")
              result_jam2 = cursor_jam2.fetchall()
              jumlahrow_jam2 = cursor_jam2.rowcount

              global tabel_jam2
              for urutan_jam2, tabel_jam2 in enumerate(result_jam2, start=0):
                id_jam2=tabel_jam2[0]
                jam2=tabel_jam2[1]
                menit2=tabel_jam2[2]
                status_jam2=tabel_jam2[3]
              
                #kirim reminder sesuai dengan jam yang ada di database
                if date_now2.hour == int(jam2) and date_now2.minute == int(menit2) and status_jam2 == "peringatan":  
                    global tabel_pengingat
                    for urutan2, tabel_pengingat in enumerate(resultsjspnotif2, start=0):
                        nama_jsp=tabel_pengingat[0]
                        no_wa2=tabel_pengingat[1]
                        tgl_sidang=tabel_pengingat[2]
                        status=tabel_pengingat[3]
                        id_jsp=tabel_pengingat[4]
                            
                    jawaban2 = "_Assalamualaikum.._ *" + nama_jsp + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " Mohon maaf sekedar mengingatkan, mohon dicek ulang ya,... apakah relaas untuk sidang besok ("+ str(tgl_sidang) +") sudah di sampaikan ke PP, jika masih ada yang belum tersampaikan, mohon segera disampaikan ya.. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " Terimakasih, selamat bekerja.." + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
                        
                    send_whatsapp_msg(no_wa2, jawaban2)
                        
                    koneklocal5 = koneksilocal()
                    cursorlocalakta2 = koneklocal5.cursor()
                    sqllocalaktax = "UPDATE sidang_jsp SET status = %s WHERE jurusita_id = %s AND tanggal_sidang = %s"
                    cursorlocalakta2.execute(sqllocalaktax, ("peringatan1",id_jsp,tgl_sidang))

                    koneklocal5.commit()
                    koneklocal5.close()
                    
                    print("Peringatan 1 Sudah dikirim "+nama_jsp+" \n")
         
              koneklocal_jam2.commit()
              koneklocal_jam2.close()

            ############################### END FUNGSI KIRIM PERINGATAN UNTUK JSP ##################
                    
            else:  
              sql3 = "SELECT A.perkara_id, A.nomor_perkara,A.jenis_perkara_text,B.nama AS nama_p,C.nama AS nama_t,D.nama AS pengacara_p,E.nama AS pengacara_t, F.ruangan_id, F.tanggal_sidang, F.agenda,J.jurusita_id, J.jurusita_nama, Y.hp_jsp FROM perkara A LEFT JOIN (SELECT perkara_id,nama FROM perkara_pihak1  GROUP BY perkara_id ) B ON B.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama FROM perkara_pihak2 GROUP BY perkara_id ) C ON C.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '1' GROUP BY perkara_id  ) D ON D.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '2' GROUP BY perkara_id  ) E ON E.perkara_id = A.perkara_id LEFT JOIN perkara_jadwal_sidang F ON F.perkara_id = A.perkara_id LEFT JOIN perkara_jurusita J ON J.perkara_id = A.perkara_id LEFT JOIN " + namadatabaselocal + ".kontak_jsp Y ON J.jurusita_id = Y.jurusita_id  WHERE F.tanggal_sidang = %s AND J.jurusita_id = %s ORDER BY J.jurusita_id ASC, nomor_perkara ASC"

              cursorjspnotif.execute(sql3, (tanggal_besok, id_jurusita))
              resultsjspnotif = cursorjspnotif.fetchall()
              jumlahrow = cursorjspnotif.rowcount
              
              print('apakah ada panggilan hari ini '+str(jumlahrow))
              
              if jumlahrow == 0: #JSP Tidak ada perkara
                print("tidak ada panggilan tidak kirim notifikasi atau sudah kirim notif \n")
                pass
              else: #JSP ada perkara hari itu
                jsp=[]
                cek=[]
                a=0
                z=0
                
                # print(resultsakta)
                global tabel_jsp
                for urutan, tabel_jsp in enumerate(resultsjspnotif, start=0):
                    nama_jsp=tabel_jsp[11]
                    tanggal_sidang=tabel_jsp[8]
                    perkaraid=tabel_jsp[0]
                    nomorperkara=tabel_jsp[1]
                    jurusita_id=tabel_jsp[10]
                    no_wa=tabel_jsp[12]
                    
                    jsp.append(tabel_jsp[1]) #menambahkan nomor perkara ke var jsp[]
                    jsp.append(tabel_jsp[9]) #menambahkan agenda ke var jsp[]
                    cek.append(jsp[a]+' '+jsp[a+1]) #menggabungkan 2 variabel jadi 1 string
                    a=a+2 #+2 sesuai dengan jumlah variabel yang di keluarkan
                    z=z+1 #hitung jumlah perkara
                            
                   # if not telp1 is None:
                     #   cektelp1 = telp1[:1]
                     #   if cektelp1 == "+":
                     #       no_wa = telp1.replace('+', '', 1)
                     #   elif cektelp1 == "0":
                     #       no_wa = telp1.replace('0', '62', 1)
                     #   else:
                     #       no_wa = telp1

                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)

                #mebuat ganti baris di WA
                enter_wa = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
                nomor_perkara = enter_wa.join(cek)

                tahun_http = (str(tanggal_sidang)[0:4])
                bulan_http = (str(tanggal_sidang)[5:7])
                tanggal_http = (str(tanggal_sidang)[8:10])
                alamat = "https://sipp.pa-pasuruan.go.id/list_jadwal_sidang/search/2/"+tanggal_http+"/"+bulan_http+"/"+tahun_http
                   
                jawaban = "*Nama Jurusita :* " + nama_jsp + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Berikut Nomor perkara, untuk sidang besok* (" + str(tanggal_sidang) + ") " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + nomor_perkara + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jumlah Perkara* " + str(z) + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jadwal Lengkap* " + alamat + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
                
                #ini nomor wa untuk bypass jika testing
                #no_wa = "6281331802929"

                send_whatsapp_msg(no_wa, jawaban)

                koneklocal = koneksilocal()
                cursorlocalakta = koneklocal.cursor()
                sqllocalakta = "insert into sidang_jsp(tanggal_sidang,jurusita_id,jurusita_nama,dikirim,status)values(%s,%s,%s,%s,%s)"
                cursorlocalakta.execute(sqllocalakta, (tanggal_sidang, jurusita_id, nama_jsp,tanggalkirim, "notifikasi"))

                if cursorlocalakta.lastrowid:
                    print('last insert id Kirim Notif Sidang JSP ', cursorlocalakta.lastrowid)
                else:
                    print('last insert id not found')

                koneklocal.commit()
                koneklocal.close()
     
        koneklocal2.close()
        koneksipp.close()

        #name = browser.find_element_by_class_name(_TEXTBOX_).text  # Contactname _6xQdq
        #if name == "Papas":
            #pass
            #names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
            #for name in names:
                #person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                #person.click()
        #else:
            #names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
            #for name in names:
                #person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                #person.click()


        print("Delay 60 detik, untuk PERINGATAN")
        time.sleep(60)
        pass
        

        
        #biar perulangan TOTAL JSP dari tabel jurusita di db sipp cuma 1x 1 menit
        #time.sleep(60)
        #print("Delay 60 detik, biar pengulangan cuma 1x")
    finally:
        koneksipp.close()
#############################################################################

#############################################################################
def notif_sidang_pp():
    print("Notif Sidang PP")
    try:
        koneksipp = koneksisipp()
        koneklocal2 = koneksilocal()
        
        cursorjsp = koneksipp.cursor()
        cursorjspnotif = koneksipp.cursor()
        cursorcek = koneklocal2.cursor()
        
        #Inisialisasi tanggal untuk kirim WA        
        date_now = datetime. now()
        date = datetime.strptime(date_now.strftime("%Y-%m-%d"), "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        tanggal_besok = modified_date.strftime("%Y-%m-%d")
        #tanggal_besok = "2021-04-08"

        sql2 = "SELECT id, nama FROM panitera_pn WHERE aktif LIKE 'Y' ORDER BY id ASC"
        cursorjsp.execute(sql2)
        resultsjsp = cursorjsp.fetchall()
         
        for data in resultsjsp:
            print(data[0], data[1])
            id_jurusita = data[0]
            
            sql4 = "SELECT * FROM sidang_pp WHERE tanggal_sidang = %s AND pp_id = %s"
            cursorcek.execute(sql4, (tanggal_besok, id_jurusita))
            resultsjspnotif2 = cursorcek.fetchall()
            jumlahrow_cek = cursorcek.rowcount
                  
            print('Cek apakah hari ini sudah kirim notif WA '+str(jumlahrow_cek))
                  
            #if jumlahrow_cek > 0: #JSP Tidak ada perkara
              #print("Sudah Kirim Notifikasi \n")
                  
            #else:  
            sql3 = "SELECT A.perkara_id, A.nomor_perkara,A.jenis_perkara_text,B.nama AS nama_p,C.nama AS nama_t,D.nama AS pengacara_p,E.nama AS pengacara_t, F.ruangan_id, F.tanggal_sidang, F.agenda,J.panitera_id, J.panitera_nama, Y.hp_pp FROM perkara A LEFT JOIN (SELECT perkara_id,nama FROM perkara_pihak1  GROUP BY perkara_id ) B ON B.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama FROM perkara_pihak2 GROUP BY perkara_id ) C ON C.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '1' GROUP BY perkara_id  ) D ON D.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '2' GROUP BY perkara_id  ) E ON E.perkara_id = A.perkara_id LEFT JOIN perkara_jadwal_sidang F ON F.perkara_id = A.perkara_id LEFT JOIN perkara_panitera_pn J ON J.perkara_id = A.perkara_id LEFT JOIN " + namadatabaselocal + ".kontak_pp Y ON J.panitera_id = Y.pp_id  WHERE F.tanggal_sidang = %s AND J.panitera_id = %s  ORDER BY J.panitera_id ASC, nomor_perkara ASC"

            cursorjspnotif.execute(sql3, (tanggal_besok, id_jurusita))
            resultsjspnotif = cursorjspnotif.fetchall()
            jumlahrow = cursorjspnotif.rowcount
              
            print('apakah ada sidang hari ini '+str(jumlahrow))
              
            if jumlahrow == 0: #JSP Tidak ada perkara
                print("tidak ada sidang tidak kirim notifikasi \n")
            else: #JSP ada perkara hari itu
                jsp=[]
                cek=[]
                a=0
                z=0
                
                # print(resultsakta)
                global tabel_jsp
                for urutan, tabel_jsp in enumerate(resultsjspnotif, start=0):
                    nama_jsp=tabel_jsp[11]
                    tanggal_sidang=tabel_jsp[8]
                    perkaraid=tabel_jsp[0]
                    nomorperkara=tabel_jsp[1]
                    jurusita_id=tabel_jsp[10]
                    no_wa=tabel_jsp[12]
                    
                    jsp.append(tabel_jsp[1]) #menambahkan nomor perkara ke var jsp[]
                    jsp.append(tabel_jsp[9]) #menambahkan agenda ke var jsp[]
                    cek.append(jsp[a]+' '+jsp[a+1]) #menggabungkan 2 variabel jadi 1 string
                    a=a+2 #+2 sesuai dengan jumlah variabel yang di keluarkan
                    z=z+1 #hitung jumlah perkara
                            
                   # if not telp1 is None:
                     #   cektelp1 = telp1[:1]
                     #   if cektelp1 == "+":
                     #       no_wa = telp1.replace('+', '', 1)
                     #   elif cektelp1 == "0":
                     #       no_wa = telp1.replace('0', '62', 1)
                     #   else:
                     #       no_wa = telp1

                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)

                #mebuat ganti baris di WA
                enter_wa = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
                nomor_perkara = enter_wa.join(cek)

                tahun_http = (str(tanggal_sidang)[0:4])
                bulan_http = (str(tanggal_sidang)[5:7])
                tanggal_http = (str(tanggal_sidang)[8:10])
                alamat = "https://sipp.pa-pasuruan.go.id/list_jadwal_sidang/search/2/"+tanggal_http+"/"+bulan_http+"/"+tahun_http
                  
                
                jawaban = "*Nama PP :* " + nama_jsp + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Berikut Nomor perkara, untuk sidang besok* (" + str(tanggal_sidang) + ") " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + nomor_perkara + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jumlah Perkara* " + str(z) + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jadwal Lengkap* " + alamat + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " Selamat bersidang yaa, semangat selalu dan jangan lupa di input SIPP nya"+ Keys.SHIFT + Keys.ENTER + Keys.SHIFT +"_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
                
                #ini nomor wa untuk bypass jika testing
                #no_wa = "6281331802929"

                send_whatsapp_msg(no_wa, jawaban)

                koneklocal = koneksilocal()
                cursorlocalakta = koneklocal.cursor()
                sqllocalakta = "insert into sidang_pp(tanggal_sidang,pp_id,pp_nama,dikirim,status)values(%s,%s,%s,%s,%s)"
                cursorlocalakta.execute(sqllocalakta, (tanggal_sidang, jurusita_id, nama_jsp,tanggalkirim, "Pesan Telah Terkirim"))

                if cursorlocalakta.lastrowid:
                    print('last insert id Kirim Notif Sidang PP ', cursorlocalakta.lastrowid)
                else:
                    print('last insert id not found')

                koneklocal.commit()
                koneklocal.close()
     
        koneklocal2.close()
        koneksipp.close()
    finally:
        koneksipp.close()
#############################################################################

#############################################################################

#############################################################################
def notif_sidang_hakim():
    print("Notif Sidang Hakim")
    try:
        koneksipp = koneksisipp()
        koneklocal2 = koneksilocal()
        
        cursorjsp = koneksipp.cursor()
        cursorjspnotif = koneksipp.cursor()
        cursorcek = koneklocal2.cursor()
        
        #Inisialisasi tanggal untuk kirim WA        
        date_now = datetime. now()
        date = datetime.strptime(date_now.strftime("%Y-%m-%d"), "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        tanggal_besok = modified_date.strftime("%Y-%m-%d")
        #tanggal_besok = "2021-04-08"

        sql2 = "SELECT id, nama FROM hakim_pn WHERE aktif LIKE 'Y' ORDER BY id ASC"
        cursorjsp.execute(sql2)
        resultsjsp = cursorjsp.fetchall()
         
        for data in resultsjsp:
            print(data[0], data[1])
            id_jurusita = data[0]
            
            sql4 = "SELECT * FROM sidang_hakim WHERE tanggal_sidang = %s AND hakim_id = %s"
            cursorcek.execute(sql4, (tanggal_besok, id_jurusita))
            resultsjspnotif2 = cursorcek.fetchall()
            jumlahrow_cek = cursorcek.rowcount
                  
            print('Cek apakah hari ini sudah kirim notif WA '+str(jumlahrow_cek))
                  
            #if jumlahrow_cek > 0: #JSP Tidak ada perkara
              #print("Sudah Kirim Notifikasi \n")
                  
            #else:  
            sql3 = "SELECT A.perkara_id, A.nomor_perkara,A.jenis_perkara_text,B.nama AS nama_p,C.nama AS nama_t,D.nama AS pengacara_p,E.nama AS pengacara_t, F.ruangan_id, F.tanggal_sidang, F.agenda,J.hakim_id, J.hakim_nama, Y.hp_hakim FROM perkara A LEFT JOIN (SELECT perkara_id,nama FROM perkara_pihak1  GROUP BY perkara_id ) B ON B.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama FROM perkara_pihak2 GROUP BY perkara_id ) C ON C.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '1' GROUP BY perkara_id  ) D ON D.perkara_id = A.perkara_id LEFT JOIN (SELECT perkara_id, nama, pihak_ke FROM perkara_pengacara WHERE pihak_ke = '2' GROUP BY perkara_id  ) E ON E.perkara_id = A.perkara_id LEFT JOIN perkara_jadwal_sidang F ON F.perkara_id = A.perkara_id LEFT JOIN perkara_hakim_pn J ON J.perkara_id = A.perkara_id LEFT JOIN " + namadatabaselocal + ".kontak_hakim Y ON J.hakim_id = Y.hakim_id  WHERE F.tanggal_sidang = %s AND J.hakim_id = %s GROUP BY J.perkara_id ORDER BY J.hakim_id ASC, nomor_perkara ASC"

            cursorjspnotif.execute(sql3, (tanggal_besok, id_jurusita))
            resultsjspnotif = cursorjspnotif.fetchall()
            jumlahrow = cursorjspnotif.rowcount
              
            print('apakah ada sidang hari ini '+str(jumlahrow))
              
            if jumlahrow == 0: #JSP Tidak ada perkara
                print("tidak ada sidang tidak kirim notifikasi \n")
            else: #JSP ada perkara hari itu
                jsp=[]
                cek=[]
                a=0
                z=0
                
                # print(resultsakta)
                global tabel_jsp
                for urutan, tabel_jsp in enumerate(resultsjspnotif, start=0):
                    nama_jsp=tabel_jsp[11]
                    tanggal_sidang=tabel_jsp[8]
                    perkaraid=tabel_jsp[0]
                    nomorperkara=tabel_jsp[1]
                    jurusita_id=tabel_jsp[10]
                    no_wa=tabel_jsp[12]
                    
                    jsp.append(tabel_jsp[1]) #menambahkan nomor perkara ke var jsp[]
                    jsp.append(tabel_jsp[9]) #menambahkan agenda ke var jsp[]
                    cek.append(jsp[a]+' '+jsp[a+1]) #menggabungkan 2 variabel jadi 1 string
                    a=a+2 #+2 sesuai dengan jumlah variabel yang di keluarkan
                    z=z+1 #hitung jumlah perkara
                            
                   # if not telp1 is None:
                     #   cektelp1 = telp1[:1]
                     #   if cektelp1 == "+":
                     #       no_wa = telp1.replace('+', '', 1)
                     #   elif cektelp1 == "0":
                     #       no_wa = telp1.replace('0', '62', 1)
                     #   else:
                     #       no_wa = telp1

                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)

                #mebuat ganti baris di WA
                enter_wa = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
                nomor_perkara = enter_wa.join(cek)

                tahun_http = (str(tanggal_sidang)[0:4])
                bulan_http = (str(tanggal_sidang)[5:7])
                tanggal_http = (str(tanggal_sidang)[8:10])
                alamat = "https://sipp.pa-pasuruan.go.id/list_jadwal_sidang/search/2/"+tanggal_http+"/"+bulan_http+"/"+tahun_http
                  
                
                jawaban = "*Nama Hakim :* " + nama_jsp + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Berikut Nomor perkara, untuk sidang besok* (" + str(tanggal_sidang) + ") " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + nomor_perkara + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jumlah Perkara* " + str(z) + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jadwal Lengkap* " + alamat + Keys.SHIFT + Keys.ENTER + Keys.SHIFT +  " Selamat bersidang Yang Mulia, semoga persidangan besok berjalan dengan lancar.."+ Keys.SHIFT + Keys.ENTER + Keys.SHIFT +"_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
                
                #ini nomor wa untuk bypass jika testing
                no_wa2 = "6281331802929"

                send_whatsapp_msg(no_wa, jawaban)
                send_whatsapp_msg(no_wa2, jawaban)

                koneklocal = koneksilocal()
                cursorlocalakta = koneklocal.cursor()
                sqllocalakta = "insert into sidang_hakim(tanggal_sidang,hakim_id,hakim_nama,dikirim,status)values(%s,%s,%s,%s,%s)"
                cursorlocalakta.execute(sqllocalakta, (tanggal_sidang, jurusita_id, nama_jsp,tanggalkirim, "Pesan Telah Terkirim"))

                if cursorlocalakta.lastrowid:
                    print('last insert id Kirim Notif Sidang Hakim ', cursorlocalakta.lastrowid)
                else:
                    print('last insert id not found')

                koneklocal.commit()
                koneklocal.close()
     
        koneklocal2.close()
        koneksipp.close()
    finally:
        koneksipp.close()
#############################################################################


def cek_ac_terbit():
    print("cek AC Terbit")
    try:
        koneksipp = koneksisipp()
        cursorakta = koneksipp.cursor()
        sqlakta = "select a.perkara_id,a.nomor_perkara,j.tgl_akta_cerai,DATE_FORMAT(j.tgl_akta_cerai,'%d/%m/%Y') as tgl_ac,j.nomor_akta_cerai,a.jenis_perkara_nama,b.pihak_id,b.nama as namap,d.telepon as telp1 from perkara_akta_cerai j left join perkara a on j.perkara_id=a.perkara_id left join perkara_pihak1 b on a.perkara_id=b.perkara_id left join pihak d on b.pihak_id=d.id left join " + namadatabaselocal + ".akta_cerai z on a.perkara_id=z.perkara_id and b.pihak_id=z.nama_id where j.tgl_akta_cerai >%s and datediff(curdate(),j.tgl_akta_cerai) >=%s and j.nomor_akta_cerai is not null and (d.telepon is not null and d.telepon<>'') and z.perkara_id is null"
        cursorakta.execute(sqlakta, (mulai, jarak))
        resultsakta = cursorakta.fetchall()
        # print(resultsakta)
        global dataakta
        for dataakta in resultsakta:
            perkaraid = dataakta[0]
            nomorperkara = dataakta[1]
            tglakta = str(dataakta[2])
            nomorakta = dataakta[4]
            pihakid = dataakta[6]
            namap = dataakta[7]
            telp1 = dataakta[8]
            if not telp1 is None:
                cektelp1 = telp1[:1]
                if cektelp1 == "+":
                    no_wa = telp1.replace('+', '', 1)
                elif cektelp1 == "0":
                    no_wa = telp1.replace('0', '62', 1)
                else:
                    no_wa = telp1

            jkt = pytz.timezone('Asia/Jakarta')
            tanggalkirim = datetime.now(jkt)

            jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Akta Cerai Telah Terbit_ " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Akta Cerai :* " + nomorakta + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tanggal Terbit :* " + tglakta + " "+ Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Khusus Untuk yang beralamat di Kota Pasuruan, Wajib membawa KTP dan KK Asli*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
            # ini nomor wa untuk bypass jika testing
            # no_wa = "6281252053793"

            send_whatsapp_msg(no_wa, jawaban)

            koneklocal = koneksilocal()
            cursorlocalakta = koneklocal.cursor()
            sqllocalakta = "insert into akta_cerai(perkara_id,nomor_perkara,tgl_ac,nomor_ac,nama_id,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursorlocalakta.execute(sqllocalakta, (
                perkaraid, nomorperkara, tglakta, nomorakta, pihakid, namap.replace("'", "''"), no_wa, jawaban,
                tanggalkirim))

            if cursorlocalakta.lastrowid:
                print('last insert id Kirim Akta Cerai ', cursorlocalakta.lastrowid)
            else:
                print('last insert id not found')

            koneklocal.commit()
            koneklocal.close()
            koneksipp.close()
    finally:
        koneksipp.close()


def cek_ac_terbit_ecourt():
    print("Cek AC Ecourt")
    try:
        koneksipp = koneksisipp()
        cursoraktakuasa = koneksipp.cursor()
        sqlakta = "select a.perkara_id,a.nomor_perkara,j.tgl_akta_cerai,DATE_FORMAT(j.tgl_akta_cerai,'%d/%m/%Y') as tgl_ac,j.nomor_akta_cerai,a.jenis_perkara_nama,b.pengacara_id,b.nama as nama_pengacara,d.telepon as telp_pengacara from perkara_akta_cerai j left join perkara a on j.perkara_id=a.perkara_id left join perkara_pengacara b on a.perkara_id=b.perkara_id left join pihak d on b.pengacara_id = d.id left join " + namadatabaselocal + ".akta_cerai z on a.perkara_id=z.perkara_id and b.pengacara_id=z.nama_id where j.tgl_akta_cerai > %s and datediff(curdate(),j.tgl_akta_cerai) >= %s  and j.nomor_akta_cerai is not null and (d.telepon is not null and d.telepon<>'') and z.perkara_id is null"
        cursoraktakuasa.execute(sqlakta, (mulai, jarak))
        resultsaktakuasa = cursoraktakuasa.fetchall()
        global dataaktakuasa
        for dataaktakuasa in resultsaktakuasa:
            perkaraid = dataaktakuasa[0]
            nomorperkara = dataaktakuasa[1]
            tglakta = str(dataaktakuasa[2])
            nomorakta = dataaktakuasa[4]
            namajnsperkara = dataaktakuasa[5]
            pengacaraid = dataaktakuasa[6]
            namapengacara = dataaktakuasa[7]
            telppengacara = dataaktakuasa[8]
            if not telppengacara is None:
                cektelpengacara = telppengacara[:1]
                if cektelpengacara == "+":
                    no_wa_pengacara = telppengacara.replace('+', '', 1)
                elif cektelpengacara == "0":
                    no_wa_pengacara = telppengacara.replace('0', '62', 1)
                else:
                    no_wa_pengacara = telppengacara

            no_wa = no_wa_pengacara
            # no_wa = "6281252053793"
            jkt = pytz.timezone('Asia/Jakarta')
            tanggalkirim = datetime.now(jkt)
            jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama Kuasa :* " + namapengacara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Akta Cerai Telah Terbit_ " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Akta Cerai :* " + nomorakta + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tanggal Akta :* " + tglakta + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"
            # print(jawaban)
            # text_box.send_keys(jawaban)
            send_whatsapp_msg(no_wa, jawaban)

            koneklocal = koneksilocal()
            cursorlocalakta = koneklocal.cursor()
            sqllocalakta = "insert into akta_cerai(perkara_id,nomor_perkara,tgl_ac,nomor_ac,nama_id,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursorlocalakta.execute(sqllocalakta, (
                perkaraid, nomorperkara, tglakta, nomorakta, pengacaraid, namapengacara.replace("'", "''"), no_wa,
                jawaban,
                tanggalkirim))

            if cursorlocalakta.lastrowid:
                print('last insert id  info Akta Cerai terbit untuk Pengacara', cursorlocalakta.lastrowid)
            else:
                print('last insert id not found')
            koneklocal.commit()
            koneklocal.close()
            koneksipp.close()
    finally:
        koneksipp.close()


def daftarbaru():
    print("Pendaftaran Baru")
    try:
        koneksipp = koneksisipp()
        cursordaftar = koneksipp.cursor()
        sqldaftar = "select a.perkara_id,a.nomor_perkara,DATE_FORMAT(a.tanggal_pendaftaran,'%d/%m/%Y') as tgl_daftar,a.jenis_perkara_id,a.jenis_perkara_nama,d.nama as namap,d.telepon as telp1,f.nama as namat,f.telepon as telp2 from perkara a left join perkara_pihak1 b on a.perkara_id=b.perkara_id left join pihak d on b.pihak_id=d.id left join perkara_pihak2 e on a.perkara_id=e.perkara_id left join pihak f on e.pihak_id=f.id left join " + namadatabaselocal + ".perkara_daftar z on a.perkara_id=z.perkara_id where a.tanggal_pendaftaran >=%s and (d.telepon is not null and d.telepon<>'') and z.perkara_id is null"
        cursordaftar.execute(sqldaftar, (mulai,))
        resultsdaftar = cursordaftar.fetchall()
        # print(resultsdaftar)
        global datadaftar
        for datadaftar in resultsdaftar:
            perkaraid = datadaftar[0]
            nomorperkara = datadaftar[1]
            tgldaftar = datadaftar[2]
            jenisperkara = datadaftar[4]
            namap = datadaftar[5]
            namat = datadaftar[7]

            if not datadaftar[6] is None:
                telpp = datadaftar[6]
                cektelp = telpp[:1]
                if cektelp == "+":
                    no_wa_p = telpp.replace('+', '', 1)
                elif cektelp == "0":
                    no_wa_p = telpp.replace('0', '62', 1)
                else:
                    no_wa_p = telpp

                no_wa = no_wa_p
                # no_wa = "6281252053793"

                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)
                jawaban = "Pendaftaran Para Pihak antara " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P:* " + str(
                    namap) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T:* " + str(
                    namat) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Telah terdaftar dengan nomor perkara :_ *" + str(
                    nomorperkara) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Daftar :* " + str(
                    tgldaftar) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + str(
                    namapa) + "_ \n"

                send_whatsapp_msg(no_wa, jawaban)

                koneklocal = koneksilocal()
                cursorlocaldaftar = koneklocal.cursor()
                sqllocaldaftar = "insert into perkara_daftar(perkara_id,nomor_perkara,tanggal_daftar,nama_pihak,nomor_hp,pesan,dikirim) values (%s, %s, %s, %s, %s, %s, %s)"
                cursorlocaldaftar.execute(sqllocaldaftar,(perkaraid, nomorperkara, tgldaftar, namap, no_wa, jawaban, tanggalkirim))
                if cursorlocaldaftar.lastrowid:
                    print('last insert id perkara daftar P', cursorlocaldaftar.lastrowid)
                else:
                    print('last insert id not found')
                koneklocal.commit()
                koneklocal.close()
            else:
                pass
            if not datadaftar[8] is None:
                telpt = datadaftar[8]
                cektelt = telpt[:1]
                if cektelt == "+":
                    no_wa_t = telpt.replace('+', '', 1)
                elif cektelt == "0":
                    no_wa_t = telpt.replace('0', '62', 1)
                else:
                    no_wa_t = telpt

                no_wat = no_wa_t
                # no_wa = "6282244339826"

                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)
                jawaban = "Pendaftaran Para Pihak antara " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P:* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T:* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Telah terdaftar dengan nomor perkara :_ *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Daftar :* " + tgldaftar + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"

                send_whatsapp_msg(no_wat, jawaban)

                koneklocal = koneksilocal()
                cursorlocaldaftar = koneklocal.cursor()
                sqllocaldaftar = "insert into perkara_daftar(perkara_id,nomor_perkara,tanggal_daftar,nama_pihak,nomor_hp,pesan,dikirim)values(%s, %s, %s, %s, %s, %s, %s) "
                cursorlocaldaftar.execute(sqllocaldaftar,(perkaraid, nomorperkara, tgldaftar, namat, no_wat, jawaban, tanggalkirim))
                if cursorlocaldaftar.lastrowid:
                    print('last insert id perkara daftar T', cursorlocaldaftar.lastrowid)
                else:
                    print('last insert id not found')
                koneklocal.commit()
                koneklocal.close()

            else:
                pass
    finally:
        koneksipp.close()


def daftarbaru_ecourt():
    print("Pendaftaran Baru E-Court")
    try:
        koneksipp = koneksisipp()
        cursordaftarecourt = koneksipp.cursor()
        sqldaftarecourt = "select a.perkara_id,a.nomor_perkara,DATE_FORMAT(a.tanggal_pendaftaran,'%d/%m/%Y') as tgl_daftar,d.nomor_register as nomor_ecourt,a.jenis_perkara_id,a.jenis_perkara_nama,c.nama as pengacara, c.telepon as telp_pengacara from perkara a LEFT JOIN perkara_efiling d ON a.nomor_perkara=d.nomor_perkara left join perkara_pengacara b on a.perkara_id=b.perkara_id left join pihak c on b.pengacara_id = c.id left join " + namadatabaselocal + ".perkara_daftar z on a.perkara_id=z.perkara_id where a.tanggal_pendaftaran >=%s and d.nomor_perkara is not null and (c.telepon is not null and c.telepon<>'') and z.perkara_id is null"
        cursordaftarecourt.execute(sqldaftarecourt, (mulai,))
        resultsdaftarecourt = cursordaftarecourt.fetchall()
        global datadaftarecourt
        for datadaftarecourt in resultsdaftarecourt:
            perkaraid = datadaftarecourt[0]
            nomorperkara = datadaftarecourt[1]
            tgldaftar = datadaftarecourt[2]
            nomorecourt = datadaftarecourt[3]
            jenisperkara = datadaftarecourt[4]
            namaperkara = datadaftarecourt[5]
            pengacara = datadaftarecourt[6]

            jkt = pytz.timezone('Asia/Jakarta')
            tanggalkirim = datetime.now(jkt)
            jawaban = "*E-Court: :* " + str(
                nomorecourt) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Telah terdaftar Dengan Nomor Perkara :_ *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Pada Tanggal : " + tgldaftar + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan ini dikirim otomatis oleh : " + namapa + "_ \n"

            if not datadaftarecourt[7] is None:
                telpkuasa = datadaftarecourt[7]
                cektelk = telpkuasa[:1]
                if cektelk == "+":
                    no_wa_pengacara = telpkuasa.replace('+', '', 1)
                elif cektelk == "0":
                    no_wa_pengacara = telpkuasa.replace('0', '62', 1)
                else:
                    no_wa_pengacara = telpkuasa

                no_wa = no_wa_pengacara
                # no_wa = "6282244339826"
                send_whatsapp_msg(no_wa, jawaban)

                ecourt = "1"
                koneklocal = koneksilocal()
                cursorlocaldaftar = koneklocal.cursor()
                sqllocaldaftar = "insert into perkara_daftar(perkara_id,nomor_perkara,tanggal_daftar,ecourt,nama_pihak,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursorlocaldaftar.execute(sqllocaldaftar, (
                    perkaraid, nomorperkara, tgldaftar, ecourt, pengacara, no_wa_pengacara, jawaban, tanggalkirim))

                if cursorlocaldaftar.lastrowid:
                    print('last insert id Ppppendaftaran Perkara Ecourt untul Lawter', cursorlocaldaftar.lastrowid)
                else:
                    print('last insert id not found')
                koneklocal.commit()
                koneklocal.close()

            else:
                pass
        koneksipp.close()
    finally:
        koneksipp.close()

def sidang_notif():
    print("Cek Notifikasi Sidang")
    try:
        koneksipp = koneksisipp()
        cursorsidang = koneksipp.cursor()
        sqldatasidang = "SELECT a.tanggal_sidang,DATE_FORMAT(a.tanggal_sidang,'%d/%m/%Y') AS tglsidangindo, a.urutan AS sidangke,a.perkara_id,b.nomor_perkara,b.jenis_perkara_nama, c.perkara_id AS perkara_id_sidang, d.efiling_id,d.nomor_register AS nomor_ecourt,  f.nama AS pengacara, f.telepon AS tlp_pengacara, h.nama AS pihak1, h.telepon AS tlp_pihak1, j.nama AS pihak2, j.telepon AS tlp_pihak2 FROM perkara_jadwal_sidang a LEFT JOIN perkara b ON a.perkara_id = b.perkara_id LEFT JOIN " + namadatabaselocal + ".`sidang_lokal` c ON a.perkara_id = c.perkara_id AND a.tanggal_sidang=c.tanggal_sidang LEFT JOIN perkara_efiling d ON b.nomor_perkara=d.nomor_perkara LEFT JOIN perkara_pengacara e ON a.perkara_id = e.perkara_id LEFT JOIN pihak f ON e.pengacara_id = f.id LEFT JOIN perkara_pihak1 g ON a.perkara_id=g.perkara_id LEFT JOIN pihak h ON g.pihak_id=h.id LEFT JOIN perkara_pihak2 i ON a.perkara_id=i.perkara_id LEFT JOIN pihak j ON i.pihak_id=j.id WHERE a.tanggal_sidang > CURDATE() AND c.perkara_id IS NULL AND ((f.telepon != '') OR (h.telepon !='') OR (j.telepon !=''))"
        cursorsidang.execute(sqldatasidang)
        resultsidang = cursorsidang.fetchall()
        jumrowceksidang = cursorsidang.rowcount
        if jumrowceksidang >= 1:
            global datasidangnotif
            for datasidangnotif in resultsidang:
                tgl_sidang_ori = datasidangnotif[0]
                tanggal_sidang = datasidangnotif[1]
                urutan = str(datasidangnotif[2])
                perkara_id = datasidangnotif[3]
                nomorperkara = datasidangnotif[4]
                jenis_perkara_nama = datasidangnotif[5]
                perkara_id_sidang = datasidangnotif[6]
                efiling_id = datasidangnotif[7]
                nomor_ecourt = datasidangnotif[8]
                pengacara = datasidangnotif[9]
                namapihak = datasidangnotif[11]
                jkt = pytz.timezone('Asia/Jakarta')
                tanggalkirim = datetime.now(jkt)
                if not datasidangnotif[10] is None:
                    telppengacara = datasidangnotif[10]
                    cektelk = telppengacara[:1]
                    if cektelk == "+":
                        no_wa_pengacara = telppengacara.replace('+', '', 1)
                    elif cektelk == "0":
                        no_wa_pengacara = telppengacara.replace('0', '62', 1)
                    else:
                        no_wa_pengacara = telppengacara

                    if '1' in urutan:
                        jawaban = "E-Court: *" + str(
                            nomor_ecourt) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nomor Perkara: *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nama: *" + pengacara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang Ke : *" + urutan + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                            tanggal_sidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Chek Ecourt untuk Panggilannya, dari *" + namapa + "* \n";
                        no_wa = no_wa_pengacara

                        send_whatsapp_msg(no_wa, jawaban)

                        koneklocal = koneksilocal()
                        cursorlocalsidangl = koneklocal.cursor()
                        ecourt = 1
                        sqllocalsidangl = "insert into " + namadatabaselocal + ".sidang_lokal(perkara_id,nomor_perkara,tanggal_sidang,ecourt,nomor_ecourt,pihak,nomorhp,dikirim,pesan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursorlocalsidangl.execute(sqllocalsidangl, (
                            perkara_id, nomorperkara, tgl_sidang_ori, ecourt, nomor_ecourt, pengacara, no_wa_pengacara,
                            tanggalkirim, jawaban))

                        koneklocal.commit()
                        koneklocal.close()
                    else:
                        jkt = pytz.timezone('Asia/Jakarta')
                        tanggalkirim = datetime.now(jkt)

                        jawaban = "E-Court: *" + str(
                            nomor_ecourt) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nomor Perkara: *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nama: *" + pengacara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang Ke: *" + urutan + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang: *" + str(
                            tanggal_sidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Dikirim otomatis oleh *" + namapa + "*_ \n";

                        no_wa = no_wa_pengacara
                        send_whatsapp_msg(no_wa, jawaban)

                        koneklocal = koneksilocal()
                        cursorlocalsidang2 = koneklocal.cursor()
                        ecourt = 1
                        sqllocalsidang2 = "insert into wa.sidang_lokal(perkara_id,nomor_perkara,tanggal_sidang,ecourt,nomor_ecourt,pihak,nomorhp,dikirim,pesan) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursorlocalsidang2.execute(sqllocalsidang2, (
                            perkara_id, nomorperkara, tgl_sidang_ori, ecourt, nomor_ecourt, pengacara, no_wa_pengacara,
                            tanggalkirim, jawaban))

                        koneklocal.commit()
                        koneklocal.close()
                else:
                    pass

                if not datasidangnotif[11] is None:
                    pihak1 = datasidangnotif[11]
                    if not datasidangnotif[12] is None:
                        tlp_pihak1 = datasidangnotif[12]
                        cektelp1 = tlp_pihak1[:1]
                        if cektelp1 == "+":
                            no_wa_pihak1 = tlp_pihak1.replace('+', '', 1)

                        elif cektelp1 == "0":
                            no_wa_pihak1 = tlp_pihak1.replace('0', '62', 1)

                        else:
                            no_wa_pihak1 = tlp_pihak1

                        jawaban = "Nomor Perkara: *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nama: *" + namapihak + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Agenda Sidang Ke : *" + urutan + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                            tanggal_sidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Dikirim otomatis oleh " + namapa + "_ \n";

                        no_wa = no_wa_pihak1
                        # no_wa = "6282244339826"

                        send_whatsapp_msg(no_wa, jawaban)

                        koneklocal = koneksilocal()
                        cursorlocalsidang = koneklocal.cursor()
                        ecourt = 1
                        sqllocalsidang = "insert into sidang_lokal(perkara_id,nomor_perkara,tanggal_sidang,ecourt,nomor_ecourt,pihak,nomorhp,dikirim,pesan)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursorlocalsidang.execute(sqllocalsidang, (
                            perkara_id, nomorperkara, tgl_sidang_ori, ecourt, nomor_ecourt, pihak1, no_wa_pihak1,
                            tanggalkirim,
                            jawaban))

                        koneklocal.commit()
                        koneklocal.close()

                    else:
                        pass
                else:
                    pass

                if not datasidangnotif[13] is None:
                    pihak2 = datasidangnotif[13]
                    if not datasidangnotif[14] is None:
                        tlp_pihak2 = datasidangnotif[14]
                        cektelp2 = tlp_pihak2[:1]
                        if cektelp2 == "+":
                            no_wa_pihak2 = tlp_pihak2.replace('+', '', 1)

                        elif cektelp2 == "0":
                            no_wa_pihak2 = tlp_pihak2.replace('0', '62', 1)

                        else:
                            no_wa_pihak2 = tlp_pihak2

                        jawaban = "Nomor Perkara: *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nama P: *" + namapihak + "* Nama T: *" + pihak2 + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Agenda Sidang Ke : *" + urutan + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                            tanggal_sidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Dikirim otomatis oleh " + namapa + "_ \n";

                        no_wa = no_wa_pihak2
                        # no_wa = "6282244339826"

                        send_whatsapp_msg(no_wa, jawaban)

                        koneklocal = koneksilocal()
                        cursorlocalsidang = koneklocal.cursor()
                        ecourt = 1
                        sqllocalsidang = "insert into sidang_lokal(perkara_id,nomor_perkara,tanggal_sidang,ecourt,nomor_ecourt,pihak,nomorhp,dikirim,pesan)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursorlocalsidang.execute(sqllocalsidang, (
                        perkara_id, nomorperkara, tgl_sidang_ori, ecourt, nomor_ecourt, pihak2, no_wa_pihak2,
                        tanggalkirim, jawaban))

                        koneklocal.commit()
                        koneklocal.close()
                    else:
                        pass
                else:
                    pass

        else:
            pass

    finally:

        koneksipp.close()


def cek_psp_ct():
    print("Notifikasi PSP CT")
    try:
        koneksipp = koneksisipp()
        cursorpsp = koneksipp.cursor()
        sqlpsp = "select a.perkara_id,a.nomor_perkara, a.jenis_perkara_text,DATE_FORMAT(c.tgl_ikrar_talak,'%d-%m-%Y') as tgl_ikrar, f.nama as pihak,f.telepon as telp_pihak,h.nama as pengacara,h.telepon as telp_pengacara, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as penerimaan, sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as pengeluaran, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah, 0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL), b.jumlah,0)) as saldo, a.proses_terakhir_text from perkara a left join perkara_biaya b on a.perkara_id=b.perkara_id left join perkara_ikrar_talak c on a.perkara_id=c.perkara_id left join (select * from perkara_pihak1 where urutan=1) d on a.perkara_id=d.perkara_id left join pihak f on d.pihak_id=f.id left join (select * from perkara_pengacara where urutan=1 group by perkara_id) g on a.perkara_id=g.perkara_id left join pihak h on g.pengacara_id=h.id where c.tgl_ikrar_talak is not null and year(c.tgl_ikrar_talak)>2018 and datediff(curdate(), c.tgl_ikrar_talak)>3 and ((f.nama is not null and (f.telepon is not null and f.telepon<>'')) or ( h.nama is not null and (h.telepon is not null and h.telepon<>''))) GROUP BY a.perkara_id having sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL), b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) > 0"
        cursorpsp.execute(sqlpsp)
        resultspsp = cursorpsp.fetchall()
        jumrow_psp = cursorpsp.rowcount
        if jumrow_psp > 0:
            global datapsp1
            for datapsp1 in resultspsp:
                perkaraid = datapsp1[0]
                nomorperkara = datapsp1[1]
                pihak = datapsp1[4]
                telppihak = datapsp1[5]
                telppengacara = datapsp1[7]
                if datapsp1[10] is None:
                    pass
                else:
                    saldo = int(datapsp1[10])

                    koneklocal = koneksilocal()
                    cursorlocalcek_kirim_psp = koneklocal.cursor()
                    sqllocal_cek_sisa_panjar = "select max(dikirim) as tgl from " + namadatabaselocal + ".sisa_panjar where perkara_id = %s"
                    cursorlocalcek_kirim_psp.execute(sqllocal_cek_sisa_panjar, (perkaraid,))
                    results_cek_sisa_panjar = cursorlocalcek_kirim_psp.fetchall()
                    global data_cek_psp_local1
                    for data_cek_psp_local1 in results_cek_sisa_panjar:
                        if data_cek_psp_local1[0] is None:
                            jkt = pytz.timezone('Asia/Jakarta')
                            tanggalkirim = datetime.now(jkt)
                            jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                int(float(saldo)),
                                2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                            # no_wa = "6281252053793"
                            if not telppihak is None:
                                cektelppihak = telppihak[:1]
                                if cektelppihak == "+":
                                    no_wa = telppihak.replace('+', '', 1)
                                elif cektelppihak == "0":
                                    no_wa = telppihak.replace('0', '62', 1)
                                else:
                                    no_wa = telppihak

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                            if not telppengacara is None:
                                cektelppengacara = telppengacara[:1]
                                if cektelppengacara == "+":
                                    no_wa = telppengacara.replace('+', '', 1)
                                elif cektelppengacara == "0":
                                    no_wa = telppengacara.replace('0', '62', 1)
                                else:
                                    no_wa = telppengacara

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                        else:
                            jkt = pytz.timezone('Asia/Jakarta')
                            waktu_now = datetime.now(jkt)
                            waktu_now_str = datetime.strftime(waktu_now, "%Y,%m,%d")
                            waktu_sekarang = datetime.strptime(waktu_now_str, '%Y,%m,%d')

                            waktu = datetime.strftime(data_cek_psp_local1[0], "%Y,%m,%d")
                            waktu_psp = datetime.strptime(waktu, '%Y,%m,%d')
                            selisih = waktu_sekarang - waktu_psp
                            diff = selisih.days
                            if diff >= 14:
                                jkt = pytz.timezone('Asia/Jakarta')
                                tanggalkirim = datetime.now(jkt)
                                jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                    int(float(saldo)),
                                    2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                                # no_wa = "6281252053793"
                                if not telppihak is None:
                                    cektelppihak = telppihak[:1]
                                    if cektelppihak == "+":
                                        no_wa = telppihak.replace('+', '', 1)
                                    elif cektelppihak == "0":
                                        no_wa = telppihak.replace('0', '62', 1)
                                    else:
                                        no_wa = telppihak

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))

                                if not telppengacara is None:
                                    cektelppengacara = telppengacara[:1]
                                    if cektelppengacara == "+":
                                        no_wa = telppengacara.replace('+', '', 1)
                                    elif cektelppengacara == "0":
                                        no_wa = telppengacara.replace('0', '62', 1)
                                    else:
                                        no_wa = telppengacara

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))
                            else:
                                pass

                    koneklocal.commit()
                    koneklocal.close()
        else:
            pass
    finally:
        koneksipp.close()


def cek_psp_volunter():
    print("Notifikasi PSP Volunterr")
    try:
        koneksipp = koneksisipp()
        cursorpsp = koneksipp.cursor()
        sqlpsp = "Select a.perkara_id,a.nomor_perkara, a.jenis_perkara_text,DATE_FORMAT(c.tanggal_putusan,'%d-%m-%Y') as tgl_putus,f.nama as pihak,f.telepon as telp_pihak,h.nama as pengacara,h.telepon as telp_pengacara, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as penerimaan, sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as pengeluaran,sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as saldo, a.proses_terakhir_text from perkara a left join perkara_biaya b on a.perkara_id=b.perkara_id left join perkara_putusan c on a.perkara_id=c.perkara_id left join (select * from perkara_pihak1 where urutan=1) d on a.perkara_id=d.perkara_id left join pihak f on d.pihak_id=f.id left join (select * from perkara_pengacara where urutan=1 group by perkara_id) g on a.perkara_id=g.perkara_id left join  pihak h on g.pengacara_id=h.id where c.tanggal_putusan is not null and year(c.tanggal_putusan)>2018 and datediff(curdate(),c.tanggal_putusan)>3 and a.alur_perkara_id=16 and ((f.nama is not null and (f.telepon is not null and f.telepon<>'')) or (h.nama is not null and (h.telepon is not null and h.telepon<>'')))GROUP BY a.perkara_id having sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) > 0"
        cursorpsp.execute(sqlpsp)
        resultspsp = cursorpsp.fetchall()
        jumrow_psp = cursorpsp.rowcount
        if jumrow_psp > 0:
            global datapsp2
            for datapsp2 in resultspsp:
                perkaraid = datapsp2[0]
                nomorperkara = datapsp2[1]
                pihak = datapsp2[4]
                telppihak = datapsp2[5]
                telppengacara = datapsp2[6]
                if datapsp2[10] is None:
                    pass
                else:
                    saldo = int(datapsp2[10])

                    koneklocal = koneksilocal()
                    cursorlocalcek_kirim_psp = koneklocal.cursor()
                    sqllocal_cek_sisa_panjar = "select max(dikirim) as tgl from " + namadatabaselocal + ".sisa_panjar where perkara_id = %s"
                    cursorlocalcek_kirim_psp.execute(sqllocal_cek_sisa_panjar, (perkaraid,))
                    results_cek_sisa_panjar = cursorlocalcek_kirim_psp.fetchall()
                    global data_cek_psp_local2
                    for data_cek_psp_local2 in results_cek_sisa_panjar:
                        if data_cek_psp_local2[0] is None:
                            jkt = pytz.timezone('Asia/Jakarta')
                            tanggalkirim = datetime.now(jkt)
                            jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                int(float(saldo)),
                                2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                            # no_wa = "6281252053793"
                            if not telppihak is None:
                                cektelppihak = telppihak[:1]
                                if cektelppihak == "+":
                                    no_wa = telppihak.replace('+', '', 1)
                                elif cektelppihak == "0":
                                    no_wa = telppihak.replace('0', '62', 1)
                                else:
                                    no_wa = telppihak

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                            if not telppengacara is None:
                                cektelppengacara = telppengacara[:1]
                                if cektelppengacara == "+":
                                    no_wa = telppengacara.replace('+', '', 1)
                                elif cektelppengacara == "0":
                                    no_wa = telppengacara.replace('0', '62', 1)
                                else:
                                    no_wa = telppengacara

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                        else:
                            jkt = pytz.timezone('Asia/Jakarta')
                            waktu_now = datetime.now(jkt)
                            waktu_now_str = datetime.strftime(waktu_now, "%Y,%m,%d")
                            waktu_sekarang = datetime.strptime(waktu_now_str, '%Y,%m,%d')

                            waktu = datetime.strftime(data_cek_psp_local2[0], "%Y,%m,%d")
                            waktu_psp = datetime.strptime(waktu, '%Y,%m,%d')
                            selisih = waktu_sekarang - waktu_psp
                            diff = selisih.days
                            if diff >= 14:
                                jkt = pytz.timezone('Asia/Jakarta')
                                tanggalkirim = datetime.now(jkt)
                                jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                    int(float(saldo)),
                                    2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                                # no_wa = "6281252053793"
                                if not telppihak is None:
                                    cektelppihak = telppihak[:1]
                                    if cektelppihak == "+":
                                        no_wa = telppihak.replace('+', '', 1)
                                    elif cektelppihak == "0":
                                        no_wa = telppihak.replace('0', '62', 1)
                                    else:
                                        no_wa = telppihak

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))

                                if not telppengacara is None:
                                    cektelppengacara = telppengacara[:1]
                                    if cektelppengacara == "+":
                                        no_wa = telppengacara.replace('+', '', 1)
                                    elif cektelppengacara == "0":
                                        no_wa = telppengacara.replace('0', '62', 1)
                                    else:
                                        no_wa = telppengacara

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))
                            else:
                                pass

                    koneklocal.commit()
                    koneklocal.close()
        else:
            pass
    finally:
        koneksipp.close()


def cek_psp_kontesius_non_ct_non_verstek():
    print("Notififikasi KOntesius non CT Non Vertek")
    try:
        koneksipp = koneksisipp()
        cursorpsp = koneksipp.cursor()
        sqlpsp = "select a.perkara_id,a.nomor_perkara, a.jenis_perkara_text,DATE_FORMAT(c.tanggal_putusan,'%d-%m-%Y') as tgl_putus,f.nama as pihak,f.telepon as telp_pihak,h.nama as pengacara,h.telepon as telp_pengacara, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as penerimaan, sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as pengeluaran, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as saldo, a.proses_terakhir_text,z.perkara_id as perkaraid_pbt from perkara a left join perkara_biaya b on a.perkara_id=b.perkara_id left join (select perkara_id,tanggal_transaksi from perkara_biaya where kategori_id=6 and tahapan_id=10) z on a.perkara_id=z.perkara_id left join perkara_putusan c on a.perkara_id=c.perkara_id left join (select * from perkara_pihak1 where urutan=1) d on a.perkara_id=d.perkara_id left join pihak f on d.pihak_id=f.id left join (select * from perkara_pengacara where urutan=1 group by perkara_id) g on a.perkara_id=g.perkara_id left join pihak h on g.pengacara_id=h.id where c.tanggal_putusan is not null and c.amar_putusan not like '%verstek%' and year(c.tanggal_putusan)>2018 and datediff(curdate(),c.tanggal_putusan)>3 and a.alur_perkara_id=15 and a.jenis_perkara_id<>346 and z.perkara_id is null and ((f.nama is not null and (f.telepon is not null and f.telepon<>'')) or (h.nama is not null and (h.telepon is not null and h.telepon<>''))) GROUP BY a.perkara_id having sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) > 0"
        cursorpsp.execute(sqlpsp)
        resultspsp = cursorpsp.fetchall()
        jumrow_psp = cursorpsp.rowcount
        if jumrow_psp > 0:
            global datapsp3
            for datapsp3 in resultspsp:
                perkaraid = datapsp3[0]
                nomorperkara = datapsp3[1]
                pihak = datapsp3[4]
                telppihak = datapsp3[5]
                telppengacara = datapsp3[7]
                if datapsp3[10] is None:
                    pass
                else:
                    saldo = int(datapsp3[10])

                    koneklocal = koneksilocal()
                    cursorlocalcek_kirim_psp = koneklocal.cursor()
                    sqllocal_cek_sisa_panjar = "select max(dikirim) as tgl from " + namadatabaselocal + ".sisa_panjar where perkara_id = %s"
                    cursorlocalcek_kirim_psp.execute(sqllocal_cek_sisa_panjar, (perkaraid,))
                    results_cek_sisa_panjar = cursorlocalcek_kirim_psp.fetchall()
                    global data_cek_psp_local3
                    for data_cek_psp_local3 in results_cek_sisa_panjar:
                        if data_cek_psp_local3[0] is None:
                            jkt = pytz.timezone('Asia/Jakarta')
                            tanggalkirim = datetime.now(jkt)
                            jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                int(float(saldo)),
                                2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                            # no_wa = "6281252053793"
                            if not telppihak is None:
                                cektelppihak = telppihak[:1]
                                if cektelppihak == "+":
                                    no_wa = telppihak.replace('+', '', 1)
                                elif cektelppihak == "0":
                                    no_wa = telppihak.replace('0', '62', 1)
                                else:
                                    no_wa = telppihak

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                            if not telppengacara is None:
                                cektelppengacara = telppengacara[:1]
                                if cektelppengacara == "+":
                                    no_wa = telppengacara.replace('+', '', 1)
                                elif cektelppengacara == "0":
                                    no_wa = telppengacara.replace('0', '62', 1)
                                else:
                                    no_wa = telppengacara

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                        else:
                            jkt = pytz.timezone('Asia/Jakarta')
                            waktu_now = datetime.now(jkt)
                            waktu_now_str = datetime.strftime(waktu_now, "%Y,%m,%d")
                            waktu_sekarang = datetime.strptime(waktu_now_str, '%Y,%m,%d')

                            waktu = datetime.strftime(data_cek_psp_local3[0], "%Y,%m,%d")
                            waktu_psp = datetime.strptime(waktu, '%Y,%m,%d')
                            selisih = waktu_sekarang - waktu_psp
                            diff = selisih.days
                            if diff >= 14:
                                jkt = pytz.timezone('Asia/Jakarta')
                                tanggalkirim = datetime.now(jkt)
                                jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                    int(float(saldo)),
                                    2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                                # no_wa = "6281252053793"
                                if not telppihak is None:
                                    cektelppihak = telppihak[:1]
                                    if cektelppihak == "+":
                                        no_wa = telppihak.replace('+', '', 1)
                                    elif cektelppihak == "0":
                                        no_wa = telppihak.replace('0', '62', 1)
                                    else:
                                        no_wa = telppihak

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))

                                if not telppengacara is None:
                                    cektelppengacara = telppengacara[:1]
                                    if cektelppengacara == "+":
                                        no_wa = telppengacara.replace('+', '', 1)
                                    elif cektelppengacara == "0":
                                        no_wa = telppengacara.replace('0', '62', 1)
                                    else:
                                        no_wa = telppengacara

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))
                            else:
                                pass

                    koneklocal.commit()
                    koneklocal.close()
        else:
            pass
    finally:
        koneksipp.close()


def cek_psp_kontesius_non_ct_verstek():
    print("Cek PSP KOntesius Non CT Verstek")
    try:
        koneksipp = koneksisipp()
        cursorpsp = koneksipp.cursor()
        sqlpsp = "select a.perkara_id,a.nomor_perkara, a.jenis_perkara_text,DATE_FORMAT(c.tanggal_putusan,'%d-%m-%Y') as tgl_putus,DATE_FORMAT(z.tanggal_transaksi,'%d-%m-%Y') as tgl_pbt, f.nama as pihak,f.telepon as telp_pihak,h.nama as pengacara,h.telepon as telp_pengacara, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as penerimaan, sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as pengeluaran, sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) as saldo, a.proses_terakhir_text,z.perkara_id as perkaraid_pbt from perkara a left join perkara_biaya b on a.perkara_id=b.perkara_id left join (select perkara_id,tanggal_transaksi from perkara_biaya where kategori_id=6 and tahapan_id=10) z on a.perkara_id=z.perkara_id left join perkara_putusan c on a.perkara_id=c.perkara_id left join (select * from perkara_pihak1 where urutan=1 group by perkara_id) d on a.perkara_id=d.perkara_id left join pihak f on d.pihak_id=f.id left join (select * from perkara_pengacara where urutan=1 limit 1) g on a.perkara_id=g.perkara_id left join pihak h on g.pengacara_id=h.id where c.tanggal_putusan is not null and  c.amar_putusan like '%verstek%' and year(c.tanggal_putusan)>2018 and datediff(curdate(),c.tanggal_putusan)>3 and a.alur_perkara_id=15 and a.jenis_perkara_id<>346 and z.perkara_id is not null and ((f.nama is not null and (f.telepon is not null and f.telepon<>'')) or (h.nama is not null and (h.telepon is not null and h.telepon<>''))) GROUP BY a.perkara_id having sum(if(b.tahapan_id=10 and b.jenis_transaksi=1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0))-sum(if(b.tahapan_id=10 and b.jenis_transaksi=-1 and (b.pihak_ke=1 OR b.pihak_ke IS NULL),b.jumlah,0)) > 0"
        cursorpsp.execute(sqlpsp)
        resultspsp = cursorpsp.fetchall()
        jumrow_psp = cursorpsp.rowcount
        if jumrow_psp > 0:
            global datapsp4
            for datapsp4 in resultspsp:
                perkaraid = datapsp4[0]
                nomorperkara = datapsp4[1]
                pihak = datapsp4[5]
                telppihak = datapsp4[6]
                namapengacara = datapsp4[7]
                telppengacara = datapsp4[8]
                if datapsp4[11] is None:
                    pass
                else:
                    saldo = int(datapsp4[11])
                    koneklocal = koneksilocal()
                    cursorlocalcek_kirim_psp = koneklocal.cursor()
                    sqllocal_cek_sisa_panjar = "select max(dikirim) as tgl from " + namadatabaselocal + ".sisa_panjar where perkara_id = %s"
                    cursorlocalcek_kirim_psp.execute(sqllocal_cek_sisa_panjar, (perkaraid,))
                    results_cek_sisa_panjar = cursorlocalcek_kirim_psp.fetchall()
                    global data_cek_psp_local4
                    for data_cek_psp_local4 in results_cek_sisa_panjar:
                        if data_cek_psp_local4[0] is None:
                            jkt = pytz.timezone('Asia/Jakarta')
                            tanggalkirim = datetime.now(jkt)
                            jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                int(float(saldo)),
                                2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                            # no_wa = "6281252053793"
                            if not telppihak is None:
                                cektelppihak = telppihak[:1]
                                if cektelppihak == "+":
                                    no_wa = telppihak.replace('+', '', 1)
                                elif cektelppihak == "0":
                                    no_wa = telppihak.replace('0', '62', 1)
                                else:
                                    no_wa = telppihak

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                            if not telppengacara is None:
                                cektelppengacara = telppengacara[:1]
                                if cektelppengacara == "+":
                                    no_wa = telppengacara.replace('+', '', 1)
                                elif cektelppengacara == "0":
                                    no_wa = telppengacara.replace('0', '62', 1)
                                else:
                                    no_wa = telppengacara

                                send_whatsapp_msg(no_wa, jawaban)

                                cursorlocalpsp = koneklocal.cursor()
                                sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                cursorlocalpsp.execute(sqllocalpsp, (
                                    perkaraid, nomorperkara, saldo, namapengacara.replace("'", "''"), no_wa, jawaban,
                                    tanggalkirim))

                        else:
                            jkt = pytz.timezone('Asia/Jakarta')
                            waktu_now = datetime.now(jkt)
                            waktu_now_str = datetime.strftime(waktu_now, "%Y,%m,%d")
                            waktu_sekarang = datetime.strptime(waktu_now_str, '%Y,%m,%d')

                            waktu = datetime.strftime(data_cek_psp_local4[0], "%Y,%m,%d")
                            waktu_psp = datetime.strptime(waktu, '%Y,%m,%d')
                            selisih = waktu_sekarang - waktu_psp
                            diff = selisih.days
                            if diff >= 14:
                                jkt = pytz.timezone('Asia/Jakarta')
                                tanggalkirim = datetime.now(jkt)
                                jawaban = "Sisa Panjar perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "sejumlah : *Rp. " + number_format(
                                    int(float(saldo)),
                                    2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Silahkan diambil di loket kasir " + namapa + ". " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                                # no_wa = "6281252053793"
                                if not telppihak is None:
                                    cektelppihak = telppihak[:1]
                                    if cektelppihak == "+":
                                        no_wa = telppihak.replace('+', '', 1)
                                    elif cektelppihak == "0":
                                        no_wa = telppihak.replace('0', '62', 1)
                                    else:
                                        no_wa = telppihak

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))

                                if not telppengacara is None:
                                    cektelppengacara = telppengacara[:1]
                                    if cektelppengacara == "+":
                                        no_wa = telppengacara.replace('+', '', 1)
                                    elif cektelppengacara == "0":
                                        no_wa = telppengacara.replace('0', '62', 1)
                                    else:
                                        no_wa = telppengacara

                                    send_whatsapp_msg(no_wa, jawaban)

                                    cursorlocalpsp = koneklocal.cursor()
                                    sqllocalpsp = "insert into sisa_panjar(perkara_id,nomor_perkara,psp,nama,nomor_hp,pesan,dikirim)values(%s,%s,%s,%s,%s,%s,%s)"
                                    cursorlocalpsp.execute(sqllocalpsp, (
                                        perkaraid, nomorperkara, saldo, pihak.replace("'", "''"), no_wa, jawaban,
                                        tanggalkirim))
                            else:
                                pass

                    koneklocal.commit()
                    koneklocal.close()
        else:
            pass

    except Exception as e:
        print(e)
        pass

    finally:
        koneksipp.close()


def cek_pmh():
    print("Cek PMH")
    try:
        koneklocal = koneksilocal()
        cursorlocal = koneklocal.cursor()
        sqlcekpmh_terkirim = "select user_sipp,validasi,max(dikirim) as tgl from reminder_sipp where validasi='pmh' and datediff(curdate(),dikirim)=0"
        cursorlocal.execute(sqlcekpmh_terkirim)
        result_cek_kirim = cursorlocal.fetchall()
        global datacekkirimpmh
        for datacekkirimpmh in result_cek_kirim:
            validasi = datacekkirimpmh[1]
            if validasi is None:
                koneksipp = koneksisipp()
                cursorpmh = koneksipp.cursor()
                sqlpmh = "select a.perkara_id, a.nomor_perkara, date_format(tanggal_pendaftaran,'%d-%m-%Y') as tgl_daftar from perkara a left join perkara_penetapan b on a.perkara_id=b.perkara_id where year(a.tanggal_pendaftaran) >= 2020 and DATEDIFF(curdate(),a.tanggal_pendaftaran) > 1 and b.perkara_id is null order by a.perkara_id"
                cursorpmh.execute(sqlpmh)
                result_pmh = cursorpmh.fetchall()
                jumrow_pmh = cursorpmh.rowcount
                if jumrow_pmh > 0:
                    for datapmh in result_pmh:
                        nomorperkara = datapmh[1]
                        koneklocal = koneksilocal()
                        cursorlocal = koneklocal.cursor()
                        sqllocal_cek_hp = "select idsipp,nomorhp from " + namadatabaselocal + ".daftar_kontak where jabatan=%s and status=%s"
                        cursorlocal.execute(sqllocal_cek_hp, ("ketua", "aktif"))
                        result_hp_ketua = cursorlocal.fetchall()
                        jumrow_hp_ketua = cursorlocal.rowcount
                        if jumrow_hp_ketua > 0:
                            for data_hp_ketua in result_hp_ketua:
                                id_ketua = data_hp_ketua[0]
                                nomorhp_ketua = data_hp_ketua[1]
                                if not nomorhp_ketua is None:
                                    cek_format_no_hp = nomorhp_ketua[:1]
                                    if cek_format_no_hp == "+":
                                        no_wa = nomorhp_ketua.replace('+', '', 1)
                                    elif cek_format_no_hp == "0":
                                        no_wa = nomorhp_ketua.replace('0', '62', 1)
                                    else:
                                        no_wa = cek_format_no_hp

                                    jawaban = "Perkara : *" + nomorperkara + "* belum PMH lebih dari 2 hari. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " _Pesan ini dikirim otomatis oleh " + namapa + "_ \n"
                                    send_whatsapp_msg(no_wa, jawaban)
                                    sleep(1)
                                    jkt = pytz.timezone('Asia/Jakarta')
                                    waktu_now = datetime.now(jkt)
                                    pengingat = "pmh"
                                    koneklocal = koneksilocal()
                                    cursorlocal = koneklocal.cursor()
                                    sqllocal_insert_data_lokal = "insert into reminder_sipp(user_sipp,nohp,validasi,wa,dikirim)values(%s,%s,%s,%s,%s)"
                                    cursorlocal.execute(sqllocal_insert_data_lokal,
                                                        (id_ketua, no_wa, pengingat, jawaban, waktu_now))
                                    koneklocal.commit()
                                    koneklocal.close()
                                else:
                                    koneklocal.close()
                                    print("Nomor HP Ketua salah format")
                                    pass
                        else:
                            koneklocal.close()
                            pass
                    koneksipp.close()
                else:
                    koneksipp.close()
                    pass
    except Exception as e:
        print(e)
        pass


def cek_penetapan():
    print("Cek Penetapan")
    try:
        koneksipp = koneksisipp()
        cursorpenetapan = koneksipp.cursor()
        sql_cek_belum_penetapan = "select count(*) as jumlah from perkara a left join perkara_panitera_pn b on a.perkara_id=b.perkara_id where DATEDIFF(curdate(),a.tanggal_pendaftaran) > 4 and year(a.tanggal_pendaftaran)>=2018 and b.perkara_id is null"
        cursorpenetapan.execute(sql_cek_belum_penetapan)
        result_cek_blm_penentapan = cursorpenetapan.fetchall()
        koneksipp.commit()
        koneksipp.close()
        global data_blm_penentapan
        for data_blm_penentapan in result_cek_blm_penentapan:
            jumlah_blm_penetapan = data_blm_penentapan[0]
            if jumlah_blm_penetapan > 0:
                koneklocal = koneksilocal()
                cursorlocal = koneklocal.cursor()
                sql_cek_pengingat = "select user_sipp,validasi,max(dikirim) as tgl from reminder_sipp where validasi='pp' and datediff(curdate(),dikirim)=0"
                cursorlocal.execute(sql_cek_pengingat)
                result_cek_pengingat = cursorlocal.fetchall()
                global validasipenetapan
                for validasipenetapan in result_cek_pengingat:
                    validasi = validasipenetapan[1]
                    if validasi is None:
                        jawaban = "*Pengingat SIPP:*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Perkara lebih dari 4 hari setelah pendaftaran, belum ada penetapan PP dan Jurusita, ada sebanyak *" + str(
                            jumlah_blm_penetapan) + "* perkara. " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                        koneklocal = koneksilocal()
                        cursorlocal = koneklocal.cursor()
                        sqllocal_cek_hp = "select idsipp,nomorhp from " + namadatabaselocal + ".daftar_kontak where jabatan=%s and status=%s"
                        cursorlocal.execute(sqllocal_cek_hp, ("panitera", "aktif"))
                        result_hp_panitera = cursorlocal.fetchall()
                        jumrow_hp_panitera = cursorlocal.rowcount
                        if jumrow_hp_panitera > 0:
                            for data_hp_panitera in result_hp_panitera:
                                id_panitera = data_hp_panitera[0]
                                nomorhp_panitera = data_hp_panitera[1]
                                if not nomorhp_panitera is None:
                                    cek_format_no_hp = nomorhp_panitera[:1]
                                    if cek_format_no_hp == "+":
                                        no_wa = nomorhp_panitera.replace('+', '', 1)
                                    elif cek_format_no_hp == "0":
                                        no_wa = nomorhp_panitera.replace('0', '62', 1)
                                    else:
                                        no_wa = cek_format_no_hp

                                    send_whatsapp_msg(no_wa, jawaban)
                                    sleep(1)
                                    jkt = pytz.timezone('Asia/Jakarta')
                                    waktu_now = datetime.now(jkt)
                                    pengingat = "pp"
                                    sqllocal_insert_data_lokal = "insert into reminder_sipp(user_sipp,nohp,validasi,wa,dikirim)values(%s,%s,%s,%s,%s)"
                                    cursorlocal.execute(sqllocal_insert_data_lokal,
                                                        (id_panitera, no_wa, pengingat, jawaban, waktu_now))
                                    koneklocal.commit()
                                    koneklocal.close()
                                else:
                                    koneklocal.close()
                                    print("Nomor HP Panitera salah format")
                        else:
                            koneklocal.close()
                            pass
                    else:
                        pass
            else:
                # koneksipp.close()
                pass
    except Exception as e:
        print(e)
        pass


def cek_phs():
    print("Cek PHS")
    try:
        koneksipp = koneksisipp()
        cursorphs = koneksipp.cursor()
        sql_cek_phs_id_hakim = "select a.hakim_id from perkara_hakim_pn a left join perkara_penetapan_hari_sidang b on a.perkara_id=b.perkara_id where year(a.tanggal_penetapan)>=2018 and a.jabatan_hakim_id=1 and a.aktif='Y' and datediff(curdate(),a.tanggal_penetapan)> 3 and b.perkara_id is null and a.perkara_id not in (select z.perkara_id from perkara_putusan z left join perkara_jadwal_sidang x on z.perkara_id=x.perkara_id where z.tanggal_putusan is not null and year(z.tanggal_putusan) >= 2018 and x.perkara_id is null) group by a.hakim_id"
        cursorphs.execute(sql_cek_phs_id_hakim, ())
        result_cek_phs_id_hakim = cursorphs.fetchall()
        jumrow_cek_phs = cursorphs.rowcount
        if jumrow_cek_phs > 0:
            global dataphs
            for dataphs in result_cek_phs_id_hakim:
                id_hakim = dataphs[0]

                koneklocal = koneksilocal()
                cursorlocal = koneklocal.cursor()
                sql_cek_data_sudah_kirim = "select user_sipp,validasi,max(dikirim) as tgl from " + namadatabaselocal + ".reminder_sipp where validasi='phs' and user_sipp=%s and datediff(curdate(),dikirim)=0"
                cursorlocal.execute(sql_cek_data_sudah_kirim, (id_hakim,))
                result_cek_pengingat = cursorlocal.fetchall()
                global validasiphs
                for validasiphs in result_cek_pengingat:
                    validasi = validasiphs[1]
                    if validasi is None:
                        koneksipp = koneksisipp()
                        cursorcekphshakim = koneksipp.cursor()
                        sql_cek_data_hakim = "select a.hakim_id, y.nomor_perkara from perkara_hakim_pn a left join perkara_penetapan_hari_sidang b on a.perkara_id=b.perkara_id left join perkara y on a.perkara_id=y.perkara_id where year(a.tanggal_penetapan)>=2018 and a.jabatan_hakim_id=1 and a.aktif='Y' and datediff(curdate(),a.tanggal_penetapan)>3 and b.perkara_id is null and a.perkara_id not in (select z.perkara_id from perkara_putusan z left join perkara_jadwal_sidang x on z.perkara_id=x.perkara_id where z.tanggal_putusan is not null and year(z.tanggal_putusan) >= 2018 and x.perkara_id is null) and a.hakim_id=%s"
                        cursorcekphshakim.execute(sql_cek_data_hakim, (id_hakim,))
                        result_data_hakim = cursorcekphshakim.fetchall()
                        jumrow_data_hakim = cursorcekphshakim.rowcount
                        if jumrow_data_hakim > 0:
                            global data_phs_hakim
                            for data_phs_hakim in result_data_hakim:
                                nomorperkara = data_phs_hakim[1]
                                cursorlocal = koneklocal.cursor()
                                sqllocal_cek_hp = "select idsipp, nomorhp from " + namadatabaselocal + ".daftar_kontak where idsipp =%s and jabatan in ('hakim', 'ketua', 'wakil')"
                                cursorlocal.execute(sqllocal_cek_hp, (id_hakim,))
                                result_hp_hakim = cursorlocal.fetchall()
                                jumrow_hp_hakim = cursorlocal.rowcount
                                if jumrow_hp_hakim > 0:
                                    for data_hp_hakim in result_hp_hakim:
                                        nomorhp_hakim = data_hp_hakim[1]
                                        if not nomorhp_hakim is None:
                                            cek_format_no_hp = nomorhp_hakim[:1]
                                            if cek_format_no_hp == "+":
                                                no_wa = nomorhp_hakim.replace('+', '', 1)
                                            elif cek_format_no_hp == "0":
                                                no_wa = nomorhp_hakim.replace('0', '62', 1)
                                            else:
                                                no_wa = nomorhp_hakim

                                            jawaban = "*Pengingat PHS :*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nomor Perkara : *" + nomorperkara + "* belum PHS lebih dari 3 hari !" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"

                                            send_whatsapp_msg(no_wa, jawaban)
                                            sleep(1)
                                            jkt = pytz.timezone('Asia/Jakarta')
                                            waktu_now = datetime.now(jkt)
                                            pengingat = "phs"
                                            koneklocal = koneksilocal()
                                            cursorlocal = koneklocal.cursor()
                                            sqllocal_insert_data_lokal = "insert into reminder_sipp(user_sipp,nohp,validasi,wa,dikirim)values(%s,%s,%s,%s,%s)"
                                            cursorlocal.execute(sqllocal_insert_data_lokal,
                                                                (id_hakim, no_wa, pengingat, jawaban, waktu_now))
                                            koneklocal.commit()
                                            koneklocal.close()
                                        else:
                                            koneklocal.commit()
                                            koneklocal.close()
                                            print("Nomor HP Ketua salah format")
                                            pass
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass

        else:
            pass

    except Exception as e:
        print(e)
        pass


def cek_input_sidang():
    print("Cek Input Sidang")
    try:
        koneksipp = koneksisipp()
        cursorsidang = koneksipp.cursor()
        sql_cek_sidang = "select a.perkara_id,a.nomor_perkara,b.panitera_id,b.panitera_nama from perkara a left join perkara_panitera_pn b on a.perkara_id=b.perkara_id where b.aktif='Y' and a.proses_terakhir_id=200"
        cursorsidang.execute(sql_cek_sidang, ())
        result_cek_sidang = cursorsidang.fetchall()
        jumrow_cek_sidang = cursorsidang.rowcount
        if jumrow_cek_sidang > 0:
            global data_cek_sidang
            for data_cek_sidang in result_cek_sidang:
                perkara_id = data_cek_sidang[0]
                nomorperkara = data_cek_sidang[1]
                id_panitera = data_cek_sidang[2]
                nama_panitera = data_cek_sidang[3]

                koneksipp = koneksisipp()
                cursorsidang_id = koneksipp.cursor()
                sql_cek_sidang_per_id = "select max(tanggal_sidang) as tgl from perkara_jadwal_sidang where perkara_id=%s"
                cursorsidang_id.execute(sql_cek_sidang_per_id, (perkara_id,))
                result_cek_sidang_per_id = cursorsidang_id.fetchall()
                jumrow_cek_sidang_per_id = cursorsidang_id.rowcount
                if jumrow_cek_sidang_per_id > 0:
                    global tglsidang
                    for tglsidang in result_cek_sidang_per_id:
                        tgl_sidang_per_id = tglsidang[0]

                        jkt = pytz.timezone('Asia/Jakarta')
                        waktu_now = datetime.now(jkt)
                        waktu_now_str = datetime.strftime(waktu_now, "%Y,%m,%d")
                        waktu_sekarang = datetime.strptime(waktu_now_str, '%Y,%m,%d')

                        tglsidang_format_indo = datetime.strftime(tgl_sidang_per_id, "%d-%m-%Y")

                        tglsidang_perk_id = datetime.strftime(tgl_sidang_per_id, "%Y,%m,%d")
                        tglsidang_perk_id_object = datetime.strptime(tglsidang_perk_id, '%Y,%m,%d')

                        selisih = abs(waktu_sekarang - tglsidang_perk_id_object)
                        diff = selisih.days

                        if diff < -2:
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            sql_cek_data_sudah_kirim = " select user_sipp,validasi,max(dikirim) as tgl from " + namadatabaselocal + ".reminder_sipp where validasi='sidang' and user_sipp=%s and datediff(curdate(),dikirim)=0"
                            cursorlocal.execute(sql_cek_data_sudah_kirim, (id_panitera,))
                            result_cek_pengingat = cursorlocal.fetchall()
                            global validasi_cek_input_sidang
                            for validasi_cek_input_sidang in result_cek_pengingat:
                                validasi = validasi_cek_input_sidang[1]
                                if validasi is None:
                                    cursorlocal = koneklocal.cursor()
                                    sqllocal_cek_hp = "select idsipp, nomorhp from " + namadatabaselocal + ".daftar_kontak where idsipp =%s and jabatan in ('panitera', 'pp')"
                                    cursorlocal.execute(sqllocal_cek_hp, (id_panitera,))
                                    result_hp_panitera = cursorlocal.fetchall()
                                    jumrow_hp_panitera = cursorlocal.rowcount
                                    if jumrow_hp_panitera > 0:
                                        global hppanitera
                                        for hppanitera in result_hp_panitera:
                                            nomorhp_panitera = hppanitera[1]
                                            if not nomorhp_panitera is None:
                                                cek_format_no_hp = nomorhp_panitera[:1]
                                                if cek_format_no_hp == "+":
                                                    no_wa = nomorhp_panitera.replace('+', '', 1)
                                                elif cek_format_no_hp == "0":
                                                    no_wa = nomorhp_panitera.replace('0', '62', 1)
                                                else:
                                                    no_wa = nomorhp_panitera

                                                jawaban = "*Pengingat Tundaan Sidang :*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Nomor Perkara : *" + nomorperkara + "*  " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "PP : *" + nama_panitera + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tundaan Sidang Belum diisi !" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang terakhir kali dilaksanakan kemarin pada tanggal : " + str(
                                                    tglsidang_format_indo) + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Pesan Percobaan  otomatis dikirim oleh " + namapa + "_ \n"
                                                send_whatsapp_msg(no_wa, jawaban)
                                                sleep(1)
                                                jkt = pytz.timezone('Asia/Jakarta')
                                                waktu_now = datetime.now(jkt)
                                                pengingat = "sidang"
                                                koneklocal = koneksilocal()
                                                cursorlocal = koneklocal.cursor()
                                                sqllocal_insert_data_lokal = "insert into reminder_sipp(user_sipp,nohp,validasi,wa,dikirim)values(%s,%s,%s,%s,%s)"
                                                cursorlocal.execute(sqllocal_insert_data_lokal,
                                                                    (id_panitera, no_wa, pengingat, jawaban, waktu_now))
                                                koneklocal.commit()
                                                koneklocal.close()
                                            else:
                                                pass
                                    else:
                                        pass
                                else:
                                    pass
                        else:
                            pass
                else:
                    pass
        else:
            pass
    except Exception as e:
        print(e)
        pass


'''
def cek_sudah_materai_belum_putus()
    try:

    except Exception as e:
        print(e)
        pass
'''

jkt = pytz.timezone('Asia/Jakarta')
sa_time = datetime.now(jkt)
jamSekarang = sa_time.strftime('%H')

if int(jamSekarang) >= int(0) and int(jamSekarang) <= int(12):
    ucapan = "Selamat Pagi"

elif int(jamSekarang) >= int(12) and int(jamSekarang) <= int(15):
    ucapan = "Selamat Siang"

elif int(jamSekarang) >= int(15) and int(jamSekarang) <= int(21):
    ucapan = "Selamat Sore"

else:
    ucapan = "Selamat Malam"


# fungsi mengambil pesan terakhir dari

def chat_history():
    text_bubbles = browser.find_elements_by_class_name("message-in")  # message-in = receiver, message-out = sender
    tmp_queue = []
    try:
        for bubble_ijo in text_bubbles:
            msg_texts = bubble_ijo.find_elements_by_class_name("copyable-text")
            for msg in msg_texts:
                tmp_queue.append(msg.text.lower())

        if len(tmp_queue) > 0:
            return tmp_queue[-1]  # Tampung pesan masuk ke antrian tmp_queue

    except StaleElementReferenceException as e:
        print(str(e))
        pass


while True:
    date_now2 = datetime.now()
    # FUNGSI NOTiFIKASI WHATSAPP UNTUK INFO PERKARA
    print(date_now2)
    cek_notif_outbox()
    cek_notif_outbox_group()
    
    #############################################
    koneklocal_jam = koneksilocal()
    cursor_jam = koneklocal_jam.cursor()

    #cari nomor hp untuk reminder siang dan sore hari
    cursor_jam.execute("SELECT * FROM setting_notif_jsp")
    result_jam = cursor_jam.fetchall()
    jumlahrow_jam = cursor_jam.rowcount

    global tabel_jam
    for urutan_jam, tabel_jam in enumerate(result_jam, start=0):
        id_jam=tabel_jam[0]
        jam=tabel_jam[1]
        menit=tabel_jam[2]
        status_jam=tabel_jam[3]
    
        #print(jam)
        #print(menit)
        #kirim pemberitahuan di jam 08.01 pagi    
        if date_now2.hour == int(jam) and date_now2.minute == int(menit) and status_jam == "notifikasi":
            notif_sidang_jsp()
            notif_sidang_pp()
            notif_sidang_hakim()
            #biar perulangan fungsi diatas cuma 1x 1 menit
            print("Delay 60 detik, untuk NOTIFIKASI Sidang")



            #name = browser.find_element_by_class_name(_TEXTBOX_).text  # Contactname _6xQdq
            #if name == "Papas":
                #pass
                #names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                #for name in names:
                    #person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                    #person.click()
            #else:
                #names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                #for name in names:
                    #person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                    #person.click()

            time.sleep(60)
            pass
            
        if date_now2.hour == int(jam) and date_now2.minute == int(menit) and status_jam == "peringatan":
            notif_sidang_jsp()
            #biar perulangan fungsi diatas cuma 1x 1 menit
            

            
            
    koneklocal_jam.commit()
    koneklocal_jam.close()
    #############################################
    
    
    daftarbaru()
    daftarbaru_ecourt()
    sidang_notif()
    cek_ac_terbit()
    cek_ac_terbit_ecourt()
    # cek_psp_ct()
    # cek_psp_volunter()
    # cek_psp_kontesius_non_ct_non_verstek()
    # cek_psp_kontesius_non_ct_verstek()
    # cek_pmh()
    # cek_penetapan()
    # cek_phs()
    # cek_input_sidang()
    # cek_sudah_materai_belum_putus()
    # cek_sudah_putus_belum_materai()

    unread = browser.find_elements_by_class_name(_UNREAD_)
    name, message = '', ''
    if len(unread) > 0:
        # print("pesan lebih dari 2 = "+str(unread))
        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(ele, 0, -20)  # geser kekiri dari titik hijau

        # di klik 2 kali karena kadang kadang whatsapp web gak respon kalau nggak 2 kali
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            pass
        try:
            name = browser.find_element_by_class_name(_NAMAKONTAK_).text  # Contactname _6xQdq
            if name == "Papas":
                pass
                names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                for name in names:
                    person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                    person.click()
            else:
                message = chat_history()  # isi pesan di tampungan tmp_queue
                nomorhppihak = re.sub('[^0-9]', '', name)
                nomorhppihakfull = nomorhppihak.replace('62', '0', 2)
                print(message)
                # simpan pesan masuk kedalam database lokal
                if message == "":
                    text_box = browser.find_element_by_class_name(_TEXTBOX_)
                    text_box.click()
                    response = "Maaf! *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa mengenali pesan text saja. *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa menjawab pesan yang sesuai dengan kata kunci saja. Untuk melihat kata kunci yang tersedia silahkan ketik *INFO*\n"
                    text_box.send_keys(response)

                    names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                    for name in names:
                        person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                        person.click()

                else:
                    koneklocal = koneksilocal()
                    if koneklocal.is_connected():
                        cursorlocal = koneklocal.cursor()
                        no_wa = re.sub('[^0-9]', '', name)
                        sqllocal = "insert into inbox(no_wa,isi_pesan,tgl_input) values (%s,%s,%s)"
                        cursorlocal.execute(sqllocal, (name, message, sa_time))
                        if cursorlocal.lastrowid:
                            print('last insert id cek wa masuk', cursorlocal.lastrowid)
                        else:
                            print('last insert id not found')

                    koneklocal.commit()
                    koneklocal.close()

                    pesan = message.split("#")
                    print(len(pesan))
                    if len(pesan) == 1:
                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        text_box.click()
                        pesan1 = pesan[0].lower()
                        koneklocal = koneksilocal()
                        cursorlocal = koneklocal.cursor()
                        querykatakunci = "select * from kata_kunci where kata_kunci=%s"
                        cursorlocal.execute(querykatakunci, (pesan1,))
                        results = cursorlocal.fetchall()

                        row = cursorlocal.rowcount
                        if row >= 1:
                            global katakunciumum
                            for katakunciumum in results:
                                ganti = katakunciumum[2].replace('|', '~')
                                for part in ganti.split('~'):
                                    action = webdriver.common.action_chains.ActionChains(browser)
                                    text_box.send_keys(part)
                                    action.key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()

                                text_box.send_keys(" \n")
                                # kirim = browser.find_element_by_xpath('// *[ @ id = "main"] / footer / div[1] / div[3] / button')
                                # kirim.click()
                                #koneklocal.commit()
                                koneklocal.close()
                        else:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            response = "Kata Kunci tidak dikenali, untuk mulai menggunakan layanan " + _NAMASINGKATANAPLIKASI_ + " kirim pesan dengan kata kunci *INFO* \n"
                            text_box.send_keys(response)

                    elif len(pesan) == 2:
                        pesan1 = pesan[0].lower()
                        pesan2 = pesan[1].lower()
                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        text_box.click()
                        if 'info' in pesan1:
                            koneksipp = koneksisipp()
                            cursor = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sql = "select perkara_id,nomor_perkara,pihak1_text,pihak2_text,para_pihak,alur_perkara_id,tanggal_pendaftaran,jenis_perkara_id,jenis_perkara_nama,tahapan_terakhir_text,proses_terakhir_text from perkara where nomor_perkara =%s"
                            cursor.execute(sql, (no_perk_lengkap,))
                            results = cursor.fetchall()
                            jumrowperkara = cursor.rowcount
                            print(str(jumrowperkara))
                            if jumrowperkara == 1:
                                global data
                                for data in results:
                                    # print(data)
                                    nomorperkara = data[1]
                                    cursorphone = koneksipp.cursor()
                                    sqltelepon = "select telepon from pihak where telepon=%s"
                                    cursorphone.execute(sqltelepon, (nomorhppihakfull,))
                                    hasilphone = cursorphone.fetchall()
                                    jumphone = cursorphone.rowcount
                                    if "0" in str(jumphone):
                                        namap = "_Disamarkan_"
                                        namat = "_Disamarkan_"
                                    else:
                                        namap = data[2]
                                        namat = data[3]
                                    tgldaftar = str(data[6])
                                    namajnsperk = data[8]
                                    tahapan_terakhir_text = data[9]
                                    proses_terakhir = data[10]
                                    jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T :* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Daftar :* " + tgldaftar + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Jenis Perkara :* " + namajnsperk + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tahapan Perkara:* " + tahapan_terakhir_text + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Proses Perkara :* " + proses_terakhir + " \n"
                                    text_box.send_keys(jawaban)
                                    koneksipp.close()
                            else:
                                jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* tidak ditemukan, pastikan Anda memasukan nomor perkara dengan benar." + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Format penulisan yang benar adalah *info#nomorperkara*" + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Contoh Nomor Perkara : *123/Pdt.G/2020/PA.Pas* menjadi *info#123/Pdt.G/2020/PA.Pas* \n"
                                text_box.send_keys(jawaban)
                                koneksipp.close()

                        elif 'sidang' in pesan1:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            koneksipp = koneksisipp()
                            cursor = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sqlsidang = "SELECT MAX(tanggal_sidang) as tgl_sidang,urutan FROM perkara_jadwal_sidang WHERE perkara_id=(select perkara_id from perkara where nomor_perkara = %s ) AND tanggal_sidang >= CURDATE()"
                            cursor.execute(sqlsidang, (no_perk_lengkap,))
                            results1 = cursor.fetchall()
                            jumrowsidang = cursor.rowcount
                            # print(str(jumrowsidang))
                            sqltahapansidang = "select tahapan_terakhir_text from perkara where perkara_id=(select perkara_id from perkara where nomor_perkara = %s)"
                            cursor.execute(sqltahapansidang, (no_perk_lengkap,))
                            results2 = cursor.fetchall()
                            jumrowtahapansidang = cursor.rowcount
                            global datasidang
                            for datasidang in results1:
                                # print(datasidang)
                                nomorperkara = no_perk_lengkap
                                tglsidang = datasidang[0]
                                # print(str(tglsidang))
                                urutansidang = str(datasidang[1])
                                if str(tglsidang) == "None":
                                    jawaban = "Nomor Perkara : *" + no_perk_lengkap + "* _Belum ada jadwal sidang_ \n"
                                    text_box.send_keys(jawaban)
                                else:
                                    jawaban = "Nomor Perkara : *" + nomorperkara + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tanggal Sidang : *" + str(
                                        tglsidang) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Sidang Ke : *" + str(
                                        urutansidang) + "* \n"
                                    text_box.send_keys(jawaban)
                            koneksipp.close()
                        elif 'akta' in pesan1:
                            print("cek_akta")
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            koneksipp = koneksisipp()
                            cursorakta = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sqlakta = "select a.perkara_id as perkaraid,a.pihak1_text,a.pihak2_text,b.perkara_id as perkaraid_akta, b.nomor_akta_cerai,b.tgl_akta_cerai as tgl_akta,a.proses_terakhir_text from perkara a left join perkara_akta_cerai b on a.perkara_id=b.perkara_id where a.perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
                            cursorakta.execute(sqlakta, (no_perk_lengkap,))
                            results = cursorakta.fetchall()
                            jumrowac = cursorakta.rowcount
                            print(str(jumrowac))
                            if jumrowac == 0:
                                jawaban = "Nomor Perkara: " + no_perk_lengkap + "  _Data tidak ditemukan di database_ \n"
                                text_box.send_keys(jawaban)
                            else:
                                global dataac
                                for dataac in results:
                                    nomorperkara = no_perk_lengkap
                                    cursorphone = koneksipp.cursor()
                                    sqltelepon = "select telepon from pihak where telepon=%s"
                                    cursorphone.execute(sqltelepon, (nomorhppihakfull,))
                                    hasilphone = cursorphone.fetchall()
                                    jumphone = cursorphone.rowcount
                                    if "0" in str(jumphone):
                                        namap = "_Disamarkan_"
                                        namat = "_Disamarkan_"
                                    else:
                                        namap = dataac[1]
                                        namat = dataac[2]

                                    nomoraktacerai = dataac[4]
                                    tglac = str(dataac[5])
                                    # print(tglac)
                                    if "None" in tglac:
                                        jawaban = "Nomor Perkara: " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Akta Cerai Belum Terbit* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tahapan Proses Perkara : *" + \
                                                  dataac[6] + "* \n"
                                        text_box.send_keys(jawaban)
                                    else:
                                        jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama P :* " + namap + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nama T :* " + namat + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Nomor Akta Cerai :* " + nomoraktacerai + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Akta Cerai :* " + tglac + " \n"
                                        text_box.send_keys(jawaban)
                                        # print(jawaban)
                            koneksipp.close()
                        elif 'putusan' in pesan1:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            # pesan2_split = pesan2.split("#", 1)
                            # getInfo(pesan1,pesan2)
                            koneksipp = koneksisipp()
                            cursor = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sql = "SELECT b.tanggal_putusan, case b.status_putusan_id when 62 then 'dikabulkan' when 63 then 'ditolak' when 64 then 'tidak dapat diterima' when 65 then 'digugurkan' when 66 then 'dicoret dari register' when 67 then 'dicabut' when 7 then 'dicabut' else '-' end as status_putusan,a.proses_terakhir_text as tahapan FROM perkara a left join perkara_putusan b on a.perkara_id=b.perkara_id WHERE a.perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
                            cursor.execute(sql, (no_perk_lengkap,))
                            resultsputusan = cursor.fetchall()
                            jumrowput = cursor.rowcount
                            # print(str(jumrowput))
                            if jumrowput == 0:
                                jawaban = "Nomor Perkara :" + nomorperkara + " tidak ditemukan di database \n"
                                text_box.send_keys(jawaban)
                            else:
                                global dataputusan
                                for dataputusan in resultsputusan:
                                    # print(dataputusan)
                                    nomorperkara = no_perk_lengkap
                                    tglputusan = str(dataputusan[0])
                                    statusputusan = dataputusan[1]
                                    tahapanputusan = dataputusan[2]
                                    if "None" in tglputusan:
                                        jawaban = "Perkara Nomor " + nomorperkara + " *Belum Putus* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "Tahapan Perkara : *" + tahapanputusan + "* \n"
                                        text_box.send_keys(jawaban)
                                    else:
                                        jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tgl Putusan :* " + tglputusan + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Status :* " + statusputusan + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Tahapan Perkara :* " + tahapanputusan + " \n"
                                        text_box.send_keys(jawaban)
                            koneksipp.close()
                        elif 'keuangan' in pesan1:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            # pesan2_split = pesan2.split("#", 1)
                            # getInfo(pesan1,pesan2)
                            koneksipp = koneksisipp()
                            cursor = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sql = "SELECT SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL)THEN jumlah ELSE 0 END) AS total_panjar,SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS total_pengeluaran, SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END)-SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS sisa FROM perkara_biaya WHERE perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
                            cursor.execute(sql, (no_perk_lengkap,))
                            resultskeuangan = cursor.fetchall()
                            jumrowkeu = cursor.rowcount
                            # print(str(jumrowkeu))
                            if jumrowkeu == 0:
                                jawaban = "Data Keuangan Perkara dengan Nomor Perkara :*" + nomorperkara + "* tidak ditemukan di database \n"
                                text_box.send_keys(jawaban)
                            else:
                                global datakeuangan
                                for datakeuangan in resultskeuangan:
                                    locale.setlocale(locale.LC_NUMERIC, '')
                                    nomorperkara = no_perk_lengkap
                                    total_panjar = str(datakeuangan[0])
                                    # print(number_format(int(float(total_panjar)),2))
                                    if "None" in total_panjar:
                                        jawaban = "Data Keuangan Perkara dengan Nomor Perkara : *" + nomorperkara + "* tidak ditemukan \n"
                                        text_box.send_keys(jawaban)
                                    else:
                                        totalpanjar = float(total_panjar)
                                        total_pengeluaran = str(datakeuangan[1])
                                        sisa = str(datakeuangan[2])
                                        jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Panjar :* Rp." + number_format(
                                            int(totalpanjar),
                                            2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Pengeluaran :* Rp." + number_format(
                                            int(float(total_pengeluaran)),
                                            2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Sisa Panjar Perkara :* Rp." + number_format(
                                            int(float(sisa)), 2) + " \n"
                                        text_box.send_keys(jawaban)
                            koneksipp.close()

                        elif 'panjar' in pesan1:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            # pesan2_split = pesan2.split("#", 1)
                            # getInfo(pesan1,pesan2)
                            koneksipp = koneksisipp()
                            cursor = koneksipp.cursor()
                            pecah_perk = pesan2.split("/", 3)
                            no_perk = pecah_perk[0]
                            #no_perk = no_perk.lstrip("0")
                            # jns_perk = pecah_perk[1][4:].upper()
                            jns_perk = pecah_perk[1].upper()
                            jns_perk = jns_perk.replace("PDT.", "Pdt.")
                            thn_perk = pecah_perk[2]
                            no_perk_lengkap = no_perk + "/" + jns_perk + "/" + thn_perk + "/" + kodePa
                            sql = "SELECT SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL)THEN jumlah ELSE 0 END) AS total_panjar,SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS total_pengeluaran, SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END)-SUM(CASE WHEN tahapan_id=10 AND jenis_transaksi=-1 AND (pihak_ke=1 OR pihak_ke IS NULL) THEN jumlah ELSE 0 END) AS sisa FROM perkara_biaya WHERE perkara_id=(select perkara_id from perkara where nomor_perkara=%s)"
                            cursor.execute(sql, (no_perk_lengkap,))
                            resultskeuangan = cursor.fetchall()
                            jumrowkeu = cursor.rowcount
                            # print(str(jumrowkeu))
                            if jumrowkeu == 0:
                                jawaban = "Data Keuangan Perkara dengan Nomor Perkara :*" + nomorperkara + "* tidak ditemukan di database \n"
                                text_box.send_keys(jawaban)
                            else:
                                global datapanjar
                                for datapanjar in resultskeuangan:
                                    locale.setlocale(locale.LC_NUMERIC, '')
                                    nomorperkara = no_perk_lengkap
                                    total_panjar = str(datapanjar[0])
                                    # print(number_format(int(float(total_panjar)),2))
                                    if "None" in total_panjar:
                                        jawaban = "Data Keuangan Perkara dengan Nomor Perkara : *" + nomorperkara + "* tidak ditemukan \n"
                                        text_box.send_keys(jawaban)
                                    else:
                                        totalpanjar = float(total_panjar)
                                        total_pengeluaran = str(datapanjar[1])
                                        sisa = str(datapanjar[2])
                                        jawaban = "*Nomor Perkara :* " + nomorperkara + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Panjar :* Rp." + number_format(
                                            int(totalpanjar),
                                            2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Total Pengeluaran :* Rp." + number_format(
                                            int(float(total_pengeluaran)),
                                            2) + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*Sisa Panjar Perkara :* Rp." + number_format(
                                            int(float(sisa)), 2) + " \n"
                                        text_box.send_keys(jawaban)
                            koneksipp.close()

                        else:
                            text_box = browser.find_element_by_class_name(_TEXTBOX_)
                            text_box.click()
                            response = "Kata Kunci tidak dikenali, untuk mulai menggunakan layanan " + _NAMASINGKATANAPLIKASI_ + " kirim pesan dengan kata kunci *INFO* \n"
                            text_box.send_keys(response)

                    elif len(pesan) == 4:
                        locale.setlocale(locale.LC_NUMERIC, '')
                        pesan1 = pesan[0].lower().replace(" ", "").title()
                        pesan2 = pesan[1].lower().replace(" ", "").title()
                        pesan3 = pesan[2].lower().replace(" ", "").title()
                        pesan4 = pesan[3].lower().replace(" ", "").title()
                        jenis_perk_gugat = ['cg', 'paw', 'aua', 'diska', 'haa', 'isbat', 'poligami']
                        jenis_perk_talak = ['ct']
                        if pesan3:
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                            cursorlocal.execute(sqllocal, (pesan3,))
                            resultspesan3 = cursorlocal.fetchall()
                            global pglp
                            for pglp in resultspesan3:
                                nilai_biayap = pglp[1]
                            koneklocal.commit()
                            koneklocal.close()
                        if pesan4:
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                            cursorlocal.execute(sqllocal, (pesan4,))
                            resultspesan4 = cursorlocal.fetchall()
                            global pglt
                            for pglt in resultspesan4:
                                nilai_biayat = pglt[1]
                            koneklocal.commit()
                            koneklocal.close()

                        koneklocal = koneksilocal()
                        cursorlocal = koneklocal.cursor()
                        sqllocal = "select SUM(biaya) as jumlahkompbiaya from komponen_biaya where status ='aktif' "
                        cursorlocal.execute(sqllocal)
                        resultskompbiaya = cursorlocal.fetchall()
                        global komponenbiaya
                        for komponenbiaya in resultskompbiaya:
                            nilai_komponen_biaya = komponenbiaya[0]
                        koneklocal.commit()
                        koneklocal.close()

                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        text_box.click()
                        if str(pesan2) in jenis_perk_gugat:
                            total_biaya = (nilai_biayap * _PERKALIAN_BIAYA_P_) + (
                                    nilai_biayat * _PERKALIAN_BIAYA_T_) + nilai_komponen_biaya
                        else:
                            total_biaya = (nilai_biayap * _PERKALIAN_BIAYA_P_) + (
                                    nilai_biayat * _PERKALIAN_BIAYA_T_) + nilai_komponen_biaya
                        response = "Perkiraan Panjar Biaya yang harus dipersiapkan adalah : *Rp." + number_format(
                            int(float(total_biaya)),
                            2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*PERHATIAN!* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Perhitungan Panjar ini bersifat  Perkiraan, bisa berubah sewaktu waktu, untuk total panjar yang benar ditentukan saat anda melakukan Pendaftaran Perkara di kantor " + namapa + "_ \n"
                        text_box.send_keys(response)
                    elif len(pesan) == 5:
                        locale.setlocale(locale.LC_NUMERIC, '')
                        pesan1 = pesan[0].lower().replace(" ", "").title()
                        pesan2 = pesan[1].lower().replace(" ", "").title()
                        pesan3 = pesan[2].lower().replace(" ", "").title()
                        pesan4 = pesan[3].lower().replace(" ", "").title()
                        jenis_perk_gugat = ['cg', 'paw', 'aua', 'diska', 'haa', 'isbat', 'poligami']
                        jenis_perk_talak = ['ct']
                        if pesan3:
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                            cursorlocal.execute(sqllocal, (pesan3,))
                            resultspesan33 = cursorlocal.fetchall()
                            global pglp2
                            for pglp2 in resultspesan33:
                                nilai_biayap = pglp2[1]
                            koneklocal.commit()
                            koneklocal.close()
                        if pesan4:
                            koneklocal = koneksilocal()
                            cursorlocal = koneklocal.cursor()
                            sqllocal = "select kecamatan,nilai from radius where kecamatan=%s limit 1"
                            cursorlocal.execute(sqllocal, (pesan4,))
                            resultspesan4 = cursorlocal.fetchall()
                            global pglt2
                            for pglt2 in resultspesan4:
                                nilai_biayat = pglt2[1]
                            koneklocal.commit()
                            koneklocal.close()

                        koneklocal = koneksilocal()
                        cursorlocal = koneklocal.cursor()
                        sqllocal = "select SUM(biaya) as jumlahkompbiaya from komponen_biaya where status ='aktif' "
                        cursorlocal.execute(sqllocal)
                        resultskompbiaya = cursorlocal.fetchall()
                        global komponenbiaya2
                        for komponenbiaya2 in resultskompbiaya:
                            nilai_komponen_biaya = komponenbiaya2[0]
                        koneklocal.commit()
                        koneklocal.close()

                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        text_box.click()
                        if str(pesan2) in jenis_perk_gugat:
                            total_biaya = (nilai_biayap * _PERKALIAN_BIAYA_P_) + (
                                    nilai_biayat * _PERKALIAN_BIAYA_T_) + nilai_komponen_biaya
                        else:
                            total_biaya = (nilai_biayap * _PERKALIAN_BIAYA_P_) + (
                                    nilai_biayat * _PERKALIAN_BIAYA_T_) + nilai_komponen_biaya
                        response = "Perkiraan Panjar Biaya yang harus dipersiapkan adalah : *Rp." + number_format(
                            int(float(total_biaya)),
                            2) + "* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + " " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "*PERHATIAN!* " + Keys.SHIFT + Keys.ENTER + Keys.SHIFT + "_Perhitungan Panjar ini bersifat  Perkiraan, bisa berubah sewaktu waktu, untuk total panjar yang benar ditentukan saat anda melakukan Pendaftaran Perkara di kantor " + namapa + "_ \n"
                        text_box.send_keys(response)
                    else:
                        text_box = browser.find_element_by_class_name(_TEXTBOX_)
                        text_box.click()
                        response = "Maaf! *" + _NAMASINGKATANAPLIKASI_ + "* tidak bisa menjawab pesan Anda. *" + _NAMASINGKATANAPLIKASI_ + "* hanya bisa menjawab pesan yang sesuai dengan kata kunci saja. Untuk melihat kata kunci yang tersedia silahkan ketik *INFO*\n"
                        text_box.send_keys(response)

                    sleep(3)  # tunda 1 detik untuk memarkir Kursor
                    names = [namaakunparkircursor]  # akun parkir untuk cursor setelah eksekusi pesan
                    for name in names:
                        person = browser.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                        person.click()

        except Exception as e:
            print(e)
            pass

    sleep(2)  # 3 detik sleep agar tidak terlalu cepat
