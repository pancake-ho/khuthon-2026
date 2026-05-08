import { useMemo, useState } from 'react'
import './App.css'

const ADMIN_PASSWORD = '0000'

const cultureCalls = [
  {
    id: 1,
    icon: '🏮',
    title: '한옥 마을 전통문화 체험',
    genre: '전통문화체험',
    target: '가족',
    time: '주말 낮',
    place: '한옥마을 / 주민센터',
    current: 28,
    goal: 30,
    createdAt: '2026-05-08',
    summary: '전통 공예와 한복 체험 요청',
    detail: '전통 공예와 한복 체험을 함께 즐기는 지역 문화 프로그램 요청입니다.',
    similarRequests: [
      '전통문화를 직접 체험하고 싶어요.',
      '아이와 함께 한복 체험을 해보고 싶어요.',
      '지역 전통문화를 쉽게 접할 기회가 필요해요.',
    ],
  },
  {
    id: 2,
    icon: '🎸',
    title: '퇴근 후 인디 음악 공연',
    genre: '공연',
    target: '청년',
    time: '평일 저녁',
    place: '청년센터 / 공공공간',
    current: 41,
    goal: 50,
    createdAt: '2026-05-07',
    summary: '가볍게 즐기는 동네 공연',
    detail: '퇴근 후 멀리 이동하지 않고 동네에서 즐길 수 있는 인디 공연 요청입니다.',
    similarRequests: [
      '평일 저녁에 볼 수 있는 공연이 있었으면 좋겠어요.',
      '지역 청년 밴드 공연을 보고 싶어요.',
      '작은 공연장이 가까이 있으면 좋겠어요.',
    ],
  },
  {
    id: 3,
    icon: '🎬',
    title: '청소년 독립영화 상영회',
    genre: '영화',
    target: '청소년',
    time: '주말 저녁',
    place: '학교 / 도서관',
    current: 18,
    goal: 30,
    createdAt: '2026-05-06',
    summary: '청소년을 위한 영화 상영',
    detail: '청소년이 안전하게 참여할 수 있는 지역 독립영화 상영회 요청입니다.',
    similarRequests: [
      '청소년끼리 볼 수 있는 영화 프로그램이 있으면 좋겠어요.',
      '학교 근처에서 영화 상영회를 열어주세요.',
      '친구들과 함께 갈 수 있는 문화 공간이 필요해요.',
    ],
  },
  {
    id: 4,
    icon: '🖼️',
    title: '동네 작가 사진 전시',
    genre: '전시',
    target: '누구나',
    time: '평일 낮',
    place: '도서관 / 문화센터',
    current: 16,
    goal: 25,
    createdAt: '2026-05-05',
    summary: '지역 작가의 작은 전시',
    detail: '지역 사진 작가의 작품을 가까운 공공공간에서 볼 수 있게 하는 전시 요청입니다.',
    similarRequests: [
      '동네 작가들의 전시를 쉽게 보고 싶어요.',
      '도서관에서 작은 사진전이 열리면 좋겠어요.',
      '지역의 모습을 담은 전시가 필요해요.',
    ],
  },
  {
    id: 5,
    icon: '🎭',
    title: '어르신을 위한 연극 관람',
    genre: '연극',
    target: '고령층',
    time: '평일 낮',
    place: '주민센터 / 복지관',
    current: 22,
    goal: 35,
    createdAt: '2026-05-04',
    summary: '가까운 곳에서 보는 연극',
    detail: '고령층이 멀리 이동하지 않고 가까운 곳에서 볼 수 있는 작은 연극 요청입니다.',
    similarRequests: [
      '어르신들이 가까운 곳에서 연극을 보면 좋겠어요.',
      '복지관에서 문화 공연이 자주 열리면 좋겠어요.',
      '낮 시간대 연극 프로그램이 필요해요.',
    ],
  },
  {
    id: 6,
    icon: '🎨',
    title: '주말 가족 공예 체험',
    genre: '체험',
    target: '가족',
    time: '주말 낮',
    place: '도서관 / 주민센터',
    current: 24,
    goal: 30,
    createdAt: '2026-05-03',
    summary: '아이와 함께하는 만들기',
    detail: '아이와 부모가 함께 참여할 수 있는 주말 공예 프로그램 요청입니다.',
    similarRequests: [
      '아이랑 같이 할 수 있는 만들기 수업이 있으면 좋겠어요.',
      '도서관에서 가족 공예 체험을 열어주세요.',
      '주말에 가족 문화 활동이 필요해요.',
    ],
  },
]

const creatorSpaces = [
  {
    id: 1,
    icon: '📚',
    name: '○○도서관 문화강의실',
    type: '공공공간',
    capacity: '30명',
    availableTime: '주말 낮',
    goodFor: '전시 / 체험 / 강연',
  },
  {
    id: 2,
    icon: '🧑‍🎤',
    name: '○○청년센터 라운지',
    type: '청년공간',
    capacity: '50명',
    availableTime: '평일 저녁',
    goodFor: '공연 / 영화 / 네트워킹',
  },
  {
    id: 3,
    icon: '🏢',
    name: '○○주민센터 다목적실',
    type: '생활문화공간',
    capacity: '40명',
    availableTime: '평일 낮',
    goodFor: '연극 / 체험 / 고령층 프로그램',
  },
]

const matchedPrograms = [
  {
    id: 1,
    icon: '🏮',
    title: '한옥 마을 전통문화 체험',
    creator: '달빛한지 공방',
    creatorInfo: '전통 공예 / 한지 조명 / 가족 체험 가능',
    space: '○○한옥문화센터',
    spaceInfo: '주말 낮 사용 가능 / 30명 수용 가능',
    status: '신청자 모집 중',
  },
  {
    id: 2,
    icon: '🎸',
    title: '퇴근 후 인디 음악 공연',
    creator: '로컬사운드 팀',
    creatorInfo: '인디 음악 / 어쿠스틱 공연 / 60분 공연 가능',
    space: '○○청년센터 라운지',
    spaceInfo: '평일 저녁 사용 가능 / 음향 장비 보유',
    status: '신청자 모집 중',
  },
  {
    id: 3,
    icon: '🖼️',
    title: '동네 작가 사진 전시',
    creator: '로컬포토랩',
    creatorInfo: '지역 사진 전시 / 작품 해설 가능',
    space: '○○도서관 전시홀',
    spaceInfo: '평일 낮 운영 가능 / 전시 벽면 보유',
    status: '신청자 모집 중',
  },
]

const myPrograms = [
  {
    id: 1,
    icon: '🏮',
    title: '우리 동네 한지 조명 만들기',
    date: '토요일 오후 2시',
    place: '○○한옥문화센터',
    target: '가족 / 누구나',
    fee: '5,000원',
    status: '신청 완료',
  },
  {
    id: 2,
    icon: '🎸',
    title: '퇴근 후 인디 어쿠스틱 공연',
    date: '금요일 오후 7시',
    place: '○○청년센터',
    target: '청년 / 누구나',
    fee: '무료',
    status: '참여 예정',
  },
  {
    id: 3,
    icon: '🖼️',
    title: '동네 작가 사진 전시 투어',
    date: '수요일 오후 1시',
    place: '○○도서관 전시홀',
    target: '누구나',
    fee: '무료',
    status: '신청 가능',
  },
]

function App() {
  const [page, setPage] = useState('home')
  const [selectedCall, setSelectedCall] = useState(cultureCalls[0])
  const [isHelpOpen, setIsHelpOpen] = useState(false)
  const [isFeatureOpen, setIsFeatureOpen] = useState(false)
  const [isAdminLoginOpen, setIsAdminLoginOpen] = useState(false)
  const [adminPassword, setAdminPassword] = useState('')
  const [isAdminAuthenticated, setIsAdminAuthenticated] = useState(false)
  const [filter, setFilter] = useState('latest')
  const [requestForm, setRequestForm] = useState({
    genre: '',
    target: '',
    time: '',
    place: '',
    message: '',
  })

  const goHome = () => {
    setPage('home')
  }

  const moveToDetail = (call) => {
    setSelectedCall(call)
  }

  const handleInputChange = (key, value) => {
    setRequestForm({
      ...requestForm,
      [key]: value,
    })
  }

  const submitRequest = () => {
    alert('Callture 요청이 등록되었습니다!')
    setPage('list')
  }

  const openAdminMode = () => {
    if (isAdminAuthenticated) {
      setPage('creator')
      return
    }

    setAdminPassword('')
    setIsAdminLoginOpen(true)
  }

  const submitAdminPassword = () => {
    if (adminPassword === ADMIN_PASSWORD) {
      setIsAdminAuthenticated(true)
      setIsAdminLoginOpen(false)
      setPage('creator')
    } else {
      alert('비밀번호가 틀렸습니다.')
    }
  }

  return (
    <div className="app">
      <header className="top-nav">
        <button className="logo-button" onClick={goHome}>
          <span>Call</span>
          <span>ture</span>
        </button>
      </header>

      {page === 'home' && (
        <HomePage
          onRequestClick={() => setPage('request')}
          onListClick={() => setPage('list')}
          onCreatorClick={openAdminMode}
          onHelpClick={() => setIsHelpOpen(true)}
          onFeatureClick={() => setIsFeatureOpen(true)}
          onMatchingClick={() => setPage('matching')}
          onMyProgramClick={() => setPage('my')}
        />
      )}

      {page === 'request' && (
        <RequestPage
          requestForm={requestForm}
          onChange={handleInputChange}
          onSubmit={submitRequest}
          onBack={goHome}
        />
      )}

      {page === 'list' && (
        <CalltureListPage
          calls={cultureCalls}
          selectedCall={selectedCall}
          onSelect={moveToDetail}
          onRequestClick={() => setPage('request')}
          filter={filter}
          onFilterChange={setFilter}
          onBack={goHome}
        />
      )}

      {page === 'creator' && (
        <CreatorModePage
          calls={cultureCalls}
          spaces={creatorSpaces}
          onBack={goHome}
        />
      )}

      {page === 'matching' && (
        <MatchingPage
          programs={matchedPrograms}
          onMyProgramClick={() => setPage('my')}
          onBack={goHome}
        />
      )}

      {page === 'my' && (
        <MyProgramPage
          programs={myPrograms}
          onBack={goHome}
        />
      )}

      {isHelpOpen && <HelpModal onClose={() => setIsHelpOpen(false)} />}
      {isFeatureOpen && <FeatureModal onClose={() => setIsFeatureOpen(false)} />}

      {isAdminLoginOpen && (
        <AdminLoginModal
          password={adminPassword}
          onChangePassword={setAdminPassword}
          onSubmit={submitAdminPassword}
          onClose={() => setIsAdminLoginOpen(false)}
        />
      )}
    </div>
  )
}

function PageLayout({ children, onBack }) {
  return (
    <main className="page">
      <BackButton onBack={onBack} />
      {children}
    </main>
  )
}

function BackButton({ onBack }) {
  return (
    <button className="back-button" onClick={onBack} aria-label="메인으로 돌아가기">
      ←
    </button>
  )
}

function HomePage({
  onRequestClick,
  onListClick,
  onCreatorClick,
  onHelpClick,
  onFeatureClick,
  onMatchingClick,
  onMyProgramClick,
}) {
  return (
    <main className="page home-page">
      <section className="simple-hero">
        <div className="brand-mark">
          <span>Call</span>
          <span>ture</span>
        </div>

        <p className="hero-description">
          요청이 모이면, 문화가 열립니다.
        </p>

        <div className="home-menu-grid">
          <button className="home-menu-card primary-card" onClick={onRequestClick}>
            <span className="menu-emoji">✍️</span>
            <strong>요청하기</strong>
          </button>

          <button className="home-menu-card" onClick={onListClick}>
            <span className="menu-emoji">📮</span>
            <strong>목록 보기</strong>
          </button>

          <button className="home-menu-card" onClick={onMatchingClick}>
            <span className="menu-emoji">🤝</span>
            <strong>매칭</strong>
          </button>

          <button className="home-menu-card" onClick={onMyProgramClick}>
            <span className="menu-emoji">🎟️</span>
            <strong>내 프로그램</strong>
          </button>

          <button className="home-menu-card" onClick={onFeatureClick}>
            <span className="menu-emoji">✨</span>
            <strong>상세정보</strong>
          </button>

          <button className="home-menu-card admin-card" onClick={onCreatorClick}>
            <span className="menu-emoji">🗺️</span>
            <strong>관리자</strong>
          </button>

          <button className="home-menu-card wide-card" onClick={onHelpClick}>
            <span className="menu-emoji">❔</span>
            <strong>진행 방식</strong>
          </button>
        </div>
      </section>
    </main>
  )
}

function HelpModal({ onClose }) {
  return (
    <div className="modal-backdrop">
      <section className="help-modal">
        <button className="modal-close-button" onClick={onClose}>
          ×
        </button>
        <p className="eyebrow">Callture</p>
        <h2>진행 방식</h2>

        <ol className="help-list">
          <li>
            <strong>요청</strong>
            <span>필요한 문화 활동을 작성합니다.</span>
          </li>
          <li>
            <strong>모이기</strong>
            <span>비슷한 요청이 하나로 묶입니다.</span>
          </li>
          <li>
            <strong>매칭</strong>
            <span>창작자와 공공공간을 연결합니다.</span>
          </li>
          <li>
            <strong>개설</strong>
            <span>작은 문화 프로그램이 열립니다.</span>
          </li>
        </ol>
      </section>
    </div>
  )
}

function FeatureModal({ onClose }) {
  return (
    <div className="modal-backdrop">
      <section className="feature-modal">
        <button className="modal-close-button" onClick={onClose}>
          ×
        </button>
        <p className="eyebrow">Callture</p>
        <h2>상세정보</h2>

        <div className="popup-feature-grid">
          <div className="popup-feature-card">
            <span>📍</span>
            <h3>요청 기반</h3>
            <p>주민이 직접 필요한 문화를 요청합니다.</p>
          </div>
          <div className="popup-feature-card">
            <span>🎨</span>
            <h3>창작자 연결</h3>
            <p>수요가 있는 요청에 지역 창작자가 연결됩니다.</p>
          </div>
          <div className="popup-feature-card">
            <span>🏛️</span>
            <h3>공간 배정</h3>
            <p>도서관, 주민센터, 청년센터를 활용합니다.</p>
          </div>
        </div>
      </section>
    </div>
  )
}

function AdminLoginModal({ password, onChangePassword, onSubmit, onClose }) {
  return (
    <div className="modal-backdrop">
      <section className="admin-login-modal">
        <button className="modal-close-button" onClick={onClose}>
          ×
        </button>

        <p className="eyebrow">Callture</p>
        <h2>관리자</h2>

        <input
          className="password-input"
          type="password"
          value={password}
          onChange={(e) => onChangePassword(e.target.value)}
          placeholder="비밀번호"
          autoFocus
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              onSubmit()
            }
          }}
        />

        <button className="primary-button full-button" onClick={onSubmit}>
          확인
        </button>
      </section>
    </div>
  )
}

function RequestPage({ requestForm, onChange, onSubmit, onBack }) {
  return (
    <PageLayout onBack={onBack}>
      <section className="section-header">
        <p className="eyebrow">Callture</p>
        <h1>무엇이 필요할까요?</h1>
      </section>

      <section className="form-card">
        <FormGroup label="장르">
          <div className="chip-row">
            {['공연', '전시', '영화', '연극', '체험', '전통문화체험', '강연'].map(
              (item) => (
                <button
                  key={item}
                  className={requestForm.genre === item ? 'chip active' : 'chip'}
                  onClick={() => onChange('genre', item)}
                >
                  {item}
                </button>
              )
            )}
          </div>
        </FormGroup>

        <FormGroup label="대상">
          <div className="chip-row">
            {['청소년', '청년', '가족', '고령층', '누구나'].map((item) => (
              <button
                key={item}
                className={requestForm.target === item ? 'chip active' : 'chip'}
                onClick={() => onChange('target', item)}
              >
                {item}
              </button>
            ))}
          </div>
        </FormGroup>

        <FormGroup label="시간">
          <div className="chip-row">
            {['평일 낮', '평일 저녁', '주말 낮', '주말 저녁'].map((item) => (
              <button
                key={item}
                className={requestForm.time === item ? 'chip active' : 'chip'}
                onClick={() => onChange('time', item)}
              >
                {item}
              </button>
            ))}
          </div>
        </FormGroup>

        <FormGroup label="장소">
          <div className="chip-row">
            {['도서관', '주민센터', '공원', '학교', '청년센터', '복지관', '상관없음'].map(
              (item) => (
                <button
                  key={item}
                  className={requestForm.place === item ? 'chip active' : 'chip'}
                  onClick={() => onChange('place', item)}
                >
                  {item}
                </button>
              )
            )}
          </div>
        </FormGroup>

        <FormGroup label="한 줄 요청">
          <textarea
            value={requestForm.message}
            onChange={(e) => onChange('message', e.target.value)}
            placeholder="예: 평일 낮에 작은 전시가 있으면 좋겠어요."
          />
        </FormGroup>

        <button className="primary-button full-button" onClick={onSubmit}>
          등록
        </button>
      </section>
    </PageLayout>
  )
}

function CalltureListPage({
  calls,
  selectedCall,
  onSelect,
  onRequestClick,
  filter,
  onFilterChange,
  onBack,
}) {
  const [isDetailOpen, setIsDetailOpen] = useState(false)

  const filteredCalls = useMemo(() => {
    const copied = [...calls]

    if (filter === 'latest') {
      return copied.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    }

    if (filter === 'rate') {
      return copied.sort((a, b) => b.current / b.goal - a.current / a.goal)
    }

    return copied.filter((call) => call.genre === filter)
  }, [calls, filter])

  const selectCall = (call) => {
    onSelect(call)
    setIsDetailOpen(false)
  }

  return (
    <PageLayout onBack={onBack}>
      <section className="section-header">
        <p className="eyebrow">Callture</p>
        <h1>요청 목록</h1>
      </section>

      <div className="filter-row">
        {[
          { key: 'latest', label: '최신순' },
          { key: 'rate', label: '달성률순' },
          { key: '전통문화체험', label: '전통문화' },
          { key: '전시', label: '전시' },
          { key: '영화', label: '영화' },
          { key: '연극', label: '연극' },
          { key: '체험', label: '체험' },
          { key: '공연', label: '공연' },
        ].map((item) => (
          <button
            key={item.key}
            className={filter === item.key ? 'filter-chip active' : 'filter-chip'}
            onClick={() => onFilterChange(item.key)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="list-layout">
        <section className="call-list">
          {filteredCalls.map((call) => (
            <CalltureCard key={call.id} call={call} onClick={() => selectCall(call)} />
          ))}
        </section>

        <section className="detail-panel compact-detail-panel">
          <div className="detail-title-row">
            <span className="big-emoji">{selectedCall.icon}</span>
            <div>
              <p className="eyebrow">선택됨</p>
              <h2>{selectedCall.title}</h2>
            </div>
          </div>

          <ProgressBar current={selectedCall.current} goal={selectedCall.goal} />

          <button
            className="secondary-button full-button"
            onClick={() => setIsDetailOpen(!isDetailOpen)}
          >
            {isDetailOpen ? '닫기' : '상세정보'}
          </button>

          {isDetailOpen && (
            <>
              <div className="condition-box">
                <h3>조건</h3>
                <p>장르: {selectedCall.genre}</p>
                <p>대상: {selectedCall.target}</p>
                <p>시간: {selectedCall.time}</p>
                <p>장소: {selectedCall.place}</p>
                <p>{selectedCall.detail}</p>
              </div>

              <div className="similar-box">
                <h3>비슷한 요청</h3>
                <ul>
                  {selectedCall.similarRequests.map((request, index) => (
                    <li key={index}>{request}</li>
                  ))}
                </ul>
              </div>
            </>
          )}

          <button className="primary-button full-button" onClick={onRequestClick}>
            나도 요청
          </button>
        </section>
      </div>
    </PageLayout>
  )
}

function CreatorModePage({ calls, spaces, onBack }) {
  const readyCalls = calls.filter((call) => call.current / call.goal >= 0.7)
  const [selectedCall, setSelectedCall] = useState(readyCalls[0])
  const [selectedSpace, setSelectedSpace] = useState(spaces[0])
  const [isDetailOpen, setIsDetailOpen] = useState(false)

  return (
    <PageLayout onBack={onBack}>
      <section className="section-header">
        <p className="eyebrow">Callture</p>
        <h1>관리자</h1>
      </section>

      <div className="creator-layout">
        <section className="creator-panel">
          <h2>요청</h2>
          <div className="mini-list">
            {readyCalls.map((call) => (
              <button
                key={call.id}
                className={selectedCall.id === call.id ? 'mini-card active' : 'mini-card'}
                onClick={() => {
                  setSelectedCall(call)
                  setIsDetailOpen(false)
                }}
              >
                <span className="mini-emoji">{call.icon}</span>
                <strong>{call.title}</strong>
                <small>{call.current}/{call.goal}명</small>
              </button>
            ))}
          </div>
        </section>

        <section className="map-panel">
          <div className="map-placeholder">
            <p>🗺️</p>
            <strong>지도 API</strong>
            <span>Kakao / Naver / Google</span>
          </div>
        </section>

        <section className="creator-panel">
          <h2>공간</h2>
          <div className="mini-list">
            {spaces.map((space) => (
              <button
                key={space.id}
                className={selectedSpace.id === space.id ? 'mini-card active' : 'mini-card'}
                onClick={() => setSelectedSpace(space)}
              >
                <span className="mini-emoji">{space.icon}</span>
                <strong>{space.name}</strong>
                <small>{space.capacity}</small>
              </button>
            ))}
          </div>
        </section>
      </div>

      <section className="match-preview-card">
        <span className="status-badge">미리보기</span>
        <h2>{selectedCall.icon} {selectedCall.title}</h2>

        <button
          className="secondary-button full-button"
          onClick={() => setIsDetailOpen(!isDetailOpen)}
        >
          {isDetailOpen ? '닫기' : '상세정보'}
        </button>

        {isDetailOpen && (
          <div className="preview-grid">
            <div>
              <h3>요청</h3>
              <p>장르: {selectedCall.genre}</p>
              <p>대상: {selectedCall.target}</p>
              <p>시간: {selectedCall.time}</p>
              <p>인원: {selectedCall.current}/{selectedCall.goal}명</p>
            </div>

            <div>
              <h3>공간</h3>
              <p>공간명: {selectedSpace.name}</p>
              <p>유형: {selectedSpace.type}</p>
              <p>수용: {selectedSpace.capacity}</p>
              <p>용도: {selectedSpace.goodFor}</p>
            </div>
          </div>
        )}

        <button
          className="primary-button full-button"
          onClick={() => alert('공간 매칭이 저장되었습니다!')}
        >
          매칭
        </button>
      </section>
    </PageLayout>
  )
}

function MatchingPage({ programs, onMyProgramClick, onBack }) {
  const [openedId, setOpenedId] = useState(null)

  return (
    <PageLayout onBack={onBack}>
      <section className="section-header">
        <p className="eyebrow">Callture</p>
        <h1>매칭</h1>
      </section>

      <section className="matching-grid">
        {programs.map((program) => {
          const isOpen = openedId === program.id

          return (
            <article className="match-card" key={program.id}>
              <span className="status-badge">{program.status}</span>
              <h2>{program.icon} {program.title}</h2>

              <button
                className="secondary-button full-button"
                onClick={() => setOpenedId(isOpen ? null : program.id)}
              >
                {isOpen ? '닫기' : '상세정보'}
              </button>

              {isOpen && (
                <>
                  <div className="match-section">
                    <h3>창작자</h3>
                    <p className="strong">{program.creator}</p>
                    <p>{program.creatorInfo}</p>
                  </div>

                  <div className="match-section">
                    <h3>공간</h3>
                    <p className="strong">{program.space}</p>
                    <p>{program.spaceInfo}</p>
                  </div>
                </>
              )}

              <button className="primary-button full-button" onClick={onMyProgramClick}>
                신청
              </button>
            </article>
          )
        })}
      </section>
    </PageLayout>
  )
}

function MyProgramPage({ programs, onBack }) {
  const [openedProgramId, setOpenedProgramId] = useState(null)

  const toggleProgram = (programId) => {
    setOpenedProgramId(openedProgramId === programId ? null : programId)
  }

  return (
    <PageLayout onBack={onBack}>
      <section className="section-header">
        <p className="eyebrow">Callture</p>
        <h1>내 프로그램</h1>
      </section>

      <section className="program-list">
        {programs.map((program) => {
          const isOpen = openedProgramId === program.id

          return (
            <article className="program-card compact-program-card" key={program.id}>
              <div className="program-summary-row">
                <div>
                  <span className="status-badge">{program.status}</span>
                  <h2>{program.icon} {program.title}</h2>
                </div>

                <button
                  className="secondary-button"
                  onClick={() => toggleProgram(program.id)}
                >
                  {isOpen ? '닫기' : '상세정보'}
                </button>
              </div>

              {isOpen && (
                <div className="program-detail-box">
                  <p>일시: {program.date}</p>
                  <p>장소: {program.place}</p>
                  <p>대상: {program.target}</p>
                  <p>참가비: {program.fee}</p>
                </div>
              )}
            </article>
          )
        })}
      </section>
    </PageLayout>
  )
}

function CalltureCard({ call, onClick }) {
  return (
    <article className="call-card" onClick={onClick}>
      <div className="card-title-row">
        <div className="card-title-left">
          <span className="card-emoji">{call.icon}</span>
          <div>
            <h2>{call.title}</h2>
            <p>{call.summary}</p>
          </div>
        </div>
        <span>{call.current}/{call.goal}</span>
      </div>

      <div className="tag-row">
        <span>#{call.genre}</span>
        <span>#{call.target}</span>
        <span>#{call.time}</span>
      </div>

      <ProgressBar current={call.current} goal={call.goal} />
    </article>
  )
}

function ProgressBar({ current, goal }) {
  const percent = Math.min(Math.round((current / goal) * 100), 100)

  return (
    <div className="progress-area">
      <div className="progress-info">
        <span>{current}명</span>
        <span>{percent}%</span>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${percent}%` }}></div>
      </div>
    </div>
  )
}

function FormGroup({ label, children }) {
  return (
    <div className="form-group">
      <label>{label}</label>
      {children}
    </div>
  )
}

export default App