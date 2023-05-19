import subprocess

class CodeExecutor:
    def __init__(self, file_name):
        self.file_name = file_name

    def execute(self):
        """
        Execute the python file
        """
        subprocess.call(["python", self.file_name])
