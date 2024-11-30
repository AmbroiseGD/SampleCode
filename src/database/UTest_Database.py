import unittest
import os
import logging
from pathlib import Path
from database import HandleDatabase

class HandleDatabase_ModifyCompany(unittest.TestCase):

    def setUp(self):
        cfd = os.path.dirname(os.path.abspath(__file__))
        print(cfd)
        logger = logging.getLogger(str(Path(cfd)/f"{__file__}.log"))
        database_path = Path(cfd).parent.parent/"test"/"test-data.json"
        print(database_path)
        self.handler = HandleDatabase(logger, database_path)
        self.old_data = self.handler.get_data()
        pass

    def tearDown(self):
        self.handler.data = self.old_data
        pass

    def test_modify_company(self):
        old_company_data = self.handler.get_company().copy()
        self.handler.modify_company("TestCompany","TestAddress","TestPhoneNumber","TestMail")
        company_data = self.handler.get_company()
        self.assertNotEqual(old_company_data,company_data)

        self.assertEqual(company_data["name"], "TestCompany")
        self.assertEqual(company_data["address"], "TestAddress")
        self.assertEqual(company_data["mail"], "TestPhoneNumber")
        self.assertEqual(company_data["phone"], "TestMail")

    def test_modify_company_not_set(self):
        self.handler.data["company"] = {
            "name": "",
            "address": "",
            "phone": "",
            "mail": ""
        }
        self.assertRaises(Exception,self.handler.modify_company,"TestCompany","TestAddress","TestPhoneNumber","TestMail")

class HandleDatabase_SetCompany(unittest.TestCase):

    def setUp(self):
        cfd = os.path.dirname(os.path.abspath(__file__))
        print(cfd)
        logger = logging.getLogger(str(Path(cfd) / f"{__file__}.log"))
        database_path = Path(cfd).parent.parent / "test" / "test-data.json"
        print(database_path)
        self.handler = HandleDatabase(logger, database_path)
        self.old_data = self.handler.get_data()
        pass

    def tearDown(self):
        self.handler.data = self.old_data
        pass

    def test_set_company_init(self):
        self.handler.data["company"] = {
            "name" : "",
            "address" : "",
            "phone" : "",
            "mail" : ""
        }
        self.handler.set_company("NewTest","NewAddress","NewPhone","NewMail")
        company_data = self.handler.get_company()
        self.assertEqual(company_data["name"], "NewTest")
        self.assertEqual(company_data["address"], "NewAddress")
        self.assertEqual(company_data["mail"], "NewMail")
        self.assertEqual(company_data["phone"], "NewPhone")

    def test_set_company_non_empty(self):
        old_company_data = self.handler.get_company().copy()
        self.assertRaises(Exception,self.handler.set_company,"NewTest","NewAddress","NewPhone","NewMail")
        company_data = self.handler.get_company()
        self.assertDictEqual(old_company_data,company_data)
if __name__ == '__main__':
    unittest.main()
