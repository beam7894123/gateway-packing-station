import asyncio
from services.api_service import APIService
from components.order_list import OrderItem, setup_order_list
from services.config_manager import ConfigManager

class BarcodeHandler:
    def __init__(self):
        self.api_service = APIService()
        self.config_manager = ConfigManager()
    
    async def handle_barcode(self,
                       barcode_text,
                       config_manager,
                       video_service,
                       listItemScaned,
                       listItemNotScaned,
                       statusBar,
                       set_status_label,):
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
                    print(order_data)
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
                        config_manager.set_order_id(order_id)
                        
                        video_service.toggle_recording()
                        set_status_label(1)
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
                    video_service.toggle_recording()
                    video_file = video_service.get_last_recorded_video()  # Implement this method in VideoCaptureService
                    set_status_label(2)
                    
                    await asyncio.sleep(1)
                    print("video file", video_file)
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
                        if order_data['status'] == '0':
                            print("Error sending order data")
                            statusBar.showMessage("Error sending order data")
                            set_status_label(3)
                            setup_order_list([], listItemScaned)
                            setup_order_list([], listItemNotScaned)
                        else:
                            print("Order data sent successfully")
                            statusBar.showMessage("Order data sent successfully")
                            setup_order_list([], listItemScaned)
                            setup_order_list([], listItemNotScaned)
                            self.config_manager.clear_order_id() # why???
                            set_status_label(0)
                except Exception as e:
                    print(f"Error sending order data: {e}")
                    statusBar.showMessage("Error sending order data")
                    set_status_label(3)
                    
        elif barcode_text.startswith("test1"):
            set_status_label(1)
        elif barcode_text.startswith("test2"):
            set_status_label(2)
        elif barcode_text.startswith("test3"):
            set_status_label(3)
        elif barcode_text.startswith("test0"):
            set_status_label(0)
                    
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
                    
                else:
                    print("No data found for this barcode")
                    statusBar.showMessage("No data found for this barcode")
                    
                
            except Exception as e:
                print(f"Error: Invalid barcode")
                statusBar.showMessage("Error: Invalid barcode")
        