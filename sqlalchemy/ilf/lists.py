#!/usr/bin/env python

from inet_old import get_session
from inet_old import Location
from inet_old import Employee, EmployeeData, EmployeeFunction
from inet_old import Project
from inet_old import Department
from inet_old import SalaryRegionCost
from inet_old import CostCenter

# imports for higher efficiency of the sql selects
from inet_old import location_table
from inet_old import project_table
from inet_old import project_country_table
from inet_old import value_country_table
from inet_old import Country
from sqlalchemy import select

import csv


class UTF8Writer:
    def __init__(self, fileobj, **kwds):
        self.writer = csv.writer(fileobj, dialect=csv.excel, **kwds)

    def writerow(self, row):
        self.writer.writerow([cell.encode('utf-8') for cell in row])
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def list_locations():
    output_file = r'c:\temp\locations.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    "id",
                    "name",
                    "street",
                    "zip",
                    "city",
                    "country",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                address = location.address
                country = address.country if address else None
                rowdata = (
                        location.id_,
                        location.name,
                        address.street if address is not None else None,
                        address.zip_code if address is not None else None,
                        address.city if address is not None else None,
                        country.name if country is not None else None,
                        )
                csv_writer.writerow([unicode(cell if cell is not None else "")
                    for cell in rowdata])

def list_companys():
    output_file = r'c:\temp\companies.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    "id",
                    "name",
                    "layer",
                    "layer1",
                    "layer2",
                    "layer3",
                    "layer4",
                    "layer5",
                    "groupid",
                    "groupname",
                    "legal",
                    "manager1",
                    "manager2",
                    "manager3",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                group_query = session.query(Location)
                group_query = group_query.filter(
                        Location.layer1==location.layer1)
                group_query = group_query.filter(
                        Location.layer2==location.layer2)
                group_query = group_query.filter(Location.layer3==0)
                group_query = group_query.filter(Location.layer4==0)
                group_query = group_query.filter(Location.layer5==0)
                group_query = group_query.filter(Location.id_!=location.id_)
                group = group_query.first()

                manager1 = location.manager1
                manager2 = location.manager2
                manager3 = location.manager3

                if manager1 is None:
                    manager_query = session.query(Employee)
                    manager_query = manager_query.join((EmployeeData,
                        Employee.E_Current_ED_ID==\
                                EmployeeData.ED_ID))
                    manager_query = manager_query.filter(
                            EmployeeData.quit_date == None)
                    manager_query = manager_query.filter(
                            EmployeeData.organized_in==location)
                    manager_query = manager_query.join(EmployeeFunction)
                    manager_query = manager_query.filter(
                            EmployeeFunction.name.like('managing director'))
                    managers = manager_query.all()
                    assert len(managers) <= 3, \
                            "we at the moment we can only handle 3 managers"
                    manager1 = managers[0] if len(managers) > 0 else None
                    manager2 = managers[1] if len(managers) > 1 else None
                    manager3 = managers[2] if len(managers) > 2 else None

                rowdata = (
                        location.id_,
                        location.name,
                        location.get_layer(),
                        location.layer1,
                        location.layer2,
                        location.layer3,
                        location.layer4,
                        location.layer5,
                        group.id_ if group is not None else "",
                        group.name if group is not None else "",
                        'y' if location.is_legal else "n",
                        manager1.login if manager1 is not None else None,
                        manager2.login if manager2 is not None else None,
                        manager3.login if manager3 is not None else None,
                        )
                csv_writer.writerow([unicode(cell if cell is not None else "")
                    for cell in rowdata])

def list_customers():
    output_file = r'c:\temp\customers.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    "location_id",
                    "location",
                    "project",
                    "project_name",
                    "customer_id",
                    "customer",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                for project in location.projects:
                    for customer in project.customers:
                        rowdata = (
                                location.id_,
                                location.name,
                                project.number,
                                project.name,
                                customer.company.C_ID,
                                customer.company.name,
                                )
                        csv_writer.writerow([unicode(cell \
                                if cell is not None else "") \
                                for cell in rowdata])

def list_project_country_locations():
    output_file = r'c:\temp\countries.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    "location_id",
                    "location",
                    "country_id",
                    "country",
                    )
            csv_writer.writerow(header)

            join = location_table.join(project_table)
            join = join.join(project_country_table)
            join = join.join(value_country_table)
            select_from = select([location_table, value_country_table],
                    from_obj=join)\
                            .group_by(location_table.c.id_,
                                    value_country_table.c.VC_ID)
            query = session.query(Location, Country).from_statement(select_from)

            for location, country in query.all():
                rowdata = (
                        location.id_,
                        location.name,
                        country.VC_ID,
                        country.name,
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

def list_departments():
    output_file = r'c:\temp\departments.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    "id"
                    "layer1",
                    "layer2",
                    "layer3",
                    "code",
                    "name",
                    "cost_center_id",
                    "cost_center",
                    "manager1_id",
                    "manager1",
                    "manager2_id",
                    "manager2",
                    "manager3_id",
                    "manager3",
                    )
            csv_writer.writerow(header)

            query = session.query(Department)
            for department in query.all():
                manager1 = department.manager1
                manager2 = department.manager2
                manager3 = department.manager3
                cost_center = department.cost_center
                rowdata = (
                        department.VDEP_ID,
                        department.layer1,
                        department.layer2,
                        department.layer3,
                        department.code,
                        department.name,
                        cost_center.VCC_ID if cost_center is not None else "",
                        cost_center.name if cost_center is not None else "",
                        manager1.E_ID if manager1 is not None else "",
                        manager1.login if manager1 is not None else "",
                        manager2.E_ID if manager2 is not None else "",
                        manager2.login if manager2 is not None else "",
                        manager3.E_ID if manager3 is not None else "",
                        manager3.login if manager3 is not None else "",
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

def list_employees():
    output_file = r'c:\temp\employee.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    "id",
                    "name",
                    "first_name",
                    "department_id",
                    "department_name",
                    )
            csv_writer.writerow(header)

            query = session.query(Employee)
            query = query.join((EmployeeData,
                Employee.E_Current_ED_ID==EmployeeData.ED_ID))
            query = query.filter(EmployeeData.quit_date==None)
            for employee in query.all():
                person = employee.person
                data = employee.data
                department = data.department if data is not None else None
                rowdata = (
                        employee.E_ID,
                        person.name,
                        person.firstname,
                        department.VDEP_ID if department is not None else None,
                        department.name if department is not None else None,
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

def list_salarys():
    output_file = r'c:\temp\salarys.csv'
    with get_session() as session:
        """query = session.query(SalaryRegionCost)
        for regioncost in query.all():
            print regioncost"""
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header = (
                    'region_id',
                    'region',
                    'year',
                    'rate_a',
                    'rate_b',
                    'rate_c',
                    'rate_d',
                    'rate_e',
                    )
            csv_writer.writerow(header)

            query = session.query(SalaryRegionCost)
            for regioncost in query.all():
                region = regioncost.region
                rowdata = (
                        region.VSR_ID if region is not None else "",
                        region.name if region is not None else "",
                        regioncost.year,
                        regioncost.rate_a,
                        regioncost.rate_b,
                        regioncost.rate_c,
                        regioncost.rate_d,
                        regioncost.rate_e,
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

def list_salary_locations():
    output_file = r'c:\temp\salary_locations.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    "id",
                    "name",
                    "region_id",
                    "region",
                    "year",
                    "rate_a",
                    "rate_b",
                    "rate_c",
                    "rate_d",
                    "rate_e",
                    )
            csv_writer.writerow(header)

            locations = session.query(Location).all()
            for location in locations:
                region = location.salary_region
                costs = region.costs if region is not None else None
                if costs is not None:
                    for cost in costs:
                        rowdata = (
                                location.id_,
                                location.name,
                                region.VSR_ID if region is not None else None,
                                region.name if region is not None else None,
                                cost.year if cost is not None else None,
                                cost.rate_a if costs is not None else None,
                                cost.rate_b if costs is not None else None,
                                cost.rate_c if costs is not None else None,
                                cost.rate_d if costs is not None else None,
                                cost.rate_e if costs is not None else None,
                                )
                        csv_writer.writerow([unicode(cell \
                                if cell is not None else "") \
                                for cell in rowdata])

def list_cost_centers():
    output_file = r'c:\temp\cost_centers.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    'id',
                    'code',
                    'name',
                    'location_id',
                    )
            csv_writer.writerow(header)

            query = session.query(CostCenter)
            for cost_center in query.all():
                rowdata = (
                        cost_center.VCC_ID,
                        cost_center.code,
                        cost_center.name,
                        cost_center.VCC_Company_LOC_ID,
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

def list_projects():
    output_file = r'c:\temp\projects.csv'
    with get_session() as session:
        with open(output_file, "wb") as file_obj:
            csv_writer = UTF8Writer(file_obj, quoting=csv.QUOTE_MINIMAL)
            header=(
                    "project_id",
                    "project_number",
                    "project_name",
                    )
            csv_writer.writerow(header)

            query = session.query(Project)
            for project in query.all():
                rowdata = (
                        project.PR_ID,
                        project.number,
                        project.name,
                        )
                csv_writer.writerow([unicode(cell \
                        if cell is not None else "") \
                        for cell in rowdata])

if __name__ == '__main__':
    list_locations()
    list_companys()
    list_customers()
    list_project_country_locations()
    list_departments()
    list_employees()
    list_salarys()
    list_salary_locations()
    list_cost_centers()
    list_projects()
