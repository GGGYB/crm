# -*- coding: utf-8 -*-
__author__ = 'Jun'


from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
import sys
from decimal import Decimal as D
from commons import common
from commons.const import const
from commons import filters
from .testAddContact import AddContact
from .testDeleteContact import DeleteContacts
from .testGetContact import GetContacts
from .testUpdateContact import UpdateContacts

class Contacts:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.add_contact = AddContact(cookie, csrf)
        self.delete_contact = DeleteContacts(cookie, csrf)
        self.get_contact = GetContacts(cookie, csrf)
        self.update_contact =UpdateContacts(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def testContacts(self):
        self.add_contact.add_contact()
        # self.add_contact.contacts_camcard_launch()
        self.get_contact.duplicate_contacts()
        self.testAdd()
        scopes = self.get_contact.get_all_scope()
        self.filters.filters_by_business('contacts', scopes)
        for scope in scopes:
            self.testUpdateContact(scope)
            self.testDeletContact(scope)


    def testAdd(self):
        contact_id = self.add_contact.add_contact()
        id = self.add_contact.add__event_for_contact(contact_id)

    def testDeletContact(self, scope):
        contact_ids = []
        for i in range(5):
            contact_ids.append(self.add_contact.add_contact())
            if i<2:
                self.delete_contact.delete_contact(contact_ids[0])
                contact_ids.remove(contact_ids[0])
        self.update_contact.batch_update_contacts(scope, contact_ids)
        self.delete_contact.delete_contacts(scope, contact_ids)

    def testUpdateContact(self, scope):
        contact_id = self.add_contact.add_contact()
        self.update_contact.write_revisit_log(scope, contact_id)
