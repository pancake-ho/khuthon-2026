const CULTURE_CALL_REQUIRED_FIELDS = [
  'id',
  'title',
  'genre',
  'target',
  'time',
  'place',
  'current',
  'goal',
  'createdAt',
  'summary',
  'similarRequests',
]

const PROGRAM_REQUIRED_FIELDS = [
  'id',
  'title',
  'creator',
  'creatorInfo',
  'space',
  'spaceInfo',
  'status',
]

const MY_PROGRAM_REQUIRED_FIELDS = [
  'id',
  'title',
  'date',
  'place',
  'target',
  'fee',
  'status',
]

export function validateCultureCall(call) {
  if (!call || typeof call !== 'object' || Array.isArray(call)) {
    return {
      valid: false,
      message: '문화콜 데이터는 객체 형태여야 합니다.',
    }
  }

  for (const field of CULTURE_CALL_REQUIRED_FIELDS) {
    if (!(field in call)) {
      return {
        valid: false,
        message: `문화콜 필수 필드가 없습니다: ${field}`,
      }
    }
  }

  if (typeof call.id !== 'number') {
    return { valid: false, message: '문화콜 id는 number여야 합니다.' }
  }

  if (typeof call.title !== 'string') {
    return { valid: false, message: '문화콜 title은 string이어야 합니다.' }
  }

  if (typeof call.genre !== 'string') {
    return { valid: false, message: '문화콜 genre는 string이어야 합니다.' }
  }

  if (typeof call.target !== 'string') {
    return { valid: false, message: '문화콜 target은 string이어야 합니다.' }
  }

  if (typeof call.time !== 'string') {
    return { valid: false, message: '문화콜 time은 string이어야 합니다.' }
  }

  if (typeof call.place !== 'string') {
    return { valid: false, message: '문화콜 place는 string이어야 합니다.' }
  }

  if (typeof call.current !== 'number') {
    return { valid: false, message: '문화콜 current는 number여야 합니다.' }
  }

  if (typeof call.goal !== 'number') {
    return { valid: false, message: '문화콜 goal은 number여야 합니다.' }
  }

  if (call.current < 0) {
    return { valid: false, message: '문화콜 current는 0 이상이어야 합니다.' }
  }

  if (call.goal <= 0) {
    return { valid: false, message: '문화콜 goal은 1 이상이어야 합니다.' }
  }

  if (typeof call.createdAt !== 'string') {
    return { valid: false, message: '문화콜 createdAt은 string이어야 합니다.' }
  }

  if (Number.isNaN(Date.parse(call.createdAt))) {
    return {
      valid: false,
      message: '문화콜 createdAt은 날짜 문자열이어야 합니다. 예: 2026-05-08',
    }
  }

  if (typeof call.summary !== 'string') {
    return { valid: false, message: '문화콜 summary는 string이어야 합니다.' }
  }

  if (!Array.isArray(call.similarRequests)) {
    return {
      valid: false,
      message: '문화콜 similarRequests는 배열이어야 합니다.',
    }
  }

  for (const request of call.similarRequests) {
    if (typeof request !== 'string') {
      return {
        valid: false,
        message: '문화콜 similarRequests의 각 항목은 string이어야 합니다.',
      }
    }
  }

  return {
    valid: true,
    message: '올바른 문화콜 데이터입니다.',
  }
}

export function validateCultureCallList(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return {
      valid: false,
      message: '문화콜 목록 응답은 객체 형태여야 합니다.',
    }
  }

  if (!Array.isArray(data.calls)) {
    return {
      valid: false,
      message: '문화콜 목록 응답은 { calls: [...] } 형태여야 합니다.',
    }
  }

  for (const call of data.calls) {
    const result = validateCultureCall(call)

    if (!result.valid) {
      return result
    }
  }

  return {
    valid: true,
    message: '올바른 문화콜 목록 데이터입니다.',
  }
}

export function validateProgram(program) {
  if (!program || typeof program !== 'object' || Array.isArray(program)) {
    return {
      valid: false,
      message: '매칭 프로그램 데이터는 객체 형태여야 합니다.',
    }
  }

  for (const field of PROGRAM_REQUIRED_FIELDS) {
    if (!(field in program)) {
      return {
        valid: false,
        message: `매칭 프로그램 필수 필드가 없습니다: ${field}`,
      }
    }
  }

  if (typeof program.id !== 'number') {
    return { valid: false, message: '매칭 프로그램 id는 number여야 합니다.' }
  }

  if (typeof program.title !== 'string') {
    return { valid: false, message: '매칭 프로그램 title은 string이어야 합니다.' }
  }

  if (typeof program.creator !== 'string') {
    return { valid: false, message: '매칭 프로그램 creator는 string이어야 합니다.' }
  }

  if (typeof program.creatorInfo !== 'string') {
    return {
      valid: false,
      message: '매칭 프로그램 creatorInfo는 string이어야 합니다.',
    }
  }

  if (typeof program.space !== 'string') {
    return { valid: false, message: '매칭 프로그램 space는 string이어야 합니다.' }
  }

  if (typeof program.spaceInfo !== 'string') {
    return {
      valid: false,
      message: '매칭 프로그램 spaceInfo는 string이어야 합니다.',
    }
  }

  if (typeof program.status !== 'string') {
    return { valid: false, message: '매칭 프로그램 status는 string이어야 합니다.' }
  }

  return {
    valid: true,
    message: '올바른 매칭 프로그램 데이터입니다.',
  }
}

export function validateProgramList(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return {
      valid: false,
      message: '매칭 프로그램 목록 응답은 객체 형태여야 합니다.',
    }
  }

  if (!Array.isArray(data.programs)) {
    return {
      valid: false,
      message: '매칭 프로그램 목록 응답은 { programs: [...] } 형태여야 합니다.',
    }
  }

  for (const program of data.programs) {
    const result = validateProgram(program)

    if (!result.valid) {
      return result
    }
  }

  return {
    valid: true,
    message: '올바른 매칭 프로그램 목록 데이터입니다.',
  }
}

export function validateMyProgram(program) {
  if (!program || typeof program !== 'object' || Array.isArray(program)) {
    return {
      valid: false,
      message: '나의 프로그램 데이터는 객체 형태여야 합니다.',
    }
  }

  for (const field of MY_PROGRAM_REQUIRED_FIELDS) {
    if (!(field in program)) {
      return {
        valid: false,
        message: `나의 프로그램 필수 필드가 없습니다: ${field}`,
      }
    }
  }

  if (typeof program.id !== 'number') {
    return { valid: false, message: '나의 프로그램 id는 number여야 합니다.' }
  }

  if (typeof program.title !== 'string') {
    return { valid: false, message: '나의 프로그램 title은 string이어야 합니다.' }
  }

  if (typeof program.date !== 'string') {
    return { valid: false, message: '나의 프로그램 date는 string이어야 합니다.' }
  }

  if (typeof program.place !== 'string') {
    return { valid: false, message: '나의 프로그램 place는 string이어야 합니다.' }
  }

  if (typeof program.target !== 'string') {
    return { valid: false, message: '나의 프로그램 target은 string이어야 합니다.' }
  }

  if (typeof program.fee !== 'string') {
    return { valid: false, message: '나의 프로그램 fee는 string이어야 합니다.' }
  }

  if (typeof program.status !== 'string') {
    return { valid: false, message: '나의 프로그램 status는 string이어야 합니다.' }
  }

  return {
    valid: true,
    message: '올바른 나의 프로그램 데이터입니다.',
  }
}

export function validateMyProgramList(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return {
      valid: false,
      message: '나의 프로그램 목록 응답은 객체 형태여야 합니다.',
    }
  }

  if (!Array.isArray(data.myPrograms)) {
    return {
      valid: false,
      message: '나의 프로그램 목록 응답은 { myPrograms: [...] } 형태여야 합니다.',
    }
  }

  for (const program of data.myPrograms) {
    const result = validateMyProgram(program)

    if (!result.valid) {
      return result
    }
  }

  return {
    valid: true,
    message: '올바른 나의 프로그램 목록 데이터입니다.',
  }
}