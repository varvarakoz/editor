from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, \
    QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

app = QApplication([])

"""Создание интерфейса"""
window = QWidget()
window.setWindowTitle('Редактор изображений')
window.resize(700, 500)

"""Виджеты окна приложения"""
btn_folder = QPushButton('Папка')
lw_files = QListWidget()
left_btn = QPushButton('Лево')
right_btn = QPushButton('Право')
mirror_btn = QPushButton('Зеркало')
sharpness_btn = QPushButton('Резкость')
black_white_btn = QPushButton('Ч/Б')
save_btn = QPushButton('Сохранить')
reset_filter_btn = QPushButton('Сбросить фильтры')
lb_image = QLabel('картинка')

"""Расположение по лэйаутам"""
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(lw_files, 95)

col2.addWidget(lb_image)

row_tools = QHBoxLayout()
row_tools.addWidget(left_btn)
row_tools.addWidget(right_btn)
row_tools.addWidget(mirror_btn)
row_tools.addWidget(sharpness_btn)
row_tools.addWidget(black_white_btn)
row_tools.addWidget(save_btn)
row_tools.addWidget(reset_filter_btn)

col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 100)

window.setLayout(row)
window.show()

work_dir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def choseWorkdir():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()

# добавить сюда проверку
def show_filename_list():
    choseWorkdir()
    if not work_dir:
        return
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    filenames = filter(os.listdir(work_dir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


btn_folder.clicked.connect(show_filename_list)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
        self.original_image = None

    def load_image(self, filename):
        """При загрузке запоминает путь и имя файла"""
        self.filename = filename
        self.dir = work_dir
        fullname = os.path.join(work_dir, filename)
        self.image = Image.open(fullname)
        self.original_image = self.image.copy()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        ''' сохраняет копию файла в подпапке '''
        path = os.path.join(work_dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def turn_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def turn_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)


    def resetImage(self):
        """сбрасывает изменения и возвращает оригинальное изображение"""
        if self.original_image is None:
            return
        self.image = self.original_image.copy()
        self.showImage(os.path.join(work_dir, self.filename))




def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        work_image.load_image(filename)
        work_image.showImage(os.path.join(work_dir, work_image.filename))

work_image = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)

mirror_btn.clicked.connect(work_image.do_flip)
black_white_btn.clicked.connect(work_image.do_bw)
sharpness_btn.clicked.connect(work_image.do_sharpen)
left_btn.clicked.connect(work_image.turn_left)
right_btn.clicked.connect(work_image.turn_right)
reset_filter_btn.clicked.connect(work_image.resetImage)


app.exec()
