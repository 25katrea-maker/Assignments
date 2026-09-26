import mysql.connector
from mysql.connector import Error


class EmployeeMySQLCRUD:
    def __init__(self, host='localhost', database='company_db', user='root', password=''):
        self.host = host
        
        self.database = database
        self.user = user
        self.password = password
        
        
        self.initializeDatabase()

    def getConnection(self):
        
        try:
            
            conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                
                user=self.user,
                password=self.password
            )
            
            
            return conn
        except Error as e:
            
            print(f"Database connection error occured: {e}")
            return None

    def initializeDatabase(self):
        try:
            
            serverConn = mysql.connector.connect(
                host=self.host,
                user=self.user,          
                password=self.password
            )
            
            cursor = serverConn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")  
            cursor.close()
            
            
            serverConn.close()

            conn = self.getConnection()
            if conn:
                
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    
                    CREATE TABLE IF NOT EXISTS employees(
                      id VARCHAR(50) PRIMARY KEY,
                      name VARCHAR(100) NOT NULL,
                      age INT NOT NULL,
                      department VARCHAR(100) NOT NULL,
                      salary DECIMAL(10,2) NOT NULL
                    )
                    
                    
                    '''
                )
                conn.commit()
                cursor.close()
                
                
                conn.close()
        except Error as e:
            print(f"Oops,Initialisation error occured: {e}")

    def createEmployee(self, emp_id: str, name: str, age: int, department: str, salary: float):
        conn = self.getConnection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO employees (id, name, age, department, salary)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (emp_id, name, age, department, salary))
            conn.commit()
            print("Employee record added successfully to the database")
            return True
        except mysql.connector.IntegrityError:
            print(f"Error: Employee with the  employee ID '{emp_id}' already exists in the database")
            return False
        except Error as e:
            print(f"MySQL error occured : {e}")
            
            return False
        finally:
            cursor.close()
            
            conn.close()

    def readEmployees(self):
        conn = self.getConnection()
        if not conn:
            
            return
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name, age, department, salary FROM employees")  
            rows = cursor.fetchall()

            if not rows:
                print("The database is empty at this very moment of time")
                return
            print("\n" + "=" * 68)
            print(f"{'ID':<10}|{'Name':<15}|{'Age':<5}|{'Department':<15}|{'Salary':<10}")
            print("-" * 68)
            for row in rows:
                print(f"{row[0]:<10}|{row[1]:<15}|{row[2]:<5}|{row[3]:<15}|{row[4]:<10.2f}")
            print("=" * 68)

        except Error as e:
            print(f"Error occured: {e}")
        finally:
            cursor.close()
            conn.close()

    def updateEmployee(self, empId: str, newName: str, newAge: str, new_dept: str, newSalary: str):
        conn = self.getConnection()
        
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT name, age, department, salary FROM employees WHERE id=%s", (empId,))
            current = cursor.fetchone()

            if not current:
                print(f"Error: Employee with employee ID '{empId}' not found in our database")
                return False
            name = newName if newName else current[0]
            age = int(newAge) if newAge else current[1]
            department = new_dept if new_dept else current[2]   
            salary = float(newSalary) if newSalary else current[3]

            query = """
                UPDATE employees
                SET name=%s, age=%s, department=%s, salary=%s
                WHERE id=%s
            """
            cursor.execute(query, (name, age, department, salary, empId))
            conn.commit()
            print(f"The employee ID '{empId}' updated successfully!")
            return True
        
        except Error as e:
            
            print(f"Error occured: {e}")
            return False
        finally:
            
            
            cursor.close()
            conn.close()

    def delete_employee(self, emp_id: str):
        
        conn = self.getConnection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM employees WHERE id = %s", (emp_id,))
            if not cursor.fetchone():
                print(f"Error: employee with employee ID '{emp_id}' is not found")
                return False

            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
            
            conn.commit()
            print(f"Employee ID '{emp_id}' deleted successfully!")
            return True
        except Error as e:
            print(f"MySQL error occured: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


def main():
    print("--- MySQL Setup ---")
    db_host = input("Enter host: ").strip() or "localhost"
    db_user = input("Enter username (default: root): ").strip() or "root"
    db_pass = input("Enter password: ").strip()

    db_manager = EmployeeMySQLCRUD(host=db_host, user=db_user, password=db_pass)

    while True:
        print("\n****")
        print("  EMPLOYEE CRUD MANAGEMENT SYSTEM     ")
        print("\n*****")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Please enter your choice (1-5): ").strip()

        if choice == '1':
            print("\n--- Adding New Employee ---")
            emp_id = input("Enter the employee ID: ").strip()
            name = input("Enter the name: ").strip()
            try:
                age = int(input("Enter the age: ").strip())
                salary = float(input("Enter the salary: ").strip())
            except ValueError:
                print("Error: Age must be an integer and Salary must be a valid number.")
                continue
            dept = input("Please enter the department: ").strip()
            db_manager.createEmployee(emp_id, name, age, dept, salary)

        elif choice == '2':
            db_manager.readEmployees()   

        elif choice == '3':
            print("\n--- Updating Employee Record ---")
            emp_id = input("Enter Employee ID to be updated: ").strip()

            name = input("Enter new Name: ").strip()
            age = input("Enter new Age: ").strip()
            dept = input("Enter new Department: ").strip()
            salary = input("Enter new Salary: ").strip()
            db_manager.updateEmployee(emp_id, name, age, dept, salary)   

        elif choice == '4':
            print("\n--- Deleting Employee Record ---")
            emp_id = input("Enter Employee ID to be deleted: ").strip()
            db_manager.delete_employee(emp_id)

        elif choice == '5':
            print("\nExiting program....")
            break
        else:
            print("Invalid choice! Please select an option between 1 and 5.")


if __name__ == "__main__":
    main()
