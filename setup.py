#!/usr/bin/env python3
import subprocess
import sys
import os


def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
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

    if install_requirements():
        print("\n설치가 완료되었습니다!")
        print("\n프로그램을 실행하려면 다음 명령어를 사용하세요:")
        print("python main.py")
    else:
        print("\n설치에 실패했습니다. 오류를 확인하고 다시 시도해주세요.")


if __name__ == "__main__":
    main()