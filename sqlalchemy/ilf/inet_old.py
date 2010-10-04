#!/usr/bin/env python

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.orm import mapper, relationship, sessionmaker
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

employee_table = Table('e_employee', metadata,
        Column('E_ID', Integer, primary_key=True),
        Column('E_P_ID', Integer), # TODO link persons
        Column('E_Current_ED_ID',
            Integer,
            ForeignKey('ed_employeedata.ED_ID')),
        Column('E_Text', String),
        Column('E_PersNr', String(15)),
        Column('E_Login', String(50)),
        Column('E_Password', String(60)),
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

employeedata_table = Table('ed_employeedata', metadata,
        Column('ED_ID', Integer, primary_key=True),
        Column('ED_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('ED_From', DateTime),
        Column('ED_To', DateTime),
        Column('ED_TimeSheet_Company_LOC_ID',
            Integer,
            ForeignKey('loc_location.LOC_ID')),
        Column('ED_Contract_Company_LOC_ID',
            Integer,
            ForeignKey('loc_location.LOC_ID')),
        Column('ED_LOC_ID', Integer, ForeignKey('loc_location.LOC_ID')),
        Column('ED_VDEP_ID', Integer), # TODO: link fields
        Column('ED_VCC_ID', Integer),
        Column('ED_VEMT_ID', Integer),
        Column('ED_VEF_ID', Integer),
        Column('ED_VGE_ID', Integer),
        Column('ED_VEE_ID', Integer),
        Column('ED_GroupLeader_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('ED_AdditionalLeader_E_ID',
            Integer,
            ForeignKey('e_employee.E_ID')),
        Column('ED_Assistant_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('ED_ApplyDate', DateTime),
        Column('ED_EntryDate', DateTime),
        Column('ED_QuitDate', DateTime),
        Column('ED_PartTimePerc', Float),
        Column('ED_Roiom', String(20)),
        Column('ED_VSRC_Rate', String(1)),
        )

location_table = Table('loc_location', metadata,
        Column('LOC_ID', Integer, primary_key=True),
        Column('LOC_L1', Integer),
        Column('LOC_L2', Integer),
        Column('LOC_L3', Integer),
        Column('LOC_L4', Integer),
        Column('LOC_L5', Integer),
        Column('LOC_IsCompany', Integer(6), key='is_legal'),
        Column('LOC_Code', String(5), key='code'),
        Column('LOC_Inactive', Integer(6), key='inactive'),
        Column('LOC_A_ID', Integer, ForeignKey('a_address.A_ID')),
        Column('LOC_Name_en', String(100), key='name'),
        Column('LOC_Name_de', String(100), key='name_de'),
        Column('LOC_ERPS_ID', Integer),
        Column('LOC_VCAL_ID', Integer),
        Column('LOC_VSR_ID', Integer),
        Column('LOC_Comments', String, key='comment'),
        Column('LOC_Manager1_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('LOC_Manager2_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('LOC_Manager3_E_ID', Integer, ForeignKey('e_employee.E_ID')),
        Column('LOC_Resp_Project_VIA_ID', Integer), # TODO: Link VIA
        Column('LOC_Resp_ProjChange_VIA_ID', Integer),
        Column('LOC_Resp_Employee_VIA_ID', Integer),
        Column('LOC_Resp_ERP_VIA_ID', Integer),
        Column('LOC_VUG_ID', Integer),
        Column('LOC_VoIPPrefix', String(15), key='voip_prefix'),
        Column('LOC_Timestamp', DateTime, key='timestamp'),
        )

address_table = Table('a_address', metadata,
        Column('A_ID', Integer, primary_key=True),
        Column('A_VAT_ID', Integer), # TODO: link entries
        Column('A_C_ID', Integer),
        Column('A_Company_A_ID', Integer),
        Column('A_P_ID', Integer),
        Column('A_LOC_ID', Integer, ForeignKey('loc_location.LOC_ID')),
        Column('A_VC_ID', Integer),
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

class Address(object):
    def __repr__(self):
        return "<%s, %s %s>" % (self.street, self.zip_code, self.city)

class Location(object):
    def __repr__(self):
        return u"<%s>" % self.name

mapper(Address, address_table)
mapper(Location, location_table, properties={
    'address': relationship(Address,
        primaryjoin=location_table.c.LOC_A_ID==address_table.c.A_ID),
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
