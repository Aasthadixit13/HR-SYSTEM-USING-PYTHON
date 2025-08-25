import streamlit as st
from pypdf import PdfReader

# ---------------- Leave Manager ----------------
# Initialize leave data in session state for persistence
if "leaves" not in st.session_state:
    st.session_state.leaves = {"total": 20, "used": 0}

# ---------------- Streamlit UI -----------------
st.title("🧑‍💼 Simple HR System")

# --- Upload PDF ---
st.header("📄 Upload HR Policy PDF")
pdf = st.file_uploader("Upload PDF", type=["pdf"])
pdf_text = ""
if pdf:
    reader = PdfReader(pdf)
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
    st.success("PDF uploaded and text extracted!")

# --- Ask Question (very simple search) ---
st.header("💬 HR Chatbot")
q = st.text_input("Ask a question about the PDF")
if q and pdf_text:
    if q.lower() in pdf_text.lower():
        st.write("✅ Found in policy document!")
    else:
        st.write("❌ Not found in document.")

# --- Leave Manager ---
st.header("🗓️ Leave Balance Tracker")
leaves = st.session_state.leaves
st.write(f"Total: {leaves['total']}, Used: {leaves['used']}, Remaining: {leaves['total']-leaves['used']}")

apply = st.number_input("Apply Leave Days", min_value=0, max_value=leaves["total"])
if st.button("Apply Leave"):
    if apply <= (leaves["total"] - leaves["used"]):
        leaves["used"] += apply
        st.success(f"Leave approved! Remaining: {leaves['total']-leaves['used']}")
    else:
        st.error("Not enough remaining leaves!")
