#!/usr/bin/env python3
"""
날짜별 정확한 테스트
"""

import sys
import os
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student, AppData
from src.google_sheets_api import GoogleSheetsAPI
from datetime import date, datetime

def test_specific_dates():
    """특정 날짜로 테스트"""

    print("=== 날짜별 정확한 테스트 ===\n")

    webapp_url = "https://script.google.com/macros/s/AKfycbxT7joPlgV9cZv_kdo5uHXoyV22v8q-nWU-aRKAuOlRaq0eHqh3w68HMLyovy8LgJVbMw/exec"
    api = GoogleSheetsAPI(webapp_url)

    test_dates = [
        date(2024, 1, 1),   # 2024-01-01
        date(2025, 9, 28),  # 2025-09-28 (사용자가 언급한 날짜)
        date(2025, 12, 25), # 2025-12-25
    ]

    for i, test_date in enumerate(test_dates):
        print(f"\n{i+1}. 테스트 날짜: {test_date}")

        # 학생 생성
        test_student = Student()
        test_student.name = f"날짜테스트_{test_date}"
        test_student.weekdays = ["월요일"]
        test_student.total_weeks = 1
        test_student.start_date = test_date
        test_student.created_at = datetime.now()
        test_student.is_active = True

        print(f"   원본 날짜: {test_student.start_date}")
        print(f"   타입: {type(test_student.start_date)}")

        # 업로드
        print("   업로드 중...")
        success, message = api.sync_students([test_student])
        if not success:
            print(f"   업로드 실패: {message}")
            continue

        # 다운로드
        print("   다운로드 중...")
        success, message, students = api.get_students_from_sheets()
        if not success:
            print(f"   다운로드 실패: {message}")
            continue

        # 비교
        found = None
        for student in students:
            if f"날짜테스트_{test_date}" in student.name:
                found = student
                break

        if found:
            print(f"   복원 날짜: {found.start_date}")
            print(f"   타입: {type(found.start_date)}")

            if str(test_student.start_date) == str(found.start_date):
                print(f"   [OK] 성공: 날짜가 정확히 일치")
            else:
                print(f"   [ERROR] 실패: 날짜 불일치")
                print(f"       원본: {test_student.start_date}")
                print(f"       복원: {found.start_date}")

                # 날짜 차이 계산
                if hasattr(found, 'start_date') and found.start_date:
                    try:
                        original_date = datetime.strptime(str(test_student.start_date), '%Y-%m-%d').date()
                        if isinstance(found.start_date, str):
                            restored_date = datetime.strptime(found.start_date, '%Y-%m-%d').date()
                        else:
                            restored_date = found.start_date

                        diff = (restored_date - original_date).days
                        print(f"       차이: {diff}일")
                    except Exception as e:
                        print(f"       차이 계산 실패: {e}")
        else:
            print(f"   데이터를 찾을 수 없음")

if __name__ == "__main__":
    try:
        test_specific_dates()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()