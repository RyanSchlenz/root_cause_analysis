import pandas as pd
import re

def main():
    # Define the paths for the input and output CSV files
    input_csv_file_path = 'filtered_groups.csv'
    output_csv_file_path = 'filtered_subjects.csv'

    # Define keyword rules for specific Subject Groups using regex
    keyword_rules = {
        'ADUC': [
            r'\bsso\b', r'\bsingle sign-on\b', r'\blogin\b', r'\bcannot login\b', r'\blogin issue\b',  
            r'\blogins\b', r'\blog ins\b', r'\bcreds check\b', r'\bpassword reset\b', 
            r'\bpw reset\b', r'\bpw\b', r'\bactive directory\b', r'\baduc\b', 
            r'\bcredential\b', r'\bcredentials\b', r'\bSSO\b', r'\bDisable Accounts\b',
        ],
        'Azure Virtual Desktop (AVD)': [
            r'\bavd\b', r'\bremote desktop\b', r'\bazure virtual desktop\b', r'\bpennant desktop\b', 
            r'\bremote desk top\b', r'\bAzure Access\b', r'\baccess to azure\b', r'\bazure\b'
        ],
        'Workday': [
            r'\bworker profile update\b', r'\bprofile update\b', r'\bupdated withholding\b'
        ],
        'HCHB': [
            r'\bhchb\b', r'\bpointcare training\b', r'\bpointcare\b', r'\bpoint care\b', 
            r'\bpoc\b', r'\bhome care home base\b', r'\bhomecarehomebase\b', r'\bworkflow\b', 
            r'\bHCHB\b', r'\bhomecare homebase\b'
        ],
        'Printer/Scanner/Copier': [
            r'\bprinter\b', r'\bscanner\b', r'\bcopier\b', r'\badd printer\b', r'\bprinterlogic\b', 
            r'\badd new printer\b', r'\bremove printer\b'
        ],
        'Drive Access': [
            r'\bj-drive\b', r'\bg-drive\b', r'\bg drive\b', r'\bshared drive\b', r'\bh-drive\b'
        ],
        'Exchange': [
            r'\bemail\b', r'\bmail\b', r'\bmailbox\b', r'\bemail inbox\b', r'\binbox\b', 
            r'\bdistribution list\b', r'\bdl\b', r'\bshared mailbox\b', r'\boutlook\b', r'\bGroup List\b'
        ],
        'Faxage': [
            r'\bfax\b', r'\bfaxage\b', r'\bfaxes\b', r'\bfaxs\b', r'\bfaxages\b', r'\bfax age\b'  
        ],
        'MOBI': [
            r'\bmobi\b', r'\bmobile\b', r'\bcellphone\b', r'\bcell\b', r'\bphone\b', r'\bphone number\b', 
            r'\bsamsung\b', r'\bandroid\b', r'\bverizon\b', r'\bactivate\b', r'\bphones\b'
        ],
        'PCC': [
            r'\bpcc\b', r'\bpointclickcare\b', r'\bpoint click care\b', r'\bPCC\b'
        ],
        'Fuze': [
            r'\bfuze\b'
        ],
        'Equipment': [
            r'\bshipping label\b', r'\bequipment order\b', r'\border equipment\b', 
            r'\bFedEx\b', r'\blaptops\b', r'\blaptop\b', r'\bcomputer\b', r'\bchromebook\b', 
            r'\bchrome book\b', r'\bntd\b', r'\bstratodesk\b', r'\bstrato desk\b', r'\btablet\b', r'\breturn label\b'
        ],
        'UAP': [
            r'\bUAP\b', r'\buser account provisioning\b', r'\btermination\b', 
            r'\btermination-\b', r'\btermed\b', r'\bTerminations\b'
        ],
        'Microsoft 365 Products': [
            r'\bExcel\b', r'\bTeams\b', r'\bteams\b', r'\bexcel\b'
        ],
        'Adobe': [
            r'\badobe\b', r'\bAdobe\b', r'\badobe pdf\b'
        ],
        'Forcura': [
            r'\bforcura\b', r'\bForcura\b'
        ],
        'Other': [
            r'\bGoogle Chrome\b'
        ],
        'Network': [
            r'\bnetwork\b', r'\binternet\b', r'\bfirewall\b', r'\bISP\b'
        ], 
        'Smartsheet': [
            r'\bsmartsheet\b', r'\bsmartsheets\b', r'\bsmart sheet\b', r'\bsmart sheets\b'
        ],
        'Pennant Guide': [
            r'\bPennU\b', r'\bPenn U\b', r'\bPennant U\b', r'\bPennant University\b', r'\bPennantUniversity\b', r'\bPennant Guide\b', r'\bPennantGuide\b', r'\bPenn Guide\b', r'\bHartford Guide\b'
        ],
        'End User Training': [
            r'\bMissed Call Follow Up\b', r'\bhelp\b', r'\bCall Back Request\b', r'\bhelp please\b', r'\burgent\b', r'\bNo vm left\b', r'\bno vm\b', r'\bUnknown caller\b', r'\bConversation with\b', r'\bCall back - no answer\b'
        ]
    }

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file_path)

    # Ensure relevant columns are treated as strings
    df['Ticket subject'] = df['Ticket subject'].astype(str)
    df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].astype(str)

    # Function to assign Product - Service Desk Tool based on Ticket subject and keyword rules
    def assign_product(ticket_subject, product_tool):
        if pd.notna(product_tool) and product_tool.strip() != 'nan' and product_tool.strip():  
            return product_tool  # Return existing value if it's not NaN or empty
        # Check for keywords in ticket subject using regex
        ticket_subject_lower = ticket_subject.lower()
        for product, patterns in keyword_rules.items():
            if any(re.search(pattern, ticket_subject_lower) for pattern in patterns):
                return product
        return 'Other'  # Return 'Other' if no match is found

    # Apply the function to update 'Product - Service Desk Tool'
    df['Product - Service Desk Tool'] = df.apply(
        lambda row: assign_product(row['Ticket subject'], row['Product - Service Desk Tool']),
        axis=1
    )

    # Set 'Product - Service Desk Tool' to 'Other' if it has no value
    df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].replace('', 'Other')

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_file_path, index=False)

    print(f"Filtered Subjects CSV file with keywords saved to {output_csv_file_path}")

if __name__ == "__main__":
    main()
