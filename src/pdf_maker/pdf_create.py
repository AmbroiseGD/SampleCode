import datetime
from pathlib import Path

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab_qr_code import qr_draw
from reportlab.lib.units import mm,cm



c = Canvas("out.pdf")
c.setTitle("Title")
c.setAuthor("Hannah Mertens")

c.setFont("Helvetica",10)
company_name = c.beginText(13*cm,28*cm)
company_name.setFont("Helvetica-Bold",10)
# A4 max 21x29,7
company_name.textLine("Hannah Mertens")
company_name.textLine("Heilpraktikerin - Osteopathie")
c.drawText(company_name)

c.setFont("Helvetica",10)
address = c.beginText(13*cm,26*cm)
for text in "Bleibtreustr. 6\n53229 Bonn".splitlines():
    address.textLine(text)
address.textLine("017623787473")
c.drawText(address)

mail = c.beginText(13*cm,24*cm)
mail.textLine("mail.address@mailservice.com")
c.drawText(mail)
#### Left Side
c.setFontSize(8)
c.drawString(2*cm,24.5*cm,"Hannah Mertens    Bleibtreustr. 6    53229 Bonn")
c.setFontSize(10)

client_block = c.beginText(2*cm,24*cm)
client_block.textLine("Agastaya Jain-Delacroix")
for text in "Franz-Peter-Kürten-Weg 13\n51069 Köln".splitlines():
    client_block.textLine(text)
c.drawText(client_block)
#####
c.setFont("Helvetica-Bold",10)
c.drawString(2*cm,20*cm,"Rechnung   Nr.{BillNumber}")
c.drawString(13*cm,20*cm,"20/10/2024")

c.drawString(2*cm,19*cm,"Patient(in)")
c.drawString(2*cm,18.5*cm,"Diagnose(n):")

c.setFont("Helvetica",10)
c.drawString(5*cm,19*cm,"{patientName}, geb. {birthDate}")
c.drawString(5*cm,18.5*cm,"HWS-Myogelose (M62.88)")


c.drawString(2*cm,17*cm,"Fur meine Leistungen erlaube ich mir wie folgt zu berechnen:")
##### Products and Service list
c.setFontSize(8)
c.drawString(2*cm,16*cm,"Datum")
c.drawString(4*cm,16*cm,"GebüH")
c.drawString(5*cm,16*cm,"Leistung")
c.drawString(14*cm,16*cm,"Anzahl") # Quantity
c.drawRightString(17*cm,16*cm,"Honorar") # WTaxes Price
c.drawRightString(19*cm,16*cm,"G-Honorar") # ATaxes Price
c.line(2*cm,15.85*cm,19*cm,15.85*cm)
serviceList = [
    {
        "date" : [2024,6,15],
        "gebuh" : "35.2",
        "serviceName" : "Osteopathische Behandlung des Schultergelenkes und der\nWirbelsäule",
        "quantity" : 1,
        "price" : 90.00,
        "priceAT" : 90.00
    },
    {
        "date" : datetime.date(2024,7,4),
        "gebuh" : "35.2",
        "serviceName" : "Osteopathische Behandlung des Schultergelenkes und der\nWirbelsäule",
        "quantity" : 1,
        "price" : 90.00,
        "priceAT" : 90.00
    },
    {
        "date" : datetime.date(2024,7,11),
        "gebuh" : "35.2",
        "serviceName" : "Osteopathische Behandlung des Schultergelenkes und der\nWirbelsäule",
        "quantity" : 1,
        "price" : 90.00,
        "priceAT" : 90.00
    },
    {
        "date" : datetime.date(2024,9,12),
        "gebuh" : "35.2",
        "serviceName" : "Osteopathische Behandlung des Schultergelenkes und der\nWirbelsäule",
        "quantity" : 1,
        "price" : 90.00,
        "priceAT" : 90.00
    },
    {
        "date" : datetime.date(2024,9,30),
        "gebuh" : "35.2",
        "serviceName" : "Osteopathische Behandlung des Schultergelenkes und der\nWirbelsäule",
        "quantity" : 1,
        "price" : 90.00,
        "priceAT" : 90.00
    }
]
index=0
for  service in serviceList :
    index += 1
    c.drawString(2 * cm, 16 * cm-index*2*8, datetime.date(*service["date"]).strftime("%d.%m.%Y"))
    c.drawString(4 * cm, 16 * cm-index*2*8, service["gebuh"])
    services = c.beginText(5 * cm, 16 * cm-index*2*8)
    services.setLeading(8)
    for text in service["serviceName"].splitlines():
        services.textLine(text)
    c.drawText(services)
    #c.drawString(5 * cm, 16 * cm-index*2*8, service["serviceName"])
    c.drawString(14 * cm, 16 * cm-index*2*8, str(service["quantity"]))  # Quantity
    c.drawRightString(17 * cm, 16 * cm-index*2*8, str(service["price"]))  # WTaxes Price
    c.drawRightString(19 * cm, 16 * cm-index*2*8, str(service["priceAT"]))  # ATaxes Price
c.line(2 * cm, 15.85 * cm-index*2*8-8, 19 * cm, 15.85 * cm-index*2*8-8)
c.setFont("Helvetica-Bold",10)
c.drawString(14*cm,15.85 * cm-(index+1)*2*8-4,"Gesamt")
c.drawRightString(19*cm,15.85 * cm-(index+1)*2*8-4,"EUR {totalPrice}")

c.drawString(2*cm,15.85 * cm-index*2*8-8-2*cm,"Mit freundlichen Grüßen")

# Final line
c.line(1.5*cm,4.5*cm,19.5*cm,4.5*cm)

FullName, IBAN, BIC, price, BillNumber = ["","","","",""]


bank_transfer = f"""BCD
    002
    1
    SCT
    {BIC}
    {FullName}
    {IBAN}
    EUR{price} 
    
    {BillNumber}
    """
qr_draw(c, bank_transfer, x="1cm", y="1cm", size="3cm")
bank_info = c.beginText(5*cm,3.5*cm)
bank_info.textLine("Scan with your bank app to pay or use the following info :")
bank_info.textLine("Hannah Mertens")
bank_info.textLine("IBAN")
bank_info.textLine("BIC")
bank_info.textLine("BillNumber")
c.drawText(bank_info)

# down blocks
c.setFont("Helvetica",8)
c.drawString(1.5*cm,0.5*cm,"Rechnung Nr. {BillNo}")
c.drawString(17.5*cm,0.5*cm,f"Seite {c.getPageNumber()}")

c.showPage()

c.save()

class InvoiceMaker:
    file :Canvas
    def __init__(self, bill_number:int, base_path:Path, date:datetime = datetime.date.today()):
        path_to_pdf = base_path / date.year / date.month / str(bill_number)+".pdf"
        self.file = Canvas(path_to_pdf)

    def add_company_block(self, company):
        self.file.drawString(12 * cm, 27 * cm, company.get("name"))
        address_block = self.file.beginText(12 * cm, 26 * cm)
        for txt in company.get("address").splitlines():
            address_block.textLine(txt)
        address_block.textLine(company.get("phone"))
        self.file.drawText(address_block)

    def add_client_block(self, company, client):
        self.file.setFontSize(8)
        self.file.drawString(2 * cm, 24.5 * cm, f"{company.get("name")}    {company.get("address").replace("\n","    ")}")
        self.file.setFontSize(10)

        client_block = self.file.beginText(2 * cm, 24 * cm)
        client_block.textLine(client["name"])
        for txt in client["address"].splitlines():
            client_block.textLine(txt)
        self.file.drawText(client_block)

    def add_footer(self, bill_no):
        self.file.setFont("Helvetica", 8)
        self.file.drawString(1.5 * cm, 0.5 * cm, f"Rechnung Nr {bill_no}")
        self.file.drawString(16.5 * cm, 0.5 * cm, f"Seite {self.file.getPageNumber()} von 'max num page'")
        self.file.showPage()

    def add_qr_code(self, bill_no, bank_data, total_price):
        # QR Code supported in (Austria, Belgium, Finland, Germany, The Netherlands)
        self.file.line(1.5 * cm, 4.5 * cm, 19.5 * cm, 4.5 * cm)
        transfer_qr = f"""BCD
        002
        1
        SCT
        {bank_data.get("BIC")}
        {bank_data.get("FullName")}
        {bank_data.get("IBAN")}
        EUR{total_price} 

        {bill_no}
        """
        qr_draw(self.file, transfer_qr, x="1cm", y="1cm", size="3cm")
        bank_block = self.file.beginText(5 * cm, 3.5 * cm)
        bank_block.textLine("Scan with your bank app to pay or use the following info :")
        bank_block.textLine(bank_data.get("FullName"))
        bank_block.textLine(bank_data.get("IBAN"))
        bank_block.textLine(bank_data.get("BIC"))
        bank_block.textLine(bill_no)
        self.file.drawText(bank_block)

    def add_bank_data(self, bill_no, bank_data):
        self.file.line(1.5 * cm, 4.5 * cm, 19.5 * cm, 4.5 * cm)
        bank_block = self.file.beginText(2 * cm, 3.5 * cm)
        bank_block.textLine("Please use the following info to make the transfer:")
        bank_block.textLine(bank_data.get("FullName"))
        bank_block.textLine(bank_data.get("IBAN"))
        bank_block.textLine(bank_data.get("BIC"))
        bank_block.textLine(bill_no)
        self.file.drawText(bank_block)

    def generate(self):
        pass