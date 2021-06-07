import sys
import requests
from PyQt5.QtGui import QIntValidator
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton


class Imdb():
    def vericek(self,url):
        self.url = url
        response = requests.get(self.url)
        html_icerigi = response.content
        soup = BeautifulSoup(html_icerigi, "html.parser")

        self.names = soup.find_all("strong", {"": ""})
        self.points = soup.find_all("div", {"class": "ipl-rating-star small"})
        self.episodes = soup.find_all("div", {"class": "image"})
        self.episode_count = len(self.episodes)
        self.sorted_list = []
        self.isimler = []
        self.puanlar = []
        self.oylar = []
        self.puanlarson = []
        self.sozluk = dict()

        for isim,puan in zip(self.names,self.points):
            isim = isim.text
            puan = puan.text
            puan = puan.strip()
            self.isimler.append(isim)
            self.puanlar.append(float(puan[:3]))
            try:
                self.oylar.append((float(puan[5]) * 1000 + float(puan[7:10])))
            except:
                self.oylar.append((float(puan[5:6]) * 1000 + float(puan[5:8])))
            self.sozluk[isim] = puan[:3]
            if len(self.sozluk) == self.episode_count:
                break
        self.puanlarson = [i*99999+j for (i,j) in zip(self.puanlar,self.oylar)]

    def sort(self,season):
        print("****************\n" + str(season) + ". Sezon\n*******************")
        for i in range(self.episode_count):
            print(self.isimler[self.puanlarson.index(max(self.puanlarson))]
                  + " : " + str(self.puanlar[self.puanlarson.index(max(self.puanlarson))]) +
                "  " + str(self.oylar[self.puanlarson.index(max(self.puanlarson))]))
            self.puanlarson[self.puanlarson.index(max(self.puanlarson))] = 0

imdb = Imdb()
url = "https://www.imdb.com/title/tt1710308/episodes?season="
for i in range(1,9):
    imdb.vericek(url+str(i))
    imdb.sort(i)


"""
class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.label = QLabel("IMDB girin")
        self.txt_imdb = QLineEdit()
        self.btn_getir = QPushButton("Getir")
        self.onlyInt = QIntValidator()
        self.txt_imdb.setValidator(self.onlyInt)

        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.txt_imdb)
        self.v_box.addWidget(self.btn_getir)

        self.btn_getir.clicked.connect(self.getir)

        self.setLayout(self.v_box)
        self.setWindowTitle("IMDB")
        self.show()

    def getir(self):
        imdb = Imdb()
        liste = imdb.func(self.txt_imdb.text())
        for i in liste:
            txt = i[0]+i[1]
            label = QLabel(txt)
            self.v_box.addWidget(label)
"""




app = QApplication(sys.argv)
#pencere = Pencere()
sys.exit(app.exec_())