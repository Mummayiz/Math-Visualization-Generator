#!/usr/bin/env python3
"""
Demo script showcasing Mamin AI integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mamin_api import MaminAPI, GoogleMathAPI
from solution_engine import SolutionEngine
from math_parser import MathParser

def demo_mamin_api():
    """Demonstrate Mamin API functionality"""
    print("🧮 Mamin AI Math Solver Demo")
    print("=" * 50)
    
    # Initialize Mamin API
    mamin = MaminAPI()
    google_math = GoogleMathAPI()
    solver = SolutionEngine()
    parser = MathParser()
    
    # Test problems
    test_problems = [
        "Solve for x: 2x + 5 = 13",
        "Find the derivative of f(x) = x² + 3x + 2",
        "Calculate the area of a circle with radius 5",
        "Solve the quadratic equation: x² - 5x + 6 = 0",
        "Find the integral of ∫(2x + 1)dx"
    ]
    
    for i, problem in enumerate(test_problems, 1):
        print(f"\n🔢 Problem {i}: {problem}")
        print("-" * 40)
        
        # Parse the problem
        problem_info = parser.parse_problem(problem)
        print(f"Problem Type: {problem_info.get('problem_type', 'unknown')}")
        print(f"Variables: {problem_info.get('variables', [])}")
        print(f"Complexity: {problem_info.get('complexity', 'unknown')}")
        
        # Solve using Mamin
        print("\n🤖 Solving with Mamin AI...")
        try:
            mamin_result = mamin.solve_math_problem(problem)
            print(f"Mamin Result: {mamin_result}")
        except Exception as e:
            print(f"Mamin API Error: {e}")
        
        # Solve using Google Math API
        print("\n🔍 Solving with Google Math API...")
        try:
            google_result = google_math.solve_math_problem(problem)
            print(f"Google Math Result: {google_result}")
        except Exception as e:
            print(f"Google Math API Error: {e}")
        
        # Solve using the complete solution engine
        print("\n⚙️  Solving with Solution Engine...")
        try:
            solution = solver.solve_problem(problem_info)
            print(f"Solution Steps: {len(solution.get('steps', []))}")
            print(f"Final Answer: {solution.get('final_answer', 'No answer')}")
            
            # Display steps
            for step in solution.get('steps', []):
                print(f"  Step {step.get('step_number', '?')}: {step.get('description', '')}")
                if step.get('equation'):
                    print(f"    Equation: {step.get('equation', '')}")
                if step.get('explanation'):
                    print(f"    Explanation: {step.get('explanation', '')}")
        except Exception as e:
            print(f"Solution Engine Error: {e}")
        
        print("\n" + "="*50)

def demo_api_key_usage():
    """Demonstrate API key usage"""
    print("\n🔑 API Key Configuration Demo")
    print("=" * 50)
    
    from config import Config
    
    print(f"Mamin API Key: {Config.MAMIN_API_KEY[:20]}..." if Config.MAMIN_API_KEY else "Not set")
    print(f"OpenAI API Key: {'Set' if Config.OPENAI_API_KEY else 'Not set'}")
    
    # Test API connectivity
    mamin = MaminAPI()
    google_math = GoogleMathAPI()
    
    print("\n🌐 Testing API Connectivity...")
    
    # Test Mamin API
    try:
        result = mamin.solve_math_problem("2 + 2 = ?")
        print(f"Mamin API Status: {'Connected' if result else 'Failed'}")
    except Exception as e:
        print(f"Mamin API Status: Failed - {e}")
    
    # Test Google Math API
    try:
        result = google_math.solve_math_problem("2 + 2 = ?")
        print(f"Google Math API Status: {'Connected' if result else 'Failed'}")
    except Exception as e:
        print(f"Google Math API Status: Failed - {e}")

def main():
    """Main demo function"""
    print("🚀 Starting Mamin AI Integration Demo")
    print("This demo showcases the mathematical reasoning capabilities")
    print("using Mamin API with fallback to Google Math API and local solving.")
    print()
    
    # Demo API key usage
    demo_api_key_usage()
    
    # Demo Mamin API functionality
    demo_mamin_api()
    
    print("\n🎉 Demo completed!")
    print("\nThe system is ready to:")
    print("1. Process math problems using Mamin AI")
    print("2. Fall back to Google Math API if needed")
    print("3. Use local mathematical solving as last resort")
    print("4. Generate educational videos with step-by-step solutions")

if __name__ == "__main__":
    main()
