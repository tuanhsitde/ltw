from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
sqldbname = 'db/MyDataBase.db'


@app.route('/')
def index():
    return '<h1>tuanh</h1>'


# Câu 2
@app.route('/Employees', methods=['GET'])
def get_Employee():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("select * from Employee")
    employees = cur.fetchall()
    employees_list = []
    for employee in employees:
        employees_list.append({"EmployeeID": employee[0], "EmployeeName": employee[1],
                               "AccountName": employee[2],
                               "EmailAddress": employee[3], "Password": employee[4],
                               "Tel": employee[5],
                               "DepartmentID": employee[6],
                               "RoleID": employee[7]})
    return jsonify(employees_list)


@app.route("/Employee/<int:id>", methods=['DELETE'])
# Ở đây em sẽ tiến hành test xóa thử Employee có id bằng 2 trong postman
def delete_Employee(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("delete from Employee where EmployeeID = ?", (id,))
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({'message': 'Employee is deleted successfully'})
    else:
        return "Employee not found", 404


# Câu 3

@app.route("/Employee", methods=['POST'])
def add_Employee():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    EmployeeName = request.json.get('EmployeeName')
    AccountName = request.json.get('AccountName')
    EmailAddress = request.json.get('EmailAddress')
    Password = request.json.get('Password')
    Tel = request.json.get('Tel')
    DepartmentID = request.json.get('DepartmentID')
    RoleID = request.json.get('RoleID')
    if EmployeeName and EmailAddress and AccountName and Password and Tel and DepartmentID and RoleID:
        cur.execute(
            'INSERT INTO Employee (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID))
        conn.commit()
        EmployeeID = cur.lastrowid
        return jsonify({'id': EmployeeID})
    else:
        return 'EmployeeName, EmailAddress, Password, Tel, TotalEmployee are required', 400


# Ở đây em sẽ thử thay đổi thông tin của Employee có id bằng 1
@app.route("/Employee/<int:id>", methods=["PUT"])
def update_Employee(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    EmployeeName = request.json.get('EmployeeName')
    AccountName = request.json.get('AccountName')
    EmailAddress = request.json.get('EmailAddress')
    Password = request.json.get('Password')
    Tel = request.json.get('Tel')
    DepartmentID = request.json.get('DepartmentID')
    RoleID = request.json.get('RoleID')
    if EmployeeName and EmailAddress and AccountName and Password and Tel and DepartmentID and RoleID:
        cur.execute(
            'UPDATE Employee SET EmployeeName = ?, AccountName = ?, EmailAddress = ?, Password = ?, Tel = ?, DepartmentID = ?, RoleID = ? WHERE EmployeeID = ?',
            (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID, id))
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({'message': 'Employee updated successfully'})
        else:
            return 'Employee not found', 404
    else:
        return 'EmployeeName, EmailAddress, Password, Tel, TotalEmployee are required', 40


# Câu 4
# a
@app.route('/search/<email>&<password>', methods=['GET'])
def search_Employee(email, password):
    # Kết nối tới database
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    # Viết câu lệnh để lấy thông tin từ database
    sqlcommand = (
                "select * from Employee where EmailAddress like '%" + email + "%' and Password like '%" + password + "%'")
    # Thực thi câu lệnh
    cur.execute(sqlcommand)
    # Lấy thông tin của nhân viên
    employee = cur.fetchall()
    # Kiểm tra xem có bản ghi hợp lệ không
    if employee:
        # Trả lại thông báo nhân viên tồn tại
        return jsonify({'message': 'Employee exists'})
    else:
        # Trả lại thông báo không tìm thấy nhân viên
        return jsonify({'message': 'Employee does not exist'})


# b
@app.route('/search/<searchInput>')
def search(searchInput):
    # Kết nối tới database
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    # Viết câu lệnh để lấy thông tin từ database
    sqlcommand = (
                "select * from Employee where EmployeeName like '%" + searchInput + "%' or AccountName like '%" + searchInput + "%' or EmailAddress like '%" + searchInput + "%'")
    cur.execute(sqlcommand)
    employees = cur.fetchall()
    employees_list = []

    for employee in employees:
        employees_list.append({"EmployeeID": employee[0], "EmployeeName": employee[1],
                               "AccountName": employee[2],
                               "EmailAddress": employee[3], "Password": employee[4],
                               "Tel": employee[5],
                               "DepartmentID": employee[6],
                               "RoleID": employee[7]})
    return jsonify(employees_list)


# ý c
@app.route("/Orders/<int:employeeID>", methods=["GET"])
def searchID(employeeID):
    # Kết nối tới database
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    # Viết câu lệnh để lấy thông tin từ database
    cur.execute("select * from Orders where EmployeeID = ?", (employeeID,))
    # Lấy thông tin của orders
    orders = cur.fetchall()
    # Tạo danh sách order
    orders_list = []
    # Duyệt qua danh sách orders
    for order in orders:
        orders_list.append({"OrderID": order[0], "CustomerKey": order[1],
                            "ProductID": order[2],
                            "Quantity": order[3],
                            "EmployeeID": order[4], })
    # Trả lại danh sách orders
    return jsonify(orders_list)


# d
@app.route('/Employees', methods=['POST'])
def add_Employees():
    # Kết nối cơ sở dữ liệu
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    employees_data = request.json
    # Kiểm tra dữ liệu nhân viên
    if employees_data is None:
        return 'Employee data is required', 400

    # Thêm nhiều thông tin nhân viên vào cơ sở dữ liệu
    for employee in employees_data:
        EmployeeName = employee.get('EmployeeName')
        AccountName = employee.get('AccountName')
        EmailAddress = employee.get('EmailAddress')
        Password = employee.get('Password')
        Tel = employee.get('Tel')
        DepartmentID = employee.get('DepartmentID')
        RoleID = employee.get('RoleID')
        # Kiểm tra thông tin nhân viên
        if EmployeeName and EmailAddress and AccountName and Password and Tel and DepartmentID and RoleID:
            # Thêm nhân viên vào cơ sở dữ liệu
            cur.execute(
                'INSERT INTO Employee (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (EmployeeName, AccountName, EmailAddress, Password, Tel, DepartmentID, RoleID))
        else:
            # Trả lại thông báo lỗi
            return 'EmployeeName, EmailAddress, Password, Tel, TotalEmployee are required', 400
    # Lưu thay đổi
    conn.commit()
    # Trả về thông báo
    return jsonify({'message': 'Employees added'})


if __name__ == '__main__':
    app.run(debug=True)

