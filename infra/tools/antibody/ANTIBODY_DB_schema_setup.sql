-- MySQL Script generated by MySQL Workbench
-- Fri 10 Jul 2015 09:49:23 AM PDT
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema _DB_NAME
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema _DB_NAME
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `_DB_NAME` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `_DB_NAME` ;

-- -----------------------------------------------------
-- Table `_DB_NAME`.`project`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`project` (
  `prj_id` INT NOT NULL COMMENT '',
  `prj_name` VARCHAR(45) NULL COMMENT '',
  `prj_repository` VARCHAR(250) NOT NULL COMMENT '',
  PRIMARY KEY (`prj_id`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `_DB_NAME`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`review` (
  `review_url` VARCHAR(200) NOT NULL COMMENT '',
  `request_timestamp` TIMESTAMP NULL COMMENT '',
  `patchset_commited` TIMESTAMP NULL COMMENT '',
  `patchset_still_exists` TINYINT NULL COMMENT '',
  `reverted` TINYINT NULL COMMENT '',
  `project_prj_id` INT NULL COMMENT '',
  PRIMARY KEY (`review_url`)  COMMENT '');


-- -----------------------------------------------------
-- Table `_DB_NAME`.`people`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`people` (
  `email_address` VARCHAR(200) NOT NULL COMMENT '',
  `commiter_since` TIMESTAMP NULL COMMENT '',
  PRIMARY KEY (`email_address`)  COMMENT '');


-- -----------------------------------------------------
-- Table `_DB_NAME`.`git_commit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`git_commit` (
  `hash` VARCHAR(40) NOT NULL COMMENT '',
  `bug_url` VARCHAR(200) NULL COMMENT '',
  `timestamp` TIMESTAMP NULL COMMENT '',
  `review_url` VARCHAR(200) NULL COMMENT '',
  `project_prj_id` INT NULL COMMENT '',
  `subject` VARCHAR(500) NULL COMMENT '',
  PRIMARY KEY (`hash`)  COMMENT '');


-- -----------------------------------------------------
-- Table `_DB_NAME`.`commit_people`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`commit_people` (
  `people_email_address` VARCHAR(200) NOT NULL COMMENT '',
  `git_commit_hash` VARCHAR(40) NOT NULL COMMENT '',
  `request_timestamp` TIMESTAMP NULL COMMENT '',
  `type` VARCHAR(10) NOT NULL COMMENT '',
  PRIMARY KEY (`people_email_address`, `git_commit_hash`, `type`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `_DB_NAME`.`review_people`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `_DB_NAME`.`review_people` (
  `people_email_address` VARCHAR(200) NOT NULL COMMENT '',
  `review_url` VARCHAR(200) NOT NULL COMMENT '',
  `timestamp` TIMESTAMP NULL COMMENT '',
  `request_timestamp` TIMESTAMP NULL COMMENT '',
  `type` VARCHAR(10) NOT NULL COMMENT '',
  PRIMARY KEY (`people_email_address`, `review_url`, `type`)  COMMENT '')
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;