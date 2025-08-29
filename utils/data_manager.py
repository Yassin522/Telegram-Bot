"""
Data management utilities for the Telegram Bot
"""
import json
import os
from typing import Dict, Set


class DataManager:
    """Manages data files for the bot"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.insults_file = os.path.join(data_dir, "insults.txt")
        self.counter_file = os.path.join(data_dir, "insult_counter.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def load_insults(self) -> Set[str]:
        """Load insults from file"""
        try:
            with open(self.insults_file, 'r', encoding='utf-8') as file:
                return set(line.strip().lower() for line in file)
        except FileNotFoundError:
            return set()
    
    def save_insult(self, word: str) -> None:
        """Save new insult to file"""
        with open(self.insults_file, 'a', encoding='utf-8') as file:
            file.write(f'{word}\n')
    
    def load_counter(self) -> Dict[str, int]:
        """Load insult counter from file"""
        try:
            with open(self.counter_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_counter(self, counter: Dict[str, int]) -> None:
        """Save insult counter to file"""
        with open(self.counter_file, 'w', encoding='utf-8') as file:
            json.dump(counter, file, ensure_ascii=False, indent=2)
    
    def increment_counter(self, username: str) -> int:
        """Increment counter for a user and return current count"""
        counter = self.load_counter()
        counter[username] = counter.get(username, 0) + 1
        current_count = counter[username]
        self.save_counter(counter)
        return current_count
    
    def get_leaderboard(self) -> Dict[str, int]:
        """Get sorted leaderboard of insult counts"""
        counter = self.load_counter()
        return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
    
    def add_insult(self, word: str) -> bool:
        """Add a new insult word to the dataset"""
        insults = self.load_insults()
        
        if word in insults:
            return False  # Already exists
        
        self.save_insult(word)
        return True  # Successfully added
