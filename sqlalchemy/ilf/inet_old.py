#!/usr/bin/env python

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.orm import backref, relationship, column_property
from sqlalchemy.types import Integer, Float, String, \
        DateTime, Date, LargeBinary

from sqlalchemy import select

logindata = {'user': 'inetusr',
        'password': 'inetpw',
        'host': 'localhost',
        'port': 3306,
        'database': 'inet',
        }
connection_pattern = 'mysql+mysqlconnector://' \
    '{user}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_pattern.format(**logindata))
metadata = MetaData(engine)

employee_table = Table('E_Employee', metadata,
        Column('E_ID', Integer, primary_key=True),
        Column('E_P_ID', Integer, ForeignKey('P_Person.P_ID')),
        Column('E_Current_ED_ID',
            Integer,
            ForeignKey('ED_EmployeeData.ED_ID')),
        Column('E_Text', String),
        Column('E_PersNr', String(15), key='personal_number'),
        Column('E_Login', String(50), key='login'),
        Column('E_Password', String(60), key='password'),
        Column('E_ChangePw', Integer(6)),
        Column('E_BadPw', Integer(6)),
        Column('E_Set_Language', String(5)),
        Column('E_Set_AppWindow', Integer),
        Column('E_Set_FontSize', Integer),
        Column('E_Set_ReceiveContacts', Integer(6)),
        Column('E_LastLoginDate', Integer),
        Column('E_LastLoginHost', Integer(40)),
        Column('E_NavbarData', LargeBinary),
        Column('E_LinkData', LargeBinary),
        Column('E_Timestamp', DateTime),
        )

employeedata_table = Table('ED_EmployeeData', metadata,
        Column('ED_ID', Integer, primary_key=True),
        Column('ED_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('ED_From', DateTime, key="from_"),
        Column('ED_To', DateTime, key="to"),
        Column('ED_TimeSheet_Company_LOC_ID',
            Integer,
            ForeignKey('LOC_Location.id_')),
        Column('ED_Contract_Company_LOC_ID',
            Integer,
            ForeignKey('LOC_Location.id_')),
        Column('ED_LOC_ID', Integer, ForeignKey('LOC_Location.id_')),
        Column('ED_VDEP_ID', Integer, ForeignKey('Value_Department.VDEP_ID')),
        Column('ED_VCC_ID', Integer, ForeignKey('Value_CostCenter.VCC_ID')),
        Column('ED_VEMT_ID', Integer),
        Column('ED_VEF_ID', Integer, ForeignKey('Value_EmployeeFunc.VEF_ID')),
        Column('ED_VGE_ID', Integer),
        Column('ED_VEE_ID', Integer),
        Column('ED_GroupLeader_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('ED_AdditionalLeader_E_ID',
            Integer,
            ForeignKey('E_Employee.E_ID')),
        Column('ED_Assistant_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('ED_ApplyDate', DateTime, key='apply_date'),
        Column('ED_EntryDate', DateTime, key='entry_date'),
        Column('ED_QuitDate', DateTime, key='quit_date'),
        Column('ED_PartTimePerc', Float),
        Column('ED_Room', String(20)),
        Column('ED_VSRC_Rate', String(1)),
        )

person_table = Table('P_Person', metadata,
        Column('P_ID', Integer, primary_key=True),
        Column('P_Name', String(100), key='name'),
        Column('P_FirstNames', String(150), key='firstname'),
        Column('P_SortName', String(200)),
        Column('P_Title', String(30)),
        Column('P_Sex', Integer, key='gender'),
        Column('P_Nation_VC_ID', Integer),
        Column('P_Nation2_VC_ID', Integer),
        Column('P_VL_ID', Integer),
        Column('P_VCS_ID', Integer),
        Column('P_Birthday', Date, key='birthday'),
        Column('P_Main_A_ID', Integer),
        Column('P_ShowAdditionalAddr', Integer),
        Column('P_Christmas_ID', Integer),
        Column('P_Christmas_E_ID', Integer),
        Column('P_Timestamp', DateTime),
        )

project_table = Table('PR_Project', metadata,
        Column('PR_ID', Integer, primary_key=True),
        Column('PR_PNr', String(10), key='number'),
        Column('PR_ONr', Integer),
        Column('PR_Master_PR_ID', Integer),
        Column('PR_Internal', Integer(6), key='internal'),
        Column('PR_Confidential', Integer(6), key='confidential'),
        Column('PR_Important', Integer(6), key='importance'),
        Column('PR_AvailableERP', Integer(6), key='erp'),
        Column('PR_BillCosts', Integer(6), key='bill_costs'),
        Column('PR_VPRPT_ID', Integer),
        Column('PR_Contract_Company_LOC_ID',
            Integer,
            ForeignKey('LOC_Location.id_')),
        Column('PR_InCharge_VDEP_ID', Integer),
        Column('PR_Redundant_VPRS_ID', Integer),
        Column('PR_Descr_de', String(150), key='name_de'),
        Column('PR_Descr_en', String(150), key='name'),
        Column('PR_Text_de', String, key='text_de'),
        Column('PR_Text_en', String, key='text'),
        Column('PR_TechData_en', String, key='techdata'),
        Column('PR_TechData_de', String, key='techdata_de'),
        Column('PR_Identified', Date, key='identified'),
        Column('PR_Start', Date, key='start'),
        Column('PR_End', Date, key='end'),
        Column('PR_OfferDate', DateTime, key='offer_date'),
        Column('PR_OfferPrice_Total', Float, key='offer_price'),
        Column('PR_OfferPrice_Own', Float, key='offer_price_own'),
        Column('PR_ContractPrice_Total', Float, key='contract_price'),
        Column('PR_ContractPrice_Own', Float, key='contract_price_own'),
        Column('PR_CustomerBudget', Float, key='customer_budget'),
        Column('PR_InvestPrice_Total', Float, key='invest_price'),
        Column('PR_SuccessPercent', Integer, key='success_percent'),
        Column('PR_Memo', String, key='memo'),
        Column('PR_Timestamp', DateTime),
        )

project_customer_table = Table('PRCUST_ProjectCustomer', metadata,
        Column('PRCUST_ID', Integer, primary_key=True),
        Column('PRCUST_PR_ID', Integer, ForeignKey('PR_Project.PR_ID')),
        Column('PRCUST_Company_A_ID', Integer, ForeignKey('A_Address.A_ID')),
        Column('PRCUST_P_ID', Integer),
        Column('PRCUST_Text', String(240)),
        Column('PRCUST_Timestamp', DateTime),
        )

project_country_table = Table('PRC_ProjectCountry', metadata,
        Column('PRC_ID', Integer, primary_key=True),
        Column('PRC_PR_ID', Integer, ForeignKey('PR_Project.PR_ID')),
        Column('PRC_VC_ID', Integer, ForeignKey('Value_Country.VC_ID')),
        Column('PRC_Text', String(240)),
        Column('PRC_Timestamp', DateTime),
        )

company_table = Table('C_Company', metadata,
        Column('C_ID', Integer, primary_key=True),
        Column('C_Name', String(200), key='name'),
        Column('C_SortName', String(200)),
        Column('C_OwnCompany', Integer(6)),
        Column('C_URL', String(150), key='url'),
        Column('C_VATID', String(30)),
        Column('C_Main_A_ID', Integer, ForeignKey('A_Address.A_ID')),
        Column('C_MainFOAs', String(250)),
        Column('C_Timestamp', DateTime),
        )

location_table = Table('LOC_Location', metadata,
        Column('LOC_ID', Integer, primary_key=True, key='id_'),
        Column('LOC_L1', Integer, key='layer1'),
        Column('LOC_L2', Integer, key='layer2'),
        Column('LOC_L3', Integer, key='layer3'),
        Column('LOC_L4', Integer, key='layer4'),
        Column('LOC_L5', Integer, key='layer5'),
        Column('LOC_IsCompany', Integer(6), key='legal'),
        Column('LOC_Code', String(5), key='code'),
        Column('LOC_Inactive', Integer(6), key='inactive'),
        Column('LOC_A_ID', Integer, ForeignKey('A_Address.A_ID')),
        Column('LOC_Name_en', String(100), key='name'),
        Column('LOC_Name_de', String(100), key='name_de'),
        Column('LOC_ERPS_ID', Integer),
        Column('LOC_VCAL_ID', Integer),
        Column('LOC_VSR_ID', Integer, ForeignKey('Value_SalaryRegion.VSR_ID')),
        Column('LOC_Comments', String, key='comment'),
        Column('LOC_Manager1_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('LOC_Manager2_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('LOC_Manager3_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('LOC_Resp_Project_VIA_ID', Integer), # TODO: Link VIA
        Column('LOC_Resp_ProjChange_VIA_ID', Integer),
        Column('LOC_Resp_Employee_VIA_ID', Integer),
        Column('LOC_Resp_ERP_VIA_ID', Integer),
        Column('LOC_VUG_ID', Integer),
        Column('LOC_VoIPPrefix', String(15), key='voip_prefix'),
        Column('LOC_Timestamp', DateTime, key='timestamp'),
        )

value_department_table = Table('Value_Department', metadata,
        Column('VDEP_ID', Integer, primary_key=True),
        Column('VDEP_L1', Integer, key='layer1'),
        Column('VDEP_L2', Integer, key='layer2'),
        Column('VDEP_L3', Integer, key='layer3'),
        Column('VDEP_Manager1_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('VDEP_Manager2_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('VDEP_Manager3_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('VDEP_Code', String(15), key='code'),
        Column('VDEP_Inactive', Integer, key='inactive'),
        Column('VDEP_VCC_ID', Integer, ForeignKey('Value_CostCenter.VCC_ID')),
        Column('VDEP_Name_en', String(50), key='name'),
        Column('VDEP_Name_de', String(50), key='name_de'),
        Column('VDEP_Resp_Project_VIA_ID', Integer), # TODO: Link VIA
        Column('VDEP_Resp_ProjChange_VIA_ID', Integer),
        Column('VDEP_Resp_Employee_VIA_ID', Integer),
        Column('VDEP_Resp_ERP_VIA_ID', Integer),
        Column('VDEP_Timestamp', DateTime),
        )

address_table = Table('A_Address', metadata,
        Column('A_ID', Integer, primary_key=True),
        Column('A_VAT_ID', Integer), # TODO: link entries
        Column('A_C_ID', Integer, ForeignKey('C_Company.C_ID')),
        Column('A_Company_A_ID', Integer),
        Column('A_P_ID', Integer),
        Column('A_LOC_ID', Integer, ForeignKey('LOC_Location.id_')),
        Column('A_VC_ID', Integer, ForeignKey('Value_Country.VC_ID')),
        Column('A_Descr', String(50), key='description'),
        Column('A_Name', String(100), key='name'),
        Column('A_Name2', String(100)),
        Column('A_Department', String),
        Column('A_Street', String, key='street'),
        Column('A_ZipCode', String(20), key='zip_code'),
        Column('A_City', String(50), key='city'),
        Column('A_State', String(50), key='state'),
        Column('A_PObox', String(20)),
        Column('A_POboxZipCode', String(20)),
        Column('A_POboxCity', String(50)),
        Column('A_TelPrefix', String(30)),
        Column('A_TelExt', String(10)),
        Column('A_Tel2', String(50)),
        Column('A_FaxPrefix', String(30)),
        Column('A_FaxExt', String(10)),
        Column('A_Fax2', String(50)),
        Column('A_Mobile', String(50)),
        Column('A_EMail', String(80)),
        Column('A_VATID', String(30)),
        Column('A_LastSeen', Date),
        Column('A_Timestamp', DateTime),
        )

value_country_table = Table('Value_Country', metadata,
        Column('VC_ID', Integer, primary_key=True),
        Column('VC_TelPrefix', String(10)),
        Column('VC_NoTelCityPrefix', Integer),
        Column('VC_AddrFormat_Norm', String),
        Column('VC_AddrFormat_PO', String),
        Column('VC_Name_en', String(30), key='name'),
        Column('VC_Name_de', String(30), key='name_de'),
        Column('VC_NationalityName_en', String(40)),
        Column('VC_NationalityName_de', String(40)),
        Column('VC_Timestamp', DateTime),
        )

value_employee_function_table = Table('Value_EmployeeFunc', metadata,
        Column('VEF_ID', Integer, primary_key=True),
        Column('VEF_Name_en', String(50), key='name'),
        Column('VEF_Name_de', String(50), key='name_de'),
        Column('VEF_Timestamp', DateTime),
        )

value_costcenter_table = Table('Value_CostCenter', metadata,
        Column('VCC_ID', Integer, primary_key=True),
        Column('VCC_Code', String(15), key='code'),
        Column('VCC_Company_LOC_ID', Integer, ForeignKey('LOC_Location.id_')),
        Column('VCC_Inactive', Integer, key='inactive'),
        Column('VCC_Name', String(50), key='name'),
        )

value_salaryregion_table = Table('Value_SalaryRegion', metadata,
        Column('VSR_ID', Integer, primary_key=True),
        Column('VSR_Name_en', String(50), key='name'),
        Column('VSR_Name_de', String(50), key='name_de'),
        )

value_salaryregioncost_table = Table('Value_SalaryRegionCosts', metadata,
        Column('VSRC_ID', Integer, primary_key=True),
        Column('VSRC_VSR_ID', Integer, ForeignKey('Value_SalaryRegion.VSR_ID')),
        Column('VSRC_Year', Integer, key='year'),
        Column('VSRC_RateA_EUR', Float, key='rate_a'),
        Column('VSRC_RateB_EUR', Float, key='rate_b'),
        Column('VSRC_RateC_EUR', Float, key='rate_c'),
        Column('VSRC_RateD_EUR', Float, key='rate_d'),
        Column('VSRC_RateE_EUR', Float, key='rate_e'),
        )

value_userright_table = Table('Value_UserRight', metadata,
        Column('VUR_ID', Integer, primary_key=True, key='id'),
        Column('VUR_Name_en', Integer, key='name'),
        Column('VUR_Name_de', Integer, key='name_de'),
        Column('VUR_Timestamp', DateTime),
        )

employeerights_table = Table('ER_EmployeeRights', metadata,
        Column('ER_ID', Integer, primary_key=True),
        Column('ER_E_ID', Integer, ForeignKey('E_Employee.E_ID')),
        Column('ER_VUR_ID', Integer, ForeignKey('Value_UserRight.id'), key='right_id'),
        Column('ER_Type', Integer, key='type'),
        Column('ER_Timestamp', DateTime),
        )

class Address(object):
    def __repr__(self):
        return u"<Address: %s, %s %s>" \
                % (self.street, self.zip_code, self.city)

class Project(object):
    def __repr__(self):
        return u"<Project: %s %s>" % (self.number, self.name)

class Company(object):
    def __repr__(self):
        return u"<Company: %s>" % self.name

class Location(object):
    def get_layer(self):
        if self.layer5:
            return 5
        if self.layer4:
            return 4
        if self.layer3:
            return 3
        if self.layer2:
            return 2
        return 1

    def __repr__(self):
        return u"<Location: %s>" % self.name

class Department(object):
    def __repr__(self):
        return u"<Department: %s %s>" % (self.code, self.name)

class Country(object):
    def __repr__(self):
        return u"<Country: %s>" % self.name

class Employee(object):
    def __repr__(self):
        return u"<Employee: %s %s>" % (self.personal_number, self.login)

class EmployeeData(object):
    def __repr__(self):
        return u"<EmployeeData: %s %s to %s>" \
                % (self.employee.login, self.from_, self.to)

class Person (object):
    def __repr__(self):
        return u"<Person: %s %s>" % (self.name, self.firstname)

class EmployeeFunction(object):
    def __repr__(self):
        return u"<EmployeeFunction: %s>" % self.name

class CostCenter(object):
    def __repr__(self):
        return u"<CostCenter: %s>" % self.name

class SalaryRegion(object):
    def __repr__(self):
        return u"<SalaryRegion: %s>" % self.name

class SalaryRegionCost(object):
    def __repr__(self):
        return u"<SalaryRegionCost: region: %s year: %s>" \
                % (self.region, self.year)

class UserRight(object):
    def __repr__(self):
        return u"<UserRight: %s %s>" \
                % (self.id, self.name)

class EmployeeRight(object):
    def __repr__(self):
        return u"<EmployeeRight: employee: %s userright: %s type: %s>" \
                % (self.ER_E_ID, self.ER_VUR_ID, self.ER_Type)

mapper(Address, address_table, properties={
    'country': relationship(Country),
    })
mapper(Project, project_table, properties={
    'is_internal': column_property(project_table.c.internal==-1),
    'is_erp': column_property(project_table.c.erp==-1), # is in agresso or not
    'is_flat': column_property(project_table.c.bill_costs==0),
    'is_confidential': column_property(project_table.c.confidential==-1),
    'customers': relationship(Address,
        secondary=project_customer_table,
        backref='orders'),
    'executer': relationship(Location,
        backref='projects'),
    'countries': relationship(Country,
        secondary=project_country_table,
        backref='projects'),
    })
mapper(Company, company_table, properties={
    'address': relationship(Address,
        primaryjoin=company_table.c.C_ID==address_table.c.A_C_ID,
        backref=backref('company', uselist=False)),
    })
mapper(Location, location_table, properties={
    'address': relationship(Address,
        primaryjoin=location_table.c.LOC_A_ID==address_table.c.A_ID),
    'manager1': relationship(Employee,
        primaryjoin=location_table.c.LOC_Manager1_E_ID==employee_table.c.E_ID),
    'manager2': relationship(Employee,
        primaryjoin=location_table.c.LOC_Manager2_E_ID==employee_table.c.E_ID),
    'manager3': relationship(Employee,
        primaryjoin=location_table.c.LOC_Manager3_E_ID==employee_table.c.E_ID),
    'is_legal': column_property(location_table.c.legal==-1),
    'salary_region': relationship(SalaryRegion),
    })
mapper(Department, value_department_table, properties={
    'manager1': relationship(Employee,
        primaryjoin=value_department_table.c.VDEP_Manager1_E_ID\
                ==employee_table.c.E_ID),
    'manager2': relationship(Employee,
        primaryjoin=value_department_table.c.VDEP_Manager2_E_ID\
                ==employee_table.c.E_ID),
    'manager3': relationship(Employee,
        primaryjoin=value_department_table.c.VDEP_Manager3_E_ID\
                ==employee_table.c.E_ID),
    'is_inactive': column_property(value_department_table.c.inactive!=0),
    'cost_center': relationship(CostCenter),
    })
mapper(Country, value_country_table)
mapper(Employee, employee_table, properties={
    'data': relationship(EmployeeData,
        primaryjoin=\
                employee_table.c.E_Current_ED_ID==employeedata_table.c.ED_ID),
    'person': relationship(Person, uselist=False),
    })
mapper(Person, person_table)
mapper(EmployeeData, employeedata_table, properties={
    'employee': relationship(Employee,
        primaryjoin=employeedata_table.c.ED_E_ID==employee_table.c.E_ID),
    'organized_in': relationship(Location,
        primaryjoin=employeedata_table.c.ED_LOC_ID==location_table.c.id_),
    'contract_in': relationship(Location,
        primaryjoin=\
                employeedata_table.c.ED_Contract_Company_LOC_ID==\
                location_table.c.id_),
    'books_in': relationship(Location,
        primaryjoin=\
                employeedata_table.c.ED_TimeSheet_Company_LOC_ID==\
                location_table.c.id_),
    'function': relationship(EmployeeFunction),
    'department': relationship(Department),
    'cost_center': relationship(CostCenter),
    })
mapper(EmployeeFunction, value_employee_function_table)
mapper(CostCenter, value_costcenter_table, properties={
    'location': relationship(Location),
    })
mapper(SalaryRegion, value_salaryregion_table)
mapper(SalaryRegionCost, value_salaryregioncost_table, properties={
    'region': relationship(SalaryRegion, backref='costs'),
    })
mapper(UserRight, value_userright_table)
mapper(EmployeeRight, employeerights_table, properties={
    'employee': relationship(Employee, backref='rights'),
    'right': relationship(Employee),
    })

Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()
