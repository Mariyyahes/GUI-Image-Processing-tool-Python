import datetime
import os
import sys
import cv2
import imutils
from PyQt5.QtWidgets import QMainWindow, QAction ,QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,QFileDialog, QGridLayout,QMessageBox
from PyQt5.QtGui import QImage, QIcon,QPixmap,QCursor
from PyQt5.uic.properties import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui, QtCore



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Tool")
        self.setWindowIcon(QIcon(r"C:\Users\marey\OneDrive\سطح المكتب\logo .w.png"))
        self.resize(1400, 700)
        self.move(100, 100)
        self.setStyleSheet("background: #F9F4ED;")
        self.fram()

    def fram(self):
        # Function to upload an image
        self.loadImage()

        # Create a QWidget for the main window
        widget = QWidget()

        # Create a QVBoxLayout to hold the buttons
        buttonLayout = QVBoxLayout()

        # Set the main widget of the QMainWindow to be the QWidget
        self.setCentralWidget(widget)

        # Create a QLabel to show the "Choose Effect" text
        label0 = QLabel()
        label1 = QLabel('Welcome to our Image Processing App ! ')
        label2 = QLabel('1- Upload an Image       2- Choose an Effect')
        label1.setStyleSheet('color: black;font-family: Century Gothic; font-size: 23px; font-weight: bold;')
        label2.setStyleSheet('color: black;font-family: Century Gothic; font-size: 18px; font-weight: Regular;')

        ''' create identical buttons with custom left & right margins
        This code will display logo 
        # Create a QLabel to display the photo
        self.photo_label = QLabel(self)
        # Set the size of the QLabel
        self.photo_label.setFixedSize(200, 40)
        # Load the photo from a file using QPixmap
        photo_pixmap = QPixmap(r" ")
        # Scale the photo to fit within the QLabel while maintaining aspect ratio
        scaled_pixmap = photo_pixmap.scaled(self.photo_label.size(), Qt.KeepAspectRatio)
        # Set the scaled photo as the pixmap of the QLabel
        self.photo_label.setPixmap(scaled_pixmap) '''

        # Create the buttons
        button1 = self.create_buttons("Grayscale image", 5, 5)
        button2 = self.create_buttons("HSL image", 5, 5)
        button3 = self.create_buttons("Rotate image", 5, 5)
        button4 = self.create_buttons("Blur Image", 5, 5)
        button5 = self.create_buttons("Edge Detection", 5, 5)
        download_b = self.create_download_button(5, 5)

        # Connect the buttons to their corresponding actions
        button1.clicked.connect(self.button1_Action)
        button2.clicked.connect(self.button2_Action)
        button3.clicked.connect(self.button3_Action)
        button4.clicked.connect(self.button4_Action)
        button5.clicked.connect(self.button5_Action)
        download_b.clicked.connect(self.download_bAction)

        # Add the labels to the QVBoxLayout
        buttonLayout.addWidget(label0)
        buttonLayout.addWidget(label1)
        buttonLayout.addWidget(label2)

        # Add the buttons to the QVBoxLayout
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        buttonLayout.addWidget(button4)
        buttonLayout.addWidget(button5)
        buttonLayout.addWidget(download_b)
        buttonLayout.setSpacing(20)
        buttonLayout.addStretch(3)

        # Create a QVBoxLayout for the image label
        imageLayout = QVBoxLayout()

        # Add the label to the QVBoxLayout
        imageLayout.addWidget(self.image_label)

        # Create a QGridLayout to hold the buttons and image sections
        grid = QGridLayout()
        grid.addLayout(buttonLayout, 0, 0)
        grid.addLayout(imageLayout, 0, 1)

        # Set the layout of the main widget to be the QGridLayout
        widget.setLayout(grid)

    def button1_Action(self):
        # Check if an image has been loaded
        try:
            # Convert the image to grayscale
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # Update the stored image to the grayscale image
            self.setPhoto(self.image)
        except Exception:
            self.error_msg("No image loaded !")

    def button2_Action(self):
        # Check if an image has been loaded
        try:
            # Convert the image to grayscale
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
            # Update the stored image to the grayscale image
            self.setPhoto(self.image)
        except Exception:
            self.error_msg("No image loaded ! \nnote: this function require BGR image")

    def button3_Action(self):
        try:
            rows, cols = self.image.shape[:2]
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            self.image = cv2.warpAffine(self.image, M, (cols, rows))
            self.setPhoto(self.image)
        except Exception:
            self.error_msg("No image loaded !")

    def button4_Action(self):
        try:
            # apply gaussian blur on src image
            self.image = cv2.blur(self.image,(40,40))
            self.setPhoto(self.image)
        except Exception :
            self.error_msg("No image loaded !")

    def button5_Action(self):
        try:
            # Canny edge detection.
            self.image = cv2.Canny(self.image, 100, 200)
            # Write image back to disk.
            self.setPhoto(self.image)
        except Exception :
            self.error_msg("No image loaded !")

    def error_msg(self,e):
        # Show error message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText("An error occurred !")
        msg_box.setInformativeText(f"{str(e)}")
        msg_box.exec_()

    def download_bAction(self):
        """ This function will download the image."""
        directory = r"C:\Users\marey\OneDrive\سطح المكتب\EVA"  # Change the file path
        # Change the current directory to specified directory
        os.chdir(directory)
        # Filename with current date and time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"savedImage_{current_time}.jpg"
        # Save the edited image to the specified file
        cv2.imwrite(filename, self.image)

    def create_buttons(self, name ,l_margin, r_margin):
        '''create identical buttons with custom left & right margins'''
        button = QPushButton(name,self)
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setFixedWidth(270)
        button.setStyleSheet(
            # setting variable margins
            "*{margin-left: " + str(l_margin) + "px;" +
            "margin-right: " + str(r_margin) + "px;" +
            '''
            border: 4px solid '#B4D1D0';
            color: black;
            font-family: 'Century Gothic';
            font-weight: bold;
            font-size: 20px;
            border-radius: 8px;
            padding: 8px 0;
            margin-top: 20px}
            *:hover{
                background: '#B4D1D0'
            }
            '''

        )
        return button

    def create_download_button(self, l_margin, r_margin):
        '''create a circular download button with custom left & right margins'''
        button = QPushButton("   Download")
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setFixedWidth(270)
        button.setStyleSheet(
            # setting variable margins
            "*{margin-left: " + str(l_margin) + "px;" +
            "margin-right: " + str(r_margin) + "px;" +
            '''
            border: 4px solid '#B4D1D0';
            color: white;
            font-family: 'Century Gothic';
            font-weight: bold;
            font-size: 20px;
            border-radius: 8px;
            padding: 0px 0;
             background-color: '#B4D1D0';
            margin-top: 20px}
            *:hover{
                background: '#B4D1D0'
            }
            '''
        )

        # create the button icon
        icon = QIcon()
        icon.addPixmap(QPixmap("C:/Users/marey/Downloads/icons8-download-24.png"), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QSize(40, 40))

        return button

    def loadImage(self):
        """ This function will load the user selected image
            and set it to label using the setPhoto function
        """
        menubar = self.menuBar()
        menubar.setStyleSheet(
            "QMenuBar { background-color:#B4D1D0; color:black; font-family: Century Gothic; font-size: 18px; font-weight: bold; higt:50px;}")
        file_menu = menubar.addMenu('File')
        open_image_action = QAction('Open Image', self)
        open_image_action.triggered.connect(self.browse_image)
        file_menu.addAction(open_image_action)

        # Create a QLabel to display the loaded image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(740, 700)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

    def browse_image(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image files (*.*)')
        self.image = cv2.imread(self.filename)
        self.setPhoto(self.image)

    def setPhoto(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        # Resize the image to a width of 640 pixels
        resized_image = cv2.resize(image, (640, int(image.shape[0] * (640 / image.shape[1]))))

        # Convert the image to RGB format
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Create a QImage from the RGB image data
        qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)

        # Create a QPixmap from the QImage and set it as the pixmap of self.image_label
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(qimage))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # terminate the app

