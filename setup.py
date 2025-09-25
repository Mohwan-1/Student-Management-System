#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path


def create_venv():
    """가상환경 생성"""
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✓ 가상환경이 이미 존재합니다.")
        return True

    try:
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
        print("✓ 가상환경(.venv)을 생성했습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 가상환경 생성 중 오류가 발생했습니다: {e}")
        return False


def get_venv_python():
    """가상환경의 Python 경로 반환"""
    if os.name == 'nt':  # Windows
        return Path(".venv/Scripts/python.exe")
    else:  # Linux/macOS
        return Path(".venv/bin/python")


def install_requirements():
    """가상환경에 패키지 설치"""
    venv_python = get_venv_python()

    if not venv_python.exists():
        print("✗ 가상환경의 Python을 찾을 수 없습니다.")
        return False

    try:
        # pip 업그레이드
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ pip을 업그레이드했습니다.")

        # 패키지 설치
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 의존성 패키지 설치가 완료되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 패키지 설치 중 오류가 발생했습니다: {e}")
        return False


def main():
    print("Student Management System 설치를 시작합니다...")
    print("=" * 50)

    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt 파일을 찾을 수 없습니다.")
        return

    # 가상환경 생성
    if not create_venv():
        return

    # 패키지 설치
    if install_requirements():
        print("\n✓ 설치가 완료되었습니다!")
        print("\n프로그램을 실행하려면 다음 명령어를 사용하세요:")
        if os.name == 'nt':  # Windows
            print("1. 가상환경 활성화: .venv\\Scripts\\activate")
            print("2. 프로그램 실행: python main.py")
            print("\n또는 한 번에: .venv\\Scripts\\python.exe main.py")
        else:  # Linux/macOS
            print("1. 가상환경 활성화: source .venv/bin/activate")
            print("2. 프로그램 실행: python main.py")
            print("\n또는 한 번에: .venv/bin/python main.py")
    else:
        print("\n✗ 설치에 실패했습니다. 오류를 확인하고 다시 시도해주세요.")


if __name__ == "__main__":
    main()