-- -- SQLite
-- -- Create the Users table
-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL UNIQUE,
--     password_hash TEXT NOT NULL,
--     role TEXT CHECK(role IN ('Student', 'Professor', 'Admin')) NOT NULL
-- );

-- -- Create the Courses table
-- CREATE TABLE courses (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     course_name TEXT NOT NULL,
--     professor_id INTEGER,
--     FOREIGN KEY (professor_id) REFERENCES users(id) ON DELETE SET NULL
-- );

-- -- Create the Grades table
-- CREATE TABLE grades (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     student_id INTEGER NOT NULL,
--     course_id INTEGER NOT NULL,
--     grade TEXT CHECK(grade IN ('A', 'B', 'C', 'D', 'F', 'Incomplete')),
--     FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
--     FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
-- );

-- -- Create the Enrollments table (optional, if needed)
-- CREATE TABLE enrollments (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     student_id INTEGER NOT NULL,
--     course_id INTEGER NOT NULL,
--     FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
--     FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
-- );

INSERT INTO users (username, password_hash, role) VALUES ('admin', 'admin', 'Admin')
-- SELECT * FROM users;