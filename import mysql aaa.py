import mysql.connector
from mysql.connector import Error, errorcode
import datetime
from tabulate import tabulate

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'doantunglam333',
    'database': 'classicmodels'
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Lỗi khi kết nối đến MySQL: {e}")
        if hasattr(e, 'errno'):
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(">>> Gợi ý: Sai tên người dùng hoặc mật khẩu trong DB_CONFIG.")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print(f">>> Gợi ý: Database '{DB_CONFIG['database']}' không tồn tại trên server MySQL.")
        print(">>> Gợi ý: Đảm bảo MySQL server đang chạy và cấu hình DB_CONFIG là chính xác.")
    return connection

def execute_read_query(query, params=None):
    connection = create_connection()
    if not connection or not connection.is_connected():
        return None
    cursor = None
    result = None
    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Lỗi khi thực thi query: {e}")
        print(f"Query: {query}")
        if params:
            print(f"Params: {params}")
        if hasattr(e, 'errno'):
            if e.errno == errorcode.ER_NO_SUCH_TABLE:
                 print(f">>> Gợi ý: Bảng được tham chiếu trong query không tồn tại trong database '{DB_CONFIG['database']}'. Kiểm tra lại tên bảng trong query.")
            elif e.errno == errorcode.ER_BAD_FIELD_ERROR:
                 print(f">>> Gợi ý: Cột được tham chiếu trong query không tồn tại trong bảng tương ứng. Kiểm tra lại tên cột trong query.")
            elif e.errno == errorcode.ER_PARSE_ERROR:
                 print(f">>> Gợi ý: Lỗi cú pháp SQL. Kiểm tra lại câu lệnh query.")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return result

def execute_modify_query(query, params=None, return_last_id=False):
    connection = create_connection()
    if not connection or not connection.is_connected():
         return False
    cursor = None
    result = False
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()

        if return_last_id:
            result = cursor.lastrowid if cursor.lastrowid else True
        else:
             result = True
        print("Thao tác thành công.")
    except Error as e:
        print(f"Lỗi khi thực thi query: {e}")
        print(f"Query: {query}")
        if params:
            print(f"Params: {params}")
        if hasattr(e, 'errno'):
            if e.errno == errorcode.ER_NO_SUCH_TABLE:
                 print(f">>> Gợi ý: Bảng được tham chiếu trong query không tồn tại trong database '{DB_CONFIG['database']}'.")
            elif e.errno == errorcode.ER_BAD_FIELD_ERROR:
                 print(f">>> Gợi ý: Cột được tham chiếu trong query không tồn tại trong bảng tương ứng.")
            elif e.errno == errorcode.ER_DUP_ENTRY:
                 print(f">>> Gợi ý: Dữ liệu bị trùng lặp (ví dụ: khóa chính hoặc khóa duy nhất đã tồn tại).")
            elif e.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                 print(f">>> Gợi ý: Không thể thêm/cập nhật dòng con: khóa ngoại không hợp lệ (dữ liệu tham chiếu không tồn tại).")
                 print(f">>> Kiểm tra xem giá trị bạn đang cố chèn/cập nhật cho cột khóa ngoại (ví dụ: customerNumber, productCode, orderID, vehicleID, deliveryID) có tồn tại trong bảng gốc tương ứng không.")
            elif e.errno == errorcode.ER_PARSE_ERROR:
                 print(f">>> Gợi ý: Lỗi cú pháp SQL. Kiểm tra lại câu lệnh query.")
            elif e.errno == errorcode.ER_DATA_TOO_LONG:
                 print(f">>> Gợi ý: Dữ liệu nhập vào quá dài cho một cột nào đó.")
        connection.rollback()
        result = False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    return result

def view_customers():
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
    print("\n--- Thêm khách hàng mới ---")
    try:
        max_id_result = execute_read_query("SELECT MAX(customerNumber) as max_id FROM customers")
        if max_id_result is None:
             print("Lỗi: Không thể lấy mã khách hàng hiện tại.")
             return
        if max_id_result and max_id_result[0]['max_id'] is not None:
             customer_number = max_id_result[0]['max_id'] + 1
        else:
             customer_number = 1 # Hoặc một giá trị khởi tạo phù hợp khác

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

        if sales_rep_num:
             emp_check = execute_read_query("SELECT employeeNumber FROM employees WHERE employeeNumber = %s", (sales_rep_num,))
             if not emp_check:
                  print(f"Cảnh báo: Mã nhân viên bán hàng {sales_rep_num} không tồn tại. Khách hàng sẽ được thêm mà không có NVBH.")
                  sales_rep_num = None

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

def view_orders(limit=20):
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
    query_order = """
        SELECT o.orderNumber, o.orderDate, o.requiredDate, o.shippedDate, o.status, o.comments,
               c.customerName, c.phone, c.addressLine1, c.city, c.country
        FROM orders o
        JOIN customers c ON o.customerNumber = c.customerNumber
        WHERE o.orderNumber = %s
    """
    order_info = execute_read_query(query_order, (order_number,))

    query_details = """
        SELECT p.productName, od.quantityOrdered, od.priceEach, (od.quantityOrdered * od.priceEach) AS subtotal
        FROM orderdetails od
        JOIN products p ON od.productCode = p.productCode
        WHERE od.orderNumber = %s
        ORDER BY od.orderLineNumber
    """
    order_details_data = execute_read_query(query_details, (order_number,))

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

        if order_details_data:
            print("\n--- Sản phẩm ---")
            details_display = [
                 {
                     "Tên sản phẩm": item.get('productName', 'N/A'),
                     "Số lượng": item.get('quantityOrdered', 0),
                     "Đơn giá": f"{item.get('priceEach', 0):,.2f}",
                     "Thành tiền": f"{item.get('subtotal', 0):,.2f}"
                 } for item in order_details_data
            ]
            print(tabulate(details_display, headers="keys", tablefmt="grid", floatfmt=".2f"))
            total_amount = sum(item.get('subtotal', 0) for item in order_details_data)
            print(f"\nTổng cộng: {total_amount:,.2f}")
        elif order_details_data is None:
             print("Lỗi khi truy vấn chi tiết sản phẩm.")
        else:
            print("Đơn hàng này không có chi tiết sản phẩm.")
    elif order_info is None:
         print(f"Lỗi khi truy vấn thông tin đơn hàng {order_number}.")
    else:
        print(f"Không tìm thấy đơn hàng với mã {order_number}.")

def add_order():
    print("\n--- Thêm đơn hàng mới ---")
    try:
        max_id_result = execute_read_query("SELECT MAX(orderNumber) as max_id FROM orders")
        if max_id_result is None:
             print("Lỗi: Không thể lấy mã đơn hàng hiện tại.")
             return
        if max_id_result and max_id_result[0]['max_id'] is not None:
             order_number = max_id_result[0]['max_id'] + 1
        else:
             order_number = 10000 # Hoặc một giá trị khởi tạo phù hợp

        cust_num_str = input("Nhập Mã Khách Hàng*: ")
        if not cust_num_str.isdigit():
            print("Lỗi: Mã khách hàng phải là số.")
            return
        customer_number = int(cust_num_str)

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
        if required_date < order_date:
            print("Lỗi: Ngày yêu cầu giao hàng không thể trước ngày đặt hàng.")
            return

        order_query = """
            INSERT INTO orders (orderNumber, orderDate, requiredDate, status, comments, customerNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        order_params = (order_number, order_date, required_date, status, comments if comments else None, customer_number)
        order_success = execute_modify_query(order_query, order_params)

        if not order_success:
            print("Không thể tạo đơn hàng chính.")
            return

        print(f"Đã tạo đơn hàng #{order_number}. Vui lòng thêm chi tiết sản phẩm.")

        line_number = 1
        added_products = False
        while True:
            print(f"\n--- Thêm sản phẩm thứ {line_number} cho đơn hàng #{order_number} ---")
            product_code = input("Nhập Mã Sản phẩm* (nhập 'xong' để kết thúc): ").strip()
            if product_code.lower() == 'xong':
                if not added_products:
                    print("Lỗi: Đơn hàng phải có ít nhất một sản phẩm.")
                    print(f"Đang xóa đơn hàng rỗng #{order_number}...")
                    execute_modify_query("DELETE FROM orderdetails WHERE orderNumber = %s", (order_number,))
                    execute_modify_query("DELETE FROM orders WHERE orderNumber = %s", (order_number,))
                    print("Đã hủy thêm đơn hàng.")
                    return
                else:
                    break

            prod_check_query = "SELECT productCode, productName, MSRP, quantityInStock FROM products WHERE productCode = %s"
            prod_check = execute_read_query(prod_check_query, (product_code,))
            if prod_check is None:
                 print("Lỗi khi kiểm tra sản phẩm.")
                 continue
            if not prod_check:
                print(f"Lỗi: Không tìm thấy sản phẩm với mã '{product_code}'.")
                continue

            current_product = prod_check[0]
            print(f"Thông tin sản phẩm: Tên: {current_product['productName']}, Giá đề xuất (MSRP): {current_product['MSRP']}, Tồn kho: {current_product['quantityInStock']}")

            quantity_str = input(f"Nhập số lượng (tối đa {current_product['quantityInStock']})*: ")
            if not quantity_str.isdigit() or int(quantity_str) <= 0:
                print("Lỗi: Số lượng phải là một số nguyên dương.")
                continue
            quantity = int(quantity_str)

            if quantity > current_product['quantityInStock']:
                print(f"Lỗi: Số lượng đặt ({quantity}) vượt quá số lượng tồn kho ({current_product['quantityInStock']}).")
                continue

            price_each_str = input(f"Nhập đơn giá (mặc định: {current_product['MSRP']}, bỏ trống để dùng mặc định): ")
            price_each = float(price_each_str) if price_each_str.replace('.', '', 1).isdigit() else current_product['MSRP']

            if price_each <= 0:
                print("Lỗi: Đơn giá phải là một số dương.")
                continue

            detail_query = """
                INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
                VALUES (%s, %s, %s, %s, %s)
            """
            detail_params = (order_number, product_code, quantity, price_each, line_number)
            detail_success = execute_modify_query(detail_query, detail_params)

            if detail_success:
                print(f"Đã thêm sản phẩm '{product_code}' vào đơn hàng.")
                line_number += 1
                added_products = True

        print(f"\nĐã thêm thành công đơn hàng #{order_number} với {line_number-1} sản phẩm.")

    except ValueError as ve:
        print(f"Lỗi định dạng dữ liệu: {ve}. Ví dụ: Ngày phải là YYYY-MM-DD, số lượng/giá phải là số.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi thêm đơn hàng: {e}")

def update_order_status(order_number, new_status):
    valid_statuses = ['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
    if new_status not in valid_statuses:
        print(f"Trạng thái '{new_status}' không hợp lệ. Các trạng thái hợp lệ: {', '.join(valid_statuses)}")
        return False

    order_check = execute_read_query("SELECT status, shippedDate FROM orders WHERE orderNumber = %s", (order_number,))
    if order_check is None:
        print(f"Lỗi khi kiểm tra đơn hàng {order_number}.")
        return False
    if not order_check:
         print(f"Lỗi: Không tìm thấy đơn hàng {order_number}.")
         return False

    current_status = order_check[0]['status']
    current_shipped_date = order_check[0]['shippedDate']

    if current_status == new_status:
         print(f"Đơn hàng {order_number} đã ở trạng thái '{new_status}'.")
         return True

    shipped_date_update_sql = ""
    if new_status == 'Shipped':
        if not current_shipped_date:
            shipped_date_update_sql = ", shippedDate = CURDATE()"
    elif current_status == 'Shipped' and new_status != 'Shipped':
        shipped_date_update_sql = ", shippedDate = NULL"

    query = f"UPDATE orders SET status = %s {shipped_date_update_sql} WHERE orderNumber = %s"
    params = (new_status, order_number)

    print(f"Đang cập nhật trạng thái đơn hàng {order_number} từ '{current_status}' thành '{new_status}'...")
    if execute_modify_query(query, params):
        return True
    return False

def assign_delivery(order_number):
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'vehicles' tồn tại và có cấu trúc phù hợp (deliveries.vehicleID -> vehicles.vehicleID). ***")
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
        existing_delivery_shipped = execute_read_query("SELECT deliveryID FROM deliveries WHERE orderID = %s", (order_number,))
        if existing_delivery_shipped:
            print(f"Đơn hàng {order_number} đã được giao và đã có thông tin giao hàng (ID: {existing_delivery_shipped[0]['deliveryID']}).")
        else:
            print(f"Đơn hàng {order_number} đã ở trạng thái 'Shipped' nhưng chưa có thông tin trong bảng 'deliveries'.")
    elif current_status == 'Cancelled':
         print(f"Lỗi: Đơn hàng {order_number} đã bị hủy, không thể gán giao hàng.")
         return
    elif current_status not in ['In Process', 'On Hold']:
        print(f"Lỗi: Đơn hàng {order_number} đang ở trạng thái '{current_status}', không thể gán giao hàng.")
        return

    delivery_check_query = "SELECT deliveryID, vehicleID FROM deliveries WHERE orderID = %s"
    existing_delivery = execute_read_query(delivery_check_query, (order_number,))

    if existing_delivery:
        print(f"Thông báo: Đơn hàng {order_number} đã được gán giao hàng trước đó (ID: {existing_delivery[0]['deliveryID']}, Xe ID: {existing_delivery[0]['vehicleID']}).")
        overwrite = input("Bạn có muốn gán lại xe khác và cập nhật ngày giao hàng không? (c/k): ").lower()
        if overwrite == 'c':
            pass
        else:
            if current_status != 'Shipped':
                confirm_ship = input(f"Đơn hàng đã có thông tin giao. Bạn có muốn cập nhật trạng thái đơn hàng thành 'Shipped' không? (c/k): ").lower()
                if confirm_ship == 'c':
                    update_order_status(order_number, 'Shipped')
            return

    vehicles_list = execute_read_query("SELECT vehicleID, vehicleType, licensePlate FROM vehicles")
    if not vehicles_list:
        print("Lỗi: Không có xe nào trong hệ thống (bảng 'vehicles' trống hoặc lỗi truy vấn).")
        return

    print("\n--- Danh sách xe có sẵn ---")
    vehicles_display = [{"ID": v['vehicleID'], "Loại xe": v['vehicleType'], "Biển số": v['licensePlate']} for v in vehicles_list]
    print(tabulate(vehicles_display, headers="keys", tablefmt="grid"))

    while True:
        try:
            selected_vehicle_id_str = input("Nhập ID của xe muốn chọn để giao hàng: ")
            selected_vehicle_id = int(selected_vehicle_id_str)
            vehicle_exists = any(v['vehicleID'] == selected_vehicle_id for v in vehicles_list)
            if vehicle_exists:
                break
            else:
                print(f"Lỗi: ID xe {selected_vehicle_id} không tồn tại trong danh sách.")
        except ValueError:
            print("Lỗi: ID xe phải là một số nguyên.")

    delivery_date_str = input(f"Nhập ngày giao hàng thực tế (YYYY-MM-DD, bỏ trống để lấy ngày hiện tại [{datetime.date.today()}]): ")
    delivery_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date() if delivery_date_str else datetime.date.today()

    if existing_delivery:
        update_query = """
            UPDATE deliveries SET vehicleID = %s, deliveryDate = %s
            WHERE orderID = %s
        """
        params_delivery = (selected_vehicle_id, delivery_date, order_number)
        print(f"Đang cập nhật thông tin giao hàng cho đơn hàng {order_number} với xe {selected_vehicle_id}...")
        success_delivery = execute_modify_query(update_query, params_delivery)
    else:
        insert_query = """
            INSERT INTO deliveries (orderID, vehicleID, deliveryDate)
            VALUES (%s, %s, %s)
        """
        params_delivery = (order_number, selected_vehicle_id, delivery_date)
        print(f"Đang gán xe {selected_vehicle_id} cho đơn hàng {order_number}...")
        success_delivery = execute_modify_query(insert_query, params_delivery)

    if success_delivery:
        print("Gán/Cập nhật thông tin giao hàng thành công.")
        print("Đang cập nhật trạng thái đơn hàng và ngày giao hàng (shippedDate) trong bảng orders...")
        update_order_query = "UPDATE orders SET status = 'Shipped', shippedDate = %s WHERE orderNumber = %s"
        update_order_params = (delivery_date, order_number)
        if execute_modify_query(update_order_query, update_order_params):
            print(f"Đơn hàng {order_number} đã được cập nhật thành 'Shipped' với ngày giao {delivery_date.strftime('%Y-%m-%d')}.")
        else:
            print(f"Lỗi khi cập nhật trạng thái/ngày giao cho đơn hàng {order_number} trong bảng orders.")
    else:
        print("Lỗi khi gán/cập nhật thông tin giao hàng trong bảng deliveries.")

def generate_delivery_invoice(order_number):
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'vehicles' tồn tại và có cấu trúc phù hợp. ***")
    query_order = """
        SELECT o.orderNumber, o.orderDate, o.requiredDate, o.shippedDate, o.status,
               c.customerName, c.phone, c.addressLine1, c.addressLine2, c.city, c.state, c.postalCode, c.country,
               d.deliveryID, d.deliveryDate,
               v.licensePlate, v.vehicleType
        FROM orders o
        JOIN customers c ON o.customerNumber = c.customerNumber
        LEFT JOIN deliveries d ON o.orderNumber = d.orderID
        LEFT JOIN vehicles v ON d.vehicleID = v.vehicleID
        WHERE o.orderNumber = %s
    """
    order_info_list = execute_read_query(query_order, (order_number,))

    query_details = """
        SELECT p.productName, od.quantityOrdered, od.priceEach, (od.quantityOrdered * od.priceEach) AS subtotal
        FROM orderdetails od
        JOIN products p ON od.productCode = p.productCode
        WHERE od.orderNumber = %s
        ORDER BY od.orderLineNumber
    """
    order_details_data = execute_read_query(query_details, (order_number,))

    if order_info_list is None:
         print(f"Lỗi khi truy vấn thông tin hóa đơn cho đơn hàng {order_number}.")
         print("(Có thể do bảng 'deliveries' hoặc 'vehicles' không tồn tại hoặc lỗi query)")
         return
    if not order_info_list:
        print(f"Không thể tạo hóa đơn: Không tìm thấy đơn hàng {order_number}.")
        return

    info = order_info_list[0]

    if info.get('status') != 'Shipped':
         print(f"Không thể tạo hóa đơn: Đơn hàng {order_number} chưa ở trạng thái 'Shipped'.")
         print(f"Trạng thái hiện tại: {info.get('status')}")
         return
    if not info.get('deliveryID') or not info.get('licensePlate'):
        print(f"Không thể tạo hóa đơn đầy đủ: Đơn hàng {order_number} đã 'Shipped' nhưng thiếu thông tin giao hàng (deliveryID hoặc xe).")
        print("Vui lòng sử dụng chức năng 'Gán giao hàng' để cập nhật.")

    print("\n" + "="*60)
    print(f"{'HÓA ĐƠN GIAO HÀNG':^60}")
    print("="*60)
    order_date_str = info['orderDate'].strftime('%Y-%m-%d') if info.get('orderDate') else 'N/A'

    actual_delivery_date = info.get('deliveryDate') or info.get('shippedDate')
    delivery_date_str = actual_delivery_date.strftime('%Y-%m-%d') if isinstance(actual_delivery_date, datetime.date) else 'N/A'

    print(f"Số đơn hàng: {info.get('orderNumber', 'N/A'):<20} Ngày đặt: {order_date_str}")
    print(f"Mã giao hàng: {info.get('deliveryID', 'Chưa có'):<18} Ngày giao: {delivery_date_str}")
    print(f"Xe giao hàng: {info.get('licensePlate', 'Chưa gán xe')} ({info.get('vehicleType', 'N/A')})")
    print("-"*60)
    print("Thông tin khách hàng:")
    print(f"  Tên: {info.get('customerName', 'N/A')}")
    print(f"  Điện thoại: {info.get('phone', 'N/A')}")
    full_address = f"{info.get('addressLine1', '')}"
    if info.get('addressLine2'):
        full_address += f", {info.get('addressLine2', '')}"
    full_address += f", {info.get('city', '')}"
    if info.get('state'):
        full_address += f", {info.get('state', '')}"
    if info.get('postalCode'):
        full_address += f" {info.get('postalCode', '')}"
    full_address += f", {info.get('country', '')}"
    print(f"  Địa chỉ: {full_address}")
    print("-"*60)
    print("Chi tiết đơn hàng:")

    if order_details_data:
        headers = ["Sản phẩm", "SL", "Đơn giá", "Thành tiền"]
        details_display_table = [
            (item.get('productName', 'N/A'),
             item.get('quantityOrdered', 0),
             f"{item.get('priceEach', 0):,.2f}",
             f"{item.get('subtotal', 0):,.2f}")
            for item in order_details_data
        ]
        print(tabulate(details_display_table, headers=headers, tablefmt="plain"))
        total_amount = sum(item.get('subtotal', 0) for item in order_details_data)
        print("-"*60)
        print(f"{'Tổng cộng:':>48} {total_amount:,.2f}")
    elif order_details_data is None:
         print("  (Lỗi khi truy vấn chi tiết sản phẩm)")
    else:
        print("  (Không có chi tiết sản phẩm)")

    print("="*60)
    print(f"{'Cảm ơn quý khách!':^60}")
    print("="*60 + "\n")

# ========== CHỨC NĂNG QUẢN LÝ CHI PHÍ (EXPENSES) ==========
def view_deliveries_brief(limit=10):
    """Hiển thị danh sách tóm tắt các chuyến giao hàng gần đây để người dùng tham khảo deliveryID."""
    query = """
        SELECT d.deliveryID, d.orderID, o.customerNumber, c.customerName, d.vehicleID, v.licensePlate, d.deliveryDate
        FROM deliveries d
        JOIN orders o ON d.orderID = o.orderNumber
        JOIN customers c ON o.customerNumber = c.customerNumber
        LEFT JOIN vehicles v ON d.vehicleID = v.vehicleID
        ORDER BY d.deliveryID DESC
        LIMIT %s
    """
    deliveries = execute_read_query(query, (limit,))
    if deliveries:
        print("\n--- Danh sách các chuyến giao hàng gần đây (để tham khảo deliveryID) ---")
        deliveries_display = [
            {
                "Delivery ID": item['deliveryID'],
                "Order ID": item['orderID'],
                "Tên KH": item.get('customerName', 'N/A'),
                "Xe ID": item['vehicleID'],
                "Biển số": item.get('licensePlate', 'N/A'),
                "Ngày giao": item['deliveryDate'].strftime('%Y-%m-%d') if item.get('deliveryDate') else 'N/A'
            }
            for item in deliveries
        ]
        print(tabulate(deliveries_display, headers="keys", tablefmt="grid"))
        return True
    elif deliveries is None:
        print("Lỗi khi truy vấn danh sách giao hàng.")
    else:
        print("Không tìm thấy chuyến giao hàng nào trong hệ thống.")
    return False

def add_expense_for_delivery():
    """Thêm chi phí cho một chuyến giao hàng cụ thể."""
    print("\n--- Thêm Chi Phí Cho Chuyến Giao Hàng ---")

    if not view_deliveries_brief():
        return

    try:
        delivery_id_str = input("Nhập ID Chuyến Giao Hàng (deliveryID) bạn muốn thêm chi phí*: ").strip()
        if not delivery_id_str.isdigit():
            print("Lỗi: ID Chuyến Giao Hàng phải là số.")
            return
        delivery_id = int(delivery_id_str)

        delivery_check = execute_read_query("SELECT deliveryID FROM deliveries WHERE deliveryID = %s", (delivery_id,))
        if not delivery_check:
            print(f"Lỗi: Không tìm thấy chuyến giao hàng với ID {delivery_id}.")
            print("Vui lòng kiểm tra lại danh sách ở trên hoặc đảm bảo chuyến giao hàng đã được tạo.")
            return

        print(f"\nĐang thêm chi phí cho Delivery ID: {delivery_id}")
        expense_type = input("Nhập loại chi phí (ví dụ: Xăng dầu, Phí cầu đường, Tiền ăn)*: ").strip()
        amount_str = input("Nhập số tiền chi phí*: ").strip()

        if not expense_type:
            print("Lỗi: Loại chi phí không được để trống.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Lỗi: Số tiền chi phí phải là một số dương.")
                return
        except ValueError:
            print("Lỗi: Số tiền chi phí phải là một số hợp lệ.")
            return

        query = """
            INSERT INTO expenses (deliveryID, expenseType, amount)
            VALUES (%s, %s, %s)
        """
        params = (delivery_id, expense_type, amount)

        if execute_modify_query(query, params, return_last_id=True):
            print(f"Đã thêm chi phí '{expense_type}' trị giá {amount:,.2f} cho chuyến giao hàng ID {delivery_id} thành công.")
        else:
            print(f"Lỗi khi thêm chi phí cho chuyến giao hàng ID {delivery_id}.")

    except ValueError:
        print("Lỗi: ID Chuyến Giao Hàng nhập vào không hợp lệ.")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")

# ========== BÁO CÁO ==========

def report_delivery_performance():
    query = """
        SELECT
            COUNT(*) AS totalOrders,
            SUM(CASE WHEN status = 'Shipped' THEN 1 ELSE 0 END) AS shippedOrders,
            SUM(CASE WHEN status = 'Shipped' AND shippedDate IS NOT NULL AND requiredDate IS NOT NULL AND shippedDate <= requiredDate THEN 1 ELSE 0 END) AS onTimeOrders,
            SUM(CASE WHEN status = 'Shipped' AND shippedDate IS NOT NULL AND requiredDate IS NOT NULL AND shippedDate > requiredDate THEN 1 ELSE 0 END) AS lateOrders,
            AVG(CASE WHEN status = 'Shipped' AND shippedDate IS NOT NULL AND orderDate IS NOT NULL THEN DATEDIFF(shippedDate, orderDate) ELSE NULL END) AS avgShippingDays
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
        avg_days_decimal = data.get('avgShippingDays')

        print(f"Tổng số đơn hàng: {total}")
        print(f"Số đơn đã giao (Shipped): {shipped}")
        if shipped > 0:
            on_time_percent = (on_time / shipped * 100) if shipped > 0 else 0
            late_percent = (late / shipped * 100) if shipped > 0 else 0
            print(f"Số đơn giao đúng hạn (shippedDate <= requiredDate): {on_time} ({on_time_percent:.2f}%)")
            print(f"Số đơn giao trễ (shippedDate > requiredDate): {late} ({late_percent:.2f}%)")
            if avg_days_decimal is not None:
                 avg_days_float = float(avg_days_decimal)
                 print(f"Thời gian giao hàng trung bình (ngày): {avg_days_float:.2f}")
            else:
                 print("Thời gian giao hàng trung bình: Chưa có đủ dữ liệu (cần shippedDate và orderDate)")
        else:
             print("Chưa có đơn hàng nào được giao để thống kê chi tiết.")
    elif report_data is None:
         print("Lỗi khi tạo báo cáo hiệu suất giao hàng.")
    else:
        print("Không có dữ liệu để tạo báo cáo hiệu suất giao hàng.")

def report_order_history(customer_number):
    cust_name_query = "SELECT customerName FROM customers WHERE customerNumber = %s"
    cust_name_result = execute_read_query(cust_name_query, (customer_number,))
    if cust_name_result is None:
         print(f"Lỗi khi truy vấn tên khách hàng {customer_number}.")
         return
    if not cust_name_result:
        print(f"Lỗi: Không tìm thấy khách hàng với mã {customer_number}.")
        return
    customer_name = cust_name_result[0]['customerName']

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
        history_display = [
            {
                "Mã ĐH": item['orderNumber'],
                "Ngày đặt": item['orderDate'].strftime('%Y-%m-%d') if item.get('orderDate') else 'N/A',
                "Trạng thái": item.get('status', 'N/A'),
                "Tổng tiền": f"{item.get('totalAmount', 0):,.2f}" if item.get('totalAmount') is not None else "0.00"
            }
            for item in history
        ]
        print(tabulate(history_display, headers="keys", tablefmt="grid"))
    elif history is None:
         print(f"Lỗi khi truy vấn lịch sử đơn hàng cho khách hàng {customer_number}.")
    else:
        print(f"Khách hàng {customer_name} (Mã KH: {customer_number}) không có lịch sử đơn hàng.")

def report_delivery_cost_summary():
    print("\n*** Chức năng này yêu cầu bảng 'deliveries' và 'expenses' tồn tại và có cấu trúc phù hợp. ***")
    query = """
        SELECT d.deliveryID, d.orderID, o.orderDate, c.customerName, SUM(e.amount) AS totalCost
        FROM deliveries d
        JOIN orders o ON d.orderID = o.orderNumber
        JOIN customers c ON o.customerNumber = c.customerNumber
        LEFT JOIN expenses e ON d.deliveryID = e.deliveryID
        GROUP BY d.deliveryID, d.orderID, o.orderDate, c.customerName
        ORDER BY d.deliveryID
    """
    costs = execute_read_query(query)
    if costs:
        print("\n--- Tổng hợp chi phí giao hàng theo chuyến ---")
        costs_display = [
            {
                "Delivery ID": item['deliveryID'],
                "Order ID": item['orderID'],
                "Ngày Đặt Hàng": item['orderDate'].strftime('%Y-%m-%d') if item.get('orderDate') else 'N/A',
                "Khách Hàng": item.get('customerName', 'N/A'),
                "Tổng chi phí GH": f"{item.get('totalCost', 0):,.2f}" if item.get('totalCost') is not None else "0.00"
            }
            for item in costs
        ]
        print(tabulate(costs_display, headers="keys", tablefmt="grid"))
    elif costs is None:
         print("Lỗi khi tạo báo cáo chi phí giao hàng.")
    else:
        print("Không có dữ liệu chi phí giao hàng để báo cáo.")

def report_grand_total_delivery_cost():
     print("\n*** Chức năng này yêu cầu bảng 'expenses' tồn tại và có cấu trúc phù hợp. ***")
     query = "SELECT SUM(amount) AS grandTotal FROM expenses"
     result = execute_read_query(query)
     if result is None:
          print("Lỗi khi tính tổng chi phí giao hàng.")
     elif result and result[0].get('grandTotal') is not None:
          grand_total_decimal = result[0]['grandTotal']
          print(f"\n--- Tổng chi phí giao hàng toàn bộ ---")
          grand_total_float = float(grand_total_decimal)
          print(f"Tổng cộng: {grand_total_float:,.2f}")
     else:
          print("Không có dữ liệu chi phí giao hàng hoặc không thể tính tổng.")

# ========== GIAO DIỆN CONSOLE ==========
def display_menu():
    print("\n" + "="*30)
    print(f"{'QUẢN LÝ GIAO HÀNG':^30}")
    print("="*30)
    print("1. Quản lý Khách hàng")
    print("2. Quản lý Đơn hàng")
    print("3. Quản lý Giao hàng & Chi phí") # Cập nhật tên menu
    print("4. Báo cáo")
    print("0. Thoát")
    print("-"*30)
    return input("Chọn chức năng: ")

def customer_menu():
    while True:
        print("\n--- Quản lý Khách hàng ---")
        print("1. Xem danh sách khách hàng")
        print("2. Tìm khách hàng theo tên")
        print("3. Thêm khách hàng mới")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ").strip()
        if choice == '1':
            view_customers()
        elif choice == '2':
            keyword = input("Nhập tên khách hàng cần tìm: ").strip()
            find_customer_by_name(keyword)
        elif choice == '3':
            add_customer()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def order_menu():
    while True:
        print("\n--- Quản lý Đơn hàng ---")
        print("1. Xem danh sách đơn hàng gần đây")
        print("2. Xem chi tiết đơn hàng")
        print("3. Thêm đơn hàng mới")
        print("4. Cập nhật trạng thái đơn hàng")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ").strip()
        if choice == '1':
            view_orders()
        elif choice == '2':
            try:
                order_num_str = input("Nhập mã đơn hàng cần xem: ").strip()
                if not order_num_str.isdigit():
                    print("Mã đơn hàng phải là số.")
                    continue
                order_num = int(order_num_str)
                view_order_details(order_num)
            except ValueError:
                print("Mã đơn hàng không hợp lệ.")
        elif choice == '3':
             add_order()
        elif choice == '4':
             try:
                order_num_str = input("Nhập mã đơn hàng cần cập nhật: ").strip()
                if not order_num_str.isdigit():
                    print("Mã đơn hàng phải là số.")
                    continue
                order_num = int(order_num_str)

                valid_statuses = ['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
                print(f"Các trạng thái hợp lệ: {', '.join(valid_statuses)}")
                new_status = input("Nhập trạng thái mới: ").strip()
                update_order_status(order_num, new_status)
             except ValueError:
                print("Mã đơn hàng không hợp lệ.")
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def delivery_menu():
     print("\n*** Lưu ý: Chức năng giao hàng yêu cầu các bảng 'deliveries', 'vehicles' (và 'expenses' cho báo cáo chi phí) tồn tại và có cấu trúc phù hợp. ***")
     print("*** Đảm bảo `deliveries.vehicleID` tham chiếu đến `vehicles.vehicleID`. ***")
     while True:
        print("\n--- Quản lý Giao hàng & Chi phí ---")
        print("1. Gán/Cập nhật giao hàng & trạng thái 'Shipped' cho đơn")
        print("2. Tạo hóa đơn giao hàng")
        print("3. Thêm chi phí cho chuyến giao hàng")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ").strip()
        if choice == '1':
            try:
                order_num_str = input("Nhập mã đơn hàng cần gán/cập nhật giao hàng: ").strip()
                if not order_num_str.isdigit():
                    print("Mã đơn hàng phải là số.")
                    continue
                order_num = int(order_num_str)
                assign_delivery(order_num)
            except ValueError:
                print("Mã đơn hàng không hợp lệ.")
        elif choice == '2':
             try:
                order_num_str = input("Nhập mã đơn hàng cần tạo hóa đơn: ").strip()
                if not order_num_str.isdigit():
                    print("Mã đơn hàng phải là số.")
                    continue
                order_num = int(order_num_str)
                generate_delivery_invoice(order_num)
             except ValueError:
                print("Mã đơn hàng không hợp lệ.")
        elif choice == '3':
            add_expense_for_delivery()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

def report_menu():
    while True:
        print("\n--- Báo cáo ---")
        print("1. Hiệu suất giao hàng (Từ bảng Orders)")
        print("2. Lịch sử đơn hàng của khách hàng")
        print("3. Chi phí giao hàng theo chuyến (Cần bảng deliveries & expenses)") # Cập nhật tên báo cáo
        print("4. Tổng chi phí giao hàng toàn bộ (Cần bảng expenses)")
        print("0. Quay lại menu chính")
        choice = input("Chọn: ").strip()
        if choice == '1':
            report_delivery_performance()
        elif choice == '2':
            try:
                cust_num_str = input("Nhập mã khách hàng: ").strip()
                if not cust_num_str.isdigit():
                    print("Mã khách hàng phải là số.")
                    continue
                cust_num = int(cust_num_str)
                report_order_history(cust_num)
            except ValueError:
                print("Mã khách hàng không hợp lệ.")
        elif choice == '3':
            report_delivery_cost_summary()
        elif choice == '4':
             report_grand_total_delivery_cost()
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    print("Đang kiểm tra kết nối database...")
    conn_test = create_connection()
    if not conn_test or not conn_test.is_connected():
        print("="*40)
        print(" LỖI KẾT NỐI DATABASE BAN ĐẦU ".center(40, "="))
        print("="*40)
        exit()
    else:
         print("Kết nối database thành công.")
         conn_test.close()

    while True:
        main_choice = display_menu()
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