from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUiType
from os import path
import logging
import sys
import spectro_features 
import load
from createDB import read_json

logging.basicConfig(filename="logFile.log",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(20)
MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"task4.ui"))

class MainApp(QtWidgets.QMainWindow,MAIN_WINDOW):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.slider.setEnabled(False)
        self.flag1 = False
        self.flag2 = False
        self.mixedAudioData = None
        self.labels = [self.label, self.label_2]
        self.load1Btn.clicked.connect(lambda: self.loadsong(0))
        self.load2Btn.clicked.connect(lambda: self.loadsong(1))
        self.slider.valueChanged.connect(lambda: self.sliderLabel.setText(str(self.slider.value())+"%"))
        self.searchBtn.clicked.connect(lambda: self.mixer())
        self.audioDatas = [None, None]
        self.audioRates = [None, None]
        self.mixedSongDB = None
        self.similarityResults = []

    def loadsong(self , indx):
        self.statusbar.showMessage("Loading Audio File "+str(indx+1))
        global audFile
        audFile, audFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File "+str(indx+1),filter="*.mp3")
        logger.info("Audio File %s Loaded"%(indx+1))
        
        if audFile == "":
            logger.info("loading cancelled")
            self.statusbar.showMessage("Loading cancelled")
            pass
        else:
            logger.info("Loading data")
            global sampRate , audioData
            try:
                sampRate, audioData = load.readAudio(audFile)
            except:
                self.show_popup("File Not Supported", "Please Select Another File")
                self.statusbar.showMessage("Error Uploading File")
                logger.warning("Error Uploading File")
                return
            
            self.audioDatas[indx] = audioData 
            self.audioRates[indx] = sampRate
            self.labels[indx].setText(audFile.split('/')[-1])
            self.statusbar.showMessage("Loading Done")
            logger.info("Loading Done")
            
        if indx == 0:
            self.flag1 = True
            
        if indx == 1:
            self.flag2 = True
            
        if self.flag1 == self.flag2 == True:
            self.slider.setEnabled(True)
    
    def mixer(self):
        w = self.slider.value()/100.0
        
        if self.flag1 == False and self.flag2 == False:
            self.show_popup("No File Selected", "You Have To Select A File")
            return
        
        if self.flag1 == True and self.flag2 == False:
            self.mixedSongDB = spectro_features.Load_Song("Loaded Song", self.audioDatas[0], self.audioRates[0])
            
        if self.flag1 == False and self.flag2 == True:
            self.mixedSongDB = spectro_features.Load_Song("Loaded Song", self.audioDatas[1], self.audioRates[1])
            
        if self.flag1 == self.flag2 == True: 
            logger.info("Start Mixing 2 songs")
            self.statusbar.showMessage("Mixing")
            try:    
                self.mixedAudioData = (w*self.audioDatas[0] + (1.0-w)*self.audioDatas[1])
            except:
                self.show_popup("Error Mixing", "Please Choose Another File")
                self.statusbar.showMessage("Error Mixing")
                logger.warning("Error Mixing")
                return
            
            self.mixedSongDB = spectro_features.Load_Song("Loaded Song", self.mixedAudioData, self.audioRates[0])
            logger.info("Mixing Done")
            self.statusbar.showMessage("Mixing Done")
        
        self.check_similarity()
    
    def check_similarity(self):
        logger.info("Searching and getting similarities")
        self.statusbar.showMessage("Getting Similarities")
        for songName, songHashes in read_json("db.json"):
            
            spectroDiff = spectro_features.get_hamming(songHashes["spectrogram_Hash"], self.mixedSongDB["Loaded Song"]["spectrogram_Hash"])
            melSpectroDiff = spectro_features.get_hamming(songHashes["melspectrogram_Hash"], self.mixedSongDB["Loaded Song"]["melspectrogram_Hash"])
            mffcDiff = spectro_features.get_hamming(songHashes["mfcc_Hash"], self.mixedSongDB["Loaded Song"]["mfcc_Hash"])
            chromaDiff = spectro_features.get_hamming(songHashes["chroma_stft_Hash"], self.mixedSongDB["Loaded Song"]["chroma_stft_Hash"])
            
            output = (spectroDiff + melSpectroDiff + mffcDiff + chromaDiff)/4
            self.similarityResults.append((songName , output*100))
            
        self.similarityResults.sort(key= lambda x: x[1], reverse=True)
        logger.info("Searching and getting similarities Done")
        self.statusbar.showMessage("Getting Similarities Done")   
        
        self.fill_table()
    
    def fill_table(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["Found Matches", "Percentage"])
        
        logger.info("Showing Results")
        self.statusbar.showMessage("Showing Results")   
        for row in range(len(self.similarityResults)):
            self.tableWidget.insertRow(row)
            
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.similarityResults[row][0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(self.similarityResults[row][1], 2))+"%"))
            
        for col in range(2):
            self.tableWidget.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            self.tableWidget.horizontalHeaderItem(col).setBackground(QtGui.QColor(57, 65, 67))                        
        self.similarityResults.clear()
        
        logger.info("Results Done")
        self.statusbar.showMessage("Results Done")   
    
    def show_popup(self, message, information):
        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText(information)
        x = msg.exec_()    
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()