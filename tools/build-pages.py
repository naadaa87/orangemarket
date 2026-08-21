#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
오렌지 마켓 홈페이지 페이지 생성 스크립트

헤더·푸터·메뉴처럼 14개 페이지에 공통으로 들어가는 부분을 한 곳에서 관리합니다.
배포에는 필요하지 않습니다. Cloudflare는 이 파일을 실행하지 않습니다.

사용법:
    cd tools && python3 build-pages.py

수정 지점:
    SITE   도메인 (canonical·og:url·sitemap 에 반영)
    NAV    상단 메뉴 구성
    header() / footer()   모든 페이지 공통 영역
    FAQS   FAQ 목록 (구조화 데이터도 함께 생성)
"""

import os, sys, json

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


SITE = "https://orange-market.pages.dev"   # 실제 도메인 확정 시 이 값만 교체
BRAND = "오렌지 마켓"

NAV = [
    ("brand.html", "브랜드"),
    ("category.html", "상품 카테고리"),
    ("deals.html", "특가·행사"),
    ("stores.html", "지점 안내"),
    ("business.html", "사업자 구매"),
    ("supply.html", "입점·납품"),
    ("faq.html", "고객센터"),
]

LOGO_MARK = """<svg class="logo__mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
<circle cx="32" cy="36" r="24" fill="#FF6A00"/>
<path d="M32 13c0-5.5 4.5-10 10-10 0 5.5-4.5 10-10 10z" fill="#2E9E4F"/>
<rect x="30.3" y="9" width="3.4" height="8" rx="1.7" fill="#8A4B12"/>
<path d="M20 33c2-2 5.2-2 7.2 0M36.8 33c2-2 5.2-2 7.2 0" stroke="#0D1B2A" stroke-width="3.2" stroke-linecap="round" fill="none"/>
<path d="M21.5 43c4.6 4.4 16.4 4.4 21 0" stroke="#0D1B2A" stroke-width="3.4" stroke-linecap="round" fill="none"/>
</svg>"""


def logo(cls="logo", href="index.html"):
    return f"""<a class="{cls}" href="{href}" aria-label="{BRAND} 홈으로">
{LOGO_MARK}
<span class="logo__wm"><b>오렌지 마켓</b><i>ORANGE MARKET</i></span>
</a>"""


def head(title, desc, path, og="og-cover.jpg", extra=""):
    full = f"{title} | {BRAND}" if path != "index.html" else title
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path == 'index.html' else path}">
<meta name="theme-color" content="#FF6A00">
<meta name="format-detection" content="telephone=no">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{'' if path == 'index.html' else path}">
<meta property="og:image" content="{SITE}/assets/img/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/favicon.svg">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{extra}
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
"""


def header(active=""):
    items = "\n".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>'
        for h, t in NAV
    )
    return f"""<div class="topbar">
  <div class="wrap">
    <p><span class="badge badge--orange"><span class="dot"></span>오픈 준비 중</span> <span class="topbar__long">&nbsp;1호점 오픈일은 확정되는 대로 이 곳과 문자로 안내드립니다.</span></p>
    <nav class="topbar__links" aria-label="보조 메뉴">
      <a href="notify.html">오픈 알림</a>
      <a href="membership.html">멤버십</a>
      <a href="faq.html">고객센터</a>
    </nav>
  </div>
</div>

<header class="hd">
  <div class="wrap">
    {logo()}
    <nav class="gnb" aria-label="주 메뉴">
{items}
      <a href="membership.html" class="gnb__extra">멤버십</a>
    </nav>
    <div class="hd__cta">
      <a class="btn btn--primary btn--sm btn--nav" href="notify.html">오픈 알림 신청</a>
      <button class="burger" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="gnb">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
"""


def footer():
    return f"""<footer class="ft">
  <div class="wrap">
    <div class="ft__grid">
      <div>
        <div class="ft__logo">{LOGO_MARK}<span class="logo__wm"><b>오렌지 마켓</b><i>ORANGE MARKET</i></span></div>
        <p class="ft__desc">제조사에서 바로 사고, 박스 단위로 담고, 창고를 그대로 매장으로 씁니다. 아낀 비용은 가격표에 그대로 반영합니다.</p>
        <p class="ft__biz">
          HMK홀딩스그룹 오렌지마켓 사업본부<br>
          상호·사업자등록번호·주소·대표자·통신판매업 신고번호는 법인 등록 완료 후 게재합니다.<br>
          고객센터 대표번호와 운영시간은 1호점 오픈에 맞춰 안내드립니다.
        </p>
      </div>
      <div>
        <h4>브랜드</h4>
        <nav aria-label="브랜드 메뉴">
          <a href="brand.html">브랜드 소개</a>
          <a href="category.html">상품 카테고리</a>
          <a href="deals.html">특가·행사</a>
          <a href="membership.html">멤버십 안내</a>
        </nav>
      </div>
      <div>
        <h4>매장</h4>
        <nav aria-label="매장 메뉴">
          <a href="stores.html">지점 안내</a>
          <a href="store-detail.html">1호점 미리보기</a>
          <a href="notify.html">오픈 알림 신청</a>
        </nav>
      </div>
      <div>
        <h4>비즈니스·고객지원</h4>
        <nav aria-label="비즈니스 메뉴">
          <a href="business.html">대량·사업자 구매</a>
          <a href="supply.html">입점·납품 제안</a>
          <a href="faq.html">자주 묻는 질문</a>
        </nav>
      </div>
    </div>
    <div class="ft__bot">
      <p>&copy; <span data-year>2026</span> HMK Holdings Group. Orange Market. All rights reserved.</p>
      <nav aria-label="약관 메뉴">
        <a href="privacy.html" class="is-strong">개인정보처리방침</a>
        <a href="terms.html">이용약관</a>
      </nav>
    </div>
  </div>
</footer>

<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def jsonld_org():
    return """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"오렌지 마켓","alternateName":"Orange Market",
"url":"%s/","logo":"%s/assets/icons/favicon.svg",
"description":"직매입·대용량·창고형 운영으로 가격을 낮춘 창고형 할인매장. 1호점 오픈 준비 중입니다.",
"parentOrganization":{"@type":"Organization","name":"HMK홀딩스그룹"}}
</script>""" % (SITE, SITE)


def crumb(items):
    """items: [(label, href|None)]"""
    parts = ['<a href="index.html">홈</a>']
    for label, href in items:
        parts.append("<span>/</span>")
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<em>{label}</em>')
    return f'<nav class="crumb" aria-label="현재 위치">{"".join(parts)}</nav>'


def phd(eyebrow, title, lead, crumb_items):
    return f"""<section class="phd">
  <div class="wrap">
    {crumb(crumb_items)}
    <p class="eyebrow mt-16">{eyebrow}</p>
    <h1 class="h1">{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""


def write(path, title, desc, body, active="", extra_head="", og="og-cover.jpg"):
    html = head(title, desc, path, og, extra_head) + header(active) + '<main id="main">\n' + body + "\n</main>\n" + footer()
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(html)
    print("written:", path, len(html), "bytes")



# ======================================================================
# p_home.py 원본 내용
# ======================================================================

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'
DOT = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="12" r="5"/></svg>'

extra = jsonld_org() + """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","name":"오렌지 마켓","url":"%s/",
"inLanguage":"ko","description":"창고형 할인매장 오렌지 마켓. 직매입·대용량·창고형 운영으로 가격을 낮춥니다. 1호점 오픈 준비 중."}
</script>""" % SITE

body = """
<!-- ============ 히어로 ============ -->
<section class="hero">
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <p class="hero__status"><span>초저가! 창고형!</span> <b>1호점 오픈 준비 중</b></p>
        <h1 class="h1">싸게 파는 이유를<br><em>숨기지 않습니다</em></h1>
        <p class="hero__lead">
          오렌지 마켓은 제조사와 산지에서 바로 사고, 낱개 대신 박스와 팔레트 단위로 담습니다.
          창고를 그대로 매장으로 쓰기 때문에 진열비와 보관비가 처음부터 가격에서 빠집니다.
        </p>
        <div class="btn-row hero__cta">
          <a class="btn btn--primary btn--lg" href="notify.html">오픈 알림 신청</a>
          <a class="btn btn--ghost btn--lg" href="stores.html">출점 계획 보기 <span class="arw" aria-hidden="true">&rarr;</span></a>
        </div>
        <p class="hero__note">휴대폰 번호만 남기면 오픈일과 첫 주 특가를 문자로 보내드립니다.</p>
      </div>
      <div class="hero__media">
        <picture>
          <source media="(max-width: 760px)" srcset="/assets/img/storefront-hero-sm.webp">
          <img src="/assets/img/storefront-hero.webp" width="1448" height="1086"
               alt="오렌지 마켓 매장 외관 조감도. 정면에 오렌지 마켓 간판과 신선식품·생활용품·대용량 특가·스마트 쇼핑 안내판이 있습니다." fetchpriority="high" decoding="async">
        </picture>
        <div class="hero__chip">
          <span class="badge badge--wait"><span class="dot"></span>진행 중</span>
          <span><span class="k">현재 단계</span><span class="v">공급사 입점·상품 소싱</span></span>
        </div>
      </div>
    </div>

    <ul class="hero__strip">
      <li class="rv"><p class="n">LOW PRICE</p><p class="t">초저가 보장</p><p class="d">같은 상품, 같은 규격이라면 가격으로 답합니다.</p></li>
      <li class="rv" data-rv-delay="60"><p class="n">BULK VALUE</p><p class="t">대용량 구성</p><p class="d">낱개 대신 박스와 묶음 단위로 담습니다.</p></li>
      <li class="rv" data-rv-delay="120"><p class="n">WAREHOUSE</p><p class="t">창고형 매장</p><p class="d">쌓아 둔 그대로 팝니다. 다시 진열하지 않습니다.</p></li>
      <li class="rv" data-rv-delay="180"><p class="n">SMART</p><p class="t">빠른 계산</p><p class="d">셀프 계산대와 모바일 영수증으로 줄을 줄입니다.</p></li>
    </ul>
  </div>
</section>

<!-- ============ 왜 싼가 ============ -->
<section class="sec">
  <div class="wrap">
    <div class="duo duo--sticky">
      <div class="duo__media rv">
        <img src="/assets/img/aisle-wide.webp" width="1448" height="1086" loading="lazy" decoding="async"
             alt="팔레트째 쌓인 상품과 통로 번호 안내판이 보이는 창고형 매장 내부.">
      </div>
      <div>
        <p class="eyebrow">WHY IT'S CHEAPER</p>
        <h2 class="h2 mt-16 mb-24">가격이 낮은 데는<br>네 가지 이유가 있습니다</h2>
        <p class="lead mb-32">
          싸다는 말만 반복하지 않겠습니다. 어디서 비용을 줄였는지 순서대로 말씀드립니다.
          이 구조가 유지되는 상품만 매장에 들입니다.
        </p>
        <ol class="why">
          <li class="why__item rv"><span class="why__no">01</span>
            <div><h3 class="h3">중간 단계를 줄입니다</h3>
            <p class="small">제조사, 산지, 총판에서 직접 매입합니다. 거치는 손이 줄면 그만큼 원가가 내려갑니다.</p></div></li>
          <li class="why__item rv"><span class="why__no">02</span>
            <div><h3 class="h3">한 번에 크게 삽니다</h3>
            <p class="small">박스·팔레트 단위로 발주해 매입 단가를 낮추고, 소분 포장과 재포장 비용을 없앱니다.</p></div></li>
          <li class="why__item rv"><span class="why__no">03</span>
            <div><h3 class="h3">회전이 느린 상품은 두지 않습니다</h3>
            <p class="small">품목 수를 넓게 벌이는 대신 잘 나가는 규격에 집중합니다. 재고가 오래 서 있으면 그 비용은 결국 가격에 실립니다.</p></div></li>
          <li class="why__item rv"><span class="why__no">04</span>
            <div><h3 class="h3">창고를 그대로 매장으로 씁니다</h3>
            <p class="small">별도 진열 작업과 이중 보관을 하지 않습니다. 매장 운영비를 낮춰 가격표에 반영합니다.</p></div></li>
        </ol>
      </div>
    </div>
  </div>
</section>

<!-- ============ 통로 안내 (시그니처) ============ -->
<section class="sec sec--paper" id="aisle">
  <div class="wrap">
    <div class="sec-head">
      <span class="sign">
        <span class="sign__plate">
          <span class="sign__no">MAP</span>
          <span class="sign__txt"><span class="sign__kr">매장 통로 안내</span><span class="sign__en">Aisle Directory</span></span>
        </span>
      </span>
      <h2 class="h2">다섯 개의 통로로<br>매장을 나눴습니다</h2>
      <p class="lead">천장 안내판의 번호만 따라가면 됩니다. 홈페이지의 카테고리 구성도 실제 매장 통로와 똑같이 맞췄습니다.</p>
    </div>

    <div class="aisle">
      <a class="aisle__it rv" href="category.html#fresh">
        <div class="aisle__hd"><span class="aisle__no">01</span>
          <span><span class="aisle__nm">신선식품</span><br><span class="aisle__en">Fresh Food</span></span></div>
        <div class="aisle__bd"><p>산지 직송 농산물과 정육·수산을 매일 들입니다.</p>
          <ul><li>채소·과일</li><li>정육</li><li>수산</li><li>계란·유제품</li></ul></div>
      </a>
      <a class="aisle__it rv" data-rv-delay="60" href="category.html#bulk">
        <div class="aisle__hd"><span class="aisle__no">02</span>
          <span><span class="aisle__nm">대용량·벌크</span><br><span class="aisle__en">Bulk Deal</span></span></div>
        <div class="aisle__bd"><p>박스와 묶음 단위로 담는 오렌지 마켓의 중심 통로입니다.</p>
          <ul><li>쌀·잡곡</li><li>생수·음료</li><li>라면·면류</li><li>간식 박스</li></ul></div>
      </a>
      <a class="aisle__it rv" data-rv-delay="120" href="category.html#living">
        <div class="aisle__hd"><span class="aisle__no">03</span>
          <span><span class="aisle__nm">생활용품</span><br><span class="aisle__en">Living</span></span></div>
        <div class="aisle__bd"><p>매달 반복해서 사는 소모품을 가장 큰 단위로 모았습니다.</p>
          <ul><li>화장지·물티슈</li><li>세제·섬유유연제</li><li>주방·욕실</li><li>수납·청소</li></ul></div>
      </a>
      <a class="aisle__it rv" data-rv-delay="180" href="category.html#home">
        <div class="aisle__hd"><span class="aisle__no">04</span>
          <span><span class="aisle__nm">가전·리빙</span><br><span class="aisle__en">Home Living</span></span></div>
        <div class="aisle__bd"><p>계절 가전과 조리도구, 침구를 시즌에 맞춰 운영합니다.</p>
          <ul><li>소형가전</li><li>조리도구</li><li>침구·홈데코</li><li>시즌 상품</li></ul></div>
      </a>
      <a class="aisle__it rv" data-rv-delay="240" href="category.html#pb">
        <div class="aisle__hd"><span class="aisle__no">05</span>
          <span><span class="aisle__nm">오렌지 PB</span><br><span class="aisle__en">Orange PB</span></span></div>
        <div class="aisle__bd"><p>같은 품질을 더 낮은 가격에 내놓기 위한 자체 브랜드입니다.</p>
          <ul><li>생수·즉석식품</li><li>쌀·기본 식자재</li><li>화장지·세제</li><li>주방 소모품</li></ul></div>
      </a>
    </div>
    <p class="mt-24"><a class="lnk" href="category.html">통로별 취급 품목 자세히 보기 <span class="arw" aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>

<!-- ============ 가격표 읽는 법 ============ -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">PRICE LABEL</p>
      <h2 class="h2">가격표에 무엇을 적을지<br>먼저 정해 두었습니다</h2>
      <p class="lead">싼 것처럼 보이게 만드는 표기는 쓰지 않습니다. 오렌지 마켓의 모든 가격표에는 아래 다섯 가지가 반드시 들어갑니다.</p>
    </div>

    <div class="pricecard">
      <div class="ptag rv" role="img" aria-label="오렌지 마켓 가격표 표기 예시. 품명, 규격, 판매가, 회원가, 단위가격, 행사 기간이 표시됩니다.">
        <div class="ptag__top"><b>초저가! 창고형!</b><span>ORANGE MARKET</span></div>
        <span class="ptag__watermark">표기 예시</span>
        <div class="ptag__bd">
          <p class="ptag__nm">오렌지 마켓 PB 생수</p>
          <p class="ptag__spec">2L × 6병 / 1박스</p>
          <div class="ptag__main">
            <p class="ptag__price"><b>0,000</b><i>원</i></p>
            <p class="ptag__mem">멤버십 회원가<b>0,000원</b></p>
          </div>
          <p class="ptag__unit"><span>단위가격</span><span>1L당 000원</span></p>
          <p class="ptag__foot"><span>행사 0월 0일 ~ 0월 0일</span><span>1인 0박스 한정</span></p>
        </div>
      </div>

      <ol class="plegend">
        <li class="rv"><span class="n">1</span><div><p class="t">품명과 규격을 같이 적습니다</p>
          <p class="d">몇 개들이인지, 총 용량이 얼마인지를 가격보다 먼저 확인할 수 있게 합니다.</p></div></li>
        <li class="rv"><span class="n">2</span><div><p class="t">판매가는 실제로 계산되는 금액입니다</p>
          <p class="d">조건이 붙은 가격을 크게 쓰고 조건을 작게 쓰는 표기는 하지 않습니다.</p></div></li>
        <li class="rv"><span class="n">3</span><div><p class="t">회원가와 일반가를 나란히 둡니다</p>
          <p class="d">회원가만 크게 보여 주고 일반가를 감추지 않습니다. 두 값을 같은 자리에서 비교하세요.</p></div></li>
        <li class="rv"><span class="n">4</span><div><p class="t">단위가격을 반드시 병기합니다</p>
          <p class="d">100g당·1L당·1개당 가격을 함께 적습니다. 용량이 다른 상품을 비교할 때 이 값이 기준입니다.</p></div></li>
        <li class="rv"><span class="n">5</span><div><p class="t">행사 기간과 한정 수량을 명시합니다</p>
          <p class="d">시작일과 종료일, 1인 구매 한도를 표시합니다. 기간이 끝나면 가격표도 함께 내립니다.</p></div></li>
      </ol>
    </div>

    <div class="note mt-40">
      <strong>오픈 전이라 실제 판매가는 아직 공개하지 않습니다.</strong>
      위 금액은 표기 방식을 보여 주기 위한 예시입니다. 상품별 가격은 매입 계약과 내부 승인이 끝난 뒤,
      오픈일에 맞춰 한 번에 공개합니다.
    </div>
  </div>
</section>

<!-- ============ 매장 미리보기 ============ -->
<section class="sec sec--navy">
  <div class="wrap">
    <div class="sec-head" style="max-width:820px">
      <p class="eyebrow">STORE PREVIEW</p>
      <h2 class="h2">이런 매장을 만들고 있습니다</h2>
      <p class="lead">설계 단계에서 확정한 매장 구성입니다. 시공이 진행되면 실제 촬영 사진으로 교체합니다.</p>
    </div>
    <div class="strip">
      <figure class="rv"><img src="/assets/img/fresh-produce.webp" width="1300" height="975" loading="lazy" decoding="async"
        alt="나무 박스에 담긴 채소와 과일이 늘어선 신선식품 코너."><figcaption>신선식품 — 산지에서 매장까지 하루</figcaption></figure>
      <figure class="rv" data-rv-delay="80"><img src="/assets/img/deal-endcap.webp" width="1300" height="975" loading="lazy" decoding="async"
        alt="통로 끝 특가 매대에 생수와 대용량 상품이 쌓여 있는 모습."><figcaption>초특가 매대 — 통로 끝에서 바로 확인</figcaption></figure>
      <figure class="rv" data-rv-delay="160"><img src="/assets/img/checkout-wide.webp" width="1400" height="1050" loading="lazy" decoding="async"
        alt="셀프 계산대 네 대와 고객센터 데스크가 있는 매장 계산 구역."><figcaption>계산·고객센터 — 셀프 계산대 운영</figcaption></figure>
    </div>
  </div>
</section>

<!-- ============ 오픈 준비 현황 ============ -->
<section class="sec" id="progress">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">OPENING PROGRESS</p>
      <h2 class="h2">지금 어디까지 왔는지<br>그대로 공개합니다</h2>
      <p class="lead">오픈 전이라고 빈 페이지를 두지 않겠습니다. 단계가 바뀔 때마다 이 화면을 갱신합니다.</p>
    </div>

    <ol class="prep">
      <li class="prep__it prep__it--done rv">
        <span class="prep__dot">""" + CHECK + """</span>
        <p class="t">브랜드·매장 콘셉트 확정</p>
        <p class="d">매장 구성, 통로 구획, 가격표 규격, 브랜드 디자인을 확정했습니다.</p>
        <p class="s"><span class="badge badge--go"><span class="dot"></span>완료</span></p>
      </li>
      <li class="prep__it prep__it--now rv" data-rv-delay="60">
        <span class="prep__dot">""" + DOT + """</span>
        <p class="t">출점 후보지 검토</p>
        <p class="d">그룹 보유 공간과 신규 부지를 대상으로 배후 수요와 주차 여건을 검토하고 있습니다.</p>
        <p class="s"><span class="badge badge--wait"><span class="dot"></span>진행 중</span></p>
      </li>
      <li class="prep__it prep__it--now rv" data-rv-delay="120">
        <span class="prep__dot">""" + DOT + """</span>
        <p class="t">공급사 입점·상품 소싱</p>
        <p class="d">카테고리별 공급사 제안을 받고 있습니다. 납품을 원하시면 지금 제안서를 보내 주세요.</p>
        <p class="s"><span class="badge badge--wait"><span class="dot"></span>제안 접수 중</span></p>
      </li>
      <li class="prep__it rv" data-rv-delay="180">
        <span class="prep__dot"></span>
        <p class="t">매장 시공·집기 반입</p>
        <p class="d">랙 설치, 냉장·냉동 설비, 계산 시스템 구축이 이어집니다.</p>
        <p class="s"><span class="badge"><span class="dot"></span>예정</span></p>
      </li>
      <li class="prep__it rv" data-rv-delay="240">
        <span class="prep__dot"></span>
        <p class="t">채용·시범 운영·오픈</p>
        <p class="d">지점 채용과 시범 운영을 마친 뒤 오픈일을 공지합니다.</p>
        <p class="s"><span class="badge"><span class="dot"></span>예정</span></p>
      </li>
    </ol>

    <div class="note note--navy mt-32">
      <strong>오픈일은 아직 확정되지 않았습니다.</strong>
      날짜가 정해지면 이 페이지와 오픈 알림 문자로 가장 먼저 알려드립니다. 확정 전 날짜를 임의로 표기하지 않습니다.
    </div>
  </div>
</section>

<!-- ============ 지점 안내 ============ -->
<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">STORES</p>
      <h2 class="h2">1호점부터 차례로<br>문을 엽니다</h2>
      <p class="lead">HMK홀딩스그룹이 보유·확보한 공간을 기준으로 출점 지역을 검토하고 있습니다. 지점이 확정되면 주소와 운영시간을 이 곳에 게재합니다.</p>
    </div>

    <div class="store rv">
      <div class="store__media">
        <img src="/assets/img/storefront-day.webp" width="1400" height="1050" loading="lazy" decoding="async"
             alt="주간 시간대에 촬영된 오렌지 마켓 매장 외관 조감도.">
      </div>
      <div class="store__bd">
        <div class="store__top">
          <span class="badge badge--navy">1호점</span>
          <span class="badge badge--wait"><span class="dot"></span>오픈 준비 중</span>
        </div>
        <h3 class="h3">오렌지 마켓 1호점</h3>
        <p class="small">창고형 레이아웃, 대형 주차, 카테고리별 통로 구획을 그대로 적용하는 기준 매장입니다.</p>
        <dl>
          <dt>지역</dt><dd>확정 후 공개</dd>
          <dt>오픈일</dt><dd>확정 후 공개</dd>
          <dt>매장 구성</dt><dd>신선식품 · 대용량 · 생활용품 · 가전리빙 · PB</dd>
          <dt>편의시설</dt><dd>주차장 · 셀프 계산대 · 고객센터 · 대형 카트</dd>
        </dl>
        <div class="btn-row mt-24">
          <a class="btn btn--navy btn--sm" href="store-detail.html">매장 구성 미리보기</a>
          <a class="btn btn--ghost btn--sm" href="notify.html">이 지점 오픈 알림 받기</a>
        </div>
      </div>
    </div>
    <p class="mt-24"><a class="lnk" href="stores.html">전체 출점 계획 보기 <span class="arw" aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>

<!-- ============ B2B ============ -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head sec-head--center">
      <p class="eyebrow">FOR BUSINESS</p>
      <h2 class="h2">사업자와 공급사를 위한 창구는<br>지금부터 열려 있습니다</h2>
    </div>
    <div class="split">
      <div class="split__it rv">
        <span class="badge badge--orange">대량 구매</span>
        <h3 class="h3">식당·카페·사무실 대량 구매</h3>
        <p class="small">정기적으로 쓰는 품목은 매장 판매가와 별개로 수량 견적을 드립니다. 세금계산서 발행과 정기 납품 일정 조율이 가능합니다.</p>
        <ul>
          <li>품목·수량 기준 견적 산출</li>
          <li>사업자 확인 후 전용 단가 적용</li>
          <li>매장 픽업 또는 지정일 납품</li>
        </ul>
        <a class="btn btn--navy" href="business.html">견적 문의하기</a>
      </div>
      <div class="split__it rv" data-rv-delay="80">
        <span class="badge badge--orange">입점·납품</span>
        <h3 class="h3">공급사 입점·납품 제안</h3>
        <p class="small">오픈 전 소싱 단계입니다. 상품, 단가, 최소 주문 수량, 인증 서류를 보내 주시면 카테고리 담당 MD가 검토 후 회신드립니다.</p>
        <ul>
          <li>카테고리별 MD 직접 검토</li>
          <li>샘플 제안·시범 입점 협의</li>
          <li>PB 제조 파트너 상시 모집</li>
        </ul>
        <a class="btn btn--navy" href="supply.html">제안서 보내기</a>
      </div>
    </div>
  </div>
</section>

<!-- ============ 오픈 알림 ============ -->
<section class="sec sec--tight sec--paper">
  <div class="wrap">
    <div class="band">
      <div class="band__grid">
        <div>
          <p class="eyebrow">OPENING ALERT</p>
          <h2 class="h2">오픈하는 날,<br>가장 먼저 알려드리겠습니다</h2>
          <p class="lead">관심 지역과 카테고리를 남겨 주시면 오픈일, 첫 주 특가, 사전 멤버십 혜택을 문자로 보내드립니다.</p>
        </div>
        <div>
          <a class="btn btn--primary btn--lg" href="notify.html">오픈 알림 신청하기</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

write("index.html",
      "오렌지 마켓 — 초저가 창고형 할인매장",
      "직매입·대용량·창고형 운영으로 가격을 낮춘 창고형 할인매장 오렌지 마켓. 1호점 오픈 준비 현황, 매장 통로 구성, 가격 표기 원칙, 입점·납품 제안 안내.",
      body, active="", extra_head=extra)



# ======================================================================
# p_pages1.py 원본 내용
# ======================================================================

# ==========================================================
# 브랜드 소개
# ==========================================================
brand = phd("BRAND", "매일 쓰는 것을<br>가장 낮은 가격으로",
            "오렌지 마켓은 창고형 할인매장입니다. 넓은 매장에 상품을 쌓아 두고, 박스 단위로 팔고, 남는 비용을 가격표에서 뺍니다. 브랜드를 만들면서 정한 기준을 그대로 적어 두었습니다.",
            [("브랜드", None)]) + """
<section class="sec">
  <div class="wrap">
    <div class="duo duo--sticky">
      <div class="duo__media duo__media--tall rv">
        <img src="/assets/img/brand-poster.webp" width="900" height="1124" loading="lazy" decoding="async"
             alt="오렌지 마켓 브랜드 포스터. 마스코트 캐릭터와 초저가 창고형 문구가 있습니다.">
      </div>
      <div>
        <p class="eyebrow">WHAT WE ARE</p>
        <h2 class="h2 mt-16 mb-24">창고를 매장으로,<br>매입을 가격으로</h2>
        <p class="lead mb-32">
          창고형 할인매장은 상품을 예쁘게 진열하는 곳이 아닙니다. 팔레트째 들여와 그 자리에서 파는 곳입니다.
          오렌지 마켓은 이 구조를 끝까지 밀고 갑니다. 대신 아낀 비용은 반드시 가격표로 돌려드립니다.
        </p>
        <ul class="chk">
          <li>같은 상품, 같은 규격이면 가격으로 비교당하겠습니다.</li>
          <li>박스와 묶음 단위를 기본 판매 단위로 삼습니다.</li>
          <li>회전이 느린 상품은 품목 수를 늘리기 위해 억지로 두지 않습니다.</li>
          <li>가격표에는 단위가격과 행사 기간을 반드시 적습니다.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">OUR PROMISE</p>
      <h2 class="h2">고객에게 드리는 세 가지 약속</h2>
      <p class="lead">지키지 못할 약속은 처음부터 걸지 않겠습니다. 아래 세 가지는 매장 운영 규칙으로 관리합니다.</p>
    </div>
    <div class="grid g-3">
      <div class="card rv">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
        <h3 class="h3">가격</h3>
        <p class="small">판매가와 회원가를 같은 자리에 표시하고, 단위가격을 함께 적습니다. 조건이 붙은 가격을 대표 가격처럼 쓰지 않습니다.</p>
      </div>
      <div class="card rv" data-rv-delay="70">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 7 12 3 4 7v10l8 4 8-4V7z"/><path d="m4 7 8 4 8-4M12 11v10"/></svg></div>
        <h3 class="h3">품질</h3>
        <p class="small">싸다고 아무거나 들이지 않습니다. 신선식품은 산지와 입고일을 관리하고, 규격과 원산지를 매대에 함께 표시합니다.</p>
      </div>
      <div class="card rv" data-rv-delay="140">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 12l2 2 4-4"/><path d="M12 3l7.5 3.4v5.1c0 4.6-3.1 8.9-7.5 10.5-4.4-1.6-7.5-5.9-7.5-10.5V6.4L12 3z"/></svg></div>
        <h3 class="h3">응대</h3>
        <p class="small">교환·환불 기준을 매장 입구와 홈페이지에 같은 문장으로 붙입니다. 지점에서 처리할 일과 본사가 처리할 일을 나눠 안내합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">HOW IT WORKS</p>
      <h2 class="h2">상품이 매장에 오기까지</h2>
      <p class="lead">오렌지 마켓의 가격은 협상만으로 만들어지지 않습니다. 매입부터 판매까지 네 단계를 같은 기준으로 관리합니다.</p>
    </div>
    <div class="duo">
      <div>
        <ol class="steps">
          <li><div><p class="t">직매입 계약</p><p class="d">제조사·산지·총판과 직접 계약합니다. 카테고리 담당 MD가 단가, 최소 주문 수량, 납품 주기를 한 번에 확정합니다.</p></div></li>
          <li><div><p class="t">대량 발주</p><p class="d">박스·팔레트 단위로 발주해 매입 단가를 낮춥니다. 소분과 재포장을 하지 않아 포장비가 붙지 않습니다.</p></div></li>
          <li><div><p class="t">창고형 적재</p><p class="d">입고한 팔레트를 그대로 매대에 올립니다. 별도 진열 작업이 없으니 인건비와 이중 보관비가 줄어듭니다.</p></div></li>
          <li><div><p class="t">회전 관리</p><p class="d">판매 속도를 매주 확인해 느린 품목은 정리하고 빠른 규격에 집중합니다. 재고가 오래 서 있으면 가격이 올라가기 때문입니다.</p></div></li>
        </ol>
      </div>
      <div class="duo__media rv">
        <img src="/assets/img/delivery-pickup.webp" width="1300" height="975" loading="lazy" decoding="async"
             alt="오렌지 마켓 배송 트럭 앞에 팔레트와 박스가 놓인 물류 하역 구역.">
      </div>
    </div>
  </div>
</section>

<section class="sec sec--navy">
  <div class="wrap">
    <div class="duo">
      <div class="duo__media rv">
        <img src="/assets/img/mascot-cart.webp" width="1171" height="941" loading="lazy" decoding="async"
             alt="카트를 밀고 있는 오렌지 마켓 마스코트 캐릭터와 통로 안내판.">
      </div>
      <div>
        <p class="eyebrow">MASCOT</p>
        <h2 class="h2 mt-16 mb-24">가격을 깎는 얼굴</h2>
        <p class="lead mb-24">
          오렌지 마켓의 마스코트는 웃고 있지만 만만하지 않습니다. 매대 앞에서 값을 한 번 더 따져 보는 표정을 그대로 캐릭터로 만들었습니다.
        </p>
        <p class="lead">
          매장 간판, 통로 안내판, 가격표, 카트, 배송 차량까지 같은 얼굴을 씁니다.
          어느 지점에 가도 같은 방식으로 안내받을 수 있도록 표기 규칙을 통일했습니다.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">BRAND SYSTEM</p>
      <h2 class="h2">브랜드 표기 기준</h2>
      <p class="lead">간판부터 가격표까지 같은 규칙을 씁니다. 협력사 제작물에도 아래 기준을 적용합니다.</p>
    </div>
    <div class="tbl tbl--scroll">
      <table>
        <caption class="sr-only">오렌지 마켓 브랜드 표기 기준</caption>
        <thead><tr><th scope="col">구분</th><th scope="col">기준</th><th scope="col">주로 쓰는 곳</th></tr></thead>
        <tbody>
          <tr><th scope="row">브랜드명</th><td>국문 <b>오렌지 마켓</b> / 영문 <b>ORANGE MARKET</b></td><td>간판, 문서, 온라인 표기</td></tr>
          <tr><th scope="row">슬로건</th><td>초저가! 창고형!</td><td>간판, 전단, 매대 헤더</td></tr>
          <tr><th scope="row">메인 컬러</th><td>오렌지 #FF6A00</td><td>가격, 행사, 버튼, 통로 번호</td></tr>
          <tr><th scope="row">서브 컬러</th><td>딥네이비 #0D1B2A</td><td>제목, 안내판 바탕, 푸터</td></tr>
          <tr><th scope="row">바탕</th><td>화이트 #FFFFFF / 라이트그레이 #F5F5F2</td><td>매장 바닥, 웹 배경, 인쇄물 여백</td></tr>
          <tr><th scope="row">서체</th><td>Pretendard (본문 Regular / 강조 Bold·Black)</td><td>웹, 사이니지, 가격표</td></tr>
          <tr><th scope="row">가격 표기</th><td>판매가 + 회원가 + 단위가격 + 행사 기간</td><td>매대 가격표, 전단, 홈페이지</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note mt-24">
      <strong>오렌지 색은 아껴 씁니다.</strong>
      가격, 행사, 버튼처럼 고객이 판단해야 하는 곳에만 씁니다. 화면 전체를 오렌지로 덮으면 정작 봐야 할 숫자가 묻히기 때문입니다.
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">HMK GROUP</p>
      <h2 class="h2">오렌지 마켓이 서 있는 자리</h2>
      <p class="lead">오렌지 마켓은 HMK홀딩스그룹의 오프라인 유통 채널입니다. 그룹이 확보한 공간과 물류, 매입 조직을 함께 씁니다.</p>
    </div>
    <div class="kv rv">
      <div><p class="k">운영 주체</p><p class="v">HMK<em>홀딩스그룹</em></p><p class="d">오렌지마켓 사업본부가 매입과 매장 운영을 담당합니다.</p></div>
      <div><p class="k">채널 성격</p><p class="v">오프라인<em>창고형</em></p><p class="d">온라인 주문·결제는 그룹 쇼핑몰에서 별도로 운영합니다.</p></div>
      <div><p class="k">상품 관리</p><p class="v">단일 재고<em>원장</em></p><p class="d">매장·라이브·온라인이 같은 상품 코드와 재고를 씁니다.</p></div>
      <div><p class="k">공급망</p><p class="v">직매입<em>중심</em></p><p class="d">통합 매입 조직이 카테고리별 공급사와 직접 계약합니다.</p></div>
    </div>
    <div class="btn-row mt-32">
      <a class="btn btn--navy" href="supply.html">공급사로 참여하기</a>
      <a class="btn btn--ghost" href="stores.html">출점 계획 보기</a>
    </div>
  </div>
</section>
"""

write("brand.html", "브랜드 소개",
      "오렌지 마켓 브랜드 소개. 창고형 할인매장의 운영 방식, 고객에게 드리는 세 가지 약속, 매입부터 판매까지의 네 단계, 브랜드 표기 기준을 안내합니다.",
      brand, active="brand.html")


# ==========================================================
# 상품 카테고리
# ==========================================================
def aisle_block(anchor, no, kr, en, img, alt, desc, rows, tags, rev=False):
    tr = "\n".join(
        f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows
    )
    chips = "".join(f'<li>{t}</li>' for t in tags)
    return f"""
<section class="sec{' sec--paper' if rev else ''}" id="{anchor}">
  <div class="wrap">
    <div class="duo{' duo--rev' if rev else ''}">
      <div class="duo__media rv">
        <img src="/assets/img/{img}" loading="lazy" decoding="async" alt="{alt}">
      </div>
      <div>
        <span class="sign">
          <span class="sign__plate">
            <span class="sign__no">{no}</span>
            <span class="sign__txt"><span class="sign__kr">{kr}</span><span class="sign__en">{en}</span></span>
          </span>
        </span>
        <p class="lead mt-24">{desc}</p>
        <ul class="tagrow">{chips}</ul>
      </div>
    </div>
    <div class="tbl tbl--scroll mt-40">
      <table>
        <caption class="sr-only">{kr} 통로 취급 품목</caption>
        <thead><tr><th scope="col" style="width:22%">품목군</th><th scope="col" style="width:44%">주요 취급 상품</th><th scope="col">판매 단위</th></tr></thead>
        <tbody>{tr}</tbody>
      </table>
    </div>
  </div>
</section>"""


cat = phd("CATEGORY", "다섯 개의 통로,<br>다섯 가지 장보기",
          "홈페이지의 카테고리 구성은 실제 매장 통로와 같습니다. 화면에서 본 순서 그대로 매장에서 찾을 수 있게 맞췄습니다.",
          [("상품 카테고리", None)]) + """
<section class="sec sec--tight">
  <div class="wrap">
    <div class="note">
      <strong>취급 품목은 오픈 전 소싱 결과에 따라 조정됩니다.</strong>
      아래 목록은 카테고리별 기본 구성 계획입니다. 지점별 실제 취급 품목과 판매가는 오픈 시점에 확정해 공개합니다.
    </div>
  </div>
</section>
""" + aisle_block(
    "fresh", "01", "신선식품", "Fresh Food", "fresh-produce.webp",
    "나무 박스에 담긴 채소와 과일이 진열된 신선식품 매대.",
    "매일 들어오고 매일 빠지는 통로입니다. 산지에서 매장까지 거치는 단계를 줄여 신선도와 가격을 동시에 잡습니다. 대용량 팩과 소가족용 규격을 함께 운영합니다.",
    [("채소·과일", "제철 채소, 국내산 과일, 대용량 박스 과일", "낱개 · 박스 · 대용량 팩"),
     ("정육", "국내산 돈육·우육, 수입 육류, 냉동 벌크", "팩 · 벌크 트레이"),
     ("수산", "냉동 수산, 손질 생선, 건해산물", "팩 · 박스"),
     ("계란·유제품", "계란 30구, 우유·요구르트 멀티팩", "판 · 멀티팩")],
    ["채소·과일", "정육", "수산", "계란·유제품", "산지 직송"]
) + aisle_block(
    "bulk", "02", "대용량·벌크", "Bulk Deal", "aisle-wide.webp",
    "팔레트에 쌓인 대용량 상품과 통로 번호 안내판이 보이는 매장 내부.",
    "오렌지 마켓의 중심 통로입니다. 한 번 사면 오래 쓰는 품목을 박스와 묶음 단위로 모았습니다. 같은 상품이라도 단위가격이 가장 낮은 규격을 골라 들입니다.",
    [("쌀·잡곡", "10kg·20kg 포대, 잡곡·현미 대용량", "포대 · 박스"),
     ("생수·음료", "2L 6입, 500mL 20입, 커피·차 멀티팩", "박스 · 팔레트"),
     ("라면·면류", "라면 멀티팩, 컵라면 박스, 건면", "박스"),
     ("간식·즉석식품", "과자 대용량 박스, 즉석밥, 냉동 간편식", "박스 · 멀티팩")],
    ["쌀·잡곡", "생수·음료", "라면·면류", "간식 박스", "즉석식품"], rev=True
) + aisle_block(
    "living", "03", "생활용품", "Living", "checkout-self.webp",
    "매장 계산 구역과 셀프 계산대, 생활용품 안내 사이니지.",
    "매달 반복해서 사는 소모품 통로입니다. 낱개로 사면 비싸지는 품목일수록 큰 단위로 담아 두었습니다. 정기적으로 쓰는 사업장이라면 대량 구매 견적도 함께 이용하실 수 있습니다.",
    [("화장지·물티슈", "3겹 화장지 30롤, 키친타월, 대용량 물티슈", "묶음 · 박스"),
     ("세제·섬유유연제", "액체세제 대용량, 리필, 섬유유연제", "통 · 박스"),
     ("주방·욕실", "위생백, 호일, 수세미, 욕실 소모품", "멀티팩"),
     ("수납·청소", "수납함, 청소도구, 종량제 대응 용품", "낱개 · 세트")],
    ["화장지·물티슈", "세제", "주방", "욕실", "수납·청소"]
) + aisle_block(
    "home", "04", "가전·리빙", "Home Living", "aisle-signage.webp",
    "번호가 붙은 통로 안내판 아래로 상품이 진열된 창고형 매장 통로.",
    "계절과 시즌에 맞춰 운영하는 통로입니다. 상시 품목을 넓게 벌이기보다, 그 시기에 실제로 필요한 상품을 물량으로 확보해 가격을 낮춥니다.",
    [("소형가전", "선풍기, 히터, 주방 소형가전", "낱개"),
     ("조리도구", "냄비·프라이팬 세트, 밀폐용기 대용량", "세트 · 멀티팩"),
     ("침구·홈데코", "이불·베개 세트, 러그, 수납 가구", "세트"),
     ("시즌 상품", "여름 물놀이, 겨울 방한, 명절 선물세트", "낱개 · 세트")],
    ["소형가전", "조리도구", "침구", "홈데코", "시즌 상품"], rev=True
) + aisle_block(
    "pb", "05", "오렌지 PB", "Orange PB", "pb-products.webp",
    "오렌지 마켓 자체 브랜드 쌀, 생수, 화장지, 세제 등 PB 상품 모음.",
    "같은 품질을 더 낮은 가격에 내놓기 위해 만든 자체 브랜드입니다. 브랜드 광고비와 유통 단계를 덜어 낸 만큼 가격을 낮추고, 원산지와 제조사 정보는 포장에 그대로 표기합니다.",
    [("기본 식자재", "PB 쌀, 밀가루, 식용유, 조미료", "포대 · 박스"),
     ("음료·즉석식품", "PB 생수, 즉석밥, 냉동식품", "박스 · 멀티팩"),
     ("생활 소모품", "PB 화장지, 물티슈, 세제", "묶음 · 박스"),
     ("주방 소모품", "PB 위생백, 호일, 키친타월", "멀티팩")],
    ["PB 쌀", "PB 생수", "PB 화장지", "PB 세제", "제조사 표기"]
) + """
<section class="sec sec--paper">
  <div class="wrap">
    <div class="split">
      <div class="split__it rv">
        <span class="badge badge--orange">사업자</span>
        <h3 class="h3">같은 품목을 정기적으로 쓰신다면</h3>
        <p class="small">식당, 카페, 사무실, 기관처럼 반복 구매하는 곳은 품목과 수량 기준으로 별도 견적을 드립니다.</p>
        <a class="btn btn--navy" href="business.html">대량 구매 문의</a>
      </div>
      <div class="split__it rv" data-rv-delay="80">
        <span class="badge badge--orange">공급사</span>
        <h3 class="h3">이 통로에 넣고 싶은 상품이 있다면</h3>
        <p class="small">카테고리별 MD가 직접 검토합니다. 상품 정보와 단가, 최소 주문 수량을 함께 보내 주세요.</p>
        <a class="btn btn--navy" href="supply.html">입점·납품 제안</a>
      </div>
    </div>
  </div>
</section>
"""

write("category.html", "상품 카테고리",
      "오렌지 마켓 상품 카테고리 안내. 신선식품, 대용량·벌크, 생활용품, 가전·리빙, 오렌지 PB 등 다섯 개 통로의 취급 품목과 판매 단위를 정리했습니다.",
      cat, active="category.html")


# ==========================================================
# 특가·행사
# ==========================================================
deals = phd("DEALS", "특가를 언제, 어떻게<br>운영하는지 먼저 공개합니다",
            "오픈 후 진행할 특가 운영 방식입니다. 행사 기간과 한도를 미리 정해 두고, 정해진 기간이 끝나면 가격표도 함께 내립니다.",
            [("특가·행사", None)]) + """
<section class="sec sec--tight">
  <div class="wrap">
    <div class="note">
      <strong>지금은 진행 중인 행사가 없습니다.</strong>
      1호점 오픈에 맞춰 첫 특가가 시작됩니다. 오픈 알림을 신청하시면 행사 시작 전에 문자로 안내드립니다.
      <a class="lnk" href="notify.html" style="margin-left:6px">오픈 알림 신청 <span class="arw" aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">DEAL TYPES</p>
      <h2 class="h2">특가는 세 가지 방식으로 운영합니다</h2>
      <p class="lead">할인 폭이 아니라 운영 방식으로 나눴습니다. 어떤 행사인지 알면 언제 사러 가야 하는지도 분명해집니다.</p>
    </div>
    <div class="grid g-3">
      <div class="card card--pad-0 card--hover rv">
        <div class="card__media"><img src="/assets/img/deal-endcap.webp" loading="lazy" decoding="async" alt="통로 끝 초특가 매대에 대용량 생수가 쌓여 있는 모습."></div>
        <div class="card__body">
          <span class="badge badge--orange">매일</span>
          <h3 class="h3 mt-12">오늘의 초특가</h3>
          <p class="small">하루 단위로 운영하는 한정 수량 행사입니다. 통로 끝 매대에서 바로 확인할 수 있고, 준비된 수량이 소진되면 종료됩니다.</p>
        </div>
      </div>
      <div class="card card--pad-0 card--hover rv" data-rv-delay="70">
        <div class="card__media"><img src="/assets/img/fresh-hall.webp" loading="lazy" decoding="async" alt="넓은 신선식품 매장 통로와 과일·채소 매대."></div>
        <div class="card__body">
          <span class="badge badge--orange">주말</span>
          <h3 class="h3 mt-12">주말 특가</h3>
          <p class="small">금요일부터 일요일까지 이어지는 행사입니다. 신선식품과 장보기 품목 위주로 구성해 주말 한 번에 채울 수 있게 합니다.</p>
        </div>
      </div>
      <div class="card card--pad-0 card--hover rv" data-rv-delay="140">
        <div class="card__media"><img src="/assets/img/aisle-wide.webp" loading="lazy" decoding="async" alt="대용량 상품이 팔레트에 쌓인 벌크 통로."></div>
        <div class="card__body">
          <span class="badge badge--orange">기간</span>
          <h3 class="h3 mt-12">대용량 특가</h3>
          <p class="small">박스·팔레트 단위 상품을 2주 단위로 운영합니다. 단위가격이 가장 크게 내려가는 행사라 사업자 구매와도 함께 안내합니다.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">RULES</p>
      <h2 class="h2">행사 가격을 다루는 규칙</h2>
      <p class="lead">특가는 매장 재량으로 바꾸지 않습니다. 아래 규칙을 시스템에서 그대로 관리합니다.</p>
    </div>
    <ol class="steps">
      <li><div><p class="t">행사 가격은 승인된 값만 게시합니다</p><p class="d">매입 단가와 행사 조건이 내부 승인을 통과한 상품만 가격표와 홈페이지에 올라갑니다. 승인 전 가격은 어디에도 노출되지 않습니다.</p></div></li>
      <li><div><p class="t">시작일과 종료일을 함께 표기합니다</p><p class="d">가격표, 전단, 홈페이지 모두 같은 기간을 표시합니다. 기간이 지나면 게시물이 자동으로 내려가고 정상가로 돌아갑니다.</p></div></li>
      <li><div><p class="t">한정 수량은 숫자로 밝힙니다</p><p class="d">1인 구매 한도와 준비 수량을 표기합니다. 수량이 소진되면 매대와 홈페이지에 품절로 바로 반영합니다.</p></div></li>
      <li><div><p class="t">지점별 차이는 지점 페이지에 적습니다</p><p class="d">행사 품목이나 기간이 지점마다 다를 수 있습니다. 다른 부분은 해당 지점 안내에서 따로 확인하실 수 있게 합니다.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="duo">
      <div class="duo__media rv">
        <img src="/assets/img/banner-navy.webp" width="1600" height="900" loading="lazy" decoding="async"
             alt="초저가 창고형 문구와 장바구니 상품이 담긴 오렌지 마켓 홍보 배너.">
      </div>
      <div>
        <p class="eyebrow">FLYER</p>
        <h2 class="h2 mt-16 mb-24">전단은 오픈에 맞춰<br>내려받으실 수 있습니다</h2>
        <p class="lead mb-24">
          행사 전단은 매장 배포본과 같은 내용을 PDF와 이미지로 올립니다.
          집에서 미리 보고 장보기 목록을 정리하실 수 있게, 행사 시작 하루 전에 게시합니다.
        </p>
        <div class="btn-row">
          <span class="btn" aria-disabled="true">전단 준비 중</span>
          <a class="btn btn--ghost" href="notify.html">전단 알림 받기</a>
        </div>
        <p class="xsmall mt-16">전단이 게시되면 이 자리에 회차별 다운로드 목록이 표시됩니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight sec--paper">
  <div class="wrap">
    <div class="band">
      <div class="band__grid">
        <div>
          <p class="eyebrow">FIRST WEEK</p>
          <h2 class="h2">첫 주 특가는<br>알림 신청자에게 먼저 안내합니다</h2>
          <p class="lead">오픈 첫 주 행사 품목과 기간을 문자로 미리 보내드립니다. 관심 카테고리를 고르면 해당 품목 위주로 안내받으실 수 있습니다.</p>
        </div>
        <div><a class="btn btn--primary btn--lg" href="notify.html">오픈 알림 신청하기</a></div>
      </div>
    </div>
  </div>
</section>
"""

write("deals.html", "특가·행사",
      "오렌지 마켓 특가 운영 안내. 오늘의 초특가, 주말 특가, 대용량 특가 운영 방식과 행사 가격 표기 규칙, 전단 게시 계획을 확인하세요.",
      deals, active="deals.html")



# ======================================================================
# p_pages2.py 원본 내용
# ======================================================================

CONSENT = """
        <div class="consent">
          <p class="consent__hd">개인정보 수집·이용 동의</p>
          <label class="check">
            <input type="checkbox" name="agreePrivacy" value="Y" required>
            <span><b>[필수]</b> 문의 접수와 회신을 위해 이름, 연락처, 문의 내용을 수집합니다. 접수일로부터 1년간 보관 후 파기합니다.
            자세한 내용은 <a href="privacy.html">개인정보처리방침</a>에서 확인하실 수 있습니다.</span>
          </label>
          <label class="check">
            <input type="checkbox" name="agreeMarketing" value="Y">
            <span><b>[선택]</b> 오픈 소식, 특가 안내, 멤버십 혜택을 문자와 이메일로 받겠습니다. 동의하지 않아도 문의 접수에는 영향이 없습니다.</span>
          </label>
          <p class="err"></p>
        </div>
        <div class="form__msg form__msg--ok" role="status">
          <strong>접수되었습니다.</strong>담당자가 확인 후 영업일 기준 3일 이내에 남겨 주신 연락처로 회신드리겠습니다.
        </div>
        <div class="form__msg form__msg--ng" role="alert">
          <strong>접수하지 못했습니다.</strong>잠시 후 다시 시도해 주세요. 계속 실패하면 고객센터 문의 페이지를 이용해 주세요.
        </div>"""

# ==========================================================
# 지점 안내
# ==========================================================
stores = phd("STORES", "1호점부터 차례로<br>문을 엽니다",
             "HMK홀딩스그룹이 보유하거나 새로 확보한 공간을 대상으로 출점 지역을 검토하고 있습니다. 지점이 확정되면 주소, 운영시간, 주차 안내를 이 페이지에 바로 게재합니다.",
             [("지점 안내", None)]) + """
<section class="sec">
  <div class="wrap" data-filter-root>
    <div class="tools">
      <div class="filters" role="group" aria-label="지점 상태 필터">
        <button class="filt" type="button" data-filter="all" aria-pressed="true">전체</button>
        <button class="filt" type="button" data-filter="ready" aria-pressed="false">오픈 준비 중</button>
        <button class="filt" type="button" data-filter="review" aria-pressed="false">검토 중</button>
        <button class="filt" type="button" data-filter="open" aria-pressed="false">영업 중</button>
      </div>
      <p class="small"><b data-count>3</b>개 지점</p>
    </div>

    <div class="grid" style="gap:16px">
      <article class="store rv" data-item data-tags="ready 1호점 수도권">
        <div class="store__media">
          <img src="/assets/img/storefront-hero.webp" loading="lazy" decoding="async" alt="오렌지 마켓 매장 외관 조감도. 정면에 브랜드 간판과 입구가 보입니다.">
        </div>
        <div class="store__bd">
          <div class="store__top">
            <span class="badge badge--navy">1호점</span>
            <span class="badge badge--wait"><span class="dot"></span>오픈 준비 중</span>
          </div>
          <h2 class="h3">오렌지 마켓 1호점</h2>
          <p class="small">창고형 레이아웃, 대형 주차, 통로 구획을 그대로 적용하는 기준 매장입니다. 이후 지점은 이 매장의 운영 결과를 반영해 설계합니다.</p>
          <dl>
            <dt>지역</dt><dd>확정 후 공개</dd>
            <dt>오픈일</dt><dd>확정 후 공개</dd>
            <dt>매장 구성</dt><dd>신선식품 · 대용량 · 생활용품 · 가전리빙 · PB</dd>
            <dt>편의시설</dt><dd>주차장 · 셀프 계산대 · 고객센터 · 대형 카트</dd>
          </dl>
          <div class="btn-row mt-24">
            <a class="btn btn--navy btn--sm" href="store-detail.html">매장 구성 미리보기</a>
            <a class="btn btn--ghost btn--sm" href="notify.html">오픈 알림 받기</a>
          </div>
        </div>
      </article>

      <article class="store rv" data-item data-tags="review 2호점">
        <div class="store__media">
          <div class="store__ph">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>
            <span>부지 검토 중<br>확정 시 사진과 주소를 게재합니다</span>
          </div>
        </div>
        <div class="store__bd">
          <div class="store__top">
            <span class="badge badge--navy">2호점</span>
            <span class="badge"><span class="dot"></span>부지 검토 중</span>
          </div>
          <h2 class="h3">오렌지 마켓 2호점</h2>
          <p class="small">1호점 운영 데이터를 확인한 뒤 출점 시기를 정합니다. 배후 수요, 주차 대수, 진입 동선을 기준으로 후보지를 좁히고 있습니다.</p>
          <dl>
            <dt>지역</dt><dd>검토 중</dd>
            <dt>오픈일</dt><dd>미정</dd>
            <dt>검토 기준</dt><dd>배후 세대수 · 주차 · 물류 접근성</dd>
          </dl>
          <div class="btn-row mt-24">
            <a class="btn btn--ghost btn--sm" href="notify.html">이 지역 오픈 알림 신청</a>
          </div>
        </div>
      </article>

      <article class="store rv" data-item data-tags="review 3호점">
        <div class="store__media">
          <div class="store__ph">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>
            <span>부지 검토 중<br>확정 시 사진과 주소를 게재합니다</span>
          </div>
        </div>
        <div class="store__bd">
          <div class="store__top">
            <span class="badge badge--navy">3호점</span>
            <span class="badge"><span class="dot"></span>검토 예정</span>
          </div>
          <h2 class="h3">오렌지 마켓 3호점</h2>
          <p class="small">그룹이 보유한 공간을 창고형 매장으로 전환하는 방안을 함께 검토합니다. 확정 전 지역명이나 일정은 표기하지 않습니다.</p>
          <dl>
            <dt>지역</dt><dd>검토 예정</dd>
            <dt>오픈일</dt><dd>미정</dd>
            <dt>검토 기준</dt><dd>층고 · 하역 동선 · 임대 조건</dd>
          </dl>
          <div class="btn-row mt-24">
            <a class="btn btn--ghost btn--sm" href="notify.html">이 지역 오픈 알림 신청</a>
          </div>
        </div>
      </article>
    </div>

    <div class="empty">
      <h3 class="h3">해당 상태의 지점이 없습니다</h3>
      <p class="small">다른 필터를 선택하거나 전체 보기로 돌아가 주세요. 새 지점은 확정되는 대로 이 목록에 추가됩니다.</p>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">STANDARD</p>
      <h2 class="h2">모든 지점에 공통으로 넣는 것</h2>
      <p class="lead">지점마다 크기와 층 구성은 달라도, 아래 항목은 어느 매장에서나 같은 방식으로 운영합니다.</p>
    </div>
    <div class="grid g-4">
      <div class="card card--flat rv">
        <div class="ico ico--navy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="9" rx="1.5"/><path d="M5 11V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v4M7 20v1M17 20v1"/></svg></div>
        <h3 class="h4">주차장</h3>
        <p class="small">카트를 그대로 밀고 갈 수 있는 평면 주차를 기본으로 합니다. 주차 대수와 요금은 지점 페이지에 표기합니다.</p>
      </div>
      <div class="card card--flat rv" data-rv-delay="60">
        <div class="ico ico--navy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="16" height="12" rx="1.6"/><path d="M8 20h8M12 16v4"/></svg></div>
        <h3 class="h4">셀프 계산대</h3>
        <p class="small">셀프 계산대와 유인 계산대를 함께 운영합니다. 대량 구매 고객을 위한 전용 라인을 따로 둡니다.</p>
      </div>
      <div class="card card--flat rv" data-rv-delay="120">
        <div class="ico ico--navy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></svg></div>
        <h3 class="h4">고객센터</h3>
        <p class="small">교환·환불, 사업자 구매, 분실물을 한 곳에서 처리합니다. 처리 기준은 매장 입구에도 같은 문장으로 게시합니다.</p>
      </div>
      <div class="card card--flat rv" data-rv-delay="180">
        <div class="ico ico--navy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h2l2.4 10.4a2 2 0 0 0 2 1.6h7.4a2 2 0 0 0 2-1.5L21 9H7"/><circle cx="10" cy="20" r="1.2"/><circle cx="17" cy="20" r="1.2"/></svg></div>
        <h3 class="h4">대형 카트</h3>
        <p class="small">박스와 팔레트 단위 상품을 담을 수 있는 대형 카트와 평판 카트를 함께 비치합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="note note--navy">
      <strong>길찾기와 지도는 지점 확정 후 연결합니다.</strong>
      주소가 확정되면 지도, 대중교통 안내, 주차 진입로 안내를 지점 상세 페이지에 함께 게재합니다.
      지금은 <a href="notify.html" style="text-decoration:underline">오픈 알림</a>을 신청해 두시면 확정 시점에 문자로 안내드립니다.
    </div>
  </div>
</section>
"""

write("stores.html", "지점 안내",
      "오렌지 마켓 지점 안내와 출점 계획. 1호점 오픈 준비 현황과 매장 공통 운영 기준, 주차·계산대·고객센터 안내를 확인하세요.",
      stores, active="stores.html")


# ==========================================================
# 1호점 미리보기
# ==========================================================
detail = phd("STORE 01", "오렌지 마켓 1호점<br>매장 구성 미리보기",
             "설계 단계에서 확정한 1호점 구성입니다. 주소와 운영시간은 확정 후 이 페이지에 바로 반영합니다. 시공이 시작되면 실제 촬영 사진으로 교체합니다.",
             [("지점 안내", "stores.html"), ("1호점", None)]) + """
<section class="sec sec--tight">
  <div class="wrap">
    <div class="kv rv">
      <div><p class="k">상태</p><p class="v" style="font-size:22px;color:var(--wait)">오픈 준비 중</p><p class="d">시공 단계 진입 전, 상품 소싱이 진행 중입니다.</p></div>
      <div><p class="k">지역</p><p class="v" style="font-size:22px">확정 후 공개</p><p class="d">부지 계약과 인허가 완료 시점에 공개합니다.</p></div>
      <div><p class="k">오픈일</p><p class="v" style="font-size:22px">확정 후 공개</p><p class="d">확정 전 예정일을 임의로 표기하지 않습니다.</p></div>
      <div><p class="k">운영시간</p><p class="v" style="font-size:22px">확정 후 공개</p><p class="d">휴무일과 함께 오픈 2주 전 안내드립니다.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">FLOOR GUIDE</p>
      <h2 class="h2">매장 구역 안내</h2>
      <p class="lead">입구에서 계산대까지 한 방향으로 돌 수 있게 통로를 배치했습니다. 번호 순서대로 따라가면 장보기가 끝납니다.</p>
    </div>
    <div class="tbl tbl--scroll">
      <table>
        <caption class="sr-only">1호점 구역별 안내</caption>
        <thead><tr><th scope="col" style="width:12%">통로</th><th scope="col" style="width:22%">구역</th><th scope="col">주요 상품</th><th scope="col" style="width:22%">참고</th></tr></thead>
        <tbody>
          <tr><th scope="row">입구</th><td>카트·안내</td><td>대형 카트, 평판 카트, 매장 안내판, 오늘의 초특가 매대</td><td>입장 시 행사 확인</td></tr>
          <tr><th scope="row">01</th><td>신선식품</td><td>채소·과일, 정육, 수산, 계란·유제품</td><td>냉장·냉동 설비 구역</td></tr>
          <tr><th scope="row">02</th><td>대용량·벌크</td><td>쌀·잡곡, 생수·음료, 라면, 간식 박스</td><td>팔레트 적재 구역</td></tr>
          <tr><th scope="row">03</th><td>생활용품</td><td>화장지, 세제, 주방·욕실, 수납·청소</td><td>대용량 묶음 중심</td></tr>
          <tr><th scope="row">04</th><td>가전·리빙</td><td>소형가전, 조리도구, 침구, 시즌 상품</td><td>시즌별 구성 변경</td></tr>
          <tr><th scope="row">05</th><td>오렌지 PB</td><td>PB 식자재, PB 생수·즉석식품, PB 생활용품</td><td>자체 브랜드 전용</td></tr>
          <tr><th scope="row">출구</th><td>계산·고객센터</td><td>셀프 계산대, 유인 계산대, 대량 구매 전용 라인, 고객센터</td><td>교환·환불 접수</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">INSIDE</p>
      <h2 class="h2">매장 이미지</h2>
      <p class="lead">설계 단계 이미지입니다. 실제 매장과 차이가 있을 수 있으며 시공 후 촬영본으로 교체합니다.</p>
    </div>
    <div class="strip">
      <figure class="rv"><img src="/assets/img/aisle-signage.webp" loading="lazy" decoding="async" alt="통로 번호 안내판이 걸린 매장 통로."><figcaption>통로 안내판</figcaption></figure>
      <figure class="rv" data-rv-delay="70"><img src="/assets/img/fresh-hall.webp" loading="lazy" decoding="async" alt="채소와 과일이 진열된 넓은 신선식품 구역."><figcaption>신선식품 구역</figcaption></figure>
      <figure class="rv" data-rv-delay="140"><img src="/assets/img/customer-center.webp" loading="lazy" decoding="async" alt="계산대와 고객센터 데스크가 있는 매장 출구 구역."><figcaption>계산·고객센터</figcaption></figure>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="duo">
      <div>
        <p class="eyebrow">NOTICE</p>
        <h2 class="h2 mt-16 mb-24">지점 공지</h2>
        <p class="lead mb-24">지점별 공지는 확정되는 대로 이 자리에 시간순으로 쌓입니다. 운영시간 변경, 휴무, 행사 안내가 여기에 올라갑니다.</p>
        <div class="empty is-on" style="text-align:left">
          <h3 class="h4 mb-12">아직 등록된 공지가 없습니다</h3>
          <p class="small">1호점 오픈 일정이 확정되면 첫 공지가 게시됩니다. 오픈 알림을 신청하시면 같은 내용을 문자로도 받아 보실 수 있습니다.</p>
          <a class="btn btn--primary btn--sm mt-16" href="notify.html">오픈 알림 신청</a>
        </div>
      </div>
      <div class="duo__media rv">
        <img src="/assets/img/checkout-wide.webp" loading="lazy" decoding="async" alt="셀프 계산대와 고객센터가 있는 매장 계산 구역 전경.">
      </div>
    </div>
  </div>
</section>
"""

write("store-detail.html", "1호점 미리보기",
      "오렌지 마켓 1호점 매장 구성 미리보기. 통로별 구역 안내, 편의시설, 지점 공지 게시 계획을 확인하세요.",
      detail, active="stores.html")


# ==========================================================
# 대량·사업자 구매
# ==========================================================
business = phd("FOR BUSINESS", "정기적으로 쓰는 품목은<br>수량으로 이야기합시다",
               "식당, 카페, 사무실, 기관처럼 같은 상품을 반복해서 쓰는 곳이라면 매장 판매가와 별도로 수량 기준 견적을 드립니다. 오픈 전에도 문의를 받고 있습니다.",
               [("사업자 구매", None)]) + """
<section class="sec">
  <div class="wrap">
    <div class="grid g-3">
      <div class="card rv">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6"/></svg></div>
        <h2 class="h3">이런 곳이 이용합니다</h2>
        <p class="small">식당·카페·급식소, 사무실·기숙사, 어린이집·학원, 숙박업소, 공사 현장, 지역 소매점처럼 정기 구매 물량이 있는 사업장입니다.</p>
      </div>
      <div class="card rv" data-rv-delay="70">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l2.5 2.5L16 9"/><rect x="4" y="4" width="16" height="16" rx="2"/></svg></div>
        <h2 class="h3">이렇게 도와드립니다</h2>
        <p class="small">품목과 수량을 알려 주시면 전용 단가를 산출합니다. 세금계산서 발행, 정기 납품 일정 조율, 매장 픽업 예약을 함께 안내합니다.</p>
      </div>
      <div class="card rv" data-rv-delay="140">
        <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
        <h2 class="h3">언제부터 가능한가요</h2>
        <p class="small">견적 상담과 사전 등록은 지금부터 가능합니다. 실제 납품과 결제는 1호점 오픈 시점부터 시작합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">PROCESS</p>
      <h2 class="h2">견적부터 납품까지</h2>
    </div>
    <ol class="steps">
      <li><div><p class="t">문의 접수</p><p class="d">아래 양식에 품목, 예상 수량, 사용 주기를 적어 보내 주세요. 상세 목록이 있다면 문의 내용에 함께 적어 주시면 됩니다.</p></div></li>
      <li><div><p class="t">사업자 확인</p><p class="d">담당자가 연락드려 사업자등록증과 담당자 정보를 확인합니다. 확인된 사업장에만 전용 단가를 적용합니다.</p></div></li>
      <li><div><p class="t">견적 회신</p><p class="d">품목별 단가, 최소 주문 수량, 납품 가능 일정을 문서로 보내드립니다. 수량 구간별 단가도 함께 안내합니다.</p></div></li>
      <li><div><p class="t">주문·수령</p><p class="d">매장 픽업 또는 지정일 납품 중 선택하실 수 있습니다. 픽업 시 대량 구매 전용 계산 라인을 이용하시면 됩니다.</p></div></li>
      <li><div><p class="t">정산·증빙</p><p class="d">세금계산서를 발행하고 거래 내역을 정리해 드립니다. 정기 구매 사업장은 월 단위 정산도 협의 가능합니다.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap-sm">
    <div class="sec-head">
      <p class="eyebrow">INQUIRY</p>
      <h2 class="h2">대량 구매 견적 문의</h2>
      <p class="lead">영업일 기준 3일 이내에 담당자가 연락드립니다. 급하신 경우 문의 내용에 희망 연락 시간을 적어 주세요.</p>
    </div>

    <form class="form" data-form="business" aria-label="대량 구매 견적 문의">
      <div class="grid g-2" style="gap:18px">
        <div class="field">
          <label for="b-company">업체명 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="b-company" name="company" type="text" required autocomplete="organization" placeholder="예) 오렌지식당">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="b-name">담당자 이름 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="b-name" name="name" type="text" required autocomplete="name" placeholder="예) 김담당">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="b-phone">연락처 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="b-phone" name="phone" type="tel" required autocomplete="tel" inputmode="numeric" placeholder="010-0000-0000">
          <p class="hint">숫자만 입력하셔도 됩니다.</p>
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="b-email">이메일</label>
          <input class="inp" id="b-email" name="email" type="email" autocomplete="email" placeholder="name@company.com">
          <p class="hint">견적서를 메일로 받으실 분만 입력하세요.</p>
          <p class="err"></p>
        </div>
      </div>

      <div class="field">
        <label for="b-biztype">업종 <span class="req" aria-hidden="true">*</span></label>
        <select class="sel" id="b-biztype" name="biztype" required>
          <option value="">선택해 주세요</option>
          <option>식당·카페·급식</option>
          <option>사무실·기업</option>
          <option>학교·학원·어린이집</option>
          <option>숙박·펜션</option>
          <option>소매점·편의점</option>
          <option>공사현장·기타</option>
        </select>
        <p class="err"></p>
      </div>

      <fieldset class="fieldset">
        <legend>관심 카테고리 <span class="hint" style="font-weight:400">(여러 개 선택 가능)</span></legend>
        <div class="chips">
          <label class="chip"><input type="checkbox" name="category" value="신선식품"><span>신선식품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="대용량·벌크"><span>대용량·벌크</span></label>
          <label class="chip"><input type="checkbox" name="category" value="생활용품"><span>생활용품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="가전·리빙"><span>가전·리빙</span></label>
          <label class="chip"><input type="checkbox" name="category" value="오렌지 PB"><span>오렌지 PB</span></label>
        </div>
      </fieldset>

      <div class="field">
        <label for="b-message">필요 품목과 수량 <span class="req" aria-hidden="true">*</span></label>
        <textarea class="txt" id="b-message" name="message" required placeholder="예) 생수 2L 6입 주 20박스, 종이컵 1000개들이 월 5박스, 화장지 30롤 월 10묶음"></textarea>
        <p class="hint">품목, 규격, 수량, 사용 주기를 적어 주시면 더 정확한 견적을 드릴 수 있습니다.</p>
        <p class="err"></p>
      </div>
""" + CONSENT + """
      <button class="btn btn--primary btn--lg" type="submit">견적 문의 보내기</button>
    </form>
  </div>
</section>
"""

write("business.html", "대량·사업자 구매",
      "오렌지 마켓 대량·사업자 구매 안내. 식당, 카페, 사무실, 기관을 위한 수량 기준 견적과 세금계산서 발행, 정기 납품 절차를 안내합니다.",
      business, active="business.html")


# ==========================================================
# 입점·납품
# ==========================================================
supply = phd("SUPPLY", "지금은 상품을<br>고르고 있는 단계입니다",
             "오픈 전 소싱이 한창입니다. 오렌지 마켓 통로에 올릴 만한 상품이 있다면 지금이 가장 좋은 시점입니다. 카테고리 담당 MD가 직접 검토하고 회신드립니다.",
             [("입점·납품", None)]) + """
<section class="sec">
  <div class="wrap">
    <div class="duo duo--sticky">
      <div class="duo__media rv">
        <img src="/assets/img/pb-products.webp" loading="lazy" decoding="async" alt="오렌지 마켓 자체 브랜드 상품 진열 이미지.">
      </div>
      <div>
        <p class="eyebrow">WHAT WE LOOK FOR</p>
        <h2 class="h2 mt-16 mb-24">이런 제안을 기다립니다</h2>
        <ul class="chk mb-32">
          <li>박스·팔레트 단위로 안정적으로 공급할 수 있는 상품</li>
          <li>같은 규격 기준으로 단위가격 경쟁력이 있는 상품</li>
          <li>회전이 빠른 생필품, 식자재, 대용량 소모품</li>
          <li>오렌지 PB로 함께 개발할 수 있는 제조 역량</li>
          <li>시즌·행사에 물량을 맞출 수 있는 공급 계획</li>
        </ul>
        <h3 class="h3 mb-12">이런 경우는 검토가 어렵습니다</h3>
        <p class="small">최소 주문 수량을 맞추기 어려운 소량 생산, 단가가 시장 대비 높은 상품, 필수 인증이나 원산지 증빙이 준비되지 않은 상품은 이번 소싱에서 제외됩니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">PROCESS</p>
      <h2 class="h2">제안부터 입점까지 다섯 단계</h2>
      <p class="lead">각 단계의 결과는 남겨 주신 연락처로 회신드립니다. 검토 결과가 부정적인 경우에도 사유를 함께 알려드립니다.</p>
    </div>
    <ol class="steps">
      <li><div><p class="t">제안 접수</p><p class="d">아래 양식으로 회사, 상품, 단가, 최소 주문 수량, 인증 보유 여부를 보내 주세요. 상세 자료는 이메일로 이어서 받습니다.</p></div></li>
      <li><div><p class="t">1차 검토</p><p class="d">카테고리 담당 MD가 상품성, 단가, 공급 안정성을 확인합니다. 영업일 기준 7일 이내에 1차 결과를 회신드립니다.</p></div></li>
      <li><div><p class="t">샘플·서류 확인</p><p class="d">샘플과 함께 사업자등록증, 품질 인증, 원산지 증빙, 보험 가입 여부를 확인합니다.</p></div></li>
      <li><div><p class="t">조건 협의</p><p class="d">단가, 납품 주기, 정산 조건, 반품 기준을 협의합니다. 행사 참여 여부도 이 단계에서 함께 정합니다.</p></div></li>
      <li><div><p class="t">계약·입점</p><p class="d">계약 체결 후 상품 코드와 발주 일정을 등록합니다. 오픈 전 계약 건은 오픈 초도 물량부터 반영됩니다.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">DOCUMENTS</p>
      <h2 class="h2">준비해 주실 서류</h2>
      <p class="lead">제안 단계에서는 아래 항목을 확인만 하고, 실제 서류는 조건 협의 단계에서 요청드립니다.</p>
    </div>
    <div class="tbl tbl--scroll">
      <table>
        <caption class="sr-only">입점 시 필요 서류</caption>
        <thead><tr><th scope="col" style="width:26%">구분</th><th scope="col" style="width:16%">필수 여부</th><th scope="col">내용</th></tr></thead>
        <tbody>
          <tr><th scope="row">사업자등록증</th><td>필수</td><td>법인 또는 개인사업자 등록증 사본</td></tr>
          <tr><th scope="row">상품 제안서</th><td>필수</td><td>상품명, 규격, 이미지, 공급 단가, 최소 주문 수량, 리드타임</td></tr>
          <tr><th scope="row">품질·안전 인증</th><td>품목별</td><td>식품 관련 인증, 전기용품 안전 확인, KC 인증 등 해당 품목의 법정 인증</td></tr>
          <tr><th scope="row">원산지·성분 자료</th><td>품목별</td><td>식품·농축수산물의 원산지, 성분표, 유통기한 기준</td></tr>
          <tr><th scope="row">생산·공급 계획</th><td>권장</td><td>월 공급 가능 수량, 성수기 대응 계획, 물류 조건</td></tr>
          <tr><th scope="row">거래 실적</th><td>권장</td><td>주요 납품처, 거래 기간(공개 가능한 범위 내)</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap wrap-sm">
    <div class="sec-head">
      <p class="eyebrow">PROPOSAL</p>
      <h2 class="h2">입점·납품 제안서 보내기</h2>
      <p class="lead">접수된 제안은 카테고리 담당 MD에게 바로 배정됩니다. 영업일 기준 7일 이내에 1차 검토 결과를 회신드립니다.</p>
    </div>

    <form class="form" data-form="supply" aria-label="입점·납품 제안">
      <div class="grid g-2" style="gap:18px">
        <div class="field">
          <label for="s-company">회사명 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="s-company" name="company" type="text" required autocomplete="organization" placeholder="예) 오렌지식품">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="s-name">담당자 이름 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="s-name" name="name" type="text" required autocomplete="name" placeholder="예) 김담당">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="s-phone">연락처 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="s-phone" name="phone" type="tel" required autocomplete="tel" inputmode="numeric" placeholder="010-0000-0000">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="s-email">이메일 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="s-email" name="email" type="email" required autocomplete="email" placeholder="name@company.com">
          <p class="hint">상세 자료와 검토 결과를 이 주소로 보내드립니다.</p>
          <p class="err"></p>
        </div>
      </div>

      <fieldset class="fieldset">
        <legend>제안 카테고리 <span class="req" aria-hidden="true">*</span></legend>
        <div class="chips">
          <label class="chip"><input type="checkbox" name="category" value="신선식품"><span>신선식품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="대용량·벌크"><span>대용량·벌크</span></label>
          <label class="chip"><input type="checkbox" name="category" value="생활용품"><span>생활용품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="가전·리빙"><span>가전·리빙</span></label>
          <label class="chip"><input type="checkbox" name="category" value="PB 제조"><span>PB 제조</span></label>
        </div>
      </fieldset>

      <div class="field">
        <label for="s-item">제안 품목 <span class="req" aria-hidden="true">*</span></label>
        <input class="inp" id="s-item" name="item" type="text" required placeholder="예) 생수 2L 6입 / 3겹 화장지 30롤">
        <p class="err"></p>
      </div>

      <div class="grid g-2" style="gap:18px">
        <div class="field">
          <label for="s-price">공급 희망 단가</label>
          <input class="inp" id="s-price" name="price" type="text" placeholder="예) 박스당 0,000원">
        </div>
        <div class="field">
          <label for="s-moq">최소 주문 수량(MOQ)</label>
          <input class="inp" id="s-moq" name="moq" type="text" placeholder="예) 100박스 / 1팔레트">
        </div>
      </div>

      <fieldset class="fieldset">
        <legend>준비된 항목 <span class="hint" style="font-weight:400">(해당하는 항목을 모두 선택해 주세요)</span></legend>
        <div class="chips">
          <label class="chip"><input type="checkbox" name="ready" value="사업자등록증"><span>사업자등록증</span></label>
          <label class="chip"><input type="checkbox" name="ready" value="품질·안전 인증"><span>품질·안전 인증</span></label>
          <label class="chip"><input type="checkbox" name="ready" value="원산지·성분 자료"><span>원산지·성분 자료</span></label>
          <label class="chip"><input type="checkbox" name="ready" value="샘플 제공 가능"><span>샘플 제공 가능</span></label>
        </div>
      </fieldset>

      <div class="field">
        <label for="s-message">제안 내용 <span class="req" aria-hidden="true">*</span></label>
        <textarea class="txt" id="s-message" name="message" required placeholder="상품 특징, 생산 능력, 납품 가능 지역, 기존 거래처 등 참고할 내용을 적어 주세요."></textarea>
        <p class="err"></p>
      </div>
""" + CONSENT + """
      <button class="btn btn--primary btn--lg" type="submit">제안서 보내기</button>
    </form>
  </div>
</section>
"""

write("supply.html", "입점·납품 제안",
      "오렌지 마켓 입점·납품 제안 안내. 소싱 기준, 제안부터 입점까지 다섯 단계, 필요 서류와 제안서 접수 양식을 확인하세요.",
      supply, active="supply.html")



# ======================================================================
# p_pages3.py 원본 내용
# ======================================================================

# ==========================================================
# 멤버십 안내
# ==========================================================
mem = phd("MEMBERSHIP", "멤버십은 오픈에 맞춰<br>함께 시작합니다",
          "회원가와 일반가를 나란히 표시하는 것이 오렌지 마켓의 기본 원칙입니다. 멤버십은 그 회원가를 받기 위한 최소한의 장치로만 운영합니다.",
          [("멤버십 안내", None)]) + """
<section class="sec sec--tight">
  <div class="wrap">
    <div class="note">
      <strong>혜택과 가입 조건은 아직 확정 전입니다.</strong>
      아래 내용은 현재 준비 중인 방향이며, 최종 정책은 1호점 오픈 전에 이 페이지에 확정 고지합니다.
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="duo duo--sticky">
      <div class="duo__media duo__media--tall rv">
        <img src="/assets/img/membership-app.webp" loading="lazy" decoding="async"
             alt="오렌지 마켓 멤버십 앱 화면과 모바일 회원 바코드 이미지.">
      </div>
      <div>
        <p class="eyebrow">PLANNED BENEFITS</p>
        <h2 class="h2 mt-16 mb-24">준비 중인 혜택</h2>
        <div class="grid" style="gap:16px">
          <div class="card card--flat rv">
            <h3 class="h4">회원가 적용</h3>
            <p class="small">가격표에 표시된 회원가로 계산됩니다. 별도 쿠폰을 찾아 붙일 필요 없이 계산 시 자동 적용되는 방식으로 준비하고 있습니다.</p>
          </div>
          <div class="card card--flat rv" data-rv-delay="60">
            <h3 class="h4">모바일 영수증</h3>
            <p class="small">종이 영수증 없이 구매 내역을 앱에서 확인합니다. 교환·환불 시 영수증을 찾지 않아도 되도록 연결합니다.</p>
          </div>
          <div class="card card--flat rv" data-rv-delay="120">
            <h3 class="h4">재구매 목록</h3>
            <p class="small">자주 사는 품목을 목록으로 저장해 두고 매장에서 바로 확인할 수 있게 합니다. 재고 상태도 함께 표시할 계획입니다.</p>
          </div>
          <div class="card card--flat rv" data-rv-delay="180">
            <h3 class="h4">행사 사전 안내</h3>
            <p class="small">관심 카테고리로 등록한 행사는 시작 전에 먼저 알려드립니다. 알림 항목은 직접 켜고 끌 수 있게 합니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">WHAT WE WON'T DO</p>
      <h2 class="h2">멤버십에서 하지 않을 것</h2>
      <p class="lead">혜택을 늘리기 위해 가격 구조를 복잡하게 만들지 않겠습니다. 아래 세 가지는 정책에서 제외합니다.</p>
    </div>
    <div class="grid g-3">
      <div class="card rv">
        <h3 class="h4">일반가를 감추지 않습니다</h3>
        <p class="small">회원가만 크게 쓰고 일반가를 지우는 표기는 하지 않습니다. 두 가격을 항상 같은 자리에 나란히 둡니다.</p>
      </div>
      <div class="card rv" data-rv-delay="70">
        <h3 class="h4">등급을 잘게 나누지 않습니다</h3>
        <p class="small">등급이 많아질수록 계산이 어려워집니다. 누구나 같은 조건에서 같은 회원가를 받는 구조를 우선 검토하고 있습니다.</p>
      </div>
      <div class="card rv" data-rv-delay="140">
        <h3 class="h4">쓰지 않을 정보는 받지 않습니다</h3>
        <p class="small">가입에 필요한 최소한의 정보만 수집합니다. 마케팅 수신 동의는 가입과 분리해 언제든 해제하실 수 있게 합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="band">
      <div class="band__grid">
        <div>
          <p class="eyebrow">PRE-REGISTER</p>
          <h2 class="h2">사전 등록해 두시면<br>가입 절차를 줄여 드립니다</h2>
          <p class="lead">오픈 알림을 신청하시면 멤버십 정책이 확정되는 대로 가장 먼저 안내드립니다. 사전 등록자에게는 오픈 첫 주 혜택을 함께 안내할 예정입니다.</p>
        </div>
        <div><a class="btn btn--primary btn--lg" href="notify.html">사전 등록하기</a></div>
      </div>
    </div>
  </div>
</section>
"""

write("membership.html", "멤버십 안내",
      "오렌지 마켓 멤버십 안내. 회원가 자동 적용, 모바일 영수증, 재구매 목록 등 준비 중인 혜택과 정책 방향을 확인하세요.",
      mem, active="")


# ==========================================================
# FAQ
# ==========================================================
FAQS = [
    ("이용", "오렌지 마켓은 언제 문을 여나요?",
     "1호점은 현재 오픈 준비 중이며 정확한 오픈일은 아직 확정되지 않았습니다. 확정 전 예정일을 임의로 안내드리지 않습니다. 오픈 알림을 신청해 두시면 날짜가 정해지는 즉시 문자로 안내드립니다."),
    ("이용", "회원이 아니어도 이용할 수 있나요?",
     "네, 회원 가입 없이 누구나 이용하실 수 있습니다. 다만 가격표에 표시된 회원가는 멤버십 가입 고객에게 적용됩니다. 일반가와 회원가는 항상 같은 가격표에 나란히 표시됩니다."),
    ("이용", "창고형 매장이면 낱개로는 못 사나요?",
     "대용량과 벌크 통로는 박스·묶음 단위가 기본이지만, 신선식품과 생활용품 일부는 낱개 규격도 함께 운영합니다. 통로마다 판매 단위가 다르니 가격표의 규격 표기를 확인해 주세요."),
    ("가격", "가격은 지점마다 다른가요?",
     "기본 판매가는 동일하게 운영합니다. 다만 행사 품목과 기간은 지점 재고 사정에 따라 달라질 수 있습니다. 지점별로 다른 부분은 해당 지점 안내 페이지에 따로 표기합니다."),
    ("가격", "단위가격은 왜 표시하나요?",
     "용량이 다른 상품을 비교하려면 총액만으로는 판단이 어렵습니다. 100g당, 1L당, 1개당 가격을 함께 적어 두면 어느 쪽이 실제로 저렴한지 바로 확인하실 수 있습니다. 오렌지 마켓의 모든 가격표에는 단위가격이 들어갑니다."),
    ("가격", "행사가 끝나면 가격은 어떻게 되나요?",
     "행사 종료일이 지나면 가격표가 내려가고 정상가로 돌아갑니다. 시작일과 종료일은 가격표, 전단, 홈페이지에 같은 기준으로 표시합니다."),
    ("결제", "어떤 결제 수단을 쓸 수 있나요?",
     "신용·체크카드, 간편결제, 현금 결제를 준비하고 있습니다. 사용 가능한 수단은 오픈 전 이 페이지와 매장 입구 안내에 확정 고지합니다."),
    ("결제", "세금계산서를 받을 수 있나요?",
     "사업자 구매의 경우 세금계산서를 발행해 드립니다. 사전에 사업자 확인 절차가 필요하니 대량·사업자 구매 페이지에서 먼저 문의해 주세요."),
    ("교환·환불", "교환과 환불은 어떻게 하나요?",
     "구매하신 지점의 고객센터에서 접수합니다. 영수증 또는 멤버십 구매 내역으로 확인이 가능합니다. 신선식품과 냉장·냉동 상품은 상품 특성상 별도 기준이 적용되며, 세부 기준은 오픈 전 이 페이지와 매장 안내판에 같은 문장으로 게시합니다."),
    ("교환·환불", "구매한 지점이 아닌 다른 지점에서도 처리되나요?",
     "가능한 범위에서 처리해 드리되, 지점 재고와 결제 방식에 따라 구매 지점에서만 처리 가능한 경우가 있습니다. 방문 전 해당 지점 고객센터로 확인해 주시면 정확합니다."),
    ("매장", "주차는 얼마나 되나요?",
     "카트를 그대로 밀고 이동할 수 있는 평면 주차를 기본으로 계획하고 있습니다. 지점별 주차 대수와 요금 정책은 지점 확정 후 해당 지점 페이지에 게재합니다."),
    ("매장", "카트는 어떤 종류가 있나요?",
     "박스와 대용량 상품을 담을 수 있는 대형 카트와, 팔레트 단위 상품을 옮길 수 있는 평판 카트를 함께 비치합니다."),
    ("매장", "매장에서 산 상품을 배송받을 수 있나요?",
     "대량 구매 고객을 대상으로 지정일 납품을 협의해 드립니다. 일반 고객 대상 배송 서비스는 오픈 이후 운영 상황을 보고 검토할 예정입니다."),
    ("사업자", "사업자 대량 구매는 어떻게 신청하나요?",
     "대량·사업자 구매 페이지의 문의 양식으로 품목과 수량을 보내 주시면 담당자가 사업자 확인 후 전용 단가를 산출해 회신드립니다. 오픈 전에도 상담과 사전 등록이 가능합니다."),
    ("사업자", "상품을 납품하고 싶습니다. 어디로 연락하면 되나요?",
     "입점·납품 페이지의 제안 양식을 이용해 주세요. 카테고리별 담당 MD에게 바로 배정되며 영업일 기준 7일 이내에 1차 검토 결과를 회신드립니다."),
    ("문의", "문의는 어디로 하면 되나요?",
     "지점 운영, 상품 재고, 교환·환불처럼 매장에서 처리할 일은 해당 지점 고객센터에서 접수합니다. 입점·납품, 대량 구매, 제휴처럼 본사에서 처리할 일은 각 페이지의 문의 양식을 이용해 주세요. 지점 대표번호는 오픈에 맞춰 안내드립니다."),
]

CATS = ["이용", "가격", "결제", "교환·환불", "매장", "사업자", "문의"]


def faq_items():
    out = []
    for cat, q, a in FAQS:
        tag = cat.replace("·", "")
        out.append(f"""      <div class="acc__it" data-item data-tags="{tag} {cat}">
        <h3><button class="acc__q" type="button"><span class="acc__cat">{cat}</span>{q}</button></h3>
        <div class="acc__a"><p>{a}</p></div>
      </div>""")
    return "\n".join(out)


def faq_ld():
    import json
    items = [{"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in FAQS]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


filt_btns = '\n'.join(
    f'<button class="filt" type="button" data-filter="{c.replace("·","")}" aria-pressed="false">{c}</button>' for c in CATS)

faq = phd("SUPPORT", "자주 묻는 질문",
          "오픈 전에 가장 많이 받는 질문을 모았습니다. 찾으시는 답이 없다면 아래 문의 창구를 이용해 주세요.",
          [("고객센터", None)]) + """
<section class="sec">
  <div class="wrap" data-filter-root>
    <div class="tools">
      <div class="filters" role="group" aria-label="질문 분류 필터">
        <button class="filt" type="button" data-filter="all" aria-pressed="true">전체</button>
""" + filt_btns + """
      </div>
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <label class="sr-only" for="faq-q">질문 검색</label>
        <input class="inp" id="faq-q" type="search" data-search placeholder="궁금한 단어로 찾아보세요">
      </div>
    </div>

    <p class="small mb-24"><b data-count>16</b>개 질문</p>

    <div class="acc" data-single>
""" + faq_items() + """
    </div>

    <div class="empty">
      <h3 class="h3">검색 결과가 없습니다</h3>
      <p class="small">다른 단어로 다시 찾아보시거나, 아래 문의 창구로 직접 물어봐 주세요.</p>
      <a class="btn btn--primary btn--sm mt-16" href="notify.html#contact">문의하기</a>
    </div>
  </div>
</section>

<section class="sec sec--paper">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">CONTACT</p>
      <h2 class="h2">어디로 문의해야 할지 헷갈리신다면</h2>
      <p class="lead">문의 내용에 따라 처리하는 곳이 다릅니다. 아래 기준으로 골라 주시면 회신이 훨씬 빨라집니다.</p>
    </div>
    <div class="tbl tbl--scroll">
      <table>
        <caption class="sr-only">문의 유형별 접수 창구</caption>
        <thead><tr><th scope="col" style="width:24%">문의 내용</th><th scope="col" style="width:20%">처리 창구</th><th scope="col">접수 방법</th></tr></thead>
        <tbody>
          <tr><th scope="row">교환·환불, 분실물, 매장 이용</th><td>구매 지점 고객센터</td><td>지점 방문 또는 지점 대표번호 (오픈 시 안내)</td></tr>
          <tr><th scope="row">상품 재고, 행사 품목</th><td>해당 지점</td><td>지점 안내 페이지의 지점 정보 (오픈 시 게재)</td></tr>
          <tr><th scope="row">대량 구매, 세금계산서</th><td>본사 영업 담당</td><td><a class="lnk" href="business.html">대량·사업자 구매 문의</a></td></tr>
          <tr><th scope="row">입점·납품, PB 제조</th><td>본사 카테고리 MD</td><td><a class="lnk" href="supply.html">입점·납품 제안</a></td></tr>
          <tr><th scope="row">오픈 일정, 신규 지점</th><td>본사 마케팅</td><td><a class="lnk" href="notify.html">오픈 알림·문의</a></td></tr>
          <tr><th scope="row">개인정보 열람·정정·삭제</th><td>개인정보 보호책임자</td><td><a class="lnk" href="privacy.html">개인정보처리방침</a></td></tr>
        </tbody>
      </table>
    </div>
    <div class="note mt-24">
      <strong>지점 대표번호와 고객센터 운영시간은 1호점 오픈에 맞춰 게재합니다.</strong>
      그 전까지는 홈페이지 문의 양식으로 접수해 주시면 담당자가 영업일 기준 3일 이내에 회신드립니다.
    </div>
  </div>
</section>
"""

write("faq.html", "자주 묻는 질문",
      "오렌지 마켓 고객센터. 이용, 가격, 결제, 교환·환불, 매장, 사업자 구매에 대한 자주 묻는 질문과 문의 유형별 접수 창구를 안내합니다.",
      faq, active="faq.html", extra_head=faq_ld())


# ==========================================================
# 오픈 알림 · 문의
# ==========================================================
notify = phd("OPENING ALERT", "오픈하는 날,<br>가장 먼저 알려드리겠습니다",
             "관심 지역과 카테고리를 남겨 주시면 오픈일, 첫 주 특가, 멤버십 사전 등록 안내를 문자로 보내드립니다. 휴대폰 번호 하나면 신청이 끝납니다.",
             [("오픈 알림·문의", None)]) + """
<section class="sec">
  <div class="wrap wrap-sm">
    <form class="form" data-form="notify" aria-label="오픈 알림 신청">
      <div class="grid g-2" style="gap:18px">
        <div class="field">
          <label for="n-name">이름 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="n-name" name="name" type="text" required autocomplete="name" placeholder="예) 김오렌">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="n-phone">휴대폰 번호 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="n-phone" name="phone" type="tel" required autocomplete="tel" inputmode="numeric" placeholder="010-0000-0000">
          <p class="hint">오픈 안내 문자를 받으실 번호입니다.</p>
          <p class="err"></p>
        </div>
      </div>

      <div class="field">
        <label for="n-email">이메일</label>
        <input class="inp" id="n-email" name="email" type="email" autocomplete="email" placeholder="name@example.com">
        <p class="hint">전단과 행사 안내를 메일로도 받으실 분만 입력하세요.</p>
        <p class="err"></p>
      </div>

      <div class="field">
        <label for="n-region">관심 지역 <span class="req" aria-hidden="true">*</span></label>
        <input class="inp" id="n-region" name="region" type="text" required placeholder="예) 경기 남부 / 서울 동부 / 시·군·구 단위">
        <p class="hint">사시는 곳이나 자주 가시는 지역을 적어 주세요. 가까운 지점이 정해지면 그 지점 소식을 우선 보내드립니다.</p>
        <p class="err"></p>
      </div>

      <fieldset class="fieldset">
        <legend>관심 카테고리 <span class="hint" style="font-weight:400">(여러 개 선택 가능)</span></legend>
        <div class="chips">
          <label class="chip"><input type="checkbox" name="category" value="신선식품"><span>신선식품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="대용량·벌크"><span>대용량·벌크</span></label>
          <label class="chip"><input type="checkbox" name="category" value="생활용품"><span>생활용품</span></label>
          <label class="chip"><input type="checkbox" name="category" value="가전·리빙"><span>가전·리빙</span></label>
          <label class="chip"><input type="checkbox" name="category" value="오렌지 PB"><span>오렌지 PB</span></label>
          <label class="chip"><input type="checkbox" name="category" value="사업자 대량구매"><span>사업자 대량구매</span></label>
        </div>
      </fieldset>

      <div class="consent">
        <p class="consent__hd">개인정보 수집·이용 동의</p>
        <label class="check">
          <input type="checkbox" name="agreePrivacy" value="Y" required>
          <span><b>[필수]</b> 오픈 알림 발송을 위해 이름, 휴대폰 번호, 관심 지역을 수집합니다. 오픈 안내 완료 후 6개월 이내에 파기합니다.
          자세한 내용은 <a href="privacy.html">개인정보처리방침</a>에서 확인하실 수 있습니다.</span>
        </label>
        <label class="check">
          <input type="checkbox" name="agreeMarketing" value="Y">
          <span><b>[선택]</b> 오픈 이후에도 특가와 행사 안내를 문자·이메일로 받겠습니다. 동의하지 않으셔도 오픈 알림은 정상 발송됩니다.
          수신 거부는 언제든 가능합니다.</span>
        </label>
        <p class="err"></p>
      </div>

      <div class="form__msg form__msg--ok" role="status">
        <strong>오픈 알림 신청이 접수되었습니다.</strong>오픈일이 확정되면 남겨 주신 번호로 가장 먼저 문자를 보내드리겠습니다.
      </div>
      <div class="form__msg form__msg--ng" role="alert">
        <strong>신청을 접수하지 못했습니다.</strong>잠시 후 다시 시도해 주세요. 계속 실패한다면 아래 일반 문의 양식으로 남겨 주시면 확인하겠습니다.
      </div>

      <button class="btn btn--primary btn--lg" type="submit">오픈 알림 신청하기</button>
      <p class="xsmall">신청 후에도 언제든 수신을 해지하실 수 있습니다. 수집한 정보는 오픈 안내 외의 목적으로 사용하지 않습니다.</p>
    </form>
  </div>
</section>

<section class="sec sec--paper" id="contact">
  <div class="wrap wrap-sm">
    <div class="sec-head">
      <p class="eyebrow">GENERAL INQUIRY</p>
      <h2 class="h2">그 밖의 문의</h2>
      <p class="lead">제휴, 채용, 언론, 기타 문의는 이 양식으로 남겨 주세요. 대량 구매와 입점·납품은 전용 양식이 따로 있습니다.</p>
    </div>

    <form class="form" data-form="general" aria-label="일반 문의">
      <div class="field">
        <label for="g-type">문의 유형 <span class="req" aria-hidden="true">*</span></label>
        <select class="sel" id="g-type" name="inquiryType" required>
          <option value="">선택해 주세요</option>
          <option>제휴·협력 제안</option>
          <option>채용 문의</option>
          <option>언론·취재</option>
          <option>부지·임대 제안</option>
          <option>기타</option>
        </select>
        <p class="err"></p>
      </div>
      <div class="grid g-2" style="gap:18px">
        <div class="field">
          <label for="g-name">이름 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="g-name" name="name" type="text" required autocomplete="name">
          <p class="err"></p>
        </div>
        <div class="field">
          <label for="g-email">이메일 <span class="req" aria-hidden="true">*</span></label>
          <input class="inp" id="g-email" name="email" type="email" required autocomplete="email" placeholder="name@example.com">
          <p class="err"></p>
        </div>
      </div>
      <div class="field">
        <label for="g-message">문의 내용 <span class="req" aria-hidden="true">*</span></label>
        <textarea class="txt" id="g-message" name="message" required placeholder="문의하실 내용을 자세히 적어 주세요."></textarea>
        <p class="err"></p>
      </div>
      <div class="consent">
        <p class="consent__hd">개인정보 수집·이용 동의</p>
        <label class="check">
          <input type="checkbox" name="agreePrivacy" value="Y" required>
          <span><b>[필수]</b> 문의 회신을 위해 이름, 이메일, 문의 내용을 수집하며 접수일로부터 1년간 보관 후 파기합니다.
          자세한 내용은 <a href="privacy.html">개인정보처리방침</a>을 확인해 주세요.</span>
        </label>
        <p class="err"></p>
      </div>
      <div class="form__msg form__msg--ok" role="status">
        <strong>문의가 접수되었습니다.</strong>담당자가 확인 후 영업일 기준 3일 이내에 이메일로 회신드리겠습니다.
      </div>
      <div class="form__msg form__msg--ng" role="alert">
        <strong>문의를 접수하지 못했습니다.</strong>잠시 후 다시 시도해 주세요.
      </div>
      <button class="btn btn--navy btn--lg" type="submit">문의 보내기</button>
    </form>
  </div>
</section>
"""

write("notify.html", "오픈 알림·문의",
      "오렌지 마켓 오픈 알림 신청. 관심 지역과 카테고리를 남기면 오픈일과 첫 주 특가를 문자로 안내드립니다. 제휴·채용·기타 문의도 함께 접수합니다.",
      notify, active="")


# ==========================================================
# 개인정보처리방침
# ==========================================================
LEGAL_NOTE = """
<section class="sec sec--tight">
  <div class="wrap wrap-sm">
    <div class="note">
      <strong>법인 등록 정보 확정 전 게시본입니다.</strong>
      상호, 사업자등록번호, 주소, 대표자, 개인정보 보호책임자 정보는 법인 등록과 법무 검토가 끝난 뒤 확정 표기합니다.
      아래 내용은 현재 운영 중인 홈페이지 문의·알림 신청에 적용됩니다.
    </div>
  </div>
</section>"""

privacy = phd("PRIVACY", "개인정보처리방침",
              "오렌지 마켓은 홈페이지에서 수집하는 개인정보를 최소한으로 유지하고, 수집 목적이 끝나면 지체 없이 파기합니다.",
              [("개인정보처리방침", None)]) + LEGAL_NOTE + """
<section class="sec">
  <div class="wrap wrap-sm">
    <div class="doc">
      <h2>1. 수집하는 개인정보 항목과 수집 방법</h2>
      <p>오렌지 마켓 홈페이지는 아래 항목을 이용자가 직접 입력하는 방식으로만 수집합니다. 별도의 자동 수집 장치를 통해 개인을 식별하는 정보를 수집하지 않습니다.</p>
      <div class="tbl tbl--scroll">
        <table>
          <thead><tr><th scope="col" style="width:26%">수집 경로</th><th scope="col" style="width:34%">수집 항목</th><th scope="col">수집 목적</th></tr></thead>
          <tbody>
            <tr><th scope="row">오픈 알림 신청</th><td>이름, 휴대폰 번호, 관심 지역, 관심 카테고리, 이메일(선택)</td><td>오픈 일정과 행사 안내 발송</td></tr>
            <tr><th scope="row">대량·사업자 구매 문의</th><td>업체명, 담당자 이름, 연락처, 이메일(선택), 업종, 문의 내용</td><td>견적 산출과 상담 회신</td></tr>
            <tr><th scope="row">입점·납품 제안</th><td>회사명, 담당자 이름, 연락처, 이메일, 제안 품목·단가 정보</td><td>공급사 검토와 결과 회신</td></tr>
            <tr><th scope="row">일반 문의</th><td>이름, 이메일, 문의 유형, 문의 내용</td><td>문의 접수와 회신</td></tr>
          </tbody>
        </table>
      </div>

      <h2>2. 개인정보의 보유 및 이용 기간</h2>
      <ul>
        <li>오픈 알림 신청 정보: 오픈 안내 발송 완료 후 6개월 이내 파기</li>
        <li>대량 구매·입점 제안·일반 문의 정보: 접수일로부터 1년 보관 후 파기</li>
        <li>마케팅 수신에 동의하신 경우: 동의를 철회하실 때까지 보관하며, 철회 즉시 파기</li>
        <li>관계 법령에서 별도 보존 기간을 정한 경우에는 해당 기간 동안 보관합니다.</li>
      </ul>

      <h2>3. 개인정보의 제3자 제공</h2>
      <p>오렌지 마켓은 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 따라 수사기관이 적법한 절차로 요구하는 경우에는 예외로 합니다.</p>

      <h2>4. 개인정보 처리의 위탁</h2>
      <p>문자·이메일 발송과 홈페이지 운영을 위해 아래와 같은 업무를 위탁할 수 있습니다. 위탁 계약 시 개인정보 보호 관련 사항을 문서로 명시하고 관리·감독합니다. 실제 위탁사가 확정되면 이 항목에 상호와 위탁 업무를 구체적으로 기재합니다.</p>
      <ul>
        <li>문자·이메일 발송 대행</li>
        <li>홈페이지 호스팅 및 데이터 보관</li>
      </ul>

      <h2>5. 이용자의 권리와 행사 방법</h2>
      <p>이용자는 언제든지 본인의 개인정보에 대해 열람, 정정, 삭제, 처리 정지를 요구하실 수 있습니다. 홈페이지 문의 양식이나 개인정보 보호책임자 연락처로 요청해 주시면 지체 없이 처리하고 결과를 알려드립니다. 마케팅 수신 동의는 언제든 철회하실 수 있으며, 철회하셔도 이미 접수된 문의에 대한 회신은 정상적으로 이루어집니다.</p>

      <h2>6. 개인정보의 파기 절차와 방법</h2>
      <p>보유 기간이 지나거나 처리 목적이 달성된 개인정보는 지체 없이 파기합니다. 전자적 파일 형태로 저장된 정보는 복구할 수 없는 방식으로 삭제하고, 종이로 출력된 정보는 분쇄하거나 소각합니다.</p>

      <h2>7. 개인정보의 안전성 확보 조치</h2>
      <ul>
        <li>접근 권한 관리: 개인정보를 처리하는 담당자를 최소한으로 지정하고 권한을 구분합니다.</li>
        <li>전송 구간 암호화: 홈페이지 전 구간에 HTTPS를 적용합니다.</li>
        <li>접속 기록 관리: 개인정보 처리 시스템의 접속 기록을 보관하고 위·변조를 방지합니다.</li>
        <li>최소 수집: 목적에 필요한 최소한의 항목만 받고, 주민등록번호는 수집하지 않습니다.</li>
      </ul>

      <h2>8. 개인정보 보호책임자</h2>
      <p>개인정보 처리에 관한 문의, 불만 처리, 피해 구제는 아래 책임자에게 연락해 주시기 바랍니다. 담당자와 연락처는 법인 등록 완료 후 이 항목에 게재합니다.</p>
      <ul>
        <li>개인정보 보호책임자: 확정 후 게재</li>
        <li>연락처: 확정 후 게재</li>
        <li>접수 창구: 홈페이지 <a href="notify.html#contact">문의 양식</a></li>
      </ul>

      <h2>9. 권익 침해 구제 방법</h2>
      <p>개인정보 침해로 인한 상담이나 신고가 필요하신 경우 아래 기관에 문의하실 수 있습니다.</p>
      <ul>
        <li>개인정보침해신고센터 (privacy.kisa.or.kr / 국번없이 118)</li>
        <li>개인정보 분쟁조정위원회 (kopico.go.kr / 1833-6972)</li>
        <li>대검찰청 사이버수사과 (spo.go.kr / 국번없이 1301)</li>
        <li>경찰청 사이버수사국 (ecrm.police.go.kr / 국번없이 182)</li>
      </ul>

      <h2>10. 개인정보처리방침의 변경</h2>
      <p>이 방침의 내용이 추가, 삭제, 수정될 경우 변경 사항을 시행 7일 전부터 홈페이지에 공지합니다. 다만 이용자 권리에 중대한 변경이 있는 경우에는 최소 30일 전에 공지합니다.</p>
      <p class="doc__date">시행일: 홈페이지 정식 오픈일 (확정 후 게재)</p>
    </div>
  </div>
</section>
"""

write("privacy.html", "개인정보처리방침",
      "오렌지 마켓 홈페이지 개인정보처리방침. 수집 항목, 보유 기간, 제3자 제공, 이용자 권리 행사 방법을 안내합니다.",
      privacy, active="")


# ==========================================================
# 이용약관
# ==========================================================
terms = phd("TERMS", "홈페이지 이용약관",
            "오렌지 마켓 홈페이지 이용에 관한 기본 사항입니다. 매장 이용과 상품 판매에 관한 약관은 정식 오픈 시점에 별도로 게시합니다.",
            [("이용약관", None)]) + LEGAL_NOTE + """
<section class="sec">
  <div class="wrap wrap-sm">
    <div class="doc">
      <h2>제1조 (목적)</h2>
      <p>이 약관은 오렌지 마켓(이하 "회사")이 운영하는 홈페이지에서 제공하는 서비스의 이용 조건과 절차, 회사와 이용자의 권리·의무를 정하는 것을 목적으로 합니다.</p>

      <h2>제2조 (용어의 정의)</h2>
      <ul>
        <li>"홈페이지"란 회사가 브랜드와 매장 정보를 안내하기 위해 운영하는 웹사이트를 말합니다.</li>
        <li>"이용자"란 홈페이지에 접속하여 정보를 이용하거나 문의·신청을 제출하는 자를 말합니다.</li>
        <li>"게시물"이란 이용자가 문의 양식 등을 통해 제출한 글, 자료, 파일을 말합니다.</li>
      </ul>

      <h2>제3조 (약관의 게시와 개정)</h2>
      <p>회사는 이 약관을 홈페이지에 상시 게시합니다. 관련 법령을 위반하지 않는 범위에서 약관을 개정할 수 있으며, 개정 시 적용일과 개정 사유를 명시해 적용일 7일 전부터 공지합니다. 이용자에게 불리한 개정의 경우 30일 전부터 공지합니다.</p>

      <h2>제4조 (서비스의 제공)</h2>
      <p>회사는 홈페이지를 통해 다음 서비스를 제공합니다.</p>
      <ul>
        <li>브랜드, 상품 카테고리, 특가 운영 방식에 관한 정보 안내</li>
        <li>지점 정보와 오픈 일정 안내</li>
        <li>오픈 알림 신청 접수 및 발송</li>
        <li>대량 구매, 입점·납품, 기타 문의 접수 및 회신</li>
      </ul>

      <h2>제5조 (정보의 정확성과 변경)</h2>
      <p>홈페이지에 게시된 오픈 일정, 지점 정보, 상품 구성, 가격 표기 예시는 준비 상황에 따라 변경될 수 있습니다. 확정되지 않은 정보에는 확정 전임을 표시하며, 확정된 내용은 지체 없이 갱신합니다. 실제 매장에서 적용되는 가격과 행사 조건은 매장 게시물과 상품 가격표를 기준으로 합니다.</p>

      <h2>제6조 (서비스의 중단)</h2>
      <p>회사는 시스템 점검, 설비 교체, 통신 장애 등 불가피한 사유가 있는 경우 서비스 제공을 일시적으로 중단할 수 있습니다. 사전에 예측 가능한 중단은 미리 공지하며, 예측할 수 없는 중단은 사후에 안내합니다.</p>

      <h2>제7조 (이용자의 의무)</h2>
      <ul>
        <li>타인의 정보를 도용하거나 허위 정보를 입력해서는 안 됩니다.</li>
        <li>홈페이지의 정상적인 운영을 방해하는 행위를 해서는 안 됩니다.</li>
        <li>회사와 제3자의 지식재산권을 침해해서는 안 됩니다.</li>
        <li>법령과 공서양속에 반하는 내용을 게시해서는 안 됩니다.</li>
      </ul>

      <h2>제8조 (게시물의 관리)</h2>
      <p>회사는 이용자가 제출한 게시물이 법령을 위반하거나 타인의 권리를 침해하는 경우 사전 통지 없이 삭제하거나 접수를 거부할 수 있습니다.</p>

      <h2>제9조 (지식재산권)</h2>
      <p>홈페이지에 게시된 브랜드명, 로고, 마스코트, 이미지, 문구, 디자인의 지식재산권은 회사에 있습니다. 회사의 사전 서면 동의 없이 복제, 배포, 2차적 저작물 작성에 이용할 수 없습니다.</p>

      <h2>제10조 (면책)</h2>
      <p>회사는 천재지변, 통신 장애 등 회사의 통제를 벗어난 사유로 서비스를 제공할 수 없는 경우 그 책임을 지지 않습니다. 이용자가 홈페이지에 게시한 정보의 정확성에 대해서도 회사는 책임을 지지 않습니다.</p>

      <h2>제11조 (준거법과 관할)</h2>
      <p>이 약관은 대한민국 법령에 따라 해석하며, 회사와 이용자 사이에 분쟁이 발생한 경우 민사소송법에 따른 관할 법원에 소를 제기합니다.</p>
      <p class="doc__date">시행일: 홈페이지 정식 오픈일 (확정 후 게재)</p>
    </div>
  </div>
</section>
"""

write("terms.html", "이용약관",
      "오렌지 마켓 홈페이지 이용약관. 서비스 제공 범위, 정보의 정확성과 변경, 이용자의 의무, 지식재산권에 관한 사항을 안내합니다.",
      terms, active="")


# ==========================================================
# 404
# ==========================================================
nf = """
<section class="sec" style="padding:120px 0">
  <div class="wrap wrap-xs tc">
    <p class="eyebrow" style="justify-content:center">404 NOT FOUND</p>
    <h1 class="h1 mt-16 mb-24">이 통로에는<br>찾으시는 게 없습니다</h1>
    <p class="lead mb-40">주소가 바뀌었거나 페이지가 삭제되었을 수 있습니다. 아래 입구로 다시 들어와 주세요.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn--primary btn--lg" href="index.html">홈으로 가기</a>
      <a class="btn btn--ghost btn--lg" href="faq.html">고객센터</a>
    </div>
  </div>
</section>
"""

write("404.html", "페이지를 찾을 수 없습니다",
      "요청하신 페이지를 찾을 수 없습니다. 오렌지 마켓 홈으로 이동해 주세요.",
      nf, active="")



# ======================================================================
# 마무리: 확장자 없는 주소로 링크 정리
#   Cloudflare Pages가 /brand.html 을 /brand 로 308 리디렉션하므로,
#   처음부터 /brand 로 링크해 불필요한 리디렉션을 없앱니다.
# ======================================================================
import re as _re, glob as _glob
from urllib.parse import urlparse as _urlparse

_HOST = _urlparse(SITE).netloc


def _clean(name):
    base = name[:-5] if name.endswith(".html") else name
    return "/" if base == "index" else "/" + base


def finalize():
    for f in sorted(_glob.glob(os.path.join(OUT, "*.html"))):
        s = open(f, encoding="utf-8").read()
        s = _re.sub(r'href="([a-z0-9\-]+)\.html(#[^"]*)?"',
                    lambda m: 'href="%s%s"' % (_clean(m.group(1) + ".html"), m.group(2) or ""), s)
        s = _re.sub(r'(href=|content=)"https://%s/([a-z0-9\-]+)\.html"' % _re.escape(_HOST),
                    lambda m: '%s"https://%s%s"' % (m.group(1), _HOST, _clean(m.group(2) + ".html")), s)
        open(f, "w", encoding="utf-8").write(s)
    print("링크를 확장자 없는 주소로 정리했습니다.")


finalize()
print("\n14개 페이지를 다시 만들었습니다.")
