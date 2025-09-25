import os
import sys
import shutil
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from PySide6.QtCore import QObject, Signal

from .crypto_utils import CryptoManager
from .models import Student, Schedule, AppData


class DataManager(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self.crypto_manager = CryptoManager()
        self.data = AppData()
        self.password: Optional[str] = None
        self._data_file_path = self._get_data_file_path()
        self._backup_folder = self._data_file_path.parent / "backups"
        self._backup_folder.mkdir(exist_ok=True)

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

        current_date = student.start_date
        current_weekday_idx = 0

        # 첫 번째 수업 날짜 찾기
        first_weekday = weekday_indices[0]
        days_to_first = first_weekday - current_date.weekday()
        if days_to_first < 0:
            days_to_first += 7
        elif days_to_first == 0:
            # 시작일이 첫 번째 수강 요일과 같으면 그 날부터 시작
            days_to_first = 0

        current_date = current_date + timedelta(days=days_to_first)

        for week in range(1, student.total_weeks + 1):
            target_weekday = weekday_indices[current_weekday_idx % len(weekday_indices)]

            # 현재 날짜에서 타겟 요일까지의 거리 계산
            if week == 1:
                # 첫 번째 주는 이미 계산됨
                schedule_date = current_date
            else:
                days_ahead = target_weekday - current_date.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                schedule_date = current_date + timedelta(days=days_ahead)

            schedule = Schedule(
                student_id=student.id,
                week_number=week,
                scheduled_date=schedule_date
            )

            self.data.schedules.append(schedule)

            current_date = schedule_date + timedelta(days=1)
            current_weekday_idx += 1

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