import enum


class QuestionType(str, enum.Enum):
    text = "text"
    single = "single"
    multiple = "multiple"


class Role(str, enum.Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"


class CourseStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
