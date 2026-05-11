from typing import List, Tuple

from src.providers import load_config
from src.repo import QuestionBank
from src.types import Question, QuizResult, QuizConfig


class QuizService:
    def present_question(self, question: Question) -> str:
        return question.correct_answer

    def validate_answer(self, question: Question, user_answer: str) -> bool:
        return user_answer.strip().lower() == question.correct_answer.strip().lower()

    def calculate_score(self, answers: List[Tuple[Question, str]]) -> QuizResult:
        total_points = sum(q.points for q, _ in answers)
        score = sum(q.points for q, a in answers if self.validate_answer(q, a))
        correct_count = sum(1 for q, a in answers if self.validate_answer(q, a))
        return QuizResult(score=score, total_points=total_points, correct_count=correct_count, answers=answers)

    def validate_answer(self, question: Question, user_answer: str) -> bool:
        pass

    def calculate_score(self, answers: List[Tuple[Question, str]]) -> QuizResult:
        pass
