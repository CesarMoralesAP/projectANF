-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: anfv3raul
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrador'),(2,'Gerente de Administración');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,2,1),(42,2,2),(43,2,4),(44,2,5),(45,2,6),(46,2,8),(47,2,9),(48,2,10),(49,2,12),(50,2,13),(51,2,14),(52,2,16),(53,2,17),(54,2,18),(55,2,20),(56,2,21),(57,2,22),(58,2,24),(59,2,25),(60,2,26),(61,2,28),(62,2,29),(63,2,30),(64,2,32),(65,2,33),(66,2,34),(67,2,36),(68,2,37),(69,2,38),(70,2,40);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Sector',7,'add_sector'),(26,'Can change Sector',7,'change_sector'),(27,'Can delete Sector',7,'delete_sector'),(28,'Can view Sector',7,'view_sector'),(29,'Can add Empresa',8,'add_empresa'),(30,'Can change Empresa',8,'change_empresa'),(31,'Can delete Empresa',8,'delete_empresa'),(32,'Can view Empresa',8,'view_empresa'),(33,'Can add Catálogo de Cuentas',9,'add_catalogocuenta'),(34,'Can change Catálogo de Cuentas',9,'change_catalogocuenta'),(35,'Can delete Catálogo de Cuentas',9,'delete_catalogocuenta'),(36,'Can view Catálogo de Cuentas',9,'view_catalogocuenta'),(37,'Can add Cuenta Contable',10,'add_cuentacontable'),(38,'Can change Cuenta Contable',10,'change_cuentacontable'),(39,'Can delete Cuenta Contable',10,'delete_cuentacontable'),(40,'Can view Cuenta Contable',10,'view_cuentacontable'),(41,'Can add Proyección Financiera',11,'add_proyeccionfinanciera'),(42,'Can change Proyección Financiera',11,'change_proyeccionfinanciera'),(43,'Can delete Proyección Financiera',11,'delete_proyeccionfinanciera'),(44,'Can view Proyección Financiera',11,'view_proyeccionfinanciera');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$94g8qEuU4Cc0q5QePXB7zE$jOkkT9VV44MYLTn3kCWDYH7duBU3Sd9EBwegASHlzXM=','2025-11-11 03:41:02.329096',1,'admin@sistema.com','Administrador','Sistema','admin@sistema.com',1,1,'2025-11-10 06:07:25.692879'),(2,'pbkdf2_sha256$1000000$yG2qSc7mlAKWctLXQAjTQT$RCAJKhn31HAU/wHYO3CF44QjjG1Y1g0O7JOK3oKTuZ0=','2025-11-11 03:40:32.759418',0,'usuario@sistema.com','Usuario','Demo','usuario@sistema.com',0,1,'2025-11-10 06:07:26.474962');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,1,1),(2,2,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalogo_cuenta`
--

DROP TABLE IF EXISTS `catalogo_cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_cuenta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `empresa_id` (`empresa_id`),
  CONSTRAINT `catalogo_cuenta_empresa_id_47eddd0d_fk_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalogo_cuenta`
--

LOCK TABLES `catalogo_cuenta` WRITE;
/*!40000 ALTER TABLE `catalogo_cuenta` DISABLE KEYS */;
INSERT INTO `catalogo_cuenta` VALUES (1,'2025-11-10 07:51:12.345566','2025-11-10 07:51:12.345587',1);
/*!40000 ALTER TABLE `catalogo_cuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuenta_contable`
--

DROP TABLE IF EXISTS `cuenta_contable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuenta_contable` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `catalogo_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cuenta_contable_catalogo_id_codigo_2eac3e51_uniq` (`catalogo_id`,`codigo`),
  CONSTRAINT `cuenta_contable_catalogo_id_d7fbdd1f_fk_catalogo_cuenta_id` FOREIGN KEY (`catalogo_id`) REFERENCES `catalogo_cuenta` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuenta_contable`
--

LOCK TABLES `cuenta_contable` WRITE;
/*!40000 ALTER TABLE `cuenta_contable` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuenta_contable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(11,'analisis','proyeccionfinanciera'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(9,'catalogos','catalogocuenta'),(10,'catalogos','cuentacontable'),(5,'contenttypes','contenttype'),(8,'empresas','empresa'),(7,'empresas','sector'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-10 06:05:38.868383'),(2,'auth','0001_initial','2025-11-10 06:05:39.493572'),(3,'admin','0001_initial','2025-11-10 06:05:39.646155'),(4,'admin','0002_logentry_remove_auto_add','2025-11-10 06:05:39.653725'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-10 06:05:39.661436'),(6,'contenttypes','0002_remove_content_type_name','2025-11-10 06:05:39.783842'),(7,'auth','0002_alter_permission_name_max_length','2025-11-10 06:05:39.849975'),(8,'auth','0003_alter_user_email_max_length','2025-11-10 06:05:39.873190'),(9,'auth','0004_alter_user_username_opts','2025-11-10 06:05:39.880590'),(10,'auth','0005_alter_user_last_login_null','2025-11-10 06:05:39.949382'),(11,'auth','0006_require_contenttypes_0002','2025-11-10 06:05:39.952483'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-10 06:05:39.959367'),(13,'auth','0008_alter_user_username_max_length','2025-11-10 06:05:40.030868'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-10 06:05:40.102597'),(15,'auth','0010_alter_group_name_max_length','2025-11-10 06:05:40.124150'),(16,'auth','0011_update_proxy_permissions','2025-11-10 06:05:40.131852'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-10 06:05:40.204109'),(18,'empresas','0001_initial','2025-11-10 06:05:40.296971'),(19,'catalogos','0001_initial','2025-11-10 06:05:40.487874'),(20,'sessions','0001_initial','2025-11-10 06:05:40.527519'),(21,'analisis','0001_initial','2025-11-10 21:14:57.748736');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dywavyfy7xrbyfj6tt6mpz9ptwri8yah','.eJxVjD0OwyAMhe_CXCGToBA6du8ZkMFOSVuBFJIp6t3rSBna6Xt-P95VwG3NYWu8hJnUVRl1-fUipheXI6AnlkfVqZZ1maM-KvpMm75X4vft7P49yNiyrO0QnUmUCKK3COAsTh2iQE4SinJx9ENPwEkIbEY2rmfXEfhJfb7wLTgA:1vIMsY:Ho1rVizMFwMPmrducdDrcmEeiKGUfMfoHf4mRI8IR4w','2025-11-11 08:03:58.195534'),('fztz9hvbhgpaagn5lp1pnwk7zstbzsgr','.eJxVjD0OwyAMhe_CXCGToBA6du8ZkMFOSVuBFJIp6t3rSBna6Xt-P95VwG3NYWu8hJnUVRl1-fUipheXI6AnlkfVqZZ1maM-KvpMm75X4vft7P49yNiyrO0QnUmUCKK3COAsTh2iQE4SinJx9ENPwEkIbEY2rmfXEfhJfb7wLTgA:1vIg1s:ic2pi_B92Oe7UYY1aPeFXSmp5c82HTFBRffKaC-aeOk','2025-11-12 04:30:52.059115');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `sector_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `empresa_sector_id_d3e136ad_fk_sector_id` (`sector_id`),
  CONSTRAINT `empresa_sector_id_d3e136ad_fk_sector_id` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresa`
--

LOCK TABLES `empresa` WRITE;
/*!40000 ALTER TABLE `empresa` DISABLE KEYS */;
INSERT INTO `empresa` VALUES (1,'2025-11-10 06:07:36.242650','2025-11-10 06:07:36.242670','Banco agrícola',1);
/*!40000 ALTER TABLE `empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proyeccion_financiera`
--

DROP TABLE IF EXISTS `proyeccion_financiera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proyeccion_financiera` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `origen` varchar(20) NOT NULL,
  `archivo` varchar(100) DEFAULT NULL,
  `datos_grafico` json DEFAULT NULL,
  `empresa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proyeccion_financiera_empresa_id_05bce411_fk_empresa_id` (`empresa_id`),
  CONSTRAINT `proyeccion_financiera_empresa_id_05bce411_fk_empresa_id` FOREIGN KEY (`empresa_id`) REFERENCES `empresa` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proyeccion_financiera`
--

LOCK TABLES `proyeccion_financiera` WRITE;
/*!40000 ALTER TABLE `proyeccion_financiera` DISABLE KEYS */;
INSERT INTO `proyeccion_financiera` VALUES (3,'2025-11-10 22:12:18.943936','2025-11-10 22:12:19.029132','prueba 2','3 metodos funcionando prueba','ARCHIVO','proyecciones/2025/11/plantilla_proyeccion_de_datos_3_metodos_fXby8Q4.xlsx','{\"valor_absoluto\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 377714.28571428574, 385428.5714285715, 393142.8571428572, 400857.14285714296, 408571.4285714287, 416285.7142857144, 424000.0000000002, 431714.2857142859, 439428.57142857165, 447142.8571428574, 454857.14285714313, 462571.42857142887], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}, \"minimos_cuadrados\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 374005.7, 380834.8000000001, 387663.9, 394493.0, 401322.1, 408151.2, 414980.3, 421809.4, 428638.5, 435467.6, 442296.7, 449125.8000000001], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}, \"valor_incremental\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 384973.8120478184, 400553.61070980807, 416763.9201201963, 433630.2568990931, 451179.1703181585, 469438.28409176593, 488436.3398594429, 508203.24242803646, 528770.1068448183, 550169.3073756269, 572434.5284651432, 595600.8177595177], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}}',1),(4,'2025-11-11 03:39:44.398891','2025-11-11 03:39:44.509222','prueba 3','asdasdasd','ARCHIVO','proyecciones/2025/11/plantilla_proyeccion_de_datos_3_metodos_Rw9QYnq.xlsx','{\"valor_absoluto\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 377714.28571428574, 385428.5714285715, 393142.8571428572, 400857.14285714296, 408571.4285714287, 416285.7142857144, 424000.0000000002, 431714.2857142859, 439428.57142857165, 447142.8571428574, 454857.14285714313, 462571.42857142887], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}, \"minimos_cuadrados\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 374005.7, 380834.8000000001, 387663.9, 394493.0, 401322.1, 408151.2, 414980.3, 421809.4, 428638.5, 435467.6, 442296.7, 449125.8000000001], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}, \"valor_incremental\": {\"valores\": [100000.0, 110000.0, 125000.0, 128000.0, 132000.0, 136000.0, 139000.0, 200000.0, 220000.0, 221000.0, 225000.0, 229000.0, 217000.0, 221000.0, 229000.0, 245000.0, 251000.0, 255000.0, 267000.0, 271000.0, 280000.0, 289000.0, 294000.0, 299000.0, 281000.0, 288000.0, 295000.0, 299000.0, 302000.0, 311000.0, 320000.0, 331000.0, 338000.0, 342000.0, 356000.0, 370000.0, 384973.8120478184, 400553.61070980807, 416763.9201201963, 433630.2568990931, 451179.1703181585, 469438.28409176593, 488436.3398594429, 508203.24242803646, 528770.1068448183, 550169.3073756269, 572434.5284651432, 595600.8177595177], \"periodos\": [\"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \"10\", \"11\", \"12\", \"13\", \"14\", \"15\", \"16\", \"17\", \"18\", \"19\", \"20\", \"21\", \"22\", \"23\", \"24\", \"25\", \"26\", \"27\", \"28\", \"29\", \"30\", \"31\", \"32\", \"33\", \"34\", \"35\", \"36\", \"37\", \"38\", \"39\", \"40\", \"41\", \"42\", \"43\", \"44\", \"45\", \"46\", \"47\", \"48\"], \"total_registros\": 48}}',1);
/*!40000 ALTER TABLE `proyeccion_financiera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sector`
--

DROP TABLE IF EXISTS `sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sector` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `creado_en` datetime(6) NOT NULL,
  `actualizado_en` datetime(6) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sector`
--

LOCK TABLES `sector` WRITE;
/*!40000 ALTER TABLE `sector` DISABLE KEYS */;
INSERT INTO `sector` VALUES (1,'2025-11-10 06:07:36.224557','2025-11-10 06:07:36.224590','Mineria'),(2,'2025-11-10 06:07:36.229335','2025-11-10 06:07:36.229352','Bancario'),(3,'2025-11-10 06:07:36.233530','2025-11-10 06:07:36.233551','Comercio'),(4,'2025-11-10 06:07:36.237379','2025-11-10 06:07:36.237399','Servicios');
/*!40000 ALTER TABLE `sector` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 22:34:28
