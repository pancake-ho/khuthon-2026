const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API 요청 실패: ${response.status}`)
  }

  return response.json()
}

// 1. Callture 요청 목록 가져오기
export function fetchCalltures() {
  return request('/api/calltures')
}

// 2. 새 Callture 요청 등록하기
export function createCalltureRequest(requestData) {
  return request('/api/calltures', {
    method: 'POST',
    body: JSON.stringify(requestData),
  })
}

// 3. 매칭된 프로그램 목록 가져오기
export function fetchPrograms() {
  return request('/api/programs')
}

// 4. 나의 프로그램 목록 가져오기
export function fetchMyPrograms() {
  return request('/api/my-programs')
}

// 5. 관리자 모드에서 요청과 공간 매칭 저장하기
export function createMatch(matchData) {
  return request('/api/matches', {
    method: 'POST',
    body: JSON.stringify(matchData),
  })
}