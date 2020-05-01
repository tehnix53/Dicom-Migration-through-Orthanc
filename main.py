import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
import os.path
import sys  # sys нужен для передачи argv в QApplication

import httplib2
import re
import requests
from PyQt5 import QtWidgets

import design  # Это наш конвертированный файл дизайна


def studies_count():
    url = 'http://localhost:8042/instances/'
    studies_list = requests.get(url).content
    studies_list = studies_list.decode('utf-8').rstrip()

    pattern = '\w+\-\w+\-\w+\-\w+\-\w+'
    re.findall(pattern, studies_list)
    studies_list = re.findall(pattern, studies_list)
    return (len(studies_list))



def show_hosts():
    url = 'http://localhost:8042/modalities/'
    images_list = requests.get(url).content
    images_list = images_list.decode('utf-8').rstrip()
    pattern = '\w+'
    re.findall(pattern, images_list)
    a = re.findall(pattern, images_list)
    return (a)


def UploadFile(path):
    global success_count
    global total_file_count
    f = open(path, "rb")
    content = f.read()
    f.close()

    try:
        sys.stdout.write("Importing %s" % path)
        h = httplib2.Http()
        headers = { 'content-type' : 'application/dicom' }
        resp, content = h.request('http://127.0.0.1:8042/instances','POST', body = content, headers = headers)

        if resp.status == 200:
            sys.stdout.write(" => success\n")

        else:
            sys.stdout.write(" => failure (Is it a DICOM file? Is there a password?)\n")
    except:
        type, value, traceback = sys.exc_info()
        sys.stderr.write(str(value))
        sys.stdout.write(" => unable to connect (Is Orthanc running? Is there a password?)\n")



class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.browse_folder)  # Выполнить функцию browse_folder
        self.pushButton_2.clicked.connect(self.start_upload)                                                            # при нажатии кнопки
        #self.listWidget.clicked.connect(self.test)
        self.pushButton_3.clicked.connect(self.clear_orthanc)
        self.pushButton_4.clicked.connect(self.show_me_hosts)
        self.pushButton_5.clicked.connect(self.push_dicom)


    def UploadDir(self, path):
        i = 0
        for root, dirs, files in os.walk(path):
             for f in files:
                 if f.endswith('.bin') or f.endswith('.dcm') or f.endswith('.dsr'):
                     i+=1

        self.completed = 0

        while self.completed < i:
            for root, dirs, files in os.walk(path):
                 for f in files:
                     if f.endswith('.bin') or f.endswith('.dcm') or f.endswith('.dsr'):
                        UploadFile(os.path.join(root, f))
                        self.completed += (1*100)/i
                        self.progressBar.setValue(self.completed)



    def send_all(self, hostname):
        url = 'http://localhost:8042/studies/'
        studies_list = requests.get(url).content
        studies_list = studies_list.decode('utf-8').rstrip()

        pattern = '\w+\-\w+\-\w+\-\w+\-\w+'
        re.findall(pattern, studies_list)
        studies_list = re.findall(pattern, studies_list)

        url = "http://localhost:8042/modalities/" + hostname + '/store'
        i = 0
        self.completed = 0
        while self.completed < len(studies_list):
            for element in (studies_list):
                requests.post(url,element)
                self.completed += (1*100)/len(studies_list)
                self.progressBar.setValue()
                i += 1
                sys.stdout.write(" => success\n"+str(i)+' images')


    def delete_all(self):

        url = 'http://localhost:8042/studies/'
        studies_list = requests.get(url).content
        studies_list = studies_list.decode('utf-8').rstrip()

        pattern = '\w+\-\w+\-\w+\-\w+\-\w+'
        re.findall(pattern, studies_list)
        studies_list = re.findall(pattern, studies_list)

        url = 'http://localhost:8042/'
        self.completed = 0
        while self.completed < len(studies_list):
            for element in (studies_list):
                requests.delete(url+'studies/'+element)
                self.completed += (1*100)/len(studies_list)
                self.progressBar.setValue(self.completed)



    def push_dicom(self):
        where = self.lineEdit_4.text()
        self.send_all(where)
        self.lineEdit_5.setText('Sent '+str(studies_count())+ ' images')

    def show_me_hosts(self):
        self.lineEdit_3.setText(str(show_hosts()))


    def start_upload(self):
        name_folder = self.lineEdit.text()
        self.UploadDir(str(name_folder).split(' ')[4])
        self.lineEdit_2.setText('Upload '+str(studies_count())+ ' files')


    def browse_folder(self):
        list_file = []
        #self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        count = 0
        name_file = []
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
           for current_dir, dirs, files in os.walk(directory):
               for i in files:
                   if i.endswith('.bin') or i.endswith('.dsr') or i.endswith('.dcm'):
                       name_file = (str(i))
                       count += 1
                       list_file += [name_file]
        #self.listWidget.addItem(str(list_file))

        self.lineEdit.clear()
        self.lineEdit.setText(str('found DICOM-files: ')+str(count)+', folder: '+directory)

    def clear_orthanc(self):
        self.delete_all()
        self.lineEdit_2.setText('Clear is finished!')



    def enter_text(self):
        ip = self.lineEdit_3.text()
        #self.lineEdit_4.clear()
        self.lineEdit_3.setText('selected: '+ip)

        title = self.lineEdit_4.text()
        #self.lineEdit_4.clear()
        self.lineEdit_4.setText('selected: '+title)

        port = self.lineEdit_5.text()
        #self.lineEdit_4.clear()
        self.lineEdit_5.setText('selected: '+port)



    def test(self):
        self.lineEdit.clear()
        self.lineEdit.setText('clicked item work')



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


