#!/usr/bin/env python3
"""
Test Python Calculator Script
This is a test file for workflow testing.
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

if __name__ == "__main__":
    print("Calculator Test")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")

