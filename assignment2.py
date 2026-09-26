import csv
import os
from typing import Dict,List

class EmployeeCRUD:
  def __init__(self,filename:str="employees.csv"):
    self.filename=filename
    self.fieldnames=["id","name","age","department","salary"]
    self.initializeFile()
    
  def initializeFile(self):
    if not os.path.exists(self.filename):
      with open(self.filename,mode='w',newline='')as file:
        writer=csv.DictWriter(file,fieldnames=self.fieldnames)
        writer.writeheader()
        
  def findEmployeeRow(self,emp_id:str)->bool:
    with open(self.filename,mode='r',newline='') as file:
      reader=csv.DictReader(file)
      for row in reader:
        if row['id']==emp_id:
          return True
    return False
  
  def createEmployee(self,empId:str,name:str,age:str,department:str,salary:str):
    if self.findEmployeeRow(empId):
      print(f"Error:Employee with ID '{empId}' already exists")
      return False
    
    with open(self.filename,mode='a',newline='') as file:
      writer=csv.DictWriter(file,fieldnames=self.fieldnames)
      writer.writerow({
        "id":empId,
        "name":name,
        "age":age,
        "department":department,
        "salary":salary
      })
    print("Employee record added successfully!")
    return True
   
  def readEmployees(self):
    if not os.path.exists(self.filename):
      print("No employee records found")
      return
    
    with open(self.filename,mode='r',newline='') as file:
      reader=csv.DictReader(file)
      rows=list(reader)
      
      if not rows:
        print("The employee table is currently empty")
        return
      
      print("\n"+"="*65)
      for row in rows:
        print(f"{'ID':<10}|{'Name':<15}|{'Age':<5}|{'Department':<15}|{'Salary':<10}")
      print("-"*65)
      
  def updateEmployee(self,empId:str,newName:str,newAge:str,newDept:str,newSalary:str):
    if not self.findEmployeeRow(empId):
      print(f"Error:Employee with ID '{empId}' not found")
      return False
    rows=[]
    with open(self.filename,mode='r',newline='') as file:
      reader=csv.DictReader(file)
      rows=list(reader)
      
    for row in rows:
      if row['id']==empId:
        row['name']=newName if newName else row['name']
        row['age']=newAge if newAge else row['name']
        row['department']=newDept if newDept else row['department']
        row['salary']=newSalary if newSalary else row['salary']
        
    with open(self.filename,mode='w',newline='') as file:
      writer=csv.DictWriter(file,fieldnames=self.fieldnames)
      writer.writeheader()
      writer.writerows(rows)
    
    print(f"->Employee ID '{empId}' updated successfully!")      
    return True
  
  def deleteEmployee(self,empId:str):
    if not self.findEmployeeRow(empId):
      print(f"Error:Employee with ID '{empId}' not found")
      return False
    
    rows=[]
    with open(self.filename,mode='r',newline='') as file:
      reader=csv.DictReader(file)
      rows=list(reader)
      
    updatedRow=[row for row in rows if row['id']!=empId]
    
    with open(self.filename,mode='w',newline='')as file:
      writer=csv.DictWriter(file,fieldnames=self.fieldnames)
      writer.writeheader()
      writer.writerows(updatedRow)
      
      print(f"Employee ID '{empId}' deleted successfully!")
      return True
  
def main():
  manager=EmployeeCRUD("employees.csv")
  while True:
    print('\n*****\n')
    print(' EMPLOYEE MANAGEMENT SYSTEM ')
    print('\n*****\n')
    print('1.Add Employee')
    print('2.View Employees')
    print('3.Update Employee')
    print('4.Delete Employee')
    print('5.Exit')
    
    choice=input('Enter your choice(1-5):').strip()
    
    if choice=='1':
      print('\n--Adding New Employee--')
      emp_id=input('Enter Employee ID: ').strip()
      name=input('Enter name:').strip()
      age=input('Enter Age:').strip()
      dept=input('Enter Department:').strip()
      salary=input('Enter Salary:').strip()
      manager.createEmployee(emp_id,name,age,dept,salary)
      
    elif choice=='2':
      manager.readEmployees()
      
    elif choice=='3':
      print('\n--Update Employee Record--')
      emp_id=input('Please enter Employee ID to update:').strip()
      name=input('Enter new name:').strip()
      age=input('Enter new Age:').strip()
      dept=input('Enter new Department:').strip()
      salary=input('Enter new Salary:').strip()
      manager.updateEmployee(emp_id,name,age,dept,salary)
      
    elif choice=='4':
      print('\n-- Delete Employee Record --')
      emp_id=input('Enter Employee ID to be deleted: ').strip()
      manager.delete_employee(emp_id)
      
    elif choice=='5':
      print('\nExiting program....')
      break
    
    else:
      print('Invalid choice.Please select an option between 1 and 5.')
      
if __name__=='__main__':
  main()
  