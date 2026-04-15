-- Learnify Database Schema
-- Run this file to create the database and all tables

CREATE DATABASE IF NOT EXISTS learnify
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE learnify;

-- ============================================
-- USERS
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    role ENUM('student', 'admin') NOT NULL DEFAULT 'student',
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB;

-- ============================================
-- CATEGORIES
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    slug VARCHAR(80) NOT NULL UNIQUE,
    icon VARCHAR(50) DEFAULT '📚'
) ENGINE=InnoDB;

-- ============================================
-- COURSES
-- ============================================
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    thumbnail VARCHAR(500) DEFAULT NULL,
    category_id INT,
    level ENUM('beginner', 'intermediate', 'advanced') NOT NULL DEFAULT 'beginner',
    status ENUM('draft', 'published') NOT NULL DEFAULT 'draft',
    admin_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_courses_category (category_id),
    INDEX idx_courses_status (status),
    INDEX idx_courses_level (level),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- SECTIONS
-- ============================================
CREATE TABLE IF NOT EXISTS sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    position INT NOT NULL DEFAULT 0,
    INDEX idx_sections_course (course_id),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- LESSONS
-- ============================================
CREATE TABLE IF NOT EXISTS lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    course_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    video_url VARCHAR(500) DEFAULT NULL,
    duration INT DEFAULT 0,
    position INT NOT NULL DEFAULT 0,
    INDEX idx_lessons_section (section_id),
    INDEX idx_lessons_course (course_id),
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- ENROLLMENTS
-- ============================================
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME DEFAULT NULL,
    UNIQUE KEY unique_enrollment (user_id, course_id),
    INDEX idx_enrollments_user (user_id),
    INDEX idx_enrollments_course (course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- LESSON PROGRESS
-- ============================================
CREATE TABLE IF NOT EXISTS lesson_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    lesson_id INT NOT NULL,
    course_id INT NOT NULL,
    completed TINYINT(1) NOT NULL DEFAULT 0,
    completed_at DATETIME DEFAULT NULL,
    UNIQUE KEY unique_progress (user_id, lesson_id),
    INDEX idx_progress_user_course (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- CERTIFICATES
-- ============================================
CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    issued_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cert_code VARCHAR(50) NOT NULL UNIQUE,
    UNIQUE KEY unique_cert (user_id, course_id),
    INDEX idx_cert_code (cert_code),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- SEED CATEGORIES
-- ============================================
INSERT IGNORE INTO categories (name, slug, icon) VALUES
('Web Development',  'web-development',  '🌐'),
('Python',           'python',           '🐍'),
('JavaScript',       'javascript',       '⚡'),
('Data Science',     'data-science',     '📊'),
('Mobile Dev',       'mobile-dev',       '📱'),
('DevOps',           'devops',           '🔧'),
('Databases',        'databases',        '🗄️'),
('UI/UX Design',     'ui-ux-design',     '🎨');

-- ============================================
-- DATABASE TRIGGERS
-- ============================================

DELIMITER //

-- 1) Trigger to auto-generate certificate code when a course is completed
CREATE TRIGGER after_enrollment_update
AFTER UPDATE ON enrollments
FOR EACH ROW
BEGIN
    -- If completed_at was just set to non-null
    IF NEW.completed_at IS NOT NULL AND OLD.completed_at IS NULL THEN
        -- Insert certificate if not exists
        INSERT IGNORE INTO certificates (user_id, course_id, cert_code)
        VALUES (
            NEW.user_id, 
            NEW.course_id, 
            CONCAT('CERT-', NEW.user_id, '-', NEW.course_id, '-', RIGHT(MD5(RAND()), 8))
        );
    END IF;
END //

-- 2) Update enrollment completion when all lessons are finished
CREATE TRIGGER after_lesson_progress_update
AFTER UPDATE ON lesson_progress
FOR EACH ROW
BEGIN
    DECLARE total_lessons INT DEFAULT 0;
    DECLARE completed_lessons INT DEFAULT 0;
    
    -- When a lesson is marked completed
    IF NEW.completed = 1 AND OLD.completed = 0 THEN
        -- Check total lessons
        SELECT COUNT(*) INTO total_lessons 
        FROM lessons 
        WHERE course_id = NEW.course_id;
        
        -- Check total completed by this user
        SELECT COUNT(*) INTO completed_lessons 
        FROM lesson_progress 
        WHERE course_id = NEW.course_id 
          AND user_id = NEW.user_id 
          AND completed = 1;
          
        -- If all are complete
        IF total_lessons > 0 AND total_lessons = completed_lessons THEN
            UPDATE enrollments 
            SET completed_at = CURRENT_TIMESTAMP 
            WHERE course_id = NEW.course_id 
              AND user_id = NEW.user_id 
              AND completed_at IS NULL;
        END IF;
    END IF;
END //

DELIMITER ;
