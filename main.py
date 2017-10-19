#author  = Natesh M Bhat
#python version = 3.5

import pymysql
from ui import Ui_MainWindow ;
from time import sleep
from threading import Thread;
import db_con

from PyQt5 import QtCore , QtGui , QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setMouseTracking(True) ;

    def closeEvent(self,event):
        try:
            con = pymysql.connect() ;
            cur = con.cursor() ;
            print("connection closed") ;
            # obj = datahandler() ;
            # obj.showtooltip( "Developed By Natesh M Bhat") ;
            app.processEvents() ;

            cur.close() ;
            con.close() ;

        except Exception as e:
            print(e) ;



class datahandler(object):
    def __init__(self):
        ui.submit_PushButton.mousePressEvent = self.connecttosql
        ui.submit_PushButton.keyPressEvent= self.connecttosql
        dbui.connect_pushbutton.mousePressEvent= self.initial_connect ;
        dbui.connect_pushbutton.keyPressEvent= self.initial_connect ;


    def initial_connect(self, event):
        self.url  = dbui.urlLineEdit.text() ;
        self.user = dbui.usernameLineEdit.text()
        self.password = dbui.passwordLineEdit.text()
        self.database = dbui.databaseNameLineEdit.text() ;

        try:
            if not self.database:
                raise Exception("Please Enter the database name :")

            self.con = pymysql.connect(host=self.url,
                                  user=self.user,
                                  password=self.password,
                                  db=self.database,
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor);

            # cur = con.cursor() ;
            self.showtooltip("Connection Sucessful ! ") ;
            self.con.autocommit(True) ;
            print("success") ;
            dbuidialog.close() ;
            Dialog.show()

        except Exception as e:
            QtWidgets.QMessageBox.critical(Dialog , "Failed to Connect" , """
Failed to Connect to Database : "{}" \nHost : "{}"
\n\nError Details :-\n\n{}""".format(self.database, self.url , e)) ;



    def replace(self , mystring ):
        mystring = mystring.replace("&" , "&amp;");
        mystring = mystring.replace("'" , "&apos;");
        mystring = mystring.replace('"' , "&quot;");
        mystring = mystring.replace("<" , "&lt;");
        mystring = mystring.replace(">" , "&gt;");
        return mystring ;


    def showtooltip(self, text):
        tt = QtWidgets.QToolTip ;
        myfont = QtGui.QFont() ;
        myfont.setFamily("caladea")
        myfont.setBold(True)
        myfont.setPointSize(20)
        tt.setFont(myfont)
        mywin = Dialog.frameGeometry() ;
        pos = mywin.center()
        pos.setX(pos.x() - 6.5 * len(text));
        pos.setY(mywin.y()-20)
        tt.showText(pos, text, Dialog ) ;



    def connecttosql(self , event):
        question = self.replace(ui.question_textedit.toPlainText()) ;

        if not question:
            QtWidgets.QMessageBox.warning(Dialog , "Empty Question field" , "Make sure that the question field is not Empty ! " , QtWidgets.QMessageBox.Ok) ;
            return ;

        if not ui.tablename_LineEdit.text():
            QtWidgets.QMessageBox.warning(Dialog, "Empty Table Name",
                                          "Table name should not be empty ! Make sure that the right table name is specified ! ",
                                          QtWidgets.QMessageBox.Ok);
            return;

        opa = self.replace(ui.alineEdit.text()) ;
        opb = self.replace(ui.bLineEdit.text() ) ;
        opc = self.replace(ui.cLineEdit.text()  ) ;
        opd = self.replace(ui.cLineEdit.text() )  ;
        rightop = 'A' if ui.aradioButton.isChecked() else 'B' if ui.bradioButton.isChecked() else 'C' if ui.cradioButton.isChecked() else 'D' ;
        codesnippet = self.replace(ui.codesnippet_textedit.toPlainText()) ;
        tablename = ui.tablename_LineEdit.text() ;

        try:
            self.con = pymysql.connect(host=self.url,
                                  user=self.user,
                                  password=self.password,
                                  db=self.database,
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor);

            with self.con.cursor() as cur:

                command = """insert into {} (Question , optiona , optionb , optionc , optiond , correct , codesnippet) values (%s, %s , %s, %s , %s , %s , %s ) """.format(tablename) ;
                strings = (
                    question ,
                    opa ,
                    opb ,
                    opc ,
                    opd,
                    rightop,
                    codesnippet
                );

                cur.execute(command , strings);
                self.con.commit();
                for i in ui.frame.findChildren((QtWidgets.QTextEdit , QtWidgets.QLineEdit)):
                    i.clear() ;

                self.showtooltip("Added to Database");
                self.con.close() ;

        except Exception as e:
            print("Failed") ;
            self.showtooltip("Failed Adding to Database") ;
            msgbox = QtWidgets.QMessageBox() ;
            msgbox.setText("Error Adding Entry to Database") ;
            msgbox.setWindowTitle("Error !") ;
            msgbox.setIcon(QtWidgets.QMessageBox.Critical) ;
            msgbox.setDetailedText(str(e)) ;
            msgbox.exec_();
            self.con.close() ;



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = mywindow()
    # Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint) ;
    ui = Ui_MainWindow()
    ui.setupUi(Dialog)


    dbuidialog = QtWidgets.QDialog();
    dbui = db_con.Ui_Dialog() ;
    dbui.setupUi(dbuidialog) ;
    datahandler() ;
    dbuidialog.exec_() ;

    sys.exit(app.exec_())

