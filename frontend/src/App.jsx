import { useMemo, useState } from 'react'
import './App.css'

const cultureCalls = [
  {
    id: 1,
    title: '한옥 마을 전통문화 체험',
    genre: '전통문화체험',
    target: '가족',
    time: '주말 낮',
    place: '한옥마을 / 주민센터',
    current: 28,
    goal: 30,
    createdAt: '2026-05-08',
    summary: '전통 공예와 한복 체험을 함께 즐기는 지역 문화 프로그램 요청',
    similarRequests: [
      '전통문화를 직접 체험할 수 있는 프로그램이 있으면 좋겠어요.',
      '아이와 함께 한복이나 공예 체험을 해보고 싶어요.',
      '지역 전통문화를 쉽게 접할 기회가 필요해요.',
    ],
  },
  {
    id: 2,
    title: '퇴근 후 인디 음악 공연',
    genre: '공연',
    target: '청년',
    time: '평일 저녁',
    place: '청년센터 / 공공공간',
    current: 41,
    goal: 50,
    createdAt: '2026-05-07',
    summary: '퇴근 후 가볍게 즐길 수 있는 동네 인디 공연 요청',
    similarRequests: [
      '평일 저녁에 부담 없이 볼 수 있는 공연이 있었으면 좋겠어요.',
      '지역 청년 밴드 공연을 보고 싶어요.',
      '멀리 가지 않아도 즐길 수 있는 작은 공연이 필요해요.',
    ],
  },
  {
    id: 3,
    title: '청소년 독립영화 상영회',
    genre: '영화',
    target: '청소년',
    time: '주말 저녁',
    place: '학교 / 도서관',
    current: 18,
    goal: 30,
    createdAt: '2026-05-06',
    summary: '청소년이 안전하게 참여할 수 있는 지역 영화 상영회 요청',
    similarRequests: [
      '청소년끼리 볼 수 있는 영화 프로그램이 있으면 좋겠어요.',
      '학교 근처에서 영화 상영회를 열어주세요.',
      '친구들과 함께 갈 수 있는 문화 공간이 필요해요.',
    ],
  },
  {
    id: 4,
    title: '동네 작가 사진 전시',
    genre: '전시',
    target: '누구나',
    time: '평일 낮',
    place: '도서관 / 문화센터',
    current: 16,
    goal: 25,
    createdAt: '2026-05-05',
    summary: '지역 사진 작가의 작품을 가까운 공공공간에서 보고 싶은 요청',
    similarRequests: [
      '동네 작가들의 전시를 쉽게 볼 수 있으면 좋겠어요.',
      '도서관 한쪽에서 작은 사진전이 열리면 좋겠어요.',
      '지역의 모습을 담은 전시가 필요해요.',
    ],
  },
  {
    id: 5,
    title: '어르신을 위한 연극 관람',
    genre: '연극',
    target: '고령층',
    time: '평일 낮',
    place: '주민센터 / 복지관',
    current: 22,
    goal: 35,
    createdAt: '2026-05-04',
    summary: '고령층이 가까운 곳에서 편하게 볼 수 있는 작은 연극 요청',
    similarRequests: [
      '어르신들이 멀리 가지 않고 연극을 볼 수 있으면 좋겠어요.',
      '복지관에서 문화 공연이 자주 열리면 좋겠어요.',
      '낮 시간대에 볼 수 있는 연극 프로그램이 필요해요.',
    ],
  },
  {
    id: 6,
    title: '주말 가족 공예 체험',
    genre: '체험',
    target: '가족',
    time: '주말 낮',
    place: '도서관 / 주민센터',
    current: 24,
    goal: 30,
    createdAt: '2026-05-03',
    summary: '아이와 함께 참여할 수 있는 주말 공예 프로그램 요청',
    similarRequests: [
      '아이랑 같이 할 수 있는 만들기 수업이 있으면 좋겠어요.',
      '도서관에서 가족 대상 공예 체험을 열어주세요.',
      '주말에 부모와 아이가 함께할 문화 활동이 필요해요.',
    ],
  },
]

const matchedPrograms = [
  {
    id: 1,
    title: '한옥 마을 전통문화 체험',
    creator: '달빛한지 공방',
    creatorInfo: '전통 공예 / 한지 조명 / 가족 체험 가능',
    space: '○○한옥문화센터',
    spaceInfo: '주말 낮 사용 가능 / 30명 수용 가능',
    status: '신청자 모집 중',
  },
  {
    id: 2,
    title: '퇴근 후 인디 음악 공연',
    creator: '로컬사운드 팀',
    creatorInfo: '인디 음악 / 어쿠스틱 공연 / 60분 공연 가능',
    space: '○○청년센터 라운지',
    spaceInfo: '평일 저녁 사용 가능 / 음향 장비 보유',
    status: '신청자 모집 중',
  },
  {
    id: 3,
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
    title: '우리 동네 한지 조명 만들기',
    date: '토요일 오후 2시',
    place: '○○한옥문화센터',
    target: '가족 / 누구나',
    fee: '5,000원',
    status: '신청 완료',
  },
  {
    id: 2,
    title: '퇴근 후 인디 어쿠스틱 공연',
    date: '금요일 오후 7시',
    place: '○○청년센터',
    target: '청년 / 누구나',
    fee: '무료',
    status: '참여 예정',
  },
  {
    id: 3,
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
  const [filter, setFilter] = useState('latest')
  const [requestForm, setRequestForm] = useState({
    genre: '',
    target: '',
    time: '',
    place: '',
    message: '',
  })

  const moveToDetail = (call) => {
    setSelectedCall(call)
    setPage('list')
  }

  const handleInputChange = (key, value) => {
    setRequestForm({
      ...requestForm,
      [key]: value,
    })
  }

  const submitRequest = () => {
    alert('문화콜 요청이 등록되었습니다!')
    setPage('list')
  }

  return (
    <div className="app">
      <header className="top-nav">
        <button className="logo-button" onClick={() => setPage('home')}>
          콜쳐
        </button>

        <nav>
          <button onClick={() => setPage('home')}>메인</button>
          <button onClick={() => setPage('request')}>요청하기</button>
          <button onClick={() => setPage('list')}>문화콜 목록</button>
          <button onClick={() => setPage('matching')}>매칭</button>
          <button onClick={() => setPage('my')}>나의 프로그램</button>
        </nav>
      </header>

      {page === 'home' && (
        <HomePage
          onRequestClick={() => setPage('request')}
          onListClick={() => setPage('list')}
          onHelpClick={() => setIsHelpOpen(true)}
        />
      )}

      {page === 'request' && (
        <RequestPage
          requestForm={requestForm}
          onChange={handleInputChange}
          onSubmit={submitRequest}
        />
      )}

      {page === 'list' && (
        <CultureCallListPage
          calls={cultureCalls}
          selectedCall={selectedCall}
          onSelect={moveToDetail}
          onRequestClick={() => setPage('request')}
          filter={filter}
          onFilterChange={setFilter}
        />
      )}

      {page === 'matching' && (
        <MatchingPage
          programs={matchedPrograms}
          onMyProgramClick={() => setPage('my')}
        />
      )}

      {page === 'my' && <MyProgramPage programs={myPrograms} />}

      {isHelpOpen && <HelpModal onClose={() => setIsHelpOpen(false)} />}
    </div>
  )
}

function HomePage({ onRequestClick, onListClick, onHelpClick }) {
  return (
    <main className="page">
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">문화 요청 매칭 플랫폼</p>
          <h1>콜쳐</h1>
          <p className="hero-description">
            우리 동네에 필요한 문화를 직접 요청하고, 요청이 모이면 실제 프로그램으로 연결해요.
          </p>

          <div className="hero-actions">
            <button className="primary-button" onClick={onRequestClick}>
              문화 요청하기
            </button>
            <button className="secondary-button" onClick={onListClick}>
              문화콜 목록 보기
            </button>
            <button className="help-button" onClick={onHelpClick}>
              진행 방식 보기
            </button>
          </div>
        </div>

        <div className="main-preview-card">
          <span className="status-badge">성사 직전</span>
          <h2>한옥 마을 전통문화 체험</h2>
          <p>28명 요청 / 목표 30명</p>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '93%' }}></div>
          </div>
          <p className="remain-text">2명만 더 모이면 매칭이 시작돼요</p>
        </div>
      </section>

      <section className="feature-grid">
        <div className="feature-card">
          <h3>요청 기반</h3>
          <p>주민이 원하는 문화 수요에서 프로그램이 시작됩니다.</p>
        </div>
        <div className="feature-card">
          <h3>창작자 연결</h3>
          <p>지역 창작자가 실제 수요가 있는 곳에서 활동합니다.</p>
        </div>
        <div className="feature-card">
          <h3>공간 매칭</h3>
          <p>도서관, 주민센터, 청년센터가 문화 공간이 됩니다.</p>
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
        <p className="eyebrow">콜쳐 이용 방법</p>
        <h2>문화콜 진행 방식</h2>

        <ol className="help-list">
          <li>
            <strong>요청 작성</strong>
            <span>사용자가 원하는 문화 활동을 장르, 대상, 시간, 장소와 함께 작성합니다.</span>
          </li>
          <li>
            <strong>요청 묶기</strong>
            <span>비슷한 요청끼리 하나의 문화콜로 묶입니다.</span>
          </li>
          <li>
            <strong>목표 달성</strong>
            <span>요청 인원이 일정 수를 넘으면 창작자와 공간 매칭이 시작됩니다.</span>
          </li>
          <li>
            <strong>프로그램 개설</strong>
            <span>지역 창작자와 공공공간이 연결되어 작은 문화 프로그램이 열립니다.</span>
          </li>
        </ol>
      </section>
    </div>
  )
}

function RequestPage({ requestForm, onChange, onSubmit }) {
  return (
    <main className="page narrow-page">
      <section className="section-header">
        <p className="eyebrow">문화 요청 작성</p>
        <h1>어떤 문화가 필요하세요?</h1>
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
            placeholder="예: 우리 동네에서 평일 낮에 볼 수 있는 작은 전시가 있으면 좋겠어요."
          />
        </FormGroup>

        <button className="primary-button full-button" onClick={onSubmit}>
          문화콜 요청하기
        </button>
      </section>
    </main>
  )
}

function CultureCallListPage({
  calls,
  selectedCall,
  onSelect,
  onRequestClick,
  filter,
  onFilterChange,
}) {
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

  return (
    <main className="page">
      <section className="section-header">
        <p className="eyebrow">문화콜 목록</p>
        <h1>신청된 문화콜</h1>
      </section>

      <div className="filter-row">
        {[
          { key: 'latest', label: '최신순' },
          { key: 'rate', label: '달성률순' },
          { key: '전통문화체험', label: '전통문화체험' },
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
            <CultureCallCard key={call.id} call={call} onClick={() => onSelect(call)} />
          ))}
        </section>

        <section className="detail-panel">
          <p className="eyebrow">선택한 문화콜</p>
          <h2>{selectedCall.title}</h2>
          <ProgressBar current={selectedCall.current} goal={selectedCall.goal} />

          <p className="highlight-text">
            {selectedCall.goal - selectedCall.current}명만 더 요청하면 창작자 매칭이
            시작돼요!
          </p>

          <div className="condition-box">
            <h3>요청 조건 요약</h3>
            <p>장르: {selectedCall.genre}</p>
            <p>대상: {selectedCall.target}</p>
            <p>시간: {selectedCall.time}</p>
            <p>장소: {selectedCall.place}</p>
            <p>{selectedCall.summary}</p>
          </div>

          <div className="similar-box">
            <h3>비슷한 요청 리스트</h3>
            <ul>
              {selectedCall.similarRequests.map((request, index) => (
                <li key={index}>{request}</li>
              ))}
            </ul>
          </div>

          <button className="primary-button full-button" onClick={onRequestClick}>
            나도 요청하기
          </button>
        </section>
      </div>
    </main>
  )
}

function MatchingPage({ programs, onMyProgramClick }) {
  return (
    <main className="page">
      <section className="section-header">
        <p className="eyebrow">창작자 · 공간 매칭</p>
        <h1>목표를 넘은 요청</h1>
      </section>

      <section className="matching-grid">
        {programs.map((program) => (
          <article className="match-card" key={program.id}>
            <span className="status-badge">{program.status}</span>
            <h2>{program.title}</h2>

            <div className="match-section">
              <h3>연결된 창작자</h3>
              <p className="strong">{program.creator}</p>
              <p>{program.creatorInfo}</p>
            </div>

            <div className="match-section">
              <h3>연결된 공공공간</h3>
              <p className="strong">{program.space}</p>
              <p>{program.spaceInfo}</p>
            </div>

            <button className="primary-button full-button" onClick={onMyProgramClick}>
              프로그램 신청하기
            </button>
          </article>
        ))}
      </section>
    </main>
  )
}

function MyProgramPage({ programs }) {
  return (
    <main className="page">
      <section className="section-header">
        <p className="eyebrow">나의 프로그램</p>
        <h1>신청자가 충족된 프로그램</h1>
      </section>

      <section className="program-list">
        {programs.map((program) => (
          <article className="program-card" key={program.id}>
            <div>
              <span className="status-badge">{program.status}</span>
              <h2>{program.title}</h2>
              <p>일시: {program.date}</p>
              <p>장소: {program.place}</p>
              <p>대상: {program.target}</p>
              <p>참가비: {program.fee}</p>
            </div>
            <button className="secondary-button">상세 보기</button>
          </article>
        ))}
      </section>
    </main>
  )
}

function CultureCallCard({ call, onClick }) {
  return (
    <article className="call-card" onClick={onClick}>
      <div className="card-title-row">
        <h2>{call.title}</h2>
        <span>{call.current}/{call.goal}명</span>
      </div>

      <p>{call.summary}</p>

      <div className="tag-row">
        <span>#{call.genre}</span>
        <span>#{call.target}</span>
        <span>#{call.time}</span>
      </div>

      <ProgressBar current={call.current} goal={call.goal} />

      <p className="remain-text">
        {call.goal - call.current}명만 더 모이면 매칭 시작
      </p>
    </article>
  )
}

function ProgressBar({ current, goal }) {
  const percent = Math.min(Math.round((current / goal) * 100), 100)

  return (
    <div className="progress-area">
      <div className="progress-info">
        <span>{current}명 요청</span>
        <span>목표 {goal}명</span>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${percent}%` }}></div>
      </div>
      <p className="progress-percent">{percent}% 달성</p>
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