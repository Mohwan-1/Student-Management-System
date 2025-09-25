#!/usr/bin/env python3
"""
간단한 API 테스트
"""

import sys
import os
import requests
import json

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import Student, AppData
from datetime import date, datetime

def test_simple_api():
    """간단한 API 테스트"""

    print("=== 간단한 API 테스트 ===\n")

    webapp_url = "https://script.google.com/macros/s/AKfycbxT7joPlgV9cZv_kdo5uHXoyV22v8q-nWU-aRKAuOlRaq0eHqh3w68HMLyovy8LgJVbMw/exec"

    # 1. 연결 테스트
    print("1. 연결 테스트...")
    try:
        payload = {'action': 'get_students'}

        response = requests.post(
            webapp_url,
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   HTTP 상태: {response.status_code}")
        print(f"   응답 텍스트: {response.text[:200]}...")

        if response.status_code == 200:
            result = response.json()
            print(f"   JSON 파싱 성공:")
            print(f"   - success: {result.get('success')}")
            print(f"   - message: {result.get('message')}")
            print(f"   - data: {len(result.get('data', []))} items")
        else:
            print("   HTTP 오류")
            return

    except Exception as e:
        print(f"   오류: {e}")
        return

    # 2. 단순한 학생 데이터 동기화 테스트
    print("\n2. 단순한 동기화 테스트...")

    test_student = Student()
    test_student.name = "API테스트"
    test_student.weekdays = ["월요일", "화요일"]
    test_student.total_weeks = 1
    test_student.start_date = date(2024, 1, 1)
    test_student.created_at = datetime.now()
    test_student.is_active = True

    app_data = AppData()
    app_data.students = [test_student]
    app_data.schedules = []  # 빈 스케줄

    try:
        payload = {
            'action': 'full_sync',
            'data': app_data.to_dict()
        }

        print(f"   전송 데이터: {json.dumps(payload, indent=2, ensure_ascii=False, default=str)}")

        response = requests.post(
            webapp_url,
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   HTTP 상태: {response.status_code}")
        print(f"   응답 텍스트: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"   결과:")
            print(f"   - success: {result.get('success')}")
            print(f"   - message: {result.get('message')}")

    except Exception as e:
        print(f"   오류: {e}")

if __name__ == "__main__":
    try:
        test_simple_api()
    except Exception as e:
        print(f"테스트 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()