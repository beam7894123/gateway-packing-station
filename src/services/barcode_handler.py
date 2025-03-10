from services.api_service import APIService
from components.order_list import OrderItem, setup_order_list
from services.config_manager import ConfigManager
from services.video_service import VideoCaptureService
from qasync import asyncSlot

class BarcodeHandler:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.video_service = VideoCaptureService()
        self.api_service = APIService()
        self._active = True
        
    def cancel(self):
        """Cancel pending operations"""
        self._active = False

    async def handle_barcode(self,
                       barcode_text,
                       config_manager,
                       listItemScaned,
                       listItemNotScaned,
                       statusBar,
                       status_callback,):
        if not self._active:
            return
        if barcode_text.startswith("start|"):
            _, order_id = barcode_text.split('|', 1)
            if order_id.isdigit():
                try:
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
                        # Set order ID and start recording
                        config_manager.set_order_id(order_id)
                        self.video_service.start_recording()
                        status_callback(1)
                    else:
                        print("No data found for this order ID")
                        statusBar.showMessage("No data found for this order ID")
                except Exception as e:
                    print(f"Error fetching order data: {e}")
                    statusBar.showMessage("Error fetching order data")
            else:
                print("Invalid order ID xwx")
                statusBar.showMessage("Invalid order ID!")
        
        # End Record and Send Order Data
        elif barcode_text.startswith("end|"):
            _, order_id = barcode_text.split('|', 1)
            if order_id.isdigit():
                try:
                    order_data = await self.api_service.post_data('/packing-station/end',
                                                    {
                                                        'orderId': order_id,
                                                        'station': config_manager.get_station_id(),
                                                        'status': '2'
                                                    })
                except Exception as e:
                    print(f"Error senting order data: {e}")
                    statusBar.showMessage("Error senting order data")
        
        # Item Scan
        else:
            try:
                barcode_data = await self.api_service.post_data('/packing-station/item/', {
                    'orderId': "1",
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
                
            except Exception as e:
                print(f"Error: Invalid barcode")
                statusBar.showMessage("Error: Invalid barcode")
                