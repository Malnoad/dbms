CREATE DATABASE  IF NOT EXISTS `classicmodels` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `classicmodels`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: classicmodels
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `current_delivery_schedule`
--

DROP TABLE IF EXISTS `current_delivery_schedule`;
/*!50001 DROP VIEW IF EXISTS `current_delivery_schedule`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `current_delivery_schedule` AS SELECT 
 1 AS `deliveryID`,
 1 AS `deliveryDate`,
 1 AS `orderID`,
 1 AS `customerName`,
 1 AS `licensePlate`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customerNumber` int NOT NULL,
  `customerName` varchar(50) NOT NULL,
  `contactLastName` varchar(50) NOT NULL,
  `contactFirstName` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `addressLine1` varchar(50) NOT NULL,
  `addressLine2` varchar(50) DEFAULT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) DEFAULT NULL,
  `postalCode` varchar(15) DEFAULT NULL,
  `country` varchar(50) NOT NULL,
  `salesRepEmployeeNumber` int DEFAULT NULL,
  `creditLimit` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`customerNumber`),
  KEY `salesRepEmployeeNumber` (`salesRepEmployeeNumber`),
  KEY `idx_customers_customerNumber` (`customerNumber`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`salesRepEmployeeNumber`) REFERENCES `employees` (`employeeNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Nguyen Trading Co.','Nguyen','Anh','084-1234567','123 Le Loi',NULL,'Ho Chi Minh','SG','700000','Vietnam',NULL,35000.00),(2,'Horizon Logistics','Tran','Linh','084-2345678','456 Tran Hung Dao',NULL,'Ha Noi','HN','100000','Vietnam',NULL,42000.00),(3,'Kobe Motors','Sato','Kenji','081-9876543','1-2-3 Shibuya',NULL,'Tokyo',NULL,'1500001','Japan',NULL,50000.00),(4,'Techone Ltd.','Pham','Huy','084-8765432','789 Nguyen Van Cu',NULL,'Can Tho','CT','900000','Vietnam',NULL,30000.00),(5,'Alpha Imports','Smith','John','001-5551234','101 Wall Street',NULL,'New York','NY','10005','USA',NULL,60000.00),(6,'Singapore Retail','Lim','Wei','065-3344556','88 Raffles Place',NULL,'Singapore',NULL,'048621','Singapore',NULL,45000.00),(7,'Bangkok Distribution','Wong','Arthit','066-4433221','99 Rama IV Road',NULL,'Bangkok',NULL,'10330','Thailand',NULL,37000.00),(8,'1','2','3','0922222222','121',NULL,'Ha Noi',NULL,NULL,'Viet',NULL,NULL);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveries`
--

DROP TABLE IF EXISTS `deliveries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveries` (
  `deliveryID` int NOT NULL AUTO_INCREMENT,
  `orderID` int DEFAULT NULL,
  `vehicleID` int DEFAULT NULL,
  `deliveryDate` date DEFAULT NULL,
  PRIMARY KEY (`deliveryID`),
  KEY `vehicleID` (`vehicleID`),
  KEY `idx_deliveries_order_vehicle` (`orderID`,`vehicleID`),
  CONSTRAINT `deliveries_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderNumber`),
  CONSTRAINT `deliveries_ibfk_2` FOREIGN KEY (`vehicleID`) REFERENCES `employees` (`employeeNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveries`
--

LOCK TABLES `deliveries` WRITE;
/*!40000 ALTER TABLE `deliveries` DISABLE KEYS */;
INSERT INTO `deliveries` VALUES (1,50001,1003,'2024-04-03'),(2,50002,1004,'2024-04-04'),(3,50003,1005,'2024-04-05'),(4,50004,1006,'2024-04-06'),(5,50005,1007,'2024-04-07'),(6,50006,1002,'2024-04-08'),(7,50007,1001,'2024-04-09');
/*!40000 ALTER TABLE `deliveries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `delivery_cost_summary`
--

DROP TABLE IF EXISTS `delivery_cost_summary`;
/*!50001 DROP VIEW IF EXISTS `delivery_cost_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `delivery_cost_summary` AS SELECT 
 1 AS `orderID`,
 1 AS `totalCost`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employeeNumber` int NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `extension` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `officeCode` varchar(10) NOT NULL,
  `reportsTo` int DEFAULT NULL,
  `jobTitle` varchar(50) NOT NULL,
  PRIMARY KEY (`employeeNumber`),
  KEY `reportsTo` (`reportsTo`),
  KEY `officeCode` (`officeCode`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`reportsTo`) REFERENCES `employees` (`employeeNumber`),
  CONSTRAINT `employees_ibfk_2` FOREIGN KEY (`officeCode`) REFERENCES `offices` (`officeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1001,'Le','Minh','x101','minh.le@example.com','1',NULL,'Sales Rep'),(1002,'Nguyen','Linh','x102','linh.nguyen@example.com','1',NULL,'Sales Rep'),(1003,'Tran','Son','x103','son.tran@example.com','2',NULL,'Delivery Driver'),(1004,'Pham','Tuan','x104','tuan.pham@example.com','2',NULL,'Delivery Driver'),(1005,'Do','Khanh','x105','khanh.do@example.com','3',NULL,'Sales Manager'),(1006,'Ho','Thao','x106','thao.ho@example.com','3',NULL,'Support Staff'),(1007,'Vo','Quang','x107','quang.vo@example.com','1',NULL,'Logistics Coordinator');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `expenseID` int NOT NULL AUTO_INCREMENT,
  `deliveryID` int DEFAULT NULL,
  `expenseType` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `vehicleID` int DEFAULT NULL,
  PRIMARY KEY (`expenseID`),
  KEY `deliveryID` (`deliveryID`),
  KEY `fk_expenses_vehicleID` (`vehicleID`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`deliveryID`) REFERENCES `deliveries` (`deliveryID`),
  CONSTRAINT `fk_expenses_vehicleID` FOREIGN KEY (`vehicleID`) REFERENCES `vehicles` (`vehicleID`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (16,1,'Fuel',150.50,NULL),(17,1,'Toll',30.00,NULL),(18,2,'Fuel',140.00,NULL),(19,3,'Packaging',45.00,NULL),(20,4,'Miscellaneous',25.00,NULL),(21,5,'Packaging',50.25,NULL),(22,6,'Toll',20.00,NULL),(23,7,'Fuel',160.00,NULL),(24,NULL,'Maintenance',200.75,1005),(25,NULL,'Driver Fee',100.00,1005),(26,NULL,'Insurance',75.00,1001),(27,NULL,'Maintenance',180.00,1003),(28,NULL,'Insurance',60.00,1002);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `feedbackID` int NOT NULL AUTO_INCREMENT,
  `orderID` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `comment` text,
  `dateSubmitted` date DEFAULT NULL,
  `customerNumber` int DEFAULT NULL,
  PRIMARY KEY (`feedbackID`),
  KEY `orderID` (`orderID`),
  KEY `fk_feedbacks_customerNumber` (`customerNumber`),
  CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderNumber`),
  CONSTRAINT `fk_feedbacks_customerNumber` FOREIGN KEY (`customerNumber`) REFERENCES `customers` (`customerNumber`),
  CONSTRAINT `feedbacks_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES (1,50001,5,'Perfect delivery!','2024-04-04',1),(2,50002,4,'Very satisfied.','2024-04-05',2),(3,50003,5,'Great packaging.','2024-04-06',3),(4,50004,3,'Arrived on time, but box damaged.','2024-04-07',4),(5,50005,4,'Smooth process.','2024-04-08',5),(6,50006,2,'Came late.','2024-04-09',6);
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offices`
--

DROP TABLE IF EXISTS `offices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offices` (
  `officeCode` varchar(10) NOT NULL,
  `city` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `addressLine1` varchar(50) NOT NULL,
  `addressLine2` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) NOT NULL,
  `postalCode` varchar(15) NOT NULL,
  `territory` varchar(10) NOT NULL,
  PRIMARY KEY (`officeCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offices`
--

LOCK TABLES `offices` WRITE;
/*!40000 ALTER TABLE `offices` DISABLE KEYS */;
INSERT INTO `offices` VALUES ('1','Ho Chi Minh','084-1112222','12 Nguyen Hue',NULL,NULL,'Vietnam','700000','SE Asia'),('2','Ha Noi','084-2223333','34 Kim Ma',NULL,NULL,'Vietnam','100000','SE Asia'),('3','Tokyo','081-1231231','9 Akihabara',NULL,NULL,'Japan','101002','Asia'),('4','Bangkok','066-5554444','56 Sukhumvit Rd',NULL,NULL,'Thailand','10110','SE Asia'),('5','Singapore','065-9998888','78 Orchard Rd',NULL,NULL,'Singapore','238839','SE Asia'),('6','New York','001-2125551234','123 Madison Ave',NULL,'NY','USA','10010','NA'),('7','London','0044-2075559876','45 Baker St',NULL,NULL,'UK','W11 7EU','Europe');
/*!40000 ALTER TABLE `offices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `order_cost`
--

DROP TABLE IF EXISTS `order_cost`;
/*!50001 DROP VIEW IF EXISTS `order_cost`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `order_cost` AS SELECT 
 1 AS `orderNumber`,
 1 AS `priceEach`,
 1 AS `quantityOrdered`,
 1 AS `total_cost`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `orderdetails`
--

DROP TABLE IF EXISTS `orderdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderdetails` (
  `orderNumber` int NOT NULL,
  `productCode` varchar(15) NOT NULL,
  `quantityOrdered` int NOT NULL,
  `priceEach` decimal(10,2) NOT NULL,
  `orderLineNumber` smallint NOT NULL,
  PRIMARY KEY (`orderNumber`,`productCode`),
  KEY `productCode` (`productCode`),
  CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`orderNumber`) REFERENCES `orders` (`orderNumber`),
  CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`productCode`) REFERENCES `products` (`productCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderdetails`
--

LOCK TABLES `orderdetails` WRITE;
/*!40000 ALTER TABLE `orderdetails` DISABLE KEYS */;
INSERT INTO `orderdetails` VALUES (50001,'P001',2,42.00,1),(50002,'P002',1,55.00,1),(50003,'P003',3,65.50,1),(50004,'P004',1,120.00,1),(50005,'P005',2,38.00,1),(50006,'P002',4,30.00,1),(50007,'P001',1,49.90,1),(50008,'P001',1,95.00,1);
/*!40000 ALTER TABLE `orderdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `orderNumber` int NOT NULL,
  `orderDate` date NOT NULL,
  `requiredDate` date NOT NULL,
  `shippedDate` date DEFAULT NULL,
  `status` varchar(15) NOT NULL,
  `comments` text,
  `customerNumber` int NOT NULL,
  PRIMARY KEY (`orderNumber`),
  KEY `idx_orders_order_id` (`orderNumber`),
  KEY `idx_orders_status` (`status`),
  KEY `idx_orders_customer_date` (`customerNumber`,`orderDate`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customerNumber`) REFERENCES `customers` (`customerNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (50001,'2023-05-01','2023-05-10','2023-05-09','Shipped',NULL,1),(50002,'2023-05-02','2023-05-12','2023-05-11','Shipped',NULL,2),(50003,'2023-05-03','2023-05-15','2023-05-14','Shipped',NULL,3),(50004,'2023-05-04','2023-05-14','2023-05-13','Shipped',NULL,4),(50005,'2023-05-05','2023-05-13','2023-05-12','Shipped',NULL,5),(50006,'2023-05-06','2023-05-16','2023-05-15','Shipped',NULL,6),(50007,'2023-05-07','2023-05-17','2023-05-16','Shipped',NULL,7),(50008,'2025-05-18','2025-06-17','2025-05-18','Shipped',NULL,1);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `customerNumber` int NOT NULL,
  `checkNumber` varchar(50) NOT NULL,
  `paymentDate` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`customerNumber`,`checkNumber`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`customerNumber`) REFERENCES `customers` (`customerNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,'CHK001','2024-04-03',84.00),(2,'CHK002','2024-04-04',55.00),(3,'CHK003','2024-04-05',196.50),(4,'CHK004','2024-04-06',120.00),(5,'CHK005','2024-04-07',76.00),(6,'CHK006','2024-04-08',49.90),(7,'CHK007','2024-04-09',120.00);
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `pending_orders`
--

DROP TABLE IF EXISTS `pending_orders`;
/*!50001 DROP VIEW IF EXISTS `pending_orders`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `pending_orders` AS SELECT 
 1 AS `orderNumber`,
 1 AS `status`,
 1 AS `orderDate`,
 1 AS `contactFirstName`,
 1 AS `contactLastName`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productlines`
--

DROP TABLE IF EXISTS `productlines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productlines` (
  `productLine` varchar(50) NOT NULL,
  `textDescription` varchar(4000) DEFAULT NULL,
  `htmlDescription` mediumtext,
  `image` mediumblob,
  PRIMARY KEY (`productLine`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productlines`
--

LOCK TABLES `productlines` WRITE;
/*!40000 ALTER TABLE `productlines` DISABLE KEYS */;
INSERT INTO `productlines` VALUES ('Classic Cars','Classic collectible cars from the 1950s–1990s',NULL,NULL),('Motorcycles','Miniature motorcycle models',NULL,NULL),('Planes','Aircraft models in various scales',NULL,NULL),('Trucks and Buses','Die-cast models of trucks and buses',NULL,NULL);
/*!40000 ALTER TABLE `productlines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `productCode` varchar(15) NOT NULL,
  `productName` varchar(70) NOT NULL,
  `productLine` varchar(50) NOT NULL,
  `productScale` varchar(10) NOT NULL,
  `productVendor` varchar(50) NOT NULL,
  `productDescription` text NOT NULL,
  `quantityInStock` smallint NOT NULL,
  `buyPrice` decimal(10,2) NOT NULL,
  `MSRP` decimal(10,2) NOT NULL,
  PRIMARY KEY (`productCode`),
  KEY `productLine` (`productLine`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`productLine`) REFERENCES `productlines` (`productLine`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('P001','1969 Ford Mustang','Classic Cars','1:18','AutoArt','Classic American muscle car',50,42.00,95.00),('P002','2001 BMW X5','Trucks and Buses','1:18','Minichamps','Luxury SUV model',30,55.00,110.00),('P003','Harley Davidson Chopper','Motorcycles','1:12','Exoto','Miniature Harley Davidson',25,65.50,125.00),('P004','Airbus A380','Planes','1:72','Dragon Models','Detailed Airbus A380 model',10,120.00,199.00),('P005','Porsche 911 Turbo','Classic Cars','1:18','Welly','Iconic sports car model',40,38.00,89.00);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `undelivered_orders`
--

DROP TABLE IF EXISTS `undelivered_orders`;
/*!50001 DROP VIEW IF EXISTS `undelivered_orders`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `undelivered_orders` AS SELECT 
 1 AS `orderNumber`,
 1 AS `customerNumber`,
 1 AS `orderDate`,
 1 AS `status`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicles` (
  `vehicleID` int NOT NULL,
  `vehicleType` varchar(50) DEFAULT NULL,
  `licensePlate` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`vehicleID`),
  KEY `idx_vehicles_plate_type` (`licensePlate`,`vehicleType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
INSERT INTO `vehicles` VALUES (1003,'Motorbike','51A-123.01'),(1006,'Motorbike','51A-456.04'),(1002,'Motorbike','51A-678.06'),(1005,'Truck','51C-345.03'),(1007,'Truck','51C-567.05'),(1004,'Van','51D-234.02'),(1001,'Van','51D-789.07');
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'classicmodels'
--

--
-- Dumping routines for database 'classicmodels'
--
/*!50003 DROP FUNCTION IF EXISTS `avg_delivery_cost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `avg_delivery_cost`() RETURNS decimal(10,2)
    DETERMINISTIC
BEGIN
    DECLARE avg_cost DECIMAL(10,2);
    SELECT AVG(Amount) INTO avg_cost FROM Expenses;
    RETURN avg_cost;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `count_vehicle_deliveries` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `count_vehicle_deliveries`(vehicle_id INT) RETURNS int
    DETERMINISTIC
BEGIN
    DECLARE delivery_count INT;
    SELECT COUNT(*) INTO delivery_count 
    FROM Deliveries 
    WHERE VehicleID = vehicle_id;
    RETURN delivery_count;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `assign_vehicle_to_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `assign_vehicle_to_order`(order_number INT)
BEGIN
    DECLARE vehicle_id INT;
    
    -- Assuming there is a vehicles table, and we need to assign the first available vehicle
    SELECT vehicle_id INTO vehicle_id
    FROM vehicles
    WHERE status = 'Available'
    LIMIT 1;
    
    -- Assign vehicle to the order
    IF vehicle_id IS NOT NULL THEN
        UPDATE orders
        SET vehicle_id = vehicle_id
        WHERE orderNumber = order_number;
        
        -- Update vehicle status
        UPDATE vehicles
        SET status = 'In use'
        WHERE vehicle_id = vehicle_id;
        
        SELECT 'Vehicle assigned successfully.' AS message;
    ELSE
        SELECT 'No available vehicles.' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `auto_assign_vehicle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `auto_assign_vehicle`(IN p_orderID INT)
BEGIN
  DECLARE v_vehicleID INT;

  SELECT vehicleID INTO v_vehicleID
  FROM vehicles
  ORDER BY RAND()
  LIMIT 1;

  INSERT INTO deliveries (orderID, vehicleID, deliveryDate)
  VALUES (p_orderID, v_vehicleID, CURDATE());
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `calculate_total_cost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `calculate_total_cost`(order_number INT)
BEGIN
    DECLARE total_cost DECIMAL(10,2);
    
    -- Calculate the total cost for the order
    SELECT SUM(od.priceEach * od.quantityOrdered) INTO total_cost
    FROM orderdetails od
    WHERE od.orderNumber = order_number;
    
    -- Return total cost
    SELECT total_cost AS total_cost;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetCustomers` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCustomers`()
begin 
	select * from customers;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_order_delivery_cost` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_order_delivery_cost`(IN p_orderID INT, OUT p_total DECIMAL(10,2))
BEGIN
  SELECT SUM(e.amount)
  INTO p_total
  FROM deliveries d
  JOIN expenses e ON d.deliveryID = e.deliveryID
  WHERE d.orderID = p_orderID;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `current_delivery_schedule`
--

/*!50001 DROP VIEW IF EXISTS `current_delivery_schedule`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `current_delivery_schedule` AS select `d`.`deliveryID` AS `deliveryID`,`d`.`deliveryDate` AS `deliveryDate`,`d`.`orderID` AS `orderID`,`c`.`customerName` AS `customerName`,`v`.`licensePlate` AS `licensePlate` from (((`deliveries` `d` join `orders` `o` on((`d`.`orderID` = `o`.`orderNumber`))) join `customers` `c` on((`o`.`customerNumber` = `c`.`customerNumber`))) join `vehicles` `v` on((`d`.`vehicleID` = `v`.`vehicleID`))) where (`o`.`status` = 'Shipped') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `delivery_cost_summary`
--

/*!50001 DROP VIEW IF EXISTS `delivery_cost_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `delivery_cost_summary` AS select `d`.`orderID` AS `orderID`,sum(`e`.`amount`) AS `totalCost` from (`deliveries` `d` join `expenses` `e` on((`d`.`deliveryID` = `e`.`deliveryID`))) group by `d`.`orderID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `order_cost`
--

/*!50001 DROP VIEW IF EXISTS `order_cost`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `order_cost` AS select `o`.`orderNumber` AS `orderNumber`,`od`.`priceEach` AS `priceEach`,`od`.`quantityOrdered` AS `quantityOrdered`,(`od`.`priceEach` * `od`.`quantityOrdered`) AS `total_cost` from (`orders` `o` join `orderdetails` `od` on((`o`.`orderNumber` = `od`.`orderNumber`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `pending_orders`
--

/*!50001 DROP VIEW IF EXISTS `pending_orders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `pending_orders` AS select `o`.`orderNumber` AS `orderNumber`,`o`.`status` AS `status`,`o`.`orderDate` AS `orderDate`,`c`.`contactFirstName` AS `contactFirstName`,`c`.`contactLastName` AS `contactLastName` from (`orders` `o` join `customers` `c` on((`o`.`customerNumber` = `c`.`customerNumber`))) where (`o`.`status` <> 'Shipped') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `undelivered_orders`
--

/*!50001 DROP VIEW IF EXISTS `undelivered_orders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `undelivered_orders` AS select `o`.`orderNumber` AS `orderNumber`,`o`.`customerNumber` AS `customerNumber`,`o`.`orderDate` AS `orderDate`,`o`.`status` AS `status` from (`orders` `o` left join `deliveries` `d` on((`o`.`orderNumber` = `d`.`orderID`))) where ((`d`.`deliveryID` is null) or (`o`.`status` <> 'Shipped')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19  1:56:43
