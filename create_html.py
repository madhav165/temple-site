import modin.pandas as pd
import os
import textwrap
from fpdf import FPDF
import re
import aspose.words as aw

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

df1 = pd.read_csv('states.csv')
df2 = pd.read_csv('temple_details.csv')

for index,row in df1.iterrows():
    state_name = row['state']
    state_name = re.sub(r'[^\w_. -]', ' ', state_name).replace('  ', ' ')
    state_name = state_name.strip().encode('latin-1', 'replace').decode('latin-1')
    print(state_name)
    state_description = row['description'].strip().encode('latin-1', 'replace').decode('latin-1')
    
    if not os.path.isdir(os.path.join('India', state_name)):
        os.mkdir(os.path.join('India', state_name))
    with open(os.path.join('India', state_name, state_name.replace(',','_').replace(' ','_')+'.txt'), 'w') as f:
        f.write(state_name+'\n')
        f.write(state_description)

    input_filename = os.path.join('India', state_name, state_name.replace(',','_').replace(' ','_')+'.txt')
    output_filename = os.path.join('India', state_name, state_name.replace(',','_').replace(' ','_')+'.pdf')
    with open(input_filename) as f:
        text = f.read()
    text_to_pdf(text, output_filename)
    os.remove(input_filename)
    
    df3 = df2.loc[df2['state']==row['state']]
    for index2, row2 in df3.iterrows():
        temple_name = row2['temple_name']
        temple_name = re.sub(r'[^\w_. -]', ' ', temple_name).replace('  ', ' ')
        temple_name = temple_name.strip().encode('latin-1', 'replace').decode('latin-1')
        print(temple_name)
        temple_details = row2['temple_details']
        temple_details = re.sub(r'[^\w_. -]', ' ', temple_details).replace('  ', ' ')
        temple_details = temple_details.strip().encode('latin-1', 'replace').decode('latin-1')
        try:
            with open(os.path.join('India', state_name, temple_name.replace(',','_').replace(' ','_')+'.txt'), 'w') as f:
                f.write(temple_name+'\n')
                f.write(temple_details)
            input_filename = os.path.join('India', state_name, temple_name.replace(',','_').replace(' ','_')+'.txt')
            output_filename = os.path.join('India', state_name, temple_name.replace(',','_').replace(' ','_')+'.pdf')
            with open(input_filename) as f:
                text = f.read()
            text_to_pdf(text, output_filename)
            os.remove(input_filename)
        except:
            pass

        

        # load TXT document
        doc = aw.Document(input_filename)
        # save TXT as PDF file
        doc.save(output_filename, aw.SaveFormat.PDF)