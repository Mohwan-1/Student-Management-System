#!/usr/bin/env python3
"""
스케줄 동기화 테스트 - 요일 변경 문제 재현
"""

import sys
import os

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student, Schedule, AppData
from src.google_sheets_api import GoogleSheetsAPI
from src.data_manager import DataManager
from datetime import date, datetime, timedelta

def test_schedule_generation_consistency():
    """스케줄 생성 일관성 테스트"""

    print("=== 스케줄 생성 일관성 테스트 ===\n")

    # 1. 데이터 매니저 생성
    data_manager = DataManager()

    # 2. 테스트 학생 생성
    test_student = Student()
    test_student.name = "홍길동_스케줄테스트"
    test_student.weekdays = ["목요일", "금요일"]  # 원본 요일
    test_student.total_weeks = 4  # 4주만 테스트
    test_student.start_date = date(2024, 1, 1)  # 2024-01-01은 월요일
    test_student.created_at = datetime.now()
    test_student.is_active = True

    print(f"1. 테스트 학생:")
    print(f"   이름: {test_student.name}")
    print(f"   요일: {test_student.weekdays}")
    print(f"   시작일: {test_student.start_date} ({get_weekday_name(test_student.start_date)})")
    print(f"   총 주차: {test_student.total_weeks}")

    # 3. 로컬에서 스케줄 생성
    print(f"\n2. 로컬 스케줄 생성...")
    data_manager.data.students = [test_student]
    data_manager._generate_schedules_for_student(test_student)

    local_schedules = [s for s in data_manager.data.schedules if s.student_id == test_student.id]
    print(f"   생성된 스케줄 수: {len(local_schedules)}")

    print(f"   로컬 스케줄:")
    for schedule in sorted(local_schedules, key=lambda x: x.week_number):
        weekday_name = get_weekday_name(schedule.scheduled_date)
        print(f"     {schedule.week_number}주차: {schedule.scheduled_date} ({weekday_name})")

    # 4. 구글 시트에 업로드
    print(f"\n3. 구글 시트 동기화...")
    webapp_url = "https://script.google.com/macros/s/AKfycbxT7joPlgV9cZv_kdo5uHXoyV22v8q-nWU-aRKAuOlRaq0eHqh3w68HMLyovy8LgJVbMw/exec"
    api = GoogleSheetsAPI(webapp_url)

    # 학생과 스케줄 모두 업로드
    app_data = AppData()
    app_data.students = [test_student]
    app_data.schedules = local_schedules

    success, message = api.full_sync(app_data)
    print(f"   업로드 결과: {success}")
    print(f"   메시지: {message}")

    if not success:
        print("업로드 실패. 테스트 중단.")
        return

    # 5. 구글 시트에서 다운로드
    print(f"\n4. 구글 시트에서 다운로드...")
    success, message, downloaded_app_data = api.sync_from_sheets_to_local()
    print(f"   다운로드 결과: {success}")
    print(f"   메시지: {message}")

    if not success or not downloaded_app_data:
        print("다운로드 실패.")
        return

    # 6. 다운로드된 데이터 분석
    downloaded_students = downloaded_app_data.students
    downloaded_schedules = downloaded_app_data.schedules

    found_student = None
    for student in downloaded_students:
        if "홍길동_스케줄테스트" in student.name:
            found_student = student
            break

    if not found_student:
        print("테스트 학생을 찾을 수 없습니다.")
        return

    student_schedules = [s for s in downloaded_schedules if s.student_id == found_student.id]

    print(f"\n5. 다운로드된 데이터:")
    print(f"   학생 요일: {found_student.weekdays}")
    print(f"   스케줄 수: {len(student_schedules)}")
    print(f"   다운로드된 스케줄:")
    for schedule in sorted(student_schedules, key=lambda x: x.week_number):
        weekday_name = get_weekday_name(schedule.scheduled_date)
        print(f"     {schedule.week_number}주차: {schedule.scheduled_date} ({weekday_name})")

    # 7. 비교 분석
    print(f"\n=== 비교 분석 ===")
    print(f"원본 학생 요일: {test_student.weekdays}")
    print(f"다운로드 학생 요일: {found_student.weekdays}")
    print(f"학생 요일 일치: {test_student.weekdays == found_student.weekdays}")

    # 스케줄 요일 분석
    print(f"\n스케줄 요일 분석:")
    print(f"로컬 스케줄 요일:")
    local_weekdays = []
    for schedule in sorted(local_schedules, key=lambda x: x.week_number):
        weekday_name = get_weekday_name(schedule.scheduled_date)
        local_weekdays.append(weekday_name)
        print(f"  {schedule.week_number}주차: {weekday_name}")

    print(f"다운로드 스케줄 요일:")
    downloaded_weekdays = []
    for schedule in sorted(student_schedules, key=lambda x: x.week_number):
        weekday_name = get_weekday_name(schedule.scheduled_date)
        downloaded_weekdays.append(weekday_name)
        print(f"  {schedule.week_number}주차: {weekday_name}")

    print(f"\n스케줄 요일 일치: {local_weekdays == downloaded_weekdays}")

    # 불일치 항목 상세 분석
    if local_weekdays != downloaded_weekdays:
        print(f"\n[ERROR] 스케줄 요일 불일치 발견!")
        max_len = max(len(local_weekdays), len(downloaded_weekdays))
        for i in range(max_len):
            local_day = local_weekdays[i] if i < len(local_weekdays) else "[없음]"
            downloaded_day = downloaded_weekdays[i] if i < len(downloaded_weekdays) else "[없음]"
            status = "[OK]" if local_day == downloaded_day else "[ERROR]"
            print(f"  {i+1}주차: {local_day} -> {downloaded_day} {status}")

def get_weekday_name(date_obj):
    """날짜를 요일명으로 변환"""
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return weekdays[date_obj.weekday()]

if __name__ == "__main__":
    try:
        test_schedule_generation_consistency()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()