"""
Thread for SQL statements
"""
import mysql.connector
from PyQt5.QtCore import QThread, pyqtSignal


class MyThread3(QThread):
    finished = pyqtSignal(object)

    def __init__(self, parent=None):
        """
        :param detected_object: the result of the detection of the ML Model; currently it is a list;
        :param parent:
        """
        super(MyThread3, self).__init__(parent)
        self.parent = parent
        self.detected_result = []  # It is assigned in the QMainWindow class;
        self.conn = mysql.connector.connect(user='root', password='qwerQWER', database='hobin')
        print('Connection to database is successful')


    def run(self):
        """
        Disadvantage: 5 queries (not 1 query)!
        If using 1 query, be carefule that customer may buy same products (query result will decrease at this situation).
        """
        print('SQL Thread get %s'% self.detected_result)
        results = []
        if len(self.detected_result)>0:
            cursor = self.conn.cursor()
            for i in self.detected_result:
                cursor.execute('select goods_name, goods_spec, sku_price from storegoods where cv_id = %s', (i,))
                results = results + cursor.fetchall()
            print(results)
            self.finished.emit(results)
            cursor.close()



if __name__ == '__main__':
    a = MyThread3()
    a.start()
    while a.isRunning():
        pass
    print('done')

