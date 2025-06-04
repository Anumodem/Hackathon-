from fpdf import FPDF  # Ensure FPDF is imported

def template_beta(pdf, data):
    theme_color = pdf.bank_config["theme_color"]  # (45, 105, 155)
    font_family = "Arial"  # Professional, widely used in financial documents
    font_size = 10
    line_h = 5
    pdf.l_margin = 15
    pdf.r_margin = 15
    pdf.set_left_margin(pdf.l_margin)
    pdf.set_right_margin(pdf.r_margin)

    # Subtle Wave Gradient Header
    def draw_wave_gradient(y, h):
        for i in range(int(h)):
            r = theme_color[0] + (i * (230 - theme_color[0]) // h)
            g = theme_color[1] + (i * (245 - theme_color[1]) // h)
            b = theme_color[2] + (i * (255 - theme_color[2]) // h)
            pdf.set_fill_color(r, g, b)
            wave_width = pdf.w * (1 - i / (2 * h))  # Tapers slightly for wave effect
            pdf.rect(0, y + i, wave_width, 1, 'F')

    draw_wave_gradient(0, 20)
    # Compact Logo
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(pdf.l_margin, 5, 25, 10, 'F')
    pdf.set_text_color(*theme_color)
    pdf.set_font(font_family, "B", 8)
    pdf.set_xy(pdf.l_margin + 2, 7)
    pdf.cell(21, 6, pdf.bank_config.get("logo_text", "BFS"), 0, 0, 'C')
    # Bank Name and Tagline
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(pdf.l_margin + 30, 5)
    pdf.set_font(font_family, "B", 14)
    pdf.cell(0, 8, pdf.bank_config['name'], 0, 0, 'L')
    pdf.set_xy(pdf.l_margin + 30, 13)
    pdf.set_font(font_family, "I", 8)
    pdf.cell(0, 6, pdf.bank_config.get("tagline", ""), 0, 0, 'L')
    pdf.set_text_color(0, 0, 0)

    # Header Badge for Loan Reference and Issue Date
    badge_width = 70
    pdf.set_fill_color(240, 245, 250)
    pdf.rect(pdf.w - pdf.r_margin - badge_width, 5, badge_width, 15, 'F', border='LR')  # Subtle side borders
    pdf.set_xy(pdf.w - pdf.r_margin - badge_width + 5, 7)
    pdf.set_font(font_family, "B", 8)
    pdf.set_text_color(*theme_color)
    pdf.cell(badge_width - 10, line_h, f"Ref: {data.get('loan_id', 'N/A')}", 0, 1, 'L')
    pdf.set_xy(pdf.w - pdf.r_margin - badge_width + 5, 12)
    pdf.cell(badge_width - 10, line_h, f"Date: {pdf.current_date}", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(25)

    # Watermark (Simulated)
    pdf.set_text_color(220, 220, 220)
    pdf.set_font(font_family, "I", 40)
    pdf.set_xy(50, 100)
    pdf.cell(0, 0, pdf.bank_config['logo_text'], 0, 0, 'C', alpha=0.2)  # FPDF doesn't support alpha; simulate with light color
    pdf.set_text_color(0, 0, 0)

    # Introductory Paragraph
    pdf.set_font(font_family, "B", 12)
    pdf.cell(0, line_h, f"To: {data.get('borrow_name', 'N/A')}", 0, 1)
    pdf.ln(3)
    pdf.set_font(font_family, "", font_size)
    pdf.multi_cell(0, line_h, f"Dear Client,\n\nWe are pleased to confirm the rollover of your loan facility with {pdf.bank_config['name']}. This document details the updated terms effective as of the rollover date. For inquiries, please contact your relationship manager or email {pdf.bank_config['contact_email']}.", 0, 1)
    pdf.ln(5)

    # Rounded Section Divider
    pdf.set_fill_color(*theme_color)
    pdf.rect(pdf.l_margin, pdf.get_y(), 30, 5, 'F', border='R')  # Rounded-like effect with short rectangle
    pdf.set_font(font_family, "B", 11)
    pdf.set_text_color(*theme_color)
    pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + 1)
    pdf.cell(20, 3, "Loan Facility", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Horizontal Borderless Table for Facility and Principal Details
    table_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_widths = [table_width * 0.45, table_width * 0.55]  # Field: 45%, Value: 55%
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", 0, 0, 'L', fill=True)
    pdf.cell(col_widths[1], line_h, "Value", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font(font_family, "", font_size)
    fields = [
        (pdf.get_label('facility_loan_type'), data.get('facility_loan_type', 'N/A')),
        (pdf.get_label('ccy'), data.get('ccy', 'N/A')),
        (pdf.get_label('current_principal_global_share'), f"{data.get('current_principal_global_share', 0.0):,.2f} {data.get('ccy', '')}"),
        (pdf.get_label('current_principal_counterparty_share'), f"{data.get('current_principal_counterparty_share', 0.0):,.2f} {data.get('ccy', '')}"),
        (pdf.get_label('interest_principal_global_share'), f"{data.get('interest_principal_global_share', 0.0):,.2f} {data.get('ccy', '')}"),
        (pdf.get_label('interest_principal_counterparty_share'), f"{data.get('interest_principal_counterparty_share', 0.0):,.2f} {data.get('ccy', '')}"),
        (pdf.get_label('new_principal_amount'), f"{data.get('new_principal_amount', 0.0):,.2f} {data.get('ccy', '')}"),
    ]
    for i, (field, value) in enumerate(fields):
        pdf.set_fill_color(245, 248, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_widths[0], line_h, field, 0, 0, 'L', fill=(i % 2 == 0))
        pdf.cell(col_widths[1], line_h, str(value), 0, 1, 'L', fill=(i % 2 == 0))
        pdf.ln(1)
    pdf.ln(5)

    # Rounded Section Divider
    pdf.set_fill_color(*theme_color)
    pdf.rect(pdf.l_margin, pdf.get_y(), 30, 5, 'F', border='R')
    pdf.set_font(font_family, "B", 11)
    pdf.set_text_color(*theme_color)
    pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + 1)
    pdf.cell(20, 3, "Rollover Terms", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Horizontal Borderless Table for Rollover Terms
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", 0, 0, 'L', fill=True)
    pdf.cell(col_widths[1], line_h, "Value", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font(font_family, "", font_size)
    date_fields = [
        (pdf.get_label('effective_date'), data.get('effective_date', 'N/A')),
        (pdf.get_label('next_maturity_date'), data.get('next_maturity_date', 'N/A')),
        (pdf.get_label('date_setting_date'), f"{data.get('date_setting_date', 'N/A')} {data.get('rate_setting_date_note', '')}"),
    ]
    for i, (field, value) in enumerate(date_fields):
        pdf.set_fill_color(245, 248, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_widths[0], line_h, field, 0, 0, 'L', fill=(i % 2 == 0))
        pdf.cell(col_widths[1], line_h, str(value), 0, 1, 'L', fill=(i % 2 == 0))
        pdf.ln(1)
    pdf.ln(5)

    # Rounded Section Divider
    pdf.set_fill_color(*theme_color)
    pdf.rect(pdf.l_margin, pdf.get_y(), 30, 5, 'F', border='R')
    pdf.set_font(font_family, "B", 11)
    pdf.set_text_color(*theme_color)
    pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + 1)
    pdf.cell(20, 3, "Rate Details", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Horizontal Borderless Table for Applicable Rates
    pdf.set_font(font_family, "B", font_size)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(col_widths[0], line_h, "Field", 0, 0, 'L', fill=True)
    pdf.cell(col_widths[1], line_h, "Value", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font(font_family, "", font_size)
    rate_fields = [
        (pdf.get_label('base_rate'), f"{data.get('base_rate', 0.0):.2f}%"),
        (pdf.get_label('spread_margin_rate'), f"{data.get('spread_margin_rate', 0.0):.2f}%"),
        (pdf.get_label('credit_adjustment_rate_cas'), f"{data.get('credit_adjustment_rate_cas', 0.0):.2f}%"),
        (pdf.get_label('all_in_rate'), f"{data.get('all_in_rate', 0.0):.2f}%"),
    ]
    for i, (field, value) in enumerate(rate_fields):
        font_style = "B" if field == pdf.get_label('all_in_rate') else ""
        pdf.set_font(font_family, font_style, font_size)
        pdf.set_fill_color(245, 248, 252) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_widths[0], line_h, field, 0, 0, 'L', fill=(i % 2 == 0))
        pdf.cell(col_widths[1], line_h, str(value), 0, 1, 'L', fill=(i % 2 == 0))
        pdf.ln(1)
    pdf.ln(5)

    # Compliance Note (Realistic Addition)
    pdf.set_fill_color(*theme_color)
    pdf.rect(pdf.l_margin, pdf.get_y(), 30, 5, 'F', border='R')
    pdf.set_font(font_family, "B", 11)
    pdf.set_text_color(*theme_color)
    pdf.set_xy(pdf.l_margin + 5, pdf.get_y() + 1)
    pdf.cell(20, 3, "Compliance", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    pdf.set_font(font_family, "", 8)
    pdf.multi_cell(0, 4, f"This rollover adheres to the master loan agreement between {data.get('borrow_name', 'the Borrower')} and {pdf.bank_config['name']}. Rates are based on SOFR (Secured Overnight Financing Rate) or equivalent, per regulatory guidelines. Unmodified terms remain in effect. Contact {pdf.bank_config['contact_email']} or your relationship manager for clarification.", 0, 1)
    pdf.ln(5)

    # Signatory
    pdf.set_font(font_family, "I", 9)
    pdf.cell(0, line_h, f"Issued by {pdf.bank_config['name']}", 0, 1)
    pdf.ln(3)
    pdf.set_font(font_family, "B", 9)
    pdf.cell(0, line_h, "Authorised Officer", 0, 1)

    # Reset margins for footer
    pdf.set_right_margin(pdf.r_margin)
