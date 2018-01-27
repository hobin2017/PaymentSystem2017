"""
QR code: Quick response code
the QR code is shown in QLabel;
"""
from PIL import Image
from PIL.ImageQt import ImageQt
import collections
import hashlib
import json
from datetime import datetime
import qrcode
import requests
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow


class Mythread5(QThread):
    """

    """
    finished = pyqtSignal(object)
    def __init__(self, parent=None):
        super(Mythread5, self).__init__(parent)
        self.parent = parent
        self.url = 'http://api.commaai.cn/order/order/create_sku_order'
        self.sign_key = '4b111cc14a33b88e37e2e2934f493458'
        self.dict01 = {"api_sign": None,
                       'utm_medium': 'app',
                       'utm_source': 'box',
                       'store_id': '2',
                       'screen_id':'1',
                       'client_time': None,
                       'buy_skuids':None,}
        self.dict02 = {}  # the dictionary object of the first HTTP result


    def api_sign_hexdigest(self, dict):
        """
        It is used to produce the digest of the information;
        The rule is specified in 'check_str';
        :param dict: the dictionary data which will be passed to the server;
        :return:
        """
        ordered_dict = collections.OrderedDict(sorted(dict.items()))
        # print('ordered_dict', ordered_dict)

        input = '&'.join([key + '=' + str(value) for (key, value) in ordered_dict.items() if key != 'api_sign'])
        # print('input', input)

        check_str = input + '&' + self.sign_key
        # print('check_str', check_str)

        hexdigest = hashlib.sha256(check_str.encode()).hexdigest()
        # print('hexdigest', hexdigest)

        return hexdigest


    def run(self):
        print('QRcode thread begins')
        self.dict01['buy_skuids'] = '567'
        self.dict01['client_time'] = str(int(datetime.now().timestamp()))
        self.dict01['api_sign'] = self.api_sign_hexdigest(self.dict01)
        resp01 = requests.post(self.url, data=self.dict01, timeout=1)
        self.dict02 = json.loads(resp01.text)
        # print(self.dict02['data']['order_link'])

        # the QR code without extra image inside it
        # img1 = qrcode.make(self.dict02['data']['order_link'])  # it is the qrcode.image.pil.PilImage class
        # self.finished.emit(img1)

        # the QR code with extra image inside it
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
        qr.add_data(self.dict02['data']['order_link'])
        qr.make(fit=True)  # to avoid data overflow errors
        img2 = qr.make_image()
        img2 = img2.convert("RGBA")
        # adding the image to the QR code
        icon = Image.open("./images/payment.png")
        img2_w, img2_h = img2.size
        factor = 4
        size_w = int(img2_w / factor)
        size_h = int(img2_h / factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        w = int((img2_w - icon_w) / 2)
        h = int((img2_h - icon_h) / 2)
        # icon = icon.convert("RGBA")
        img2.paste(icon, (w, h), icon)
        self.finished.emit(img2)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.label1 = QLabel()
        self.thread = Mythread5(self)
        self.thread.finished.connect(self.work1)
        self.pixmap01 = QPixmap()
        self.setCentralWidget(self.label1)
        self.thread.start()

    def work1(self, img_qrcode):
        imageq = ImageQt(img_qrcode)
        qimage = QImage(imageq)
        self.pixmap01.convertFromImage(qimage)
        self.label1.setPixmap(self.pixmap01)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    sys.exit(app.exec_())


