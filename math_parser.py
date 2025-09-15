import re
import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, expand, factor
from typing import Dict, List, Tuple, Optional, Any
import ast

class MathParser:
    """Parses and analyzes mathematical expressions and problems"""
    
    def __init__(self):
        self.common_variables = ['x', 'y', 'z', 't', 'a', 'b', 'c', 'n', 'm']
        self.operators = ['+', '-', '*', '/', '^', '**', '=', '<', '>', '<=', '>=']
        
    def parse_problem(self, text: str) -> Dict[str, Any]:
        """Parse a mathematical problem and extract key information"""
        problem_info = {
            'original_text': text,
            'problem_type': None,
            'variables': [],
            'expressions': [],
            'equations': [],
            'instructions': [],
            'complexity': 'basic'
        }
        
        # Clean and normalize text
        cleaned_text = self._clean_text(text)
        
        # Extract variables
        problem_info['variables'] = self._extract_variables(cleaned_text)
        
        # Extract mathematical expressions
        problem_info['expressions'] = self._extract_expressions(cleaned_text)
        
        # Extract equations
        problem_info['equations'] = self._extract_equations(cleaned_text)
        
        # Extract instructions
        problem_info['instructions'] = self._extract_instructions(cleaned_text)
        
        # Classify problem type
        problem_info['problem_type'] = self._classify_problem_type(cleaned_text)
        
        # Assess complexity
        problem_info['complexity'] = self._assess_complexity(problem_info)
        
        return problem_info
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize mathematical text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Replace common math symbols
        replacements = {
            '×': '*',
            '÷': '/',
            '²': '**2',
            '³': '**3',
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'infinity',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '±': '+-'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def _extract_variables(self, text: str) -> List[str]:
        """Extract mathematical variables from text"""
        # Pattern to find single letter variables
        variable_pattern = r'\b[a-zA-Z]\b'
        variables = re.findall(variable_pattern, text)
        
        # Filter out common words that aren't variables
        non_variables = {'and', 'or', 'the', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with'}
        variables = [v for v in variables if v.lower() not in non_variables]
        
        return list(set(variables))
    
    def _extract_expressions(self, text: str) -> List[str]:
        """Extract mathematical expressions from text"""
        # Pattern to find mathematical expressions
        # This is a simplified pattern - in practice, you'd want more sophisticated parsing
        expr_pattern = r'[0-9+\-*/^()xXyYzZaAbBcC]+\s*[+\-*/=]\s*[0-9+\-*/^()xXyYzZaAbBcC]+'
        expressions = re.findall(expr_pattern, text)
        
        return expressions
    
    def _extract_equations(self, text: str) -> List[str]:
        """Extract equations from text"""
        # Split by common equation indicators
        equation_indicators = ['=', 'equals', 'is equal to', '=']
        equations = []
        
        for indicator in equation_indicators:
            if indicator in text:
                parts = text.split(indicator)
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    if left and right:
                        equations.append(f"{left} = {right}")
        
        return equations
    
    def _extract_instructions(self, text: str) -> List[str]:
        """Extract problem-solving instructions"""
        instruction_keywords = [
            'solve', 'find', 'calculate', 'compute', 'evaluate',
            'simplify', 'expand', 'factor', 'differentiate', 'integrate',
            'graph', 'plot', 'sketch', 'draw'
        ]
        
        instructions = []
        sentences = re.split(r'[.!?]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in instruction_keywords):
                instructions.append(sentence)
        
        return instructions
    
    def _classify_problem_type(self, text: str) -> str:
        """Classify the type of mathematical problem"""
        text_lower = text.lower()
        
        # Algebra
        if any(keyword in text_lower for keyword in ['solve', 'equation', 'variable', 'unknown']):
            if any(keyword in text_lower for keyword in ['quadratic', 'x²', 'x^2']):
                return 'quadratic_equation'
            elif any(keyword in text_lower for keyword in ['linear', 'slope', 'intercept']):
                return 'linear_equation'
            else:
                return 'algebra'
        
        # Calculus
        if any(keyword in text_lower for keyword in ['derivative', 'integral', 'limit', 'differentiate', 'integrate']):
            if 'derivative' in text_lower or 'differentiate' in text_lower:
                return 'derivative'
            elif 'integral' in text_lower or 'integrate' in text_lower:
                return 'integral'
            else:
                return 'calculus'
        
        # Geometry
        if any(keyword in text_lower for keyword in ['area', 'perimeter', 'volume', 'triangle', 'circle', 'rectangle']):
            return 'geometry'
        
        # Trigonometry
        if any(keyword in text_lower for keyword in ['sin', 'cos', 'tan', 'angle', 'triangle']):
            return 'trigonometry'
        
        # Statistics
        if any(keyword in text_lower for keyword in ['mean', 'median', 'mode', 'standard deviation', 'probability']):
            return 'statistics'
        
        return 'general'
    
    def _assess_complexity(self, problem_info: Dict[str, Any]) -> str:
        """Assess the complexity of the mathematical problem"""
        complexity_score = 0
        
        # Count variables
        complexity_score += len(problem_info['variables'])
        
        # Count equations
        complexity_score += len(problem_info['equations'])
        
        # Count expressions
        complexity_score += len(problem_info['expressions'])
        
        # Check for advanced concepts
        text_lower = problem_info['original_text'].lower()
        if any(keyword in text_lower for keyword in ['derivative', 'integral', 'limit']):
            complexity_score += 3
        if any(keyword in text_lower for keyword in ['quadratic', 'polynomial']):
            complexity_score += 2
        if any(keyword in text_lower for keyword in ['trigonometry', 'sin', 'cos', 'tan']):
            complexity_score += 2
        
        if complexity_score <= 2:
            return 'basic'
        elif complexity_score <= 5:
            return 'intermediate'
        else:
            return 'advanced'
    
    def convert_to_sympy(self, expression: str) -> Optional[Any]:
        """Convert a mathematical expression to SymPy format"""
        try:
            # Replace common math functions
            expression = expression.replace('sqrt', 'sqrt')
            expression = expression.replace('sin', 'sin')
            expression = expression.replace('cos', 'cos')
            expression = expression.replace('tan', 'tan')
            expression = expression.replace('log', 'log')
            expression = expression.replace('ln', 'log')
            
            # Handle power notation
            expression = expression.replace('^', '**')
            
            # Parse with SymPy
            return sp.sympify(expression)
        except Exception as e:
            print(f"Error converting expression to SymPy: {e}")
            return None
