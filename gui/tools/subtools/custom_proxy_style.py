from PySide6.QtWidgets import QProxyStyle, QStyle


class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 55
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)
