#!/usr/bin/env python3
"""
실제 구글 시트 동기화 테스트
"""

import sys
import os

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student, AppData
from src.google_sheets_api import GoogleSheetsAPI
from datetime import date, datetime

def test_real_sync():
    """실제 구글 시트와 동기화 테스트"""

    print("=== 실제 구글 시트 동기화 테스트 ===\n")

    # 1. API 초기화
    webapp_url = "https://script.google.com/macros/s/AKfycbxT7joPlgV9cZv_kdo5uHXoyV22v8q-nWU-aRKAuOlRaq0eHqh3w68HMLyovy8LgJVbMw/exec"
    api = GoogleSheetsAPI(webapp_url)

    # 2. 연결 테스트
    print("1. 연결 테스트...")
    success, message = api.test_connection()
    print(f"   결과: {success}")
    print(f"   메시지: {message}\n")

    if not success:
        print("연결 테스트 실패. 테스트를 중단합니다.")
        return

    # 3. 테스트 학생 생성
    test_student = Student()
    test_student.name = "홍길동_테스트"
    test_student.weekdays = ["목요일", "금요일"]  # 원본 요일
    test_student.total_weeks = 12
    test_student.start_date = date(2024, 1, 1)
    test_student.created_at = datetime.now()
    test_student.is_active = True
    test_student.color = "#FF5733"

    print(f"2. 테스트 학생 데이터:")
    print(f"   이름: {test_student.name}")
    print(f"   요일: {test_student.weekdays}")
    print(f"   요일 개수: {len(test_student.weekdays)}")

    # 4. 학생 데이터 업로드
    print(f"\n3. 구글 시트에 업로드...")
    success, message = api.sync_students([test_student])
    print(f"   결과: {success}")
    print(f"   메시지: {message}")

    if not success:
        print("업로드 실패. 테스트를 중단합니다.")
        return

    # 5. 구글 시트에서 다운로드
    print(f"\n4. 구글 시트에서 다운로드...")
    success, message, students = api.get_students_from_sheets()
    print(f"   결과: {success}")
    print(f"   메시지: {message}")
    print(f"   학생 수: {len(students)}")

    if not success or not students:
        print("다운로드 실패 또는 데이터 없음.")
        return

    # 6. 원본과 복원된 데이터 비교
    found_student = None
    for student in students:
        if student.name == "홍길동_테스트":
            found_student = student
            break

    if not found_student:
        print("테스트 학생을 찾을 수 없습니다.")
        return

    print(f"\n5. 복원된 학생 데이터:")
    print(f"   이름: {found_student.name}")
    print(f"   요일: {found_student.weekdays}")
    print(f"   요일 개수: {len(found_student.weekdays)}")

    # 7. 비교 결과
    print(f"\n=== 비교 결과 ===")
    print(f"원본 요일:   {test_student.weekdays}")
    print(f"복원 요일:   {found_student.weekdays}")
    print(f"일치 여부:   {test_student.weekdays == found_student.weekdays}")

    if test_student.weekdays != found_student.weekdays:
        print(f"[ERROR] 요일 데이터 불일치 발견!")
        print(f"   원본 길이: {len(test_student.weekdays)}")
        print(f"   복원 길이: {len(found_student.weekdays)}")

        # 요일별 비교
        max_len = max(len(test_student.weekdays), len(found_student.weekdays))
        for i in range(max_len):
            orig = test_student.weekdays[i] if i < len(test_student.weekdays) else "[없음]"
            rest = found_student.weekdays[i] if i < len(found_student.weekdays) else "[없음]"
            status = "[OK]" if orig == rest else "[ERROR]"
            print(f"   인덱스 {i}: '{orig}' -> '{rest}' {status}")

        # 원본에서 요일 인덱스 확인
        weekdays_order = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        print(f"\n요일 순서 분석:")
        print(f"   원본:")
        for day in test_student.weekdays:
            idx = weekdays_order.index(day) if day in weekdays_order else -1
            print(f"     {day} -> 인덱스 {idx}")
        print(f"   복원:")
        for day in found_student.weekdays:
            idx = weekdays_order.index(day) if day in weekdays_order else -1
            print(f"     {day} -> 인덱스 {idx}")

    else:
        print(f"[OK] 요일 데이터가 정확히 일치합니다!")

    # 8. 기타 필드 비교
    print(f"\n=== 기타 필드 비교 ===")
    fields_to_check = [
        ('이름', 'name'),
        ('총 주차', 'total_weeks'),
        ('시작일', 'start_date'),
        ('활성 상태', 'is_active'),
        ('색상', 'color')
    ]

    for field_name, attr_name in fields_to_check:
        orig_value = getattr(test_student, attr_name)
        rest_value = getattr(found_student, attr_name)
        status = "[OK]" if orig_value == rest_value else "[ERROR]"
        print(f"{field_name}: {orig_value} -> {rest_value} {status}")

if __name__ == "__main__":
    try:
        test_real_sync()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()