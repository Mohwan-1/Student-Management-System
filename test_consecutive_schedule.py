#!/usr/bin/env python3
"""
연속 요일 스케줄 생성 테스트
"""

import sys
import os
from datetime import date, datetime

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student
from src.data_manager import DataManager

def test_consecutive_weekdays():
    """연속 요일 스케줄 생성 테스트"""

    print("=== 연속 요일 스케줄 생성 테스트 ===\n")

    # 데이터 매니저 생성
    data_manager = DataManager()

    # 테스트 케이스들
    test_cases = [
        {
            "name": "홍길동_수목연속",
            "weekdays": ["수요일", "목요일"],
            "start_date": date(2024, 1, 1),  # 2024-01-01은 월요일
            "total_weeks": 3
        },
        {
            "name": "김영희_화수목연속",
            "weekdays": ["화요일", "수요일", "목요일"],
            "start_date": date(2024, 1, 1),
            "total_weeks": 2
        },
        {
            "name": "이철수_금토연속",
            "weekdays": ["금요일", "토요일"],
            "start_date": date(2024, 1, 5),  # 2024-01-05는 금요일
            "total_weeks": 2
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"{i}. 테스트 케이스: {case['name']}")
        print(f"   요일: {case['weekdays']}")
        print(f"   시작일: {case['start_date']} ({get_weekday_name(case['start_date'])})")
        print(f"   총 주차: {case['total_weeks']}")

        # 학생 생성
        student = Student()
        student.name = case['name']
        student.weekdays = case['weekdays']
        student.start_date = case['start_date']
        student.total_weeks = case['total_weeks']
        student.created_at = datetime.now()
        student.is_active = True

        # 기존 데이터 초기화
        data_manager.data.students = []
        data_manager.data.schedules = []

        # 스케줄 생성
        data_manager.data.students.append(student)
        data_manager._generate_schedules_for_student(student)

        # 결과 출력
        schedules = [s for s in data_manager.data.schedules if s.student_id == student.id]
        schedules.sort(key=lambda x: x.scheduled_date)

        print(f"   생성된 스케줄:")
        for schedule in schedules:
            weekday = get_weekday_name(schedule.scheduled_date)
            week_info = get_week_number(case['start_date'], schedule.scheduled_date)
            print(f"     {schedule.week_number}차시: {schedule.scheduled_date} ({weekday}) - {week_info}")

        # 검증
        verify_schedule(case, schedules)
        print()

def get_weekday_name(date_obj):
    """날짜를 요일명으로 변환"""
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return weekdays[date_obj.weekday()]

def get_week_number(start_date, target_date):
    """시작일 기준 주차 계산"""
    days_diff = (target_date - start_date).days
    week_num = (days_diff // 7) + 1
    return f"{week_num}주차"

def verify_schedule(case, schedules):
    """스케줄 검증"""
    weekdays = case['weekdays']
    expected_total = len(weekdays) * case['total_weeks']

    if len(schedules) != expected_total:
        print(f"   [ERROR] 스케줄 개수 불일치: 예상 {expected_total}개, 실제 {len(schedules)}개")
        return False

    # 주차별로 그룹핑
    weeks = {}
    for schedule in schedules:
        week_key = get_week_number(case['start_date'], schedule.scheduled_date)
        if week_key not in weeks:
            weeks[week_key] = []
        weeks[week_key].append(schedule)

    print(f"   [검증] 주차별 스케줄:")
    all_correct = True

    for week_key in sorted(weeks.keys()):
        week_schedules = sorted(weeks[week_key], key=lambda x: x.scheduled_date)
        week_weekdays = [get_weekday_name(s.scheduled_date) for s in week_schedules]

        if week_weekdays == weekdays:
            print(f"     {week_key}: {week_weekdays} [OK]")
        else:
            print(f"     {week_key}: {week_weekdays} [ERROR] (예상: {weekdays})")
            all_correct = False

    if all_correct:
        print(f"   [OK] 모든 스케줄이 올바르게 생성됨")
    else:
        print(f"   [ERROR] 스케줄 생성에 문제가 있음")

    return all_correct

if __name__ == "__main__":
    try:
        test_consecutive_weekdays()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()