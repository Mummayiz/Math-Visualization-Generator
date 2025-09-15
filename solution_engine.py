import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, expand, factor, latex
import re
from typing import Dict, List, Tuple, Any, Optional
import openai
from config import Config
from mamin_api import MaminAPI, GoogleMathAPI

class SolutionEngine:
    """Handles mathematical reasoning and step-by-step problem solving"""
    
    def __init__(self):
        # Primary: Mamin API
        self.mamin_client = MaminAPI()
        # Fallback: Google Math API
        self.google_math_client = GoogleMathAPI()
        # Last resort: OpenAI
        self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
        
    def solve_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve a mathematical problem step by step using Mamin API"""
        problem_text = problem_info.get('original_text', '')
        
        # Try Mamin API first
        try:
            print("Using Mamin API for mathematical reasoning...")
            mamin_result = self.mamin_client.solve_math_problem(problem_text)
            
            if mamin_result.get('success', False):
                return self._format_mamin_result(mamin_result, problem_info)
            else:
                print("Mamin API failed, trying Google Math API...")
                google_result = self.google_math_client.solve_math_problem(problem_text)
                if google_result.get('success', False):
                    return self._format_mamin_result(google_result, problem_info)
        except Exception as e:
            print(f"Mamin/Google API failed: {e}")
        
        # Fallback to local solving methods
        print("Using local mathematical solving methods...")
        problem_type = problem_info.get('problem_type', 'general')
        
        # Try local SymPy solving first
        local_solution = self._try_local_sympy_solve(problem_info)
        if local_solution and local_solution.get('steps'):
            return local_solution
        
        # Fallback to specific problem type solvers
        if problem_type == 'algebra' or problem_type == 'linear_equation':
            return self._solve_algebra_problem(problem_info)
        elif problem_type == 'quadratic_equation':
            return self._solve_quadratic_problem(problem_info)
        elif problem_type == 'derivative':
            return self._solve_derivative_problem(problem_info)
        elif problem_type == 'integral':
            return self._solve_integral_problem(problem_info)
        elif problem_type == 'geometry':
            return self._solve_geometry_problem(problem_info)
        elif problem_type == 'trigonometry':
            return self._solve_trigonometry_problem(problem_info)
        else:
            return self._solve_general_problem(problem_info)
    
    def _format_mamin_result(self, mamin_result: Dict[str, Any], problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format Mamin API result into our standard solution format"""
        solution = {
            'problem_type': problem_info.get('problem_type', 'general'),
            'steps': [],
            'final_answer': mamin_result.get('final_answer'),
            'explanation': []
        }
        
        # Convert Mamin steps to our format
        mamin_steps = mamin_result.get('steps', [])
        for i, step in enumerate(mamin_steps, 1):
            formatted_step = {
                'step_number': i,
                'description': step.get('description', f'Step {i}'),
                'equation': step.get('equation', ''),
                'explanation': step.get('explanation', '')
            }
            solution['steps'].append(formatted_step)
        
        # If no steps from Mamin, create a basic structure
        if not solution['steps']:
            solution['steps'].append({
                'step_number': 1,
                'description': 'Problem Analysis',
                'equation': problem_info.get('original_text', ''),
                'explanation': 'Analyzing the mathematical problem using Mamin AI.'
            })
        
        return solution
    
    def _try_local_sympy_solve(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Try to solve using local SymPy methods"""
        try:
            problem_text = problem_info.get('original_text', '')
            equations = problem_info.get('equations', [])
            
            if not equations and '=' in problem_text:
                # Try to extract equation from problem text
                if 'solve for' in problem_text.lower():
                    # Extract equation after "solve for"
                    parts = problem_text.split('solve for', 1)
                    if len(parts) > 1:
                        equation_part = parts[1].strip()
                        if ':' in equation_part:
                            equation_part = equation_part.split(':', 1)[1].strip()
                        equations = [equation_part]
            
            if not equations:
                return None
            
            solution = {
                'problem_type': problem_info.get('problem_type', 'general'),
                'steps': [],
                'final_answer': None,
                'explanation': []
            }
            
            step_count = 1
            
            for equation in equations:
                if '=' in equation:
                    left, right = equation.split('=', 1)
                    left_expr = self._parse_expression(left.strip())
                    right_expr = self._parse_expression(right.strip())
                    
                    # Create equation
                    eq = sp.Eq(left_expr, right_expr)
                    
                    # Add step
                    step = {
                        'step_number': step_count,
                        'description': f'Given equation: {equation}',
                        'equation': str(eq),
                        'explanation': 'This is the equation we need to solve.'
                    }
                    solution['steps'].append(step)
                    step_count += 1
                    
                    # Solve the equation
                    variables = list(eq.free_symbols)
                    if variables:
                        solutions = sp.solve(eq, variables[0])
                        
                        step = {
                            'step_number': step_count,
                            'description': f'Solve for {variables[0]}',
                            'equation': f'{variables[0]} = {solutions}',
                            'explanation': f'Using algebraic manipulation to solve for {variables[0]}.'
                        }
                        solution['steps'].append(step)
                        solution['final_answer'] = f'{variables[0]} = {solutions}'
                        step_count += 1
            
            return solution if solution['steps'] else None
            
        except Exception as e:
            print(f"Local SymPy solving failed: {e}")
            return None
    
    def _solve_algebra_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve linear algebra problems"""
        solution = {
            'problem_type': 'algebra',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        equations = problem_info.get('equations', [])
        variables = problem_info.get('variables', ['x'])
        
        if not equations:
            return solution
        
        try:
            # Convert equations to SymPy format
            sympy_equations = []
            for eq in equations:
                if '=' in eq:
                    left, right = eq.split('=', 1)
                    sympy_eq = sp.Eq(
                        self._parse_expression(left.strip()),
                        self._parse_expression(right.strip())
                    )
                    sympy_equations.append(sympy_eq)
            
            if sympy_equations:
                # Solve the system
                variables_sym = [symbols(var) for var in variables]
                solutions = solve(sympy_equations, variables_sym)
                
                # Generate step-by-step solution
                step_count = 1
                for i, eq in enumerate(sympy_equations):
                    step = {
                        'step_number': step_count,
                        'description': f"Given equation {i+1}",
                        'equation': latex(eq),
                        'explanation': f"This is equation {i+1} from the problem."
                    }
                    solution['steps'].append(step)
                    step_count += 1
                
                # Add solving steps
                if solutions:
                    step = {
                        'step_number': step_count,
                        'description': "Solve the system of equations",
                        'equation': f"Solution: {solutions}",
                        'explanation': "Using algebraic manipulation to solve for the variables."
                    }
                    solution['steps'].append(step)
                    solution['final_answer'] = solutions
                else:
                    step = {
                        'step_number': step_count,
                        'description': "No solution found",
                        'equation': "No solution exists",
                        'explanation': "The system of equations has no solution."
                    }
                    solution['steps'].append(step)
        
        except Exception as e:
            solution['steps'].append({
                'step_number': 1,
                'description': "Error in solving",
                'equation': f"Error: {str(e)}",
                'explanation': "An error occurred while solving the problem."
            })
        
        return solution
    
    def _solve_quadratic_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve quadratic equations"""
        solution = {
            'problem_type': 'quadratic_equation',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        equations = problem_info.get('equations', [])
        
        if not equations:
            return solution
        
        try:
            for eq in equations:
                if '=' in eq:
                    left, right = eq.split('=', 1)
                    # Move everything to left side
                    equation = sp.Eq(
                        self._parse_expression(left.strip()),
                        self._parse_expression(right.strip())
                    )
                    
                    # Convert to standard form ax² + bx + c = 0
                    standard_form = equation.lhs - equation.rhs
                    
                    step = {
                        'step_number': 1,
                        'description': "Given quadratic equation",
                        'equation': latex(equation),
                        'explanation': "This is the quadratic equation we need to solve."
                    }
                    solution['steps'].append(step)
                    
                    step = {
                        'step_number': 2,
                        'description': "Convert to standard form",
                        'equation': f"{latex(standard_form)} = 0",
                        'explanation': "Move all terms to one side to get the standard form ax² + bx + c = 0."
                    }
                    solution['steps'].append(step)
                    
                    # Solve using quadratic formula
                    x = symbols('x')
                    solutions = solve(standard_form, x)
                    
                    step = {
                        'step_number': 3,
                        'description': "Apply quadratic formula",
                        'equation': f"x = {solutions}",
                        'explanation': "Using the quadratic formula: x = (-b ± √(b² - 4ac)) / 2a"
                    }
                    solution['steps'].append(step)
                    
                    solution['final_answer'] = solutions
                    break
        
        except Exception as e:
            solution['steps'].append({
                'step_number': 1,
                'description': "Error in solving",
                'equation': f"Error: {str(e)}",
                'explanation': "An error occurred while solving the quadratic equation."
            })
        
        return solution
    
    def _solve_derivative_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve derivative problems"""
        solution = {
            'problem_type': 'derivative',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        expressions = problem_info.get('expressions', [])
        
        if not expressions:
            return solution
        
        try:
            for expr_str in expressions:
                # Parse expression
                expr = self._parse_expression(expr_str)
                x = symbols('x')
                
                step = {
                    'step_number': 1,
                    'description': "Given function",
                    'equation': f"f(x) = {latex(expr)}",
                    'explanation': "This is the function we need to differentiate."
                }
                solution['steps'].append(step)
                
                # Find derivative
                derivative = diff(expr, x)
                
                step = {
                    'step_number': 2,
                    'description': "Apply differentiation rules",
                    'equation': f"f'(x) = {latex(derivative)}",
                    'explanation': "Using the power rule, product rule, and chain rule as needed."
                }
                solution['steps'].append(step)
                
                # Simplify if possible
                simplified = simplify(derivative)
                if simplified != derivative:
                    step = {
                        'step_number': 3,
                        'description': "Simplify the derivative",
                        'equation': f"f'(x) = {latex(simplified)}",
                        'explanation': "Simplify the expression to get the final answer."
                    }
                    solution['steps'].append(step)
                
                solution['final_answer'] = latex(simplified)
                break
        
        except Exception as e:
            solution['steps'].append({
                'step_number': 1,
                'description': "Error in solving",
                'equation': f"Error: {str(e)}",
                'explanation': "An error occurred while finding the derivative."
            })
        
        return solution
    
    def _solve_integral_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve integral problems"""
        solution = {
            'problem_type': 'integral',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        expressions = problem_info.get('expressions', [])
        
        if not expressions:
            return solution
        
        try:
            for expr_str in expressions:
                # Parse expression
                expr = self._parse_expression(expr_str)
                x = symbols('x')
                
                step = {
                    'step_number': 1,
                    'description': "Given function",
                    'equation': f"∫ {latex(expr)} dx",
                    'explanation': "This is the integral we need to evaluate."
                }
                solution['steps'].append(step)
                
                # Find integral
                integral = integrate(expr, x)
                
                step = {
                    'step_number': 2,
                    'description': "Apply integration rules",
                    'equation': f"∫ {latex(expr)} dx = {latex(integral)} + C",
                    'explanation': "Using integration rules such as power rule, substitution, or integration by parts."
                }
                solution['steps'].append(step)
                
                solution['final_answer'] = latex(integral) + " + C"
                break
        
        except Exception as e:
            solution['steps'].append({
                'step_number': 1,
                'description': "Error in solving",
                'equation': f"Error: {str(e)}",
                'explanation': "An error occurred while evaluating the integral."
            })
        
        return solution
    
    def _solve_geometry_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve geometry problems"""
        solution = {
            'problem_type': 'geometry',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        # Use AI to solve geometry problems
        if self.openai_client:
            try:
                prompt = f"""
                Solve this geometry problem step by step:
                {problem_info['original_text']}
                
                Provide:
                1. What is given
                2. What we need to find
                3. Step-by-step solution with formulas
                4. Final answer
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                
                ai_solution = response.choices[0].message.content
                
                # Parse AI response into steps
                lines = ai_solution.split('\n')
                step_count = 1
                current_step = ""
                
                for line in lines:
                    if line.strip():
                        if line.strip().startswith(('1.', '2.', '3.', '4.')):
                            if current_step:
                                solution['steps'].append({
                                    'step_number': step_count,
                                    'description': f"Step {step_count}",
                                    'equation': current_step,
                                    'explanation': current_step
                                })
                                step_count += 1
                            current_step = line.strip()
                        else:
                            current_step += " " + line.strip()
                
                if current_step:
                    solution['steps'].append({
                        'step_number': step_count,
                        'description': f"Step {step_count}",
                        'equation': current_step,
                        'explanation': current_step
                    })
                
            except Exception as e:
                solution['steps'].append({
                    'step_number': 1,
                    'description': "Error in solving",
                    'equation': f"Error: {str(e)}",
                    'explanation': "An error occurred while solving the geometry problem."
                })
        
        return solution
    
    def _solve_trigonometry_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve trigonometry problems"""
        solution = {
            'problem_type': 'trigonometry',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        # Use AI for trigonometry problems
        if self.openai_client:
            try:
                prompt = f"""
                Solve this trigonometry problem step by step:
                {problem_info['original_text']}
                
                Provide:
                1. What is given
                2. What we need to find
                3. Step-by-step solution with trigonometric identities
                4. Final answer
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                
                ai_solution = response.choices[0].message.content
                
                # Parse AI response into steps
                lines = ai_solution.split('\n')
                step_count = 1
                current_step = ""
                
                for line in lines:
                    if line.strip():
                        if line.strip().startswith(('1.', '2.', '3.', '4.')):
                            if current_step:
                                solution['steps'].append({
                                    'step_number': step_count,
                                    'description': f"Step {step_count}",
                                    'equation': current_step,
                                    'explanation': current_step
                                })
                                step_count += 1
                            current_step = line.strip()
                        else:
                            current_step += " " + line.strip()
                
                if current_step:
                    solution['steps'].append({
                        'step_number': step_count,
                        'description': f"Step {step_count}",
                        'equation': current_step,
                        'explanation': current_step
                    })
                
            except Exception as e:
                solution['steps'].append({
                    'step_number': 1,
                    'description': "Error in solving",
                    'equation': f"Error: {str(e)}",
                    'explanation': "An error occurred while solving the trigonometry problem."
                })
        
        return solution
    
    def _solve_general_problem(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve general mathematical problems using AI"""
        solution = {
            'problem_type': 'general',
            'steps': [],
            'final_answer': None,
            'explanation': []
        }
        
        if self.openai_client:
            try:
                prompt = f"""
                Solve this mathematical problem step by step:
                {problem_info['original_text']}
                
                Provide a detailed step-by-step solution with:
                1. Understanding the problem
                2. Identifying the approach
                3. Step-by-step solution
                4. Final answer
                5. Verification if applicable
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                
                ai_solution = response.choices[0].message.content
                
                # Parse AI response into steps
                lines = ai_solution.split('\n')
                step_count = 1
                current_step = ""
                
                for line in lines:
                    if line.strip():
                        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                            if current_step:
                                solution['steps'].append({
                                    'step_number': step_count,
                                    'description': f"Step {step_count}",
                                    'equation': current_step,
                                    'explanation': current_step
                                })
                                step_count += 1
                            current_step = line.strip()
                        else:
                            current_step += " " + line.strip()
                
                if current_step:
                    solution['steps'].append({
                        'step_number': step_count,
                        'description': f"Step {step_count}",
                        'equation': current_step,
                        'explanation': current_step
                    })
                
            except Exception as e:
                solution['steps'].append({
                    'step_number': 1,
                    'description': "Error in solving",
                    'equation': f"Error: {str(e)}",
                    'explanation': "An error occurred while solving the problem."
                })
        
        return solution
    
    def _parse_expression(self, expr_str: str) -> Any:
        """Parse a mathematical expression string into SymPy format"""
        try:
            # Clean the expression
            expr_str = expr_str.strip()
            
            # Replace common symbols
            replacements = {
                '^': '**',
                '×': '*',
                '÷': '/',
                'π': 'pi',
                '√': 'sqrt',
                '∞': 'oo'
            }
            
            for old, new in replacements.items():
                expr_str = expr_str.replace(old, new)
            
            # Parse with SymPy
            return sp.sympify(expr_str)
        except Exception as e:
            print(f"Error parsing expression '{expr_str}': {e}")
            return expr_str
