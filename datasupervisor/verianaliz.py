import csv
import os
import tkinter
from tkinter import Button
import time
from datetime import datetime
import matplotlib.pyplot as plt
#import filesearch
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math
import numpy as np
class dosya_aktar():
    def __init__(self,isim,yol=None):
        self.vericount = 0
        self.defaultpath = os.getcwd() #Default dosya yolu
        self.surelist = []
        self.sensor1 = []
        self.sensor2 = []
        self.anglelist1 = ["0"]
        self.anglelist2 = ["0"]
        self.errorflag = False
        self.peakcount = 0
        self.curtime = 0
        self.peaklist= []
        try:
            os.chdir(yol)
        except:
            print("dir hatası")
#-------------------------------DOSYA AÇILIR-------------------------------------------------------                         
        
        with open(isim,newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')

            for self.r in spm:    # DATA İÇERİSİNDEKİ HER BİR VERİYİ DENETLER
            
                self.veriayir()
                self.hatadetect()
                if len(self.surelist) > 2:
                    self.peakdetect() # PEAK VAR MI ?
                
                #except :
                    #print("Hata, veri doğru ayrılamadı")
                self.vericount+=1
            if self.errorflag == False:
                    print("Hatalı veri bulunamadı ! ")
                    
            inf = "Veri Sayisi : " + str(self.vericount-8)+"\nPeak Sayısı : "+ str(self.peakcount) +\
            "\n Enjeksiyon Başlangıç Peak Time : " + str(self.peaklist[0]) +"\n Enjeksiyon Süresi : "+str(self.peaklist[1])
            if self.peakcount>2:
                print("Maşallaah")
            self.veri_sayisi = self.vericount-8
            self.denetle() #ALINAN VERİLERİ İNCELE
            os.chdir(self.defaultpath) # ANA DOSYA YOLUNA GERİ DÖN
            print(inf)
            
    def veriayir(self,):
            self.a = self.r[0].split(',')   # SURE VERİSİNİ AYIRIR
            if self.vericount>6:  #ilk 6 veri info satırlarıdır
                self.b = self.r[1].split(',')  #SENSOR 2 'nin verilerini ayırır
                self.surelist.append(str(self.a[0]))
                self.sensor1.append(str(self.a[1]))
                self.sensor2.append(str(self.b[0])) #VERİLERİ AYIRIP LİSTELERE KAYDEDER
                            
        
    def hatadetect(self,):
            if self.vericount > 6:
                if float(self.b[0]) > 20 or float(self.a[1]) > 20: # HATALI DURUM KOŞULLARI
                    self.info = "Süre : "+ str(self.a[0]) + "\nSensör 1: " + str(self.a[1]) + \
                                "\nSensör 2 : " + str(self.b[0]) 
                    print(self.info)
                    print("*" * 50)
                    self.hatakayit() #HATALI DURUMU BİR LOG DOSYASINA KAYDEDEN FONKSİYON
                    self.errorflag = True        
    def hatakayit(self,):
            os.chdir(self.defaultpath)
            os.chdir("Errors")
            print(str(datetime.now())[11:16])
            self.filename  = str(datetime.now())[0:10] + "_"+str(datetime.now())[11:13]+ \
                             "-"+ str(datetime.now())[14:16]+".txt"
            
            self.errorlog = open(self.filename,'a+')
            self.errorlog.write(self.info)
            self.errorlog.write('\n' + '*'*50 + '\n')
            self.errorlog.close()
    
    def peakdetect(self,):
        self.fark1 = abs(float(str(self.sensor1[-1]))) - abs(float(str(self.sensor1[-2]))) 
        if self.fark1 > abs(float(str(self.sensor1[-1])))*50/100 :#EĞER BASINÇ FARKI %50 DEN FAZLA DEĞİŞMİŞ İSE
            self.peak()

    def peak(self,):
        self.peakcount +=1
        self.reftime = float(str(self.surelist[-1]))
        self.pressure_time =float(str(self.reftime)) - float(str(self.curtime))
        self.peaklist.append(self.pressure_time)
        self.curtime = self.reftime
        
#-------------------------------GRAFİK ÇİZDİRME-------------------------------------------------------                         
    def plot (self,):  
            """
            inf = ' Sure ' + str(len(self.surelist)) + ' Sens ' + str(len(self.sensor1))
            print(inf)
            print(self.surelist)
            print('----------------')
            print(self.sensor1)
            """
            def draw(name,ccolor,title,xlabel,ylabel,axisx,axisy):
                name.plot(axisx,axisy,color = ccolor)
                name.set_title(title)
                name.set_xlabel(xlabel)
                name.set_ylabel(ylabel)
                
            fig,(sub1,sub3) = plt.subplots(2)
            fig,(sub2,sub4) = plt.subplots(2)
            #fig = plt.figure()
            #sub = fig.add_subplot(111)
            draw(sub1,"darkred","SENSÖR 1","Süre(ms)","Basınç(kPa)",self.surelist,self.sensor1)
            draw(sub2,'darkred',"SENSÖR 2","Süre(ms)","Basınç(kPa)",self.surelist,self.sensor2)
            draw(sub3,'lightblue',"SENSRÖR 1 AÇILAR", "Süre (ms)"," Açı (Derece)",self.surelist,self.anglelist1)
            draw(sub4,'lightblue',"SENSRÖR 2 AÇILAR", "Süre (ms)"," Açı (Derece)",self.surelist,self.anglelist2)
            plt.show()
#-------------------------------VERİLERİN AÇILARINI BULMAK-------------------------------------------------------       
    def acibul1(self,veri):
            if veri < len(self.surelist)-1:
                self.y = float(self.sensor1[veri+1]) - float(self.sensor1[veri])
                self.x = 100*float(self.surelist[veri+1]) - 100*float(self.surelist[veri])
                self.tan = self.y / self.x
                self.angle = math.degrees(math.atan(self.tan))
                self.anglelist1.append(self.angle)
                
    def  acibul2(self,veri):
            if veri < len(self.surelist)-1:
                self.y2 = float(self.sensor2[veri+1]) - float(self.sensor2[veri])
                self.x2 = 100*float(self.surelist[veri+1]) - 100*float(self.surelist[veri])
                self.tan2 = self.y2 / self.x2
                self.angle2 = math.degrees(math.atan(self.tan2))
                self.anglelist2.append(self.angle2)
                
    def acibul(self,x2,x1,t2,t1):
                y = float(x2) - float(x1)
                x = 100*float(t2) - 100*float(t1)
                tan = y/x
                self.aci = math.degrees(math.atan(tan))
#-------------------------------VERİLERİ İNCELE-------------------------------------------------------                   
    def denetle(self,):
             for i in range (0,len(self.surelist)):
                 self.acibul1(i)
                 self.acibul2(i)

#-------------------------------DOSYALARI BULMA MODÜLÜ-------------------------------------------------------      
class sorgu():
    def __init__(self,):
        self.defaultpath = os.getcwd() #Default dosya yolu
        os.chdir("Datas")
        self.temppath = os.getcwd()
        self.gui()
        
    def gui(self,):
        self.penc = Tk()
        self.penc.title("Veri Analiz")
        self.penc.geometry("500x500")
        
        def check():
            if len(self.sorgu) < 1:
                messagebox.showerror("HATA !","Dosya seçmediniz !")
                self.gui()

        def atama(entr):
            self.sorgu = entr
            self.penc.destroy()
            check()
            self.search()
            return None
        def entry():
            self.entr = Entry(self.penc,width = 5)
            self.entr.bind("<Return>", (lambda event: atama(self.entr.get())))
            self.entr.pack()
        def tarih():
            Label(self.penc,text = "İstediğiniz dosya için tarih giriniz (YIL-AY-GUN seklinde)").pack()
            entry()
        def askdir():
            self.sorgu = filedialog.askdirectory(initialdir =self.temppath ,title = "Dosya Seçiniz",)
            self.penc.destroy()
            check()
            self.search()
        Button(self.penc,text = "Tarih ile arama ",command = tarih).pack()
        Button(self.penc,text = "Dosya Bul",command = askdir).pack()

        self.penc.mainloop()
                
    def search(self,):
        try:
            os.chdir("Datas")
        except:
            pass
        try:
            os.chdir(self.sorgu)
        except:
            #messagebox("HATA !", "Tarihi yanlis girdiniz ve ya o tarih de dosya bulunmamakta,tekrar deneyin. ")
            print("hatali")
            self.gui()
            return None
        os.chdir(self.sorgu)
        self.dosya_yolu = os.getcwd()
        self.dosyalar = os.listdir()
        self.files = []
        self.cout = 0
        print("Arama başlatılıyor..")
        time.sleep(0.5)
        for i in self.dosyalar:
            self.check(i)
            if self.flag:
                self.cout +=1
                self.files.append(i)
                self.dosyaid = i[20:26]
                self.dosyah = i[33:39][0:2]
                self.dosyamin = i[33:39][2:4]
                self.dosyas = i[33:39][4:6]
                self.dosyadate = self.dosyah + ":" + self.dosyamin + ":" + self.dosyas
                self.dosyainfo  =  "Dosya No : " + str(self.cout) + "  Saat : "+self.dosyah +":"+self.dosyamin+":"+self.dosyas
                print(self.dosyainfo,"\n")
        self.secim = int(input("Hangi dosyayi istiyorsunuz ?\n"))
        self.dosya = self.files[self.secim-1]
        os.chdir(self.defaultpath)
        
    def check(self,x):
        c = 0
        b = list(x)
        
        vflag = False
        cflag = False
        sflag = False
        self.flag = False
        
        for i in b[::-1]:
            c+=1
            if i == "v":
                vflag = True
            if i == "s" :
                sflag = True
            if i == "c":
                cflag = True
            if c == 3 and vflag and sflag and cflag:
                self.flag = True
                break
    

        

#yenisorgu = sorgu()

#yeni = dosya_aktar(yenisorgu.dosya,yenisorgu.dosya_yolu)
