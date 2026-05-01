import streamlit as st
import requests
import json
from datetime import date, timedelta
import os
import io

try:
    from weasyprint import HTML as WeasyprintHTML
    PDF_SUPPORT = True
except Exception:
    PDF_SUPPORT = False

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be FIRST streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InvoicePro PK",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  LANGUAGE DATA
# ─────────────────────────────────────────────
LANG = {
    "en": {
        "title": "InvoicePro PK",
        "subtitle": "Freelance Invoice Generator",
        "lang_btn": "🇵🇰 اردو",
        "step1": "Fill your info",
        "step2": "Add client name",
        "step3": "Add services",
        "step4": "✨ Get AI Tips",
        "step5": "🖨 Save PDF",
        "your_info": "👤 Your Info",
        "your_name": "Your Name",
        "your_service": "Service",
        "your_contact": "Email / Phone",
        "client_info": "🏢 Client Info",
        "client_name": "Client Name",
        "client_country": "Country",
        "inv_details": "📋 Invoice Details",
        "inv_num": "Invoice #",
        "currency": "Currency",
        "issue_date": "Issue Date",
        "due_date": "Due Date",
        "services": "🛠 Services / Items",
        "desc_col": "Description",
        "qty_col": "Qty",
        "rate_col": "Rate",
        "total_col": "Total",
        "add_item": "＋ Add Item",
        "tax": "Tax %",
        "discount": "Discount %",
        "notes": "Notes / Bank Details",
        "ai_btn": "✨ Get AI Tips",
        "pdf_btn": "🖨 Download Invoice (PDF)",
        "ai_title": "✨ AI Tips",
        "ai_wait": "Generating tips, please wait...",
        "preview_title": "📄 Live Invoice Preview",
        "bill_to": "Bill To",
        "invoice_word": "INVOICE",
        "subtotal": "Subtotal",
        "discount_lbl": "Discount",
        "tax_lbl": "Tax",
        "total_lbl": "TOTAL",
        "footer_txt": "Generated with InvoicePro PK — Professional Freelance Invoicing",
        "ph_name": "e.g. Ali Hassan",
        "ph_service": "e.g. Web Developer",
        "ph_contact": "ali@gmail.com | 0300-0000000",
        "ph_client": "e.g. ABC Company",
        "ph_notes": "Bank: HBL | Account: 12345678 | Payment within 7 days",
        "ph_desc": "Service description",
        "ai_prompt": (
            "You are a Pakistani freelance invoice expert. "
            "Freelancer '{name}' provides '{serv}'. "
            "Invoice total is {amt} {cur}, client is from {country}. "
            "Give exactly 3 practical tips IN ENGLISH: "
            "1) How to receive payment 2) Professional invoice tips 3) How to deal with the client. "
            "Keep it short, friendly, max 5 lines."
        ),
        "currencies": ["PKR — Pakistani Rupee", "USD — US Dollar", "AED — UAE Dirham", "GBP — British Pound", "SAR — Saudi Riyal"],
        "cur_codes":  ["PKR", "USD", "AED", "GBP", "SAR"],
        "countries": ["Pakistan", "UAE", "USA", "UK", "Saudi Arabia", "Canada", "Australia"],
        "no_api_key": "⚠️ ANTHROPIC_API_KEY not set. Please add it to your environment variables to use AI tips.",
        "default_tip": "💡 Always include clear payment terms in your invoice. A 7-day deadline helps clients pay faster!",
    },
    "ur": {
        "title": "InvoicePro PK",
        "subtitle": "فری لانس انوائس جنریٹر",
        "lang_btn": "🇬🇧 English",
        "step1": "اپنی معلومات بھریں",
        "step2": "کلائنٹ نام لکھیں",
        "step3": "خدمات شامل کریں",
        "step4": "✨ AI مشورہ لیں",
        "step5": "🖨 PDF محفوظ کریں",
        "your_info": "👤 آپ کی معلومات",
        "your_name": "آپ کا نام",
        "your_service": "سروس",
        "your_contact": "ای میل / فون",
        "client_info": "🏢 کلائنٹ معلومات",
        "client_name": "کلائنٹ نام",
        "client_country": "ملک",
        "inv_details": "📋 انوائس تفصیل",
        "inv_num": "انوائس نمبر",
        "currency": "کرنسی",
        "issue_date": "تاریخ",
        "due_date": "آخری تاریخ",
        "services": "🛠 خدمات / آئٹمز",
        "desc_col": "تفصیل",
        "qty_col": "تعداد",
        "rate_col": "ریٹ",
        "total_col": "کل",
        "add_item": "＋ آئٹم شامل کریں",
        "tax": "ٹیکس %",
        "discount": "چھوٹ %",
        "notes": "نوٹس / بینک تفصیل",
        "ai_btn": "✨ AI مشورہ لیں",
        "pdf_btn": "🖨 انوائس PDF ڈاؤنلوڈ کریں",
        "ai_title": "✨ AI کا مشورہ",
        "ai_wait": "مشورہ تیار ہو رہا ہے...",
        "preview_title": "📄 لائیو انوائس پریویو",
        "bill_to": "بل بھیجیں",
        "invoice_word": "INVOICE",
        "subtotal": "کل رقم",
        "discount_lbl": "چھوٹ",
        "tax_lbl": "ٹیکس",
        "total_lbl": "کل",
        "footer_txt": "InvoicePro PK کے ساتھ بنایا گیا",
        "ph_name": "مثلاً علی حسن",
        "ph_service": "مثلاً ویب ڈویلپر",
        "ph_contact": "ali@gmail.com | 0300-0000000",
        "ph_client": "مثلاً ABC کمپنی",
        "ph_notes": "بینک: HBL | اکاونٹ: 12345678 | 7 دن میں ادائیگی",
        "ph_desc": "خدمت کی تفصیل",
        "ai_prompt": (
            "Tu ek Pakistani freelance invoice expert hai. "
            "Freelancer '{name}' '{serv}' karta hai. "
            "Invoice ki total {amt} {cur} hai, client {country} se hai. "
            "Bilkul 3 practical tips URDU mein do: "
            "1) Payment kaise milegi 2) Professional invoice tips 3) Client se kaise deal karein. "
            "Short aur friendly raho, max 5 lines."
        ),
        "currencies": ["PKR — پاکستانی روپیہ", "USD — امریکی ڈالر", "AED — درہم", "GBP — پاؤنڈ", "SAR — سعودی ریال"],
        "cur_codes":  ["PKR", "USD", "AED", "GBP", "SAR"],
        "countries": ["پاکستان", "متحدہ عرب امارات", "امریکہ", "برطانیہ", "سعودی عرب", "کینیڈا", "آسٹریلیا"],
        "no_api_key": "⚠️ ANTHROPIC_API_KEY سیٹ نہیں ہے۔",
        "default_tip": "💡 ہر انوائس میں payment کی آخری تاریخ ضرور لکھیں۔ 7 دن کی deadline سے clients جلدی ادائیگی کرتے ہیں!",
    },
}

CUR_SYMBOLS = {"PKR": "Rs. ", "USD": "$ ", "AED": "AED ", "GBP": "£", "SAR": "SAR "}

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
DEFAULTS = {
    "lang": "en",
    "inv_items": [{"desc": "", "qty": 1.0, "rate": 0.0}],
    "ai_tip": "",
    "fname": "",
    "fservice": "",
    "fcontact": "",
    "cname": "",
    "c_country_idx": 0,
    "inv_num": "INV-001",
    "cur_idx": 0,
    "issue_date": date.today(),
    "due_date": date.today() + timedelta(days=7),
    "tax_pct": 0.0,
    "disc_pct": 0.0,
    "notes": "",
}
for _k, _v in DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def L(key):
    return LANG[st.session_state.lang][key]

def get_cur_code():
    return L("cur_codes")[st.session_state.cur_idx]

def get_cur_sym():
    return CUR_SYMBOLS.get(get_cur_code(), get_cur_code() + " ")

def calc(items, disc, tax):
    sub = sum(max(it["qty"], 0) * max(it["rate"], 0) for it in items)
    da  = sub * disc / 100
    aft = sub - da
    ta  = aft * tax / 100
    return sub, da, ta, aft + ta

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background:#0a0a0a !important;
    color:#e5e5e5 !important;
    font-family:'Segoe UI',Arial,sans-serif !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
#MainMenu, footer { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-thumb{background:#6c63ff;border-radius:3px}

.topbar-wrap {
    background:#111;
    border-bottom:2px solid #6c63ff;
    padding:12px 20px 10px 20px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:0;
}
.logo-box {
    width:36px;height:36px;
    background:#6c63ff;border-radius:8px;
    display:inline-flex;align-items:center;justify-content:center;
    color:#fff;font-weight:800;font-size:15px;
    vertical-align:middle;margin-right:10px;
}
.logo-name{font-size:16px;font-weight:700;color:#fff;display:inline}
.logo-sub{font-size:11px;color:#888;padding-left:46px;margin-top:2px}

.guide-bar {
    background:#161625;border-bottom:1px solid #2a2a3a;
    padding:9px 20px;display:flex;gap:18px;flex-wrap:wrap;
    margin-bottom:0;
}
.gstep{display:flex;align-items:center;gap:7px}
.gnum{
    width:22px;height:22px;background:#6c63ff;border-radius:50%;
    color:#fff;font-size:10px;font-weight:700;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.gtxt{color:#bbb;font-size:12px}

.slabel{
    font-size:10px;font-weight:700;color:#a78bfa;
    text-transform:uppercase;letter-spacing:.1em;
    border-left:3px solid #6c63ff;padding-left:8px;
    margin:14px 0 6px;display:block;
}

/* inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background:#1e1e1e !important;
    border:1.5px solid #3a3a3a !important;
    border-radius:7px !important;
    color:#fff !important;
    font-size:13px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color:#6c63ff !important;
    background:#1a1a2e !important;
    box-shadow:none !important;
}
div[data-baseweb="select"] > div {
    background:#1e1e1e !important;
    border:1.5px solid #3a3a3a !important;
    border-radius:7px !important;
}
div[data-baseweb="select"] * {color:#fff !important}
[data-testid="stDateInput"] input {
    background:#1e1e1e !important;border:1.5px solid #3a3a3a !important;
    color:#fff !important;border-radius:7px !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stDateInput"] label {
    color:#aaa !important;font-size:12px !important;font-weight:500 !important;
}

/* buttons */
.stButton > button {
    border-radius:8px !important;font-weight:700 !important;
    font-size:13px !important;padding:9px 12px !important;
    width:100% !important;transition:all .2s !important;
    cursor:pointer !important;
}
.wrap-lang .stButton > button {
    background:#6c63ff !important;color:#fff !important;
    border:2px solid #8b85ff !important;
    font-size:13px !important;white-space:nowrap !important;
    font-family:'Segoe UI',Tahoma,Arial,sans-serif !important;
    letter-spacing:0 !important;
}
.wrap-lang .stButton > button:hover {background:#5a52e0 !important;color:#fff !important}

.wrap-ai .stButton > button {
    background:#6c63ff !important;color:#fff !important;
    border:2px solid #8b85ff !important;
}
.wrap-ai .stButton > button:hover {background:#7c73ff !important}

.wrap-add .stButton > button {
    background:#1a2a1a !important;color:#2ecc71 !important;
    border:2px solid #2ecc71 !important;
    margin-bottom:10px;
}
.wrap-add .stButton > button:hover {background:#2ecc71 !important;color:#000 !important}

.wrap-del .stButton > button {
    background:#3a1010 !important;color:#ff6b6b !important;
    border:1.5px solid #cc3333 !important;
    padding:5px 8px !important;font-size:14px !important;
    min-height:unset !important;
}
.wrap-del .stButton > button:hover {background:#cc3333 !important;color:#fff !important}

[data-testid="stDownloadButton"] > button {
    background:#e67e22 !important;color:#fff !important;
    border:2px solid #f39c12 !important;
    border-radius:8px !important;font-weight:700 !important;
    font-size:13px !important;width:100% !important;
    padding:9px 12px !important;
}
[data-testid="stDownloadButton"] > button:hover {background:#f39c12 !important}

.tipbox {
    background:#1a1030;border:2px solid #6c63ff;
    border-radius:10px;padding:14px 16px;margin-top:14px;
}
.tiplabel{font-size:11px;color:#a78bfa;font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px}
.tiptext{font-size:13px;color:#ddd;line-height:1.75;white-space:pre-wrap}

/* invoice card */
.inv-card {
    background:#fff;border-radius:12px;
    padding:26px;color:#111;
    box-shadow:0 4px 24px rgba(108,99,255,.15);
    font-family:'Segoe UI',Arial,sans-serif;
}
.phead{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px}
.pbrand{font-size:20px;font-weight:800;color:#6c63ff}
.pbrand-sub{font-size:12px;color:#888;margin-top:2px}
.pbrand-con{font-size:11px;color:#999;margin-top:2px}
.pbadge{background:#6c63ff;color:#fff;font-size:10px;font-weight:700;padding:5px 14px;border-radius:22px;letter-spacing:.07em}
.pmeta{display:flex;justify-content:space-between;gap:14px;margin-bottom:16px}
.ppty{flex:1}
.ppty-lbl{font-size:9px;color:#aaa;text-transform:uppercase;letter-spacing:.08em;margin-bottom:3px}
.ppty-name{font-size:14px;font-weight:700;color:#111}
.ppty-detail{font-size:12px;color:#777}
.pinfos{display:grid;grid-template-columns:1fr 1fr;gap:6px;min-width:160px}
.pinfo{background:#f4f3ff;border-radius:7px;padding:6px 10px}
.pinfo-lbl{font-size:9px;color:#aaa}
.pinfo-val{font-size:12px;font-weight:600;color:#333}
.pdiv{border:none;border-top:1px solid #eee;margin:14px 0}
.ptable{width:100%;border-collapse:collapse;font-size:12px}
.ptable th{font-size:9px;color:#aaa;text-transform:uppercase;padding:4px 6px;border-bottom:1px solid #eee;text-align:left;letter-spacing:.05em}
.ptable td{padding:7px 6px;border-bottom:.5px solid #f5f5f5;color:#444}
.ptable td:last-child,.ptable th:last-child{text-align:right}
.ptotals{margin-left:auto;width:52%;margin-top:12px}
.ptrow{display:flex;justify-content:space-between;font-size:12px;color:#666;padding:3px 0}
.ptrow.grand{font-size:15px;font-weight:800;color:#111;border-top:2px solid #6c63ff;margin-top:8px;padding-top:8px}
.ptrow.red{color:#e74c3c}
.pnotes{font-size:11px;color:#666;background:#f9f9f9;border-radius:7px;padding:9px 12px;margin-top:12px;border-left:3px solid #6c63ff}
.pfooter{margin-top:14px;font-size:10px;color:#ccc;border-top:1px solid #eee;padding-top:9px;text-align:center}
.prev-label{font-size:12px;color:#888;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.dot{width:8px;height:8px;background:#6c63ff;border-radius:50%;display:inline-block;flex-shrink:0}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TOP BAR  (HTML logo + Streamlit lang button)
# ─────────────────────────────────────────────
tc1, tc2 = st.columns([8, 1])
with tc1:
    st.markdown(f"""
    <div class="topbar-wrap">
      <div>
        <span class="logo-box">IP</span>
        <span class="logo-name">{L('title')}</span>
        <div class="logo-sub">{L('subtitle')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
with tc2:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='wrap-lang'>", unsafe_allow_html=True)
    if st.button(L("lang_btn"), key="btn_lang"):
        st.session_state.lang = "ur" if st.session_state.lang == "en" else "en"
        st.session_state.ai_tip = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GUIDE STEPS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="guide-bar">
  <div class="gstep"><div class="gnum">1</div><div class="gtxt">{L('step1')}</div></div>
  <div class="gstep"><div class="gnum">2</div><div class="gtxt">{L('step2')}</div></div>
  <div class="gstep"><div class="gnum">3</div><div class="gtxt">{L('step3')}</div></div>
  <div class="gstep"><div class="gnum">4</div><div class="gtxt">{L('step4')}</div></div>
  <div class="gstep"><div class="gnum">5</div><div class="gtxt">{L('step5')}</div></div>
</div>
<div style="height:4px"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN 2-COLUMN LAYOUT
# ─────────────────────────────────────────────
left_col, right_col = st.columns(2, gap="small")

# ══════════════════════════════
#  LEFT — FORM
# ══════════════════════════════
with left_col:

    # YOUR INFO
    st.markdown(f"<span class='slabel'>{L('your_info')}</span>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        new_val = st.text_input(L("your_name"), placeholder=L("ph_name"),
                                value=st.session_state.fname, key="inp_fname")
        st.session_state.fname = new_val
    with r1c2:
        new_val = st.text_input(L("your_service"), placeholder=L("ph_service"),
                                value=st.session_state.fservice, key="inp_fservice")
        st.session_state.fservice = new_val

    new_val = st.text_input(L("your_contact"), placeholder=L("ph_contact"),
                             value=st.session_state.fcontact, key="inp_fcontact")
    st.session_state.fcontact = new_val

    # CLIENT INFO
    st.markdown(f"<span class='slabel'>{L('client_info')}</span>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        new_val = st.text_input(L("client_name"), placeholder=L("ph_client"),
                                value=st.session_state.cname, key="inp_cname")
        st.session_state.cname = new_val
    with r2c2:
        clist = L("countries")
        if st.session_state.c_country_idx >= len(clist):
            st.session_state.c_country_idx = 0
        chosen_country = st.selectbox(L("client_country"), options=clist,
                                      index=st.session_state.c_country_idx, key="sel_country")
        st.session_state.c_country_idx = clist.index(chosen_country)

    # INVOICE DETAILS
    st.markdown(f"<span class='slabel'>{L('inv_details')}</span>", unsafe_allow_html=True)
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        new_val = st.text_input(L("inv_num"), value=st.session_state.inv_num, key="inp_invnum")
        st.session_state.inv_num = new_val
    with r3c2:
        curlist = L("currencies")
        if st.session_state.cur_idx >= len(curlist):
            st.session_state.cur_idx = 0
        chosen_cur = st.selectbox(L("currency"), options=curlist,
                                  index=st.session_state.cur_idx, key="sel_currency")
        st.session_state.cur_idx = curlist.index(chosen_cur)

    r4c1, r4c2 = st.columns(2)
    with r4c1:
        new_val = st.date_input(L("issue_date"), value=st.session_state.issue_date, key="inp_idate")
        st.session_state.issue_date = new_val
    with r4c2:
        new_val = st.date_input(L("due_date"), value=st.session_state.due_date, key="inp_ddate")
        st.session_state.due_date = new_val

    # SERVICES / ITEMS
    st.markdown(f"<span class='slabel'>{L('services')}</span>", unsafe_allow_html=True)

    # column headers
    hh1, hh2, hh3, hh4 = st.columns([3, 1, 1.5, 0.5])
    for col, lbl in zip([hh1, hh2, hh3], ["desc_col", "qty_col", "rate_col"]):
        col.markdown(
            f"<div style='font-size:11px;color:#a78bfa;font-weight:700;"
            f"text-transform:uppercase;padding-bottom:6px;letter-spacing:.08em'>{L(lbl)}</div>",
            unsafe_allow_html=True
        )

    to_delete = []
    for i, item in enumerate(st.session_state.inv_items):
        ic1, ic2, ic3, ic4 = st.columns([3, 1, 1.5, 0.5])
        with ic1:
            v = st.text_input("d", value=item["desc"], placeholder=L("ph_desc"),
                              label_visibility="collapsed", key=f"d_{i}")
            st.session_state.inv_items[i]["desc"] = v
        with ic2:
            v = st.number_input("q", value=float(item["qty"]), min_value=0.0, step=1.0,
                                label_visibility="collapsed", key=f"q_{i}")
            st.session_state.inv_items[i]["qty"] = v
        with ic3:
            v = st.number_input("r", value=float(item["rate"]), min_value=0.0, step=500.0,
                                label_visibility="collapsed", key=f"r_{i}")
            st.session_state.inv_items[i]["rate"] = v
        with ic4:
            st.markdown("<div class='wrap-del'>", unsafe_allow_html=True)
            if st.button("🗑", key=f"del_{i}"):
                to_delete.append(i)
            st.markdown("</div>", unsafe_allow_html=True)

    if to_delete:
        for di in sorted(to_delete, reverse=True):
            st.session_state.inv_items.pop(di)
        if len(st.session_state.inv_items) == 0:
            st.session_state.inv_items = [{"desc": "", "qty": 1.0, "rate": 0.0}]
        st.rerun()

    st.markdown("<div class='wrap-add'>", unsafe_allow_html=True)
    if st.button(L("add_item"), key="btn_add"):
        st.session_state.inv_items.append({"desc": "", "qty": 1.0, "rate": 0.0})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # TAX & DISCOUNT
    tx1, tx2 = st.columns(2)
    with tx1:
        v = st.number_input(L("tax"), value=st.session_state.tax_pct,
                            min_value=0.0, max_value=100.0, step=1.0, key="inp_tax")
        st.session_state.tax_pct = v
    with tx2:
        v = st.number_input(L("discount"), value=st.session_state.disc_pct,
                            min_value=0.0, max_value=100.0, step=1.0, key="inp_disc")
        st.session_state.disc_pct = v

    # NOTES
    v = st.text_area(L("notes"), value=st.session_state.notes,
                     placeholder=L("ph_notes"), height=80, key="inp_notes")
    st.session_state.notes = v

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ACTION BUTTONS
    ab1, ab2 = st.columns(2)

    # ── AI TIPS BUTTON ──
    with ab1:
        st.markdown("<div class='wrap-ai'>", unsafe_allow_html=True)
        ai_clicked = st.button(L("ai_btn"), key="btn_ai")
        st.markdown("</div>", unsafe_allow_html=True)

    if ai_clicked:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            st.session_state.ai_tip = L("no_api_key")
        else:
            sub, _, _, total_amt = calc(
                st.session_state.inv_items,
                st.session_state.disc_pct,
                st.session_state.tax_pct
            )
            prompt_text = L("ai_prompt").format(
                name=st.session_state.fname or "Freelancer",
                serv=st.session_state.fservice or "services",
                amt=int(round(total_amt)),
                cur=get_cur_code(),
                country=chosen_country,
            )
            with st.spinner(L("ai_wait")):
                try:
                    resp = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-sonnet-4-5",
                            "max_tokens": 500,
                            "messages": [{"role": "user", "content": prompt_text}],
                        },
                        timeout=30,
                    )
                    data = resp.json()
                    if "content" in data and data["content"]:
                        st.session_state.ai_tip = data["content"][0]["text"]
                    else:
                        st.session_state.ai_tip = L("default_tip")
                except Exception:
                    st.session_state.ai_tip = L("default_tip")

    # ── DOWNLOAD BUTTON ──
    with ab2:
        sub, da, ta, total_val = calc(
            st.session_state.inv_items, st.session_state.disc_pct, st.session_state.tax_pct
        )
        sym = get_cur_sym()

        rows_html = ""
        for it in st.session_state.inv_items:
            rt = max(it["qty"], 0) * max(it["rate"], 0)
            rows_html += (
                f"<tr><td>{it['desc'] or 'Service'}</td>"
                f"<td style='text-align:center'>{int(it['qty'])}</td>"
                f"<td style='text-align:right'>{sym}{int(it['rate']):,}</td>"
                f"<td style='text-align:right'>{sym}{int(rt):,}</td></tr>"
            )

        d_row = (f"<div class='ptrow' style='color:#e74c3c'><span>{L('discount_lbl')}</span>"
                 f"<span>-{sym}{int(da):,}</span></div>") if da > 0 else ""
        t_row = (f"<div class='ptrow'><span>{L('tax_lbl')}</span>"
                 f"<span>{sym}{int(ta):,}</span></div>") if ta > 0 else ""
        n_html = f"<div class='pnotes'>{st.session_state.notes}</div>" if st.session_state.notes else ""

        pdf_html = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'><title>Invoice {st.session_state.inv_num}</title>
<style>
body{{font-family:'Segoe UI',Arial,sans-serif;padding:30px;color:#111;max-width:720px;margin:0 auto}}
.pbrand{{font-size:22px;font-weight:800;color:#6c63ff}}
.pbrand-sub{{font-size:12px;color:#888;margin-top:2px}}
.pbrand-con{{font-size:11px;color:#999;margin-top:2px}}
.pbadge{{background:#6c63ff;color:#fff;padding:5px 14px;border-radius:22px;font-size:10px;font-weight:700}}
.phead{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px}}
.pmeta{{display:flex;justify-content:space-between;gap:14px;margin-bottom:16px}}
.ppty{{flex:1}}.ppty-lbl{{font-size:9px;color:#aaa;text-transform:uppercase;margin-bottom:3px}}
.ppty-name{{font-size:14px;font-weight:700}}.ppty-detail{{font-size:12px;color:#777}}
.pinfos{{display:grid;grid-template-columns:1fr 1fr;gap:6px;min-width:165px}}
.pinfo{{background:#f4f3ff;border-radius:7px;padding:6px 10px}}
.pinfo-lbl{{font-size:9px;color:#aaa}}.pinfo-val{{font-size:12px;font-weight:600}}
.pdiv{{border:none;border-top:1px solid #eee;margin:14px 0}}
.ptable{{width:100%;border-collapse:collapse;font-size:13px}}
.ptable th{{font-size:9px;color:#aaa;text-transform:uppercase;padding:5px 6px;border-bottom:1px solid #eee;text-align:left}}
.ptable td{{padding:8px 6px;border-bottom:.5px solid #f5f5f5}}
.ptable td:last-child,.ptable th:last-child{{text-align:right}}
.ptotals{{margin-left:auto;width:50%;margin-top:14px}}
.ptrow{{display:flex;justify-content:space-between;font-size:12px;color:#666;padding:3px 0}}
.ptrow.grand{{font-size:15px;font-weight:800;color:#111;border-top:2px solid #6c63ff;margin-top:8px;padding-top:8px}}
.pnotes{{font-size:11px;color:#666;background:#f9f9f9;padding:9px 12px;border-radius:7px;margin-top:14px;border-left:3px solid #6c63ff}}
.pfooter{{font-size:10px;color:#ccc;border-top:1px solid #eee;padding-top:9px;margin-top:14px;text-align:center}}
@media print{{body{{padding:10px}}}}
</style></head><body>
<div class='phead'>
  <div>
    <div class='pbrand'>{st.session_state.fname or 'Your Name'}</div>
    <div class='pbrand-sub'>{st.session_state.fservice or 'Service'}</div>
    <div class='pbrand-con'>{st.session_state.fcontact}</div>
  </div>
  <div class='pbadge'>{L('invoice_word')}</div>
</div>
<div class='pmeta'>
  <div class='ppty'>
    <div class='ppty-lbl'>{L('bill_to')}</div>
    <div class='ppty-name'>{st.session_state.cname or 'Client Name'}</div>
    <div class='ppty-detail'>{chosen_country}</div>
  </div>
  <div class='pinfos'>
    <div class='pinfo'><div class='pinfo-lbl'>{L('inv_num')}</div><div class='pinfo-val'>{st.session_state.inv_num}</div></div>
    <div class='pinfo'><div class='pinfo-lbl'>{L('issue_date')}</div><div class='pinfo-val'>{st.session_state.issue_date}</div></div>
    <div class='pinfo' style='grid-column:span 2'><div class='pinfo-lbl'>{L('due_date')}</div><div class='pinfo-val'>{st.session_state.due_date}</div></div>
  </div>
</div>
<hr class='pdiv'>
<table class='ptable'>
  <thead><tr>
    <th>{L('desc_col')}</th><th>{L('qty_col')}</th>
    <th style='text-align:right'>{L('rate_col')}</th>
    <th style='text-align:right'>{L('total_col')}</th>
  </tr></thead>
  <tbody>{rows_html}</tbody>
</table>
<div class='ptotals'>
  <div class='ptrow'><span>{L('subtotal')}</span><span>{sym}{int(sub):,}</span></div>
  {d_row}{t_row}
  <div class='ptrow grand'><span>{L('total_lbl')}</span><span>{sym}{int(total_val):,}</span></div>
</div>
{n_html}
<div class='pfooter'>{L('footer_txt')}</div>
</body></html>"""

        if PDF_SUPPORT:
            try:
                pdf_bytes = WeasyprintHTML(string=pdf_html).write_pdf()
                st.download_button(
                    label=L("pdf_btn"),
                    data=pdf_bytes,
                    file_name=f"invoice_{st.session_state.inv_num}.pdf",
                    mime="application/pdf",
                    key="btn_dl",
                )
            except Exception as e:
                st.download_button(
                    label="🖨 Download Invoice (HTML)",
                    data=pdf_html.encode("utf-8"),
                    file_name=f"invoice_{st.session_state.inv_num}.html",
                    mime="text/html",
                    key="btn_dl",
                )
        else:
            st.download_button(
                label="🖨 Download Invoice (HTML)",
                data=pdf_html.encode("utf-8"),
                file_name=f"invoice_{st.session_state.inv_num}.html",
                mime="text/html",
                key="btn_dl",
            )

    # AI TIP BOX
    if st.session_state.ai_tip:
        st.markdown(
            f"<div class='tipbox'>"
            f"<div class='tiplabel'>{L('ai_title')}</div>"
            f"<div class='tiptext'>{st.session_state.ai_tip}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# ══════════════════════════════
#  RIGHT — LIVE PREVIEW
# ══════════════════════════════
with right_col:
    sub, da, ta, total_val = calc(
        st.session_state.inv_items, st.session_state.disc_pct, st.session_state.tax_pct
    )
    sym = get_cur_sym()

    rows_prev = ""
    for it in st.session_state.inv_items:
        rt = max(it["qty"], 0) * max(it["rate"], 0)
        rows_prev += (
            f"<tr><td>{it['desc'] or 'Service'}</td>"
            f"<td style='text-align:center'>{int(it['qty'])}</td>"
            f"<td style='text-align:right'>{sym}{int(it['rate']):,}</td>"
            f"<td style='text-align:right'>{sym}{int(rt):,}</td></tr>"
        )

    d_row_p = (f"<div class='ptrow red'><span>{L('discount_lbl')}</span>"
               f"<span>-{sym}{int(da):,}</span></div>") if da > 0 else ""
    t_row_p = (f"<div class='ptrow'><span>{L('tax_lbl')}</span>"
               f"<span>{sym}{int(ta):,}</span></div>") if ta > 0 else ""
    notes_p = f"<div class='pnotes'>{st.session_state.notes}</div>" if st.session_state.notes else ""

    totals_block = f"""
  <div class='ptotals'>
    <div class='ptrow'><span>{L('subtotal')}</span><span>{sym}{int(sub):,}</span></div>
    {d_row_p}
    {t_row_p}
    <div class='ptrow grand'><span>{L('total_lbl')}</span><span>{sym}{int(total_val):,}</span></div>
  </div>"""

    dn = st.session_state.fname    or ("Your Name"   if st.session_state.lang == "en" else "آپ کا نام")
    ds = st.session_state.fservice or ("Service"     if st.session_state.lang == "en" else "سروس")
    dc = st.session_state.cname   or ("Client Name" if st.session_state.lang == "en" else "کلائنٹ نام")

    st.markdown(f"""
<div class='prev-label'><span class='dot'></span>{L('preview_title')}</div>
<div class='inv-card'>
  <div class='phead'>
    <div>
      <div class='pbrand'>{dn}</div>
      <div class='pbrand-sub'>{ds}</div>
      <div class='pbrand-con'>{st.session_state.fcontact}</div>
    </div>
    <div class='pbadge'>{L('invoice_word')}</div>
  </div>
  <div class='pmeta'>
    <div class='ppty'>
      <div class='ppty-lbl'>{L('bill_to')}</div>
      <div class='ppty-name'>{dc}</div>
      <div class='ppty-detail'>{chosen_country}</div>
    </div>
    <div class='pinfos'>
      <div class='pinfo'><div class='pinfo-lbl'>{L('inv_num')}</div><div class='pinfo-val'>{st.session_state.inv_num}</div></div>
      <div class='pinfo'><div class='pinfo-lbl'>{L('issue_date')}</div><div class='pinfo-val'>{st.session_state.issue_date}</div></div>
      <div class='pinfo' style='grid-column:span 2'><div class='pinfo-lbl'>{L('due_date')}</div><div class='pinfo-val'>{st.session_state.due_date}</div></div>
    </div>
  </div>
  <hr class='pdiv'>
  <table class='ptable'>
    <thead><tr>
      <th>{L('desc_col')}</th>
      <th>{L('qty_col')}</th>
      <th style='text-align:right'>{L('rate_col')}</th>
      <th style='text-align:right'>{L('total_col')}</th>
    </tr></thead>
    <tbody>{rows_prev}</tbody>
  </table>
  {totals_block}
  {notes_p}
  <div class='pfooter'>{L('footer_txt')}</div>
</div>
""", unsafe_allow_html=True)
