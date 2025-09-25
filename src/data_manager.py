import os
import sys
import shutil
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from PySide6.QtCore import QObject, Signal

from .crypto_utils import CryptoManager
from .models import Student, Schedule, AppData
from .google_sheets_api import GoogleSheetsManager


class DataManager(QObject):
    dataChanged = Signal()
    syncStatusChanged = Signal(str)  # 동기화 상태 변경 시그널

    def __init__(self):
        super().__init__()
        self.crypto_manager = CryptoManager()
        self.data = AppData()
        self.password: Optional[str] = None
        self._data_file_path = self._get_data_file_path()
        self._backup_folder = self._data_file_path.parent / "backups"
        self._backup_folder.mkdir(exist_ok=True)

        # 구글 시트 매니저 초기화
        self.sheets_manager = GoogleSheetsManager()
        self._initialize_google_sheets()

    def _get_data_file_path(self) -> Path:
        # exe 파일이 있는 폴더에 데이터 저장
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 exe 파일인 경우
            exe_dir = Path(sys.executable).parent
        else:
            # 개발 환경에서 실행하는 경우
            exe_dir = Path(__file__).parent.parent

        return exe_dir / '.env'

    def has_existing_data(self) -> bool:
        return self._data_file_path.exists()

    def set_password(self, password: str) -> bool:
        self.password = password
        return True

    def verify_password(self, password: str) -> bool:
        if not self.has_existing_data():
            return False

        try:
            with open(self._data_file_path, 'rb') as f:
                encrypted_data = f.read()
            return self.crypto_manager.verify_password(encrypted_data, password)
        except Exception:
            return False

    def load_data(self, password: str) -> bool:
        if not self.has_existing_data():
            self.password = password
            return True

        try:
            with open(self._data_file_path, 'rb') as f:
                encrypted_data = f.read()

            data_dict = self.crypto_manager.decrypt_data(encrypted_data, password)
            self.data = AppData.from_dict(data_dict)
            self.password = password
            self.dataChanged.emit()
            return True
        except Exception as e:
            print(f"Failed to load data: {e}")
            return False

    def save_data(self) -> bool:
        if not self.password:
            return False

        try:
            encrypted_data = self.crypto_manager.encrypt_data(
                self.data.to_dict(),
                self.password
            )

            temp_file = self._data_file_path.with_suffix('.tmp')
            with open(temp_file, 'wb') as f:
                f.write(encrypted_data)

            if self._data_file_path.exists():
                shutil.move(str(self._data_file_path), str(temp_file.with_suffix('.bak')))

            shutil.move(str(temp_file), str(self._data_file_path))

            if temp_file.with_suffix('.bak').exists():
                temp_file.with_suffix('.bak').unlink()

            self.data.metadata["last_backup"] = datetime.now().isoformat()
            self.dataChanged.emit()
            return True
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False

    def create_backup(self) -> bool:
        if not self.has_existing_data():
            return False

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self._backup_folder / f"backup_{timestamp}.sms"
            shutil.copy2(str(self._data_file_path), str(backup_file))

            self._cleanup_old_backups()
            return True
        except Exception as e:
            print(f"Failed to create backup: {e}")
            return False

    def _cleanup_old_backups(self):
        try:
            backup_files = sorted(self._backup_folder.glob("backup_*.sms"))
            if len(backup_files) > 10:
                for old_backup in backup_files[:-10]:
                    old_backup.unlink()
        except Exception:
            pass

    def restore_from_backup(self, backup_file_path: str) -> bool:
        """백업 파일에서 데이터를 복원"""
        try:
            from pathlib import Path
            backup_path = Path(backup_file_path)

            if not backup_path.exists():
                print(f"Backup file not found: {backup_file_path}")
                return False

            # 현재 데이터 백업 (복원 실패 시 롤백용)
            rollback_file = None
            if self._data_file_path.exists():
                rollback_file = self._data_file_path.with_suffix('.rollback')
                shutil.copy2(str(self._data_file_path), str(rollback_file))

            try:
                # 백업 파일을 현재 데이터 파일로 복사
                shutil.copy2(str(backup_path), str(self._data_file_path))

                # 복원된 데이터 로드 시도
                if self.password:
                    success = self.load_data(self.password)
                    if success:
                        # 롤백 파일 삭제 (복원 성공)
                        if rollback_file and rollback_file.exists():
                            rollback_file.unlink()

                        print(f"Successfully restored backup from: {backup_file_path}")
                        return True
                    else:
                        # 로드 실패 - 롤백
                        if rollback_file and rollback_file.exists():
                            shutil.move(str(rollback_file), str(self._data_file_path))
                        print("Failed to load restored data - rolled back")
                        return False
                else:
                    print("No password set for data restoration")
                    return False

            except Exception as e:
                # 복원 실패 - 롤백
                if rollback_file and rollback_file.exists():
                    shutil.move(str(rollback_file), str(self._data_file_path))
                print(f"Restore failed, rolled back: {e}")
                return False

        except Exception as e:
            print(f"Failed to restore from backup: {e}")
            return False

    def add_student(self, student: Student) -> bool:
        try:
            self.data.students.append(student)
            self._generate_schedules_for_student(student)
            self.save_data()
            return True
        except Exception as e:
            print(f"Failed to add student: {e}")
            return False

    def update_student(self, student: Student) -> bool:
        try:
            for i, existing_student in enumerate(self.data.students):
                if existing_student.id == student.id:
                    self.data.students[i] = student
                    self._regenerate_schedules_for_student(student)
                    self.save_data()
                    return True
            return False
        except Exception as e:
            print(f"Failed to update student: {e}")
            return False

    def remove_student(self, student_id: str) -> bool:
        try:
            self.data.students = [s for s in self.data.students if s.id != student_id]
            self.data.schedules = [s for s in self.data.schedules if s.student_id != student_id]
            self.save_data()
            return True
        except Exception as e:
            print(f"Failed to remove student: {e}")
            return False

    def get_students(self) -> List[Student]:
        return self.data.students

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        for student in self.data.students:
            if student.id == student_id:
                return student
        return None

    def get_schedules(self) -> List[Schedule]:
        return self.data.schedules

    def get_schedules_for_date(self, target_date: date) -> List[Schedule]:
        return [s for s in self.data.schedules if s.scheduled_date == target_date]

    def get_schedules_for_student(self, student_id: str) -> List[Schedule]:
        return [s for s in self.data.schedules if s.student_id == student_id]

    def move_schedule(self, schedule_id: str, new_date: date) -> bool:
        try:
            for i, schedule in enumerate(self.data.schedules):
                if schedule.id == schedule_id:
                    old_date = schedule.scheduled_date
                    self.data.schedules[i].scheduled_date = new_date
                    self.data.schedules[i].updated_at = datetime.now()

                    student = self.get_student_by_id(schedule.student_id)
                    if student:
                        self._reschedule_following_schedules(student, schedule, old_date)

                    self.save_data()
                    return True
            return False
        except Exception as e:
            print(f"Failed to move schedule: {e}")
            return False

    def _generate_schedules_for_student(self, student: Student):
        weekday_map = {
            "월요일": 0, "화요일": 1, "수요일": 2, "목요일": 3,
            "금요일": 4, "토요일": 5, "일요일": 6
        }

        weekday_indices = [weekday_map[day] for day in student.weekdays if day in weekday_map]
        if not weekday_indices:
            return

        # 요일들을 정렬 (월요일=0 ~ 일요일=6 순서)
        weekday_indices.sort()

        # 시작일 기준으로 첫 주의 시작 월요일 찾기
        start_date = student.start_date
        days_since_monday = start_date.weekday()  # 월요일=0, 일요일=6
        week_start = start_date - timedelta(days=days_since_monday)

        schedule_count = 0
        for week_num in range(1, student.total_weeks + 1):
            current_week_start = week_start + timedelta(weeks=week_num - 1)

            for weekday_idx in weekday_indices:
                # 해당 주의 해당 요일 날짜 계산
                schedule_date = current_week_start + timedelta(days=weekday_idx)

                # 시작일 이전의 날짜는 건너뛰기
                if schedule_date < start_date:
                    continue

                schedule_count += 1
                schedule = Schedule(
                    student_id=student.id,
                    week_number=schedule_count,
                    scheduled_date=schedule_date
                )

                self.data.schedules.append(schedule)

    def _regenerate_schedules_for_student(self, student: Student):
        self.data.schedules = [s for s in self.data.schedules if s.student_id != student.id]
        self._generate_schedules_for_student(student)

    def _reschedule_following_schedules(self, student: Student, moved_schedule: Schedule, old_date: date):
        weekday_map = {
            "월요일": 0, "화요일": 1, "수요일": 2, "목요일": 3,
            "금요일": 4, "토요일": 5, "일요일": 6
        }

        weekday_indices = [weekday_map[day] for day in student.weekdays if day in weekday_map]
        if not weekday_indices:
            return

        student_schedules = sorted(
            [s for s in self.data.schedules if s.student_id == student.id and s.week_number > moved_schedule.week_number],
            key=lambda x: x.week_number
        )

        if not student_schedules:
            return

        current_date = moved_schedule.scheduled_date
        current_weekday_idx = student.weekdays.index(
            [k for k, v in weekday_map.items() if v == moved_schedule.scheduled_date.weekday()][0]
        ) if moved_schedule.scheduled_date.weekday() in weekday_indices else 0

        for schedule in student_schedules:
            current_weekday_idx = (current_weekday_idx + 1) % len(weekday_indices)
            target_weekday = weekday_indices[current_weekday_idx]

            days_ahead = target_weekday - current_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7

            new_date = current_date + timedelta(days=days_ahead)

            for i, s in enumerate(self.data.schedules):
                if s.id == schedule.id:
                    self.data.schedules[i].scheduled_date = new_date
                    self.data.schedules[i].updated_at = datetime.now()
                    break

            current_date = new_date

    def mark_schedule_completed(self, schedule_id: str, completed: bool = True) -> bool:
        try:
            for i, schedule in enumerate(self.data.schedules):
                if schedule.id == schedule_id:
                    self.data.schedules[i].is_completed = completed
                    self.data.schedules[i].updated_at = datetime.now()
                    self.save_data()
                    return True
            return False
        except Exception as e:
            print(f"Failed to mark schedule as completed: {e}")
            return False

    def update_schedule_memo(self, schedule_id: str, memo: str) -> bool:
        """일정의 메모를 업데이트"""
        try:
            for i, schedule in enumerate(self.data.schedules):
                if schedule.id == schedule_id:
                    old_memo = self.data.schedules[i].memo
                    self.data.schedules[i].memo = memo
                    self.data.schedules[i].updated_at = datetime.now()
                    print(f"메모 업데이트: {schedule_id} - '{old_memo}' -> '{memo}'")

                    # 데이터 저장
                    save_success = self.save_data()
                    print(f"데이터 저장 성공: {save_success}")

                    return True
            print(f"스케줄을 찾을 수 없음: {schedule_id}")
            return False
        except Exception as e:
            print(f"Failed to update schedule memo: {e}")
            return False

    def get_schedule_by_id(self, schedule_id: str) -> Optional[Schedule]:
        """스케줄 ID로 스케줄 조회"""
        for schedule in self.data.schedules:
            if schedule.id == schedule_id:
                return schedule
        return None

    def _initialize_google_sheets(self):
        """구글 시트 초기화"""
        webapp_url = "https://script.google.com/macros/s/AKfycbxT7joPlgV9cZv_kdo5uHXoyV22v8q-nWU-aRKAuOlRaq0eHqh3w68HMLyovy8LgJVbMw/exec"
        self.sheets_manager.initialize(webapp_url)

    def is_google_sheets_available(self) -> bool:
        """구글 시트 연결 가능 여부 확인"""
        return self.sheets_manager.is_initialized()

    def test_google_sheets_connection(self) -> tuple[bool, str]:
        """구글 시트 연결 테스트"""
        if not self.is_google_sheets_available():
            return False, "구글 시트가 초기화되지 않았습니다."

        api = self.sheets_manager.get_api()
        if api:
            return api.test_connection()
        return False, "API 인스턴스를 가져올 수 없습니다."

    def sync_to_google_sheets(self) -> tuple[bool, str]:
        """로컬 데이터를 구글 시트로 동기화"""
        if not self.is_google_sheets_available():
            return False, "구글 시트가 초기화되지 않았습니다."

        try:
            self.syncStatusChanged.emit("구글 시트로 동기화 중...")

            api = self.sheets_manager.get_api()
            if not api:
                return False, "API 인스턴스를 가져올 수 없습니다."

            success, message = api.sync_from_local_to_sheets(self.data)

            if success:
                self.syncStatusChanged.emit("동기화 완료")
            else:
                self.syncStatusChanged.emit("동기화 실패")

            return success, message

        except Exception as e:
            error_message = f"동기화 중 오류 발생: {str(e)}"
            self.syncStatusChanged.emit("동기화 실패")
            return False, error_message

    def sync_from_google_sheets(self) -> tuple[bool, str]:
        """구글 시트에서 로컬로 데이터 동기화"""
        if not self.is_google_sheets_available():
            return False, "구글 시트가 초기화되지 않았습니다."

        try:
            self.syncStatusChanged.emit("구글 시트에서 데이터 가져오는 중...")

            api = self.sheets_manager.get_api()
            if not api:
                return False, "API 인스턴스를 가져올 수 없습니다."

            success, message, app_data = api.sync_from_sheets_to_local()

            if success and app_data:
                # 기존 데이터 백업 생성
                backup_success = self.create_backup()
                if not backup_success:
                    print("기존 데이터 백업 생성 실패 - 계속 진행")

                # 새 데이터로 교체
                self.data = app_data

                # 로컬에 저장
                save_success = self.save_data()
                if save_success:
                    self.dataChanged.emit()
                    self.syncStatusChanged.emit("동기화 완료")
                    return True, f"{message} (로컬 저장 완료)"
                else:
                    self.syncStatusChanged.emit("로컬 저장 실패")
                    return False, "구글 시트에서 가져왔지만 로컬 저장에 실패했습니다."
            else:
                self.syncStatusChanged.emit("동기화 실패")
                return False, message

        except Exception as e:
            error_message = f"동기화 중 오류 발생: {str(e)}"
            self.syncStatusChanged.emit("동기화 실패")
            return False, error_message

    def create_google_sheets_backup(self) -> tuple[bool, str, Optional[Dict]]:
        """구글 시트에서 백업 생성"""
        if not self.is_google_sheets_available():
            return False, "구글 시트가 초기화되지 않았습니다.", None

        try:
            api = self.sheets_manager.get_api()
            if not api:
                return False, "API 인스턴스를 가져올 수 없습니다.", None

            return api.create_backup()

        except Exception as e:
            return False, f"백업 생성 중 오류 발생: {str(e)}", None

    def get_google_sheets_stats(self) -> tuple[bool, str, Optional[Dict]]:
        """구글 시트 데이터 통계 조회"""
        if not self.is_google_sheets_available():
            return False, "구글 시트가 초기화되지 않았습니다.", None

        try:
            api = self.sheets_manager.get_api()
            if not api:
                return False, "API 인스턴스를 가져올 수 없습니다.", None

            return api.get_data_stats()

        except Exception as e:
            return False, f"통계 조회 중 오류 발생: {str(e)}", None