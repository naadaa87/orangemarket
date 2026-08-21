/**
 * POST /api/lead — 홈페이지 문의·오픈알림 접수
 *
 * Cloudflare Pages Functions로 자동 배포됩니다. 별도 설정 없이도 동작하며,
 * 아래 바인딩을 연결하면 저장과 알림이 함께 처리됩니다.
 *
 *  [KV 네임스페이스]  변수명 LEADS
 *      Pages 프로젝트 > Settings > Functions > KV namespace bindings
 *      연결하면 접수 건이 lead:<타입>:<시각>:<난수> 키로 저장됩니다.
 *
 *  [환경 변수]  LEAD_WEBHOOK_URL   (선택)
 *      Slack Incoming Webhook, Google Apps Script, 사내 API 주소 등.
 *      값이 있으면 접수 즉시 해당 주소로 JSON을 전달합니다.
 *
 *  [환경 변수]  ALLOWED_ORIGIN     (선택)
 *      기본값은 요청이 들어온 사이트 자신입니다. 다른 도메인에서 호출하려면 지정하세요.
 *
 * 바인딩이 하나도 없으면 검증만 수행하고 성공을 반환합니다(개발·미리보기용).
 */

const LIMITS = {
  name: 40, company: 80, phone: 20, email: 120, region: 80,
  item: 200, price: 60, moq: 60, biztype: 40, inquiryType: 40, message: 4000,
};

const FORM_TYPES = ["notify", "business", "supply", "general"];

const REQUIRED = {
  notify: ["name", "phone", "region"],
  business: ["company", "name", "phone", "biztype", "message"],
  supply: ["company", "name", "phone", "email", "item", "message"],
  general: ["inquiryType", "name", "email", "message"],
};

const json = (data, status = 200, origin = "*") =>
  new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "Access-Control-Allow-Origin": origin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });

/** 제어문자 제거 + 길이 제한 */
function clean(value, max) {
  if (value === undefined || value === null) return "";
  const text = Array.isArray(value) ? value.join(", ") : String(value);
  // eslint-disable-next-line no-control-regex
  return text.replace(/[\u0000-\u001F\u007F]/g, " ").trim().slice(0, max || 200);
}

export async function onRequestOptions(context) {
  const origin = context.env.ALLOWED_ORIGIN || new URL(context.request.url).origin;
  return json({ ok: true }, 204, origin);
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const origin = env.ALLOWED_ORIGIN || new URL(request.url).origin;

  let raw;
  try {
    raw = await request.json();
  } catch {
    return json({ ok: false, error: "본문을 읽지 못했습니다." }, 400, origin);
  }

  const formType = FORM_TYPES.includes(raw.formType) ? raw.formType : "general";

  // 봇 차단: 화면에 없는 필드가 채워져 있으면 조용히 성공 처리
  if (clean(raw.website, 50)) return json({ ok: true, id: "skipped" }, 200, origin);

  const record = { formType };
  for (const key of Object.keys(LIMITS)) {
    const value = clean(raw[key], LIMITS[key]);
    if (value) record[key] = value;
  }
  record.category = clean(raw.category, 200);
  record.ready = clean(raw.ready, 200);
  record.agreePrivacy = raw.agreePrivacy === "Y" || raw.agreePrivacy === true;
  record.agreeMarketing = raw.agreeMarketing === "Y" || raw.agreeMarketing === true;

  // 필수값 검증
  const missing = (REQUIRED[formType] || []).filter((key) => !record[key]);
  if (missing.length) {
    return json({ ok: false, error: "필수 항목이 비어 있습니다.", fields: missing }, 400, origin);
  }
  if (!record.agreePrivacy) {
    return json({ ok: false, error: "개인정보 수집·이용 동의가 필요합니다." }, 400, origin);
  }
  if (record.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(record.email)) {
    return json({ ok: false, error: "이메일 형식을 확인해 주세요." }, 400, origin);
  }
  if (record.phone && !/^0\d{1,2}-?\d{3,4}-?\d{4}$/.test(record.phone.replace(/\s/g, ""))) {
    return json({ ok: false, error: "휴대폰 번호 형식을 확인해 주세요." }, 400, origin);
  }

  // 수신 메타 (개인 식별 목적이 아닌 접수 추적용)
  record.receivedAt = new Date().toISOString();
  record.pageUrl = clean(raw.pageUrl, 200);
  record.referrer = clean(raw.referrer, 200);
  record.country = request.headers.get("CF-IPCountry") || "";

  const id = `lead:${formType}:${Date.now()}:${crypto.randomUUID().slice(0, 8)}`;

  // 1) KV 저장
  if (env.LEADS) {
    try {
      await env.LEADS.put(id, JSON.stringify(record), {
        // 오픈알림 12개월, 문의 24개월 후 자동 삭제 (개인정보처리방침 보관기간 기준)
        expirationTtl: formType === "notify" ? 60 * 60 * 24 * 365 : 60 * 60 * 24 * 730,
        metadata: { formType, receivedAt: record.receivedAt },
      });
    } catch (err) {
      console.error("KV put failed", err);
      return json({ ok: false, error: "저장에 실패했습니다." }, 500, origin);
    }
  }

  // 2) 웹훅 전달 (실패해도 접수는 유효)
  if (env.LEAD_WEBHOOK_URL) {
    try {
      await fetch(env.LEAD_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, ...record }),
      });
    } catch (err) {
      console.error("webhook failed", err);
    }
  }

  return json({ ok: true, id }, 200, origin);
}

/** POST 외 메서드 차단 */
export async function onRequest(context) {
  if (context.request.method === "POST" || context.request.method === "OPTIONS") {
    return context.next();
  }
  return json({ ok: false, error: "POST 요청만 처리합니다." }, 405);
}
