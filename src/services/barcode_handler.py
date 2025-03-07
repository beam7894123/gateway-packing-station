from services.api_service import APIService
from components.order_list import OrderItem, setup_order_list

def handle_barcode(barcode_text, config_manager, listItemScaned, listItemNotScaned, statusBar):
    # Start load order data and Start Record <--- NEED ADD
    if barcode_text.startswith("start|"):
        _, order_id = barcode_text.split('|', 1)
        if order_id.isdigit():
            try:
                order_data = APIService.post_data('/packing-station/start',
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
                else:
                    print("No data found for this order ID")
                    statusBar.showMessage("No data found for this order ID")
            except Exception as e:
                print(f"Error fetching order data: {e}")
                statusBar.showMessage("Error fetching order data")
        else:
            print("Invalid order ID xwx")
            statusBar.showMessage("Invalid order ID!")
            
    else:
        try:
            barcode_data = APIService.post_data('/packing-station/item/', {
                'orderId': "1",
                'station': config_manager.get_station_id(),
                'itemCode': barcode_text
            })
            # print(barcode_data.get('statusCode'))
            
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
            