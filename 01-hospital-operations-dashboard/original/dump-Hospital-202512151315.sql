-- MySQL dump 10.13  Distrib 9.5.0, for macos15 (arm64)
--
-- Host: localhost    Database: Hospital
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'acb82e3c-c956-11f0-927b-6e03c6d9ec11:1-982';

--
-- Table structure for table `Affiliated_With`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Affiliated_With` (
  `Physician` int NOT NULL,
  `Department` int NOT NULL,
  `PrimaryAffiliation` bit(1) NOT NULL,
  PRIMARY KEY (`Physician`,`Department`),
  KEY `fk_Affiliated_With_Department_DepartmentID` (`Department`),
  CONSTRAINT `fk_Affiliated_With_Department_DepartmentID` FOREIGN KEY (`Department`) REFERENCES `Department` (`DepartmentID`),
  CONSTRAINT `fk_Affiliated_With_Physician_EmployeeID` FOREIGN KEY (`Physician`) REFERENCES `Physician` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Appointment`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Appointment` (
  `AppointmentID` int NOT NULL,
  `Patient` int NOT NULL,
  `PrepNurse` int DEFAULT NULL,
  `Physician` int NOT NULL,
  `Starto` datetime NOT NULL,
  `Endo` datetime NOT NULL,
  `ExaminationRoom` text NOT NULL,
  PRIMARY KEY (`AppointmentID`),
  KEY `fk_Appointment_Patient_SSN` (`Patient`),
  KEY `fk_Appointment_Nurse_EmployeeID` (`PrepNurse`),
  KEY `fk_Appointment_Physician_EmployeeID` (`Physician`),
  CONSTRAINT `fk_Appointment_Nurse_EmployeeID` FOREIGN KEY (`PrepNurse`) REFERENCES `Nurse` (`EmployeeID`),
  CONSTRAINT `fk_Appointment_Patient_SSN` FOREIGN KEY (`Patient`) REFERENCES `Patient` (`SSN`),
  CONSTRAINT `fk_Appointment_Physician_EmployeeID` FOREIGN KEY (`Physician`) REFERENCES `Physician` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Department`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Department` (
  `DepartmentID` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Head` int NOT NULL,
  PRIMARY KEY (`DepartmentID`),
  KEY `fk_Department_Physician_EmployeeID` (`Head`),
  CONSTRAINT `fk_Department_Physician_EmployeeID` FOREIGN KEY (`Head`) REFERENCES `Physician` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Medication`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Medication` (
  `Code` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Brand` varchar(30) NOT NULL,
  `Description` varchar(30) NOT NULL,
  PRIMARY KEY (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Nurse`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Nurse` (
  `EmployeeID` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Position` varchar(30) NOT NULL,
  `Registered` bit(1) NOT NULL,
  `SSN` int NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Patient`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient` (
  `SSN` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Address` varchar(30) NOT NULL,
  `Phone` varchar(30) NOT NULL,
  `InsuranceID` int NOT NULL,
  `PCP` int NOT NULL,
  PRIMARY KEY (`SSN`),
  KEY `fk_Patient_Physician_EmployeeID` (`PCP`),
  CONSTRAINT `fk_Patient_Physician_EmployeeID` FOREIGN KEY (`PCP`) REFERENCES `Physician` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Physician`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Physician` (
  `EmployeeID` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Position` varchar(30) NOT NULL,
  `SSN` int NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Prescribes`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prescribes` (
  `Physician` int NOT NULL,
  `Patient` int NOT NULL,
  `Medication` int NOT NULL,
  `Date` datetime NOT NULL,
  `Appointment` int DEFAULT NULL,
  `Dose` varchar(30) NOT NULL,
  PRIMARY KEY (`Physician`,`Patient`,`Medication`,`Date`),
  KEY `fk_Prescribes_Patient_SSN` (`Patient`),
  KEY `fk_Prescribes_Medication_Code` (`Medication`),
  KEY `fk_Prescribes_Appointment_AppointmentID` (`Appointment`),
  CONSTRAINT `fk_Prescribes_Appointment_AppointmentID` FOREIGN KEY (`Appointment`) REFERENCES `Appointment` (`AppointmentID`),
  CONSTRAINT `fk_Prescribes_Medication_Code` FOREIGN KEY (`Medication`) REFERENCES `Medication` (`Code`),
  CONSTRAINT `fk_Prescribes_Patient_SSN` FOREIGN KEY (`Patient`) REFERENCES `Patient` (`SSN`),
  CONSTRAINT `fk_Prescribes_Physician_EmployeeID` FOREIGN KEY (`Physician`) REFERENCES `Physician` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Procedures`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Procedures` (
  `Code` int NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Cost` double NOT NULL,
  PRIMARY KEY (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Room`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Room` (
  `RoomNumber` int NOT NULL,
  `RoomType` varchar(30) NOT NULL,
  `BlockFloor` int NOT NULL,
  `BlockCode` int NOT NULL,
  `Unavailable` bit(1) NOT NULL,
  PRIMARY KEY (`RoomNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Stay`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stay` (
  `StayID` int NOT NULL,
  `Patient` int NOT NULL,
  `Room` int NOT NULL,
  `StayStart` datetime NOT NULL,
  `StayEnd` datetime NOT NULL,
  PRIMARY KEY (`StayID`),
  KEY `fk_Stay_Patient_SSN` (`Patient`),
  KEY `fk_Stay_Room_Number` (`Room`),
  CONSTRAINT `fk_Stay_Patient_SSN` FOREIGN KEY (`Patient`) REFERENCES `Patient` (`SSN`),
  CONSTRAINT `fk_Stay_Room_Number` FOREIGN KEY (`Room`) REFERENCES `Room` (`RoomNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Trained_In`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Trained_In` (
  `Physician` int NOT NULL,
  `Treatment` int NOT NULL,
  `CertificationDate` datetime NOT NULL,
  `CertificationExpires` datetime NOT NULL,
  PRIMARY KEY (`Physician`,`Treatment`),
  KEY `fk_Trained_In_Procedures_Code` (`Treatment`),
  CONSTRAINT `fk_Trained_In_Physician_EmployeeID` FOREIGN KEY (`Physician`) REFERENCES `Physician` (`EmployeeID`),
  CONSTRAINT `fk_Trained_In_Procedures_Code` FOREIGN KEY (`Treatment`) REFERENCES `Procedures` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Undergoes`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Undergoes` (
  `Patient` int NOT NULL,
  `Procedures` int NOT NULL,
  `Stay` int NOT NULL,
  `DateUndergoes` datetime NOT NULL,
  `Physician` int NOT NULL,
  `AssistingNurse` int DEFAULT NULL,
  PRIMARY KEY (`Patient`,`Procedures`,`Stay`,`DateUndergoes`),
  KEY `fk_Undergoes_Procedures_Code` (`Procedures`),
  KEY `fk_Undergoes_Stay_StayID` (`Stay`),
  KEY `fk_Undergoes_Physician_EmployeeID` (`Physician`),
  KEY `fk_Undergoes_Nurse_EmployeeID` (`AssistingNurse`),
  CONSTRAINT `fk_Undergoes_Nurse_EmployeeID` FOREIGN KEY (`AssistingNurse`) REFERENCES `Nurse` (`EmployeeID`),
  CONSTRAINT `fk_Undergoes_Patient_SSN` FOREIGN KEY (`Patient`) REFERENCES `Patient` (`SSN`),
  CONSTRAINT `fk_Undergoes_Physician_EmployeeID` FOREIGN KEY (`Physician`) REFERENCES `Physician` (`EmployeeID`),
  CONSTRAINT `fk_Undergoes_Procedures_Code` FOREIGN KEY (`Procedures`) REFERENCES `Procedures` (`Code`),
  CONSTRAINT `fk_Undergoes_Stay_StayID` FOREIGN KEY (`Stay`) REFERENCES `Stay` (`StayID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'Hospital'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-15 13:15:43
