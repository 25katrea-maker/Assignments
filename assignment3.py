import sqlite3
import sys

class EmployeeDatabaseCRUD:
  def __init__(self,dbName:str='employees.db'):
    self.dbName=dbName
    self.initializeDatabase()
    
  def initializeDatabase(self):
    with sqlite3.connect(self.dbName)as conn:
      cursor=conn.cursor()
      cursor.execute('''
                     CREATE TABLE IF NOT EXISTS employees(
                       id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       age INTEGER NOT NULL,
                       department TEXT NOT NULL,
                       salary REAL NOT NULL
                     )
                     ''')
      conn.commit()
      
  def createEmployee(self,emp_id:str,name:str,age:int,department:str,salary:float):
    try:
      with sqlite3.connect(self.dbName) as conn:
        cursor=conn.cursor()
        cursor.execute("""
                       INSERT INTO employees(id,name,age,department,salary)
                       VALUES(?,?,?,?,?)
                       """,(emp_id,name,age,department,salary))
        conn.commit()
      print('The employee record has been added successfully to the database!')
      return True
    
    except sqlite3.IntegrityError:
      print(f"Error:Employee with empoyess ID '{emp_id}' already exists")
      return False
    except Exception as e:
      print(f"Database error:{e}")
      return False
    
    
  def readEmployees(self):
    with sqlite3.connect(self.dbName) as conn:
      cursor=conn.cursor()
      cursor.execute("SELECT id,name,age,department,salary FROM employees")
      rows=cursor.fetchall()
      
      if not rows:
        print("The employee database is currently empty")
        return
      
      print("\n"+"="*68)
      print(f"{'ID':<10}|{'Name':<15}|{'Age':<5}|{'Department':<15}|{'Salary':<10}")
      print("-"*68)
      for row in rows:
        print(f"{row[0]:<10}|{row[1]:<15}|{row[2]:<5}|{row[3]:<15}|{row[4]:<10.2f}")
      print('='*68) 
      
def updateEmployee(self,empId:str,newAge:str,newDept:str,newSalary:str):
  with sqlite3.connect(self.db_name) as conn:
    cursor=conn.cursor()
    
    cursor.execute("SELECT name,age,dapartment,salary FROM employees WHERE id=?",(empId,))
    current=cursor.fetchone()
    
    if not current:
      print(f"Error:Employee with employee ID '{empId}' not found.")
      return False
    name=new_name if new_name else current[0]
    age=int(newAge)if newAge else current[1]
    department=newDept if newDept else current[2]
    salary=float(newSalary)if newSalary else current[3]
    
    cursor.execute("""
                   UPDATE employees
                   SET name=?,age=?,separtment=?,salary=?
                   WHERE id=?
                   """,(name,age,department,salary,empId))
    conn.commit()
    
  print(f"Employee ID '{empId}' updated successfully!")
  return True

def deleteEmployee(self,emp_id:str):
  with sqlite3.connect(self.db_name)as conn:
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM employees WHERE id=?",(emp_id,))
    if not cursor.fetchone():
      print(f"Error:Employee with empoyee id '{emp_id}' not found.")
      return False
    
    cursor.execute("DELETE FROM employees WHERE id=?",(emp_id,))
    conn.commit()
  print(f"->Employee ID '{emp_id}' deleted successfully!")
  return True

def main():
  dbManager=EmployeeDatabaseCRUD("employee1.db")
  while True:
    print('\n*****')
    print('EMPLOYEE MANAGEMENT SYSTEM ')
    print('\n*****')
    print("1.Add Employees")
    print("2.View Employees")
    print("3.Update Employees")
    print("4.Delete Employees")
    print("5.Exit")
    
    choice=input("Please enter your choice(1-5):").strip()
    if choice=='1':
      print("\n--Adding  New Employee--")
      empID=input("Enter Employee ID:").strip()
      name=input("Enter the name of the employee:").strip()
      try:
        age=int(input("Enter the age of the employee:").strip())
        salary=float(input("Enter the salary of the employee:").strip())
      except ValueError:
        print('Error:Age must be an integer and Salary must be a valid number')
        continue
      
      dept=input("Enter the department:").strip()
      dbManager.createEmployee(empID,name,age,dept,salary)
      dbManager.createEmployee(empID,name,age,dept,salary)
      
    elif choice=='2':
      dbManager.readEmployees()
      
    elif choice=='3':
      print("\n--Updating Employee Record--")
      empID=input("Enter Employee ID to be updated:").strip()
      name=input("Enter the new name:").strip()
      age=input("Enter the new age:").strip()
      dept=input("Enter the new department:").strip()
      salary=input("Enter the new salary:").strip()
      dbManager.update_employee(empID,name,age,dept,salary)
      
    elif choice=='4':
      print("\n--Delete Employee Record--")
      empID=input("Enter Employee ID to be deleted:").strip()
      dbManager.delete_employee(empID)
      
    elif choice=='5':
      print("\n Exiting program....")
      break
    else:
      print("Invalid choice!Please select an option between 1 and 5.")
      
if __name__=='__main__':
  main()