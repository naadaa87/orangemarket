# 오렌지 마켓 홈페이지 (orange-market-web)

HMK홀딩스그룹 창고형 할인매장 **오렌지 마켓**의 브랜드·지점 안내 사이트입니다.
`HMK 홈페이지/프로그램 통합 제작기획서` 중 **07. HMK오렌지마켓 홈페이지** 명세를 기준으로 제작했습니다.

- 성격 : 정식 오픈 전 Launch Site (기대고객·공급사 DB 확보)
- 1차 범위 : 온라인 주문·결제 없음 (해당 기능은 10번 E커머스 쇼핑몰에서 운영)
- 빌드 도구 없음 : HTML·CSS·JS 정적 파일 그대로 배포

---

## 1. 5분 만에 배포하기

### 1-1. GitHub 저장소에 올리기

```bash
cd orange-market-web

git init
git branch -M main
git add .
git commit -m "오렌지마켓 홈페이지 초기 구축"

# GitHub에서 만든 빈 저장소 주소로 바꿔 주세요
git remote add origin https://github.com/<계정>/<저장소>.git
git push -u origin main
```

> 기획서 2-3의 Monorepo 구조를 따를 경우, 이 폴더 전체를 `apps/orange-market-web/` 위치에 넣으면 됩니다.
> 그 경우 아래 **Root directory** 값만 `apps/orange-market-web`으로 지정하시면 동일하게 동작합니다.

### 1-2. Cloudflare Pages 연결

1. Cloudflare 대시보드 → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. 방금 올린 저장소를 선택
3. 빌드 설정을 아래와 같이 입력합니다.

| 항목 | 값 |
|---|---|
| Project name | `hmk-orange-market` |
| Production branch | `main` |
| Framework preset | **None** |
| Build command | **(비워 둡니다)** |
| Build output directory | `/` &nbsp;*(Monorepo면 `apps/orange-market-web`)* |
| Root directory | `/` &nbsp;*(Monorepo면 `apps/orange-market-web`)* |

4. **Save and Deploy** 를 누르면 1~2분 안에 `https://<프로젝트명>.pages.dev` 주소가 나옵니다.

빌드 명령이 없으므로 실패할 여지가 거의 없습니다. 이후 `main`에 push할 때마다 자동 재배포되고,
Pull Request를 열면 검수용 Preview URL이 따로 생성됩니다.

### 1-3. 배포 직후 반드시 바꿔야 할 값

도메인이 확정되면 아래 세 곳의 주소를 실제 도메인으로 교체하세요.

| 파일 | 위치 | 현재 값 |
|---|---|---|
| 모든 `.html` | `<link rel="canonical">`, `og:url`, `og:image` | `https://orange-market.pages.dev` |
| `sitemap.xml` | 모든 `<loc>` | `https://orange-market.pages.dev` |
| `robots.txt` | `Sitemap:` | `https://orange-market.pages.dev` |

한 번에 바꾸는 방법 :

```bash
# macOS
grep -rl "orange-market.pages.dev" . | xargs sed -i '' 's|orange-market.pages.dev|www.오렌지마켓도메인.co.kr|g'

# Linux
grep -rl "orange-market.pages.dev" . | xargs sed -i 's|orange-market.pages.dev|www.오렌지마켓도메인.co.kr|g'
```

또는 `tools/build-pages.py` 상단의 `SITE` 값을 바꾸고 재생성해도 됩니다. (4장 참고)

---

## 2. 문의 폼 연결하기

문의·오픈알림 폼 4종(오픈알림 / 대량구매 / 입점납품 / 일반문의)은
`functions/api/lead.js` 한 파일이 모두 처리합니다. Cloudflare Pages Functions로 **자동 인식**되므로
별도 설정 없이도 배포 즉시 동작합니다.

다만 저장소를 연결하지 않으면 접수 내용이 어디에도 남지 않습니다. 아래 둘 중 하나는 꼭 설정해 주세요.

### 방법 A. KV에 저장하기 (권장)

1. Cloudflare 대시보드 → **Workers & Pages** → **KV** → **Create namespace**
   이름 예시 : `orange-market-leads`
2. Pages 프로젝트 → **Settings** → **Functions** → **KV namespace bindings** → **Add binding**

| Variable name | KV namespace |
|---|---|
| `LEADS` | `orange-market-leads` |

3. Production / Preview 양쪽에 모두 추가한 뒤 재배포합니다.

저장 키 형식은 `lead:<폼종류>:<접수시각>:<난수>` 이며,
개인정보처리방침의 보관기간에 맞춰 오픈알림은 12개월, 문의는 24개월 후 자동 삭제됩니다.

접수 내역 확인은 KV 네임스페이스 화면에서 직접 보거나, 아래 명령으로 내려받을 수 있습니다.

```bash
npx wrangler kv key list --namespace-id <네임스페이스ID>
npx wrangler kv key get "lead:notify:1735..." --namespace-id <네임스페이스ID>
```

### 방법 B. 웹훅으로 즉시 알림받기

Pages 프로젝트 → **Settings** → **Environment variables** 에 추가합니다.

| Variable name | Value |
|---|---|
| `LEAD_WEBHOOK_URL` | Slack Incoming Webhook 주소 또는 사내 API 주소 |

접수될 때마다 아래 형태의 JSON이 전달됩니다.

```json
{
  "id": "lead:supply:1735689600000:a1b2c3d4",
  "formType": "supply",
  "company": "오렌지식품",
  "name": "김담당",
  "phone": "010-1234-5678",
  "email": "kim@example.com",
  "item": "생수 2L 6입",
  "category": "대용량·벌크",
  "agreePrivacy": true,
  "agreeMarketing": false,
  "receivedAt": "2026-01-01T00:00:00.000Z"
}
```

A와 B를 함께 켜면 저장과 알림이 동시에 처리됩니다.
나중에 ERP(13번 통합매입관리)의 공급사 제안 API가 준비되면 `LEAD_WEBHOOK_URL`만 그 주소로 바꾸면 됩니다.

### 검증 규칙

서버에서도 아래를 다시 확인합니다. 프런트 검증만 믿지 않습니다.

- 폼 종류별 필수값 확인 (누락 시 400)
- 개인정보 수집·이용 동의 없으면 거부
- 이메일·휴대폰 형식 확인
- 제어문자 제거 및 항목별 길이 제한
- 숨김 필드(`website`)가 채워지면 봇으로 판단해 무시

---

## 3. 커스텀 도메인과 보안

### 도메인 연결

Pages 프로젝트 → **Custom domains** → **Set up a domain** 에서 도메인을 입력합니다.
Cloudflare에서 네임서버를 관리 중이면 DNS 레코드가 자동 생성되고, HTTPS 인증서도 자동 발급됩니다.

### 이미 적용된 보안 헤더 (`_headers`)

| 헤더 | 목적 |
|---|---|
| `Content-Security-Policy` | 스크립트·스타일·폰트 출처를 지정 도메인으로 제한 |
| `Strict-Transport-Security` | HTTPS 강제 (1년) |
| `X-Frame-Options`, `frame-ancestors` | 외부 사이트 iframe 삽입 차단 |
| `X-Content-Type-Options` | MIME 스니핑 차단 |
| `Referrer-Policy` | 외부 이동 시 경로 정보 최소 전달 |
| `Permissions-Policy` | 위치·마이크·카메라 권한 차단 |

> 웹폰트를 사내망에서 직접 호스팅해야 한다면, CSP의 `cdn.jsdelivr.net`·`fonts.googleapis.com` 항목을 지우고
> 6장의 폰트 자체 호스팅 방법을 따라 주세요.

### 주소 규칙 (중요)

Cloudflare Pages는 **`/brand.html` 요청을 자동으로 `/brand` 로 308 리디렉션**합니다.
이 동작은 대시보드에서 끌 수 없습니다.

따라서 `_redirects` 에 아래와 같은 규칙을 넣으면 **무한 리디렉션 루프**가 생겨
`ERR_TOO_MANY_REDIRECTS` 오류가 납니다.

```
# 절대 넣지 마세요 — 무한 루프가 생깁니다
/brand    /brand.html    200
```

```
/brand  →  (내 규칙) /brand.html  →  (Cloudflare 기본) /brand  →  (내 규칙) /brand.html  →  …
```

확장자 없는 주소는 **아무 설정 없이 이미 동작**하므로 규칙을 적을 필요가 없습니다.
사이트의 모든 내부 링크도 `href="/brand"` 형태로 되어 있어 리디렉션 없이 바로 열립니다.

현재 `_redirects` 에는 실제로 다른 페이지로 보내야 하는 별칭만 들어 있습니다.

| 입력 주소 | 이동할 곳 |
|---|---|
| `/open`, `/contact`, `/inquiry` | `/notify` |
| `/store` | `/stores` |
| `/stores/1` | `/store-detail` |
| `/franchise`, `/partner` | `/supply` |
| `/b2b` | `/business` |

---

## 4. 폴더 구조와 수정 방법

```
orange-market-web/
├─ index.html              홈
├─ brand.html              브랜드 소개
├─ category.html           상품 카테고리 (통로 01~05)
├─ deals.html              특가·행사
├─ stores.html             지점 안내 (상태 필터)
├─ store-detail.html       1호점 미리보기
├─ business.html           대량·사업자 구매 + 견적 폼
├─ supply.html             입점·납품 + 제안 폼
├─ membership.html         멤버십 안내
├─ faq.html                자주 묻는 질문 (검색·분류 필터)
├─ notify.html             오픈 알림 신청 + 일반 문의
├─ privacy.html            개인정보처리방침
├─ terms.html              이용약관
├─ 404.html                오류 페이지
│
├─ assets/
│  ├─ css/site.css         디자인 시스템 전체 (토큰 → 컴포넌트 순)
│  ├─ js/site.js           헤더·아코디언·필터·폼검증 (라이브러리 없음)
│  ├─ img/                 WebP 이미지 38장 (데스크톱 + `-sm` 모바일본)
│  └─ icons/favicon.svg
│
├─ functions/api/lead.js   문의 접수 API (Pages Functions)
├─ tools/build-pages.py    페이지 재생성 스크립트 (선택)
├─ tools/serve.py          로컬 미리보기 서버 (선택)
│
├─ _headers                보안 헤더·캐시 정책
├─ _redirects              짧은 주소 연결
├─ robots.txt / sitemap.xml / site.webmanifest
├─ CONTENT-GUIDE.md        확정 전 항목 교체 위치 안내
└─ README.md
```

### 로컬에서 확인하기

HTML 파일을 더블클릭해서 열면 `/brand` 같은 주소가 동작하지 않습니다.
Cloudflare와 같은 방식으로 확인하려면 아래 중 하나를 쓰세요.

```bash
python3 tools/serve.py          # 내장 미리보기 서버 → http://localhost:8080
npx wrangler pages dev .        # Cloudflare 공식 도구 (Functions 폼까지 함께 테스트)
```

문의 폼(`functions/api/lead.js`)까지 확인하려면 `wrangler` 쪽을 쓰셔야 합니다.

### 내용을 고치는 두 가지 방법

**① HTML을 직접 고칩니다 (간단한 문구 수정)**
해당 `.html` 파일을 열어 문장을 바꾸고 push하면 끝입니다.

**② 생성 스크립트로 다시 만듭니다 (헤더·푸터·메뉴처럼 모든 페이지에 걸친 수정)**
헤더와 푸터는 14개 파일에 똑같이 들어가 있습니다. 한 번에 바꾸려면 :

```bash
cd tools
python3 build-pages.py          # 14개 html을 모두 다시 생성
```

`build-pages.py` 안에서 `SITE`(도메인), `NAV`(메뉴), 헤더·푸터 HTML을 관리합니다.
이 스크립트는 배포에 필요하지 않습니다. Cloudflare는 실행하지 않으며 개발 편의용입니다.

---

## 5. 디자인 시스템 요약

`assets/css/site.css` 최상단 `:root` 의 값만 바꾸면 사이트 전체 톤이 바뀝니다.

| 토큰 | 값 | 사용처 |
|---|---|---|
| `--orange` | `#FF6A00` | 가격, 행사, 버튼, 통로 번호 |
| `--navy` | `#0D1B2A` | 제목, 안내판 바탕, 푸터 |
| `--paper` | `#F5F5F2` | 섹션 교차 배경 |
| `--ink` / `--muted` | `#1A1A1A` / `#6B6B63` | 본문 / 보조 문구 |
| `--go` / `--wait` | `#00806A` / `#A86400` | 완료 / 진행중 상태 |
| `--wrap` | `1280px` | 최대 콘텐츠 폭 |

기획서 3-4의 지시대로 **화이트·차콜을 넓게 쓰고 오렌지는 가격·행사·CTA에만** 씁니다.
상태 표시는 색상만으로 구분하지 않고 항상 텍스트 라벨을 함께 넣습니다(WCAG AA).

**시그니처 컴포넌트**

- `.sign` — 매장 천장 통로 안내판을 옮긴 섹션 헤더
- `.aisle` — 통로 01~05 카테고리 카드 (홈페이지 순서 = 실제 매장 통로 순서)
- `.ptag` / `.plegend` — 가격표 표기 규격과 항목 설명
- `.prep` — 오픈 준비 단계 타임라인

---

## 6. 자주 하는 작업

### 지점을 추가하려면

`stores.html` 에서 `<article class="store" data-item data-tags="...">` 블록을 통째로 복사한 뒤
`data-tags` 값을 상태에 맞게 바꿉니다. (`ready` 오픈준비 / `review` 검토중 / `open` 영업중)
필터 버튼은 이 값을 기준으로 동작하므로 별도 수정이 필요 없습니다.

### FAQ를 추가하려면

`faq.html` 의 `.acc__it` 블록을 복사하고 `data-tags` 에 분류명을 넣습니다.
구조화 데이터(FAQPage JSON-LD)도 함께 반영하려면 `tools/build-pages.py` 의 `FAQS` 목록에 추가한 뒤 재생성하세요.

### 이미지를 교체하려면

`assets/img/` 에 같은 파일명으로 덮어씁니다. WebP 권장이며, 원본 PNG는 아래 명령으로 변환합니다.

```bash
python3 -c "
from PIL import Image
im = Image.open('원본.png').convert('RGB')
im.thumbnail((1400, 1400))
im.save('assets/img/이름.webp', 'WEBP', quality=82, method=6)
"
```

`-sm` 이 붙은 파일은 모바일용 축소본입니다. 히어로 이미지만 `<picture>` 로 분기하고 있습니다.

### 폰트를 자체 호스팅하려면

현재 Pretendard와 Archivo를 CDN에서 불러옵니다. 사내 정책상 외부 요청이 막혀 있다면 :

1. [Pretendard 릴리스](https://github.com/orioncactus/pretendard/releases)에서 `woff2` 를 받아 `assets/fonts/` 에 넣습니다.
2. `site.css` 상단에 `@font-face` 를 선언합니다.
3. 모든 `.html` 의 `<link rel="stylesheet" href="https://cdn.jsdelivr.net/...">` 와 Google Fonts 링크를 지웁니다.
4. `_headers` 의 CSP에서 `cdn.jsdelivr.net`, `fonts.googleapis.com`, `fonts.gstatic.com` 을 제거합니다.

CDN이 막혀도 `Apple SD Gothic Neo` → `맑은 고딕` 순으로 대체되므로 화면이 깨지지는 않습니다.

---

## 7. 배포 전 확인 목록

기획서 07-5의 수용기준(Definition of Done)에 맞춘 점검 항목입니다.

**콘텐츠**
- [ ] `CONTENT-GUIDE.md` 의 "확정 후 공개" 항목을 실제 값으로 교체했습니다
- [ ] 오픈 준비 현황(홈 `#progress`)의 단계별 상태가 실제 진행과 일치합니다 — **AC-01**
- [ ] 상품 가격은 매입 계약·내부 승인이 끝난 값만 게시했습니다 — **AC-02**
- [ ] 푸터의 법인 정보(상호·사업자번호·주소·대표자·통신판매업 신고번호)를 채웠습니다
- [ ] 개인정보처리방침의 보호책임자와 위탁사 정보를 확정했습니다

**기능**
- [ ] 문의 폼 4종이 실제로 접수되고 담당자에게 전달됩니다 — **AC-03**
- [ ] KV 또는 웹훅 바인딩이 Production·Preview 양쪽에 설정되어 있습니다
- [ ] 지점 공지를 수정하면 바로 반영됩니다 — **AC-04**

**품질**
- [ ] 모바일(390px)·태블릿·데스크톱에서 레이아웃이 깨지지 않습니다
- [ ] 키보드 Tab만으로 모든 메뉴와 폼을 조작할 수 있습니다
- [ ] 커스텀 도메인의 canonical·og:url·sitemap 주소가 실제 도메인입니다
- [ ] `_redirects` 에 `/경로 → /경로.html 200` 형태의 규칙이 없습니다 (무한 루프 원인)
- [ ] Google Search Console에 `sitemap.xml` 을 제출했습니다

---

## 8. 브랜치 운영 (기획서 원칙 7·8)

```
main        ← Production 배포. 직접 push 금지
  ↑ PR + 리뷰 승인
feature/*   ← 작업 브랜치. PR 생성 시 Preview URL 자동 발급
```

Cloudflare Pages는 PR마다 Preview URL을 만듭니다.
`Preview → 사람 검수 → main 병합 → Production` 순서를 지켜 주세요.
GitHub 저장소 **Settings → Branches** 에서 `main` 브랜치 보호 규칙(리뷰 1인 이상 필수)을 켜 두시길 권합니다.

---

## 9. 문의

기획·명세 관련 : `HMK 홈페이지/프로그램 통합 제작기획서` 07장
사이트 구조·코드 관련 : 이 저장소의 Issues
