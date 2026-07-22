import streamlit as st


def render_sources(sources):
    if not sources:
        return

    st.markdown("### Sources")

    for source in sources:
        st.markdown(
            f"📄 {source['document_name']} — Page {source['page']}"
        )