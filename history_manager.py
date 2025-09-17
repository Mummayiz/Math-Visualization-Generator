import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import Config

class HistoryManager:
    """Manages the history of math problems and solutions"""
    
    def __init__(self):
        self.history_file = os.path.join(Config.OUTPUT_FOLDER, 'history.json')
        self.ensure_history_file()
    
    def ensure_history_file(self):
        """Create history file if it doesn't exist"""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def save_question(self, image_filename: str, extracted_text: str, 
                     problem_info: Dict[str, Any], solution: Dict[str, Any], 
                     video_filename: str) -> str:
        """Save a question and its solution to history"""
        try:
            # Load existing history
            history = self.load_history()
            
            # Create new entry
            entry = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'image_filename': image_filename,
                'extracted_text': extracted_text,
                'problem_info': problem_info,
                'solution': solution,
                'video_filename': video_filename,
                'problem_type': problem_info.get('problem_type', 'unknown'),
                'complexity': problem_info.get('complexity', 'unknown'),
                'final_answer': solution.get('final_answer', 'No answer available')
            }
            
            # Add to beginning of list (most recent first)
            history.insert(0, entry)
            
            # Save back to file
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return entry['id']
            
        except Exception as e:
            print(f"Error saving question to history: {e}")
            return None
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load all history entries"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific question by ID"""
        history = self.load_history()
        for entry in history:
            if entry['id'] == question_id:
                return entry
        return None
    
    def delete_question(self, question_id: str) -> bool:
        """Delete a question from history"""
        try:
            history = self.load_history()
            history = [entry for entry in history if entry['id'] != question_id]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error deleting question: {e}")
            return False
    
    def clear_history(self) -> bool:
        """Clear all history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def get_recent_questions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent questions (already sorted by most recent first)"""
        history = self.load_history()
        return history[:limit]
    
    def search_questions(self, query: str) -> List[Dict[str, Any]]:
        """Search questions by text content"""
        history = self.load_history()
        query_lower = query.lower()
        
        results = []
        for entry in history:
            if (query_lower in entry.get('extracted_text', '').lower() or
                query_lower in entry.get('problem_type', '').lower() or
                query_lower in entry.get('final_answer', '').lower()):
                results.append(entry)
        
        return results

