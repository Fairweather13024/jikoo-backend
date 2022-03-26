from sqlalchemy import event
from sqlalchemy.sql.schema import Table
from sqlalchemy.engine.base import Connection
from dataclasses import dataclass
from typing import Optional

from db.extensions import db


@dataclass
class Deal(db.Model):
    """
    Table for deals
     :param deal_id: unique deal id
     :param business_profile_id: business_profile_id
     :param name: deal name
     :param status_id: deal status
    """

    # adding specification to create json object
    deal_id: int
    business_profile_id: int
    name: str
    status: str

    __tablename__ = "deals"

    deal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_profile_id = db.Column(
        db.Integer, db.ForeignKey("business_profiles.profile_id"), nullable=False
    )
    name = db.Column(db.String(), nullable=False)
    status_id = db.Column(db.String(), nullable=False)

    def __init__(self, name: str, business_profile_id: int, status_id: int):
        self.name = name
        self.business_profile_id = business_profile_id
        self.status_id = status_id


@dataclass
class Transaction(db.Model):
    """
    Table for transactions
     :param transaction_id: unique deal id
     :param business_profile_id: business profile id
     :param name: deal name
     :param status_id: deal status
    """

    # adding specification to create json object
    transaction_id: int
    business_profile_id: int
    name: str
    status: str

    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_profile_id = db.Column(
        db.Integer, db.ForeignKey("business_profiles.profile_id"), nullable=False
    )
    name = db.Column(db.String(), nullable=False)
    status_id = db.Column(db.String(), nullable=False)

    def __init__(self, name: str, business_profile_id: int, status_id: int):
        self.name = name
        self.business_profile_id = business_profile_id
        self.status_id = status_id


@dataclass
class Project(db.Model):
    """
    Table for projects
     :param project_id: unique project id
     :param business_profile_id: id of the business profile
     :param status_id: status id of the project
     :param description: description of the project
     :param region: region of the particular project
     :param country: country of the particular project
     :param industry_type_id: industry_type_id of the project
     :param funded_by_equity: if the project is funded by equity
     :param equity_type_id: the type of equity used for project
     :param funded_by_debt: if the project is funded by debt
     :param debt_type_id: the type of debt used for project
     :param revenue: revenue of the project
     :param ebitda: ebitda of the project
    """

    # adding specification to create json object
    project_id: int
    business_profile_id: int
    status_id: int
    description: str
    region: str
    country: str
    industry_type_id: int
    funded_by_equity: bool
    equity_type_id: int
    funded_by_debt: bool
    debt_type_id: int
    revenue: int
    ebitda: int

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_profile_id = db.Column(db.Integer, db.ForeignKey("business_profiles.profile_id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.status_id"), nullable=False)
    description = db.Column(db.String(), nullable=False)
    region = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    industry_type_id = db.Column(db.Integer, db.ForeignKey("industry_types.industry_type_id"), nullable=False)
    funded_by_equity = db.Column(db.Boolean, nullable=False, default=False)
    equity_type_id = db.Column(db.Integer, db.ForeignKey("equity_types.equity_type_id"), nullable=True)
    funded_by_debt = db.Column(db.Boolean, nullable=False, default=False)
    debt_type_id = db.Column(db.Integer, db.ForeignKey("debt_types.debt_type_id"), nullable=True)
    revenue = db.Column(db.Integer, nullable=True, default=0)
    ebitda = db.Column(db.Integer, nullable=True, default=0)

    def __init__(
            self,
            business_profile_id: int,
            status_id: int,
            description: str,
            region: str,
            country: str,
            industry_type_id: int,
            funded_by_equity: bool,
            funded_by_debt: bool,
            equity_type_id: Optional[int] = None,
            debt_type_id: Optional[int] = None,
            revenue: Optional[int] = None,
            ebitda: Optional[int] = None
    ):
        self.business_profile_id = business_profile_id
        self.status_id = status_id
        self.description = description
        self.region = region
        self.country = country
        self.industry_type_id = industry_type_id
        self.funded_by_equity = funded_by_equity
        self.equity_type_id = equity_type_id
        self.funded_by_debt = funded_by_debt
        self.debt_type_id = debt_type_id
        self.revenue = revenue
        self.ebitda = ebitda


@dataclass
class BusinessProfile(db.Model):
    """
    Table for business profiles
     :param profile_id: unique profile id
     :param name: name of the particular profile
     :param country: country of the particular profile
     :param phone_number: phone number of the particular profile
     :param heard_about_by: how did the profile owner heard about our company
     :param user_type_id: user type of the particular profile
     :param business_type_id: business type id of the particular profile
     :param email: email address of the particular profile
     :param email_verified: if the profile's email is verified
     :param password: password of a particular profile (no encryption is used as of now)
     :param website: website of the profile
     :param business_size: business size of the profile
     :param country_code: country code of the profile
     :param office_phone_number: office phone number of the profile
     :param address_line_1: address line 1 of the profile
     :param address_line_2: address line 2 of the profile
     :param city: city of the profile
     :param post_code: postcode of the profile
     :param description: description of the profile
     :param industry_type_id: industry_type_id of the profile
     :param projects: posts, written by the user
     :param messages: comments, written by the user
     :param contacts: user's favorite posts
     :param deals: comments, written by the user
     :param transactions: user's favorite posts
    """

    # adding specification to create json object
    profile_id: int
    name: str
    country: str
    phone_number: str
    user_type_id: int
    business_type_id: int
    heard_about_by: str
    email: str
    email_verified: bool
    password: str
    website: str
    business_size: int
    country_code: str
    office_phone_number: str
    address_line_1: str
    address_line_2: str
    city: str
    post_code: str
    description: str
    industry_type_id: int
    __tablename__ = "business_profiles"

    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    country = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    user_type_id = db.Column(
        db.Integer, db.ForeignKey("user_types.user_type_id"), nullable=False
    )
    business_type_id = db.Column(
        db.Integer, db.ForeignKey("business_types.business_type_id"), nullable=False
    )
    heard_about_by = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    email_verified = db.Column(db.Boolean, nullable=False, default=0)
    password = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(), nullable=True)
    business_size = db.Column(db.String(), nullable=False)
    country_code = db.Column(db.String(), nullable=False)
    office_phone_number = db.Column(db.String(), nullable=True)
    address_line_1 = db.Column(db.String(), nullable=False)
    address_line_2 = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    post_code = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    industry_type_id = db.Column(
        db.Integer, db.ForeignKey("industry_types.industry_type_id"), nullable=False
    )
    projects = db.relationship("Project", backref="business_profiles", lazy="subquery")
    deals = db.relationship("Deal", backref="business_profiles", lazy="subquery")
    transactions = db.relationship("Transaction", backref="business_profiles", lazy="subquery")

    def __init__(
            self,
            name: str,
            country: str,
            phone_number: str,
            user_type_id: int,
            business_type_id: int,
            heard_about_by: str,
            email: str,
            email_verified: bool,
            password: str,
            website: str,
            business_size: int,
            country_code: str,
            office_phone_number: str,
            address_line_1: str,
            address_line_2: str,
            city: str,
            post_code: str,
            description: str,
            industry_type_id: int
    ):
        self.name = name
        self.country = country
        self.phone_number = phone_number
        self.user_type_id = user_type_id
        self.business_type_id = business_type_id
        self.heard_about_by = heard_about_by
        self.email = email
        self.email_verified = email_verified
        self.password = password
        self.website = website
        self.business_size = business_size
        self.country_code = country_code
        self.office_phone_number = office_phone_number
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.post_code = post_code
        self.description = description
        self.industry_type_id = industry_type_id


    @classmethod
    def lookup(cls, name: str):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def identify(cls, id: str):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.profile_id


@dataclass
class UserType(db.Model):
    """
    Table for user types
     :param user_type_id: unique user type id
     :param user_type: user type name
    """

    # adding specification to create json object
    user_type_id: int
    user_type: str

    __tablename__ = "user_types"

    user_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(), nullable=False)


@dataclass
class BusinessType(db.Model):
    """
    Table for business types
     :param business_type_id: unique business type id
     :param business_type: business type name
    """

    # adding specification to create json object
    business_type_id: int
    business_type: str

    __tablename__ = "business_types"

    business_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_type = db.Column(db.String(), nullable=False)


@dataclass
class IndustryType(db.Model):
    """
    Table for industry types
     :param industry_type_id: unique industry type id
     :param industry_type: industry type name
    """

    # adding specification to create json object
    industry_type_id: int
    industry_type: str

    __tablename__ = "business_types"

    industry_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    industry_type = db.Column(db.String(), nullable=False)


@dataclass
class Status(db.Model):
    """
    Table for statuses
     :param status_id: unique industry type id
     :param status: industry type name
    """

    # adding specification to create json object
    status_id: int
    status: str

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(), nullable=False)


@dataclass
class EquityType(db.Model):
    """
    Table for equity types
     :param equity_type_id: unique equity type id
     :param equity_type: equity type name
    """

    # adding specification to create json object
    equity_type_id: int
    equity_type: str

    __tablename__ = "equity_types"

    equity_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equity_type = db.Column(db.String(), nullable=False)


@dataclass
class DebtType(db.Model):
    """
    Table for equity types
     :param debt_type_id: unique equity type id
     :param debt_type: equity type name
    """

    # adding specification to create json object
    debt_type_id: int
    debt_type: str

    __tablename__ = "debt_types"

    debt_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    debt_type = db.Column(db.String(), nullable=False)


def insert_initial_user_types(target: Table, connection: Connection, **kw):
    user_type_1 = UserType(
        user_type_id=1,
        user_type='Free'
    )
    user_type_2 = UserType(
        user_type_id=2,
        user_type='Paid'
    )
    db.session.add(user_type_1)
    db.session.add(user_type_2)
    db.session.commit()


def insert_initial_business_types(target: Table, connection: Connection, **kw):
    business_type_1 = BusinessType(
        business_type_id=1,
        business_type='Non-Profit'
    )
    business_type_2 = BusinessType(
        business_type_id=2,
        business_type='For-Profit'
    )
    db.session.add(business_type_1)
    db.session.add(business_type_2)
    db.session.commit()


def insert_initial_industry_types(target: Table, connection: Connection, **kw):
    industry_type_1 = IndustryType(
        industry_type_id=1,
        industry_type='EdTech'
    )
    industry_type_2 = IndustryType(
        industry_type_id=2,
        industry_type='FinTech'
    )
    db.session.add(industry_type_1)
    db.session.add(industry_type_2)
    db.session.commit()


def insert_initial_statuses(target: Table, connection: Connection, **kw):
    status_1 = Status(
        status_id=1,
        status='Pending'
    )
    status_2 = Status(
        status_id=2,
        status='Completed'
    )
    status_3 = Status(
        status_id=3,
        status='Rejected'
    )
    status_4 = Status(
        status_id=4,
        status='Active'
    )
    status_5 = Status(
        status_id=2,
        status='Approved'
    )
    status_6 = Status(
        status_id=2,
        status='Non-Active'
    )
    db.session.add(status_1)
    db.session.add(status_2)
    db.session.add(status_3)
    db.session.add(status_4)
    db.session.add(status_5)
    db.session.add(status_6)
    db.session.commit()


def insert_initial_equity_types(target: Table, connection: Connection, **kw):
    equity_type_1 = EquityType(
        equity_type_id=1,
        equity_type='Development Capital'
    )
    equity_type_2 = EquityType(
        equity_type_id=2,
        equity_type='Private Equity'
    )
    equity_type_3 = EquityType(
        equity_type_id=2,
        equity_type='Venture Capital'
    )
    db.session.add(equity_type_1)
    db.session.add(equity_type_2)
    db.session.add(equity_type_3)
    db.session.commit()


def insert_initial_debt_types(target: Table, connection: Connection, **kw):
    debt_type_1 = DebtType(
        debt_type_id=1,
        debt_type='Bridge Finance'
    )
    debt_type_2 = DebtType(
        debt_type_id=2,
        debt_type='Corporate Debt'
    )
    debt_type_3 = DebtType(
        debt_type_id=2,
        debt_type='Mezzanine'
    )
    db.session.add(debt_type_1)
    db.session.add(debt_type_2)
    db.session.add(debt_type_3)
    db.session.commit()


event.listen(UserType.__table__, "after_create", insert_initial_user_types)
event.listen(BusinessType.__table__, "after_create", insert_initial_business_types)
event.listen(IndustryType.__table__, "after_create", insert_initial_industry_types)
event.listen(Status.__table__, "after_create", insert_initial_statuses)
event.listen(EquityType.__table__, "after_create", insert_initial_equity_types)
event.listen(DebtType.__table__, "after_create", insert_initial_debt_types)
