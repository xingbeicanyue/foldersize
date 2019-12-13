try:
    import PySide2
    from PySide2.QtCore import QPoint, QPointF, QRectF, QLineF
    from PySide2.QtGui import QPainterPath, QPolygonF
    from utils.geometryUtils.geometry import SegPathType, createPath


# region QPoint、QPointF

    def ptToQPt(pt: tuple) -> QPoint:
        """ point -> QPoint """
        return QPoint(pt[0], pt[1])


    def qPtToPt(pt: QPoint) -> tuple:
        """ QPoint -> point """
        return pt.x(), pt.y()


    def ptToQPtF(pt: tuple) -> QPointF:
        """ point -> QPointF """
        return QPointF(pt[0], pt[1])


    def qPtFToPt(pt: QPointF) -> tuple:
        """ QPointF -> point """
        return pt.x(), pt.y()

# endregion


# region QRectF

    def aabbToQRectF(aabb: tuple) -> QRectF:
        """ aabb -> QRectF """
        return QRectF(aabb[0], aabb[2], aabb[1] - aabb[0], aabb[3] - aabb[2])


    def qRectFToAabb(rect: QRectF) -> tuple:
        """ QRectF -> aabb """
        return rect.left, rect.right, rect.top, rect.bottom

# endregion


# region QLineF

    def toQLineF(segline: tuple) -> QLineF:
        """ segline -> QRectF """
        return QLineF(QPointF(segline[0][0], segline[0][1]), QPointF(segline[1][0], segline[1][1]))

# endregion


# region QPolygonF

    def polylineToQPolygonF(polyline: list) -> QPolygonF:
        """ polyline -> QPolygonF """
        return QPolygonF([ptToQPtF(pt) for pt in polyline])

# endregion


# region QPainterPath

    def seglineToQPainterPath(segline: tuple) -> QPainterPath:
        """ segline -> QPainterPath """
        result = QPainterPath()
        result.moveTo(ptToQPtF(segline[0]))
        result.lineTo(ptToQPtF(segline[1]))
        return result


    def ellipseToQPainterPath(ellipse: tuple) -> QPainterPath:
        """ ellipse -> QPainterPath """
        return pathToQPainterPath(createPath(ellipse=ellipse, toBezier=True))


    def polylineToQPainterPath(polyline: list) -> QPainterPath:
        """ polyline -> QPainterPath """
        result = QPainterPath()
        if len(polyline) == 0:
            return result
        result.moveTo(ptToQPtF(polyline[0]))
        for i in range(1, len(polyline)):
            result.lineTo(ptToQPtF(polyline[i]))
        return result


    def pathToQPainterPath(path: list) -> QPainterPath:
        """ path -> QPainterPath """
        result = QPainterPath()
        if len(path) == 0:
            return result
        result.moveTo(ptToQPtF(path[0][1][0]))
        for i in range(len(path)):
            if path[i][0] == SegPathType.Segline:
                result.lineTo(ptToQPtF(path[i][1][1]))
            elif path[i][0] == SegPathType.Arc:
                raise Exception('[Error] pathToQPainterPath: 未完成')
            elif path[i][0] == SegPathType.Bezier:
                result.cubicTo(ptToQPtF(path[i][1][1]), ptToQPtF(path[i][1][2]), ptToQPtF(path[i][1][3]))
        return result
        
# endregion

except:
    pass