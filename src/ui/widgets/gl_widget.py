"""OpenGL widget for CNC machine visualization."""

from __future__ import annotations

from math import cos, radians, sin

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QOpenGLWidget

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LINES,
    GL_LIGHT0,
    GL_LIGHTING,
    GL_MODELVIEW,
    GL_POSITION,
    GL_PROJECTION,
    GL_QUADS,
    glBegin,
    glClear,
    glClearColor,
    glColor3f,
    glEnable,
    glEnd,
    glLightfv,
    glLoadIdentity,
    glMatrixMode,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glScalef,
    glTranslatef,
    glVertex3f,
)
from OpenGL.GLU import gluLookAt, gluPerspective


class GLWidget(QOpenGLWidget):
    """Basic OpenGL viewport with camera controls and axis motion."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._last_pos = QPoint()
        self._yaw = 35.0
        self._pitch = 25.0
        self._distance = 900.0
        self._pan_x = 0.0
        self._pan_y = -120.0
        self._axis_positions = {"X": 0.0, "Y": 0.0, "Z": 0.0}

    def initializeGL(self) -> None:
        glClearColor(0.08, 0.09, 0.12, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def resizeGL(self, width: int, height: int) -> None:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / max(height, 1)
        gluPerspective(45.0, aspect, 0.1, 5000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        eye_x, eye_y, eye_z = self._camera_position()
        gluLookAt(
            eye_x,
            eye_y,
            eye_z,
            self._pan_x,
            self._pan_y,
            0.0,
            0.0,
            1.0,
            0.0,
        )

        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 1000.0, 1.0))

        self._draw_grid()
        self._draw_machine()

    def set_axis_position(self, axis: str, value: float) -> None:
        if axis in self._axis_positions:
            self._axis_positions[axis] = value
            self.update()

    def _camera_position(self) -> tuple[float, float, float]:
        yaw_rad = radians(self._yaw)
        pitch_rad = radians(self._pitch)
        x = self._distance * cos(pitch_rad) * cos(yaw_rad) + self._pan_x
        y = self._distance * cos(pitch_rad) * sin(yaw_rad) + self._pan_y
        z = self._distance * sin(pitch_rad)
        return x, y, z

    def _draw_grid(self) -> None:
        glColor3f(0.2, 0.22, 0.26)
        glBegin(GL_LINES)
        for i in range(-500, 501, 50):
            glVertex3f(i, -500, 0)
            glVertex3f(i, 500, 0)
            glVertex3f(-500, i, 0)
            glVertex3f(500, i, 0)
        glEnd()

    def _draw_box(self, width: float, depth: float, height: float) -> None:
        w = width / 2
        d = depth / 2
        h = height
        glBegin(GL_QUADS)
        glVertex3f(-w, -d, 0)
        glVertex3f(w, -d, 0)
        glVertex3f(w, d, 0)
        glVertex3f(-w, d, 0)

        glVertex3f(-w, -d, h)
        glVertex3f(w, -d, h)
        glVertex3f(w, d, h)
        glVertex3f(-w, d, h)

        glVertex3f(-w, -d, 0)
        glVertex3f(w, -d, 0)
        glVertex3f(w, -d, h)
        glVertex3f(-w, -d, h)

        glVertex3f(-w, d, 0)
        glVertex3f(w, d, 0)
        glVertex3f(w, d, h)
        glVertex3f(-w, d, h)

        glVertex3f(-w, -d, 0)
        glVertex3f(-w, d, 0)
        glVertex3f(-w, d, h)
        glVertex3f(-w, -d, h)

        glVertex3f(w, -d, 0)
        glVertex3f(w, d, 0)
        glVertex3f(w, d, h)
        glVertex3f(w, -d, h)
        glEnd()

    def _draw_machine(self) -> None:
        x = self._axis_positions["X"]
        y = self._axis_positions["Y"]
        z = self._axis_positions["Z"]

        glColor3f(0.3, 0.32, 0.36)
        self._draw_box(800, 500, 60)

        glPushMatrix()
        glTranslatef(-300, 0, 60)
        glPushMatrix()
        glTranslatef(0, y, 0)

        glPushMatrix()
        glTranslatef(-300, 0, 60)
        glColor3f(0.35, 0.36, 0.4)
        self._draw_box(120, 120, 300)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(300, 0, 60)
        glColor3f(0.35, 0.36, 0.4)
        self._draw_box(120, 120, 300)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 340)
        glColor3f(0.4, 0.42, 0.46)
        self._draw_box(720, 140, 80)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(x, 0, 380)
        glColor3f(0.25, 0.5, 0.7)
        self._draw_box(200, 160, 80)

        glTranslatef(0, 0, 80)
        glColor3f(0.25, 0.6, 0.6)
        self._draw_box(180, 140, 60)

        glTranslatef(0, 0, -z)
        glColor3f(0.8, 0.4, 0.3)
        self._draw_box(60, 60, 180)
        glPopMatrix()
        glPopMatrix()

    def mousePressEvent(self, event) -> None:
        self._last_pos = event.pos()

    def mouseMoveEvent(self, event) -> None:
        delta = event.pos() - self._last_pos
        self._last_pos = event.pos()
        if event.buttons() & Qt.LeftButton:
            self._yaw += delta.x() * 0.5
            self._pitch += delta.y() * 0.5
            self._pitch = max(-89.0, min(89.0, self._pitch))
            self.update()
        elif event.buttons() & Qt.RightButton:
            self._pan_x += delta.x() * 2.0
            self._pan_y -= delta.y() * 2.0
            self.update()

    def wheelEvent(self, event) -> None:
        self._distance -= event.angleDelta().y() * 0.2
        self._distance = max(200.0, min(2000.0, self._distance))
        self.update()
