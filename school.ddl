CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    class_name VARCHAR(5) NOT NULL,
    age INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS students_marks (
    id UUID PRIMARY KEY,
    student_id UUID NOT NULL,
    subject TEXT NOT NULL,
    mark INTEGER NOT NULL DEFAULT 5,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT fk_student_id
        FOREIGN KEY (student_id)
        REFERENCES students (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS students_name_idx ON students (name);
CREATE INDEX IF NOT EXISTS students_marks_student_id_idx ON students_marks (student_id);