import streamlit as st
from datetime import date, timedelta
from io import BytesIO
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InvoicePro PK",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Language strings ──────────────────────────────────────────────────────────
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
        "desc": "Description",
        "qty": "Qty",
        "rate": "Rate",
        "total": "Total",
        "add_item": "＋ Add Item",
        "tax": "Tax %",
        "discount": "Discount %",
        "notes": "Notes / Bank Details",
        "ai_btn": "✨ Get AI Tips",
        "pdf_btn": "🖨 Save as PDF",
        "ai_title": "✨ AI Tips",
        "ai_wait": "Generating tips...",
        "preview_title": "📄 Live Invoice Preview",
        "bill_to": "Bill To",
        "invoice_word": "INVOICE",
        "subtotal": "Subtotal",
        "discount_lbl": "Discount",
        "tax_lbl": "Tax",
        "total_lbl": "TOTAL",
        "footer": "Generated with InvoicePro PK — Professional Freelance Invoicing",
        "ph_name": "Ali Hassan",
        "ph_service": "Web Developer",
        "ph_contact": "ali@gmail.com  |  0300-0000000",
        "ph_client": "ABC Company",
        "ph_notes": "Bank: HBL  |  Account: 12345678  |  Payment within 7 days",
        "ph_desc": "Service description",
        "ai_prompt": (
            "You are a Pakistani freelance invoice expert. "
            "Freelancer named {name} provides {serv}. "
            "Invoice is for {amt} {cur}, client is from {country}. "
            "Give 3 practical tips IN ENGLISH about: "
            "1) How to receive payment 2) Professional invoice tips 3) How to deal with the client. "
            "Be short, friendly, max 5 lines total."
        ),
        "delete": "🗑",
        "currency_options": {
            "PKR — Pakistani Rupee": "PKR",
            "USD — US Dollar": "USD",
            "AED — UAE Dirham": "AED",
            "GBP — British Pound": "GBP",
            "SAR — Saudi Riyal": "SAR",
        },
        "countries": ["Pakistan", "UAE", "USA", "UK", "Saudi Arabia", "Canada", "Australia"],
        "dir": "ltr",
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
        "desc": "تفصیل",
        "qty": "تعداد",
        "rate": "ریٹ",
        "total": "کل",
        "add_item": "＋ آئٹم شامل کریں",
        "tax": "ٹیکس %",
        "discount": "چھوٹ %",
        "notes": "نوٹس / بینک تفصیل",
        "ai_btn": "✨ AI مشورہ لیں",
        "pdf_btn": "🖨 PDF محفوظ کریں",
        "ai_title": "✨ AI کا مشورہ",
        "ai_wait": "تھوڑا انتظار کریں...",
        "preview_title": "📄 لائیو انوائس پریویو",
        "bill_to": "بل بھیجیں",
        "invoice_word": "INVOICE",
        "subtotal": "کل رقم",
        "discount_lbl": "چھوٹ",
        "tax_lbl": "ٹیکس",
        "total_lbl": "کل",
        "footer": "InvoicePro PK کے ساتھ بنایا گیا",
        "ph_name": "علی حسن",
        "ph_service": "ویب ڈویلپر",
        "ph_contact": "ali@gmail.com  |  0300-0000000",
        "ph_client": "ABC کمپنی",
        "ph_notes": "بینک: HBL  |  اکاونٹ: 12345678  |  7 دن میں ادائیگی",
        "ph_desc": "خدمت کی تفصیل",
        "ai_prompt": (
            "Tu ek Pakistani freelance expert hai. "
            "{name} naam ka freelancer {serv} karta hai. "
            "Invoice {amt} {cur} ki hai, client {country} se hai. "
            "URDU mein 3 practical tips do — payment lene ka tareeqa, professional invoice tips, aur client se deal karna. "
            "Short aur friendly raho, max 5 lines."
        ),
        "delete": "🗑",
        "currency_options": {
            "PKR — پاکستانی روپیہ": "PKR",
            "USD — امریکی ڈالر": "USD",
            "AED — درہم": "AED",
            "GBP — پاؤنڈ": "GBP",
            "SAR — سعودی ریال": "SAR",
        },
        "countries": ["پاکستان", "متحدہ عرب امارات", "امریکہ", "برطانیہ", "سعودی عرب", "کینیڈا", "آسٹریلیا"],
        "dir": "rtl",
    },
}

CURRENCY_SYMBOLS = {"PKR": "Rs. ", "USD": "$ ", "AED": "AED ", "GBP": "£", "SAR": "SAR "}

# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if "items" not in st.session_state:
        st.session_state.items = [{"desc": "", "qty": 1, "rate": 0.0}]
    if "ai_tip" not in st.session_state:
        st.session_state.ai_tip = ""
    if "from_name" not in st.session_state:
        st.session_state.from_name = ""
    if "from_service" not in st.session_state:
        st.session_state.from_service = ""
    if "from_contact" not in st.session_state:
        st.session_state.from_contact = ""
    if "client_name" not in st.session_state:
        st.session_state.client_name = ""
    if "client_country_idx" not in st.session_state:
        st.session_state.client_country_idx = 0
    if "inv_num" not in st.session_state:
        st.session_state.inv_num = "INV-001"
    if "currency_idx" not in st.session_state:
        st.session_state.currency_idx = 0
    if "issue_date" not in st.session_state:
        st.session_state.issue_date = date.today()
    if "due_date" not in st.session_state:
        st.session_state.due_date = date.today() + timedelta(days=7)
    if "tax_pct" not in st.session_state:
        st.session_state.tax_pct = 0.0
    if "disc_pct" not in st.session_state:
        st.session_state.disc_pct = 0.0
    if "notes" not in st.session_state:
        st.session_state.notes = ""

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
def T(key):
    return LANG[st.session_state.lang][key]

def fmt_money(n, cur):
    sym = CURRENCY_SYMBOLS.get(cur, cur + " ")
    return f"{sym}{int(round(n)):,}"

def calc_totals(items, disc_pct, tax_pct):
    sub = sum((it["qty"] or 1) * (it["rate"] or 0) for it in items)
    da = sub * disc_pct / 100
    after_disc = sub - da
    ta = after_disc * tax_pct / 100
    total = after_disc + ta
    return sub, da, ta, total

def get_currency_code():
    cur_opts = list(T("currency_options").values())
    return cur_opts[st.session_state.currency_idx]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── General ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
    color: #e5e5e5 !important;
    font-family: 'Segoe UI', Arial, sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #6c63ff; border-radius: 3px; }

/* ── Top Bar ── */
.topbar {
    background: #111;
    border-bottom: 2px solid #6c63ff;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
}
.logo-box {
    width: 38px; height: 38px;
    background: #6c63ff; border-radius: 9px;
    display: inline-flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 800; font-size: 16px;
    vertical-align: middle; margin-right: 10px;
}
.logo-name { font-size: 16px; font-weight: 700; color: #fff; display: inline; }
.logo-sub { font-size: 11px; color: #888; }

/* ── Guide steps ── */
.guide-bar {
    background: #161625;
    border-bottom: 1px solid #2a2a3a;
    padding: 10px 24px;
    display: flex;
    gap: 20px;
    overflow-x: auto;
    margin: 0 -1rem;
    flex-wrap: wrap;
}
.gstep { display: flex; align-items: center; gap: 8px; white-space: nowrap; }
.gnum {
    width: 24px; height: 24px;
    background: #6c63ff; border-radius: 50%;
    color: #fff; font-size: 11px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
}
.gtxt { color: #bbb; font-size: 12px; }

/* ── Section labels ── */
.slabel {
    font-size: 10px; font-weight: 700; color: #a78bfa;
    text-transform: uppercase; letter-spacing: .1em;
    border-left: 3px solid #6c63ff; padding-left: 8px;
    margin: 10px 0 4px 0; display: block;
}

/* ── Streamlit inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
div[data-baseweb="select"] > div {
    background: #1e1e1e !important;
    border: 1.5px solid #3a3a3a !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #6c63ff !important;
    background: #1a1a2e !important;
}
div[data-baseweb="select"] * { color: #fff !important; }
[data-testid="stDateInput"] input {
    background: #1e1e1e !important;
    border: 1.5px solid #3a3a3a !important;
    color: #fff !important;
    border-radius: 8px !important;
}

/* ── Streamlit labels ── */
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stDateInput"] label {
    color: #aaa !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    border-radius: 9px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 12px !important;
    transition: all .2s !important;
    border: none !important;
}
.btn-ai > button {
    background: #6c63ff !important;
    color: #fff !important;
    border: 2px solid #8b85ff !important;
}
.btn-ai > button:hover { background: #7c73ff !important; transform: translateY(-1px); }
.btn-pdf > button {
    background: #e67e22 !important;
    color: #fff !important;
    border: 2px solid #f39c12 !important;
}
.btn-pdf > button:hover { background: #f39c12 !important; }
.btn-add > button {
    background: #1a2a1a !important;
    color: #2ecc71 !important;
    border: 2px solid #2ecc71 !important;
}
.btn-add > button:hover { background: #2ecc71 !important; color: #000 !important; }
.btn-del > button {
    background: #3a1010 !important;
    color: #ff6b6b !important;
    border: 1.5px solid #cc3333 !important;
    border-radius: 7px !important;
    padding: 4px 8px !important;
    font-size: 13px !important;
    min-height: unset !important;
    width: auto !important;
}
.btn-del > button:hover { background: #cc3333 !important; color: #fff !important; }

/* ── AI Tip Box ── */
.tipbox {
    background: #1a1030;
    border: 2px solid #6c63ff;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 12px;
}
.tiplabel {
    font-size: 11px; color: #a78bfa; font-weight: 700;
    text-transform: uppercase; letter-spacing: .07em; margin-bottom: 8px;
}
.tiptext { font-size: 13px; color: #ddd; line-height: 1.7; white-space: pre-wrap; }

/* ── Invoice Preview Card ── */
.inv-card {
    background: #fff;
    border-radius: 12px;
    padding: 28px;
    color: #111;
    box-shadow: 0 4px 24px rgba(108,99,255,.15);
    font-family: 'Segoe UI', Arial, sans-serif;
}
.phead { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
.pbrand { font-size: 21px; font-weight: 800; color: #6c63ff; }
.pbrand-sub { font-size: 12px; color: #888; margin-top: 2px; }
.pbrand-con { font-size: 11px; color: #999; margin-top: 2px; }
.pbadge {
    background: #6c63ff; color: #fff;
    font-size: 10px; font-weight: 700;
    padding: 5px 14px; border-radius: 22px; letter-spacing: .07em;
}
.pmeta { display: flex; justify-content: space-between; gap: 14px; margin-bottom: 16px; }
.ppty-lbl { font-size: 9px; color: #aaa; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 3px; }
.ppty-name { font-size: 14px; font-weight: 700; color: #111; }
.ppty-detail { font-size: 12px; color: #777; }
.pinfos { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; min-width: 165px; }
.pinfo { background: #f4f3ff; border-radius: 7px; padding: 6px 10px; }
.pinfo-lbl { font-size: 9px; color: #aaa; }
.pinfo-val { font-size: 12px; font-weight: 600; color: #333; }
.pdiv { border: none; border-top: 1px solid #eee; margin: 14px 0; }
.ptable { width: 100%; border-collapse: collapse; font-size: 12px; }
.ptable th {
    font-size: 9px; color: #aaa; text-transform: uppercase;
    padding: 4px 6px; border-bottom: 1px solid #eee;
    text-align: left; letter-spacing: .05em;
}
.ptable td { padding: 7px 6px; border-bottom: .5px solid #f5f5f5; color: #444; }
.ptable td:last-child, .ptable th:last-child { text-align: right; }
.ptotals { margin-left: auto; width: 52%; margin-top: 12px; }
.ptrow { display: flex; justify-content: space-between; font-size: 12px; color: #666; padding: 3px 0; }
.ptrow.grand {
    font-size: 15px; font-weight: 800; color: #111;
    border-top: 2px solid #6c63ff; margin-top: 8px; padding-top: 8px;
}
.ptrow.red { color: #e74c3c; }
.pnotes {
    font-size: 11px; color: #666; background: #f9f9f9;
    border-radius: 7px; padding: 9px 12px; margin-top: 12px;
    border-left: 3px solid #6c63ff;
}
.pfooter {
    margin-top: 14px; font-size: 10px; color: #ccc;
    border-top: 1px solid #eee; padding-top: 9px; text-align: center;
}
/* ── Form section background ── */
[data-testid="column"]:first-child {
    background: #141414;
    border-right: 1px solid #2a2a2a;
    padding: 16px 20px !important;
}
[data-testid="column"]:last-child {
    background: #0f0f0f;
    padding: 16px 20px !important;
}
/* ── Divider ── */
hr { border-color: #2a2a2a !important; }

/* ── Reduce streamlit spacing ── */
.block-container { padding: 0 1rem !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] > div { margin-bottom: 0 !important; }
div.row-widget.stButton { margin-bottom: 4px; }
[data-testid="stNumberInput"] { margin-bottom: 4px; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: #e67e22 !important;
    color: #fff !important;
    border: 2px solid #f39c12 !important;
    width: 100% !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top Bar ───────────────────────────────────────────────────────────────────
other_lang = "ur" if st.session_state.lang == "en" else "en"
other_lang_label = T("lang_btn")

st.markdown(f"""
<div class="topbar">
  <div>
    <span class="logo-box">IP</span>
    <span class="logo-name">{T('title')}</span>
    <div class="logo-sub" style="padding-left:48px">{T('subtitle')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Language toggle (rendered after topbar div, floated via column trick)
_, lang_col = st.columns([5, 1])
with lang_col:
    if st.button(other_lang_label, key="lang_toggle"):
        st.session_state.lang = other_lang
        st.rerun()

# ── Guide Steps ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="guide-bar">
  <div class="gstep"><div class="gnum">1</div><div class="gtxt">{T('step1')}</div></div>
  <div class="gstep"><div class="gnum">2</div><div class="gtxt">{T('step2')}</div></div>
  <div class="gstep"><div class="gnum">3</div><div class="gtxt">{T('step3')}</div></div>
  <div class="gstep"><div class="gnum">4</div><div class="gtxt">{T('step4')}</div></div>
  <div class="gstep"><div class="gnum">5</div><div class="gtxt">{T('step5')}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="small")

# ══════════════════════ LEFT FORM ═════════════════════════════════════════════
with left_col:

    # ── Your Info ──
    st.markdown(f"<span class='slabel'>{T('your_info')}</span>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.from_name = st.text_input(
            T("your_name"), value=st.session_state.from_name,
            placeholder=T("ph_name"), key="inp_fname"
        )
    with c2:
        st.session_state.from_service = st.text_input(
            T("your_service"), value=st.session_state.from_service,
            placeholder=T("ph_service"), key="inp_fserv"
        )
    st.session_state.from_contact = st.text_input(
        T("your_contact"), value=st.session_state.from_contact,
        placeholder=T("ph_contact"), key="inp_fcon"
    )

    # ── Client Info ──
    st.markdown(f"<span class='slabel'>{T('client_info')}</span>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.client_name = st.text_input(
            T("client_name"), value=st.session_state.client_name,
            placeholder=T("ph_client"), key="inp_cname"
        )
    with c2:
        countries = T("countries")
        idx = st.session_state.client_country_idx
        if idx >= len(countries):
            idx = 0
        chosen_country = st.selectbox(
            T("client_country"), options=countries, index=idx, key="sel_country"
        )
        st.session_state.client_country_idx = countries.index(chosen_country)

    # ── Invoice Details ──
    st.markdown(f"<span class='slabel'>{T('inv_details')}</span>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.inv_num = st.text_input(
            T("inv_num"), value=st.session_state.inv_num, key="inp_invnum"
        )
    with c2:
        cur_opts = list(T("currency_options").keys())
        idx = st.session_state.currency_idx
        if idx >= len(cur_opts):
            idx = 0
        chosen_cur_label = st.selectbox(
            T("currency"), options=cur_opts, index=idx, key="sel_currency"
        )
        st.session_state.currency_idx = cur_opts.index(chosen_cur_label)

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.issue_date = st.date_input(
            T("issue_date"), value=st.session_state.issue_date, key="inp_idate"
        )
    with c2:
        st.session_state.due_date = st.date_input(
            T("due_date"), value=st.session_state.due_date, key="inp_ddate"
        )

    # ── Services / Items ──
    st.markdown(f"<span class='slabel'>{T('services')}</span>", unsafe_allow_html=True)

    # Header row
    hc1, hc2, hc3, hc4 = st.columns([3, 1, 1.5, 0.6])
    hc1.markdown(f"<div style='font-size:10px;color:#666;font-weight:600;text-transform:uppercase'>{T('desc')}</div>", unsafe_allow_html=True)
    hc2.markdown(f"<div style='font-size:10px;color:#666;font-weight:600;text-transform:uppercase'>{T('qty')}</div>", unsafe_allow_html=True)
    hc3.markdown(f"<div style='font-size:10px;color:#666;font-weight:600;text-transform:uppercase'>{T('rate')}</div>", unsafe_allow_html=True)

    items_to_delete = []
for i, item in enumerate(st.session_state["items"]):
    ic1, ic2, ic3, ic4 = st.columns([3, 1, 1.5, 0.6])
    with ic1:
            new_desc = st.text_input(
                "desc", value=item["desc"],
                placeholder=T("ph_desc"),
                label_visibility="collapsed",
                key=f"item_desc_{i}"
            )
            st.session_state.items[i]["desc"] = new_desc
        with ic2:
            new_qty = st.number_input(
                "qty", value=float(item["qty"]),
                min_value=0.0, step=1.0,
                label_visibility="collapsed",
                key=f"item_qty_{i}"
            )
            st.session_state.items[i]["qty"] = new_qty
        with ic3:
            new_rate = st.number_input(
                "rate", value=float(item["rate"]),
                min_value=0.0, step=100.0,
                label_visibility="collapsed",
                key=f"item_rate_{i}"
            )
            st.session_state.items[i]["rate"] = new_rate
        with ic4:
            st.markdown("<div class='btn-del'>", unsafe_allow_html=True)
            if st.button("🗑", key=f"del_{i}"):
                items_to_delete.append(i)
            st.markdown("</div>", unsafe_allow_html=True)

    # Process deletions
    if items_to_delete:
        for idx in sorted(items_to_delete, reverse=True):
            if len(st.session_state.items) > 1:
                st.session_state.items.pop(idx)
        st.rerun()

    st.markdown("<div class='btn-add'>", unsafe_allow_html=True)
    if st.button(T("add_item"), key="add_item_btn"):
        st.session_state.items.append({"desc": "", "qty": 1, "rate": 0.0})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tax & Discount ──
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.tax_pct = st.number_input(
            T("tax"), value=st.session_state.tax_pct,
            min_value=0.0, max_value=100.0, step=1.0, key="inp_tax"
        )
    with c2:
        st.session_state.disc_pct = st.number_input(
            T("discount"), value=st.session_state.disc_pct,
            min_value=0.0, max_value=100.0, step=1.0, key="inp_disc"
        )

    # ── Notes ──
    st.session_state.notes = st.text_area(
        T("notes"), value=st.session_state.notes,
        placeholder=T("ph_notes"), height=80, key="inp_notes"
    )

    # ── Action Buttons ──
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)

    # AI Tips Button
    with b1:
        st.markdown("<div class='btn-ai'>", unsafe_allow_html=True)
        if st.button(T("ai_btn"), key="ai_btn"):
            cur_code = get_currency_code()
            sub, _, _, _ = calc_totals(
                st.session_state.items,
                st.session_state.disc_pct,
                st.session_state.tax_pct
            )
            prompt = T("ai_prompt").format(
                name=st.session_state.from_name or "Freelancer",
                serv=st.session_state.from_service or "services",
                amt=int(round(sub)),
                cur=cur_code,
                country=chosen_country,
            )
            try:
                client = anthropic.Anthropic()
                with st.spinner(T("ai_wait")):
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                st.session_state.ai_tip = response.content[0].text
            except Exception as e:
                if st.session_state.lang == "en":
                    st.session_state.ai_tip = "Tip: Always include clear payment terms in your invoice. A 7-day deadline helps clients pay faster!"
                else:
                    st.session_state.ai_tip = "مشورہ: ہر انوائس میں payment کی آخری تاریخ ضرور لکھیں۔ 7 دن کی deadline سے clients جلدی ادائیگی کرتے ہیں!"
        st.markdown("</div>", unsafe_allow_html=True)

    # PDF / Print button using HTML generation + download
    with b2:
        cur_code = get_currency_code()
        cur_sym = CURRENCY_SYMBOLS.get(cur_code, cur_code + " ")
        sub, da, ta, total = calc_totals(
            st.session_state.items, st.session_state.disc_pct, st.session_state.tax_pct
        )

        # Build items rows HTML
        items_html = ""
        for it in st.session_state.items:
            row_total = (it["qty"] or 1) * (it["rate"] or 0)
            items_html += f"""
            <tr>
              <td>{it['desc'] or 'Service'}</td>
              <td style='text-align:center'>{int(it['qty'])}</td>
              <td style='text-align:right'>{cur_sym}{int(it['rate']):,}</td>
              <td style='text-align:right'>{cur_sym}{int(row_total):,}</td>
            </tr>"""

        disc_row = f"<div class='ptrow' style='color:#e74c3c'><span>{T('discount_lbl')}</span><span>-{cur_sym}{int(da):,}</span></div>" if da > 0 else ""
        tax_row = f"<div class='ptrow'><span>{T('tax_lbl')}</span><span>{cur_sym}{int(ta):,}</span></div>" if ta > 0 else ""
        notes_html = f"<div class='pnotes'>{st.session_state.notes}</div>" if st.session_state.notes else ""

        pdf_html = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'>
<title>Invoice {st.session_state.inv_num}</title>
<style>
body{{font-family:'Segoe UI',Arial,sans-serif;padding:30px;color:#111;max-width:720px;margin:0 auto}}
.pbrand{{font-size:22px;font-weight:800;color:#6c63ff}}
.pbrand-sub{{font-size:12px;color:#888;margin-top:2px}}
.pbrand-con{{font-size:11px;color:#999;margin-top:2px}}
.pbadge{{background:#6c63ff;color:#fff;padding:5px 14px;border-radius:22px;font-size:10px;font-weight:700;letter-spacing:.07em}}
.phead{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px}}
.pmeta{{display:flex;justify-content:space-between;gap:14px;margin-bottom:16px}}
.ppty{{flex:1}}
.ppty-lbl{{font-size:9px;color:#aaa;text-transform:uppercase;letter-spacing:.08em;margin-bottom:3px}}
.ppty-name{{font-size:14px;font-weight:700}}
.ppty-detail{{font-size:12px;color:#777}}
.pinfos{{display:grid;grid-template-columns:1fr 1fr;gap:6px;min-width:165px}}
.pinfo{{background:#f4f3ff;border-radius:7px;padding:6px 10px}}
.pinfo-lbl{{font-size:9px;color:#aaa}}
.pinfo-val{{font-size:12px;font-weight:600}}
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
    <div class='pbrand'>{st.session_state.from_name or 'Your Name'}</div>
    <div class='pbrand-sub'>{st.session_state.from_service or 'Service'}</div>
    <div class='pbrand-con'>{st.session_state.from_contact}</div>
  </div>
  <div class='pbadge'>{T('invoice_word')}</div>
</div>
<div class='pmeta'>
  <div class='ppty'>
    <div class='ppty-lbl'>{T('bill_to')}</div>
    <div class='ppty-name'>{st.session_state.client_name or 'Client Name'}</div>
    <div class='ppty-detail'>{chosen_country}</div>
  </div>
  <div class='pinfos'>
    <div class='pinfo'><div class='pinfo-lbl'>{T('inv_num')}</div><div class='pinfo-val'>{st.session_state.inv_num}</div></div>
    <div class='pinfo'><div class='pinfo-lbl'>{T('issue_date')}</div><div class='pinfo-val'>{st.session_state.issue_date}</div></div>
    <div class='pinfo' style='grid-column:span 2'><div class='pinfo-lbl'>{T('due_date')}</div><div class='pinfo-val'>{st.session_state.due_date}</div></div>
  </div>
</div>
<hr class='pdiv'>
<table class='ptable'>
  <thead><tr>
    <th>{T('desc')}</th>
    <th>{T('qty')}</th>
    <th style='text-align:right'>{T('rate')}</th>
    <th style='text-align:right'>{T('total')}</th>
  </tr></thead>
  <tbody>{items_html}</tbody>
</table>
<div class='ptotals'>
  <div class='ptrow'><span>{T('subtotal')}</span><span>{cur_sym}{int(sub):,}</span></div>
  {disc_row}
  {tax_row}
  <div class='ptrow grand'><span>{T('total_lbl')}</span><span>{cur_sym}{int(total):,}</span></div>
</div>
{notes_html}
<div class='pfooter'>{T('footer')}</div>
</body></html>"""

        st.download_button(
            label=T("pdf_btn"),
            data=pdf_html.encode("utf-8"),
            file_name=f"invoice_{st.session_state.inv_num}.html",
            mime="text/html",
            key="download_pdf"
        )

    # ── AI Tip Display ──
    if st.session_state.ai_tip:
        st.markdown(f"""
        <div class='tipbox'>
          <div class='tiplabel'>{T('ai_title')}</div>
          <div class='tiptext'>{st.session_state.ai_tip}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════ RIGHT PREVIEW ═════════════════════════════════════════
with right_col:
    st.markdown(f"<div style='font-size:12px;color:#888;margin-bottom:12px;display:flex;align-items:center;gap:7px'><span style='width:8px;height:8px;background:#6c63ff;border-radius:50%;display:inline-block'></span>{T('preview_title')}</div>", unsafe_allow_html=True)

    cur_code = get_currency_code()
    cur_sym = CURRENCY_SYMBOLS.get(cur_code, cur_code + " ")

    sub, da, ta, total = calc_totals(
        st.session_state.items, st.session_state.disc_pct, st.session_state.tax_pct
    )

    # Build items rows
    items_rows = ""
    for it in st.session_state.items:
        row_total = (it["qty"] or 1) * (it["rate"] or 0)
        items_rows += f"""
        <tr>
          <td>{it['desc'] or 'Service'}</td>
          <td style='text-align:center'>{int(it['qty'])}</td>
          <td style='text-align:right'>{cur_sym}{int(it['rate']):,}</td>
          <td style='text-align:right'>{cur_sym}{int(row_total):,}</td>
        </tr>"""

    disc_row_prev = f"<div class='ptrow red'><span>{T('discount_lbl')}</span><span>-{cur_sym}{int(da):,}</span></div>" if da > 0 else ""
    tax_row_prev = f"<div class='ptrow'><span>{T('tax_lbl')}</span><span>{cur_sym}{int(ta):,}</span></div>" if ta > 0 else ""
    notes_prev = f"<div class='pnotes'>{st.session_state.notes}</div>" if st.session_state.notes else ""

    preview_html = f"""
    <div class='inv-card'>
      <div class='phead'>
        <div>
          <div class='pbrand'>{st.session_state.from_name or ('Aap Ka Naam' if st.session_state.lang == 'en' else 'آپ کا نام')}</div>
          <div class='pbrand-sub'>{st.session_state.from_service or ('Service' if st.session_state.lang == 'en' else 'سروس')}</div>
          <div class='pbrand-con'>{st.session_state.from_contact}</div>
        </div>
        <div class='pbadge'>{T('invoice_word')}</div>
      </div>
      <div class='pmeta'>
        <div class='ppty'>
          <div class='ppty-lbl'>{T('bill_to')}</div>
          <div class='ppty-name'>{st.session_state.client_name or ('Client Ka Naam' if st.session_state.lang == 'en' else 'کلائنٹ نام')}</div>
          <div class='ppty-detail'>{chosen_country}</div>
        </div>
        <div class='pinfos'>
          <div class='pinfo'><div class='pinfo-lbl'>{T('inv_num')}</div><div class='pinfo-val'>{st.session_state.inv_num}</div></div>
          <div class='pinfo'><div class='pinfo-lbl'>{T('issue_date')}</div><div class='pinfo-val'>{st.session_state.issue_date}</div></div>
          <div class='pinfo' style='grid-column:span 2'><div class='pinfo-lbl'>{T('due_date')}</div><div class='pinfo-val'>{st.session_state.due_date}</div></div>
        </div>
      </div>
      <hr class='pdiv'>
      <table class='ptable'>
        <thead><tr>
          <th>{T('desc')}</th>
          <th>{T('qty')}</th>
          <th style='text-align:right'>{T('rate')}</th>
          <th style='text-align:right'>{T('total')}</th>
        </tr></thead>
        <tbody>{items_rows}</tbody>
      </table>
      <div class='ptotals'>
        <div class='ptrow'><span>{T('subtotal')}</span><span>{cur_sym}{int(sub):,}</span></div>
        {disc_row_prev}
        {tax_row_prev}
        <div class='ptrow grand'><span>{T('total_lbl')}</span><span>{cur_sym}{int(total):,}</span></div>
      </div>
      {notes_prev}
      <div class='pfooter'>{T('footer')}</div>
    </div>
    """

    st.markdown(preview_html, unsafe_allow_html=True)
