from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, Date, Time, Double, Boolean, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

# Database configuration: Reads the DATABASE_URL environment variable.
# If not set, it defaults to a MySQL connection string using pymysql.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://user:password@mysql:3306/mydatabase"
)

# Create the database engine which manages the DB connection pool.
engine = create_engine(DATABASE_URL)

# Configure a session factory for handling database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative model definitions.
Base = declarative_base()


# ----------- Company Models -----------

# Represents a company entity.
class Company(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    nit = Column(Integer)
    address = Column(String(100))
    email = Column(String(50))
    type_industry = Column(String(30))
    url_logo = Column(String(100))

    users = relationship("UserCompany", back_populates="company")
    departments = relationship("Department", back_populates="company")


# Represents user credentials linked to a company.
class UserCompany(Base):
    __tablename__ = 'user_company'

    user_company_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.company_id'))
    username = Column(String(50))
    password = Column(String(50))

    company = relationship("Company", back_populates="users")


# ----------- Location Models -----------

# Represents a continent.
class Continent(Base):
    __tablename__ = 'continent'

    continent_id = Column(Integer, primary_key=True)
    name = Column(String(100))

    countries = relationship("Country", back_populates="continent")


# Represents a country, which belongs to a continent.
class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    continent_id = Column(Integer, ForeignKey('continent.continent_id'))

    continent = relationship("Continent", back_populates="countries")
    states = relationship("State", back_populates="country")


# Represents a state or province, part of a country.
class State(Base):
    __tablename__ = 'state'

    state_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    country_id = Column(Integer, ForeignKey('country.country_id'))

    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")


# Represents a city, part of a state.
class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    state_id = Column(Integer, ForeignKey('state.state_id'))

    state = relationship("State", back_populates="cities")


# Represents a department within a company.
class Department(Base):
    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    company_id = Column(Integer, ForeignKey('company.company_id'))

    company = relationship("Company", back_populates="departments")


# ----------- Employee Models -----------

# Represents a job role.
class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(50))

    employees = relationship("Employee", back_populates="role")


# Represents an employee in the company.
class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone_number = Column(Integer)
    hire_date = Column(Date)
    role_id = Column(Integer, ForeignKey('role.role_id'))
    manager_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=True)
    department_id = Column(Integer, ForeignKey('department.department_id'))
    url_foto = Column(String(100))
    status = Column(Boolean)

    role = relationship("Role", back_populates="employees")
    manager = relationship("Employee", remote_side=[employee_id])
    evaluations = relationship("Evaluation", back_populates="employee")
    schedules = relationship("Schedule", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")
    work_absences = relationship("WorkAbsence", back_populates="employee")
    history = relationship("History", back_populates="employee", uselist=False)


# Represents an evaluation record for an employee.
class Evaluation(Base):
    __tablename__ = 'evaluation'

    evaluation_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    evaluation_date = Column(Date)
    punctuality = Column(Integer)
    performance = Column(Integer)
    courtesy = Column(Integer)
    precision = Column(Integer)
    collaboration = Column(Integer)
    proactivity = Column(Integer)

    employee = relationship("Employee", back_populates="evaluations")


# Represents the employment history of an employee (resignation, dismissal, etc.).
class History(Base):
    __tablename__ = 'history'

    history_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    date_of_dismissal = Column(Date)
    reason = Column(String(100))

    employee = relationship("Employee", back_populates="history")


# ----------- Payroll Models -----------

# Represents an employee's work schedule.
class Schedule(Base):
    __tablename__ = 'schedule'

    schedule_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    start_time = Column(Time)
    end_time = Column(Time)
    break_start = Column(Time)
    break_end = Column(Time)

    employee = relationship("Employee", back_populates="schedules")


# Represents payroll information for an employee.
class Payroll(Base):
    __tablename__ = 'payroll'

    payroll_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    payment_date = Column(Date)
    base_salary = Column(Double)
    bonuses = Column(Double)
    total_payment = Column(Double)
    payment_method_id = Column(Integer, ForeignKey('payment_method.payment_method_id'))

    employee = relationship("Employee", back_populates="payrolls")
    payment_method = relationship("PaymentMethod", back_populates="payrolls")


# Represents different methods of payment (e.g., cash, bank transfer, etc.).
class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    payment_method_id = Column(Integer, primary_key=True)
    name = Column(String(50))

    payrolls = relationship("Payroll", back_populates="payment_method")


# ----------- Absence Models -----------

# Represents types of absences (vacation, sick leave, personal leave, etc.).
class AbsenceType(Base):
    __tablename__ = 'absence_type'

    absence_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(50))

    absences = relationship("WorkAbsence", back_populates="absence_type")


# Represents an absence event for an employee.
class WorkAbsence(Base):
    __tablename__ = 'work_absences'

    absence_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    absence_type_id = Column(Integer, ForeignKey('absence_type.absence_type_id'))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String(100))

    employee = relationship("Employee", back_populates="work_absences")
    absence_type = relationship("AbsenceType", back_populates="absences")


# Create all tables defined in the Base metadata if they don't exist.
Base.metadata.create_all(bind=engine)