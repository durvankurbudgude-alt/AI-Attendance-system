import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="
            background:white;
            border-left: 8px solid #EB459E;
            padding:25px;
            border-radius:20px;
            border:1px solid black;
            margin-bottom:20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        ">
            <h3 style="
                margin:0;
                color:#1e293b;
                font-size:1.5rem;
                font-weight:700;
            ">
                {name}
            </h3>

            <p style="
                color:#475569;
                margin:10px 0 18px 0;
                font-size:1rem;
            ">
                Code :
                <span style="
                    background:#E0E3FF;
                    color:#5865F2;
                    padding:3px 10px;
                    border-radius:6px;
                    font-weight:600;
                ">
                    {code}
                </span>
                | Section : {section}
            </p>
    """

    if stats:
        html += """
            <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:8px;">
        """

        for icon, label, value in stats:
            html += f"""
                <div style="
                    background:#F8E8F1;
                    padding:10px 14px;
                    border-radius:12px;
                    font-size:1rem;
                    border:1px solid #f1c4dc;
                    display:flex;
                    align-items:center;
                    gap:8px;
                    color:#1e293b;
                    font-weight:500;
                ">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <span style="color:#334155;">{label}:</span>
                    <span style="
                        color:#7C3AED;
                        font-weight:800;
                        font-size:1.05rem;
                    ">
                        {value}
                    </span>
                </div>
            """

        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
