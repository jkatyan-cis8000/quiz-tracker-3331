import json
import yaml
from pathlib import Path

from types import QuizConfig


def load_config(path: str) -> QuizConfig:
    """Load configuration from YAML or JSON file."""
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(file_path, 'r') as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            config_data = yaml.safe_load(f)
        else:
            config_data = json.load(f)
    
    return QuizConfig(
        show_answers_after=config_data.get('show_answers_after', False),
        question_bank_path=config_data.get('question_bank_path', 'questions.json')
    )
