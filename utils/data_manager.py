"""
Data management utilities for the Telegram Bot
"""
import json
import os
import re
from typing import Dict, Set, List


class DataManager:
    """Manages data files for the bot"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.insults_file = os.path.join(data_dir, "insults.txt")
        self.counter_file = os.path.join(data_dir, "insult_counter.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Cache insults for better performance
        self._insults_cache = None
        self._cache_dirty = True
    
    def load_insults(self) -> Set[str]:
        """Load insults from file with caching"""
        if self._insults_cache is None or self._cache_dirty:
            try:
                with open(self.insults_file, 'r', encoding='utf-8') as file:
                    insults = set()
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):  # Skip empty lines and comments
                            insults.add(line.lower())
                    self._insults_cache = insults
                    self._cache_dirty = False
            except FileNotFoundError:
                self._insults_cache = set()
                self._cache_dirty = False
            except Exception as e:
                print(f"Error loading insults: {e}")
                self._insults_cache = set()
                self._cache_dirty = False
        
        return self._insults_cache
    
    def save_insult(self, word: str) -> None:
        """Save new insult to file"""
        try:
            with open(self.insults_file, 'a', encoding='utf-8') as file:
                file.write(f'{word}\n')
            self._cache_dirty = True  # Mark cache as dirty
        except Exception as e:
            print(f"Error saving insult: {e}")
    
    def load_counter(self) -> Dict[str, int]:
        """Load insult counter from file"""
        try:
            with open(self.counter_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading counter: {e}")
            return {}
    
    def save_counter(self, counter: Dict[str, int]) -> None:
        """Save insult counter to file"""
        try:
            with open(self.counter_file, 'w', encoding='utf-8') as file:
                json.dump(counter, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving counter: {e}")
    
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
    
    def remove_insult(self, word: str) -> bool:
        """Remove an insult word from the dataset"""
        insults = self.load_insults()
        
        if word not in insults:
            return False  # Doesn't exist
        
        try:
            # Read all lines and filter out the word to remove
            with open(self.insults_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Filter out the word (case-insensitive)
            filtered_lines = [line for line in lines if line.strip().lower() != word.lower()]
            
            # Write back the filtered content
            with open(self.insults_file, 'w', encoding='utf-8') as file:
                file.writelines(filtered_lines)
            
            self._cache_dirty = True  # Mark cache as dirty
            return True
        except Exception as e:
            print(f"Error removing insult: {e}")
            return False
    
    def search_insults(self, query: str) -> List[str]:
        """Search for insults containing the query"""
        insults = self.load_insults()
        query = query.lower()
        return [insult for insult in insults if query in insult]
    
    def get_insult_stats(self) -> Dict[str, int]:
        """Get statistics about the insults dataset"""
        insults = self.load_insults()
        return {
            'total_insults': len(insults),
            'short_insults': len([i for i in insults if len(i) <= 3]),
            'medium_insults': len([i for i in insults if 3 < len(i) <= 6]),
            'long_insults': len([i for i in insults if len(i) > 6])
        }
    
    def validate_insult_file(self) -> Dict[str, List[str]]:
        """Validate the insults file and report issues"""
        issues = {
            'duplicates': [],
            'empty_lines': [],
            'invalid_encoding': []
        }
        
        try:
            with open(self.insults_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            seen = set()
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    issues['empty_lines'].append(f"Line {i}")
                elif line.lower() in seen:
                    issues['duplicates'].append(f"Line {i}: {line}")
                else:
                    seen.add(line.lower())
                    
        except UnicodeDecodeError:
            issues['invalid_encoding'].append("File contains invalid UTF-8 characters")
        except Exception as e:
            issues['invalid_encoding'].append(f"Error reading file: {e}")
        
        return issues
