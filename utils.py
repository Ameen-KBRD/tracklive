#!/usr/bin/env python3
import sys

R = '\033[31m'
G = '\033[32m'
C = '\033[36m'
W = '\033[0m'
Y = '\033[33m'

def print_msg(msg):
    """Print colored message"""
    print(msg)

def print_error(msg):
    """Print error message"""
    print(f"{R}[!] {msg}{W}")

def print_success(msg):
    """Print success message"""
    print(f"{G}[+] {msg}{W}")

def print_info(msg):
    """Print info message"""
    print(f"{C}[*] {msg}{W}")
