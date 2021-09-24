from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtMultimedia
import sys, os

'''
Writer: kprxn
Github: https://github.com/kprxn
'''

class Window(QWidget):
    def __init__(self, title, shape, icon):
        super().__init__()
        self.title = title
        self.x, self.y, self.w, self.h = shape
        self.icon = QIcon(icon)
        self.path = os.path.join("C:\\", "Users", os.getlogin(), "Music")
        self.music_files = {}
        self.vbox = QVBoxLayout()
        self.initUI()
        self.setLayout(self.vbox)
        self.show()

    def GetMusics(self):
        for file in os.listdir(self.path):
            if file.endswith(".mp3"):
                self.music_files[file] = os.path.join(self.path, file)
                self.music_files_list.addItem(QListWidgetItem(file))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.x, self.y, self.w, self.h)

        self.vbox.addWidget(QLabel(text="Select Music: "))
        self.music_files_list = QListWidget()
        self.music_files_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.music_files_list.itemSelectionChanged.connect(self.GetPlayer)
        self.vbox.addWidget(self.music_files_list)

        self.GetMusics()
        self.music_files_list.setCurrentRow(0)

        hbox = QHBoxLayout()
        self.before_btn = QPushButton(text="Before", clicked=self.BeforeMusic)
        hbox.addWidget(self.before_btn)

        self.play_btn = QPushButton(text="Play", clicked=self.PlayMusic)
        hbox.addWidget(self.play_btn)

        self.pause_btn = QPushButton(text="Pause", clicked=self.PauseMusic)
        hbox.addWidget(self.pause_btn)

        self.next_btn = QPushButton(text="Next", clicked=self.NextMusic)
        hbox.addWidget(self.next_btn)
        self.vbox.addLayout(hbox)

        self.volume_slider = QSlider(Qt.Horizontal, valueChanged=self.SetVolume)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.vbox.addWidget(self.volume_slider)

    def GetPlayer(self):
        music = self.music_files_list.currentItem().text()
        music_loc = self.music_files[music]
        music_url = QUrl.fromLocalFile(music_loc)
        self.content = QtMultimedia.QMediaContent(music_url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(self.content)
        self.PlayMusic()

    def PlayMusic(self):
        self.player.play()

    def PauseMusic(self):
        self.player.pause()

    def BeforeMusic(self):
        music = self.music_files_list.currentIndex()
        before_music = music.row() - 1
        if before_music < 0:
            self.music_files_list.setCurrentRow(self.music_files_list.count() - 1)
            self.PlayMusic()
        else:
            self.music_files_list.setCurrentRow(before_music)
            self.PlayMusic()

    def NextMusic(self):
        music = self.music_files_list.currentIndex()
        next_music = music.row() + 1
        if next_music == self.music_files_list.count():
            self.music_files_list.setCurrentRow(0)
            self.PlayMusic()
        else:
            self.music_files_list.setCurrentRow(next_music)
            self.PlayMusic()

    def SetVolume(self):
        self.player.setVolume(self.volume_slider.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window("MP3 Player", (100, 100, 500, 500), "../img/icon.png")
    app.setStyle("Windows")
    app.exec_()