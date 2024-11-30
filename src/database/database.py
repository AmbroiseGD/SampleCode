import json
from dataclasses import dataclass,field
from datetime import datetime
from enum import Enum
import logging


@dataclass
class Company:
    name : str
    address : str
    phone : str
    mail : str

@dataclass
class ClientBill :
    on_going : field(default_factory=list)
    paid : field(default_factory=list)

@dataclass
class Contact:
    name: str
    mail: str
    address: str
    phone: str
    bills : ClientBill

class BillStatus(Enum) :
    ONGOING = "ONGOING"
    PAID = "PAID"

@dataclass
class Product:
    name : str
    price : float
    quantity : float

class ServiceRate(Enum) :
    HOURLY = "HOURLY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

@dataclass
class Service:
    name : str
    price : str
    rate : ServiceRate = ServiceRate.HOURLY

@dataclass
class Bill:
    number : int
    date : datetime
    contactName : Contact
    products : field(default_factory=dict[Product])
    status: BillStatus = BillStatus.ONGOING

@dataclass
class BankData:
    bank : str
    name : str
    iban : str
    bic : str

class HandleDatabase :
    """
    Read the database to re/initialise the software
    """
    # REGEX IBAN : [A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}
    data = {
        "company": {
            "name": "",
            "address": "",
            "phone": "",
            "mail": ""
        },
        "contacts": {},
        "bills": {},
        "products": {},
        "bank_accounts": {}
    }
    path_to_database=""
    def __init__(self, logger : logging.Logger ,path_to_database ):
        self.log = logger
        self.path_to_database = path_to_database
        database_file= open(self.path_to_database,"r")
        self.data = json.load(database_file)
        database_file.close()

    def __del__(self):
        database_file = open(self.path_to_database, "w")
        json.dump(self.data, database_file, indent=4)
        database_file.close()

    def get_data(self):
        return self.data

    def get_data_class(self):
        company = self.data.get("company")
        database = {
            "company" : Company(company.get("name"),company.get("address"),company.get("phone"),company.get("mail")),
            "contacts": {},
            "products": {},
            "services": {},
            "bank_accounts": {},
            "bills": {
                "received" : {},
                "sent":{}
            }
        }
        for contact in self.data.get("contacts").values():
            client_bills = ClientBill(contact["bills"][BillStatus.ONGOING],contact["bills"][BillStatus.PAID])
            database["contacts"][contact["name"]]= Contact(
                contact["name"],contact["mail"],contact["address"],contact["phone"],client_bills)
        for bank_account in self.data.get("bank_accounts").values():
            database["bank_accounts"][bank_account["IBAN"]] = BankData(
                bank=bank_account["bank"],
                name=bank_account["name"],
                iban=bank_account["IBAN"],
                bic= bank_account["BIC"]
            )
        for product in self.data["products"].values():
            database["products"][product["name"]] = Product(
                name= product["name"],
                price= product["price"],
                quantity= product["quantity"]
            )
        for service in self.data["services"].values():
            database["services"][service["name"]] = Service(
                name= service["name"],
                price= service["price"],
                rate= ServiceRate(service["rate"])
            )
        for bill_no, received_bill in self.data["bills"]["received"].items():
            database["bills"]["received"][bill_no]= Bill(
                number=bill_no,
                date= received_bill["date"],
                contactName= received_bill["contact_name"],
                status= BillStatus(received_bill["status"]),
                products=[] # to figure it out
            )
        return database

    def print_data(self):
        print(json.dumps(self.data,indent=2))

    ##### Company
    def set_company(self,name :str, address:str, phone:str, mail:str) ->None:
        company = self.data.get("company")
        if company.get("name") + company.get("address")+company.get("mail")+company.get("phone") != "":
            logging.warning("The company has already been set, please use modify to update it.")
        else :
            company["name"]=name
            company["address"]=address
            company["phone"]=phone
            company["mail"]=mail

    def modify_company(self, name:str=None, address:str=None, phone:str=None, mail:str=None) -> None:
        company = self.data.get("company")
        if company.get("name") + company.get("address")+company.get("mail")+company.get("phone") == "":
            logging.warning("The company has not been set, please set it first.")
        else :
            if name is not None:
                logging.info(f'Company name changed from {company.get("name")} to {name}.')
                company["name"] = name
            if address is not None:
                logging.info(f'Company address changed from {company.get("address")} to {address}.')
                company["address"] = address
            if phone is not None:
                logging.info(f'Company phone changed from {company.get("phone")} to {phone}.')
                company["phone"] = phone
            if mail is not None:
                logging.info(f'Company mail changed from {company.get("mail")} to {mail}.')
                company["mail"] = mail
            logging.info(f"Company Data : \n {json.dumps(company,indent=2)}.")

    def get_company(self) -> dict :
        return self.data.get("company")
    ##### Contacts
    def add_contact(self,name:str, gender: str , address:str, phone:str, mail:str, birth_date:datetime):
        contacts = self.data.get("contacts")
        if name not in contacts :
            contacts[name]= {
                "name" : name,
                "gender" : gender,
                "address" : address,
                "phone" : phone,
                "mail" : mail,
                "birth_date" : birth_date.strftime("%Y-%m-%d"),
                "bills" : {
                    "ONGOING" : [],
                    "PAID" : []
                }
            }
        else :
            logging.ERROR(f"This contact already exists with the following information.\n {json.dumps(contacts[name],indent=2)}")
            raise Exception(f"This contact already exists with the following information.\n {json.dumps(contacts[name],indent=2)}")

    def modify_contact(self, old_name:str, new_name:str=None, gender:str = None, address:str=None, phone:str=None, mail:str=None, birth_date:datetime = None):
        contacts = self.data.get("contacts")
        if old_name not in contacts:
            logging.ERROR("This contact you are trying to modify does not exist in this database.")
            raise Exception("This contact you are trying to modify does not exist in this database.")
        else:
            contact = contacts.get(old_name)
            if new_name is not None :
                contacts.pop(old_name)
                logging.info(f'Contact name changed from {old_name} to {new_name}.')
                contact["name"]=new_name
                contacts[new_name]=contact
            if address is not None:
                logging.info(f'Contact name changed from {contact["address"]} to {address}.')
                contact["address"] = address
            if mail is not None:
                logging.info(f'Contact name changed from {contact["mail"]} to {mail}.')
                contact["mail"] = mail
            if phone is not None:
                logging.info(f'Contact name changed from {contact["phone"]} to {phone}.')
                contact["phone"] = phone
            logging.info(f"After changes the contact is \n {json.dumps(contact,indent=2)}")

    def delete_contact(self, name:str):
        contacts=self.data.get("contacts")
        if name not in contacts:
            logging.ERROR("This contact you are trying to delete does not exist in this database.")
            raise Exception("This contact you are trying to delete does not exist in this database.")
        else :
            logging.info(f"The contact info were : \n {json.dumps(contacts.get(name))}")
            contacts.pop(name)
            # check if unpaid bills ?

    def get_contact(self, name:str) -> dict:
        return self.data.get("contacts").get(name)
    ##### Products
    def add_product(self, name:str, price:float, quantity:float):
        products = self.data.get("products")
        if name not in products :
            products[name] = {
                "name" : name,
                "price" : price,
                "quantity" : quantity
            }
        else :
            self.log.error("This product name is already used.")
            raise Exception("This product name is already used.")

    def modify_product(self, old_name: str, new_name: str = None, price: float = None, quantity: float = None):
        products = self.data.get("products")
        if old_name not in products:
            logging.ERROR("This product you are trying to modify does not exist in this database.")
            raise Exception("This product you are trying to modify does not exist in this database.")
        else:
            product = products.get(old_name)
            if new_name is not None:
                products.pop(old_name)
                logging.info(f'Product name changed from {old_name} to {new_name}.')
                product["name"] = new_name
                products[new_name] = product
            if price is not None:
                logging.info(f'Product name changed from {product["price"]} to {price}.')
                product["price"] = price
            if quantity is not None:
                logging.info(f'Product name changed from {product["quantity"]} to {quantity}.')
                product["quantity"] = quantity
            logging.info(f"After changes the product is \n {json.dumps(product, indent=2)}")

    def delete_product(self, name: str):
        products = self.data.get("products")
        if name not in products:
            logging.ERROR("This product you are trying to delete does not exist in this database.")
            raise Exception("This product you are trying to delete does not exist in this database.")
        else:
            logging.info(f"The product info were : \n {json.dumps(products.get(name))}")
            products.pop(name)

    ##### Services
    def add_service(self, name:str, price:float, rate:str):
        services = self.data.get("services")
        if name not in services:
            services[name] = {
                "name": name,
                "price": price,
                "type" : rate
            }
        else:
            self.log.error("This service name is already used.")
            raise Exception("This service name is already used.")

    def modify_service(self, old_name: str, new_name: str = None, price: float = None, rate: str = None):
        services = self.data.get("services")
        if old_name not in services:
            logging.ERROR("This service you are trying to modify does not exist in this database.")
            raise Exception("This service you are trying to modify does not exist in this database.")
        else:
            service = services.get(old_name)
            if new_name is not None:
                services.pop(old_name)
                logging.info(f'Service name changed from {old_name} to {new_name}.')
                service["name"] = new_name
                services[new_name] = service
            if price is not None:
                logging.info(f'Service name changed from {service["price"]} to {price}.')
                service["price"] = price
            if rate is not None:
                logging.info(f'Service name changed from {service["rate"]} to {rate}.')
                service["rate"] = rate
            logging.info(f"After changes the service is \n {json.dumps(service, indent=2)}")

    def delete_service(self, name: str):
        services = self.data.get("services")
        if name not in services:
            logging.ERROR("This service you are trying to delete does not exist in this database.")
            raise Exception("This service you are trying to delete does not exist in this database.")
        else:
            logging.info(f"The service info were : \n {json.dumps(services.get(name))}")
            services.pop(name)

    ##### Bank Accounts
    ##### Bills
    def new_invoice(self, patient_name:str, products:dict):
        bills = self.data.get("bills").get("invoice")
        billNumber = max(bills.keys())+1
        today_date=datetime.today().strftime("%d/%m/%Y")
        patient = self.data.get("contacts").get(patient_name)

        #create_invoice_pdf()


