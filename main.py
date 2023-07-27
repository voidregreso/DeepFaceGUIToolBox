import os
import sys

import cv2
import urllib3
import requests
import ventana
import proxy_dlg
import conf_routine

from requests import exceptions
from urllib import error
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, \
    QMessageBox
from PyQt5.QtCore import Qt, QThread, QMutex, pyqtSignal, QMutexLocker
from PyQt5.QtGui import QPixmap, QImage

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "SFace"]
bkends = ['retinaface', 'mtcnn', 'opencv', 'ssd', 'mediapipe']

oimg = aimg = bimg = ''

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
        with QMutexLocker(qmut_1):
            self.res, self.anos, self.genero, self.raza, self.emo, \
            self.area, self.d_raza, self.d_emo, self.d_gen, self.errmsg = analyze(self.oi, self.bke[self.wui.lista_bkends.currentIndex()])
        self._signal.emit()

    def get_result(self):
        return self.res, self.anos, self.genero, self.raza, self.emo, \
               self.area, self.d_raza, self.d_emo, self.d_gen, self.errmsg


class VeriThread(QThread):
    _signal = pyqtSignal()

    def __init__(self, ai, bi, wui, mods):
        super().__init__()
        self.ai = ai
        self.bi = bi
        self.wui = wui
        self.mods = mods

    def run(self):
        with QMutexLocker(qmut_2):
            self.res, self.sim, self.errmsg = match_two(self.ai, self.bi, self.mods[self.wui.lista_modulos.currentIndex()])
        self._signal.emit()

    def get_result(self):
        return self.res, self.sim, self.errmsg


def analyze(img_path, dbkend):
    try:
        dic = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'race', 'emotion'], detector_backend=dbkend)[0]
        return True, dic['age'], str(dic['gender']), dic['race'], str(dic['emotion']), dic['region'], dic['dominant_race'], dic['dominant_emotion'], dic['dominant_gender'], ''
    except Exception as e:
        print(f'Error occurred: {e}')
        return False, None, None, None, None, None, None, None, None, str(e)

def match_two(img_p1, img_p2, modulo):
    try:
        result = DeepFace.verify(img1_path=img_p1, img2_path=img_p2, model_name=modulo)
        return result['verified'], 100 - float(result['distance']) * 100.0, ''
    except Exception as e:
        print(f'Error occurred: {e}')
        return False, 0.0, str(e)

def abrir_archivo(ui, mw, idx):
    global oimg, aimg, bimg
    fileName, _ = QFileDialog.getOpenFileName(mw, "Choose your file", os.getcwd(), "Picture Files(*.jpg;*.png;*.bmp);;All Files(*)")
    
    if not fileName.strip():
        return

    imgb = QPixmap()
    imgb.load(fileName)
    scene = QGraphicsScene()
    scene.addItem(QGraphicsPixmapItem(imgb))
    viewer = [ui.img_cargado, ui.img_izq, ui.img_dch][idx]
    viewer.setScene(scene)
    viewer.fitInView(QGraphicsPixmapItem(QPixmap(imgb)))

    if idx == 0:
        oimg = fileName
    elif idx == 1:
        aimg = fileName
    elif idx == 2:
        bimg = fileName


def show_proc_analyze(ui, thd):
    res, anos, genero, raza, emo, area, d_raza, d_emo, d_gen, errmsg = thd.get_result()
    ui.statusbar.showMessage('Ready')
    ui.progressBar.setRange(0, 1)
    ui.progressBar.setValue(1)
    if res:
        ui.anno.setText(str(anos))
        ui.genero.setText(d_gen)
        ui.raza.setText(d_raza)
        ui.emocion.setText(d_emo)
        extra_text = f"Possible races & ethnicities: {raza}\nPossible emotions: {emo}\nRecognized area: {area}\nPossible genders: {genero}"
        ui.textBrowser.setText(extra_text)
        img = cv2.imread(oimg)
        colors = (0, 0, 255)
        cv2.rectangle(img, (area['x'], area['y']), (area['x']+area['w'], area['y']+area['h']), colors, (img.shape[0] + img.shape[1]) // 320)
        bold = (img.shape[0] + img.shape[1]) // 1100
        cv2.putText(img, f"{d_raza} : {round(raza[d_raza], 2)} %", (img.shape[1]//6, img.shape[0]*11//12), cv2.FONT_HERSHEY_COMPLEX, bold, (0, 0, 255), bold * 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        itm = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(itm)
        ui.img_cargado.setScene(scene)
        ui.img_cargado.fitInView(QGraphicsPixmapItem(QPixmap(pix)))
    else:
        QMessageBox.warning(ui.centralwidget, 'Operation failed', f'Cannot analyze due to: {errmsg}', QMessageBox.Ok)


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


def guardar_conf(dialog):
    if dialog.edt_ipaddr.toPlainText().strip() and dialog.edt_puerto.toPlainText().strip():
        conf_routine.WriteCfg(dialog.checo_habil.isChecked(), 'http' if dialog.radio_http.isChecked() else 'socks',
                              dialog.edt_ipaddr.toPlainText().strip(), dialog.edt_puerto.toPlainText().strip())
    else:
        QMessageBox.warning(dialog.parentWidget(), 'Error', 'Please input necessary informations!', QMessageBox.Ok)
    dialog.close()


def ProbarConexion(dialog):
    urllib3.disable_warnings()
    try:
        requests.get('https://google.com/', verify=False)
        QMessageBox.information(dialog.parentWidget(), 'Tips', 'Test of connection is successful', QMessageBox.Ok)
    except (error.URLError, exceptions.ProxyError, exceptions.SSLError, exceptions.HTTPError,
            exceptions.ConnectionError) as e:
        QMessageBox.critical(dialog.parentWidget(), 'Error', 'Proxy does not work: ' + str(e), QMessageBox.Ok)


class ChildWin(QDialog, proxy_dlg.Ui_ProxDlg):
    def __init__(self):
        super(ChildWin, self).__init__()
        self.setupUi(self)


def goto_proxysets():
    dialog = ChildWin()

    dialog.btn_cancel.clicked.connect(dialog.close)
    dialog.btn_prueba.clicked.connect(lambda: ProbarConexion(dialog))

    enabled, proto, ipaddr, puerto = conf_routine.ReadCfg()
    dialog.checo_habil.setChecked(enabled)
    for control in [dialog.radio_http, dialog.radio_socks, dialog.edt_puerto, dialog.edt_ipaddr, dialog.btn_prueba]:
        control.setEnabled(enabled)

    dialog.radio_http.setChecked(proto == 'http')
    dialog.radio_socks.setChecked(proto == 'socks')
    if ipaddr and puerto:
        dialog.edt_ipaddr.setText(ipaddr)
        dialog.edt_puerto.setText(puerto)

    dialog.btn_ok.clicked.connect(lambda: guardar_conf(dialog))
    dialog.checo_habil.stateChanged.connect(lambda state: set_allEnable(dialog, dialog.checo_habil.isChecked()))
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