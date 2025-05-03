import mysql.connector
from mysql.connector import Error, errorcode # Import errorcode để kiểm tra lỗi cụ thể
import datetime
from tabulate import tabulate # Thư viện để in bảng đẹp hơn

# --- Cấu hình kết nối Database ---
# !!! THAY THẾ BẰNG THÔNG TIN CỦA BẠN !!!
DB_CONFIG = {
    'host': '127.0.0.1',       # Hoặc địa chỉ IP/hostname của server MySQL
    'user': 'root',   # Tên người dùng MySQL (Đã hoàn nguyên)
    'password': 'doantunglam333', # Mật khẩu MySQL của bạn
    'database': 'classicmodels'  # Tên database (Đã hoàn nguyên)
}

# --- Hàm tạo kết nối ---
def create_connection():
    """Tạo kết nối đến MySQL Database"""
    connection = None
    try:
        # Sử dụng cấu hình DB_CONFIG đã cập nhật
        connection = mysql.connector.connect(**DB_CONFIG)
        # Không cần in ra khi thành công, chỉ báo lỗi nếu thất bại
    except Error as e:
        print(f"Lỗi khi kết nối đến MySQL: {e}")
        # Hiển thị chi tiết hơn nếu lỗi xác thực hoặc database không tồn tại
        if hasattr(e, 'errno'): # Kiểm tra xem có thuộc tính errno không
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(">>> Gợi ý: Sai tên người dùng hoặc mật khẩu trong DB_CONFIG.")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print(f">>> Gợi ý: Database '{DB_CONFIG['database']}' không tồn tại trên server MySQL.")
        print(">>> Gợi ý: Đảm bảo MySQL server đang chạy và cấu hình DB_CONFIG là chính xác.")
    return connection

# --- Hàm thực thi câu lệnh Query (SELECT) ---
def execute_read_query(query, params=None):
    """Thực thi câu lệnh SELECT và trả về kết quả"""
    connection = create_connection()
    # Quan trọng: Kiểm tra kết nối trước khi tạo cursor
    if not connection or not connection.is_connected():
        # create_connection đã in lỗi rồi
        return None # Trả về None nếu không kết nối được
    cursor = None # Khởi tạo cursor là None
    result = None
    try:
        cursor = connection.cursor(dictionary=True) # dictionary=True để trả về dạng dict
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Lỗi khi thực thi query: {e}")
        # In ra câu lệnh và tham số nếu có lỗi để dễ debug
        print(f"Query: {query}")
        if params:
            print(f"Params: {params}")
        # Kiểm tra lỗi cụ thể, ví dụ bảng không tồn tại
        if hasattr(e, 'errno'):
            if e.errno == errorcode.ER_NO_SUCH_TABLE:
                 print(f">>> Gợi ý: Bảng được tham chiếu trong query không tồn tại trong database '{DB_CONFIG['database']}'. Kiểm tra lại tên bảng trong query.")
            elif e.errno == errorcode.ER_BAD_FIELD_ERROR:
                 print(f">>> Gợi ý: Cột được tham chiếu trong query không tồn tại trong bảng tương ứng. Kiểm tra lại tên cột trong query.")
            elif e.errno == errorcode.ER_PARSE_ERROR:
                 print(f">>> Gợi ý: Lỗi cú pháp SQL. Kiểm tra lại câu lệnh query.")

    finally:
        # Đảm bảo cursor và connection được đóng ngay cả khi có lỗi
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return result

# --- Hàm thực thi câu lệnh Modify (INSERT, UPDATE, DELETE) ---
def execute_modify_query(query, params=None, return_last_id=False):
    """
    Thực thi câu lệnh INSERT, UPDATE, DELETE.
    Trả về True nếu thành công, False nếu thất bại.
    Nếu return_last_id=True và là lệnh INSERT, trả về ID của bản ghi mới nhất (hoặc True nếu không có lastrowid).
    """
    connection = create_connection()
    # Quan trọng: Kiểm tra kết nối trước khi tạo cursor
    if not connection or not connection.is_connected():
         # create_connection đã in lỗi rồi
         return False # Trả về False nếu không kết nối được

    cursor = None # Khởi tạo cursor là None
    result = False
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit() # Commit thay đổi

        if return_last_id:
            # Trả về ID nếu có, nếu không (VD: UPDATE/DELETE) thì trả về True vì commit thành công
            result = cursor.lastrowid if cursor.lastrowid else True
        else:
             result = True # Mặc định trả về True nếu thành công
        print("Thao tác thành công.")
    except Error as e:
        print(f"Lỗi khi thực thi query: {e}")
        # In ra câu lệnh và tham số nếu có lỗi để dễ debug
        print(f"Query: {query}")
        if params:
            print(f"Params: {params}")
        # Kiểm tra lỗi cụ thể
        if hasattr(e, 'errno'):
            if e.errno == errorcode.ER_NO_SUCH_TABLE:
                 print(f">>> Gợi ý: Bảng được tham chiếu trong query không tồn tại trong database '{DB_CONFIG['database']}'.")
            elif e.errno == errorcode.ER_BAD_FIELD_ERROR:
                 print(f">>> Gợi ý: Cột được tham chiếu trong query không tồn tại trong bảng tương ứng.")
            elif e.errno == errorcode.ER_DUP_ENTRY:
                 print(f">>> Gợi ý: Dữ liệu bị trùng lặp (ví dụ: khóa chính hoặc khóa duy nhất đã tồn tại).")
            elif e.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                 print(f">>> Gợi ý: Không thể thêm/cập nhật dòng con: khóa ngoại không hợp lệ (dữ liệu tham chiếu không tồn tại).")
            elif e.errno == errorcode.ER_PARSE_ERROR:
                 print(f">>> Gợi ý: Lỗi cú pháp SQL. Kiểm tra lại câu lệnh query.")
            elif e.errno == errorcode.ER_DATA_TOO_LONG:
                 print(f">>> Gợi ý: Dữ liệu nhập vào quá dài cho một cột nào đó.")

        connection.rollback() # Rollback nếu có lỗi
        result = False # Đảm bảo trả về False khi có lỗi
    finally:
        # Đảm bảo cursor và connection được đóng ngay cả khi có lỗi
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return result

# === QUẢN LÝ KHÁCH HÀNG ===

def view_customers():
    """Hiển thị danh sách khách hàng"""
    query = "SELECT customerNumber, customerName, phone, city, country FROM customers ORDER BY customerNumber LIMIT 20"
    customers = execute_read_query(query)
    if customers:
        print("\n--- Danh sách khách hàng ---")
        headers = customers[0].keys() if customers else ["Mã KH", "Tên KH", "Điện thoại", "Thành phố", "Quốc gia"]
        print(tabulate(customers, headers="keys", tablefmt="grid"))
    elif customers is None:
        print("Lỗi khi truy vấn danh sách khách hàng.")
    else:
        print("Không tìm thấy khách hàng nào.")

def find_customer_by_name(name_keyword):
    """Tìm kiếm khách hàng theo tên"""
    query = "SELECT customerNumber, customerName, phone, city, country FROM customers WHERE customerName LIKE %s"
    params = (f"%{name_keyword}%",)
    customers = execute_read_query(query, params)
    if customers:
        print(f"\n--- Kết quả tìm kiếm khách hàng cho '{name_keyword}' ---")
        headers = customers[0].keys() if customers else ["Mã KH", "Tên KH", "Điện thoại", "Thành phố", "Quốc gia"]
        print(tabulate(customers, headers="keys", tablefmt="grid"))
    elif customers is None:
         print(f"Lỗi khi tìm kiếm khách hàng '{name_keyword}'.")
    else:
        print(f"Không tìm thấy khách hàng nào có tên chứa '{name_keyword}'.")

def add_customer():
    """Thêm một khách hàng mới"""
    print("\n--- Thêm khách hàng mới ---")
    try:
        # Sử dụng logic tạo ID cho classicmodels
        max_id_result = execute_read_query("SELECT MAX(customerNumber) as max_id FROM customers")
        if max_id_result is None:
             print("Lỗi: Không thể lấy mã khách hàng hiện tại.")
             return
        if max_id_result and max_id_result[0]['max_id'] is not None:
             customer_number = max_id_result[0]['max_id'] + 1
        else:
             customer_number = 103 # Giá trị mặc định nếu bảng trống

        # Các tên cột khớp với classicmodels
        customer_name = input("Tên khách hàng*: ")
        contact_last_name = input("Họ người liên hệ*: ")
        contact_first_name = input("Tên người liên hệ*: ")
        phone = input("Số điện thoại*: ")
        address1 = input("Địa chỉ dòng 1*: ")
        address2 = input("Địa chỉ dòng 2 (bỏ trống nếu không có): ")
        city = input("Thành phố*: ")
        state = input("Bang/Tỉnh (bỏ trống nếu không có): ")
        postal_code = input("Mã bưu chính (bỏ trống nếu không có): ")
        country = input("Quốc gia*: ")
        sales_rep_num_str = input("Mã nhân viên bán hàng (số, bỏ trống nếu không có): ")
        credit_limit_str = input("Hạn mức tín dụng (số, bỏ trống nếu không có): ")

        if not all([customer_name, contact_last_name, contact_first_name, phone, address1, city, country]):
            print("Lỗi: Vui lòng nhập đầy đủ thông tin bắt buộc (*).")
            return

        sales_rep_num = int(sales_rep_num_str) if sales_rep_num_str.isdigit() else None
        credit_limit = float(credit_limit_str) if credit_limit_str.replace('.', '', 1).isdigit() else None
        address2 = address2 if address2 else None
        state = state if state else None
        postal_code = postal_code if postal_code else None

        # Kiểm tra xem salesRepEmployeeNumber có tồn tại trong bảng employees không
        if sales_rep_num:
             emp_check = execute_read_query("SELECT employeeNumber FROM employees WHERE employeeNumber = %s", (sales_rep_num,))
             if not emp_check:
                  print(f"Cảnh báo: Mã nhân viên bán hàng {sales_rep_num} không tồn tại. Khách hàng sẽ được thêm mà không có NVBH.")
                  sales_rep_num = None # Đặt lại thành None nếu không hợp lệ

        # Query và params khớp với classicmodels
        query = """
            INSERT INTO customers (customerNumber, customerName, contactLastName, contactFirstName, phone,
                                   addressLine1, addressLine2, city, state, postalCode, country,
                                   salesRepEmployeeNumber, creditLimit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (customer_number, customer_name, contact_last_name, contact_first_name, phone,
                  address1, address2, city, state, postal_code, country,
                  sales_rep_num, credit_limit)

        success = execute_modify_query(query, params)
        if success:
            print(f"Đã thêm khách hàng mới thành công với Mã KH: {customer_number}")

    except ValueError:
        print("Lỗi: Dữ liệu nhập vào không hợp lệ (ví dụ: mã NV hoặc hạn mức tín dụng phải là số).")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi thêm khách hàng: {e}")


# === QUẢN LÝ ĐƠN HÀNG ===

def view_orders(limit=20):
    """Hiển thị danh sách đơn hàng gần đây"""
    # Query khớp classicmodels
    query = """
        SELECT o.orderNumber, o.orderDate, c.customerName, o.status
        FROM orders o
        JOIN customers c ON o.customerNumber = c.customerNumber
        ORDER BY o.orderDate DESC, o.orderNumber DESC
        LIMIT %s
    """
    params = (limit,)
    orders = execute_read_query(query, params)
    if orders:
        print("\n--- Danh sách đơn hàng ---")
        orders_display = [
            {k: (v.strftime('%Y-%m-%d') if isinstance(v, datetime.date) else v) for k, v in row.items()}
            for row in orders
        ]
        print(tabulate(orders_display, headers="keys", tablefmt="grid"))
    elif orders is None:
         print("Lỗi khi truy vấn danh sách đơn hàng.")
    else:
        print("Không tìm thấy đơn hàng nào.")

def view_order_details(order_number):
    """Hiển thị chi tiết một đơn hàng"""
    # Query khớp classicmodels
    query_order = """
        SELECT o.orderNumber, o.orderDate, o.requiredDate, o.shippedDate, o.status, o.comments,
               c.customerName, c.phone, c.addressLine1, c.city, c.country
        FROM orders o
        JOIN customers c ON o.customerNumber = c.customerNumber
        WHERE o.orderNumber = %s
    """
    order_info = execute_read_query(query_order, (order_number,))

    # Query khớp classicmodels
    query_details = """
        SELECT p.productName, od.quantityOrdered, od.priceEach, (od.quantityOrdered * od.priceEach) AS subtotal
        FROM orderdetails od
        JOIN products p ON od.productCode = p.productCode
        WHERE od.orderNumber = %s
        ORDER BY od.orderLineNumber
    """
    order_details = execute_read_query(query_details, (order_number,))

    if order_info:
        info = order_info[0]
        print(f"\n--- Chi tiết đơn hàng #{order_number} ---")
        print(f"Khách hàng: {info.get('customerName', 'N/A')} ({info.get('phone', 'N/A')})")
        print(f"Địa chỉ: {info.get('addressLine1', '')}, {info.get('city', '')}, {info.get('country', '')}")
        order_date_str = info['orderDate'].strftime('%Y-%m-%d') if info.get('orderDate') else 'N/A'
        required_date_str = info['requiredDate'].strftime('%Y-%m-%d') if info.get('requiredDate') else 'N/A'
        shipped_date_str = info['shippedDate'].strftime('%Y-%m-%d') if info.get('shippedDate') else 'Chưa giao'
        print(f"Ngày đặt: {order_date_str}")
        print(f"Ngày yêu cầu: {required_date_str}")
        print(f"Ngày giao: {shipped_date_str}")
        print(f"Trạng thái: {info.get('status', 'N/A')}")
        print(f"Ghi chú: {info.get('comments', 'Không có')}")

        if order_details:
            print("\n--- Sản phẩm ---")
            headers = ["Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"]
            details_display = [
                 {
                     "Tên sản phẩm": item.get('productName', 'N/A'),
                     "Số lượng": item.get('quantityOrdered', 0),
                     "Đơn giá": f"{item.get('priceEach', 0):,.2f}",
                     "Thành tiền": f"{item.get('subtotal', 0):,.2f}"
                 } for item in order_details
            ]
            print(tabulate(details_display, headers="keys", tablefmt="grid", floatfmt=".2f"))
            total_amount = sum(item.get('subtotal', 0) for item in order_details)
            print(f"\nTổng cộng: {total_amount:,.2f}")
        elif order_details is None:
             print("Lỗi khi truy vấn chi tiết sản phẩm.")
        else:
            print("Đơn hàng này không có chi tiết sản phẩm.")
    elif order_info is None:
         print(f"Lỗi khi truy vấn thông tin đơn hàng {order_number}.")
    else:
        print(f"Không tìm thấy đơn hàng với mã {order_number}.")


def add_order():
    """Thêm một đơn hàng mới"""
    print("\n--- Thêm đơn hàng mới ---")
    try:
        # Logic tạo ID cho classicmodels
        max_id_result = execute_read_query("SELECT MAX(orderNumber) as max_id FROM orders")
        if max_id_result is None:
             print("Lỗi: Không thể lấy mã đơn hàng hiện tại.")
             return
        if max_id_result and max_id_result[0]['max_id'] is not None:
             order_number = max_id_result[0]['max_id'] + 1
        else:
             order_number = 10100 # Giá trị mặc định nếu bảng trống

        cust_num_str = input("Nhập Mã Khách Hàng*: ")
        if not cust_num_str.isdigit():
            print("Lỗi: Mã khách hàng phải là số.")
            return
        customer_number = int(cust_num_str)

        # Query kiểm tra khách hàng khớp classicmodels
        cust_check = execute_read_query("SELECT customerNumber FROM customers WHERE customerNumber = %s", (customer_number,))
        if cust_check is None:
             print("Lỗi khi kiểm tra khách hàng.")
             return
        if not cust_check:
            print(f"Lỗi: Không tìm thấy khách hàng với mã {customer_number}.")
            return

        order_date_str = input("Ngày đặt hàng (YYYY-MM-DD, bỏ trống để lấy ngày hiện tại): ")
        required_date_str = input("Ngày yêu cầu giao hàng (YYYY-MM-DD)*: ")
        comments = input("Ghi chú (bỏ trống nếu không có): ")
        status = "In Process"

        order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date() if order_date_str else datetime.date.today()
        required_date = datetime.datetime.strptime(required_date_str, '%Y-%m-%d').date() if required_date_str else None

        if not required_date:
             print("Lỗi: Ngày yêu cầu giao hàng là bắt buộc.")
             return

        # Query INSERT orders khớp classicmodels
        order_query = """
            INSERT INTO orders (orderNumber, orderDate, requiredDate, status, comments, customerNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        order_params = (order_number, order_date, required_date, status, comments if comments else None, customer_number)
        order_success = execute_modify_query(order_query, order_params)

        if not order_success:
            return

        print(f"Đã tạo đơn hàng #{order_number}. Vui lòng thêm chi tiết sản phẩm.")

        line_number = 1
        while True:
            print(f"\n--- Thêm sản phẩm thứ {line_number} cho đơn hàng #{order_number} ---")
            product_code = input("Nhập Mã Sản phẩm* (nhập 'xong' để kết thúc): ")
            if product_code.lower() == 'xong':
                if line_number == 1:
                    print("Lỗi: Đơn hàng phải có ít nhất một sản phẩm.")
                    print(f"Đang xóa đơn hàng rỗng #{order_number}...")
                    execute_modify_query("DELETE FROM orders WHERE orderNumber = %s", (order_number,))
                    print("Đã hủy thêm đơn hàng.")
                    return
                else:
                    break

            # Query kiểm tra sản phẩm và cột giá khớp classicmodels
            prod_check = execute_read_query("SELECT productCode, buyPrice FROM products WHERE productCode = %s", (product_code,))
            if prod_check is None:
                 print("Lỗi khi kiểm tra sản phẩm.")
                 continue
            if not prod_check:
                print(f"Lỗi: Không tìm thấy sản phẩm với mã '{product_code}'.")
                continue

            quantity_str = input("Nhập số lượng*: ")
            # Cột đơn giá (priceEach) khớp classicmodels
            price_each_str = input(f"Nhập đơn giá (mặc định: {prod_check[0]['buyPrice']}, bỏ trống để dùng mặc định): ")

            if not quantity_str.isdigit() or int(quantity_str) <= 0:
                print("Lỗi: Số lượng phải là một số nguyên dương.")
                continue

            quantity = int(quantity_str)
            price_each = float(price_each_str) if price_each_str.replace('.', '', 1).isdigit() else prod_check[0]['buyPrice']

            # Query INSERT orderdetails khớp classicmodels
            detail_query = """
                INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
                VALUES (%s, %s, %s, %s, %s)
            """
            detail_params = (order_number, product_code, quantity, price_each, line_number)
            detail_success = execute_modify_query(detail_query, detail_params)

            if detail_success:
                print(f"Đã thêm sản phẩm '{product_code}' vào đơn hàng.")
                line_number += 1

        print(f"\nĐã thêm thành công đơn hàng #{order_number} với {line_number-1} sản phẩm.")

    except ValueError as ve:
        print(f"Lỗi định dạng dữ liệu: {ve}. Ví dụ: Ngày phải là YYYY-MM-DD, số lượng/giá phải là số.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi thêm đơn hàng: {e}")


def update_order_status(order_number, new_status):
    """Cập nhật trạng thái đơn hàng"""
    valid_statuses = ['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
    if new_status not in valid_statuses:
        print(f"Trạng thái '{new_status}' không hợp lệ. Các trạng thái hợp lệ: {', '.join(valid_statuses)}")
        return False

    # Query kiểm tra đơn hàng khớp classicmodels
    order_check = execute_read_query("SELECT status FROM orders WHERE orderNumber = %s", (order_number,))
    if order_check is None:
        print(f"Lỗi khi kiểm tra đơn hàng {order_number}.")
        return False
    if not order_check:
         print(f"Lỗi: Không tìm thấy đơn hàng {order_number}.")
         return False

    current_status = order_check[0]['status']
    if current_status == new_status:
         print(f"Đơn hàng {order_number} đã ở trạng thái '{new_status}'.")
         return True

    # Query UPDATE orders khớp classicmodels
    if new_status == 'Shipped':
        query = "UPDATE orders SET status = %s, shippedDate = COALESCE(shippedDate, CURDATE()) WHERE orderNumber = %s"
        params = (new_status, order_number)
    elif new_status in ['Cancelled', 'On Hold']:
         query = "UPDATE orders SET status = %s, shippedDate = NULL WHERE orderNumber = %s"
         params = (new_status, order_number)
    else:
        query = "UPDATE orders SET status = %s WHERE orderNumber = %s"
        params = (new_status, order_number)

    print(f"Đang cập nhật trạng thái đơn hàng {order_number} từ '{current_status}' thành '{new_status}'...")
    return execute_modify_query(query, params)

# === QUẢN LÝ GIAO HÀNG ===
# Lưu ý: Các hàm giao hàng (assign_delivery, create_invoice, báo cáo chi phí)
# dựa trên các bảng deliveries, vehicles, expenses có thể không tồn tại
# hoặc có cấu trúc khác trong 'classicmodels' gốc.
# Cần điều chỉnh các hàm này nếu bạn muốn chúng hoạt động với 'classicmodels'.
# Hiện tại, các hàm này được giữ lại nhưng có thể gây lỗi nếu bảng không tồn tại.

def assign_delivery(order_number):
    """Gán giao hàng cho một đơn hàng (Logic đơn giản: chọn xe ngẫu nhiên)"""
    # !!! Bảng deliveries, vehicles có thể không tồn tại trong classicmodels !!!
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'vehicles' tồn tại và có cấu trúc phù hợp. ***")
    # 1. Kiểm tra đơn hàng
    order_query = "SELECT status FROM orders WHERE orderNumber = %s"
    order_result = execute_read_query(order_query, (order_number,))
    if order_result is None:
         print(f"Lỗi khi kiểm tra đơn hàng {order_number}.")
         return
    if not order_result:
        print(f"Lỗi: Không tìm thấy đơn hàng {order_number}.")
        return
    current_status = order_result[0]['status']

    if current_status == 'Shipped':
        print(f"Lỗi: Đơn hàng {order_number} đã được giao.")
        return
    if current_status == 'Cancelled':
         print(f"Lỗi: Đơn hàng {order_number} đã bị hủy.")
         return

    # 2. Kiểm tra giao hàng cũ (Bảng deliveries?)
    delivery_check_query = "SELECT deliveryID FROM deliveries WHERE orderID = %s" # Giả định bảng deliveries tồn tại
    existing_delivery = execute_read_query(delivery_check_query, (order_number,))
    if existing_delivery is None:
         print(f"Cảnh báo/Lỗi: Không thể kiểm tra lịch sử giao hàng (bảng 'deliveries' có thể không tồn tại hoặc lỗi query).")
         # return # Thoát nếu cần kiểm tra chặt chẽ
    elif existing_delivery:
        print(f"Thông báo: Đơn hàng {order_number} đã được gán giao hàng trước đó (ID: {existing_delivery[0]['deliveryID']}).")
        overwrite = input("Đơn hàng đã được gán. Bạn có muốn gán lại xe khác không? (c/k): ").lower()
        if overwrite == 'c':
             print("Đang xóa gán cũ...")
             delete_success = execute_modify_query("DELETE FROM deliveries WHERE orderID = %s", (order_number,))
             if not delete_success:
                  print("Lỗi khi xóa gán giao hàng cũ.")
                  return
        else:
             return

    # 3. Chọn xe (Bảng vehicles?)
    vehicle_query = "SELECT vehicleID FROM vehicles ORDER BY RAND() LIMIT 1" # Giả định bảng vehicles tồn tại
    vehicle_result = execute_read_query(vehicle_query)
    if vehicle_result is None:
        print("Cảnh báo/Lỗi: Không thể truy vấn danh sách xe (bảng 'vehicles' có thể không tồn tại hoặc lỗi query).")
        print("Không thể tự động gán xe.")
        return
    if not vehicle_result:
        print("Lỗi: Không tìm thấy xe nào trong hệ thống (bảng 'vehicles' có thể trống).")
        return
    selected_vehicle_id = vehicle_result[0]['vehicleID']

    # 4. Tạo bản ghi giao hàng (Bảng deliveries?)
    insert_query = """
        INSERT INTO deliveries (orderID, vehicleID, deliveryDate)
        VALUES (%s, %s, CURDATE())
    """ # Giả định bảng deliveries tồn tại
    params = (order_number, selected_vehicle_id)
    print(f"Đang gán xe {selected_vehicle_id} cho đơn hàng {order_number}...")
    success = execute_modify_query(insert_query, params)

    # 5. Cập nhật trạng thái 'Shipped'
    if success:
        print("Gán giao hàng thành công. Đang cập nhật trạng thái đơn hàng thành 'Shipped'.")
        update_order_status(order_number, 'Shipped')

# === TẠO HÓA ĐƠN GIAO HÀNG ===
def create_invoice(order_number):
    """Tạo và hiển thị hóa đơn giao hàng đơn giản"""
    generate_delivery_invoice(order_number)

def generate_delivery_invoice(order_number):
    """Tạo và hiển thị hóa đơn giao hàng đơn giản"""
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'vehicles' tồn tại và có cấu trúc phù hợp. ***")
    # !!! Query này dựa trên các bảng có thể không tồn tại trong classicmodels (deliveries, vehicles) !!!
    query_order = """
        SELECT o.orderNumber, o.orderDate, o.requiredDate, o.shippedDate, o.status,
               c.customerName, c.phone, c.addressLine1, c.addressLine2, c.city, c.state, c.postalCode, c.country,
               d.deliveryID, d.deliveryDate, v.licensePlate, v.vehicleType
        FROM orders o
        JOIN customers c ON o.customerNumber = c.customerNumber
        LEFT JOIN deliveries d ON o.orderNumber = d.orderID  -- Bảng deliveries?
        LEFT JOIN vehicles v ON d.vehicleID = v.vehicleID    -- Bảng vehicles?
        WHERE o.orderNumber = %s
    """
    order_info_list = execute_read_query(query_order, (order_number,))

    # Query chi tiết đơn hàng vẫn dùng bảng của classicmodels
    query_details = """
        SELECT p.productName, od.quantityOrdered, od.priceEach, (od.quantityOrdered * od.priceEach) AS subtotal
        FROM orderdetails od
        JOIN products p ON od.productCode = p.productCode
        WHERE od.orderNumber = %s
        ORDER BY od.orderLineNumber
    """
    order_details = execute_read_query(query_details, (order_number,))

    if order_info_list is None:
         print(f"Lỗi khi truy vấn thông tin hóa đơn cho đơn hàng {order_number}.")
         print("(Có thể do bảng 'deliveries' hoặc 'vehicles' không tồn tại)")
         return
    if not order_info_list:
        print(f"Không thể tạo hóa đơn: Không tìm thấy đơn hàng {order_number} hoặc thiếu thông tin giao hàng.")
        basic_order_info = execute_read_query("SELECT * FROM orders WHERE orderNumber = %s", (order_number,))
        if not basic_order_info:
             print(f"(Đơn hàng {order_number} không tồn tại)")
        else:
             print("(Có thể do bảng 'deliveries' hoặc 'vehicles' không tồn tại hoặc chưa có dữ liệu)")
        return

    info = order_info_list[0]

    # Kiểm tra trạng thái 'Shipped'
    if info.get('status') != 'Shipped':
         print(f"Không thể tạo hóa đơn: Đơn hàng {order_number} chưa ở trạng thái 'Shipped'.")
         return

    print("\n" + "="*60)
    print(f"{'HÓA ĐƠN GIAO HÀNG':^60}")
    print("="*60)
    order_date_str = info['orderDate'].strftime('%Y-%m-%d') if info.get('orderDate') else 'N/A'
    delivery_date_str = info.get('deliveryDate')
    if isinstance(delivery_date_str, datetime.date):
         delivery_date_str = delivery_date_str.strftime('%Y-%m-%d')
    else:
         delivery_date_str = info.get('shippedDate', 'N/A')
         if isinstance(delivery_date_str, datetime.date):
              delivery_date_str = delivery_date_str.strftime('%Y-%m-%d')

    print(f"Số đơn hàng: {info.get('orderNumber', 'N/A'):<20} Ngày đặt: {order_date_str}")
    print(f"Mã giao hàng: {info.get('deliveryID', 'N/A'):<18} Ngày giao: {delivery_date_str}")
    print(f"Xe giao hàng: {info.get('licensePlate', 'N/A')} ({info.get('vehicleType', 'N/A')})")
    print("-"*60)
    print("Thông tin khách hàng:")
    print(f"  Tên: {info.get('customerName', 'N/A')}")
    print(f"  Điện thoại: {info.get('phone', 'N/A')}")
    print(f"  Địa chỉ: {info.get('addressLine1', '')}")
    if info.get('addressLine2'):
        print(f"           {info.get('addressLine2', '')}")
    print(f"           {info.get('city', '')}, {info.get('state', '')} {info.get('postalCode', '')}")
    print(f"           {info.get('country', '')}")
    print("-"*60)
    print("Chi tiết đơn hàng:")

    if order_details:
        headers = ["Sản phẩm", "SL", "Đơn giá", "Thành tiền"]
        details_display = [
            (item.get('productName', 'N/A'), item.get('quantityOrdered', 0), f"{item.get('priceEach', 0):,.2f}", f"{item.get('subtotal', 0):,.2f}")
            for item in order_details
        ]
        print(tabulate(details_display, headers=headers, tablefmt="plain"))
        total_amount = sum(item.get('subtotal', 0) for item in order_details)
        print("-"*60)
        print(f"{'Tổng cộng:':>48} {total_amount:,.2f}")
    elif order_details is None:
         print("  (Lỗi khi truy vấn chi tiết sản phẩm)")
    else:
        print("  (Không có chi tiết sản phẩm)")

    print("="*60)
    print(f"{'Cảm ơn quý khách!':^60}")
    print("="*60 + "\n")


# === BÁO CÁO ===

def report_delivery_performance():
    """Báo cáo hiệu suất giao hàng cơ bản (ví dụ: tỷ lệ giao đúng hạn)"""
    # Query khớp classicmodels
    query = """
        SELECT
            COUNT(*) AS totalOrders,
            SUM(CASE WHEN status = 'Shipped' THEN 1 ELSE 0 END) AS shippedOrders,
            SUM(CASE WHEN status = 'Shipped' AND shippedDate <= requiredDate THEN 1 ELSE 0 END) AS onTimeOrders,
            SUM(CASE WHEN status = 'Shipped' AND shippedDate > requiredDate THEN 1 ELSE 0 END) AS lateOrders,
            AVG(CASE WHEN status = 'Shipped' THEN DATEDIFF(shippedDate, orderDate) ELSE NULL END) AS avgShippingDays
        FROM orders
    """
    report_data = execute_read_query(query)
    if report_data and report_data[0] is not None:
        data = report_data[0]
        print("\n--- Báo cáo hiệu suất giao hàng ---")
        total = data.get('totalOrders', 0)
        shipped = data.get('shippedOrders', 0)
        on_time = data.get('onTimeOrders', 0) if data.get('onTimeOrders') is not None else 0
        late = data.get('lateOrders', 0) if data.get('lateOrders') is not None else 0
        avg_days = data.get('avgShippingDays')

        print(f"Tổng số đơn hàng: {total}")
        print(f"Số đơn đã giao: {shipped}")
        if shipped > 0:
            on_time_percent = (on_time / shipped * 100) if shipped > 0 else 0
            late_percent = (late / shipped * 100) if shipped > 0 else 0
            print(f"Số đơn giao đúng hạn (shippedDate <= requiredDate): {on_time} ({on_time_percent:.2f}%)")
            print(f"Số đơn giao trễ (shippedDate > requiredDate): {late} ({late_percent:.2f}%)")
            if avg_days is not None:
                 # Chuyển Decimal thành float trước khi định dạng
                 print(f"Thời gian giao hàng trung bình (ngày): {float(avg_days):.2f}")
            else:
                 print("Thời gian giao hàng trung bình: Chưa có dữ liệu")
        else:
             print("Chưa có đơn hàng nào được giao để thống kê chi tiết.")
    elif report_data is None:
         print("Lỗi khi tạo báo cáo hiệu suất giao hàng.")
    else:
        print("Không có dữ liệu để tạo báo cáo hiệu suất giao hàng.")


def report_order_history(customer_number):
    """Báo cáo lịch sử đơn hàng của một khách hàng"""
    # Query lấy tên khách hàng khớp classicmodels
    cust_name_query = "SELECT customerName FROM customers WHERE customerNumber = %s"
    cust_name_result = execute_read_query(cust_name_query, (customer_number,))
    if cust_name_result is None:
         print(f"Lỗi khi truy vấn tên khách hàng {customer_number}.")
         return
    if not cust_name_result:
        print(f"Lỗi: Không tìm thấy khách hàng với mã {customer_number}.")
        return
    customer_name = cust_name_result[0]['customerName']

    # Query lấy lịch sử đơn hàng khớp classicmodels
    query = """
        SELECT o.orderNumber, o.orderDate, o.status, SUM(od.quantityOrdered * od.priceEach) as totalAmount
        FROM orders o
        LEFT JOIN orderdetails od ON o.orderNumber = od.orderNumber
        WHERE o.customerNumber = %s
        GROUP BY o.orderNumber, o.orderDate, o.status
        ORDER BY o.orderDate DESC
    """
    history = execute_read_query(query, (customer_number,))

    if history:
        print(f"\n--- Lịch sử đơn hàng của {customer_name} (Mã KH: {customer_number}) ---")
        headers = ["Mã ĐH", "Ngày đặt", "Trạng thái", "Tổng tiền"]
        history_display = [
            (item['orderNumber'],
             item['orderDate'].strftime('%Y-%m-%d') if item.get('orderDate') else 'N/A',
             item.get('status', 'N/A'),
             f"{item.get('totalAmount', 0):,.2f}" if item.get('totalAmount') is not None else "0.00")
            for item in history
        ]
        print(tabulate(history_display, headers=headers, tablefmt="grid"))
    elif history is None:
         print(f"Lỗi khi truy vấn lịch sử đơn hàng cho khách hàng {customer_number}.")
    else:
        print(f"Khách hàng {customer_name} (Mã KH: {customer_number}) không có lịch sử đơn hàng.")


def report_delivery_cost_summary():
    """Báo cáo tổng hợp chi phí giao hàng theo từng đơn hàng"""
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'expenses' tồn tại và có cấu trúc phù hợp. ***")
    # !!! Query này dựa trên bảng deliveries và expenses có thể không tồn tại trong classicmodels !!!
    query = """
        SELECT d.orderID, SUM(e.amount) AS totalCost
        FROM deliveries d
        JOIN expenses e ON d.deliveryID = e.deliveryID
        GROUP BY d.orderID
        ORDER BY d.orderID
    """
    costs = execute_read_query(query)
    if costs:
        print("\n--- Tổng hợp chi phí giao hàng theo đơn hàng ---")
        headers = ["Mã Đơn Hàng", "Tổng chi phí giao hàng"]
        costs_display = [(item['orderID'], f"{item.get('totalCost', 0):,.2f}") for item in costs]
        print(tabulate(costs_display, headers=headers, tablefmt="grid"))
    elif costs is None:
         print("Lỗi khi tạo báo cáo chi phí giao hàng (bảng 'deliveries' hoặc 'expenses' có thể không tồn tại).")
    else:
        print("Không có dữ liệu chi phí giao hàng để báo cáo.")

def report_grand_total_delivery_cost():
     """Báo cáo tổng chi phí giao hàng của tất cả các đơn"""
     print("\n*** Chức năng này yêu cầu bảng 'expenses' tồn tại và có cấu trúc phù hợp. ***")
     # !!! Query này dựa trên bảng expenses có thể không tồn tại trong classicmodels !!!
     query = "SELECT SUM(amount) AS grandTotal FROM expenses"
     result = execute_read_query(query)
     if result is None:
          print("Lỗi khi tính tổng chi phí giao hàng (bảng 'expenses' có thể không tồn tại).")
     elif result and result[0].get('grandTotal') is not None:
          grand_total = result[0]['grandTotal']
          print(f"\n--- Tổng chi phí giao hàng toàn bộ ---")
          # Chuyển Decimal thành float
          print(f"Tổng cộng: {float(grand_total):,.2f}")
     else:
          print("Không có dữ liệu chi phí giao hàng hoặc không thể tính tổng.")


# === GIAO DIỆN CONSOLE ===

def main_menu():
    """Hiển thị menu chính"""
    return display_menu()

def display_menu():
    """Hiển thị menu chính"""
    print("\n" + "="*30)
    # Đã bỏ "(LAB4.2)"
    print("   QUẢN LÝ GIAO HÀNG")
    print("="*30)
    print("1. Quản lý Khách hàng")
    print("2. Quản lý Đơn hàng")
    print("3. Quản lý Giao hàng (Cần bảng deliveries/vehicles)") # Ghi chú
    print("4. Báo cáo")
    print("0. Thoát")
    print("-"*30)
    return input("Chọn chức năng: ")

def customer_menu():
    """Menu quản lý khách hàng"""
    while True:
        print("\n--- Quản lý Khách hàng ---")
        print("1. Xem danh sách khách hàng")
        print("2. Tìm khách hàng theo tên")
        print("3. Thêm khách hàng mới")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ")
        if choice == '1':
            view_customers()
        elif choice == '2':
            keyword = input("Nhập tên khách hàng cần tìm: ")
            find_customer_by_name(keyword)
        elif choice == '3':
            add_customer()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def order_menu():
    """Menu quản lý đơn hàng"""
    while True:
        print("\n--- Quản lý Đơn hàng ---")
        print("1. Xem danh sách đơn hàng gần đây")
        print("2. Xem chi tiết đơn hàng")
        print("3. Thêm đơn hàng mới")
        print("4. Cập nhật trạng thái đơn hàng")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ")
        if choice == '1':
            view_orders()
        elif choice == '2':
            try:
                order_num = int(input("Nhập mã đơn hàng cần xem: "))
                view_order_details(order_num)
            except ValueError:
                print("Mã đơn hàng phải là số.")
        elif choice == '3':
             add_order()
        elif choice == '4':
             try:
                order_num = int(input("Nhập mã đơn hàng cần cập nhật: "))
                valid_statuses = ['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
                print(f"Các trạng thái hợp lệ: {', '.join(valid_statuses)}")
                new_status = input("Nhập trạng thái mới: ")
                update_order_status(order_num, new_status)
             except ValueError:
                print("Mã đơn hàng phải là số.")
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def delivery_menu():
     """Menu quản lý giao hàng"""
     print("\n*** Lưu ý: Chức năng giao hàng yêu cầu các bảng 'deliveries', 'vehicles', 'expenses' tồn tại và có cấu trúc phù hợp. ***")
     while True:
        print("\n--- Quản lý Giao hàng ---")
        print("1. Gán giao hàng & cập nhật trạng thái 'Shipped'")
        print("2. Tạo hóa đơn giao hàng (cho đơn đã Shipped)")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ")
        if choice == '1':
            try:
                order_num = int(input("Nhập mã đơn hàng cần gán giao hàng: "))
                assign_delivery(order_num)
            except ValueError:
                print("Mã đơn hàng phải là số.")
        elif choice == '2':
             try:
                order_num = int(input("Nhập mã đơn hàng cần tạo hóa đơn: "))
                create_invoice(order_num)
             except ValueError:
                print("Mã đơn hàng phải là số.")
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def report_menu():
    """Menu báo cáo"""
    while True:
        print("\n--- Báo cáo ---")
        print("1. Hiệu suất giao hàng")
        print("2. Lịch sử đơn hàng của khách hàng")
        print("3. Chi phí giao hàng theo đơn hàng (Cần bảng deliveries/expenses)") # Ghi chú
        print("4. Tổng chi phí giao hàng toàn bộ (Cần bảng expenses)") # Ghi chú
        print("0. Quay lại menu chính")
        choice = input("Chọn: ")
        if choice == '1':
            report_delivery_performance()
        elif choice == '2':
            try:
                cust_num = int(input("Nhập mã khách hàng: "))
                report_order_history(cust_num)
            except ValueError:
                print("Mã khách hàng phải là số.")
        elif choice == '3':
            report_delivery_cost_summary()
        elif choice == '4':
             report_grand_total_delivery_cost()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")


# --- Hàm main chạy ứng dụng ---
if __name__ == "__main__":
    # Kiểm tra kết nối ban đầu
    print("Đang kiểm tra kết nối database...")
    conn_test = create_connection()
    if not conn_test or not conn_test.is_connected():
        print("="*40)
        print(" LỖI KẾT NỐI DATABASE BAN ĐẦU ".center(40, "="))
        print("="*40)
        # create_connection đã in chi tiết lỗi và gợi ý
        exit() # Thoát nếu không kết nối được
    else:
         print("Kết nối database thành công.")
         conn_test.close() # Đóng kết nối thử nghiệm

    # Vòng lặp menu chính
    while True:
        main_choice = main_menu()
        if main_choice == '1':
            customer_menu()
        elif main_choice == '2':
            order_menu()
        elif main_choice == '3':
            delivery_menu()
        elif main_choice == '4':
            report_menu()
        elif main_choice == '0':
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
