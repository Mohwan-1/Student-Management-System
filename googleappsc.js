/**
 * 학생 관리 시스템을 위한 구글 앱스 스크립트
 * 구글 시트 ID: 1vmMqkGpcaQUGK7YAXDhYNZro2ZwJut6-LSpXYY-4YXE
 */

const SHEET_ID = '1vmMqkGpcaQUGK7YAXDhYNZro2ZwJut6-LSpXYY-4YXE';

/**
 * 웹앱 진입점 - HTTP 요청 처리
 */
function doPost(e) {
  try {
    const request = JSON.parse(e.postData.contents);
    const action = request.action;

    switch (action) {
      case 'sync_students':
        return syncStudents(request.data);
      case 'sync_schedules':
        return syncSchedules(request.data);
      case 'get_students':
        return getStudents();
      case 'get_schedules':
        return getSchedules();
      case 'full_sync':
        return fullSync(request.data);
      case 'test_simple_sync':
        return testSimpleSync(request.data);
      default:
        return createResponse(false, 'Unknown action');
    }
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 학생 데이터를 구글 시트에 동기화
 */
function syncStudents(studentsData) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    let sheet = spreadsheet.getSheetByName('Students');

    if (!sheet) {
      sheet = spreadsheet.insertSheet('Students');
      // 헤더 설정
      sheet.getRange(1, 1, 1, 8).setValues([[
        'ID', '이름', '총 주차', '수업 요일', '시작일', '생성일', '활성 상태', '색상'
      ]]);
      sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
    }

    // 기존 데이터 삭제 (헤더 제외)
    if (sheet.getLastRow() > 1) {
      sheet.deleteRows(2, sheet.getLastRow() - 1);
    }

    // 새 데이터 추가
    if (studentsData && studentsData.length > 0) {
      const values = studentsData.map(student => [
        student.id,
        student.name,
        student.total_weeks,
        student.weekdays.join(', '),
        student.start_date,
        student.created_at,
        student.is_active ? '활성' : '비활성',
        student.color
      ]);

      sheet.getRange(2, 1, values.length, 8).setValues(values);

      // 날짜 열 포맷팅
      sheet.getRange(2, 5, values.length, 1).setNumberFormat('yyyy-mm-dd');
      sheet.getRange(2, 6, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    }

    return createResponse(true, `${studentsData.length}명의 학생 데이터가 동기화되었습니다.`);
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 스케줄 데이터를 구글 시트에 동기화
 */
function syncSchedules(schedulesData) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    let sheet = spreadsheet.getSheetByName('Schedules');

    if (!sheet) {
      sheet = spreadsheet.insertSheet('Schedules');
      // 헤더 설정
      sheet.getRange(1, 1, 1, 8).setValues([[
        'ID', '학생 ID', '주차', '예정일', '완료 여부', '메모', '생성일', '수정일'
      ]]);
      sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
    }

    // 기존 데이터 삭제 (헤더 제외)
    if (sheet.getLastRow() > 1) {
      sheet.deleteRows(2, sheet.getLastRow() - 1);
    }

    // 새 데이터 추가
    if (schedulesData && schedulesData.length > 0) {
      const values = schedulesData.map(schedule => [
        schedule.id,
        schedule.student_id,
        schedule.week_number,
        schedule.scheduled_date,
        schedule.is_completed ? '완료' : '미완료',
        schedule.memo || '',
        schedule.created_at,
        schedule.updated_at
      ]);

      sheet.getRange(2, 1, values.length, 8).setValues(values);

      // 날짜 열 포맷팅
      sheet.getRange(2, 4, values.length, 1).setNumberFormat('yyyy-mm-dd');
      sheet.getRange(2, 7, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
      sheet.getRange(2, 8, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    }

    return createResponse(true, `${schedulesData.length}개의 스케줄이 동기화되었습니다.`);
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 구글 시트에서 학생 데이터 가져오기
 */
function getStudents() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName('Students');

    if (!sheet || sheet.getLastRow() <= 1) {
      return createResponse(true, '학생 데이터가 없습니다.', []);
    }

    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).getValues();
    const students = data.map(row => {
      const originalDate = row[4];
      const formattedDate = formatDateUltraSafe(originalDate);

      console.log(`Student ${row[1]}: Original date: ${originalDate}, Formatted: ${formattedDate}`);

      return {
        id: row[0],
        name: row[1],
        total_weeks: row[2],
        weekdays: row[3] ? row[3].split(', ') : [],
        start_date: formattedDate,
        created_at: formatDateTime(row[5]),
        is_active: row[6] === '활성',
        color: row[7]
      };
    });

    return createResponse(true, `${students.length}명의 학생 데이터를 가져왔습니다.`, students);
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 구글 시트에서 스케줄 데이터 가져오기
 */
function getSchedules() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName('Schedules');

    if (!sheet || sheet.getLastRow() <= 1) {
      return createResponse(true, '스케줄 데이터가 없습니다.', []);
    }

    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).getValues();
    const schedules = data.map(row => {
      const originalDate = row[3];
      const formattedDate = formatDateUltraSafe(originalDate);

      console.log(`Schedule ${row[0]}: Original date: ${originalDate}, Formatted: ${formattedDate}`);

      return {
        id: row[0],
        student_id: row[1],
        week_number: row[2],
        scheduled_date: formattedDate,
        is_completed: row[4] === '완료',
        memo: row[5] || '',
        created_at: formatDateTime(row[6]),
        updated_at: formatDateTime(row[7])
      };
    });

    return createResponse(true, `${schedules.length}개의 스케줄을 가져왔습니다.`, schedules);
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 간단한 테스트 동기화
 */
function testSimpleSync(appData) {
  try {
    console.log('=== SIMPLE SYNC TEST ===');
    console.log('Received appData:', JSON.stringify(appData));

    let studentsMessage = 'students test ok';
    let schedulesMessage = 'schedules test ok';
    let studentsSuccess = true;
    let schedulesSuccess = true;

    console.log('Variables before message construction:');
    console.log('- studentsMessage:', studentsMessage, typeof studentsMessage);
    console.log('- schedulesMessage:', schedulesMessage, typeof schedulesMessage);

    const result = `테스트 결과 - 학생: ${studentsMessage}, 스케줄: ${schedulesMessage}`;
    console.log('Final result:', result);

    return createResponse(true, result);
  } catch (error) {
    console.error('Simple sync test error:', error);
    return createResponse(false, error.toString());
  }
}

/**
 * 전체 데이터 동기화 (학생 + 스케줄)
 */
function fullSync(appData) {
  // Declare all variables at function scope to avoid scope issues
  var studentsSuccess = false;
  var studentsMessage = 'not processed';
  var schedulesSuccess = false;
  var schedulesMessage = 'not processed';

  try {
    console.log('=== FULL SYNC START ===');
    console.log('Received appData keys:', Object.keys(appData || {}));

    // 학생 데이터 동기화
    console.log('=== STUDENTS SYNC START ===');
    try {
      var studentsArray = appData && appData.students ? appData.students : [];
      console.log('Processing', studentsArray.length, 'students');

      var studentsResult = syncStudentsData(studentsArray);
      console.log('Students sync returned:', studentsResult);

      if (studentsResult) {
        studentsSuccess = studentsResult.success === true;
        studentsMessage = studentsResult.message || 'no message';
      } else {
        studentsSuccess = false;
        studentsMessage = 'null result from syncStudentsData';
      }
      console.log('Students final - success:', studentsSuccess, 'message:', studentsMessage);
    } catch (e) {
      studentsSuccess = false;
      studentsMessage = 'Students exception: ' + e.toString();
      console.error('Students error:', e);
    }

    // 스케줄 데이터 동기화
    console.log('=== SCHEDULES SYNC START ===');
    try {
      var schedulesArray = appData && appData.schedules ? appData.schedules : [];
      console.log('Processing', schedulesArray.length, 'schedules');

      var schedulesResult = syncSchedulesData(schedulesArray);
      console.log('Schedules sync returned:', schedulesResult);

      if (schedulesResult) {
        schedulesSuccess = schedulesResult.success === true;
        schedulesMessage = schedulesResult.message || 'no message';
      } else {
        schedulesSuccess = false;
        schedulesMessage = 'null result from syncSchedulesData';
      }
      console.log('Schedules final - success:', schedulesSuccess, 'message:', schedulesMessage);
    } catch (e) {
      schedulesSuccess = false;
      schedulesMessage = 'Schedules exception: ' + e.toString();
      console.error('Schedules error:', e);
    }

    const finalResult = {
      studentsSuccess,
      studentsMessage,
      schedulesSuccess,
      schedulesMessage
    };

    console.log('Final sync result:', finalResult);

    if (studentsSuccess && schedulesSuccess) {
      // 메타데이터 업데이트
      updateMetadata(appData.metadata || {});

      const studentCount = appData.students ? appData.students.length : 0;
      const scheduleCount = appData.schedules ? appData.schedules.length : 0;

      const successMessage = `전체 동기화 완료: ${studentCount}명 학생, ${scheduleCount}개 스케줄`;
      console.log('Returning success:', successMessage);

      return createResponse(true, successMessage);
    } else {
      console.log('Final variables before message:');
      console.log('- studentsMessage:', studentsMessage);
      console.log('- schedulesMessage:', schedulesMessage);

      // Use simple concatenation instead of template literals
      var failMessage = '동기화 실패 - 학생: ' + studentsMessage + ', 스케줄: ' + schedulesMessage;
      console.log('Final message:', failMessage);

      return createResponse(false, failMessage);
    }
  } catch (error) {
    console.error('Full sync error:', error);
    return createResponse(false, error.toString());
  }
}

/**
 * 학생 데이터 동기화 (내부용)
 */
function syncStudentsData(studentsData) {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  let sheet = spreadsheet.getSheetByName('Students');

  if (!sheet) {
    sheet = spreadsheet.insertSheet('Students');
    sheet.getRange(1, 1, 1, 8).setValues([[
      'ID', '이름', '총 주차', '수업 요일', '시작일', '생성일', '활성 상태', '색상'
    ]]);
    sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
  }

  if (sheet.getLastRow() > 1) {
    sheet.deleteRows(2, sheet.getLastRow() - 1);
  }

  if (studentsData && studentsData.length > 0) {
    const values = studentsData.map(student => [
      student.id,
      student.name,
      student.total_weeks,
      student.weekdays.join(', '),
      student.start_date,
      student.created_at,
      student.is_active ? '활성' : '비활성',
      student.color
    ]);

    sheet.getRange(2, 1, values.length, 8).setValues(values);
    sheet.getRange(2, 5, values.length, 1).setNumberFormat('yyyy-mm-dd');
    sheet.getRange(2, 6, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');

    return { success: true, message: `${studentsData.length}명의 학생 데이터가 동기화되었습니다.` };
  } else {
    return { success: true, message: `학생 데이터 없음 (시트 초기화 완료)` };
  }
}

/**
 * 스케줄 데이터 동기화 (내부용)
 */
function syncSchedulesData(schedulesData) {
  const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
  let sheet = spreadsheet.getSheetByName('Schedules');

  if (!sheet) {
    sheet = spreadsheet.insertSheet('Schedules');
    sheet.getRange(1, 1, 1, 8).setValues([[
      'ID', '학생 ID', '주차', '예정일', '완료 여부', '메모', '생성일', '수정일'
    ]]);
    sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
  }

  if (sheet.getLastRow() > 1) {
    sheet.deleteRows(2, sheet.getLastRow() - 1);
  }

  if (schedulesData && schedulesData.length > 0) {
    const values = schedulesData.map(schedule => [
      schedule.id,
      schedule.student_id,
      schedule.week_number,
      schedule.scheduled_date,
      schedule.is_completed ? '완료' : '미완료',
      schedule.memo || '',
      schedule.created_at,
      schedule.updated_at
    ]);

    sheet.getRange(2, 1, values.length, 8).setValues(values);
    sheet.getRange(2, 4, values.length, 1).setNumberFormat('yyyy-mm-dd');
    sheet.getRange(2, 7, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    sheet.getRange(2, 8, values.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');

    return { success: true, message: `${schedulesData.length}개의 스케줄이 동기화되었습니다.` };
  } else {
    return { success: true, message: `스케줄 데이터 없음 (시트 초기화 완료)` };
  }
}

/**
 * 메타데이터 시트 업데이트
 */
function updateMetadata(metadata) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    let sheet = spreadsheet.getSheetByName('Metadata');

    if (!sheet) {
      sheet = spreadsheet.insertSheet('Metadata');
      sheet.getRange(1, 1, 1, 2).setValues([['Key', 'Value']]);
      sheet.getRange(1, 1, 1, 2).setFontWeight('bold');
    }

    // 기존 메타데이터 삭제
    if (sheet.getLastRow() > 1) {
      sheet.deleteRows(2, sheet.getLastRow() - 1);
    }

    // 새 메타데이터 추가
    const metadataEntries = Object.entries(metadata);
    if (metadataEntries.length > 0) {
      const values = metadataEntries.map(([key, value]) => [key, value]);
      sheet.getRange(2, 1, values.length, 2).setValues(values);
    }

    // 동기화 시간 추가
    sheet.getRange(sheet.getLastRow() + 1, 1, 1, 2).setValues([
      ['last_sync', new Date().toISOString()]
    ]);

  } catch (error) {
    console.error('메타데이터 업데이트 실패:', error);
  }
}

/**
 * 개별 학생 업데이트
 */
function updateStudent(studentData) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName('Students');

    if (!sheet) {
      return createResponse(false, 'Students 시트가 없습니다.');
    }

    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).getValues();
    const rowIndex = data.findIndex(row => row[0] === studentData.id);

    if (rowIndex === -1) {
      // 새 학생 추가
      const newRow = [
        studentData.id,
        studentData.name,
        studentData.total_weeks,
        studentData.weekdays.join(', '),
        studentData.start_date,
        studentData.created_at,
        studentData.is_active ? '활성' : '비활성',
        studentData.color
      ];
      sheet.getRange(sheet.getLastRow() + 1, 1, 1, 8).setValues([newRow]);
    } else {
      // 기존 학생 업데이트
      const updatedRow = [
        studentData.id,
        studentData.name,
        studentData.total_weeks,
        studentData.weekdays.join(', '),
        studentData.start_date,
        studentData.created_at,
        studentData.is_active ? '활성' : '비활성',
        studentData.color
      ];
      sheet.getRange(rowIndex + 2, 1, 1, 8).setValues([updatedRow]);
    }

    return createResponse(true, '학생 정보가 업데이트되었습니다.');
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 개별 스케줄 업데이트
 */
function updateSchedule(scheduleData) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName('Schedules');

    if (!sheet) {
      return createResponse(false, 'Schedules 시트가 없습니다.');
    }

    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).getValues();
    const rowIndex = data.findIndex(row => row[0] === scheduleData.id);

    if (rowIndex === -1) {
      // 새 스케줄 추가
      const newRow = [
        scheduleData.id,
        scheduleData.student_id,
        scheduleData.week_number,
        scheduleData.scheduled_date,
        scheduleData.is_completed ? '완료' : '미완료',
        scheduleData.memo || '',
        scheduleData.created_at,
        scheduleData.updated_at
      ];
      sheet.getRange(sheet.getLastRow() + 1, 1, 1, 8).setValues([newRow]);
    } else {
      // 기존 스케줄 업데이트
      const updatedRow = [
        scheduleData.id,
        scheduleData.student_id,
        scheduleData.week_number,
        scheduleData.scheduled_date,
        scheduleData.is_completed ? '완료' : '미완료',
        scheduleData.memo || '',
        scheduleData.created_at,
        scheduleData.updated_at
      ];
      sheet.getRange(rowIndex + 2, 1, 1, 8).setValues([updatedRow]);
    }

    return createResponse(true, '스케줄이 업데이트되었습니다.');
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 학생 삭제
 */
function deleteStudent(studentId) {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const sheet = spreadsheet.getSheetByName('Students');

    if (!sheet) {
      return createResponse(false, 'Students 시트가 없습니다.');
    }

    const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 1).getValues();
    const rowIndex = data.findIndex(row => row[0] === studentId);

    if (rowIndex !== -1) {
      sheet.deleteRow(rowIndex + 2);
      return createResponse(true, '학생이 삭제되었습니다.');
    } else {
      return createResponse(false, '학생을 찾을 수 없습니다.');
    }
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 백업 생성
 */
function createBackup() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupName = `StudentManagement_Backup_${timestamp}`;

    const backup = spreadsheet.copy(backupName);

    return createResponse(true, `백업이 생성되었습니다: ${backupName}`, {
      backupId: backup.getId(),
      backupUrl: backup.getUrl()
    });
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 데이터 통계 가져오기
 */
function getDataStats() {
  try {
    const studentsResult = getStudents();
    const schedulesResult = getSchedules();

    if (!studentsResult.success || !schedulesResult.success) {
      return createResponse(false, '데이터를 가져올 수 없습니다.');
    }

    const students = studentsResult.data || [];
    const schedules = schedulesResult.data || [];

    const stats = {
      totalStudents: students.length,
      activeStudents: students.filter(s => s.is_active).length,
      totalSchedules: schedules.length,
      completedSchedules: schedules.filter(s => s.is_completed).length,
      pendingSchedules: schedules.filter(s => !s.is_completed).length,
      lastSync: new Date().toISOString()
    };

    return createResponse(true, '통계 데이터를 가져왔습니다.', stats);
  } catch (error) {
    return createResponse(false, error.toString());
  }
}

/**
 * 응답 객체 생성
 */
function createResponse(success, message, data = null) {
  const response = {
    success: success,
    message: message,
    timestamp: new Date().toISOString()
  };

  if (data !== null) {
    response.data = data;
  }

  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * 날짜 포맷팅 함수
 */
function formatDate(date) {
  if (!date) return '';
  if (typeof date === 'string') return date;

  // 구글 시트의 날짜 객체인 경우 로컬 시간으로 변환
  if (date instanceof Date) {
    // 시간대 오프셋을 고려하여 로컬 날짜로 변환
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    return localDate.toISOString().split('T')[0];
  }

  return date.toString();
}

/**
 * 안전한 날짜 포맷팅 함수 (시간대 문제 해결)
 */
function formatDateSafe(date) {
  if (!date) return '';
  if (typeof date === 'string') return date;

  if (date instanceof Date) {
    // 방법 1: 로컬 날짜 직접 추출 (시간대 무시)
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    console.log(`formatDateSafe: Input ${date.toISOString()}, Output: ${year}-${month}-${day}`);
    return `${year}-${month}-${day}`;
  }

  return date.toString();
}

/**
 * 더 안전한 날짜 포맷팅 (UTC 오프셋 고려)
 */
function formatDateUltraSafe(date) {
  console.log(`formatDateUltraSafe called with:`, date, `Type:`, typeof date);

  if (!date) return '';
  if (typeof date === 'string') {
    console.log(`Returning string as-is:`, date);
    return date;
  }

  if (date instanceof Date) {
    console.log(`Processing Date object:`);
    console.log(`- toISOString(): ${date.toISOString()}`);
    console.log(`- toString(): ${date.toString()}`);
    console.log(`- getTime(): ${date.getTime()}`);

    // 방법 1: UTC 기준으로 날짜 추출 (시간대 변환 없이)
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
    const day = String(date.getUTCDate()).padStart(2, '0');
    const utcResult = `${year}-${month}-${day}`;
    console.log(`UTC method result: ${utcResult}`);

    // 방법 2: 로컬 날짜 추출
    const localYear = date.getFullYear();
    const localMonth = String(date.getMonth() + 1).padStart(2, '0');
    const localDay = String(date.getDate()).padStart(2, '0');
    const localResult = `${localYear}-${localMonth}-${localDay}`;
    console.log(`Local method result: ${localResult}`);

    // 방법 3: Locale 기준 날짜 추출 (기존 방법)
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'Asia/Seoul' };
    const formatted = date.toLocaleDateString('ko-KR', options);
    const parts = formatted.replace(/\./g, '').split(' ').filter(p => p);
    let localeResult = '';
    if (parts.length >= 3) {
      const [year, month, day] = parts;
      localeResult = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    }
    console.log(`Locale method result: ${localeResult}`);

    // UTC 방법을 사용하되, 로컬과 비교해서 차이가 있으면 로컬 사용
    const finalResult = utcResult;
    console.log(`Final result: ${finalResult}`);
    return finalResult;
  }

  return date.toString();
}

function formatDateTime(date) {
  if (!date) return '';
  if (typeof date === 'string') return date;

  if (date instanceof Date) {
    // 시간대 오프셋을 고려하여 로컬 시간으로 변환
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    return localDate.toISOString();
  }

  return date.toString();
}

/**
 * 테스트 함수 - 구글 앱스 스크립트 에디터에서 실행 가능
 */
function testConnection() {
  try {
    const spreadsheet = SpreadsheetApp.openById(SHEET_ID);
    console.log('연결 성공:', spreadsheet.getName());

    // 테스트 데이터
    const testStudent = {
      id: 'test-student-1',
      name: '테스트 학생',
      total_weeks: 12,
      weekdays: ['월요일', '수요일'],
      start_date: '2024-01-01',
      created_at: new Date().toISOString(),
      is_active: true,
      color: '#FF5733'
    };

    const result = updateStudent(testStudent);
    console.log('테스트 결과:', JSON.parse(result.getContent()));

  } catch (error) {
    console.error('연결 실패:', error);
  }
}

/**
 * 트리거 설정을 위한 함수
 */
function setupTriggers() {
  // 기존 트리거 삭제
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // 매일 백업 생성 (오전 2시)
  ScriptApp.newTrigger('createDailyBackup')
    .timeBased()
    .everyDays(1)
    .atHour(2)
    .create();
}

/**
 * 일일 백업 함수
 */
function createDailyBackup() {
  try {
    createBackup();
    console.log('일일 백업이 생성되었습니다.');
  } catch (error) {
    console.error('일일 백업 실패:', error);
  }
}