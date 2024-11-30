import datetime
from pathlib import Path

from reportlab.pdfgen.canvas import Canvas
from reportlab_qr_code import qr_draw
from reportlab.lib.units import mm,cm

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