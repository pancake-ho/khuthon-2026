"""
Django 프로젝트 실행 및 관리 파일
"""

import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        raise ImportError(
            "Django 라이브러리를 import할 수 없습니다. "
            "가상환경이 활성화되어 있는 지, requirements.txt 설치가 완료되었는 지 확인해주세요."
        ) from e
    
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()