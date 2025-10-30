from ipykernel.kernelbase import Kernel
from pinochle import nock, to_noun, parse, pretty
import traceback
import re

def preprocess_hoon_syntax(code):
    """Convert Hoon syntax to plain Nock syntax
    
    Converts:
    - %0, %1, %2, etc. → 0, 1, 2, etc.
    - .*(subject formula) stays as-is
    """
    # Replace %N (where N is a number) with just N
    code = re.sub(r'%(\d+)', r'\1', code)
    return code

class NockKernel(Kernel):
    implementation = 'Nock'
    implementation_version = '1.0'
    language = 'nock'
    language_version = '4K'
    language_info = {
        'name': 'nock',
        'mimetype': 'text/plain',
        'file_extension': '.nock',
    }
    banner = """Nock 4K Kernel - An Urbit Nock interpreter
Version 1.0
Copyright (c) 2025 N. E. Davis for Urbit Systems Technical Journal
License: MIT

For help, type :help
"""
    help_links = [
        {
            'text': 'Nock Specification',
            'url': 'https://nock.is/content/specification/index.html'
        },
        {
            'text': 'Urbit Documentation', 
            'url': 'https://docs.urbit.org'
        },
        {
            'text': 'NockApp Documentation',
            'url': 'https://docs.nockchain.org'
        }
    ]
    variables = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject = 0  # Default subject
        self.last_result = None

    def substitute_variables(self, code):
        """Replace variable names with their values in the code string"""
        import re
        
        # Find all potential variable references (words that aren't inside brackets/quotes)
        # We'll do a simple approach: replace whole words that match variable names
        for var_name in self.variables:
            # Use word boundaries to avoid partial matches
            # Match the variable name when it's not part of a larger word
            pattern = r'\b' + re.escape(var_name) + r'\b'
            replacement = pretty(self.variables[var_name], False)
            code = re.sub(pattern, replacement, code)
        
        return code

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
               allow_stdin=False):
        """Execute user code"""
        
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
        
        try:
            code = code.strip()

            # Preprocess Hoon syntax (convert %N to N)
            code = preprocess_hoon_syntax(code)

            # Handle Hoon dottar syntax: .*(subject formula)
            if code.startswith('.*(') and code.endswith(')'):
                # Extract the content between .*( and )
                inner = code[3:-1].strip()
                inner = self.substitute_variables(inner)
                # Parse as a cell [subject formula]
                expr = parse(inner)
                if not hasattr(expr, 'head'):
                    output = "Error: .*() requires [subject formula]"
                else:
                    result = nock(expr.head, expr.tail)
                    self.last_result = result
                    # Also update subject to match what was used
                    self.subject = expr.head
                    output = pretty(result, False)
            
            # Handle special commands
            elif code.startswith(':subject'):
                # Set subject: `:subject [1 2 3]`
                subject_str = code[8:].strip()
                subject_str = self.substitute_variables(subject_str)
                self.subject = parse(subject_str)
                output = f"Subject set to: {pretty(self.subject, False)}"
                
            elif code.startswith(':formula'):
                # Evaluate formula against current subject: `:formula [0 1]`
                formula_str = code[8:].strip()
                formula_str = self.substitute_variables(formula_str)
                formula = parse(formula_str)
                result = nock(self.subject, formula)
                self.last_result = result
                output = pretty(result, False)
                
            elif code.startswith(':nock'):
                # Full nock expression: `:nock [subject formula]`
                expr_str = code[5:].strip()
                expr_str = self.substitute_variables(expr_str)
                expr = parse(expr_str)
                if not hasattr(expr, 'head'):
                    output = "Error: :nock requires [subject formula]"
                else:
                    result = nock(expr.head, expr.tail)
                    self.last_result = result
                    output = pretty(result, False)
                    
            elif code.startswith(':show'):
                # Show current state or specific variable
                parts = code.split(None, 1)  # Split on first whitespace
                
                if len(parts) == 1:
                    # :show with no args - show everything
                    output = f"Subject: {pretty(self.subject, False)}\n"
                    if self.last_result is not None:
                        output += f"Last result: {pretty(self.last_result, False)}\n"
                    
                    # Check if variables dict exists
                    if hasattr(self, 'variables') and self.variables:
                        output += "\nVariables:\n"
                        for var_name, var_value in self.variables.items():
                            output += f"  {var_name} = {pretty(var_value, False)}\n"
                    else:
                        output += "\nNo variables defined"
                else:
                    # :show varname - show specific variable
                    var_name = parts[1].strip()
                    if hasattr(self, 'variables') and var_name in self.variables:
                        output = f"{var_name} = {pretty(self.variables[var_name], False)}"
                    else:
                        output = f"Variable '{var_name}' not found"                    

            elif code.startswith(':help'):
                output = """Nock Kernel Commands:
    :subject <noun>    - Set the subject for subsequent formulas
    :formula <formula> - Evaluate formula against current subject
    :nock <expr>       - Evaluate full nock expression [subject formula]
    :show              - Show current subject and last result
    :<varname>         - Define variable 'varname' with a noun value
    :show <varname>    - Show value of variable 'varname'
    :help              - Show this help message

    Hoon Syntax:
    .*(subject formula) - Evaluate using Hoon dottar syntax

    Examples:
    :subject [42 43 44]
    :formula [0 2]              # Returns 42
    :nock [[1 2] [0 1]]         # Returns [1 2]
    .*(42 [0 1])                # Hoon syntax - returns 42
    .*([1 2 3] [0 2])           # Returns 1
    
    You can also evaluate formulas directly (uses current subject):
    [0 1]                       # Same as :formula [0 1]
    [4 0 1]                     # Increment the subject

    :increment [4 0 1]
    .*(43 increment)
    """
            elif code.startswith(':'):
                # Define a variable. E.g., `:var-name [1 2 3]`
                match = re.match(r':\s*([a-zA-Z_][a-zA-Z0-9_-]*)\s+(.+)', code)
                if match:
                    var_name = match.group(1)
                    var_value_str = match.group(2).strip()
                    # SUBSTITUTE VARIABLES BEFORE PARSING
                    var_value_str = self.substitute_variables(var_value_str)
                    var_value = parse(var_value_str)
                    if not hasattr(self, 'variables'):
                        self.variables = {}
                    self.variables[var_name] = var_value
                    output = f"Variable '{var_name}' set to: {pretty(var_value, False)}"
                else:
                    output = "Error: Invalid variable assignment syntax. Use :varname <noun>"
                    self.last_result = None
            else:
                # Default: treat as formula against current subject
                code = self.substitute_variables(code)
                formula = parse(code)
                result = nock(self.subject, formula)
                self.last_result = result
                output = pretty(result, False)
            
            if not silent:
                stream_content = {'name': 'stdout', 'text': output + '\n'}
                self.send_response(self.iopub_socket, 'stream', stream_content)

            return {'status': 'ok',
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {}}

        except Exception as e:
            if not silent:
                error_content = {
                    'name': 'stderr',
                    'text': f"Error: {str(e)}\n{traceback.format_exc()}"
                }
                self.send_response(self.iopub_socket, 'stream', error_content)

            return {'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': type(e).__name__,
                    'evalue': str(e),
                    'traceback': traceback.format_exc().split('\n')}

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=NockKernel)
