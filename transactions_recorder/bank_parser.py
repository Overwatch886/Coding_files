import pdfplumber
import pandas as pd
import re
from datetime import datetime

# --- FILE CONFIGURATION ---
FILES = {
    "Kuda": "Customer Statement (1)(kuda).pdf",
    "OPay": "OLAYEMI BASIRAT OSENI_8056668785_20250910125239 (1)(opay).pdf",
    "Access": "Statement_1930839340_20250910142102 (1)(access).pdf"
}
OUTPUT_FILE = "MoneyManager_Import_Complete.tsv"

# --- HELPER FUNCTIONS ---

def clean_amount(text):
    """
    Aggressively extracts a number from a string, handling Nigerian PDF quirks.
    Examples: "N 5,000.00" -> 5000.0, "-2.483.00" -> -2483.0
    """
    if not text: return 0.0
    
    # 1. Remove obvious currency chars and noise
    text = re.sub(r'[N#=,\s]', '', str(text))
    
    # 2. Check for negative sign at start
    is_negative = text.startswith('-')
    
    # 3. Extract all digits and dots
    # This handles cases like "2.483.00" where OCR sees extra dots
    digits_only = re.sub(r'[^\d.]', '', text)
    
    if not digits_only: return 0.0
    
    # 4. Fix multiple dots (e.g. 1.250.50 -> 1250.50)
    if digits_only.count('.') > 1:
        parts = digits_only.split('.')
        # Join all parts except last as integer part, last part as decimal
        digits_only = "".join(parts[:-1]) + "." + parts[-1]
        
    try:
        val = float(digits_only)
        return -val if is_negative else val
    except:
        return 0.0

def get_opay_amount(line, description):
    """
    OPay text lines are messy. We try to find the amount at the end or middle.
    Logic: Find the number with the most decimal precision or consistent formatting.
    """
    # Remove the date from the line first
    line_no_date = re.sub(r'\d{4}\s+[A-Za-z]{3}\s+\d{2}', '', line)
    
    # Find all potential number patterns (e.g., -500.00, 20.00)
    # Regex: Optional minus, digits, optional comma/dot separators, decimal part
    matches = re.findall(r'(-?[\d.,]+)', line_no_date)
    
    valid_amounts = []
    for m in matches:
        # Filter out obvious non-amounts (like reference numbers which are long integers)
        clean = m.replace(',', '').replace('.', '')
        if len(clean) > 8 and '.' not in m: continue # Likely a ref number
        if m == '.' or m == '-': continue
        
        try:
            val = clean_amount(m)
            valid_amounts.append(val)
        except: continue
        
    if not valid_amounts: return 0.0
    
    # Heuristics:
    # 1. If description contains "Withdrawal", "Transfer to", "Airtime", "Auto-save", expect Negative.
    # 2. If "Deposit", "Transfer from", "Interest", expect Positive.
    
    amount = valid_amounts[0] # Default to first found
    
    # OWealth specific: sometimes amounts are tiny (0.09), sometimes large
    # OPay often prints the balance AFTER the amount. We usually want the first number.
    
    desc_lower = description.lower()
    if any(x in desc_lower for x in ['withdrawal', 'transfer to', 'airtime', 'auto-save', 'debit']):
        amount = -abs(amount)
    elif any(x in desc_lower for x in ['deposit', 'transfer from', 'credit']):
        amount = abs(amount)
        
    return amount

# --- PARSERS ---

def parse_opay_universal(pdf_path):
    transactions = []
    print(f"--- Processing OPay: {pdf_path} ---")
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            page_count = 0
            
            for line in lines:
                # OPay Date Pattern: "2025 Aug 01" (YYYY MMM DD)
                # We use regex to find lines starting with this pattern
                date_match = re.search(r'(\d{4}\s+[A-Za-z]{3}\s+\d{2})', line)
                
                if date_match:
                    date_str = date_match.group(1)
                    
                    # Description is text between date and amount.
                    # Since parsing text is messy, we take the whole line and clean it later.
                    full_text = line.replace(date_str, "").strip()
                    
                    # Extract amount using helper
                    amount = get_opay_amount(line, full_text)
                    
                    # Refine Description: Remove the amount numbers from the text
                    # (Simple cleanup)
                    desc_clean = re.sub(r'[\d.,-]', '', full_text).strip()
                    desc_clean = re.sub(r'\s+', ' ', desc_clean) # Remove double spaces
                    
                    if amount == 0 and "Opening Balance" not in full_text:
                        # Sometimes OPay splits lines. If amount is 0, we might be missing it.
                        # For now, we skip zero amounts to avoid noise.
                        continue

                    transactions.append({
                        "Date": datetime.strptime(date_str, "%Y %b %d").strftime("%Y-%m-%d"),
                        "Account": "OPay",
                        "Category": "Uncategorized",
                        "Amount": amount,
                        "Note": desc_clean
                    })
                    page_count += 1
            
            print(f"   Page {i+1}: Found {page_count} txns")

    return pd.DataFrame(transactions)

def parse_kuda_universal(pdf_path):
    transactions = []
    print(f"--- Processing Kuda: {pdf_path} ---")
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            page_count = 0
            
            for line in lines:
                # Kuda Date Pattern: "01/08/25" (DD/MM/YY)
                # Check start of line, allowing for some whitespace
                date_match = re.search(r'^\s*(\d{2}/\d{2}/\d{2})', line)
                
                if date_match:
                    date_str = date_match.group(1)
                    
                    # Kuda Text Line usually: Date Time Amount Description
                    # But extracting text muddles columns.
                    
                    # 1. Identify amount. Look for numbers with dots/commas.
                    # Kuda amounts are usually like "5,000.00" or "300.00"
                    amounts = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', line)
                    
                    if not amounts: continue
                    
                    # Usually the first amount found is the transaction amount
                    # (The second might be the balance)
                    raw_amount = float(amounts[0].replace(',', ''))
                    
                    desc_lower = line.lower()
                    
                    # 2. Determine Sign based on keywords
                    # Kuda keywords: "outward", "airtime", "withdrawal", "web payment" -> Negative
                    # "inward", "deposit" -> Positive
                    if any(x in desc_lower for x in ['outward', 'transfer to', 'airtime', 'paycom', 'withdrawal']):
                        final_amount = -raw_amount
                    elif any(x in desc_lower for x in ['inward', 'transfer from', 'deposit']):
                        final_amount = raw_amount
                    else:
                        # Fallback: if we can't tell, assume negative for safety (spending) 
                        # unless it explicitly says 'credit'
                        final_amount = -raw_amount

                    # 3. Clean Description
                    # Remove date, time (XX:XX:XX), and amounts from text
                    clean_desc = re.sub(r'\d{2}/\d{2}/\d{2}', '', line) # Remove date
                    clean_desc = re.sub(r'\d{2}:\d{2}:\d{2}', '', clean_desc) # Remove time
                    clean_desc = re.sub(r'[\d,]+\.\d{2}', '', clean_desc) # Remove amounts
                    clean_desc = re.sub(r'[#N]', '', clean_desc).strip() # Remove currency symbols
                    
                    transactions.append({
                        "Date": datetime.strptime(date_str, "%d/%m/%y").strftime("%Y-%m-%d"),
                        "Account": "Kuda",
                        "Category": "Uncategorized",
                        "Amount": final_amount,
                        "Note": clean_desc
                    })
                    page_count += 1
            print(f"   Page {i+1}: Found {page_count} txns")
            
    return pd.DataFrame(transactions)

def parse_access_universal(pdf_path):
    transactions = []
    print(f"--- Processing Access: {pdf_path} ---")
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            page_count = 0
            
            for line in lines:
                # Access Date Pattern: "01-AUG-25"
                date_match = re.search(r'^\s*(\d{2}-[A-Z]{3}-\d{2})', line)
                
                if date_match:
                    date_str = date_match.group(1)
                    
                    # Access structure in text is hard because Debit/Credit columns merge.
                    # We rely on finding the amounts.
                    amounts = re.findall(r'([\d,]+\.\d{2})', line)
                    
                    if not amounts: continue
                    
                    # If 1 amount found -> likely Debit or Credit (Balance on next line?)
                    # If 2 amounts found -> Amount and Balance
                    
                    raw_val = float(amounts[0].replace(',', ''))
                    
                    # Access uses specific keywords for debits usually
                    desc_lower = line.lower()
                    
                    # Access usually: Date | Value Date | Description | Debit | Credit | Balance
                    # If the text line ends with the amount, it might be the balance.
                    # This is tricky. Let's use the table extractor for Access ONLY, as it was working fine previously.
                    # But since we are here, let's try a hybrid approach.
                    
                    # Actually, Access PDFs are very standard. Let's assume Credit if "Transfer from" or "Deposit"
                    is_credit = False
                    if "transfer from" in desc_lower or "deposit" in desc_lower:
                        is_credit = True
                    
                    # If we found 3 numbers, the middle one might be credit?
                    # Let's revert to simple logic: 
                    # If Note contains "Transfer to", "Airtime", "Commission", "VAT" -> Negative
                    if any(x in desc_lower for x in ['transfer to', 'airtime', 'commission', 'vat', 'withdrawal', 'sms alert']):
                        final_amount = -raw_val
                    else:
                        final_amount = raw_val

                    # Clean Note
                    clean_desc = re.sub(r'\d{2}-[A-Z]{3}-\d{2}', '', line)
                    clean_desc = re.sub(r'[\d,]+\.\d{2}', '', clean_desc).strip()
                    
                    transactions.append({
                        "Date": datetime.strptime(date_str, "%d-%b-%y").strftime("%Y-%m-%d"),
                        "Account": "Access Bank",
                        "Category": "Uncategorized",
                        "Amount": final_amount,
                        "Note": clean_desc
                    })
                    page_count += 1
            print(f"   Page {i+1}: Found {page_count} txns")

    return pd.DataFrame(transactions)

# --- MAIN EXECUTION ---
def main():
    all_dfs = []
    
    try:
        df_kuda = parse_kuda_universal(FILES["Kuda"])
        all_dfs.append(df_kuda)
    except Exception as e: print(f"Kuda Error: {e}")

    try:
        df_opay = parse_opay_universal(FILES["OPay"])
        all_dfs.append(df_opay)
    except Exception as e: print(f"OPay Error: {e}")

    try:
        df_access = parse_access_universal(FILES["Access"])
        all_dfs.append(df_access)
    except Exception as e: print(f"Access Error: {e}")

    if all_dfs:
        final = pd.concat(all_dfs, ignore_index=True)
        final.sort_values(by="Date", inplace=True)
        
        # Final cleanup of Note column (remove common noise)
        final['Note'] = final['Note'].str.replace(r'[^\w\s-]', '', regex=True)
        
        final.to_csv(OUTPUT_FILE, sep='\t', index=False)
        
        print("\n" + "="*40)
        print(f"COMPLETE! {len(final)} Total Transactions.")
        print(f"Saved to: {OUTPUT_FILE}")
        print("="*40)
        print(final.groupby('Account').size()) # Print count per bank
    else:
        print("Fatal: No data found.")

if __name__ == "__main__":
    main()