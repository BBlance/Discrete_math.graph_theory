from PySide2.QtCore import QPointF

import math

center = QPointF(0, 0)
edge = QPointF(20, 20)
print(math.atan((edge.y() - center.y()) / (edge.x() - center.x()))*(180/math.pi))
