from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
# Set your expiry date (YYYY, MM, DD)
expiry_date = datetime(2026, 12, 24)
current_date = datetime.now()
if current_date > expiry_date:
    print("This script has expired. Please contact the developer.")
    exit()  # stop script
else:
    print("Script active. Running...")

directory = 'd:\\link\\chapter\\'
for xhtmlfile in os.listdir(directory):
    if xhtmlfile.endswith(".xhtml"):
        # Build the full file path
        file_path = os.path.join(directory, xhtmlfile)
    with open(file_path, encoding='utf-8') as f:
        htmlfile = f.read()

    soup = BeautifulSoup(htmlfile, "html.parser")

    header_elements = soup.find_all('section')
    # Print the text content of each <header> element containing a heading
    def main_toc():
        for header in header_elements:
                heading = header.find(['h1', 'h2', 'h3'])
                
                if heading:
                    section = heading.find_parent('section')
                    
                    aside = heading.find_parent('aside')

                    if section:
                        section_id = section.get('id')
                        heading_name = heading.name
                        heading_name_id = heading.get('id')
                        
                        #print(f"Section ID: {section_id}")
                        with open(directory + "nav.xhtml", "a", encoding='utf-8') as f:
                          f.write(f'''<li class="{heading_name}"><a href="{xhtmlfile}#{heading_name_id}">{heading.text}</a></li>\n''')

                    '''if aside:
                        aside_id = aside.get('id')
                        heading_name = heading.name
                        print(f"Aside ID: {aside_id}")
                        with open("d:\\nav.txt", "a") as f:
                          f.write(f"\n{file_path}#{aside_id}\t{heading_name}")


                        #print(f"Header Text: {heading.text}\n")'''

    def lot():
        header_elements = soup.find_all('caption')
        for lof in header_elements:
            loi_parent = lof.parent
            loi_id = loi_parent.get('id')
            #print(loi_id)
            loi_text = lof.text
            #print(loi_text)
            with open(directory+"lot.htm", "a", encoding="utf-8") as f:
                f.write(f'''<li><a href="{xhtmlfile}#{loi_id}">{lof}</a></li>\n''')

    def loi():
        header_elements = soup.find_all('figcaption')
        for lof in header_elements:
            loi_parent = lof.parent
            if loi_parent.find('img'):
                loi_id = loi_parent.get('id')
                #print(loi_id)
                loi_text = lof.text
                #print(loi_text)
                with open(directory+"loi.htm", "a", encoding="utf-8") as f:
                    f.write(f'''<li><a href="{xhtmlfile}#{loi_id}">{lof}</a></li>\n''')
    def loi_table():
        header_elements = soup.find_all('figcaption')
        for lof in header_elements:
            loi_parent = lof.parent
            if loi_parent.find('table'):
                #print(loi_parent)
                loi_id = loi_parent.get('id')
                #print(loi_id)
                loi_text = lof.text
                #print(loi_text)
                with open(directory+"lot.htm", "a", encoding="utf-8") as f:
                    f.write(f'''<li><a href="{xhtmlfile}#{loi_id}">{lof}</a></li>\n''')

    def all_loi():
        header_elements = soup.find_all('figcaption')
        for lof in header_elements:
            loi_parent = lof.parent
            loi_id = loi_parent.get('id')
            loi_text = lof.text
            with open(directory+"loi_all.htm", "a", encoding="utf-8") as f:
                f.write(f'''<li><a href="{xhtmlfile}#{loi_id}">{lof}</a></li>\n''')

    def pagelist():
        pagelists = soup.find_all(attrs={'epub:type':'pagebreak'})
        try:
            for pagelist in pagelists:
                pg_id = pagelist['id']
                pg_id_split = pg_id.split('Page_')
                pg_num = pg_id_split[1]
                with open(directory + "pagelist.htm", "a", encoding="utf-8") as f:
                    f.write(f'''<li><a href="{xhtmlfile}#{pg_id}">{pg_num}</a></li>\n''')
                with open(directory + "pagelist_checkseq.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{xhtmlfile}\t{pg_id}\t{pg_num}\n''')
        except Exception as e:
            with open(directory + "Error.htm", "a", encoding="utf-8") as f:
                f.write(f'''{xhtmlfile}\t{pagelist}\t{e}\n<br></br>''')
                

    def image_list():
        images = soup.select('body img:not(annotation-xml img)')
        for img in images:
            img_src = img['src']
            # Split into parts
            folder, filename = os.path.split(img_src)
            name, ext = os.path.splitext(filename)
            with open("d:\\link\\image.htm", "a", encoding="utf-8") as f:
               f.write(f'''<item id="{name}" href="{img_src}" media-type="image/png" />\n''')
    def manifest_xhtml():
        xhtmlfile_split = xhtmlfile.split(".xhtml")
        file_name = xhtmlfile_split[0]
        with open(directory+"manifest_xhtml.opf", "a", encoding="utf-8") as f:
            f.write(f'''<item id="{file_name}" href="{file_name}.xhtml" media-type="application/xhtml+xml" properties="scripted"/>\n''')

    def spine_xhtml():
        xhtmlfile_split = xhtmlfile.split(".xhtml")
        file_name = xhtmlfile_split[0]
        with open(directory+"spine_xhtml.opf", "a", encoding="utf-8") as f:
            f.write(f'''<itemref idref="{file_name}" linear="yes"/>\n''')

            
        
    def table_not_nested_with_figure():
        tables = soup.find_all("table")
        for table in tables:
            if not any(table.find_parents('figure')):
                line, col = table.sourceline, table.sourcepos
                #print(line, col)
                with open(directory + "table_not_nested_with_figure.htm", "a", encoding="utf-8") as f:
                    f.write(f'''{xhtmlfile}\t{line, col}\n''')


    
    main_toc()
    lot()
    loi()
    loi_table()
    all_loi()
    pagelist()
    image_list()
    manifest_xhtml()
    spine_xhtml()
    table_not_nested_with_figure()

    
def unused_img():
    with open("d:\\link\\image.htm", "r+", encoding="utf-8") as f:
        img_lists = f.read()
        soup = BeautifulSoup(img_lists, "html.parser")
        img_name_c = []
        img_items = soup.find_all("item")
        for img_item in img_items:
            img_name_f = img_item.get('href')
            img_name = img_name_f.split('images/')
            img_name_c.append(img_name[1])
        #print(img_name_c)
        
    directory_path = 'd:\\link\\images\\'
    images = []
    for pngfile in os.listdir(directory_path):
        images.append(pngfile)
    for image in images:
        if image in img_name_c:
            pass
        else:
            with open(directory + "unused_imagelist.txt", "a", encoding="utf-8") as f:
                f.write(f'''{image}\t is unused\n''')
        


unused_img()

with open(directory + "finished.txt", "a", encoding="utf-8") as f:
    f.write(f'''task completed''')

print("finished")

