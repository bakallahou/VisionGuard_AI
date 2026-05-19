from fpdf import FPDF
import sqlite3
from datetime import datetime
import os
import pandas as pd  # ✅ AJOUTÉ POUR L'EXPORT EXCEL

# =========================================
# GENERATE PDF REPORT
# =========================================

def generate_pdf_report():

    conn = sqlite3.connect("database/attendance.db")

    query = "SELECT * FROM attendance"

    rows = conn.execute(query).fetchall()

    conn.close()

    # =====================================
    # CREATE PDF
    # =====================================

    pdf = FPDF()

    pdf.add_page()

    # =====================================
    # TITLE
    # =====================================

    pdf.set_font("Arial", "B", 20)

    pdf.cell(
        200,
        10,
        txt="VISIONGUARD AI REPORT",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # =====================================
    # DATE
    # =====================================

    current_date = datetime.now().strftime("%Y-%m-%d")

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        200,
        10,
        txt=f"Date : {current_date}",
        ln=True
    )

    pdf.ln(10)

    # =====================================
    # TABLE HEADER
    # =====================================

    pdf.set_font("Arial", "B", 12)

    pdf.cell(20, 10, "ID", 1)

    pdf.cell(70, 10, "NAME", 1)

    pdf.cell(50, 10, "DATE", 1)

    pdf.cell(40, 10, "TIME", 1)

    pdf.ln()

    # =====================================
    # TABLE CONTENT
    # =====================================

    pdf.set_font("Arial", "", 11)

    for row in rows:

        pdf.cell(20, 10, str(row[0]), 1)

        pdf.cell(70, 10, str(row[1]), 1)

        pdf.cell(50, 10, str(row[2]), 1)

        pdf.cell(40, 10, str(row[3]), 1)

        pdf.ln()

    # =====================================
    # CREATE REPORTS FOLDER
    # =====================================

    if not os.path.exists("reports"):

        os.makedirs("reports")

    # =====================================
    # SAVE PDF
    # =====================================

    filename = f"reports/attendance_report_{current_date}.pdf"

    pdf.output(filename)

    return filename

# =========================================
# GENERATE EXCEL REPORT (✅ AJOUTÉ)
# =========================================

def generate_excel_report():

    conn = sqlite3.connect(
        "database/attendance.db"
    )

    query = "SELECT * FROM attendance"

    df = pd.read_sql(query, conn)

    conn.close()

    # =====================================
    # CREATE REPORTS FOLDER
    # =====================================

    if not os.path.exists("reports"):

        os.makedirs("reports")

    # =====================================
    # SAVE EXCEL
    # =====================================

    current_date = datetime.now().strftime("%Y-%m-%d")

    filename = (
        f"reports/attendance_report_{current_date}.xlsx"
    )

    df.to_excel(
        filename,
        index=False
    )

    return filename

# =========================================
# SEND EMAIL REPORT
# =========================================

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email.mime.text import MIMEText

from email import encoders


def send_email_report(report_path):

    sender_email = "bakallahoussam@gmail.com"

    sender_password = "fbsj meuh nuxc tvmt"

    receiver_email = "bakallahoussam@gmail.com"

    subject = "VisionGuard AI Attendance Report"

    body = """
    Bonjour,

    Veuillez trouver ci-joint le rapport
    généré automatiquement par VisionGuard AI.

    Cordialement,
    VisionGuard AI
    """

    # =====================================
    # CREATE EMAIL
    # =====================================

    message = MIMEMultipart()

    message["From"] = sender_email

    message["To"] = receiver_email

    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    # =====================================
    # ATTACH REPORT
    # =====================================

    attachment = open(
        report_path,
        "rb"
    )

    part = MIMEBase(
        "application",
        "octet-stream"
    )

    part.set_payload(
        attachment.read()
    )

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(report_path)}"
    )

    message.attach(part)

    # =====================================
    # SMTP SERVER
    # =====================================

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    text = message.as_string()

    server.sendmail(
        sender_email,
        receiver_email,
        text
    )

    server.quit()
