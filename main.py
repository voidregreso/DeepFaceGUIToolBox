import os
import sys

import urllib3
import requests
import cv2
import ventana
import proxy_dlg
import conf_routine

from requests import exceptions
from urllib import error
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, \
    QMessageBox
from PyQt5.QtCore import Qt, QThread, QMutex, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
bkends = ['retinaface', 'mtcnn', 'opencv', 'ssd', 'dlib', 'mediapipe']

oimg = ''
aimg = ''
bimg = ''


def analyze(img_path, dbkend):
    try:
        dic = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race', 'emotion'], detector_backend=dbkend)
        anos = dic['age']
        genero = dic['gender']
        raza = dic['race']
        emo = dic['emotion']
        area = dic['region']
        d_raza = dic['dominant_race']
        d_emo = dic['dominant_emotion']
        return True, anos, genero, raza, emo, area, d_raza, d_emo, ''
    except Exception as e:
        print('Error occurred: ' + str(e))
        return False, None, None, None, None, None, None, None, str(e)


def matchdos(img_p1, img_p2, modulo):
    try:
        verdad = DeepFace.verify(img1_path=img_p1, img2_path=img_p2, model_name=modulo)
        print(verdad)
        estado = verdad['verified']
        sim = 100 - float(verdad['distance']) * 100.0
        return estado, sim, ''
    except Exception as e:
        print('Error occurred: ' + str(e))
        return False, 0.0, str(e)


def abrir_archivo(ui, mw, idx):
    global oimg, aimg, bimg
    fileName, fileType = QFileDialog.getOpenFileName(mw, "Choose your file", os.getcwd(),
                                                     "Picture Files(*.jpg;*.png;*.bmp);;All Files(*)")
    if len(fileName.strip()) != 0:
        imgb = QPixmap()
        imgb.load(fileName)
        itm = QGraphicsPixmapItem(imgb)
        scene = QGraphicsScene()
        scene.addItem(itm)
        if idx == 0:
            ui.img_cargado.setScene(scene)
            ui.img_cargado.fitInView(QGraphicsPixmapItem(QPixmap(imgb)))
            oimg = fileName
        elif idx == 1:
            ui.img_izq.setScene(scene)
            ui.img_izq.fitInView(QGraphicsPixmapItem(QPixmap(imgb)))
            aimg = fileName
        elif idx == 2:
            ui.img_dch.setScene(scene)
            ui.img_dch.fitInView(QGraphicsPixmapItem(QPixmap(imgb)))
            bimg = fileName


qmut_1 = QMutex()
qmut_2 = QMutex()


class AnaThread(QThread):
    _signal = pyqtSignal()

    def __init__(self, oi, wui, bke):
        super().__init__()
        self.oi = oi
        self.wui = wui
        self.bke = bke

    def run(self):
        qmut_1.lock()
        self.res, self.anos, self.genero, self.raza, self.emo, \
        self.area, self.d_raza, self.d_emo, self.errmsg = analyze(self.oi, self.bke[self.wui.lista_bkends.currentIndex()])
        qmut_1.unlock()
        self._signal.emit()

    def get_result(self):
        return self.res, self.anos, self.genero, self.raza, self.emo, \
               self.area, self.d_raza, self.d_emo, self.errmsg


class VeriThread(QThread):
    _signal = pyqtSignal()

    def __init__(self, ai, bi, wui, mods):
        super().__init__()
        self.ai = ai
        self.bi = bi
        self.wui = wui
        self.mods = mods

    def run(self):
        qmut_2.lock()
        self.res, self.sim, self.errmsg = matchdos(self.ai, self.bi, self.mods[self.wui.lista_modulos.currentIndex()])
        qmut_2.unlock()
        self._signal.emit()

    def get_result(self):
        return self.res, self.sim, self.errmsg


def show_proc_analyze(ui, thd):
    res, anos, genero, raza, emo, area, d_raza, d_emo, errmsg = thd.get_result()
    ui.statusbar.showMessage('Ready')
    ui.progressBar.setRange(0, 1)
    ui.progressBar.setValue(1)
    if res == True:
        ui.anno.setText(str(anos))
        ui.genero.setText(genero)
        ui.raza.setText(d_raza)
        ui.emocion.setText(d_emo)
        extra_text = 'Possible races & ethnicities: ' + str(raza) + '\n' + 'Possible emotions: ' + str(
            emo) + '\n' + 'Recognized area: ' + str(area)
        ui.textBrowser.setText(extra_text)
        img = cv2.imread(oimg)
        colors = (0, 0, 255)
        cv2.rectangle(img, (area['x'], area['y']), (area['x']+area['w'], area['y']+area['h']),
                      colors, int((img.shape[0] + img.shape[1]) / 320))
        bold = int((img.shape[0]+img.shape[1])/1100)
        cv2.putText(img, d_raza + ' : ' + str(round(raza[d_raza], 2)) + ' %', (int(img.shape[1]/6), int(img.shape[0]*11/12)),
                        cv2.FONT_HERSHEY_COMPLEX, bold, (0, 0, 255), bold * 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x0 = img.shape[1]
        y0 = img.shape[0]
        frame = QImage(img, x0, y0, x0 * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        itm = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(itm)
        ui.img_cargado.setScene(scene)
        ui.img_cargado.fitInView(QGraphicsPixmapItem(QPixmap(pix)))
    else:
        QMessageBox.warning(ui.centralwidget, 'Operation failed', 'Cannot analyze due to: ' + errmsg, QMessageBox.Ok)


def multi_proc_analyze(ui):
    global oimg
    if not (oimg == ''):
        thd = AnaThread(oimg, ui, bkends)
        thd._signal.connect(lambda: show_proc_analyze(ui, thd))
        ui.statusbar.showMessage('In Progress...')
        ui.progressBar.setRange(0, 0)
        thd.start()


def show_proc_veri(ui, thd):
    res, sim, errmsg = thd.get_result()
    ui.statusbar.showMessage('Ready')
    ui.progressBar.setRange(0, 1)
    ui.progressBar.setValue(1)
    if res == True:
        ui.estado.setStyleSheet('color: green')
        ui.estado.setText('Success! Similarity: ' + str(round(sim, 2)) + '%')
    else:
        ui.estado.setStyleSheet('color: red')
        ui.estado.setText('Failed! Similarity: ' + str(round(sim, 2)) + '%')
        if len(errmsg.strip()) != 0:
            QMessageBox.warning(ui.centralwidget, 'Operation failed', 'Cannot verify due to: ' + errmsg,
                                QMessageBox.Ok)


def multi_proc_veri(ui):
    global aimg, bimg
    if (not aimg == '') and (not bimg == ''):
        thd = VeriThread(aimg, bimg, ui, models)
        thd._signal.connect(lambda: show_proc_veri(ui, thd))
        ui.statusbar.showMessage('In Progress...')
        ui.progressBar.setRange(0, 0)
        thd.start()


class ChildWin(QDialog, proxy_dlg.Ui_ProxDlg):
    def __init__(self):
        super(ChildWin, self).__init__()
        self.setupUi(self)


def guardar_conf(dialog):
    enabled = dialog.checo_habil.isChecked()
    proto = 'http' if dialog.radio_http.isChecked() else 'socks'
    ipaddr = dialog.edt_ipaddr.toPlainText().strip()
    puerto = dialog.edt_puerto.toPlainText().strip()
    if len(ipaddr) != 0 and len(puerto) != 0:
        conf_routine.WriteCfg(enabled, proto, ipaddr, puerto)
        dialog.close()
    else:
        QMessageBox.warning(dialog.parentWidget(), 'Error', 'Please input necessary informations!', QMessageBox.Ok)
        dialog.close()


def set_allEnable(dlg, enable):
    dlg.radio_http.setEnabled(enable)
    dlg.radio_socks.setEnabled(enable)
    dlg.edt_puerto.setEnabled(enable)
    dlg.edt_ipaddr.setEnabled(enable)
    dlg.btn_prueba.setEnabled(enable)


def ProbarConexion(dialog):
    urllib3.disable_warnings()
    try:
        requests.get('https://google.com/', verify=False)
        QMessageBox.information(dialog.parentWidget(), 'Tips', 'Test of connection is successful', QMessageBox.Ok)
    except (error.URLError, exceptions.ProxyError, exceptions.SSLError, exceptions.HTTPError, exceptions.ConnectionError) as e:
        QMessageBox.critical(dialog.parentWidget(), 'Error', 'Proxy does not work: ' + str(e), QMessageBox.Ok)


def goto_proxysets():
    dialog = ChildWin()

    dialog.btn_cancel.clicked.connect(lambda: dialog.close())
    dialog.btn_prueba.clicked.connect(lambda: ProbarConexion(dialog))
    enabled, proto, ipaddr, puerto = conf_routine.ReadCfg()
    dialog.checo_habil.setChecked(enabled)
    set_allEnable(dialog, enabled)
    if len(proto) == 0 or len(ipaddr) == 0 or len(puerto) == 0:
        dialog.radio_http.setChecked(True)
        dialog.radio_socks.setChecked(False)
    else:
        if proto == 'http':
            dialog.radio_http.setChecked(True)
            dialog.radio_socks.setChecked(False)
        elif proto == 'socks':
            dialog.radio_http.setChecked(False)
            dialog.radio_socks.setChecked(True)
        dialog.edt_ipaddr.setText(ipaddr)
        dialog.edt_puerto.setText(puerto)

    dialog.btn_ok.clicked.connect(lambda: guardar_conf(dialog))
    dialog.checo_habil.stateChanged.connect(lambda state: set_allEnable(dialog, dialog.checo_habil.isChecked()))
    dialog.show()
    dialog.exec_()

def iniciar_componentes(ui, mw):
    ui.statusbar.showMessage('Ready')
    ui.progressBar.setRange(0, 1)
    ui.actionOpen.triggered.connect(lambda: abrir_archivo(ui, mw, 0))
    ui.sel_btn1.clicked.connect(lambda: abrir_archivo(ui, mw, 1))
    ui.sel_btn2.clicked.connect(lambda: abrir_archivo(ui, mw, 2))
    ui.lista_bkends.addItems(bkends)
    ui.lista_modulos.addItems(models)
    ui.anabtn.clicked.connect(lambda: multi_proc_analyze(ui))
    ui.verificar.clicked.connect(lambda: multi_proc_veri(ui))
    ui.actionExit.triggered.connect(lambda: exit(0))
    ui.actionAcercade.triggered.connect(lambda: QMessageBox.aboutQt(mw, 'About PyQt5'))
    ui.actionProxy.triggered.connect(goto_proxysets)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enabled, proto, ipaddr, puerto = conf_routine.ReadCfg()
    if enabled == False:
        conf_routine.activate(proto, ipaddr, puerto, False)
    else:
        if len(proto) != 0 and len(ipaddr) != 0 and len(puerto) != 0:
            conf_routine.activate(proto, ipaddr, puerto, True)
    MainWindow = QMainWindow()
    MainWindow.setWindowFlags(MainWindow.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    ui = ventana.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
    MainWindow.show()
    iniciar_componentes(ui, MainWindow)
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
