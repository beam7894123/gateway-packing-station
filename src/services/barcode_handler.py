import asyncio
from services.api_service import APIService
from components.order_list import OrderItem, setup_order_list
from services.config_manager import ConfigManager
from PySide6.QtCore import Signal, QObject, QTimer
from PySide6.QtWidgets import QMessageBox

class BarcodeHandler(QObject):
    
    log_signal = Signal(str, str)  # Signal(message, message_type)
    barcode_scanned = Signal(str)  # Signal(barcode)
    
    def __init__(self):
        super().__init__()
        self.api_service = APIService()
        self.config_manager = ConfigManager()
    
    # if else is love if else is life XD
    async def handle_barcode(self,
                       barcode_text,
                       config_manager,
                       video_service,
                       listItemScaned,
                       listItemNotScaned,
                       statusBar,
                       set_status_label,):
        # It only starts recording when the barcode starts with "start|[NUMBER]" if in the future we change the barcode format we need to change this =w=
        if barcode_text.startswith("start|"):
            _, order_id = barcode_text.split('|', 1)
            if order_id.isdigit():
                if config_manager.get_order_id():
                    self.log_signal.emit(f"Error: Order ID {config_manager.get_order_id()} already loaded!", "error")
                    return
                try:
                    self.log_signal.emit(f"Loading Order ID: {order_id}", "info")
                    order_data = await self.api_service.post_data('/packing-station/start',
                                                    {
                                                        'orderId': order_id,
                                                        'station': config_manager.get_station_id(),
                                                        'status': '1'
                                                    })
                    if order_data:
                        scanned_items = [
                            OrderItem(item['image'],
                                    item['name'],
                                    item['price'],
                                    item['scannedQuantity'])  
                            for item in order_data['scanned']
                        ]
                        unscanned_items = [
                            OrderItem(item['image'],
                                    item['name'],
                                    item['price'],
                                    item['unscannedQuantity'])  
                            for item in order_data['unscanned']
                        ]
                        setup_order_list(scanned_items, listItemScaned)
                        setup_order_list(unscanned_items, listItemNotScaned)
                        self.log_signal.emit(f"Order ID: {order_id} loaded!", "success")
                        config_manager.set_order_id(order_id)
                        
                        video_service.start_recording()
                        set_status_label(1)
                        self.log_signal.emit(f"Start Recording (Order ID: {order_id})", "info")
                    else:
                        print("No data found for this order ID")
                        statusBar.showMessage("No data found for this order ID")
                        self.log_signal.emit(f"Order ID: {order_id} not found!", "error")
                except Exception as e:
                    print(f"Error fetching order data: {e}")
                    self.log_signal.emit(f"Order ID: {order_id} | {order_data.get('message', 'Unknown error')}", "error")
                    statusBar.showMessage("Error fetching order data")
            else:
                print("Invalid order ID xwx")
                statusBar.showMessage("Invalid order ID!")
                self.log_signal.emit(f"Invalid order ID: {order_id}", "error")
        
        # End Record and Send Order Data
        elif barcode_text.startswith("end|"):
            _, order_id = barcode_text.split('|', 1)
            if order_id.isdigit():
                if not config_manager.get_order_id():
                    self.log_signal.emit(f"Error no OrderID load yet!", "error")
                    return
                try:
                    if listItemNotScaned.model().rowCount() > 0:
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setWindowTitle('Warning Unscanned Items Detected!')
                        msg_box.setText('There are still items in the unscanned list. \nAre you sure you want to finish this order now?')
                        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        msg_box.setDefaultButton(QMessageBox.No)

                        # Create a QTimer to close the dialog after 10 seconds
                        timer = QTimer(msg_box)
                        timer.setInterval(5000)  # 10 seconds
                        timer.setSingleShot(True)
                        timer.timeout.connect(msg_box.defaultButton().animateClick)
                        timer.start()
                        timer.timeout.connect(lambda: msg_box.done(QMessageBox.No))
                        reply = msg_box.exec()

                        if reply == QMessageBox.No:
                            return
                except Exception as e:
                    self.log_signal.emit(f"Error: {order_id} | {e('message', 'Unknown error')}", "error")
                    set_status_label(3)
                    return
                    
                try:
                    video_service.stop_recording()
                    self.log_signal.emit(f"Stopped recording (Order ID: {order_id})", "info")
                    video_file = video_service.get_last_recorded_video()  # Implement this method in VideoCaptureService
                    set_status_label(2)
                    
                    await asyncio.sleep(1)
                    self.log_signal.emit(f"Sending Order ID: {order_id} data...", "info")
                    order_data = await self.api_service.post_data(
                        '/packing-station/finish',
                        {
                            'orderId': order_id,
                            'station': self.config_manager.get_station_id(),
                            'status': '2'
                        },
                        file_path=video_file
                    )
                    
                    if order_data:
                        if order_data['statusCode'] == '0' or order_data['statusCode'] == 404:
                            print("Error sending order data")
                            statusBar.showMessage("Error sending order data")
                            set_status_label(3)
                            setup_order_list([], listItemScaned)
                            setup_order_list([], listItemNotScaned)
                            self.log_signal.emit(f"Error sending Order ID: {order_id} | {order_data.get('message', 'Unknown error')}", "error")
                        else:
                            print("Order data sent successfully")
                            statusBar.showMessage("Order data sent successfully")
                            setup_order_list([], listItemScaned)
                            setup_order_list([], listItemNotScaned)
                            self.config_manager.clear_order_id() # why???
                            set_status_label(0)
                            self.log_signal.emit(f"Order ID: {order_id} data sent!", "success")
                except Exception as e:
                    print(f"Error sending order data: {e}")
                    statusBar.showMessage("Error sending order data")
                    set_status_label(3)
                    self.log_signal.emit(f"Error sending Order ID: {order_id}| {order_data.get('message', 'Unknown error')}", "error")     
        # Item Scan
        else:
            try:
                barcode_data = await self.api_service.post_data('/packing-station/item/', {
                    'orderId': config_manager.get_order_id(),
                    'station': config_manager.get_station_id(),
                    'itemCode': barcode_text
                })
                
                if barcode_data:
                    scanned_items = [
                        OrderItem(item['image'],
                                item['name'],
                                item['price'],
                                item['scannedQuantity'])  
                        for item in barcode_data['scanned']
                    ]
                    unscanned_items = [
                        OrderItem(item['image'],
                                item['name'],
                                item['price'],
                                item['unscannedQuantity'])  
                        for item in barcode_data['unscanned']
                    ]
                    setup_order_list(scanned_items, listItemScaned)
                    setup_order_list(unscanned_items, listItemNotScaned)
                    self.log_signal.emit(f"Barcode: {barcode_text} scanned!", "success")
                else:
                    print("No data found for this barcode")
                    statusBar.showMessage("No data found for this barcode")
                    self.log_signal.emit(f"Error: passing barcode xwx", "error")
                    
                
            except Exception as e: # Error handling for Item Scan
                print(f"Error: {e}")
                statusBar.showMessage("Error: Invalid barcode")
                if barcode_data.get('statusCode') == 400:
                    self.log_signal.emit(f"Scan start barcode first!", "error")
                    return
                if barcode_data.get('statusCode') == 403:
                    self.log_signal.emit(f"Barcode: {barcode_text} already scanned!", "error")
                    return
                else:
                     self.log_signal.emit(f"Error: Barcode: {barcode_text}", "error")
        