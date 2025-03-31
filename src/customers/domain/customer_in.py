from shared.exceptions.generic import GenericException
from shared.infrastructure.get_uuid import get_uuid
from shared.infrastructure.timestamps import get_timestamp
from shared.value_objects.agent_id import AgentID
from shared.value_objects.company import Company
from shared.value_objects.customer_external_id import CustomerExternalId
from shared.value_objects.delegation import Delegation
from shared.value_objects.email import Email
from shared.value_objects.name import Name
from shared.value_objects.phone import Phone
from shared.value_objects.gdpr import Gdpr


class CustomerIn:

    def __init__(self, name=None, email=None, phone=None, centribot_external_id=None, customer_id=None, active=True,
                 company=None, agent_id=None, last_comment_at=None, delegation=None, external_id=None, gdpr=None,
                 patch=False):
        self.patch = patch
        self.customer_id = customer_id or get_uuid()
        self.name = name
        self.email = email
        self.phone = phone
        self.centribot_external_id = centribot_external_id
        self.active = active
        self.timestamp_at = get_timestamp()
        self.company = company
        self.agent_id = agent_id
        self.last_comment_at = last_comment_at
        self.delegation = delegation
        self.external_id = external_id
        self.gdpr = gdpr
        self.gdpr_updated = False

        if not patch:
            self.__check()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = Name(name).name if name is not None or not self.patch else None

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if email:
            email = Email(email).email

        self.__email = email

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if phone:
            phone = Phone(phone).phone

        self.__phone = phone

    @property
    def centribot_external_id(self):
        return self.__centribot_external_id

    @centribot_external_id.setter
    def centribot_external_id(self, centribot_external_id):
        if centribot_external_id:
            # todo check centribot_external_id format
            pass
        self.__centribot_external_id = centribot_external_id

    def __check(self):
        if not self.email and not self.phone and not self.centribot_external_id:
            raise GenericException('Must exist at least one of: email, phone, centribot_external_id')

    @property
    def company(self):
        return self.__company

    @company.setter
    def company(self, company):
        self.__company = Company(company).company

    @property
    def agent_id(self):
        return self.__agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        self.__agent_id = AgentID(agent_id).agent_id

    @property
    def delegation(self):
        return self.__delegation

    @delegation.setter
    def delegation(self, delegation):
        self.__delegation = Delegation(delegation).delegation

    @property
    def external_id(self):
        return self.__external_id

    @external_id.setter
    def external_id(self, external_id):
        self.__external_id = CustomerExternalId(external_id).external_id

    @property
    def gdpr(self):
        return self.__gdpr

    @gdpr.setter
    def gdpr(self, gdpr):
        self.__gdpr = Gdpr(gdpr).gdpr if gdpr is not None else None
