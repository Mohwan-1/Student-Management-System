#!/usr/bin/env python3
"""
요일 데이터 동기화 테스트 스크립트
"""

import sys
import os

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student
from src.google_sheets_api import GoogleSheetsAPI
from datetime import date, datetime

def test_weekdays_conversion():
    """요일 데이터 변환 테스트"""

    print("=== 요일 데이터 동기화 테스트 ===\n")

    # 1. 테스트 학생 데이터 생성
    test_student = Student()
    test_student.name = "홍길동"
    test_student.weekdays = ["목요일", "금요일"]  # 원본 데이터
    test_student.start_date = date(2024, 1, 1)
    test_student.created_at = datetime.now()

    print(f"1. 원본 학생 데이터:")
    print(f"   이름: {test_student.name}")
    print(f"   요일: {test_student.weekdays}")
    print(f"   요일 문자열: {', '.join(test_student.weekdays)}")

    # 2. to_dict() 변환
    student_dict = test_student.to_dict()
    print(f"\n2. to_dict() 변환 결과:")
    print(f"   weekdays: {student_dict['weekdays']}")

    # 3. 구글 시트 업로드 시뮬레이션 (join 과정)
    weekdays_string = ', '.join(student_dict['weekdays'])
    print(f"\n3. 구글 시트 업로드 시 (join):")
    print(f"   요일 문자열: '{weekdays_string}'")

    # 4. 구글 시트 다운로드 시뮬레이션 (split 과정)
    weekdays_split = weekdays_string.split(', ') if weekdays_string else []
    print(f"\n4. 구글 시트 다운로드 시 (split):")
    print(f"   분할된 요일: {weekdays_split}")

    # 5. from_dict() 복원
    restored_dict = {
        "id": student_dict["id"],
        "name": student_dict["name"],
        "total_weeks": student_dict["total_weeks"],
        "weekdays": weekdays_split,  # 구글 시트에서 가져온 데이터
        "start_date": student_dict["start_date"],
        "created_at": student_dict["created_at"],
        "is_active": student_dict["is_active"],
        "color": student_dict["color"]
    }

    restored_student = Student.from_dict(restored_dict)
    print(f"\n5. from_dict() 복원 결과:")
    print(f"   이름: {restored_student.name}")
    print(f"   요일: {restored_student.weekdays}")

    # 6. 비교 결과
    print(f"\n=== 비교 결과 ===")
    print(f"원본 요일:   {test_student.weekdays}")
    print(f"복원 요일:   {restored_student.weekdays}")
    print(f"일치 여부:   {test_student.weekdays == restored_student.weekdays}")

    if test_student.weekdays != restored_student.weekdays:
        print(f"[ERROR] 요일 데이터가 일치하지 않습니다!")
        print(f"   원본 길이: {len(test_student.weekdays)}")
        print(f"   복원 길이: {len(restored_student.weekdays)}")

        for i, (orig, rest) in enumerate(zip(test_student.weekdays, restored_student.weekdays)):
            if orig != rest:
                print(f"   인덱스 {i}: '{orig}' -> '{rest}'")
    else:
        print(f"[OK] 요일 데이터가 정확히 일치합니다!")

def test_edge_cases():
    """엣지 케이스 테스트"""

    print(f"\n=== 엣지 케이스 테스트 ===")

    test_cases = [
        ["월요일"],
        ["월요일", "수요일", "금요일"],
        ["토요일", "일요일"],
        [],  # 빈 배열
        ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],  # 모든 요일
    ]

    for i, weekdays in enumerate(test_cases):
        print(f"\n테스트 케이스 {i+1}: {weekdays}")

        # Join → Split 과정
        weekdays_string = ', '.join(weekdays) if weekdays else ''
        weekdays_restored = weekdays_string.split(', ') if weekdays_string else []

        print(f"  문자열화: '{weekdays_string}'")
        print(f"  복원: {weekdays_restored}")
        print(f"  일치: {weekdays == weekdays_restored}")

        if weekdays != weekdays_restored:
            print(f"  [ERROR] 불일치!")
        else:
            print(f"  [OK] 일치!")

if __name__ == "__main__":
    try:
        test_weekdays_conversion()
        test_edge_cases()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()