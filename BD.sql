CREATE DATABASE  IF NOT EXISTS `estoque` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `estoque`;
-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: estoque
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.2

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
-- Table structure for table `ficha_tecnica_insumo`
--

DROP TABLE IF EXISTS `ficha_tecnica_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ficha_tecnica_insumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_ficha_tecnica` int NOT NULL,
  `id_insumo` int NOT NULL,
  `quantidade` decimal(9,3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_ficha_tecnica_insumo_ficha_tecnica_idx` (`id_ficha_tecnica`),
  KEY `fk_ficha_tecnica_insumo_insumo_idx` (`id_insumo`),
  CONSTRAINT `fk_ficha_tecnica_insumo_ficha_tecnica` FOREIGN KEY (`id_ficha_tecnica`) REFERENCES `fichas_tecnicas` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ficha_tecnica_insumo_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ficha_tecnica_insumo`
--

LOCK TABLES `ficha_tecnica_insumo` WRITE;
/*!40000 ALTER TABLE `ficha_tecnica_insumo` DISABLE KEYS */;
/*!40000 ALTER TABLE `ficha_tecnica_insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ficha_tecnica_pedido`
--

DROP TABLE IF EXISTS `ficha_tecnica_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ficha_tecnica_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_ficha_tecnica` int NOT NULL,
  `id_pedido` int NOT NULL,
  `valor_unitario` decimal(11,2) NOT NULL,
  `quantidade` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_ficha_tecnica_pedido_fichas_tecnicas_idx` (`id_ficha_tecnica`),
  KEY `fk_ficha_tecnica_pedido_pedidos_idx` (`id_pedido`),
  CONSTRAINT `fk_ficha_tecnica_pedido_fichas_tecnicas` FOREIGN KEY (`id_ficha_tecnica`) REFERENCES `fichas_tecnicas` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ficha_tecnica_pedido_pedidos` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ficha_tecnica_pedido`
--

LOCK TABLES `ficha_tecnica_pedido` WRITE;
/*!40000 ALTER TABLE `ficha_tecnica_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `ficha_tecnica_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fichas_tecnicas`
--

DROP TABLE IF EXISTS `fichas_tecnicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fichas_tecnicas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `valor` decimal(11,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fichas_tecnicas`
--

LOCK TABLES `fichas_tecnicas` WRITE;
/*!40000 ALTER TABLE `fichas_tecnicas` DISABLE KEYS */;
/*!40000 ALTER TABLE `fichas_tecnicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `quantidade` decimal(12,3) NOT NULL,
  `unidade_medida` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_insumos_UNIQUE` (`id`),
  UNIQUE KEY `nome_UNIQUE` (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notas_fiscais`
--

DROP TABLE IF EXISTS `notas_fiscais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notas_fiscais` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nfce` varchar(9) NOT NULL,
  `serie` varchar(3) NOT NULL,
  `data_emissao` date NOT NULL,
  `cnpj_fornecedor` char(18) NOT NULL,
  `nome_fornecedor` varchar(100) NOT NULL,
  `valor` decimal(11,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_notas_fiscais_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notas_fiscais`
--

LOCK TABLES `notas_fiscais` WRITE;
/*!40000 ALTER TABLE `notas_fiscais` DISABLE KEYS */;
/*!40000 ALTER TABLE `notas_fiscais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `data` date NOT NULL,
  `telefone` varchar(11) NOT NULL,
  `valor` decimal(11,2) NOT NULL,
  `observacoes` text,
  `cpf_cnpj` varchar(18) DEFAULT NULL,
  `cep` char(9) DEFAULT NULL,
  `unidade_federal` char(2) DEFAULT NULL,
  `cidade` varchar(60) DEFAULT NULL,
  `bairro` varchar(60) DEFAULT NULL,
  `rua` varchar(100) DEFAULT NULL,
  `numero` varchar(5) DEFAULT NULL,
  `complemento` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos_customizacao`
--

DROP TABLE IF EXISTS `pedidos_customizacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_customizacao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_item_pedido` int NOT NULL,
  `id_insumo_removido` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cust_insumo` (`id_insumo_removido`),
  KEY `fk_cust_item` (`id_item_pedido`),
  CONSTRAINT `fk_cust_insumo` FOREIGN KEY (`id_insumo_removido`) REFERENCES `insumos` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_cust_item` FOREIGN KEY (`id_item_pedido`) REFERENCES `ficha_tecnica_pedido` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_customizacao`
--

LOCK TABLES `pedidos_customizacao` WRITE;
/*!40000 ALTER TABLE `pedidos_customizacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos_customizacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro_compras`
--

DROP TABLE IF EXISTS `registro_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `id_nota_fiscal` int NOT NULL,
  `quantidade` decimal(12,3) NOT NULL,
  `valor` decimal(11,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_registro_compras_insumos_idx` (`id_insumo`),
  KEY `fk_registro_compras_notas_fiscais_idx` (`id_nota_fiscal`),
  CONSTRAINT `fk_registro_compras_insumos` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_registro_compras_notas_fiscais` FOREIGN KEY (`id_nota_fiscal`) REFERENCES `notas_fiscais` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_compras`
--

LOCK TABLES `registro_compras` WRITE;
/*!40000 ALTER TABLE `registro_compras` DISABLE KEYS */;
/*!40000 ALTER TABLE `registro_compras` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-10  2:26:47
