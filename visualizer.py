import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import sympy as sp
from sympy import symbols, lambdify
from typing import Dict, List, Tuple, Any, Optional
import io
from PIL import Image, ImageDraw, ImageFont
import math

class MathVisualizer:
    """Creates visual representations of mathematical concepts and solutions"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.fig_size = (12, 8)
        self.dpi = 100
        
    def create_problem_visualization(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Create a visual representation of the math problem"""
        problem_type = problem_info.get('problem_type', 'general')
        
        if problem_type == 'algebra' or problem_type == 'linear_equation':
            return self._visualize_linear_equation(problem_info)
        elif problem_type == 'quadratic_equation':
            return self._visualize_quadratic_equation(problem_info)
        elif problem_type == 'derivative':
            return self._visualize_derivative(problem_info)
        elif problem_type == 'integral':
            return self._visualize_integral(problem_info)
        elif problem_type == 'geometry':
            return self._visualize_geometry(problem_info)
        elif problem_type == 'trigonometry':
            return self._visualize_trigonometry(problem_info)
        else:
            return self._visualize_general_problem(problem_info)
    
    def create_step_visualization(self, step: Dict[str, Any], step_number: int) -> Image.Image:
        """Create a visual representation of a solution step"""
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Add step number
        ax.text(0.5, 9.5, f"Step {step_number}", fontsize=20, fontweight='bold', ha='center')
        
        # Add description
        ax.text(0.5, 8.5, step.get('description', ''), fontsize=16, ha='center', wrap=True)
        
        # Add equation
        equation = step.get('equation', '')
        if equation:
            ax.text(0.5, 7, f"${equation}$", fontsize=18, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        # Add explanation
        explanation = step.get('explanation', '')
        if explanation:
            ax.text(0.5, 5, explanation, fontsize=14, ha='center', va='top', wrap=True)
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_linear_equation(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize linear equations"""
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        
        # Extract equation
        equations = problem_info.get('equations', [])
        if equations:
            equation = equations[0]
            ax.text(0.5, 0.5, f"${equation}$", fontsize=24, ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.7))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title("Linear Equation Problem", fontsize=20, fontweight='bold')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_quadratic_equation(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize quadratic equations with graph"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Left plot: Equation
        equations = problem_info.get('equations', [])
        if equations:
            equation = equations[0]
            ax1.text(0.5, 0.5, f"${equation}$", fontsize=20, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title("Quadratic Equation", fontsize=16, fontweight='bold')
        
        # Right plot: Graph
        try:
            # Try to plot the quadratic function
            x = symbols('x')
            expr = self._parse_equation_to_expr(equation)
            if expr:
                f = lambdify(x, expr, 'numpy')
                x_vals = np.linspace(-10, 10, 1000)
                y_vals = f(x_vals)
                
                ax2.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
                ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                ax2.grid(True, alpha=0.3)
                ax2.set_xlabel('x')
                ax2.set_ylabel('f(x)')
                ax2.set_title('Graph of the Quadratic Function')
                ax2.legend()
        except:
            ax2.text(0.5, 0.5, "Graph not available", ha='center', va='center', fontsize=16)
            ax2.axis('off')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_derivative(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize derivative problems with function and derivative graphs"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Left plot: Original function
        expressions = problem_info.get('expressions', [])
        if expressions:
            expr_str = expressions[0]
            ax1.text(0.5, 0.5, f"$f(x) = {expr_str}$", fontsize=18, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title("Original Function", fontsize=16, fontweight='bold')
        
        # Right plot: Graph
        try:
            x = symbols('x')
            expr = self._parse_expression_to_expr(expr_str)
            if expr:
                f = lambdify(x, expr, 'numpy')
                x_vals = np.linspace(-5, 5, 1000)
                y_vals = f(x_vals)
                
                ax2.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
                ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                ax2.grid(True, alpha=0.3)
                ax2.set_xlabel('x')
                ax2.set_ylabel('f(x)')
                ax2.set_title('Graph of the Function')
                ax2.legend()
        except:
            ax2.text(0.5, 0.5, "Graph not available", ha='center', va='center', fontsize=16)
            ax2.axis('off')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_integral(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize integral problems with area under curve"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Left plot: Integral expression
        expressions = problem_info.get('expressions', [])
        if expressions:
            expr_str = expressions[0]
            ax1.text(0.5, 0.5, f"$\\int {expr_str} \\, dx$", fontsize=20, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.7))
        
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title("Integral Expression", fontsize=16, fontweight='bold')
        
        # Right plot: Area under curve
        try:
            x = symbols('x')
            expr = self._parse_expression_to_expr(expr_str)
            if expr:
                f = lambdify(x, expr, 'numpy')
                x_vals = np.linspace(-3, 3, 1000)
                y_vals = f(x_vals)
                
                ax2.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
                ax2.fill_between(x_vals, 0, y_vals, alpha=0.3, color='blue', label='Area under curve')
                ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                ax2.grid(True, alpha=0.3)
                ax2.set_xlabel('x')
                ax2.set_ylabel('f(x)')
                ax2.set_title('Area Under the Curve')
                ax2.legend()
        except:
            ax2.text(0.5, 0.5, "Graph not available", ha='center', va='center', fontsize=16)
            ax2.axis('off')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_geometry(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize geometry problems"""
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        
        # Create a simple geometric shape based on problem type
        text = problem_info.get('original_text', '').lower()
        
        if 'triangle' in text:
            # Draw a triangle
            triangle = patches.Polygon([(2, 2), (6, 2), (4, 6)], linewidth=2, 
                                     edgecolor='blue', facecolor='lightblue', alpha=0.7)
            ax.add_patch(triangle)
            ax.text(4, 4, 'Triangle', ha='center', va='center', fontsize=16, fontweight='bold')
        elif 'circle' in text:
            # Draw a circle
            circle = patches.Circle((4, 4), 2, linewidth=2, edgecolor='red', 
                                  facecolor='lightcoral', alpha=0.7)
            ax.add_patch(circle)
            ax.text(4, 4, 'Circle', ha='center', va='center', fontsize=16, fontweight='bold')
        elif 'rectangle' in text:
            # Draw a rectangle
            rectangle = patches.Rectangle((2, 2), 4, 3, linewidth=2, edgecolor='green', 
                                        facecolor='lightgreen', alpha=0.7)
            ax.add_patch(rectangle)
            ax.text(4, 3.5, 'Rectangle', ha='center', va='center', fontsize=16, fontweight='bold')
        else:
            # Generic geometry visualization
            ax.text(0.5, 0.5, "Geometry Problem", fontsize=20, ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.7))
        
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title("Geometry Problem", fontsize=18, fontweight='bold')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_trigonometry(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize trigonometry problems with unit circle and graphs"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Left plot: Unit circle
        circle = patches.Circle((0, 0), 1, linewidth=2, edgecolor='blue', fill=False)
        ax1.add_patch(circle)
        
        # Draw axes
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Draw angle
        theta = np.pi/4  # 45 degrees
        ax1.plot([0, np.cos(theta)], [0, np.sin(theta)], 'r-', linewidth=2)
        ax1.plot(np.cos(theta), np.sin(theta), 'ro', markersize=8)
        
        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.set_aspect('equal')
        ax1.set_title('Unit Circle', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Right plot: Trigonometric functions
        x = np.linspace(0, 2*np.pi, 1000)
        ax2.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
        ax2.plot(x, np.cos(x), 'r-', linewidth=2, label='cos(x)')
        ax2.plot(x, np.tan(x), 'g-', linewidth=2, label='tan(x)')
        
        ax2.set_xlim(0, 2*np.pi)
        ax2.set_ylim(-2, 2)
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('x (radians)')
        ax2.set_ylabel('y')
        ax2.set_title('Trigonometric Functions', fontsize=16, fontweight='bold')
        ax2.legend()
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _visualize_general_problem(self, problem_info: Dict[str, Any]) -> Image.Image:
        """Visualize general mathematical problems"""
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        
        # Display the problem text
        problem_text = problem_info.get('original_text', 'Mathematical Problem')
        ax.text(0.5, 0.5, problem_text, fontsize=16, ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.7),
               wrap=True)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title("Mathematical Problem", fontsize=20, fontweight='bold')
        
        # Convert to PIL Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        
        return img
    
    def _parse_equation_to_expr(self, equation: str) -> Optional[Any]:
        """Parse equation string to SymPy expression"""
        try:
            if '=' in equation:
                left, right = equation.split('=', 1)
                return sp.sympify(left.strip()) - sp.sympify(right.strip())
            else:
                return sp.sympify(equation)
        except:
            return None
    
    def _parse_expression_to_expr(self, expr_str: str) -> Optional[Any]:
        """Parse expression string to SymPy expression"""
        try:
            return sp.sympify(expr_str)
        except:
            return None
