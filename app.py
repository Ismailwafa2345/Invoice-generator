import streamlit as st
from datetime import date, timedelta

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
        "pdf_btn": "🖨 Save as HTML/PDF",
        "ai_title": "✨ AI Tips",
        "ai_wait": "Generating tips...",
        "preview_title": "📄 Live Invoice Preview",
        "bill_to": "Bill To",
        "invoice_word": "INVOICE",
        "subtotal": "Subtotal",
        "discount_lbl": "Discount",
        "tax_lbl": "Tax",
        "total_lbl": "TOTAL",
        "footer": "Generated with InvoicePro PK",
        "ph_name": "Ali Hassan",
        "ph_service": "Web Developer",
        "ph_contact": "ali@gmail.com | 0300-0000000",
        "ph_client": "ABC Company",
        "ph_notes": "Bank: HBL | Account: 12345678",
        "ph_desc": "Service description",
        "ai_prompt": "You are a Pakistani freelance expert. {name} provides {serv}. Invoice {amt} {cur}, client from {country}. Give 3 short tips.",
        "countries": ["Pakistan", "UAE", "USA", "UK", "Saudi Arabia", "Canada", "Australia"],
        "currency_options": {"PKR": "PKR", "USD": "USD", "AED": "AED", "GBP": "GBP", "SAR": "SAR"},
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
        "ph_contact": "ali@gmail.com | 0300-0000000",
        "ph_client": "ABC کمپنی",
        "ph_notes": "بینک: HBL | اکاونٹ: 12345678",
        "ph_desc": "خدمت کی تفصیل",
        "ai_prompt": "Tu ek Pakistani freelance expert hai. {name} ka invoice {amt} {cur} ka hai. Urdu mein 3 mashwaray do.",
        "countries": ["پاکستان", "متحدہ عرب امارات", "امریکہ", "برطانیہ", "سعودی عرب", "کینیڈا", "آسٹریلیا"],
        "currency_options": {"PKR": "PKR", "USD": "USD", "AED": "AED", "GBP": "GBP", "SAR": "SAR"},
    }
}

CURRENCY_SYMBOLS = {"PKR": "Rs. ", "USD": "$ ", "AED": "AED ", "GBP": "£", "SAR": "SAR "}

# ── Session state init ────────────────────────────────────────────────────────
if "lang" not in st.session_state: st.session_state.lang = "en"
if "items" not in st.session_state: st.session_state.items = [{"desc": "", "qty": 1, "rate": 0.0}]
if "ai_tip" not in st.session_state: st.session_state.ai_tip = ""

# ── Helpers ───────────────────────────────────────────────────────────────────
def T(key): return LANG[st.session_state.lang][key]

def calc_totals():
    sub = sum(it["qty"] * it["rate"] for it in st.session_state.items)
    tax_amt = sub * (st.session_state.get("tax_pct", 0) / 100)
    disc_amt = sub * (st.session_state.get("disc_pct", 0) / 100)
    total = sub + tax_amt - disc_amt
    return sub, disc_amt, tax_amt, total

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .inv-card { background: white; color: black; padding: 30px; border-radius: 10px; }
    .slabel { color: #6c63ff; font-weight: bold; font-size: 14px; display: block; margin-top: 20px; }
    .btn-add button { background-color: #2ecc71 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar / Top Bar ──────────────────────────────────────────────────────────
col1, col2 = st.columns([5,1])
with col1:
    st.title(T("title"))
with col2:
    if st.button(T("lang_btn")):
        st.session_state.lang = "ur" if st.session_state.lang == "en" else "en"
        st.rerun()

# ── Main UI ───────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown(f"<span class='slabel'>{T('your_info')}</span>", unsafe_allow_html=True)
    f_name = st.text_input(T("your_name"), placeholder=T("ph_name"))
    f_serv = st.text_input(T("your_service"), placeholder=T("ph_service"))
    f_cont = st.text_input(T("your_contact"), placeholder=T("ph_contact"))

    st.markdown(f"<span class='slabel'>{T('client_info')}</span>", unsafe_allow_html=True)
    c_name = st.text_input(T("client_name"), placeholder=T("ph_client"))
    c_country = st.selectbox(T("client_country"), T("countries"))

    st.markdown(f"<span class='slabel'>{T('services')}</span>", unsafe_allow_html=True)
    
    for i, item in enumerate(st.session_state.items):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 0.5])
        st.session_state.items[i]["desc"] = c1.text_input(f"Desc {i}", value=item["desc"], label_visibility="collapsed", key=f"d_{i}")
        st.session_state.items[i]["qty"] = c2.number_input(f"Qty {i}", value=float(item["qty"]), step=1.0, label_visibility="collapsed", key=f"q_{i}")
        st.session_state.items[i]["rate"] = c3.number_input(f"Rate {i}", value=float(item["rate"]), step=10.0, label_visibility="collapsed", key=f"r_{i}")
        if c4.button("🗑", key=f"del_{i}"):
            if len(st.session_state.items) > 1:
                st.session_state.items.pop(i)
                st.rerun()

    if st.button(T("add_item")):
        st.session_state.items.append({"desc": "", "qty": 1, "rate": 0.0})
        st.rerun()

    st.session_state.tax_pct = st.number_input(T("tax"), 0.0, 100.0, 0.0)
    st.session_state.disc_pct = st.number_input(T("discount"), 0.0, 100.0, 0.0)
    notes = st.text_area(T("notes"), placeholder=T("ph_notes"))

with right:
    st.subheader(T("preview_title"))
    sub, disc, tax, total = calc_totals()
    
    # Simple Preview Card
    st.markdown(f"""
    <div class="inv-card">
        <h2 style="color:#6c63ff">{f_name or 'Your Name'}</h2>
        <p>{f_serv or 'Service'}<br>{f_cont}</p>
        <hr>
        <p><b>Bill To:</b> {c_name or 'Client Name'} ({c_country})</p>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background:#f4f4f4"><th>Desc</th><th>Qty</th><th>Total</th></tr>
            {"".join([f"<tr><td>{it['desc']}</td><td>{it['qty']}</td><td>{it['qty']*it['rate']}</td></tr>" for it in st.session_state.items])}
        </table>
        <hr>
        <p align="right">Subtotal: {sub}<br>Tax: {tax}<br>Discount: {disc}<br><b>Total: {total}</b></p>
        <p style="font-size:10px; color:gray">{notes}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(T("ai_btn")):
        st.session_state.ai_tip = "Tip: Use a clear bank name and IBAN for international payments."
        st.info(st.session_state.ai_tip)

    st.download_button("Download Invoice", "Dummy Content", "invoice.html")
