from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter
from PySide6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
import requests

class OrderItem:
    def __init__(self, image_url, name, price, quantity):
        self.image_url = image_url
        self.name = name
        self.price = price
        self.quantity = quantity

class OrderItemModel(QStandardItemModel):
    def __init__(self, order_items):
        super().__init__()
        for item in order_items:
            self.add_item(item)
    
    def add_item(self, order_item):
        item = QStandardItem()
        item.setData(order_item, Qt.UserRole)
        item.setEditable(False)
        self.appendRow(item)

class ItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option: QStyleOptionViewItem, index):
        order_item = index.data(Qt.UserRole)
        if not order_item:
            return

        painter.save()

        # Highlight background if selected
        # if option.state & QStyleOptionViewItem.State_Selected:
        #     painter.fillRect(option.rect, option.palette.highlight())

        # Load and draw image
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(order_item.image_url).content)
        image_size = QSize(50, 50)
        image_rect = QRect(option.rect.left() + 10, option.rect.top() + 5, image_size.width(), image_size.height())
        painter.drawPixmap(image_rect, pixmap)

        # Draw text next to the image
        text_rect = QRect(image_rect.right() + 10, option.rect.top(), option.rect.width() - image_rect.width() - 20, option.rect.height())
        text = f"{order_item.name} - ${order_item.price} x {order_item.quantity}"
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(300, 60)

def setup_order_list(order_items, list_view):
    """Attach the OrderList model and delegate to an existing QListView."""
    model = OrderItemModel(order_items)
    list_view.setModel(model)
    list_view.setItemDelegate(ItemDelegate())