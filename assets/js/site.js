/* ============================================================
   오렌지마켓 — 공통 스크립트
   의존성 없음. 모든 기능은 해당 요소가 있을 때만 동작합니다.
   ============================================================ */
(function () {
  "use strict";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 헤더 : 모바일 메뉴 · 스크롤 그림자 · 현재 메뉴 ---------- */
  function header() {
    var hd = $(".hd");
    if (!hd) return;

    var burger = $(".burger", hd);
    if (burger) {
      burger.addEventListener("click", function () {
        var open = hd.classList.toggle("is-open");
        burger.setAttribute("aria-expanded", String(open));
        document.body.style.overflow = open ? "hidden" : "";
      });
      $$(".gnb a", hd).forEach(function (a) {
        a.addEventListener("click", function () {
          hd.classList.remove("is-open");
          burger.setAttribute("aria-expanded", "false");
          document.body.style.overflow = "";
        });
      });
      window.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && hd.classList.contains("is-open")) burger.click();
      });
    }

    var onScroll = function () { hd.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    // 현재 페이지 메뉴 표시
    // Cloudflare Pages는 /brand.html 을 /brand 로 정규화하므로 양쪽 모두 인식합니다.
    var norm = function (path) {
      var p = (path || "").split("?")[0].split("#")[0];
      p = p.replace(/\/+$/, "");
      p = p.replace(/\.html$/, "");
      p = p.replace(/\/index$/, "");
      if (p.charAt(0) !== "/") p = "/" + p;
      return p === "" ? "/" : p;
    };
    var here = norm(location.pathname);
    $$(".gnb a", hd).forEach(function (a) {
      if (norm(a.getAttribute("href")) === here) a.setAttribute("aria-current", "page");
    });
  }

  /* ---------- 스크롤 등장 ---------- */
  function reveal() {
    var items = $$(".rv");
    if (!items.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var delay = parseInt(el.getAttribute("data-rv-delay") || "0", 10);
        setTimeout(function () { el.classList.add("is-in"); }, delay);
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 아코디언 ---------- */
  function accordion() {
    $$(".acc").forEach(function (acc) {
      var single = acc.hasAttribute("data-single");
      $$(".acc__q", acc).forEach(function (q) {
        var item = q.closest(".acc__it");
        var panel = $(".acc__a", item);
        if (panel && !panel.id) panel.id = "acc-" + Math.random().toString(36).slice(2, 8);
        q.setAttribute("aria-expanded", item.classList.contains("is-open") ? "true" : "false");
        if (panel) q.setAttribute("aria-controls", panel.id);
        q.addEventListener("click", function () {
          var open = item.classList.contains("is-open");
          if (single && !open) {
            $$(".acc__it.is-open", acc).forEach(function (o) {
              o.classList.remove("is-open");
              $(".acc__q", o).setAttribute("aria-expanded", "false");
            });
          }
          item.classList.toggle("is-open", !open);
          q.setAttribute("aria-expanded", String(!open));
        });
      });
    });
  }

  /* ---------- 필터 + 검색 ---------- */
  /* 사용법: [data-filter-root] 안에 .filt[data-filter], [data-search], [data-item][data-tags] */
  function filters() {
    $$("[data-filter-root]").forEach(function (root) {
      var btns = $$(".filt", root);
      var input = $("[data-search]", root);
      var items = $$("[data-item]", root);
      var empty = $(".empty", root);
      var count = $("[data-count]", root);
      var active = "all";

      function apply() {
        var q = (input ? input.value : "").trim().toLowerCase();
        var shown = 0;
        items.forEach(function (el) {
          var tags = (el.getAttribute("data-tags") || "").toLowerCase();
          var text = el.textContent.toLowerCase();
          var okTag = active === "all" || tags.indexOf(active) > -1;
          var okQ = !q || text.indexOf(q) > -1 || tags.indexOf(q) > -1;
          var ok = okTag && okQ;
          el.style.display = ok ? "" : "none";
          if (ok) shown++;
        });
        if (empty) empty.classList.toggle("is-on", shown === 0);
        if (count) count.textContent = String(shown);
      }

      btns.forEach(function (b) {
        b.addEventListener("click", function () {
          active = b.getAttribute("data-filter") || "all";
          btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
          apply();
        });
      });
      if (input) {
        var t;
        input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(apply, 120); });
      }
      apply();
    });
  }

  /* ---------- 폼 ---------- */
  var LABEL = {
    name: "이름", phone: "휴대폰 번호", email: "이메일", company: "업체명",
    region: "관심 지역", message: "문의 내용", category: "관심 카테고리",
    item: "제안 품목", biztype: "업종", agreePrivacy: "개인정보 수집·이용 동의"
  };

  function setErr(field, msg) {
    if (!field) return;
    field.classList.add("is-err");
    var box = $(".err", field);
    if (box) box.textContent = msg;
    var ctl = $(".inp, .txt, .sel", field);
    if (ctl) ctl.setAttribute("aria-invalid", "true");
  }
  function clearErr(field) {
    if (!field) return;
    field.classList.remove("is-err");
    var ctl = $(".inp, .txt, .sel", field);
    if (ctl) ctl.removeAttribute("aria-invalid");
  }

  function validate(form) {
    var ok = true, first = null;
    $$(".field", form).forEach(clearErr);

    $$("[required]", form).forEach(function (ctl) {
      if (ctl.type === "checkbox") return;
      var field = ctl.closest(".field");
      var v = (ctl.value || "").trim();
      var name = LABEL[ctl.name] || "필수 항목";
      if (!v) {
        setErr(field, name + "을(를) 입력해 주세요.");
        ok = false; first = first || ctl;
        return;
      }
      if (ctl.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
        setErr(field, "이메일 형식을 확인해 주세요. 예) name@company.com");
        ok = false; first = first || ctl;
      }
      if (ctl.type === "tel" && !/^0\d{1,2}-?\d{3,4}-?\d{4}$/.test(v.replace(/\s/g, ""))) {
        setErr(field, "휴대폰 번호를 숫자로 정확히 입력해 주세요. 예) 010-1234-5678");
        ok = false; first = first || ctl;
      }
    });

    var agree = $('input[name="agreePrivacy"]', form);
    if (agree && !agree.checked) {
      var f = agree.closest(".consent") || agree.closest(".field");
      if (f) {
        f.classList.add("is-err");
        var e = $(".err", f);
        if (e) e.textContent = "개인정보 수집·이용에 동의해야 접수할 수 있습니다.";
      }
      ok = false; first = first || agree;
    }

    if (first) {
      first.focus({ preventScroll: true });
      first.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    }
    return ok;
  }

  function collect(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (data[k] === undefined) data[k] = v;
      else if (Array.isArray(data[k])) data[k].push(v);
      else data[k] = [data[k], v];
    });
    data.formType = form.getAttribute("data-form") || "general";
    data.pageUrl = location.pathname;
    data.referrer = document.referrer || "";
    return data;
  }

  function forms() {
    $$("form[data-form]").forEach(function (form) {
      var msg = $(".form__msg", form);
      var okMsg = $(".form__msg--ok", form);
      var ngMsg = $(".form__msg--ng", form);
      var btn = $('button[type="submit"]', form);

      $$(".inp, .txt, .sel", form).forEach(function (ctl) {
        ctl.addEventListener("input", function () { clearErr(ctl.closest(".field")); });
      });
      var agree = $('input[name="agreePrivacy"]', form);
      if (agree) agree.addEventListener("change", function () {
        var box = agree.closest(".consent") || agree.closest(".field");
        if (box) box.classList.remove("is-err");
      });

      form.setAttribute("novalidate", "novalidate");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (okMsg) okMsg.classList.remove("is-on");
        if (ngMsg) ngMsg.classList.remove("is-on");
        if (!validate(form)) return;

        var label = btn ? btn.textContent : "";
        if (btn) { btn.disabled = true; btn.textContent = "접수 중…"; }

        fetch("/api/lead", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(collect(form))
        })
          .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("HTTP " + r.status)); })
          .then(function () {
            form.reset();
            if (okMsg) {
              okMsg.classList.add("is-on");
              okMsg.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
              okMsg.setAttribute("tabindex", "-1");
              okMsg.focus({ preventScroll: true });
            }
          })
          .catch(function () {
            if (ngMsg) {
              ngMsg.classList.add("is-on");
              ngMsg.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
            }
          })
          .finally(function () {
            if (btn) { btn.disabled = false; btn.textContent = label; }
          });
      });
    });
  }

  /* ---------- 푸터 연도 ---------- */
  function year() {
    $$("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
  }

  /* ---------- 실행 ---------- */
  function init() {
    header(); reveal(); accordion(); filters(); forms(); year();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
