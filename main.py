import streamlit as st
import tempfile
import os

from helper import get_answer, vectorstore

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0f172a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Main Container */
.main .block-container {
    max-width: 900px;
    padding-top: 1rem;
}

/* User Bubble */
.user-message {
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px 0;
    width: fit-content;
    max-width: 75%;
    margin-left: auto;
    word-wrap: break-word;
}

/* Assistant Bubble */
.assistant-message {
    background: #1e293b;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 10px 0;
    width: fit-content;
    max-width: 75%;
    margin-right: auto;
    word-wrap: break-word;
}

/* Hide Streamlit Branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# =========================
# PDF UPLOAD FUNCTION
# =========================

def upload_pdf(uploaded_files):

    for uploaded_file in uploaded_files:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(
                uploaded_file.getvalue()
            )

            temp_path = tmp_file.name

        try:

            vectorstore.add_documents(
                temp_path
            )

        except Exception as e:

            st.error(
                f"Error processing {uploaded_file.name}: {e}"
            )

        finally:

            if os.path.exists(temp_path):
                os.remove(temp_path)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🤖 AI Assistant")

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        with st.spinner(
            "Indexing PDFs..."
        ):

            upload_pdf(
                uploaded_files
            )

        st.session_state.uploaded_files = [
            file.name
            for file in uploaded_files
        ]

        st.success(
            "PDFs indexed successfully."
        )

    if st.session_state.uploaded_files:

        st.markdown("### Uploaded PDFs")

        for file in st.session_state.uploaded_files:

            st.write(f"📄 {file}")

    st.divider()

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

# =========================
# MAIN PAGE
# =========================

st.title("💬 Chat Assistant")

# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-message">
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input(
    "Message Assistant..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.rerun()

# =========================
# GENERATE ANSWER
# =========================

if (
    len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):

    question = st.session_state.messages[-1]["content"]

    with st.spinner("Thinking..."):

        try:

            answer = get_answer(
                question
            )

        except Exception as e:

            answer = f"Error: {str(e)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()