import smtplib
from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QPushButton, QTextEdit, QFileDialog, QLabel
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SpamMail kliens (hungarian)")

        button_1 = QPushButton("INDULJON A \nSPAMELÉS!")
        global TextEdit
        TextEdit = QTextEdit("Az e-mail szövege!")
        button_3 = QPushButton("Válassz ki egy \ncsatolandó fájlt!")
        button_3.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        global label
        label = QLabel("--- VIGYÁZZ! Még nem csatoltál fájlt! ---")
        label_ = QLabel("by ProgrammerGnome")
        global textEdit_5
        textEdit_5 = QTextEdit("Az e-mail cím, amire küldeni szeretnéd!")
        label_6 = QLabel("Ez egy gmail spam alkalmazás. \n\nAz SMTP felhasználónév és\nalkalmazásjelszó az SMTP_datas.txt \n"+
        "fájl első két sorában található meg.")
        label_6_1 = QLabel("A levél tárgyát az \nelküldött aktuális \ndarabszám képzi.")
        global textEdit_7
        textEdit_7 = QTextEdit("Hányszor szeretnéd elküldeni a levelet?")

        button_1.setCheckable(True)
        button_1.clicked.connect(self.copyText)
        button_3.clicked.connect(self.open_file_dialog)

        grid_layout = QGridLayout()
        grid_layout.addWidget(button_1,0,0)
        grid_layout.addWidget(TextEdit,0,1,1,2) #Take up 1 row and 2 columns
        grid_layout.addWidget(button_3,1,0,2,1) #Take up 2 rows and 1 column
        grid_layout.addWidget(label,3,1)
        grid_layout.addWidget(label_,4,0)
        grid_layout.addWidget(textEdit_5,1,1)
        grid_layout.addWidget(label_6,1,2)
        grid_layout.addWidget(label_6_1,2,2)
        grid_layout.addWidget(textEdit_7,2,1)

        self.setLayout(grid_layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global file_name
        file_name, _ = QFileDialog.getOpenFileName(self, "Fájl kiválasztása", "",
                                                          "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f'Kiválasztott fájl: {file_name}')
            label.setText(f'Kiválasztott fájl: {file_name}')

    def copyText(self):
        global body, ranger, to_addr
        body = TextEdit.toPlainText()
        to_addr = textEdit_5.toPlainText()
        ranger = int(textEdit_7.toPlainText())

        self.the_button_was_clicked()

    def the_button_was_clicked(self):
        print("A spamelés elindult!")

        # Csatlakozás az SMTP szerverhez
        f = open("SMTP_datas.txt", "r")
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = f.readline()
        smtp_password = f.readline()

        # E-mail beállítások
        from_addr = smtp_username

        counter = 0
        for i in range(ranger):
            counter = counter+1

            # E-mail elkészítése
            msg = MIMEMultipart()
            msg.attach(MIMEText(body))
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = str(counter)
            try:
                file = file_name
                attachment = open(file,'rb')
                obj = MIMEBase('application','octet-stream')
                obj.set_payload((attachment).read())
                encoders.encode_base64(obj)
                obj.add_header('Content-Disposition',"attachment; filename= "+"Fatel")  #Tetszés szerint módosítható.
                msg.attach(obj)
            except:
                print("De csatolt fájl nélkül...")

            # E-mail küldése
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
