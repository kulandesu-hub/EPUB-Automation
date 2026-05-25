from bs4 import BeautifulSoup
from bs4 import Doctype
from langdetect import detect, LangDetectException
import unicodedata
import os
import re
directory_path = 'D:\\link\\chapter\\'

css_folder = r"D:\\link\\chapter\\"
xhtml_folder = r"D:\\link\\chapter\\"
##xhtml_folder = r"D:\\link\\all_xhtml\\"


def span_bold():
    bold_classes = set()

    # STEP 1: Find classes using font-weight in CSS
    for file in os.listdir(css_folder):
        if file.endswith(".css"):
            with open(os.path.join(css_folder, file), encoding="utf-8") as f:
                css = f.read()

            matches = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*font-weight\s*:\s*(bold|[6-9]00)', css)

            for m in matches:
                bold_classes.add(m[0])

        else:
            print(f"Not found CSS {file}")
    with open(directory_path + "bold_classes.htm", "a", encoding="utf-8") as f:
        f.write(f"{file}\tBOLD class: {bold_classes}\t{bold_classes}\n")

    print("Classes using font-weight:", bold_classes)

    print("\n---- HTML usage ----\n")

    # STEP 2: Check which HTML tags use those classes
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            for tag in soup.find_all(True):
                classes = tag.get("class")
                if classes:
                    for c in classes:
                        if c in bold_classes:
                            text = tag.get_text(strip=True)
                            print(file, "|", tag.name, "|", c, "|", text[:60])
                            with open(directory_path + "bold_classes_used_HTML.htm", "a", encoding="utf-8") as f:
                                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{tag.name}\t{c}\t{text[:60]}\n")

def span_italic():
    italic_classes = set()

    # STEP 1: Find classes using font-style: italic
    for file in os.listdir(css_folder):
        if file.endswith(".css"):
            with open(os.path.join(css_folder, file), encoding="utf-8") as f:
                css = f.read()
            

            matches = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*font-style\s*:\s*italic', css)

            for m in matches:
                italic_classes.add(m)
        else:
            print(f"not found css {file}")
        
    with open(directory_path + "italic_classes.htm", "a", encoding="utf-8") as f:
        f.write(f"ITALIC class: {italic_classes}\n")
    print("Classes using italic:", italic_classes)

    print("\n---- HTML usage ----\n")

    # STEP 2: Check which HTML tags use those classes
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            for tag in soup.find_all(True):
                classes = tag.get("class")
                if classes:
                    for c in classes:
                        if c in italic_classes:
                            text = tag.get_text(strip=True)
                            print(file, "|", tag.name, "|", c, "|", text[:60])
                            with open(directory_path + "italic_classes_used_HTML.htm", "a", encoding="utf-8") as f:
                                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{tag.name}\t{c}\t{text[:60]}\n")

def Nav_TOC():
##    nav_file = "nav.xhtml"
    nav_file = "toc.xhtml"
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            files.append(file)
    #print(files)

    # Read nav.xhtml
    with open(os.path.join(xhtml_folder, nav_file), encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

        
    navlinks = soup.find("nav", {"epub:type": "toc"})
    #print(navlinks)
    nav_links = []
    for navlink in navlinks.find_all("a", href=True):
        href1 = navlink["href"].split('/')[-1]
        href2 = href1.split('#')[0]
        nav_links.append(href2)
        
    #print("nav links", nav_links)

    missing = []
    for f in files:
         if f not in nav_links:
            missing.append(f)
            
    print("Files not listed in nav TOC:")
    for m in missing:
        print(m)
        with open(directory_path + "missing_nav_TOC.htm", "a", encoding="utf-8") as f:
            f.write(f"{m}\n")
    
    with open(directory_path + "missing_nav_TOC.htm", "a", encoding="utf-8") as f:
        f.write(f"Task completed\n")
            
def all_epub_type():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
            
    atrr_epub_types = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        #print(file)
        tags = soup.find_all(attrs={'epub:type': True})
        for tag in tags:
            atrr_name = tag.name
            atrr_epub_type = tag.get('epub:type')
            atrr_epub_types.append(atrr_epub_type)
            #atrr_class = tag.get('class')
            #print(f"{xhtmlfile}\t{atrr_name}\t{atrr_epub_type}\t{atrr_class}")
            with open(directory_path + "epub_type_elements.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{atrr_name}\t{atrr_epub_type}\n")
    uniq_epub_types = set(atrr_epub_types)
    deprecated_terms = ['annoref', 'annotation', 'biblioentry', 'bridgehead', 'endnote', 'help', 'note', 'rearnotes', 'sidebar', 'subchapter', 'warning']
    with open(directory_path + "deprecated_epub_type.htm", "a", encoding="utf-8") as f:
     f.write(f"All assigned epub:type values\t{uniq_epub_types}\n")

    deprecated_terms_uniq = []
    for uniq_epub_type in uniq_epub_types:
        if uniq_epub_type in deprecated_terms:
            deprecated_terms_uniq.append(uniq_epub_type)
    print(deprecated_terms_uniq)
    with open(directory_path + "deprecated_epub_type.htm", "a", encoding="utf-8") as f:
     f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\tepub:type '{deprecated_terms_uniq}' is deprecated and no longer recommended\n")
    
def all_role_type():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
            
    atrr_epub_types = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        #print(file)
        tags = soup.find_all(attrs={'role': True})
        for tag in tags:
            atrr_name = tag.name
            atrr_epub_type = tag.get('role')
            atrr_epub_types.append(atrr_epub_type)
            #atrr_class = tag.get('class')
            #print(f"{xhtmlfile}\t{atrr_name}\t{atrr_epub_type}\t{atrr_class}")
            with open(directory_path + "role_elements.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{atrr_name}\t{atrr_epub_type}\n")
    uniq_epub_types = set(atrr_epub_types)


def mandate_tags():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
    atrr_epub_types = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            html_content = f.read() 
            soup = BeautifulSoup(f, "lxml")

        # Check XML declaration
        if not html_content.strip().startswith('<?xml'):
            #print(f"{file}: XML declaration is not found")
            with open(directory_path + "mandate_tag.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t1:1\t{file}: XML declaration is not found\n")
            

        doctype = [x for x in soup.contents if isinstance(x, Doctype)]
        

        if doctype and doctype[0] == "html":
            ##print("DOCTYPE html exists")
            pass
        else:
            #print(f"{file}: DOCTYPE html missing or different")
            with open(directory_path + "mandate_tag.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t1:1\tDOCTYPE html missing or different\n")

        meta = soup.find("meta", charset="utf-8")
        if meta is None:
            #print(f"{file}: <meta charset=\"utf-8\"/> is not found")
            with open(directory_path + "mandate_tag.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t1:1\t<meta charset=\"utf-8\"/> is not found\n")

def pageTitle():
    import difflib
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        first_headings = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"])
        title = soup.find(["title"])
        if first_headings:
            title_text = title.text.strip()
            heading_text = first_headings.text.strip()
            
            with open(directory_path + "pagetitle.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{title.text.strip()}\t{first_headings.text.strip()}\n")
            differ = difflib.Differ()
            diff = list(differ.compare(title_text.lower().split(), heading_text.lower().split()))
            result = []
            for word in diff:
                if word.startswith('- '):
                    result.append(f'<span style="color: red;">{word[2:]}</span>')
                elif word.startswith('+ '):
                    #result.append(f'<span style="color: green;">{word[2:]}</span>')
                    pass
                elif word.startswith('? '):
                    continue
                else:
                    result.append(word[2:])
            jointext1_text2 = ' '.join(result)
            line, col = first_headings.sourceline, first_headings.sourcepos
            with open(directory_path+"diff.htm", "a", encoding="utf-8") as fs:
                fs.write(f'''<p>{file}\t{line}:{col}\t{title.text.strip()} <--> {first_headings.text.strip()}<br/><span class="DIFF">{jointext1_text2}</span></p>\n''')
        else:
            with open(directory_path + "No_pagetitle_heading.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{line}:{col}\t{title.text.strip()}\tNo heading found<br/>\n")

def Bold_italic_formating_H():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        first_headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "th"])
        try:
            for first_heading in first_headings:
                b_H = first_heading.find(['b', 'i', 'strong', 'em'])
                if b_H is not None:
                    #print(f"{b_H},{b_H.sourceline}:{b_H.sourcepos}\t{file}")
                    with open(directory_path + "Bold_italic_formating_H.htm", "a", encoding="utf-8") as f:
                        f.write(f'''{file}\t{b_H.sourceline}:{b_H.sourcepos}\t{b_H}\t{first_heading}\n''')
                    
        except Exception as e:
            print(f"{e}, in {file}")

        first_headings2 = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        try:
            for first_heading2 in first_headings2:
                b_H2 = first_heading2.find('span', class_=["bold", "italic"])
                if b_H2 is not None:
                    #print(f"{b_H},{b_H.sourceline}:{b_H.sourcepos}\t{file}")
                    with open(directory_path + "span_Bold_italic_formating_H.htm", "a", encoding="utf-8") as f:
                        f.write(f'''{file}\t{b_H2.sourceline}:{b_H2.sourcepos}\t{b_H2}\t{first_heading2}\n''')
                    
        except Exception as d:
            print(f"{d}, in {file}")

def all_caps_texts():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        all_caps_texts = soup.find_all(string=True)
        for text in all_caps_texts:
            if len(text) > 3: 
                if text.strip().isupper() and any(c.isalpha() for c in text):
                    line, col = text.parent.sourceline, text.parent.sourcepos
                    text_parent = text.parent
                    text_parent2 = text_parent.parent
                    #print(f"All caps text: '{text.strip()}'")
                    with open(directory_path + "all_caps_texts.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{line}:{col}\t{text_parent.name}\t{text_parent2.name}\t{text.strip()}'\n" )

def lang_detect():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for text in soup.find_all(string=True):
            text = text.strip()
            if len(text) < 7:   # skip short strings
                continue
            try:
                lang = detect(text)
                with open(directory_path + "lang_detect_elements.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{lang} -> {text}\n")
            except LangDetectException as e:
                pass
                print(e)
def Page_Breaks_newformat():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
            pagebreak_id = pagebreak.get('id')
            aria_lbls_id = pagebreak.get('aria-labelledby')
            all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}
            element = soup.find(id=aria_lbls_id)
            aria_lbl_linked_text = element.text.strip()
            with open(directory_path + "new_page_format_text.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file}\t{pagebreak_id}\t{aria_lbl_linked_text}\n''')
            with open(directory_path + "new_page_format.htm", "a", encoding="utf-8") as f:
                f.write(f'''{pagebreak}\t{element}\n''')

        pagebreak_atleast = soup.find(attrs={'epub:type':'pagebreak'})
        if pagebreak_atleast is None:
            with open(directory_path + "pagebreak_missing.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file} doesn't has pagebreak marker\n''')

def Page_List():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    page_links = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
            pagebreak_id = pagebreak.get('id')
            page_link = f"{file}#{pagebreak_id}"
            page_links.append(page_link)

    with open(directory_path + "pagelist.htm", "a", encoding="utf-8") as f:
        f.write(f'''{page_links}\n''')

    # Read nav.xhtml
##    nav_file = "nav.xhtml"
    nav_file = "toc.xhtml"
    with open(os.path.join(xhtml_folder, nav_file), encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    navlinks = soup.find("nav", {"epub:type": "page-list"})
    nav_links = []
    for navlink in navlinks.find_all("a", href=True):
        href = navlink["href"].split("/")[-1]
        nav_links.append(href)
    #print(nav_links)

    for page_id in page_links:
        if page_id not in nav_links:
            print(f"{page_id} is missing to nav page-list")
            with open(directory_path + "pagelist_missing.htm", "a", encoding="utf-8") as f:
                f.write(f'''{page_id} is missing in nav pagelist\n''')
        
    with open(directory_path + "pagelist_missing.htm", "a", encoding="utf-8") as f:
        f.write(f'''Task Completed\n''')

def unique_page_label():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    pagebreak_ids = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
            pagebreak_id = pagebreak.get('id')
            if not pagebreak_id or not pagebreak_id.strip():
                print(pagebreak)
            pagebreak_ids.append(pagebreak_id)

    seen = set()
    duplicates = set()
    for id in pagebreak_ids:
        if id in seen:
            duplicates.add(id)
        else:
            seen.add(id)
    with open(directory_path + "duplicate_pagebreak.htm", "a", encoding="utf-8") as f:
        f.write(f"Duplicate pageid {list(duplicates)} found")
    print(f"Duplicate pageid {list(duplicates)} found")

def http_link():
    from bs4 import BeautifulSoup, Comment
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    pagebreak_ids = []
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        a_tags = soup.find_all('a')
        for a_tag in a_tags:
            href = a_tag.get('href')
            if href is not None:
                if href.startswith('http') or href.startswith('//') or href.startswith('mailto') or 'www.' in href:
                    #print(f"External URL: {href}")
                    line, col = a_tag.sourceline, a_tag.sourcepos
                    with open(directory_path+"external.htm", "a", encoding="utf-8") as fs:
                        fs.write(f'''<p>{file}\t{line}:{col}\t{a_tag}\t{href}\t{a_tag.text}</p>\n''')
                   
                                
            else:
                    line, col = a_tag.sourceline, a_tag.sourcepos
                    with open(directory_path+"invalide_a.htm", "a", encoding="utf-8") as fs:
                                fs.write(f'''<p>{file}\t{line}:{col}\t{a_tag}</p>\n''')

        pattern = re.compile(r'(www|http|@)')
        # Find all text nodes except comments
        for text in soup.find_all(string=True):
            if isinstance(text, Comment):  # skip comments
                continue
            if pattern.search(text):
                #print("Found:", text)
                if not text.find_parent('a'):
                    line, col = text.find_parents()[0].sourceline, text.find_parents()[0].sourcepos
                    with open(directory_path + "External_link_citation_not_linked.htm", "a", encoding="utf-8") as f:
                        f.write(f"\n {file} \t {line}:{col}\t<span style=\"color:red\">Text:{text}</span>\t{text.parent.name}.{text.parent.get('class')}-->\t{text.parent.parent.name}.{text.parent.parent.get('class')}-->\t{text.parent.parent.parent.name}.{text.parent.parent.parent.get('class')}<br/>")

    

def para_decimal_list():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        number_pattern = re.compile(r'^\s*\d+\.\s*')
        
        for p in soup.find_all("p"):
            #text = p.get_text(strip=True)
            text = p.get_text(" ", strip=True)
            if number_pattern.match(text):
                print("Fake ordered list item:", text)
                line, col = p.sourceline, p.sourcepos
                with open(directory_path + "no_decimal_list.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{text}\n")
                
def para_alpha_list():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        number_pattern = re.compile(r'^\s*\(?([a-zA-Z])[\.\)]\s*')
        
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if number_pattern.match(text):
                print("Fake ordered list item:", text)
                line, col = p.sourceline, p.sourcepos
                with open(directory_path + "no_alpha_list.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{text}\n")
def para_roman_list():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        number_pattern = re.compile(r'^\s*\(?([ivxlcdmIVXLCDM]+)[\.\)]\s*')
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if number_pattern.match(text):
                print("Fake ordered list item:", text)
                line, col = p.sourceline, p.sourcepos
                with open(directory_path + "no_roman_list.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{text}\n")
def para_ul_list():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        number_pattern = re.compile(r'^\s*[-•‣◦▪*]\s+[A-Za-z]')
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if number_pattern.match(text):
                print("Fake ordered list item:", text)
                line, col = p.sourceline, p.sourcepos
                with open(directory_path + "no_ul_list.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{text}\n")
def Page_Breaks_Inside_Headers():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
                if pagebreak.find_parent(re.compile(r'^h\d$')):
                    line, col = pagebreak.sourceline, pagebreak.sourcepos
                    with open(directory_path + "pagebreak.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{line}:{col}\t{pagebreak}\n" )
                    print(f"{pagebreak} found inside the header")

    with open(directory_path + "pagebreak.htm", "a", encoding="utf-8") as f:
        f.write(f"TASK completed\n" )

def has_decomposed(text):
        return any(unicodedata.combining(ch) for ch in text)
            
def Unicode_normalization():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for tag in soup.find_all(string=True):
            if has_decomposed(tag):
                parent = tag.parent
                line, col = parent.sourceline, parent.sourcepos
                tag_s = tag.strip()
                print("Found")
                with open(directory_path + "nfd.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{tag_s}\n" )
        text_content = soup.get_text()
        invalid_chars = ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', 
        '\u0306', '\u0307', '\u0308', '\u0309', '\u030A', '\u030B', 
        '\u030C', '\u030D', '\u030E', '\u0311', '\u0315', '\u0323', 
        '\u0327', '\u0328', '\u0333', '\u0336', '\u033E', '\u033F', 
        '\u0359', '\u035B', '\u035C', '\uFB00', '\uFB01', '\uFB02', '\uFB03', '\uFB04', '\uFB05', '\uFB06']

        for tag in soup.find_all(string=True):
            if any(char in tag for char in invalid_chars):
                #print(f"Invalid char found in tag: {tag.parent.name}")
                #print(f"Text: {tag.strip()}")
                #print(f"Source line: {tag.parent.sourceline}, Source position: {tag.parent.sourcepos}")
                #print("Found invalid characters:", invalid_chars)
                print("Found")
                with open(directory_path+"Ligature_char.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{file}\t{tag.parent.sourceline}:{tag.parent.sourcepos}\t{tag.strip()}")
    with open(directory_path+"Ligature_char.htm", "a", encoding="utf-8") as fs:
        fs.write(f"Task completed")

def consecutive_pagebreak():
    from bs4 import BeautifulSoup, Tag
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreak_tags = soup.find_all(attrs={"epub:type":"pagebreak"})
        for i in range(len(pagebreak_tags) - 1):
            if isinstance(pagebreak_tags[i].next_sibling, Tag) and pagebreak_tags[i].next_sibling.get('epub:type') == 'pagebreak':
                #print(f"</span><span> detected between: '{pagebreak_tags[i]}' and '{pagebreak_tags[i+1]}'")
                line, col = pagebreak_tags[i].sourceline, pagebreak_tags[i].sourcepos
                print(f"{pagebreak_tags[i]}' and '{pagebreak_tags[i+1]}")
                with open(directory_path + "consecutive_pagebreak.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t</span><span> detected between: '{pagebreak_tags[i]}' and '{pagebreak_tags[i+1]}'\n" )

def aside_untitled_section():
    import difflib
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for idx, section in enumerate(soup.find_all("aside"), start=1):
            # Check for <header> or any heading tag
            has_heading = section.find(["header", "h1", "h2", "h3", "h4", "h5", "h6"])
            if has_heading:
                labledby = section.find_all(attrs={"aria-labelledby"})
                if labledby is None:
                    labelby = section['aria-labelledby']
                else:

                    aria_lbls = soup.find_all(attrs={"aria-labelledby":True})
                    all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}

                    aria_lbl_id = section.get('aria-labelledby')
                    element = soup.find(id=aria_lbl_id)
                    aria_lbl_text = section.find_next(['h1','h2','h3','h4','h5','h6']).text.strip()
                    aria_lbl_linked_text = element.text.strip()
                    with open(directory_path + "aside_aria_labelledby.htm", "a", encoding="utf-8") as f:
                      f.write(f"{file}\t{section.sourceline}:{section.sourcepos}\t{aria_lbl_id}\t{aria_lbl_text}\t{aria_lbl_linked_text}\n")

                    differ = difflib.Differ()
                    diff = list(differ.compare(aria_lbl_text.lower().split(), aria_lbl_linked_text.lower().split()))
                    result = []
                    for word in diff:
                        if word.startswith('- '):
                            result.append(f'<span style="color: red;">{word[2:]}</span>')
                        elif word.startswith('+ '):
                            #result.append(f'<span style="color: green;">{word[2:]}</span>')
                            pass
                        elif word.startswith('? '):
                            continue
                        else:
                            result.append(word[2:])
                    jointext1_text2 = ' '.join(result)
                    line, col = section.sourceline, section.sourcepos
                    with open(directory_path+"aside_diff.htm", "a", encoding="utf-8") as fs:
                        fs.write(f'''<p>{file}\t{line}:{col}\t{aria_lbl_text}\t
    <-->\t<span class="IDREF">{aria_lbl_linked_text}</span><br/><span class="DIFF">{jointext1_text2}</span></p>\n''')

                    line, col = section.sourceline, section.sourcepos
                    open_aside = str(section).split(">")[0] + ">"
                    with open(directory_path + "aside_titled.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{line}:{col}\t{open_aside} is equired accessible name (aria-labelledby) except only roles such as 'doc-footnote', 'doc-pullquote', 'doc-tip' and 'doc-example'\t\n")
            else:
                line, col = section.sourceline, section.sourcepos
                tag_str = str(section)
                open_tag = tag_str[:tag_str.find(">")+1]
                with open(directory_path + "aside_untitled.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{open_tag}\t\n")
def untitled_section():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for idx, section in enumerate(soup.find_all("section"), start=1):
            # Check for <header> or any heading tag
            has_heading = section.find(["header", "h1", "h2", "h3", "h4", "h5", "h6"])
            if has_heading:
                labledby = section.find_all(attrs={"aria-labelledby"})
##                if labledby is None:
##                    labelby = section['aria-labelledby']
##                else:
##                    line, col = section.sourceline, section.sourcepos
##                    open_aside = str(section).split(">")[0] + ">"
##                    with open(directory_path + "section_titled.htm", "a", encoding="utf-8") as f:
##                        f.write(f"{file}\t{line}:{col}\t{open_aside} is equired accessible name (aria-labelledby) except only roles such as 'doc-footnote', 'doc-pullquote', 'doc-tip' and 'doc-example'\t\n")
                
            else:
                line, col = section.sourceline, section.sourcepos
                tag_str = str(section)
                open_tag = tag_str[:tag_str.find(">")+1]
                with open(directory_path + "untitled.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{line}:{col}\t{open_tag}\t\n")
def Redundant_title_aria():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for tag in soup.find_all(True):
            if tag.has_attr("title") and tag.has_attr("aria-label"):
##                if tag["title"].strip() == tag["aria-label"].strip():
                    redundant_title_aria = str(tag).split(">")[0]+">"
                    with open(directory_path + "Redundant_title_aria.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{redundant_title_aria}\n")

def aria_label():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        aria_lbls = soup.find_all(attrs={"aria-label":True})
        for aria_lbl in aria_lbls:
            p0 = aria_lbl
            p1 = aria_lbl.parent
            p2 = p1.parent if p1 else None
            p3 = p2.parent if p2 else None
            p4 = p3.parent if p3 else None

            aria_lbls_text = aria_lbl['aria-label']
            aria_lbls_tag_name = aria_lbl.name
            line, col = aria_lbl.sourceline, aria_lbl.sourcepos
            with open(directory_path + "aria_label.htm", "a", encoding="utf-8") as f:
              f.write(f"{file}\t{line}:{col}\t{aria_lbls_tag_name}\t{aria_lbls_text}\t{p0.get('epub:type') if p1 else None}"
                    f"\t{p0.attrs.keys()}\t{p1.name if p1 else None}:{p1.get('class') if p1 else None}\n"
                    )                      
            
def aria_labelledby():
    import difflib
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        aria_lbls = soup.find_all(attrs={"aria-labelledby":True})
        all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}
        for aria_lbl in aria_lbls:
            try:
                aria_lbl_id = aria_lbl['aria-labelledby']
                element = soup.find(id=aria_lbl_id)
                aria_lbl_text = aria_lbl.find_next(['h1','h2','h3','h4','h5','h6']).text.strip()
                aria_lbl_linked_text = element.text.strip()
                with open(directory_path + "aria_labelledby.htm", "a", encoding="utf-8") as f:
                  f.write(f"{file}\t{aria_lbl.sourceline}:{aria_lbl.sourcepos}\t{aria_lbl_id}\t{aria_lbl_text}\t{aria_lbl_linked_text}\n")

                differ = difflib.Differ()
                diff = list(differ.compare(aria_lbl_text.lower().split(), aria_lbl_linked_text.lower().split()))
                result = []
                for word in diff:
                    if word.startswith('- '):
                        result.append(f'<span style="color: red;">{word[2:]}</span>')
                    elif word.startswith('+ '):
                        #result.append(f'<span style="color: green;">{word[2:]}</span>')
                        pass
                    elif word.startswith('? '):
                        continue
                    else:
                        result.append(word[2:])
                jointext1_text2 = ' '.join(result)
                line, col = aria_lbl.sourceline, aria_lbl.sourcepos
                with open(directory_path+"diff.htm", "a", encoding="utf-8") as fs:
                    fs.write(f'''<p>{file}\t{line}:{col}\t{aria_lbl_text}\t
<-->\t<span class="IDREF">{aria_lbl_linked_text}</span><br/><span class="DIFF">{jointext1_text2}</span></p>\n''')


            except Exception as e:
                with open(directory_path + "aria_labelledby_no_Heading.htm", "a", encoding="utf-8") as f:
                  f.write(f"{file}\t{aria_lbl.sourceline}:{aria_lbl.sourcepos}\t{aria_lbl_id}\t{e}\n")
                #print(f"{file}\t{aria_lbl.sourceline}:{aria_lbl.sourcepos}\t{aria_lbl_id}\t{e}")
def aria_describedby():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        aria_lbls = soup.find_all(attrs={"aria-describedby":True})
        all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}
        for aria_lbl in aria_lbls:
            aria_lbl_id = aria_lbl['aria-describedby']
            element = soup.find(id=aria_lbl_id)
            aria_lbl_text = aria_lbl
            
            aria_lbl_linked_text = element
            with open(directory_path + "aria-describedby.htm", "a", encoding="utf-8") as f:
              f.write(f'''{file}\t{aria_lbl.sourceline}:{aria_lbl.sourcepos}\t{aria_lbl}\t{aria_lbl_linked_text}\n''')
        
    with open(directory_path + "aria-describedby.htm", "a", encoding="utf-8") as f:
      f.write(f'''Task completed''')

def len_aria_labelledby():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        aria_lbls = soup.find_all('section', attrs={"aria-labelledby":True})
        aria_length = len(aria_lbls)
        with open(directory_path + "len_aria_labelledby.htm", "a", encoding="utf-8") as f:
            f.write(f"{file}\t{aria_length}\n")

def th_empty():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    with open(directory_path+"th_result.htm", "a", encoding="utf-8") as fs:
        fs.write(f"EMPTY TH checking ...")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        tfoot_elements = soup.find_all('th')
        for i, atag in enumerate(tfoot_elements):
            if atag.text is None or atag.text.strip() == '':
                th_text = atag.text
                #th_id = atag['id']
                line, col = atag.sourceline, atag.sourcepos
                #print("No text", atag)
                with open(directory_path+"th_result.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"\n{file}\t{line}:{col}\t{th_text}\t{atag}")
    with open(directory_path+"th_result.htm", "a", encoding="utf-8") as fs:
        fs.write(f"\nEMPTY TH checking finished")
                
def hidden():
    bold_classes = set()

    # STEP 1: Find classes using font-weight in CSS
    for file in os.listdir(css_folder):
        if file.endswith(".css"):
            with open(os.path.join(css_folder, file), encoding="utf-8") as f:
                css = f.read()

            matches = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*?(display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0)', css)
            print(f"match: {matches}")

            for m in matches:
                bold_classes.add(m[0])

        else:
            print(f"Not found CSS {file}")
    with open(directory_path + "hidden_classes.htm", "a", encoding="utf-8") as f:
        f.write(f"BOLD class: {bold_classes}\n")

    print("Classes using font-weight:", bold_classes)

    print("\n---- HTML usage ----\n")

    # STEP 2: Check which HTML tags use those classes
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            for tag in soup.find_all(True):
                classes = tag.get("class")
                if classes:
                    for c in classes:
                        if c in bold_classes:
                            text = tag.get_text(strip=True)
                            print(file, "|", tag.name, "|", c, "|", text[:60])
                            with open(directory_path + "hidden_classes_used_HTML.htm", "a", encoding="utf-8") as f:
                                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{tag.name}\t{c}\t{text[:60]}\n")

def css_disallowed():
    disallowed_classes = set()

    pattern = r'(.*?)\{[^}]*?(color|background-color)\s*:\s*#(?:000000|ffffff)[^}]*?\}'
    
    

    # STEP 1: Find classes in CSS
    for file in os.listdir(css_folder):
        if file.endswith(".css"):
            with open(os.path.join(css_folder, file), encoding="utf-8") as f:
                css = f.read()
            print(f"Found CSS: {file}")

            matches = re.findall(pattern, css, re.IGNORECASE)

            for selector, _ in matches:
                
                selector = selector.strip()

                # Extract class names (.className)
                class_matches = re.findall(r'\.(\w+)', selector)
                for cls in class_matches:
                    disallowed_classes.add(cls)

        else:
            print(f"Not CSS file: {file}")

    print("Disallowed classes:", disallowed_classes)
    with open(directory_path + "CSS_disallowed_classes.htm", "a", encoding="utf-8") as f:
        f.write(f"Disallowed_classes: {disallowed_classes}\n")

    print("\n---- HTML usage ----\n")

    # STEP 2: Check usage in HTML
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            for tag in soup.find_all(True):
                classes = tag.get("class")
                if classes:
                    for c in classes:
                        if c in disallowed_classes:
                            text = tag.get_text(strip=True)
                            with open(directory_path + "Disallowed_CSS_used_HTML.htm", "a", encoding="utf-8") as f:
                                f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{tag.name}\t{c}{text[:60]}\n")

def all_List():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        lists = soup.find_all(['ol','ul','dl'])
        for table in lists:
            table_parent = table
            line, col = table.sourceline, table.sourcepos
            with open(directory_path + "all_list.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{line}:{col}\t{table_parent}\n" )

def all_table():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        with open(directory_path + "all_table.htm", "a", encoding="utf-8") as f:
            f.write('''<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<style>th:before{content:"◄" attr(scope) "►" " ";color:red}thead:after{content:"thead"}tbody:before{content:"tbody"}</style>
</head>
<body>\n''')
        tables = soup.select('table')
        for table in tables:
            table_parent = table
            line, col = table.sourceline, table.sourcepos
            with open(directory_path + "all_table.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{line}:{col}\t{table_parent}\n" )
        with open(directory_path + "all_table.htm", "a", encoding="utf-8") as f:
            f.write(f'''</body>\n</html>''' )


def noteref():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        noterefs = soup.select('sup a')
        for noteref in noterefs:
            line, col = noteref.sourceline, noteref.sourcepos
            with open(directory_path+"noteref.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"{file}\t{line}:{col}\t{noteref}<br/>\n")
            
        noterefs2 = soup.select('a sup')
        for noteref2 in noterefs2:
            print(f"always use 'sup a'")
            line2, col2 = noteref2.sourceline, noteref2.sourcepos
            with open(directory_path+"noteref2.htm", "a", encoding="utf-8") as fs:
                    fs.write(f"{file}\t{line2}:{col2}\t{noteref2}<br/>\n")
def single_column_table():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        tables = soup.select('table')
        for table in tables:
            rows = table.find_all('tr')
            if all(len(row.find_all(['td', 'th'])) == 1 for row in rows):
                line, col = table.sourceline, table.sourcepos
                with open(directory_path + "single_column_table.htm", "a", encoding="utf-8") as f:
                   f.write(f"{file}\t{line}:{col}\t{table}\n" )

    with open(directory_path + "single_column_table.htm", "a", encoding="utf-8") as f:
       f.write(f"TASK Completed\n" )

def br_Body():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for heading in soup.find_all("br"):
            with open(directory_path + "br_tag.htm", "a", encoding="utf-8") as f:
               f.write(f"{file}\t{heading.sourceline}:{heading.sourcepos}\t{heading}\t{heading.parent}\n" )
        for text_node in soup.find_all(string=True):
            text = text_node.get_text()
            if "\xa0" in text:
                with open(directory_path + "nbsp.htm", "a", encoding="utf-8") as f:
                   f.write(f"{file}\t{text_node.parent.sourceline}:{text_node.parent.sourcepos}\t{text_node.parent}\t{text_node}\n" )
            
def repeated_char():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for text_node in soup.find_all(string=True):

            matches = re.finditer(r'(\.\.\.|(\.\s){2,}\.|_{2,}|\u005F)', text_node)

            for m in matches:
                #print(f"Found: {repr(m.group())} at position {m.start()}")
                with open(directory_path + "repeated_char.htm", "a", encoding="utf-8") as f:
                   f.write(f"{file}\t{text_node.parent.sourceline}:{m.start()}\t{text_node.parent}\tFound: {repr(m.group())}\n")
    
def drop_cap():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for tag in soup.find_all():
            if tag.string and re.match(r"^[A-Za-z]$", tag.string.strip()):
                with open(directory_path + "drop_cap.htm", "a", encoding="utf-8") as f:
                   f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{tag}{tag.next_sibling}\n" )
        for smalltag in soup.find_all("small"):
            print(smalltag)
            with open(directory_path + "small_tag.htm", "a", encoding="utf-8") as f:
               f.write(f"{file}\t{smalltag.sourceline}:{smalltag.sourcepos}\t{smalltag}{smalltag.next_sibling}\n" )
            


def check_math_followed_img():
    import re
    import os
    from bs4 import BeautifulSoup, Comment
    from PIL import Image

    img_folder = r"D:\\link\\chapter\\images"
    xhtml_folder = r"D:\\link\\chapter\\"

    # ---- Image files ----
    imgfiles = [f for f in os.listdir(img_folder) if f.endswith(".png")]

    rerun_img_file_count = len(imgfiles)

    for imgfile in imgfiles:
        img_path = os.path.join(img_folder, imgfile)
        with Image.open(img_path) as img:
            rounded = round(img.height / 34, 2)
            print(f"{imgfile} → {rounded}")

    # ---- XHTML processing ----
    rerun_math = 0
    rerun_img = 0

    for file in os.listdir(xhtml_folder):
        if file.endswith((".xhtml", ".html")):

            with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            comments = soup.find_all(string=lambda t: isinstance(t, Comment))

            for comment in comments:
                if "<math" in comment and "</math>" in comment:

                    comment_soup = BeautifulSoup(comment, "html.parser")
                    math = comment_soup.find("math", class_="rerun")

                    if math:
                        rerun_math += 1

                        # ✅ get next actual tag (skip text/newlines)
                        next_tag = comment.find_next_sibling()

                        if next_tag and next_tag.name == "img":
                            rerun_img += 1

    # ---- Result ----
    if rerun_math == rerun_img == rerun_img_file_count:
        print(f"PASS: math={rerun_math}, img tag={rerun_img}, img files={rerun_img_file_count}")
        #replace_block()
      
    else:
        print(f"FAIL: math={rerun_math}, img tag={rerun_img}, img files={rerun_img_file_count}")
        
def notes():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        notes = soup.find_all(class_='fn')
        for note in notes:
            with open(directory_path + "notes.htm", "a", encoding="utf-8") as f:
               f.write(f"{file}\t{note.sourceline}:{note.sourcepos}\t{note}\n" )
        
def inline_styles():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    styles = set()
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        for tag in soup.find_all(style=True):
            style_1 = tag['style'].strip()
            styles.add(tag['style'].strip())
            with open(directory_path + "inline_style.htm", "a", encoding="utf-8") as f:
               f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t{style_1}\n" )

    for s in sorted(styles):
        with open(directory_path + "inline_style_uniq.htm", "a", encoding="utf-8") as f:
           f.write(f"{file}\t{s}\n" )


def img_transparent():
    import os
    from PIL import Image

    folder = r"D:/link/images/"  # your folder path

    for file in os.listdir(folder):
        if file.lower().endswith(".png"):
            path = os.path.join(folder, file)

            img = Image.open(path).convert("RGBA")
            alpha = img.getchannel("A")

            if alpha.getextrema()[0] < 255:
                #print("Transparent:", file)
                with open(xhtml_folder + "Transparent_img.htm", "a", encoding="utf-8") as f:
                   f.write(f"{file}\n" )
            

def Breaks_Inside_Headers():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all('br')
        for pagebreak in pagebreaks:
                if pagebreak.find_parent(re.compile(r'^h\d$')):
                    line, col = pagebreak.sourceline, pagebreak.sourcepos
                    with open(directory_path + "break.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{line}:{col}\t{pagebreak}\n" )
                    print(f"{pagebreak} found inside the header")

def duplicate_pageid():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        pagesid=[]
        for pagebreak in pagebreaks:
            pageid = pagebreak.get('id')
            pagesid.append(pageid)
        for all_pageid in pagesid:
            print(all_pageid)
            with open(directory_path+"all_pageid.htm", "a", encoding="utf-8") as fs:
                fs.write(f"{all_pageid}\n")

def alt_length():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        alt_texts = soup.find_all(attrs={"alt":True})
        for alt_text in alt_texts:
            alt_text_value = alt_text['alt']
            alt_length = len(alt_text_value)
            if alt_length > 200:
                with open(directory_path + "alt-text_length_output.htm", "a", encoding="utf-8") as f:
                    f.write(f"XHTML_{file}\t{alt_text.sourceline}:{alt_text.sourcepos}\t{alt_text}\t{alt_text_value}\t{alt_length}\n")
                #print(alt_length)
            else:
                with open(directory_path + "alt-text_length_lessthan_200.htm", "a", encoding="utf-8") as f:
                    f.write(f"XHTML_{file}\t{alt_text.sourceline}:{alt_text.sourcepos}\t{alt_text}\t{alt_text_value}\t{alt_length}\n")
                #print(alt_length)

def italic_length():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        italic_texts = soup.find_all(['i','em'])
        for italic_text in italic_texts:
            text = italic_text.get_text(strip=True)
            italic_text_length = len(text)
            
            with open(directory_path + "italic_length.htm", "a", encoding="utf-8") as f:
                f.write(f"{file}\t{italic_text.sourceline}:{italic_text.sourcepos}\t{italic_text.string}\t{italic_text_length}\n")
            

def math_namespace():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        maths = soup.find_all('math', attrs={'xmlns':False})
        for math in maths:
            #print('{math}')
            line, col = math.sourceline, math.sourcepos
            with open(directory_path + "xmlns_math.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file}\t{line}\txmlns="http://www.w3.org/1998/Math/MathML" is missing<br/>\n''')

        math_ns = soup.find_all(attrs={'xmlns:m':"http://www.w3.org/1998/Math/MathML"})
        for math_namespace in math_ns:
            line, col = math_namespace.sourceline, math_namespace.sourcepos
            with open(directory_path + "xmlns_math_found.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file}\t{line}:{col}\t{math_namespace.name}\n''')
            
        

def alt_none():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")


        alt_texts = soup.find_all(attrs={"alt":True})
        for alt_text in alt_texts:
            alt_text_value = alt_text['alt']
            alt_text_value_length = len(alt_text_value)
            if alt_text_value == "":
                with open(directory_path + "None_alttext.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{alt_text_value}\t{alt_text}\n")
            else:
                with open(directory_path + "Image_alttext.htm", "a", encoding="utf-8") as f:
                    f.write(f"{file}\t{alt_text_value}\t{alt_text}\t{alt_text_value_length}\n")


def back_linkd():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

            # Collect all IDs
            ids = {tag.get("id") for tag in soup.find_all(attrs={"id": True})}

            errors = []

            # Check all anchor links
            for a in soup.find_all("a", href=True):

                href = a["href"]

                if href.startswith("#"):
                    target_id = href[1:]

                    if target_id not in ids:
                        errors.append(f"Broken link: {href}")

            # Check doc-backlink specifically
            for a in soup.find_all("a", href=True):
                line = a.sourceline
                pos = a.sourcepos
                href = a["href"]

                if href.startswith("#"):
                    target_id = href[1:]

                    # Detect rc pattern (backlink target)
                    if target_id.startswith("rc"):
                        if a.get("role") != "doc-backlink":
                            errors.append(f"Missing doc-backlink role: {href}")
                            with open(directory_path + "backlink_not_applied.htm", "a", encoding="utf-8") as f:
                                f.write(f"{file}\t{line}:{pos}\t{href}\n")

            # Write results
            if errors:
                print(f"\nFILE: {file}\n")
                for err in errors:
                    print(f"{err}\n")

    print("✅ Validation completed!")
    with open(directory_path + "backlink_not_applied.htm", "a", encoding="utf-8") as f:
        f.write(f"Task Completed\n")

def opf_meta_Hazard():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".opf"):
            files.append(file)
            print(f"opf file {file} found")
        else:
            pass
            #print(f"Non opf file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        hazards = soup.find_all("meta", {"property": "schema:accessibilityHazard"})
        values = [tag.text.strip() for tag in hazards]
        required = {
            "noFlashingHazard",
            "noMotionSimulationHazard",
            "noSoundHazard"
        }
        if "none" in values:
             print("Warning: 'none' is not recommended")
        if required.issubset(set(values)):
            print("Correct: All required hazard metadata present")
        else:
            missing = required - set(values)
            print("Missing:", missing)

def math_alttext():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        alt_texts = soup.find_all(attrs={"alttext":True})
        for alt_text in alt_texts:
            alt_text_value = alt_text['alttext']
            with open(directory_path + "math_alttext.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file}\t{alt_text.sourceline}:{alt_text.sourcepos}\t{alt_text}\t<span style="color:Red">{alt_text_value}</span><br/>\n''')
def math_Fallback_image():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        alt_texts = soup.find_all('math')
        for alt_text in alt_texts:
            alt_text_value = alt_text['altimg']
            with open(directory_path + "math_Fallback_image.htm", "a", encoding="utf-8") as f:
                f.write(f'''<p>{file}\t{alt_text.sourceline}:{alt_text.sourcepos}\t{alt_text}<br/><img src="{alt_text_value}"/><br/></p>\n''')


def opf_accessibilityFeature():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".opf"):
            files.append(file)
            print(f"opf file {file} found")
        else:
            pass
            #print(f"Non opf file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        hazards = soup.find_all("meta", {"property": "schema:accessibilityFeature"})
        values = [tag.text.strip() for tag in hazards]
        values_set = set(values)
        required = {
            "alternativeText",
            "displayTransformability",
            "highContrastDisplay",
            "index",
            "longDescription",
            "pageBreakMarkers",
            "pageNavigation",
            "readingOrder",
            "structuralNavigation",
            "tableOfContents",
            "unlocked",
            "describedMath",
            "MathML",
            "ARIA",

        }
        if required.issubset(set(values)):
            print("Correct: All required schema:accessibilityFeature metadata present")
        else:
            missing = required - set(values)
            print(f"Missing: {missing} \n")

        additional = values_set - required
        if additional:
            print(f"INFO: Additional values found: {additional}\n")

def math_deprecated():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    deprecated = ["mathcolor", "mathbackground", "mathsize", "displaystyle", "scriptlevel"]

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        for tag in soup.find_all(True):
            for attr in deprecated:
                if tag.has_attr(attr):
                    #print(f"<{tag.name}> uses deprecated attribute '{attr}'")
                    with open(directory_path + "math_deprecated.htm", "a", encoding="utf-8") as f:
                        f.write(f"{file}\t{tag.sourceline}:{tag.sourcepos}\t<{tag.name}> uses deprecated attribute '{attr}'\n")

def show_hide_link():
    import difflib
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        aria_lbls = soup.find_all(attrs={"aria-controls":True})
        all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}
        for aria_lbl in aria_lbls:
            aria_lbl_id = aria_lbl['aria-controls']
            element = soup.find(id=aria_lbl_id)
            aria_lbl_text = aria_lbl.find_next().text.strip()
            print(aria_lbl_id)
            aria_lbl_linked_text = element.text.strip()
                
def new_line():
    directory_path_output = 'D:\\link\\chapter\\output\\'
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        file_name = file.split(".xhtml")
        print(file_name)
        # Define block elements
        block_elements = [
            "p", "div", "section","figure", "h1", "h2", "h3", "h4", "h5", "h6", "aside",
            "ul", "ol", "li", "table", "tr", "blockquote"
        ]

        for tag in soup.find_all(block_elements):
            tag.insert_before("\n")
            tag.insert_after("\n")

        #print(soup.prettify())
        with open(directory_path_output + file_name[0] + "_output" + ".xhtml", "a", encoding="utf-8") as f:
            f.write(str(soup))

def page_break_each():
    directory_path_output = 'D:\\link\\chapter\\'
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        pagebreak = soup.find(attrs={"epub:type":"pagebreak"})
        if pagebreak is None:
            print(f"Error: At least one page break marker is required per chapter in {file}.")
            
def back_link():
    directory_path_output = 'D:\\link\\chapter\\'
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        backlinks = soup.find_all(attrs={"role":"doc-backlink"})
        for backlink in backlinks:
            p1 = backlink.parent
            p2 = p1.parent if p1 else None
            p3 = p2.parent if p2 else None
            p4 = p3.parent if p3 else None
            with open(directory_path + "backlink.htm", "a", encoding="utf-8") as f:
                f.write(
                    f"{file}\t"
                    f"{backlink.sourceline}:{backlink.sourcepos}\t"
                    f"{backlink}\t"
                    f"{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                )

def pagebreak_missing():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    missing_files = set()
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreak_atleast = soup.find(attrs={'epub:type':'pagebreak'})

        if pagebreak_atleast is None:
            missing_files.add(file)
    with open(directory_path + "pagebreak_missing.htm", "a", encoding="utf-8") as f:
        f.write(f'''{missing_files} doesn't has pagebreak marker\n''')

def Emphasis_Bolding():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        bold_italics = soup.find_all(['b', 'i', 'strong', 'em'])
        for bold_italic in bold_italics:
            p1 = bold_italic.parent
            p2 = p1.parent if p1 else None
            p3 = p2.parent if p2 else None
            p4 = p3.parent if p3 else None

            if bold_italic.name == "strong":
                with open(directory_path + "Emphasis_strong.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{file}\t{bold_italic.sourceline}:{bold_italic.sourcepos}\t{bold_italic}'''
                    f"\t{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"\t{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"\t{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"\t{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                            )
            elif bold_italic.name == "em":
                with open(directory_path + "Emphasis_em.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{file}\t{bold_italic.sourceline}:{bold_italic.sourcepos}\t{bold_italic}'''
                    f"\t{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"\t{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"\t{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"\t{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                            )
            elif bold_italic.name == "i":
                with open(directory_path + "Emphasis_talic.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{file}\t{bold_italic.sourceline}:{bold_italic.sourcepos}\t{bold_italic}'''
                    f"\t{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"\t{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"\t{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"\t{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                            )
            elif bold_italic.name == "b":
                with open(directory_path + "Emphasis_Bolding.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{file}\t{bold_italic.sourceline}:{bold_italic.sourcepos}\t{bold_italic}'''
                    f"\t{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"\t{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"\t{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"\t{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                            )


def Roman_numerals_match():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pagebreaks = soup.find_all(attrs={'epub:type':'pagebreak'})
        for pagebreak in pagebreaks:
            pagebreak_id = pagebreak.get('id')
            aria_label = pagebreak.get('aria-label')
            id_split = pagebreak_id.split('Page_')[1]
            if id_split != aria_label:
                print(f'''Page marker mismatch: {id_split} does not match {aria_label}''')
                with open(directory_path + "Roman_numerals_match.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{file}\t{pagebreak.sourceline}:{pagebreak.sourcepos}'''
                            f'''\t{pagebreak}\tPage marker mismatch: '{id_split}' does not match '{aria_label}'\n''')
                
    with open(directory_path + "Roman_numerals_match.htm", "a", encoding="utf-8") as f:
        f.write(f'''Task completed''')

def Meaningful_Link_Text():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    
    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        a_tags = soup.find_all('a')
        for a_tag in a_tags:
            p1 = a_tag
            p2 = p1.parent if p1 else None
            p3 = p2.parent if p2 else None
            p4 = p3.parent if p3 else None

            a_tag_text = a_tag.text
            with open(directory_path + "Meaningful_Link_Text.htm", "a", encoding="utf-8") as f:
                f.write(f'''{file}\t{a_tag.sourceline}:{a_tag.sourcepos}\t'''
                        f'''{a_tag_text}\t'''
                    f"{p1.name if p1 else None}:{p1.get('class') if p1 else None}\t"
                    f"{p2.name if p2 else None}:{p2.get('class') if p2 else None}\t"
                    f"{p3.name if p3 else None}:{p3.get('class') if p3 else None}\t"
                    f"{p4.name if p4 else None}:{p4.get('class') if p4 else None}\n"
                        )
def OPF_cover_image_meta():

    files = []
    Nonfiles = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".opf"):
            files.append(file)
            #print(f"opf file {file} found")
        else:
            Nonfiles.append(file)

    print(f"OPF files: {files}")
    print(f"Non OPF files: {Nonfiles}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        cover_metas = soup.find_all('meta', attrs={'name': 'cover'})

        if cover_metas:
            for cover_meta in cover_metas:

                cover_meta_id = cover_meta.get('content')

                if not cover_meta_id:
                    continue

                cover_image_tag = soup.find(id=cover_meta_id)

                if cover_image_tag is None:
                    print("FAIL: Cover image item was not found in manifest")
                    continue

                cover_image_properties = cover_image_tag.get('properties', '')

                if "cover-image" == cover_image_properties:
                    print(f"PASS: The cover image was correctly identified using the “cover-image” property in the manifest")
                else:
                    print(f'''FAIL: The cover image was incorrectly "{cover_image_properties}" identified instead “cover-image” property in the manifest''')

                    with open(directory_path + "OPF_cover_image_meta.htm", "a", encoding="utf-8") as f:
                        f.write(
                            f'''FAIL: The cover image was incorrectly "{cover_image_properties}" identified instead “cover-image” property in the manifest\n'''
                        )
        else:
            print("Missing!!!")
            with open(directory_path + "OPF_cover_image_meta.htm", "a", encoding="utf-8") as f:
                f.write(
                    f"Missing: <meta name=“cover” content=“cover-image”/> \n"
                )



    with open(directory_path + "OPF_cover_image_meta.htm", "a", encoding="utf-8") as f:
        f.write(f'''Task completed\n''')

def figure_info():
    files = []
    for file in os.listdir(xhtml_folder):
        if file.endswith(".xhtml") or file.endswith(".html"):
            files.append(file)
        else:
            print(f"Non xhtml file {file}")

    for file in files:
        with open(os.path.join(xhtml_folder, file), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        figure = soup.find_all('figure')
        with open(directory_path + "figure.htm", "a", encoding="utf-8") as f:
            f.write(f'''{figure}\n''')


##figure_info()
##new_line()
##show_hide_link()
##alt_none()        
##alt_length()
##Emphasis_Bolding()
##check_math_followed_img()
##test()
##pageTitle()
##inline_styles()
##css_disallowed()
##Breaks_Inside_Headers()
##Bold_italic_formating_H()                
##aria_label()
##aria_labelledby()
##len_aria_labelledby()
##aria_describedby()    
##drop_cap()
##all_caps_texts()
##italic_length()
##br_Body()
##repeated_char()
##lang_detect()
##Nav_TOC()
##hidden()
##pagebreak_missing()
##Roman_numerals_match()
##consecutive_pagebreak()
##Page_List()
##unique_page_label()
##Page_Breaks_newformat()    
##duplicate_pageid()
##http_link()
##Meaningful_Link_Text()
##back_linkd()
##back_link()
notes()
noteref()
##para_ul_list()
##para_decimal_list()        
##para_alpha_list()        
##para_roman_list()        
##all_List()
##all_table()
##math_namespace()
##all_epub_type()            
##all_role_type()
##Page_Breaks_Inside_Headers()
##math_deprecated()
##single_column_table()
##Unicode_normalization()            
##aside_untitled_section()
##untitled_section()
##Redundant_title_aria()
##mandate_tags()
##th_empty()
##span_bold()
##span_italic()
##img_transparent()
##math_alttext()            
##page_break_each()
##math_Fallback_image()
##OPF_cover_image_meta()
##opf_accessibilityFeature()
##opf_meta_Hazard()


print("Done!!!")
