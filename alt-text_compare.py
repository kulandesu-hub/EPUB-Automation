import difflib
import os
import re

def highlight_differences_html(str1, str2):
    # Create a Differ object
    differ = difflib.Differ()

    # Compare the two strings
    diff = list(differ.compare(str1.split(), str2.split()))
    #print(diff)

    # Highlight the differences
    result = []
    for word in diff:
        if word.startswith('- '):
            result.append(f'<span style="color: red;">{word[2:]}</span>')
        elif word.startswith('+ '):
            result.append(f'<span style="color: green;">{word[2:]}</span>')
        elif word.startswith('? '):
            continue
        else:
            result.append(word[2:])
    
    return ' '.join(result)


directory_path1 = 'D:\\alt-text_report\\'
with open(directory_path1 + "html_alttext.htm", encoding="utf-8") as f:
    html_content = f.read()

with open(directory_path1 + "excel_alt_text.htm", encoding="utf-8") as f:
    xl_content = f.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
soup2 = BeautifulSoup(xl_content, 'html.parser')

directory_path1 = 'D:\\alt-text_report\\'
with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
    f.write('''<table border="1">''')
with open(directory_path1 + "XL_sorted.htm", 'a', encoding="utf-8") as f:
    f.write('''<table border="1">''')

with open(directory_path1 + "HTML_Sorted.htm", 'a', encoding="utf-8") as f:
    f.write('''<table border="1">''')


tr_tds = soup.find_all('tr', class_="td")
for tr_td in tr_tds:
    td_elements = tr_td.find_all('td')
    file_names = tr_td.find('td')
    print(file_names)
    html_file_names = file_names.parent
    
    
    with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
        f.write(str(html_file_names))
    with open(directory_path1 + "HTML_Sorted.htm", 'a', encoding="utf-8") as f:
        f.write(str(html_file_names))


    file_names = file_names.get_text()
    print(file_names)
    try:
        xl_trs = soup2.find(text=file_names).parent
        
        xls_tr = xl_trs.parent
        
        xl_alltd = xls_tr.find_all('td')

        html_short_alt = td_elements[3].text
        xl_short_alt = xl_alltd[3].text
        
        with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
            f.write(str(xls_tr)+ '''<tr><td colspan="7" style="color:red">break</td></tr> ''')
        with open(directory_path1 + "XL_sorted.htm", 'a', encoding="utf-8") as f:
            f.write(str(xls_tr)+ '''<tr><td colspan="7" style="color:red">break</td></tr> ''')
        

        highlighted_diff_html = highlight_differences_html(html_short_alt, xl_short_alt)
        html_output = f'<p>{highlighted_diff_html}</p>'
        #print(html_output)
        with open(directory_path1 + 'highlighted_diff.html', 'a') as file:
            file.write(html_output)

        with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
         f.write('''<tr><td colspan="6" style="background-color: pink;" align="left"><b>Combined Short Alt-text:</b><br/>'''
                 + str(html_output) + '''<br/></td></tr>''')

        html_long_alt = td_elements[4]

        if html_long_alt.find('aside'):
             aside = html_long_alt.find('aside')
        else:
            continue
        if html_long_alt.find('summary'):
            summary = html_long_alt.find('summary')
            summary_heading = summary.text
        else:
            continue
        
        html_cleaned_summary = summary_heading.replace("Extended description for ", '', 1).strip()

        
        
        html_long_alttet = aside.text
        xl_long_alttext = xl_alltd[4].text
        xl_heading = xl_alltd[5].text

        html_long_alttet_cleanup = html_long_alttet.lstrip("\n")
        #print(html_cleaned_summary)
        #print(html_long_alttet_cleanup)
        #print(xl_long_alttext)



        highlighted_diff_html = highlight_differences_html(html_long_alttet_cleanup, xl_long_alttext)
        html_output = f'<p>{highlighted_diff_html}</p>'
        #print(html_output)
        with open(directory_path1 + 'highlighted_diff.html', 'a') as file:
            file.write(html_output)
        
        with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
         f.write('''<tr><td colspan="6" style="background-color: orange;" align="left"><b>Combined Long Alt-text:</b><br/>'''
                 + str(html_output) + '''<br/></td></tr>''')

        highlighted_diff_html = highlight_differences_html(html_cleaned_summary, xl_heading)
        html_output = f'<p>{highlighted_diff_html}</p>'
        #print(html_output)
        with open(directory_path1 + 'highlighted_diff.html', 'a') as file:
            file.write(html_output)

        with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
         f.write('''<tr><td colspan="6" style="background-color: yellow;" align="left"><b>Combined Alt-text Heading:</b><br/>'''
                 + str(html_output) + '''<br/></td></tr>''')
        

    except Exception as e:
        with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
            f.write('''<tr><td colspan="6" align="center" style="color:red">''' + str(file_names) + ''' is Not found in Excel</td></tr>''')
        with open(directory_path1 + "HTML_Sorted.htm", 'a', encoding="utf-8") as f:
            f.write('''<tr><td colspan="6" align="center" style="color:red">''' + str(file_names) + ''' is Not found in Excel</td></tr>''')

            #print(e)
        
with open(directory_path1 + "merge.htm", 'a', encoding="utf-8") as f:
    f.write('''</table>''')
with open(directory_path1 + "HTML_Sorted.htm", 'a', encoding="utf-8") as f:
    f.write('''</table>''')
with open(directory_path1 + "XL_sorted.htm", 'a', encoding="utf-8") as f:
    f.write('''</table>''')

print("Finished")

with open("D:\\alt-text_report\\alt-text_compare_finished.txt", "a", encoding="utf-8") as f:
    f.write("task completed")
print('Finished')
