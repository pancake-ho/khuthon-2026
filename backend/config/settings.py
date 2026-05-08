"""
Django 프로젝트의 백엔드 및 프론트엔드 기본 설정 파일
현재 기준
- BE: DJango
- FE: React 전제
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variables
load_dotenv(BASE_DIR / ".env")