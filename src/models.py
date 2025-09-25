from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import uuid


@dataclass
class Student:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    total_weeks: int = 1
    weekdays: List[str] = field(default_factory=list)
    start_date: date = field(default_factory=date.today)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    color: str = "#FF5733"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "total_weeks": self.total_weeks,
            "weekdays": self.weekdays,
            "start_date": self.start_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "color": self.color
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        student = cls()
        student.id = data.get("id", str(uuid.uuid4()))
        student.name = data.get("name", "")
        student.total_weeks = data.get("total_weeks", 1)
        student.weekdays = data.get("weekdays", [])
        student.start_date = date.fromisoformat(data.get("start_date", date.today().isoformat()))
        student.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        student.is_active = data.get("is_active", True)
        student.color = data.get("color", "#FF5733")
        return student


@dataclass
class Schedule:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str = ""
    week_number: int = 1
    scheduled_date: date = field(default_factory=date.today)
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "week_number": self.week_number,
            "scheduled_date": self.scheduled_date.isoformat(),
            "is_completed": self.is_completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Schedule':
        schedule = cls()
        schedule.id = data.get("id", str(uuid.uuid4()))
        schedule.student_id = data.get("student_id", "")
        schedule.week_number = data.get("week_number", 1)
        schedule.scheduled_date = date.fromisoformat(data.get("scheduled_date", date.today().isoformat()))
        schedule.is_completed = data.get("is_completed", False)
        schedule.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        schedule.updated_at = datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        return schedule


@dataclass
class AppData:
    students: List[Student] = field(default_factory=list)
    schedules: List[Schedule] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {
                "version": "1.0",
                "last_backup": datetime.now().isoformat()
            }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "students": [student.to_dict() for student in self.students],
            "schedules": [schedule.to_dict() for schedule in self.schedules],
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppData':
        app_data = cls()
        app_data.students = [Student.from_dict(s) for s in data.get("students", [])]
        app_data.schedules = [Schedule.from_dict(s) for s in data.get("schedules", [])]
        app_data.metadata = data.get("metadata", {
            "version": "1.0",
            "last_backup": datetime.now().isoformat()
        })
        return app_data