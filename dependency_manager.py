"""
Helper module for handling dependencies in the HR AI Assistant application.
This allows the app to run even when certain dependencies are missing,
by providing mock implementations or gracefully degrading functionality.
"""

import importlib
import subprocess
import sys
from typing import List, Dict, Any, Optional

class DependencyManager:
    """Manages dependencies for the HR AI Assistant application."""
    
    @staticmethod
    def ensure_package_installed(package_name: str, import_name: Optional[str] = None) -> bool:
        """
        Ensures that a Python package is installed.
        
        Args:
            package_name: The name of the package to install via pip
            import_name: The name to use when importing (if different from package_name)
            
        Returns:
            bool: True if the package is (now) installed, False if installation failed
        """
        name_to_import = import_name or package_name
        
        try:
            importlib.import_module(name_to_import)
            return True
        except ImportError:
            try:
                print(f"Installing {package_name}...")
                subprocess.check_call(["pip", "install", package_name])
                importlib.import_module(name_to_import)
                return True
            except (subprocess.SubprocessError, ImportError):
                print(f"Failed to install {package_name}")
                return False
    
    @staticmethod
    def mock_module(module_path: str, mock_obj: Any) -> None:
        """
        Creates a mock module in sys.modules to prevent import errors.
        
        Args:
            module_path: Dotted path to the module (e.g., 'google.adk')
            mock_obj: The mock object to use as the module
        """
        parts = module_path.split('.')
        
        # Create parent modules if needed
        current = ""
        for part in parts[:-1]:
            current = current + "." + part if current else part
            if current not in sys.modules:
                sys.modules[current] = type('', (), {})()
        
        # Set the actual mock module
        sys.modules[module_path] = mock_obj
    
    @staticmethod
    def install_dependencies(dependencies: List[Dict[str, str]]) -> Dict[str, bool]:
        """
        Attempts to install multiple dependencies.
        
        Args:
            dependencies: List of dicts with 'package' and optional 'import_name' keys
            
        Returns:
            Dict[str, bool]: Results of installation attempts
        """
        results = {}
        for dep in dependencies:
            package = dep['package']
            import_name = dep.get('import_name', package)
            results[package] = DependencyManager.ensure_package_installed(package, import_name)
        return results
