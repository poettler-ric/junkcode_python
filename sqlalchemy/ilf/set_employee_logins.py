#!/usr/bin/env python

"""
Updates a table with values taken from another joined table.
"""

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select, update
from sqlalchemy.sql.expression import func

user = "inetusr"
password = "inetpw"
host = "localhost"
port = 3306
db = "inet"

# setup engine and bound metadata
engine = create_engine("mysql+mysqlconnector://%s:%s@%s:%d/%s"
        % (user, password, host, port, db))
metadata = MetaData(engine)

# reflect the needed tables
persons = Table("P_Person", metadata, autoload=True)
employee = Table("E_Employee", metadata, autoload=True)
employee_data = Table("ED_EmployeeData", metadata, autoload=True)
location = Table("LOC_Location", metadata, autoload=True)
employee_training = Table("ET_EmployeeTraining", metadata, autoload=True)
employee_training_status = Table("Value_EmployeeTrainingStatus", metadata, autoload=True)

# prepare the query from which to select the values
query = select([func.concat(persons.c.P_Name, ", ", persons.c.P_FirstNames)],
    persons.c.P_ID==employee.c.E_P_ID).limit(1)

# create a update which takes the values from the query
update = employee.update().values(E_Login=query)

print str(update)
update.execute()
