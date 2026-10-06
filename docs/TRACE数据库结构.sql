-- TRACE V2.0 一期数据库设计基线。表按业务需求划分，无表数量上限。
-- 仅面向新建专用数据库；转换为Alembic迁移后在MySQL验证。
-- MySQL 8.0.16及以上兼容环境，BIGINT ID由API以字符串返回。
-- 不含DROP、演示账号密码和二期预测/帮扶/辅导员表。
-- 时间戳UTC，applied_on为本地业务日期。JSON结构与跨用户归属由服务层校验。
-- 该文件已做静态结构检查，尚未声称在MySQL执行通过。
SET NAMES utf8mb4;
SET time_zone = '+00:00';

CREATE TABLE users (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(16) NOT NULL DEFAULT 'student',
  token_version INT NOT NULL DEFAULT 1,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(username),
  CHECK(role IN ('student','admin'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE student_profiles (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  nickname VARCHAR(64) NOT NULL,
  education VARCHAR(16),
  target_category VARCHAR(16),
  preferred_cities_json JSON,
  version INT NOT NULL DEFAULT 1,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  CHECK(education IS NULL OR education IN ('college','bachelor','master')),
  CHECK(target_category IS NULL OR target_category IN ('python','frontend','data'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE jobs (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(64) NOT NULL,
  title VARCHAR(150) NOT NULL,
  company VARCHAR(150) NOT NULL,
  category VARCHAR(16) NOT NULL,
  city VARCHAR(64) NOT NULL,
  education VARCHAR(16) NOT NULL,
  job_type VARCHAR(16) NOT NULL,
  salary_min INT,
  salary_max INT,
  required_skills_json JSON NOT NULL,
  description TEXT NOT NULL,
  source_type VARCHAR(16) NOT NULL DEFAULT 'synthetic',
  source_url VARCHAR(1000),
  dataset_version VARCHAR(32) NOT NULL,
  content_hash CHAR(64) NOT NULL,
  jd_version INT NOT NULL DEFAULT 1,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(code),
  INDEX ix_jobs_filter(category,city,is_active),
  CHECK(category IN ('python','frontend','data')),
  CHECK(job_type IN ('internship','full_time')),
  CHECK(salary_min IS NULL OR salary_min>=0),
  CHECK(salary_max IS NULL OR salary_max>=0),
  CHECK(salary_min IS NULL OR salary_max IS NULL OR salary_min<=salary_max)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_chunks (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_id BIGINT NOT NULL,
  jd_version INT NOT NULL,
  chunk_no INT NOT NULL,
  content TEXT NOT NULL,
  content_hash CHAR(64) NOT NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(job_id,jd_version,chunk_no),
  FOREIGN KEY(job_id) REFERENCES jobs(id),
  CHECK(chunk_no>=0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE diagnosis_records (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  client_request_id VARCHAR(64) NOT NULL,
  input_hash CHAR(64) NOT NULL,
  template_version VARCHAR(32) NOT NULL,
  rule_version VARCHAR(32) NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'draft',
  answers_json JSON NOT NULL,
  result_json JSON,
  version INT NOT NULL DEFAULT 1,
  completed_at DATETIME(6),
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id,client_request_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  INDEX ix_diagnosis_history(user_id,status,created_at),
  CHECK(status IN ('draft','completed')),
  CHECK(status<>'completed' OR (result_json IS NOT NULL AND completed_at IS NOT NULL))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE recommendation_records (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  diagnosis_id BIGINT NOT NULL,
  client_request_id VARCHAR(64) NOT NULL,
  input_hash CHAR(64) NOT NULL,
  index_version VARCHAR(64) NOT NULL,
  rule_version VARCHAR(32) NOT NULL,
  query_snapshot_json JSON NOT NULL,
  items_json JSON NOT NULL,
  reason_status VARCHAR(16) NOT NULL DEFAULT 'pending',
  reason_error_code VARCHAR(64),
  reason_started_at DATETIME(6),
  reason_attempts INT NOT NULL DEFAULT 0,
  version INT NOT NULL DEFAULT 1,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id,client_request_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(diagnosis_id) REFERENCES diagnosis_records(id),
  INDEX ix_recommendation_history(user_id,created_at),
  CHECK(reason_status IN ('pending','running','ai_ready','fallback')),
  CHECK(reason_attempts BETWEEN 0 AND 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE interview_questions (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(64) NOT NULL,
  category VARCHAR(16) NOT NULL,
  difficulty TINYINT NOT NULL,
  prompt TEXT NOT NULL,
  reference_answer TEXT NOT NULL,
  rubric_json JSON NOT NULL,
  question_version VARCHAR(32) NOT NULL,
  dataset_version VARCHAR(32) NOT NULL,
  content_hash CHAR(64) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(code),
  INDEX ix_question_selection(category,difficulty,is_active),
  CHECK(category IN ('python','frontend','data')),
  CHECK(difficulty BETWEEN 1 AND 3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE interview_sessions (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  client_request_id VARCHAR(64) NOT NULL,
  input_hash CHAR(64) NOT NULL,
  category VARCHAR(16) NOT NULL,
  selection_seed VARCHAR(64) NOT NULL,
  rule_version VARCHAR(32) NOT NULL,
  rules_snapshot_json JSON NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'answering',
  score_started_at DATETIME(6),
  score_attempts INT NOT NULL DEFAULT 0,
  total_score DECIMAL(5,1),
  report_mode VARCHAR(16),
  report_json JSON,
  error_code VARCHAR(64),
  version INT NOT NULL DEFAULT 1,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id,client_request_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  INDEX ix_interview_history(user_id,created_at),
  CHECK(status IN ('answering','scoring','completed','failed')),
  CHECK(total_score IS NULL OR total_score BETWEEN 0 AND 100),
  CHECK(score_attempts BETWEEN 0 AND 2),
  CHECK(report_mode IS NULL OR report_mode IN ('ai','all_skipped','mock')),
  CHECK(status<>'completed' OR (report_json IS NOT NULL AND total_score IS NOT NULL))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE interview_answers (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  session_id BIGINT NOT NULL,
  question_id BIGINT NOT NULL,
  turn_no TINYINT NOT NULL,
  question_snapshot_json JSON NOT NULL,
  answer_text TEXT,
  skipped BOOLEAN NOT NULL DEFAULT FALSE,
  submitted_at DATETIME(6),
  score DECIMAL(5,1),
  feedback_json JSON,
  version INT NOT NULL DEFAULT 1,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(session_id,turn_no),
  UNIQUE(session_id,question_id),
  FOREIGN KEY(session_id) REFERENCES interview_sessions(id),
  FOREIGN KEY(question_id) REFERENCES interview_questions(id),
  CHECK(turn_no BETWEEN 1 AND 5),
  CHECK(score IS NULL OR score BETWEEN 0 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_favorites (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  job_id BIGINT NOT NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id,job_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(job_id) REFERENCES jobs(id),
  INDEX ix_favorite_history(user_id,created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE job_applications (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  job_id BIGINT NOT NULL,
  job_snapshot_json JSON NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'submitted',
  applied_on DATE NOT NULL,
  note VARCHAR(1000) NOT NULL DEFAULT '',
  source_type VARCHAR(16) NOT NULL DEFAULT 'self_reported',
  version INT NOT NULL DEFAULT 1,
  is_demo BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(user_id,job_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(job_id) REFERENCES jobs(id),
  INDEX ix_application_history(user_id,status,applied_on),
  CHECK(status IN ('submitted','interviewing','offer','rejected','withdrawn')),
  CHECK(source_type='self_reported')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ai_call_logs (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  business_type VARCHAR(32) NOT NULL,
  business_id BIGINT NOT NULL,
  attempt_no TINYINT NOT NULL,
  request_key VARCHAR(128) NOT NULL,
  provider VARCHAR(64) NOT NULL,
  model_id VARCHAR(128) NOT NULL,
  prompt_version VARCHAR(32) NOT NULL,
  input_hash CHAR(64) NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'running',
  provider_request_id VARCHAR(191),
  input_tokens INT,
  output_tokens INT,
  reserved_cny DECIMAL(12,6) NOT NULL,
  charged_cny DECIMAL(12,6),
  duration_ms INT,
  error_code VARCHAR(64),
  finished_at DATETIME(6),
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  UNIQUE(business_type,business_id,attempt_no),
  UNIQUE(request_key),
  FOREIGN KEY(user_id) REFERENCES users(id),
  INDEX ix_call_quota(user_id,business_type,created_at),
  INDEX ix_call_budget(status,created_at),
  CHECK(business_type IN ('recommendation','interview')),
  CHECK(status IN ('running','succeeded','failed','unknown')),
  CHECK(attempt_no BETWEEN 1 AND 2),
  CHECK(reserved_cny>=0),
  CHECK(charged_cny IS NULL OR charged_cny>=0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
