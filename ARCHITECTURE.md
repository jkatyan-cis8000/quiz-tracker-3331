# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- `src/types/__init__.py`: Pure type definitions for domain models
- `src/config/__init__.py`: Configuration loading and default values
- `src/repo/__init__.py`: Question bank persistence (file-based)
- `src/service/__init__.py`: Quiz business logic (scoring, validation, flow)
- `src/ui/__init__.py`: CLI user interface
- `src/runtime/__init__.py`: Main entry point, orchestration
- `src/providers/__init__.py`: Cross-cutting concerns (config loading helper)
- `src/utils/__init__.py`: Pure helper functions (no internal imports)

## Interfaces

### Types
- `QuestionType`: Enum (`MULTIPLE_CHOICE`, `SHORT_ANSWER`)
- `Question`: dataclass with `id`, `text`, `type`, `options` (list), `correct_answer`, `points`
- `QuizConfig`: dataclass with `show_answers_after`, `question_bank_path`
- `QuizResult`: dataclass with `score`, `total_points`, `correct_count`, `answers` (list of user answers)

### Config
- `load_config(path: str) -> QuizConfig`: Load configuration from YAML/JSON

### Repo
- `QuestionBank`: class with `load_questions(path: str) -> list[Question]`, `save_questions(path: str, questions: list[Question])`

### Service
- `QuizService`: class with
  - `present_question(question: Question) -> str`: display and get answer
  - `validate_answer(question: Question, user_answer: str) -> bool`: compare answers
  - `calculate_score(answers: list[Tuple[Question, str]]) -> QuizResult`

### UI
- `QuizUI`: class with
  - `display_question(question: Question) -> None`
  - `get_user_answer(question: Question) -> str`
  - `display_result(result: QuizResult, show_answers: bool) -> None`
  - `display_question_with_correct(question: Question, user_answer: str, is_correct: bool) -> None`

### Runtime
- `main()`: entry point, orchestrates config -> repo -> service -> ui flow

## Shared Data Structures

```python
# QuestionType enum
class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"

# Question dataclass
@dataclass
class Question:
    id: str
    text: str
    type: QuestionType
    options: list[str]  # Only for multiple_choice
    correct_answer: str
    points: int

# QuizConfig dataclass
@dataclass
class QuizConfig:
    show_answers_after: bool
    question_bank_path: str

# QuizResult dataclass
@dataclass
class QuizResult:
    score: int
    total_points: int
    correct_count: int
    answers: list[tuple[Question, str]]  # (question, user_answer)
```

## External Dependencies

- `PyYAML`: For configuration file parsing (if using YAML format)
