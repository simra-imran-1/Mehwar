"""Scoped presentation styles for the MEHWAR evidence workspace."""

WORKSPACE_CSS = """
<style>
/* A fixed visual system, independent of the browser's light/dark preference.
   Scope native overrides to Streamlit test IDs and keyed containers. */
.stApp { background: #f3f5f5; color: #172d3b; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"] { display: none; }
.stMainBlockContainer { padding: 2.8rem 3rem 3rem; max-width: 1800px; }
[data-testid="stMain"] [data-testid="stMarkdownContainer"] { color: #172d3b; }
[data-testid="stMain"] [data-testid="stCaptionContainer"] { color: #546974; }
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 { color: #172d3b; }
[data-testid="stMain"] a { color: #2458a6; }
[data-testid="stSidebar"] {
    background: #152d3b; border-right: 1px solid #28414e;
}
[data-testid="stSidebarContent"] { padding-top: 2.2rem; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] label, [data-testid="stSidebar"] h2 {
    color: #e5edef;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #a7b9c3; }
[data-testid="stSidebar"] h2 {
    font-size: 15px; font-weight: 600; letter-spacing: .02em; margin: 18px 0 8px;
}
.mw-rail-brand {
    border-top: 3px solid #8eafbc; padding-top: 16px; margin-bottom: 26px;
    font-size: 12px; letter-spacing: .18em; color: #adc5d0;
}
.mw-rail-brand strong {
    display: block; font-size: 21px; letter-spacing: .015em;
    font-weight: 500; color: #f2f6f7; margin-top: 7px;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"] {
    padding: 12px 10px; border: 1px solid #314955; border-radius: 7px;
    margin: 4px 0; background: #1b3442; width: 100%;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"],
[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) {
    background: #2b4858; border-color: #99b9cc;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"] p {
    font-size: 13px; line-height: 1.5;
}
[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100%; min-height: 44px; background: #203d4d; color: #e8f0f4;
    border: 1px solid #557180; border-radius: 6px;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
    background: #dbe9ee; color: #122b39; border-color: #dbe9ee; font-weight: 600;
}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    border-color: #dbe9ee; background: #345467;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
    background: #f5f9fa; color: #122b39;
}
[data-testid="stSidebar"] button:focus-visible,
[data-testid="stSidebar"] label:focus-within {
    outline: 2px solid #b8d8ed; outline-offset: 3px;
}
.st-key-identity { border-bottom: 1px solid #d4dfe1; padding-bottom: 16px; }
.st-key-identity h1 {
    font-size: 34px; line-height: 1.2; letter-spacing: -.04em;
    font-weight: 800; padding: 0; margin: 0;
}
.mw-descriptor { font-size: 14px; line-height: 1.45; max-width: 610px; }
.mw-prototype {
    font-size: 13px; letter-spacing: .06em; text-transform: uppercase;
    text-align: right; line-height: 1.8; color: #546974;
}
.st-key-thesis p { font-size: clamp(21px, 1.6vw, 28px); line-height: 1.3; }
.st-key-thesis strong { font-weight: 500; letter-spacing: -.035em; }
.st-key-thesis { padding: 2px 0; }
.st-key-evidence-banner [data-testid="stAlert"] {
    background: #e8eef1; color: #304e60; border: 1px solid #d6e1e6;
    border-left: 3px solid #63849a; border-radius: 5px; padding: 12px 18px;
}
.st-key-evidence-banner [data-testid="stAlert"] p {
    color: #304e60; font-size: 13px; line-height: 1.55; margin-bottom: 3px;
}
.st-key-evidence-banner [data-testid="stAlert"] strong {
    font-size: 11px; letter-spacing: .1em;
}
.st-key-evidence-banner
    [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
    background: #fbf1de; border-color: #dfbe80;
}
.st-key-trajectory-panel, .st-key-run-summary, .st-key-reference-context {
    background: #fff; border: 1px solid #d4dfe1; border-radius: 10px;
    padding: 24px; box-shadow: 0 3px 9px #1b364207;
}
.st-key-trajectory-panel { border-top: 3px solid #253f50; }
.st-key-run-summary { border-top: 3px solid #567995; }
.st-key-reference-context { background: #edf1f1; box-shadow: none; padding: 20px 24px; }
.mw-eyebrow {
    color: #526d7c; font-size: 11px; line-height: 1.4;
    text-transform: uppercase; letter-spacing: .14em; font-weight: 600;
}
.mw-panel-heading { display: flex; justify-content: space-between; align-items: center;
    }
.mw-panel-heading h2 { font-size: 25px; margin: 4px 0 0; font-weight: 600; }
.mw-tag {
    font: 12px Consolas, monospace; background: #eef2f4; color: #536975;
    padding: 6px 10px; border: 1px solid #dbe3e7; border-radius: 4px;
}
.mw-outcome { font-size: clamp(26px, 2vw, 34px); line-height: 1.15;
    letter-spacing: -.035em; font-weight: 600; margin: 9px 0 3px; }
.st-key-evidence-status p, .st-key-evidence-status-observed p { font-size: 11px;
    line-height: 1.5; letter-spacing: .025em; }
.st-key-evidence-status strong, .st-key-evidence-status-observed strong {
    display: inline-block; background: #eaf0f5; color: #365777;
    padding: 6px 9px; border-radius: 4px; font-weight: 600;
}
.st-key-evidence-status-observed strong { background: #fcf0d9; color: #815416; }
.mw-measures { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 20px;
    margin: 2px 0 0; padding: 17px 0; border-top: 1px solid #e1e7e9;
    border-bottom: 1px solid #e1e7e9; }
.mw-measures dt, .mw-record dt, .mw-reference dt {
    font-size: 12px; color: #526b7a; font-weight: 400; margin-bottom: 6px;
}
.mw-measures dd { font-size: 40px; line-height: 1; letter-spacing: -.04em;
    margin: 0; font-weight: 500; font-variant-numeric: tabular-nums; }
.mw-record { margin: 0; display: grid; gap: 13px; }
.mw-record dd { margin: 0; color: #203c4e; font: 15px/1.5 Consolas, monospace;
    overflow-wrap: anywhere; }
.mw-record .mw-identity { font-size: 12px; }
.mw-reference { display: grid; grid-template-columns: 1fr 2fr; gap: 12px; margin: 10px 0
    0; }
.mw-reference dd { margin: 0; font: 16px/1.5 Consolas, monospace; overflow-wrap:
    anywhere; }
.mw-reference-title { font-size: 17px; font-weight: 600; margin: 5px 0 0; }
.st-key-reference-context [data-testid="stCaptionContainer"] p {
    font-size: 12px; line-height: 1.5;
}
.mw-legend { display: flex; flex-wrap: wrap; gap: 10px 20px; padding-top: 13px;
    border-top: 1px solid #e0e7ea; font-size: 12px; color: #435c6b; }
.mw-legend span { display: inline-flex; align-items: center; gap: 7px; }
.mw-legend i { display: inline-block; width: 19px; height: 0; border-top: 3px solid
    #2563eb; }
.mw-legend .reference { border-top: 2px dashed #6b7280; }
.mw-legend .obstacle { width: 8px; height: 8px; background: #374151; border: 0; }
.mw-legend .start { width: 9px; height: 9px; background: #16a34a; border: 0; transform:
    rotate(45deg); }
.mw-legend .goal { width: auto; height: auto; color: #ea580c; font: bold 19px Arial;
    border: 0; }
.mw-legend .recurrence { width: 11px; height: 11px; border: 2px solid #dc2626;
    border-radius: 50%; }
.st-key-trajectory-panel [data-testid="stCaptionContainer"] p {
    font-size: 12px; line-height: 1.55;
}
.st-key-raw-context { border: 1px solid #d4dfe1; border-radius: 6px;
    padding: 12px 18px; background: #e9eeee; }
.st-key-raw-context p { font-size: 13px; color: #3d5664; line-height: 1.5; }
.mw-record-heading { display: flex; align-items: baseline; justify-content:
    space-between;
    gap: 20px; padding: 11px 0 2px; }
.mw-record-heading h2 { font-size: 18px; font-weight: 600; margin: 0; }
.mw-record-heading p { font-size: 12px; color: #607580; margin: 0; }
[data-testid="stMain"] [data-testid="stExpander"] {
    background: #fff; border-radius: 6px; border-color: #d4dfe1;
}
[data-testid="stMain"] [data-testid="stExpander"] summary {
    color: #304e60; padding: 13px 16px;
}
[data-testid="stMain"] [data-testid="stExpander"] summary p { font-size: 13px; }
[data-testid="stMain"] [data-testid="stExpander"] summary:hover { color: #2458a6; }
[data-testid="stMain"] [data-testid="stExpander"] [data-testid="stAlert"] {
    background: #fbf1de; color: #61451d; border: 1px solid #e4d1ad;
}
[data-testid="stMain"] [data-testid="stExpander"] [data-testid="stAlert"] p { color:
    #61451d; }
@media (max-width: 1300px) {
    .stMainBlockContainer { padding: 2.5rem 1.5rem; }
    .st-key-trajectory-panel, .st-key-run-summary, .st-key-reference-context { padding:
    18px; }
    .mw-reference { grid-template-columns: 1fr; }
    .mw-outcome { font-size: 26px; }
}
@media (max-width: 1000px) {
    .st-key-evidence-workspace > [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    .st-key-evidence-workspace > [data-testid="stHorizontalBlock"] >
    [data-testid="stColumn"] {
        min-width: 100%; width: 100%; flex: 1 1 100%;
    }
    .mw-prototype { text-align: left; }
    .mw-record-heading { flex-wrap: wrap; gap: 8px; }
}
[data-testid="stMain"] [data-testid="stCaptionContainer"] p { color: #526976; }
[data-testid="stSidebar"] button[kind="primary"] p { color: #122b39; }
[data-testid="stSidebar"] button[kind="primary"]:hover p { color: #122b39; }
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
    color: #d9e7ec;
}
.st-key-reference-context h3.mw-reference-title {
    font-size: 19px; line-height: 1.4; padding: 0; margin: 5px 0 0;
}
.st-key-evidence-banner [data-testid="stAlertContainer"] {
    background: transparent; padding: 0;
}
.st-key-evidence-status p, .st-key-evidence-status-observed p {
    font-size: 12px; letter-spacing: .025em;
}
.st-key-evidence-banner [data-testid="stAlertContentInfo"],
.st-key-evidence-banner [data-testid="stAlertContentWarning"] {
    background: transparent;
}
[data-testid="stSidebar"] [data-testid="stRadioOption"]
    > div > div > div:not([data-testid]) { display: none; }
.st-key-trajectory-panel [data-testid="stCaptionContainer"] p,
.st-key-reference-context [data-testid="stCaptionContainer"] p {
    font-size: 13px; color: #435e6e;
}
[data-testid="stCaptionContainer"] { opacity: 1; }
[data-testid="stMain"] [data-testid="stExpander"] summary { background: #fff; }
[data-testid="stMain"] [data-testid="stExpander"] details[open] summary {
    background: #e9eff1;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] code {
    background: #213d4b; color: #c4d9e4;
}
</style>
"""
