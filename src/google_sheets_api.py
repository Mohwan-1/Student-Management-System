import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .models import Student, Schedule, AppData


class GoogleSheetsAPI:
    """구글 시트와 연동하기 위한 API 클래스"""

    def __init__(self, webapp_url: str):
        self.webapp_url = webapp_url
        self.timeout = 30  # 30초 타임아웃

    def _make_request(self, action: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """구글 앱스 스크립트로 HTTP 요청 전송"""
        try:
            payload = {
                'action': action,
                'timestamp': datetime.now().isoformat()
            }

            if data:
                payload['data'] = data

            response = requests.post(
                self.webapp_url,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'success': False,
                    'message': f'HTTP 오류: {response.status_code}',
                    'timestamp': datetime.now().isoformat()
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': '요청 시간 초과 (30초)',
                'timestamp': datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'네트워크 오류: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'알 수 없는 오류: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }

    def test_connection(self) -> Tuple[bool, str]:
        """연결 테스트"""
        try:
            result = self._make_request('get_students')
            if result['success']:
                return True, "구글 시트 연결 성공"
            else:
                return False, f"연결 실패: {result['message']}"
        except Exception as e:
            return False, f"연결 테스트 실패: {str(e)}"

    def sync_students(self, students: List[Student]) -> Tuple[bool, str]:
        """학생 데이터를 구글 시트에 동기화"""
        try:
            students_data = [student.to_dict() for student in students]
            result = self._make_request('sync_students', students_data)

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"학생 동기화 실패: {str(e)}"

    def sync_schedules(self, schedules: List[Schedule]) -> Tuple[bool, str]:
        """스케줄 데이터를 구글 시트에 동기화"""
        try:
            schedules_data = [schedule.to_dict() for schedule in schedules]
            result = self._make_request('sync_schedules', schedules_data)

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"스케줄 동기화 실패: {str(e)}"

    def full_sync(self, app_data: AppData) -> Tuple[bool, str]:
        """전체 데이터 동기화"""
        try:
            data = app_data.to_dict()
            result = self._make_request('full_sync', data)

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"전체 동기화 실패: {str(e)}"

    def get_students_from_sheets(self) -> Tuple[bool, str, List[Student]]:
        """구글 시트에서 학생 데이터 가져오기"""
        try:
            result = self._make_request('get_students')

            if result['success']:
                students_data = result.get('data', [])
                students = []

                for student_dict in students_data:
                    try:
                        student = Student.from_dict(student_dict)
                        students.append(student)
                    except Exception as e:
                        print(f"학생 데이터 파싱 오류: {e}")
                        continue

                return True, result['message'], students
            else:
                return False, result['message'], []

        except Exception as e:
            return False, f"학생 데이터 가져오기 실패: {str(e)}", []

    def get_schedules_from_sheets(self) -> Tuple[bool, str, List[Schedule]]:
        """구글 시트에서 스케줄 데이터 가져오기"""
        try:
            result = self._make_request('get_schedules')

            if result['success']:
                schedules_data = result.get('data', [])
                schedules = []

                for schedule_dict in schedules_data:
                    try:
                        schedule = Schedule.from_dict(schedule_dict)
                        schedules.append(schedule)
                    except Exception as e:
                        print(f"스케줄 데이터 파싱 오류: {e}")
                        continue

                return True, result['message'], schedules
            else:
                return False, result['message'], []

        except Exception as e:
            return False, f"스케줄 데이터 가져오기 실패: {str(e)}", []

    def update_student(self, student: Student) -> Tuple[bool, str]:
        """개별 학생 업데이트"""
        try:
            student_data = student.to_dict()
            result = self._make_request('update_student', student_data)

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"학생 업데이트 실패: {str(e)}"

    def update_schedule(self, schedule: Schedule) -> Tuple[bool, str]:
        """개별 스케줄 업데이트"""
        try:
            schedule_data = schedule.to_dict()
            result = self._make_request('update_schedule', schedule_data)

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"스케줄 업데이트 실패: {str(e)}"

    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """학생 삭제"""
        try:
            result = self._make_request('delete_student', {'student_id': student_id})

            if result['success']:
                return True, result['message']
            else:
                return False, result['message']

        except Exception as e:
            return False, f"학생 삭제 실패: {str(e)}"

    def create_backup(self) -> Tuple[bool, str, Optional[Dict]]:
        """백업 생성"""
        try:
            result = self._make_request('create_backup')

            if result['success']:
                backup_info = result.get('data', {})
                return True, result['message'], backup_info
            else:
                return False, result['message'], None

        except Exception as e:
            return False, f"백업 생성 실패: {str(e)}", None

    def get_data_stats(self) -> Tuple[bool, str, Optional[Dict]]:
        """데이터 통계 조회"""
        try:
            result = self._make_request('get_data_stats')

            if result['success']:
                stats = result.get('data', {})
                return True, result['message'], stats
            else:
                return False, result['message'], None

        except Exception as e:
            return False, f"통계 조회 실패: {str(e)}", None

    def sync_from_local_to_sheets(self, app_data: AppData) -> Tuple[bool, str]:
        """로컬 데이터를 구글 시트로 업로드"""
        success, message = self.full_sync(app_data)
        return success, f"로컬 → 구글 시트: {message}"

    def sync_from_sheets_to_local(self) -> Tuple[bool, str, Optional[AppData]]:
        """구글 시트에서 로컬로 데이터 다운로드"""
        try:
            # 학생 데이터 가져오기
            students_success, students_msg, students = self.get_students_from_sheets()
            if not students_success:
                return False, f"학생 데이터 가져오기 실패: {students_msg}", None

            # 스케줄 데이터 가져오기
            schedules_success, schedules_msg, schedules = self.get_schedules_from_sheets()
            if not schedules_success:
                return False, f"스케줄 데이터 가져오기 실패: {schedules_msg}", None

            # AppData 객체 생성
            app_data = AppData()
            app_data.students = students
            app_data.schedules = schedules
            app_data.metadata = {
                "version": "1.0",
                "last_sync": datetime.now().isoformat(),
                "sync_source": "google_sheets"
            }

            return True, f"구글 시트 → 로컬: {len(students)}명 학생, {len(schedules)}개 스케줄", app_data

        except Exception as e:
            return False, f"구글 시트에서 로컬로 동기화 실패: {str(e)}", None


# 싱글톤 인스턴스 생성을 위한 클래스
class GoogleSheetsManager:
    """구글 시트 매니저 싱글톤"""

    _instance = None
    _api = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleSheetsManager, cls).__new__(cls)
        return cls._instance

    def initialize(self, webapp_url: str):
        """API 초기화"""
        self._api = GoogleSheetsAPI(webapp_url)

    def get_api(self) -> Optional[GoogleSheetsAPI]:
        """API 인스턴스 반환"""
        return self._api

    def is_initialized(self) -> bool:
        """초기화 여부 확인"""
        return self._api is not None