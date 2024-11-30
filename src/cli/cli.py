import click
import json
import os
from pathlib import Path
from database import database as db
import logging
from click import password_option


@click.group("cli")
def cli():
    pass

@cli.group("database")
def database():
    if "SimpleAccounting" not in os.listdir(Path(os.environ.get("TMPDIR"))) :
        os.mkdir(Path(os.environ.get("TMPDIR"))/"SimpleAccounting")
    pass

@database.command("init")
@click.argument("database_name", type=click.STRING)
def init_database(database_name):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path)+".log")
    init_file = {
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
    if not os.path.exists(file_path):
        click.echo(f"Creating Database in {file_path}.")
        logger.info(f"Creating Database in {file_path}.")
        with open(file_path, "w") as database_file:
            json.dump(init_file, database_file, indent=4)
        if input("Would you like to set company data? These information can be set and modified later on.[Y|n]") in  ["Y","Yes","y","yes"]:
            name = input("What is the name of the company?")
            address = input("What is the address of the company?")
            phone = input("What is the phone number of the company?")
            mail = input("What is the mail address of the company?")
            set_company(database_name, name, address, phone, mail)
    else :
        click.echo(f"A Database already exists at this path ({file_path}).\nPlease remove it first.")
        logger.warning(f"A Database already exists at this path ({file_path}).\nPlease remove it first.")

@database.command("remove")
@click.argument("database_name", type=click.STRING)
def delete_database(database_name):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    else:
        logger = logging.getLogger(str(file_path) + ".log")
        os.remove(file_path)
        click.echo(f"The Database {database_name} has been successfully removed.")
        logger.info(f"The Database {database_name} has been successfully removed.")

@database.command("list")
def print_databases():
    for datab in list_databases():
        click.echo(datab)

def list_databases():
    folder_path = Path(os.environ.get("TMPDIR")) / "SimpleAccounting"
    folder = os.listdir(folder_path)
    databases_list =[file.replace(".json", "") for file in folder if Path(file).suffix == ".json"]
    return databases_list

@cli.group("set")
def set_database():
    pass

@set_database.command("company")
@click.argument("database_name", type=click.STRING)
@click.argument('name', type=click.STRING)
@click.argument('address', type=click.STRING)
@click.argument('phone', type=click.STRING)
@click.argument('mail', type=click.STRING)
def set_company(database_name, name, address, phone, mail):
    """
    Set or Modify the company infos.

    :param database_name: Name of the database.
    :param name: Name of the company.
    :param address: Address of the company.
    :param phone: Phone Number of the company.
    :param mail: Mail Address of the company.
    :return: Updates the database with given data.
    """
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.set_company(name, address, phone, mail)

@cli.group()
def add():
    pass

@add.command("contact")
@click.argument("database_name", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.argument("gender", type=click.Choice(["female","male"]))
@click.argument("mail", type=click.STRING)
@click.argument("address",type=click.STRING)
@click.argument("phone", type=click.STRING)
@click.argument("birthdate", type=click.DateTime(formats=["%Y-%m-%d"]))
def add_contact(database_name, name,gender, address, phone, mail,birthdate):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.add_contact(name,gender, address, phone, mail,birthdate)

@add.command("product")
@click.argument("database_name", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.argument("price", type=click.FloatRange(0))
@click.argument("quantity",type=click.FloatRange(0))
def add_product(database_name, name, price, quantity):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.add_product(name, price, quantity)

@add.command("service")
@click.argument("database_name", type=click.Choice(list_databases()))
@click.argument("name", type=click.STRING)
@click.argument("price", type=click.FloatRange(0))
@click.argument("rate",type=click.Choice(["HOURLY","WEEKLY","MONTHLY"]))
def add_service(database_name:str, name:str, price:float, rate:str):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.add_service(name, price, rate)

@add.command("bank")
@click.argument("name", type=click.STRING)
@click.argument("bank_name", type=click.STRING)
@click.argument("iban", type=click.STRING)
@click.argument("bic",type=click.STRING)
@click.argument("password", type=password_option())
def add_bank_account():
    pass

@cli.group("modify")
def modify_database():
    # Warning that every modification is definitive.
    pass

@modify_database.command("company")
@click.argument("database_name", type=click.STRING)
@click.option('--name',"-n", type=click.STRING, default=None, help='Change Company name in database')
@click.option('--address',"-a", type=click.STRING, default=None, help='Change Company address in database')
@click.option('--phone',"-p", type=click.STRING, default=None, help='Change Company phone in database')
@click.option('--mail',"-m", type=click.STRING, default=None, help='Change Company mail in database')
def modify_company(database_name, name, address, phone, mail):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.modify_company(name, address, phone, mail)

@modify_database.command("contact")
@click.argument("database_name", type=click.STRING)
@click.argument("contact_name", type=click.STRING)
@click.option('--name',"-n", type=click.STRING, default=None, help='Change Contact name in database')
@click.option('--address',"-a", type=click.STRING, default=None, help='Change Contact address in database')
@click.option('--phone',"-p", type=click.STRING, default=None, help='Change Contact phone in database')
@click.option('--mail',"-m", type=click.STRING, default=None, help='Change Contact mail in database')
def modify_contact(database_name, contact_name, name, address, phone, mail):
    file_path = Path(os.environ.get("TMPDIR"))/"SimpleAccounting"/f"{database_name}.json"
    logger = logging.getLogger(str(file_path) + ".log")
    handler = db.HandleDatabase(logger, file_path)
    handler.modify_contact(contact_name, name, address, phone, mail)

@cli.group("delete")
def delete_database_parts():
    # Warning that every deletion is definitive.
    pass