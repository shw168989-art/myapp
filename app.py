<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동물 캐릭터로 알아보는 나의 스트레스 대처 유형</title>
  <!-- Google Fonts 연동 -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
  <!-- CSS Stylesheet -->
  <link rel="stylesheet" href="src/style.css">
</head>
<body>
  <div class="app-container">
    <!-- 배경 데코레이션 블러 서클 -->
    <div class="bg-circle bg-circle-1"></div>
    <div class="bg-circle bg-circle-2"></div>

    <main class="card-wrapper">
      
      <!-- 1. 홈 스크린 -->
      <section id="screen-home" class="screen active">
        <div class="home-content">
          <div class="badge">Psychology Test</div>
          <h1 class="main-title">나의 스트레스<br>대처 동물은?</h1>
          <p class="subtitle">단 8개의 질문으로 알아보는 나의 스트레스 극복 성향과 마음의 날씨</p>
          
          <div class="main-illustration">
            <div class="emoji-group">
              <span class="animated-emoji">🦁</span>
              <span class="animated-emoji">🐨</span>
              <span class="animated-emoji">🐬</span>
              <span class="animated-emoji">🦊</span>
            </div>
          </div>

          <div class="action-group">
            <button id="btn-start" class="btn btn-primary">테스트 시작하기</button>
            <button id="btn-resume" class="btn btn-secondary hidden">이어서 진행하기</button>
            <button id="btn-view-history" class="btn btn-link">지난 결과 보기</button>
          </div>
        </div>
      </section>

      <!-- 2. 검사 진행 스크린 -->
      <section id="screen-test" class="screen">
        <div class="test-header">
          <button id="btn-back" class="btn-icon-back" aria-label="이전 단계로">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          </button>
          <div class="progress-container">
            <div class="progress-text"><span id="current-question-num">1</span>/8</div>
            <div class="progress-bar-bg">
              <div id="progress-bar-fill" class="progress-bar-fill"></div>
            </div>
          </div>
        </div>

        <div class="test-body">
          <h2 id="question-text" class="question-title">질문 텍스트가 로드되는 중입니다...</h2>
          <div class="options-container">
            <button class="option-card" data-option="A">
              <div class="option-letter">A</div>
              <p class="option-text" id="option-a-text">답변 A</p>
            </button>
            <button class="option-card" data-option="B">
              <div class="option-letter">B</div>
              <p class="option-text" id="option-b-text">답변 B</p>
            </button>
          </div>
        </div>
      </section>

      <!-- 3. 결과 분석 스크린 -->
      <section id="screen-result" class="screen">
        <div class="result-header">
          <div class="badge success-badge">진단 완료</div>
          <h2 class="result-title-label">당신의 스트레스 대처 유형은...</h2>
        </div>

        <div class="result-body">
          <div class="result-animal-card">
            <span id="result-emoji" class="result-emoji">🦁</span>
            <h3 id="result-name" class="result-animal-name">용감한 사자형</h3>
            <p id="result-tagline" class="result-tagline">"정면 돌파! 문제를 직면하고 해결해야 직성이 풀리는 스타일"</p>
          </div>

          <div class="result-details">
            <div class="detail-section">
              <h4>💡 나의 대처 방식 특징</h4>
              <p id="result-desc">특징 설명글이 표시됩니다.</p>
            </div>
            
            <div class="detail-section highlight-box">
              <h4>🎯 마인드셋 추천 처방</h4>
              <p id="result-prescription">조언 가이드가 표시됩니다.</p>
            </div>
          </div>

          <div class="action-group vertical-group">
            <button id="btn-copy-link" class="btn btn-secondary">결과 링크 복사하기</button>
            <div class="btn-row">
              <button id="btn-restart" class="btn btn-primary">다시 테스트하기</button>
              <button id="btn-home" class="btn btn-outline">홈으로</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. 지난 기록(History) 스크린 -->
      <section id="screen-history" class="screen">
        <div class="history-header">
          <h2 class="history-title">지난 테스트 기록</h2>
          <p class="history-subtitle">로컬에 저장된 나의 스트레스 관리 여정</p>
        </div>

        <div class="history-body">
          <ul id="history-list" class="history-list">
            <!-- 동적으로 히스토리 아이템 삽입 예정 -->
          </ul>
          
          <div id="history-empty" class="history-empty hidden">
            <span class="empty-icon">📂</span>
            <p>저장된 테스트 기록이 없습니다.<br>첫 테스트를 시작해 보세요!</p>
          </div>
        </div>

        <div class="history-footer">
          <button id="btn-clear-history" class="btn btn-danger">모든 기록 삭제</button>
          <button id="btn-history-back" class="btn btn-primary">홈으로 돌아가기</button>
        </div>
      </section>

    </main>
  </div>

  <!-- JavaScript Modules -->
  <script src="src/app.js"></script>
</body>
</html>
