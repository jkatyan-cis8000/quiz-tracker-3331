from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"


@dataclass
class Question:
    id: str
    text: str
    type: QuestionType
    options: list[str]
    correct_answer: str
    points: int


@dataclass
class QuizConfig:
    show_answers_after: bool
    question_bank_path: str


@dataclass
class QuizResult:
    score: int
    total_points: int
    correct_count: int
    answers: list[tuple[Question, str]]
