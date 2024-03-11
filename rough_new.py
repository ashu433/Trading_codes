import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import Qt

class LinePlotWidget(QGraphicsView):
    markers = []  # Define markers at the class level

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.plot_line()

    def plot_line(self):
        x = np.arange(0, 10, 0.1)
        y = np.sin(x)

        for i in range(len(x)):
            ellipse = QGraphicsEllipseItem(x[i] * 20, -y[i] * 50, 10, 10)
            ellipse.setBrush(Qt.blue)
            self.scene.addItem(ellipse)
            self.markers.append(ellipse)

    def mouseMoveEvent(self, event):
        for marker in self.markers:
            marker_center = marker.boundingRect().center()
            distance = marker_center - event.pos()
            if distance.manhattanLength() < 10:  # Adjust the attraction distance as needed
                marker.setPos(event.pos() - marker_center)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Interactive Line Plot")
        self.central_widget = LinePlotWidget()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
