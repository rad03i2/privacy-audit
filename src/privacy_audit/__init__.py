"""Privacy Audit public API."""
from .scanner import Finding, scan_path, scan_text

__version__ = "1.0.0"
__author__ = "Radwan Abdulhadi Ahmed / @rad03i2"

__all__ = ["Finding", "scan_path", "scan_text", "__version__"]
