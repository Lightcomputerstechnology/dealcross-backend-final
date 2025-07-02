#!/usr/bin/env python

import typer
import asyncio
import os

app = typer.Typer(help="Dealcross Management CLI")

@app.command()
def migrate():
    """Run Aerich migrations"""
    os.system("aerich upgrade")

@app.command()
def makemigrations():
    """Generate new migrations"""
    os.system("aerich migrate")

@app.command()
def seed_admin():
    """Seed default admin user"""
    os.system("python seed_admin.py")

@app.command()
def test():
    """Run tests"""
    os.system("pytest -v")

@app.command()
def lint():
    """Run ruff and mypy"""
    os.system("ruff .")
    os.system("mypy .")

@app.command()
def format():
    """Run black formatter"""
    os.system("black .")

@app.command()
def run():
    """Run FastAPI app"""
    os.system("uvicorn main:app --host 0.0.0.0 --port 10000 --reload")

if __name__ == "__main__":
    app()
