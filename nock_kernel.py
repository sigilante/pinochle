from ipykernel.kernelbase import Kernel
from noun import parse, pretty
from nock import nock, to_noun
import sys
import traceback

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
    banner = "Nock 4K Kernel - An Urbit Nock interpreter"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject = 0  # Default subject
        self.last_result = None

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
               allow_stdin=False):
        """Execute user code"""
        
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}
        
        try:
            code = code.strip()
            
            # Handle Hoon dottar syntax: .*(subject formula)
            if code.startswith('.*(') and code.endswith(')'):
                # Extract the content between .*( and )
                inner = code[3:-1].strip()
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
                self.subject = parse(subject_str)
                output = f"Subject set to: {pretty(self.subject, False)}"
                
            elif code.startswith(':formula'):
                # Evaluate formula against current subject: `:formula [0 1]`
                formula_str = code[8:].strip()
                formula = parse(formula_str)
                result = nock(self.subject, formula)
                self.last_result = result
                output = pretty(result, False)
                
            elif code.startswith(':nock'):
                # Full nock expression: `:nock [subject formula]`
                expr_str = code[5:].strip()
                expr = parse(expr_str)
                if not hasattr(expr, 'head'):
                    output = "Error: :nock requires [subject formula]"
                else:
                    result = nock(expr.head, expr.tail)
                    self.last_result = result
                    output = pretty(result, False)
                    
            elif code.startswith(':show'):
                # Show current state
                output = f"Subject: {pretty(self.subject, False)}\n"
                if self.last_result is not None:
                    output += f"Last result: {pretty(self.last_result, False)}"
                    
            elif code.startswith(':help'):
                output = """Nock Kernel Commands:
    :subject <noun>    - Set the subject for subsequent formulas
    :formula <formula> - Evaluate formula against current subject
    :nock <expr>       - Evaluate full nock expression [subject formula]
    :show              - Show current subject and last result
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
    """
            else:
                # Default: treat as formula against current subject
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
