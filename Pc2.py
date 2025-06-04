def template_beta(pdf, data):
    theme_color = pdf.bank_config["theme_color"]
    font_family = "Helvetica"
    font_size = 10
    line_h = 6
    pdf.l_margin = 15
    pdf.r_margin = 15
    pdf.set_left_margin(pdf.l_margin)
    pdf.set_right_margin(pdf.r_margin)

    # Header with background and logo
    pdf.set_fill_color(*theme_color)
    pdf.rect(0, 0, pdf.w, 30, 'F')
    pdf._draw_logo_placeholder(pdf.l_margin, 5, 40, 20, bg_color=(255, 255, 255), text_color=theme_color)
    pdf.set_xy(pdf.w - pdf.r_margin - 100, 10)
    pdf.set_font(font_family, "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(90, 15, pdf.bank_config['name'], 0, 0, 'R')
    pdf.set_xy(pdf.w - pdf.r_margin - 100, 20)
    pdf.set_font(font_family, "I", 10)
    pdf.cell(90, 10, pdf.bank_config.get("tagline", ""), 0, 0, 'R')
    pdf.set_y(35)

    # Title and Borrower Information
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_family, "B", 14)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(0, 10, "Loan Rollover Confirmation", border='TBLR', ln=1, align='C', fill=True)
    pdf.set_font(font_family, "", font_size)
    pdf.cell(0, line_h, f"To: {data.get('borrow_name', 'N/A')}", ln=1)
    pdf.cell(0, line_h, f"Ref: {data.get('loan_id', 'N/A')} | Issued: {pdf.current_date}", ln=1, align='R')
    pdf.ln(10)

    # Introductory Paragraph (Alpha-like)
    pdf.set_font(font_family, "", font_size)
    pdf.multi_cell(0, line_h, f"Dear Valued Client,\n\nThis document confirms the successful rollover of your loan facility with {pdf.bank_config['name']}. Below, we outline the key terms and conditions of this rollover for your records. Please review the details carefully and contact us at {pdf.bank_config['contact_email']} for any inquiries.", 0, 1)
    pdf.ln(5)

    # Table for Facility and Principal Details
    pdf._common_section_title("Facility and Principal Details", text_color=theme_color)
    col_widths = [(pdf.w - pdf.l_margin - pdf.r_margin) * 0.5] * 2
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", border='TBLR', align='C', fill=True)
    pdf.cell(col_widths[1], line_h, "Details", border='TBLR', align='C', fill=True)
    pdf.ln(line_h)
    pdf.set_font(font_family, "", font_size)
    fields = [
        (pdf.get_label('facility_loan_type'), data.get('facility_loan_type', 'N/A')),
        (pdf.get_label('ccy'), data.get('ccy', 'N/A')),
        (pdf.get_label('current_principal_global_share'), f"{data.get('current_principal_global_share', 0.0):,.5f} {data.get('ccy', '')}"),
        (pdf.get_label('current_principal_counterparty_share'), f"{data.get('current_principal_counterparty_share', 0.0):,.5f} {data.get('ccy', '')}"),
        (pdf.get_label('interest_principal_global_share'), f"{data.get('interest_principal_global_share', 0.0):,.5f} {data.get('ccy', '')}"),
        (pdf.get_label('interest_principal_counterparty_share'), f"{data.get('interest_principal_counterparty_share', 0.0):,.5f} {data.get('ccy', '')}"),
        (pdf.get_label('new_principal_amount'), f"{data.get('new_principal_amount', 0.0):,.5f} {data.get('ccy', '')}"),
    ]
    for field, value in fields:
        pdf.cell(col_widths[0], line_h, field, border='TBLR', align='L')
        pdf.cell(col_widths[1], line_h, str(value), border='TBLR', align='L')
        pdf.ln(line_h)
    pdf.ln(5)

    # Table for Rollover Terms and Dates
    pdf._common_section_title("Rollover Terms and Dates", text_color=theme_color)
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", border='TBLR', align='C', fill=True)
    pdf.cell(col_widths[1], line_h, "Details", border='TBLR', align='C', fill=True)
    pdf.ln(line_h)
    pdf.set_font(font_family, "", font_size)
    date_fields = [
        (pdf.get_label('effective_date'), data.get('effective_date', 'N/A')),
        (pdf.get_label('next_maturity_date'), data.get('next_maturity_date', 'N/A')),
        (pdf.get_label('date_setting_date'), f"{data.get('date_setting_date', 'N/A')} {data.get('rate_setting_date_note', '')}"),
    ]
    for field, value in date_fields:
        pdf.cell(col_widths[0], line_h, field, border='TBLR', align='L')
        pdf.cell(col_widths[1], line_h, str(value), border='TBLR', align='L')
        pdf.ln(line_h)
    pdf.ln(5)

    # Table for Applicable Rates
    pdf._common_section_title("Applicable Rates", text_color=theme_color)
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", border='TBLR', align='C', fill=True)
    pdf.cell(col_widths[1], line_h, "Details", border='TBLR', align='C', fill=True)
    pdf.ln(line_h)
    pdf.set_font(font_family, "", font_size)
    rate_fields = [
        (pdf.get_label('base_rate'), f"{data.get('base_rate', 0.0):.5f}%"),
        (pdf.get_label('spread_margin_rate'), f"{data.get('spread_margin_rate', 0.0):.5f}%"),
        (pdf.get_label('credit_adjustment_rate_cas'), f"{data.get('credit_adjustment_rate_cas', 0.0):.5f}%"),
        (pdf.get_label('all_in_rate'), f"{data.get('all_in_rate', 0.0):.5f}%"),
    ]
    for field, value in rate_fields:
        font_style = "B" if field == pdf.get_label('all_in_rate') else ""
        pdf.set_font(font_family, font_style, font_size)
        pdf.cell(col_widths[0], line_h, field, border='TBLR', align='L')
        pdf.cell(col_widths[1], line_h, str(value), border='TBLR', align='L')
        pdf.ln(line_h)
    pdf.ln(5)

    # Governing Terms Paragraph (Alpha-like)
    pdf._common_section_title("Governing Terms", text_color=theme_color)
    pdf.set_font(font_family, "", 8)
    pdf.multi_cell(0, 4.5, f"This rollover is governed by the master loan agreement and any amendments agreed between {data.get('borrow_name', 'the Borrower')} and {pdf.bank_config['name']}. All terms not modified herein remain in full effect. For further assistance, please contact your relationship manager or email {pdf.bank_config['contact_email']}.", 0, 1)
    pdf.ln(10)

    # Signatory
    pdf.set_font(font_family, "", font_size)
    pdf.cell(0, line_h, "Authorised Signatory,", 0, 1)
    pdf.ln(8)
    pdf.set_font(font_family, "B", font_size)
    pdf.cell(0, line_h, pdf.bank_config['name'], 0, 1)
