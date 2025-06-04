from fpdf import FPDF  # Ensure FPDF is imported for gradient support

def template_beta(pdf, data):
    theme_color = pdf.bank_config["theme_color"]  # (45, 105, 155)
    font_family = "Arial"  # Modern, clean font
    font_size = 10
    line_h = 5
    pdf.l_margin = 15
    pdf.r_margin = 15
    pdf.set_left_margin(pdf.l_margin)
    pdf.set_right_margin(pdf.r_margin)

    # Gradient Header
    def draw_gradient(y, h):
        for i in range(int(h)):
            r = theme_color[0] + (i * (200 - theme_color[0]) // h)
            g = theme_color[1] + (i * (220 - theme_color[1]) // h)
            b = theme_color[2] + (i * (255 - theme_color[2]) // h)
            pdf.set_fill_color(r, g, b)
            pdf.rect(0, y + i, pdf.w, 1, 'F')

    draw_gradient(0, 25)
    pdf._draw_logo_placeholder(pdf.l_margin, 5, 30, 15, bg_color=(255, 255, 255), text_color=theme_color)
    pdf.set_xy(pdf.w - pdf.r_margin - 90, 8)
    pdf.set_font(font_family, "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(80, 10, pdf.bank_config['name'], 0, 0, 'R')
    pdf.set_xy(pdf.w - pdf.r_margin - 90, 18)
    pdf.set_font(font_family, "I", 9)
    pdf.cell(80, 8, pdf.bank_config.get("tagline", ""), 0, 0, 'R')
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(30)

    # Sidebar for Key Info
    sidebar_width = 50
    pdf.set_fill_color(240, 245, 250)
    pdf.rect(pdf.w - pdf.r_margin - sidebar_width, 30, sidebar_width, 60, 'F')
    pdf.set_xy(pdf.w - pdf.r_margin - sidebar_width + 5, 35)
    pdf.set_font(font_family, "B", 10)
    pdf.set_text_color(*theme_color)
    pdf.cell(sidebar_width - 10, line_h, "Loan Reference", 0, 1)
    pdf.set_font(font_family, "", 9)
    pdf.multi_cell(sidebar_width - 10, line_h, data.get('loan_id', 'N/A'), 0, 'L')
    pdf.set_xy(pdf.w - pdf.r_margin - sidebar_width + 5, 50)
    pdf.set_font(font_family, "B", 10)
    pdf.cell(sidebar_width - 10, line_h, "Issued", 0, 1)
    pdf.set_font(font_family, "", 9)
    pdf.multi_cell(sidebar_width - 10, line_h, pdf.current_date, 0, 'L')
    pdf.set_text_color(0, 0, 0)

    # Main Content Area
    pdf.set_left_margin(pdf.l_margin)
    pdf.set_right_margin(pdf.r_margin + sidebar_width + 5)
    pdf.set_y(30)

    # Introductory Paragraph
    pdf.set_font(font_family, "B", 12)
    pdf.cell(0, line_h, f"To: {data.get('borrow_name', 'N/A')}", 0, 1)
    pdf.ln(3)
    pdf.set_font(font_family, "", font_size)
    pdf.multi_cell(0, line_h, f"Dear Valued Client,\n\nWe are pleased to confirm the rollover of your loan facility with {pdf.bank_config['name']}. Below are the updated terms for your review. Please contact us at {pdf.bank_config['contact_email']} with any questions.", 0, 1)
    pdf.ln(5)

    # Stylized Divider
    pdf.set_line_width(0.5)
    pdf.set_draw_color(*theme_color)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin - sidebar_width - 5, pdf.get_y())
    pdf.ln(5)

    # Borderless Table for Facility and Principal Details
    pdf._common_section_title("Loan Facility Details", text_color=theme_color, font_size=11)
    table_width = pdf.w - pdf.l_margin - pdf.r_margin - sidebar_width - 5
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)  # Light background for header
    pdf.cell(table_width, line_h, "Details", 0, 1, 'L', fill=True)
    pdf.ln(2)
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
        pdf.set_fill_color(245, 248, 252)  # Subtle background for rows
        pdf.cell(table_width, line_h, f"{field}: {value}", 0, 1, 'L', fill=(field == fields[0][0]))  # Background only for first row
        pdf.ln(1)  # Small spacing between rows
    pdf.ln(5)

    # Divider
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin - sidebar_width - 5, pdf.get_y())
    pdf.ln(5)

    # Borderless Table for Rollover Terms
    pdf._common_section_title("Rollover Terms", text_color=theme_color, font_size=11)
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(table_width, line_h, "Details", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font(font_family, "", font_size)
    date_fields = [
        (pdf.get_label('effective_date'), data.get('effective_date', 'N/A')),
        (pdf.get_label('next_maturity_date'), data.get('next_maturity_date', 'N/A')),
        (pdf.get_label('date_setting_date'), f"{data.get('date_setting_date', 'N/A')} {data.get('rate_setting_date_note', '')}"),
    ]
    for field, value in date_fields:
        pdf.set_fill_color(245, 248, 252)
        pdf.cell(table_width, line_h, f"{field}: {value}", 0, 1, 'L', fill=(field == date_fields[0][0]))
        pdf.ln(1)
    pdf.ln(5)

    # Divider
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin - sidebar_width - 5, pdf.get_y())
    pdf.ln(5)

    # Borderless Table for Applicable Rates
    pdf._common_section_title("Applicable Rates", text_color=theme_color, font_size=11)
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(table_width, line_h, "Details", 0, 1, 'L', fill=True)
    pdf.ln(2)
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
        pdf.set_fill_color(245, 248, 252)
        pdf.cell(table_width, line_h, f"{field}: {value}", 0, 1, 'L', fill=(field == rate_fields[0][0]))
        pdf.ln(1)
    pdf.ln(5)

    # Divider
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin - sidebar_width - 5, pdf.get_y())
    pdf.ln(5)

    # Governing Terms Paragraph
    pdf._common_section_title("Governing Terms", text_color=theme_color, font_size=11)
    pdf.set_font(font_family, "", 8)
    pdf.multi_cell(0, 4, f"This rollover is governed by the master loan agreement between {data.get('borrow_name', 'the Borrower')} and {pdf.bank_config['name']}. All unmodified terms remain in effect. Contact us at {pdf.bank_config['contact_email']} for assistance.", 0, 1)
    pdf.ln(10)

    # Signatory
    pdf.set_font(font_family, "I", font_size)
    pdf.cell(0, line_h, "On behalf of Beta Financial Services", 0, 1)
    pdf.ln(5)
    pdf.set_font(font_family, "B", font_size)
    pdf.cell(0, line_h, "Authorised Signatory", 0, 1)

    # Reset margins for footer
    pdf.set_right_margin(pdf.r_margin)
