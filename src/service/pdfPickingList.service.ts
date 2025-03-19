import puppeteer from 'puppeteer';
import * as bwipJs from 'bwip-js';
import * as fs from 'fs';
import * as path from 'path';

// async function generateItemCodeBarcode(itemCode: string) { // Generate barcode --> save it --> load it again --> cover to base64 XD
//     return new Promise((resolve, reject) => {
//         bwipJs.toBuffer(
//             {
//                 bcid: 'code128',
//                 text: itemCode,
//                 scale: 3,
//                 height: 10,
//                 includetext: true,
//             },
//             (err, pngBuffer) => {
//                 if (err) reject(err);
//                 else {
//                     const barcodePath = path.join(__dirname, '../../assets/barcodes', `${itemCode}.png`);

//                     // Ensure barcode directory exists
//                     const barcodeDir = path.dirname(barcodePath);
//                     if (!fs.existsSync(barcodeDir)) {
//                         fs.mkdirSync(barcodeDir, { recursive: true });
//                     }

//                     fs.writeFileSync(barcodePath, pngBuffer);
//                     console.log(`Barcode generated: ${barcodePath}`);
//                     const barcodeBuffer = fs.readFileSync(barcodePath);
//                     const barcodeBase64 = `data:image/png;base64,${barcodeBuffer.toString('base64')}`;
//                     resolve(barcodeBase64);
//                 }
//             }
//         );
//     });
// }

async function generateItemCodeBarcode(itemCode: string): Promise<string> {
    try {
        const itemCodeBarcodeImage = await bwipJs.toBuffer({
            bcid: 'code128',       
            text: itemCode,
            scale: 3,              
            height: 10,          
            includetext: true,     
            textxalign: 'center',
        });

        // Convert buffer to Base64 string
        return itemCodeBarcodeImage.toString('base64');
    } catch (error) {
        console.error(`Failed to generate barcode for ${itemCode}:`, error);
        throw new Error(`Failed to generate barcode`);
    }
}

async function generateOrderBarcode(orderId: number, text: string): Promise<string> {
    try {
        const barcodeImage = await bwipJs.toBuffer({
            bcid: 'code128',       
            text: `${text}|${orderId}`,
            scale: 3,              
            height: 10,          
            includetext: false,     
            textxalign: 'center',
        });

        // Convert buffer to Base64 string
        return barcodeImage.toString('base64');
    } catch (error) {
        console.error(`Failed to generate barcode for order-${orderId}:`, error);
        throw new Error(`Failed to generate barcode`);
    }
}

async function pdfPickingList(order) {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      });
    const page = await browser.newPage();

    for (const orderItem of order.orderItems) {
        orderItem.barcodePath = await generateItemCodeBarcode(orderItem.item.itemCode);
    }

    const OrderStartBarcode = await generateOrderBarcode(order.id, 'start');
    const OrderEndBarcode = await generateOrderBarcode(order.id, 'end');

    // Generate the HTML content for the PDF
    const htmlContent = `
        <html>
        <head>
            <title>Picking Order #${order.id}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .header {
                    text-align: center;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                .items-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .items-table th, .items-table td {
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: left;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Picking Order #${order.id}</h1>
                <div style="text-align: center;">
                    <img src="data:image/png;base64,${OrderStartBarcode}" height="50" alt="Order Barcode"/>
                </div>
                <p>Customer: ${order.customer}</p>
                <p>Order Date: ${new Date(order.createdAt).toLocaleDateString()}</p>
            </div>
            <table class="items-table">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Item</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Barcode</th>
                    </tr>
                </thead>
                <tbody>
                    ${order.orderItems.map(item => `
                        <tr>
                            <td><img src="${item.item.image}" height="50" /></td>
                            <td>${item.item.name}</td>
                            <td>${item.item.price}</td>
                            <td>${item.quantity}</td>
                            <td><img src="data:image/png;base64,${item.barcodePath}" height="50" /></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            &nbsp;
            <div style="text-align: center;">
                <img src="data:image/png;base64,${OrderEndBarcode}" height="50" alt="Order Barcode"/>
            </div>
        </body>
        </html>
    `;

    // console.log(htmlContent);
    await page.setContent(htmlContent);
    const pdfBuffer = await page.pdf({ format: 'A4' });
    await browser.close();

    return pdfBuffer;  // Return the PDF buffer
}

export { pdfPickingList };