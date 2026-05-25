from bs4 import BeautifulSoup, Comment
import os
import re
from datetime import datetime
# Set your expiry date (YYYY, MM, DD)
expiry_date = datetime(2026, 5, 24)
current_date = datetime.now()
if current_date > expiry_date:
    print("This script has expired. Please contact the developer.")
    exit()  # stop script
else:
    print("Script active. Running...")

directory_path = 'D:\\link\\chapter\\'

for xhtmlfile in os.listdir(directory_path):
    if xhtmlfile.endswith(".xhtml"):
        # Build the full file path
        file_path = os.path.join(directory_path, xhtmlfile)
    with open(file_path, encoding="utf-8") as f:
        html_content = f.read()
    from bs4 import BeautifulSoup
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    def not_link_citation_main(citations):
        for citation in citations:
            text = rf"{citation}"
            #pattern = rf"({text}) [0-9A-Z]"
            pattern = rf"(\b{text} ([0-9A-Z])?\d+(\.\d+)?)"
            matches = soup.find_all(string=re.compile(pattern))
            for match in matches:
                if match:
                    if not match.find_parent('a'):
                        line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                        with open(directory_path + "citation_main_not_linked.htm", "a", encoding="utf-8") as f:
                            f.write(f'''\n {xhtmlfile}\t{line}:{col}\t{citation}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>''')
    def not_link_citation(citations):
        for citation in citations:
            text = rf"{citation}"
            #pattern = rf"({text}) [0-9A-Z]"
            pattern = rf"(\b{text} ([0-9A-Z])?\d+(\.\d+)?\b)"
            matches = soup.find_all(string=re.compile(pattern))
            for match in matches:
                if match:
                    if not match.find_parent('a'):
                        line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                        with open(directory_path + "citation1_not_linked.htm", "a", encoding="utf-8") as f:
                            f.write(f'''\n {xhtmlfile}\t{line}:{col}\t{citation}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>''')
    main_citations = [
     "Figure",
     "Section",
     "Sections",
     "Eq.",
     "Eq",
     "Eqs",
     "Table",
     "TABLE",
     "Illustrations",
     "Illustration",
     "Example",
     "Equation",
     "Chapter",
     "Part",
     "Parts",
     "Problem",
     "Exercise",
     "Reaction",
     "Box",
     "Boxs",
     "LO",
     "page",
     "pages",
     "Figures",
     "Tables",
     "Examples",
     "Equations",
     "Chapters",
     "Problems",
     "Exercises",
     "Reactions",
     "Appendix",
     "DO IT!",
     "Definition",
     "Question",
     "Questions",
     "paragraphs",
     "paragraph"

     ]
    citations = [
     "Tax Planning Problem",
     "Algorithm",
     "Algorithms",
     "Tax Planning Problems",
     "Application Problem",
     "Application Problems",
     "Multiple Choice Question",
     "Multiple Choice Questions",
     "Discussion Questions",
     "Discussion Question",
     "Brief Exercise",
     "Brief Exercises",
     "Practice Problem",
     "Applied Learning",
     "Now You Do It",
     "Let’s Walk Through It",
     "expression",
     "formula",
     "note",
     "notes",
     "Color Plate",
     "Color Plates",
     "expressions",
     "formulas",
     "Chapter End Review Problem",
     "Chapter End Review Problems",
     "Exhibit",
     "Exhibits",
     "DO IT!",
     "IT’s About Business",
     "Technology Guide",
     
    ]

    def not_link_numbers():
        # Find all <a> tags
        a_tags = soup.find_all('a')

        for a in soup.find_all('a'):
            sib = a.next_sibling
            text = ''
            if isinstance(sib, str):
                text = sib
            elif sib:
                text = sib.get_text()
            nums = re.findall(r'\b\d+.\d+\b', text)
            if nums:
                line, col = a.find_parents()[0].sourceline, a.find_parents()[0].sourcepos
                with open(directory_path + "Numbers_not_linked.htm", "a", encoding="utf-8") as f:
                    f.write(f"\n {xhtmlfile} \t {line}:{col}\t{a.text!r} → {nums}<br/>\n")
                #print(f'{a.text!r} → {nums}')

    def not_link_citation2(citation_2):
        for citation in citation_2:
            text = rf"{citation}"
            #pattern = rf"^({text})([0-9A-Z]\.[0-9A-Z])"
            pattern = rf"(\b{text}\d+(\.\d+)?\b)"
            matches = soup.find_all(string=re.compile(pattern))
            for match in matches:
                if match:
                    if not match.find_parent('a'):
                        line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                        with open(directory_path + "citation2_not_linked.htm", "a", encoding="utf-8") as f:
                            f.write(f'''\n {xhtmlfile}\t{line}:{col}\t{citation}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>''')

    citation_2 = ["LO", "BE", "D", "E", "P"]

    
    def check_chapterlink():
        pattern = re.compile(r'"?([A-Z][A-Za-z\s&]+?)"?\s+chapter')
        matches = soup.find_all(string=re.compile(pattern))
        for match in matches:
            if match:
                if not match.find_parent('a'):
                    line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                    with open(directory_path + "chapter_link.htm", "a", encoding="utf-8") as f:
                        f.write(f'''\n {xhtmlfile}\t{line}:{col}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>''')
    def check_reflink():
        pattern = re.compile(r'\[\s*\d+(?:\s*,\s*(?:\d+|p{1,2}\.?\s*\d+(?:-\d+)?))?\s*\]')
        matches = soup.find_all(string=re.compile(pattern))
        #print(matches)
        for match in matches:
            if match:
                if not match.find_parent('a'):
                    line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                    with open(directory_path + "ref_link.htm", "a", encoding="utf-8") as f:
                        f.write(f'''\n {xhtmlfile}\t{line}:{col}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>\n''')

    check_reflink()
    def check_seelink():
        pattern = re.compile(r'\(?see\s+(?:the\s+)?["\']?([A-Z][A-Za-z\s&]+?)["\']?\)?')
        matches = soup.find_all(string=re.compile(pattern))
        for match in matches:
            if match:
                if not match.find_parent('a'):
                    line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                    with open(directory_path + "see_link.htm", "a", encoding="utf-8") as f:
                        f.write(f'''\n {xhtmlfile}\t{line}:{col}\t<span style=\"color:red\">Text:{match}</span>\t{match.parent.name}.{match.parent.get('class')}-->\t{match.parent.parent.name}.{match.parent.parent.get('class')}-->\t{match.parent.parent.parent.name}.{match.parent.parent.parent.get('class')}<br/>''')

    pattern = re.compile(r'(www|http|@)')
    def not_link_website():
        # Find all text nodes except comments
        for text in soup.find_all(string=True):
            if isinstance(text, Comment):  # skip comments
                continue
            if pattern.search(text):
                #print("Found:", text)
                if not text.find_parent('a'):
                    line, col = text.find_parents()[0].sourceline, text.find_parents()[0].sourcepos
                    with open(directory_path + "External_link_citation_not_linked.htm", "a", encoding="utf-8") as f:
                        f.write(f"\n {xhtmlfile} \t {line}:{col}\t<span style=\"color:red\">Text:{text}</span>\t{text.parent.name}.{text.parent.get('class')}-->\t{text.parent.parent.name}.{text.parent.parent.get('class')}-->\t{text.parent.parent.parent.name}.{text.parent.parent.parent.get('class')}<br/>")
                    

    not_link_numbers()
    check_chapterlink()
    check_seelink()
    not_link_citation_main(main_citations)
    not_link_citation(citations)
    not_link_citation2(citation_2)
    not_link_website()
    
    def Page_Breaks_Inside_Headers():
        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
                if pagebreak.find_parent(re.compile(r'^h\d$')):
                    line, col = pagebreak.sourceline, pagebreak.sourcepos
                    with open(directory_path + "pagebreak_placement_check.htm", "a", encoding="utf-8") as f:
                        f.write(f"{xhtmlfile}\t{line}:{col}\t{pagebreak}'\n" )
                    #print("pagebreak found inside the header")
                else:
                    pass

    Page_Breaks_Inside_Headers()
    def th_empty():
        tfoot_elements = soup.find_all('th')
        for i, atag in enumerate(tfoot_elements):
            if atag.text is None or atag.text.strip() == '':
                th_text = atag.text
                #th_id = atag['id']
                line, col = atag.sourceline, atag.sourcepos
                #print("No text", atag)
                with open(directory_path+"TABLE_empty_th.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{xhtmlfile}\t{line}:{col}\t{th_text}\t{atag}<br/>")
    th_empty()
    def th_scope():
        th_scopes = soup.find_all('th')
        for th_scope in th_scopes:
            is_th_scope = th_scope.get('scope')
            if is_th_scope is None:
                line, col = th_scope.sourceline, th_scope.sourcepos
                with open(directory_path+"TABLE_th_scope_missing.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{xhtmlfile}\t{line}:{col}\t{th_scope}<br/>")
    th_scope()
    def td_thead():
        theads = soup.find_all('thead')
        for thead in theads:
            thead_td = thead.find('td')
            if thead_td is not None:
                line, col = thead_td.sourceline, thead_td.sourcepos
                with open(directory_path+"TABLE_change_thead_td_TH.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{xhtmlfile}\t{line}:{col}\t{thead_td}<br/>")
    td_thead()
    def not_th():
        theads = soup.find_all('b')
        for thead in theads:
            thead_td = thead.find_parent('td')
            if thead_td is not None:
                line, col = thead_td.sourceline, thead_td.sourcepos
                with open(directory_path+"TABLE_change_td_TH_scope.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{xhtmlfile}\t{line}:{col}\t{thead_td}<br/>")
    not_th()

    def incorrect_scope():
        theads = soup.find_all('th')
        for thead in theads:
            thead_td = thead.find_parent('tbody')
            if thead_td is not None:
                R_th = thead.get('scope')
                if R_th != 'row':
                    line, col = thead.sourceline, thead.sourcepos
                    with open(directory_path+"TABLE_check_incorrect_scope.htm", "a", encoding="utf-8") as fs:
                        fs.write(f"\n{xhtmlfile}\t{line}:{col}\trow\t{thead}<br/>")
            colspan_th = thead.get('colspan')
            if colspan_th is not None:
                    colspan_scope = thead.get('scope')
                    if colspan_scope != 'colgroup':
                        line, col = thead.sourceline, thead.sourcepos
                        with open(directory_path+"TABLE_check_incorrect_scope.htm", "a", encoding="utf-8") as fs:
                            fs.write(f"\n{xhtmlfile}\t{line}:{col}\trowgroup\t{thead}<br/>")
                        
            rowspan_th = thead.get('rowspan')
            if rowspan_th is not None:
                    rowspan_scope = thead.get('scope')
                    if rowspan_scope != 'rowgroup':
                        line, col = thead.sourceline, thead.sourcepos
                        with open(directory_path+"TABLE_check_incorrect_scope.htm", "a", encoding="utf-8") as fs:
                            fs.write(f"\n{xhtmlfile}\t{line}:{col}\trowgroup\t{thead}<br/>")
                    
    incorrect_scope()

    def th_b():
        theads = soup.find_all('b')
        for thead in theads:
            thead_td = thead.find_parent('th')
            if thead_td is not None:
                line, col = thead_td.sourceline, thead_td.sourcepos
                with open(directory_path+"TABLE_remove_bold_TH.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{xhtmlfile}\t{line}:{col}\t{thead}<br/>")
    th_b()
    
    def table_not_nested_with_figure():
        tables = soup.find_all("table")
        for table in tables:
            if not any(table.find_parents('figure')):
                line, col = table.sourceline, table.sourcepos
                #print(line, col)
                with open(directory_path + "Table_not_nested_with_figure.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{xhtmlfile}\t{line}:{col}<br/>\n''')

    table_not_nested_with_figure()    

    def index_page_link():
        # Match numbers and ranges (e.g., 322–323, 152)
        pattern = re.compile(r'\b\d+\b')
        matches = soup.find_all(string=pattern)
        for match in matches:
            if not match.find_parent('a'):  # skip numbers inside <a>
                for num in pattern.findall(match):
                    # ignore if this text node contains a dash (range)
                    if '–' in match or '-' in match:
                        continue
                    line, col = match.find_parents()[0].sourceline, match.find_parents()[0].sourcepos
                    with open(directory_path + "index_link.htm", "a", encoding="utf-8") as f:
                        f.write(f'''\n {xhtmlfile}\t{line}:{col}\t{num}<br/>''')

    index_page_link()

    def aside_follow_div():
            asides = soup.find_all("aside")
            for aside in asides:
                try:
                    next_tag = aside.find_next()
                    if next_tag and next_tag.name == 'div' and next_tag.get("class") == ["top", "hr"]:
                        pass
                    else:
                        line, col = aside.sourceline, aside.sourcepos
                        with open(directory_path + "aside_top_hr_missing.htm", "a", encoding="utf-8") as f:
                            f.write(f'''{xhtmlfile}\t{line}:{col}\t\t<aside> not followed by <div class="top hr"><hr/></div><br></br>\n''')
                    last_sib = aside.find_all()[-1]
                    if last_sib and last_sib.name == 'hr':
                        pass
                    else:
                        line, col = aside.sourceline, aside.sourcepos
                        with open(directory_path + "aside_top_hr_missing.htm", "a", encoding="utf-8") as f:
                            f.write(f'''{xhtmlfile}\t{line}:{col}\t\t<aside> not end with <div class="top hr"><hr/></div><br></br>\n''')
                except Exception as e:
                    with open(directory_path + "aside_Error.htm", "a", encoding="utf-8") as f:
                        f.write(f'''{xhtmlfile}\t{line}:{col}\tEMPTY <aside><br></br>\n''')
                    print(e)
                    
    aside_follow_div()



print("finished")

with open(directory_path + "finished.txt", "a", encoding="utf-8") as f:
    f.write(f'''finished''')
