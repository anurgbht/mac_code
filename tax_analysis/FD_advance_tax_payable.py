"""
This script calculates the interest and tax liability for Fixed Deposits (FDs) on a conservative basis, considering the interest accrued up to the Analysis Date or Maturity Date, whichever is earlier. It generates a report showing the interest earned, total tax liability, estimated TDS, and net advance tax payable for each quarter.
how to run - 
uv run python tax_analysis/FD_advance_tax_payable.py
"""
import json
import pandas as pd
from datetime import datetime, date

import json
import pandas as pd
from datetime import datetime, date

def get_quarter_end(d):
    """Returns the end date of the calendar quarter for a given date."""
    if d.month <= 3: return date(d.year, 3, 31)
    if d.month <= 6: return date(d.year, 6, 30)
    if d.month <= 9: return date(d.year, 9, 30)
    return date(d.year, 12, 31)

def calculate_conservative_tax(principal, annual_rate_pct, start_str, end_str, analysis_date_str=None, tax_slab=0.30, show_fy="all"):
    """
    Calculates interest and tax up to the Analysis Date or Maturity Date, whichever is earlier.
    """
    start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
    maturity_date = datetime.strptime(end_str, '%Y-%m-%d').date()
    
    # Determine the date to stop calculations
    if analysis_date_str:
        analysis_date = datetime.strptime(analysis_date_str, '%Y-%m-%d').date()
    else:
        analysis_date = date.today()
    
    # Effective end is the point where we stop the math
    effective_end_date = min(maturity_date, analysis_date)
    
    rate = annual_rate_pct / 100
    current_principal = principal
    current_date = start_date
    records = []
    
    # Only run the loop if we haven't passed the effective end date
    while current_date < effective_end_date:
        q_end = get_quarter_end(current_date)
        # Calculate interest only until the end of the quarter or the analysis limit
        period_end = min(q_end, effective_end_date)
        
        days = (period_end - current_date).days
        if current_date == start_date: days += 1 
            
        q_interest = current_principal * rate * (days / 365)
        
        if period_end.month >= 4:
            fy = f"{period_end.year}-{period_end.year+1}"
        else:
            fy = f"{period_end.year-1}-{period_end.year}"
            
        m = period_end.month
        q_name = 'Q1 (Apr-Jun)' if m==6 else 'Q2 (Jul-Sep)' if m==9 else 'Q3 (Oct-Dec)' if m==12 else 'Q4 (Jan-Mar)'
        
        records.append({'FY': fy, 'Quarter': q_name, 'Interest': q_interest})
        
        current_principal += q_interest
        current_date = period_end + pd.Timedelta(days=1)

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    summary = df.groupby(['FY', 'Quarter'])['Interest'].sum().reset_index()
    
    effective_tax_rate = tax_slab * 1.04 # 30% Slab + 4% Cess
    fy_totals = summary.groupby('FY')['Interest'].transform('sum')
    
    summary['Total Tax Liability'] = summary['Interest'] * effective_tax_rate
    summary['Est. TDS (10%)'] = summary.apply(lambda x: x['Interest'] * 0.10 if fy_totals[summary.index[summary['Interest'] == x['Interest']][0]] > 40000 else 0, axis=1)
    summary['Net Advance Tax to Pay'] = (summary['Total Tax Liability'] - summary['Est. TDS (10%)']).clip(lower=0)

    if show_fy != "all":
        summary = summary[summary['FY'] == show_fy]

    # Add totals row
    totals = summary.select_dtypes(include=['number']).sum()
    totals['FY'] = 'TOTAL'
    totals['Quarter'] = ''
    summary = pd.concat([summary, pd.DataFrame([totals])], ignore_index=True)

    summary['Interest'] = summary['Interest'].round(2)
    summary['Total Tax Liability'] = summary['Total Tax Liability'].round(2)
    summary['Est. TDS (10%)'] = summary['Est. TDS (10%)'].round(2)
    summary['Net Advance Tax to Pay'] = summary['Net Advance Tax to Pay'].round(2)
    
    return summary

if __name__ == "__main__":
    
    # SET YOUR ANALYSIS DATE HERE (e.g., Today's date or Feb 7, 2026)
    analysis_date = "2026-02-07" 
    analysis_fy = "2025-2026"  # Set to "all" to show all financial years or specify a particular FY like "2025-2026"
    
    with open("tax_analysis/FD_details.json", "r") as f:
        FD_details = json.load(f)

    for fd_name, input_data in FD_details.items():
        print(f"\n--- {fd_name} ---")
        print(f"--- Analysis as of {analysis_date} ---")
        print(f"Principal: {input_data['principal']}, Rate: {input_data['rate']}%, Start: {input_data['start']}, End: {input_data['end']}")
        # --- INPUT DATA ---
        principal = input_data['principal']
        rate = input_data['rate']
        start = input_data['start']
        end = input_data['end']

        report = calculate_conservative_tax(principal, rate, start, end, analysis_date_str=analysis_date, show_fy=analysis_fy)
        report.to_excel(f"tax_analysis/reports/{fd_name}_tax_report.xlsx", index=False)
        print(report.to_string(index=False))