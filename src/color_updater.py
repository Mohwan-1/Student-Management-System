from .student_form import StudentForm


def update_existing_student_colors(data_manager):
    """기존 수강생들의 색상을 강렬한 고대비 색상으로 업데이트"""
    students = data_manager.get_students()

    if not students:
        return

    # 임시 StudentForm 인스턴스 생성하여 색상 생성 기능 사용
    temp_form = StudentForm(data_manager)

    # 모든 기존 색상을 초기화
    used_colors = set()

    for student in students:
        # 기존 색상 목록에서 해당 학생 제외하고 새 색상 생성
        original_color = student.color

        # 새로운 강렬한 색상 생성
        new_color = temp_form.generate_unique_color()

        # 중복 체크
        while new_color in used_colors:
            new_color = temp_form.generate_unique_color()

        student.color = new_color
        used_colors.add(new_color)

        print(f"수강생 '{student.name}' 색상 업데이트: {original_color} -> {new_color}")

    # 변경사항 저장
    data_manager.save_data()
    print(f"총 {len(students)}명 수강생의 색상이 강렬한 색상으로 업데이트되었습니다.")