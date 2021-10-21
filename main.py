import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5 import QtCore
from design import Ui_Lab1_security
import os, stat, shutil


class Window(QMainWindow, Ui_Lab1_security):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        self.button_start.clicked.connect(self.start_function)
        self.button_end.clicked.connect(self.end_function)
        self.button_pwd.clicked.connect(self.pwd)
        self.button_cd.clicked.connect(self.cd)
        self.button_ls.clicked.connect(self.ls)
        self.button_mkdir.clicked.connect(self.mkdir)
        self.button_rmdir.clicked.connect(self.rmdir)
        self.button_vi.clicked.connect(self.vi)
        self.button_rmfile.clicked.connect(self.rmfile)




    def update_paths():
        global lst_paths, lst_directories, lst_files, index
        lst_paths = []
        lst_directories = []
        lst_files = []
        index = 0
        for path, directory, file in os.walk(top="/home/anton/lab1_security/Dir0"):
            lst_paths.append(path)
            lst_directories.append(directory)
            lst_files.append(file)


    def start_function(self):
        directories = r"Dir0/Dir1/Dir2/Dir3/Dir4"
        try:
            os.makedirs(directories)
        except FileExistsError:
            pass
        for i in range(5):
            file = open(f"Dir{i}/dir{i}.txt", "w+")
            os.chdir(f"Dir{i}")
            file.write(f"Directory{i}")
            file.close()
        os.chmod("/home/anton/lab1_security/Dir0" ,stat.S_IRWXU)
        Window.update_paths()



    def end_function(self):
        try:
            shutil.rmtree("/home/anton/lab1_security/Dir0")
        except FileNotFoundError:
            sys.exit()
        sys.exit()


    def clear_all(self):
        self.line_edit_pwd.clear()
        self.line_edit_ls.clear()
        self.line_edit_cd.clear()
        self.line_edit_mkdir.clear()
        self.line_edit_rmfile.clear()
        self.line_edit_rmdir.clear()
        self.line_edit_vi.clear()
        self.text_edit_vi.clear()


    def pwd(self):
        if self.radiobutton_blocked_user.isChecked():
            self.line_edit_pwd.clear()
            self.line_edit_pwd.setText("Permission denied!")
        else:
            self.line_edit_pwd.clear()
            self.line_edit_pwd.setText(lst_paths[index])


    def ls(self):
        if self.radiobutton_blocked_user.isChecked():
            self.line_edit_ls.clear()
            self.line_edit_ls.setText("Permission denied!")
        else:
            self.line_edit_ls.clear()
            self.line_edit_ls.setText(f"{lst_directories[index]} {lst_files[index]}")


    def cd(self):
        global index
        if self.radiobutton_blocked_user.isChecked():
            self.line_edit_cd.clear()
            self.line_edit_cd.setText("Permission denied!")
        else:
            text_cd = self.line_edit_cd.text()
            if text_cd in lst_paths:
                os.chdir(text_cd)
                self.line_edit_cd.setText("Ok!")
                index = lst_paths.index(text_cd)
            else:
                self.line_edit_cd.setText("Error in path!")


    def mkdir(self):
        text_mkdir = self.line_edit_mkdir.text()
        if self.radiobutton_root.isChecked():
            if text_mkdir not in lst_paths:
                os.mkdir(text_mkdir)
                self.line_edit_mkdir.clear()
                self.line_edit_mkdir.setText("Ok!")
                Window.update_paths()

            else:
                self.line_edit_mkdir.clear()
                self.line_edit_mkdir.setText("Error in path!")
        
        else:
            self.line_edit_mkdir.clear()
            self.line_edit_mkdir.setText("Permission denied!")


    def rmfile(self):
        text_rmfile = self.line_edit_rmfile.text()
        if self.radiobutton_root.isChecked():
            if text_rmfile.split("/")[-1] in lst_files[index]:
                os.remove(text_rmfile)
                self.line_edit_rmfile.clear()
                self.line_edit_rmfile.setText("Ok!")
                Window.update_paths()

            else:
                self.line_edit_rmfile.clear()
                self.line_edit_rmfile.setText("Error in path!")
                print(text_rmfile.split("/")[-1])
                print(lst_files)
        
        else:
            self.line_edit_rmfile.clear()
            self.line_edit_rmfile.setText("Permission denied!")



    def rmdir(self):
        text_rmdir = self.line_edit_rmdir.text()
        if self.radiobutton_root.isChecked():
            if text_rmdir in lst_paths:
                shutil.rmtree(text_rmdir)
                self.line_edit_rmdir.clear()
                self.line_edit_rmdir.setText("Ok!")
                Window.update_paths()

            else:
                self.line_edit_rmdir.clear()
                self.line_edit_rmdir.setText("Error in path!")
        
        else:
            self.line_edit_rmdir.clear()
            self.line_edit_rmdir.setText("Permission denied!")


    def vi(self):
        name_file = self.line_edit_vi.text()
        content_file = self.text_edit_vi.toPlainText()
        if self.radiobutton_root.isChecked():
            if name_file not in lst_files[index]:
                os.chdir(lst_paths[index])
                with open(name_file, 'x') as f:
                    f.write(content_file)
                self.line_edit_vi.clear()
                self.line_edit_vi.setText("Ok!")
                self.text_edit_vi.clear()
                self.text_edit_vi.insertPlainText("Ok!")
                Window.update_paths()
            else:
                self.line_edit_vi.clear()
                self.line_edit_vi.setText("Error in path!")
                self.text_edit_vi.clear()
                self.text_edit_vi.insertPlainText("Error in path!")
        
        else:
            self.line_edit_rmdir.clear()
            self.line_edit_rmdir.setText("Permission denied!")



if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
