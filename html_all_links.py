import shutil
import requests
import difflib
import os
import re
from datetime import datetime
# Set your expiry date (YYYY, MM, DD)
expiry_date = datetime(2026, 5, 24)
current_date = datetime.now()
if current_date > expiry_date:
    print("Version Updated. Please contact the developer.")
    exit()  # stop script
else:
    print("Running...")
    
directory = 'D:\\link\\chapter\\'
output_path = 'D:\\link\\External_link\\'

# Delete directory if it exists
if os.path.exists(output_path):
    shutil.rmtree(output_path)

# Create new directory
os.makedirs(output_path)

for xhtmlfile in os.listdir(directory):
    if xhtmlfile.endswith("html"):
        # Build the full file path
        file_path = os.path.join(directory, xhtmlfile)
    with open(file_path, encoding="utf-8", errors="ignore") as f:
        htmlfile = f.read()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmlfile, 'html.parser')
    # Find all elements with id attributes in the current document
    print(f"{xhtmlfile} is progress ...")

    all_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}

    # Find all <a> tags
    a_tags = soup.find_all('a')

    # Check if href is a valid id reference or an external link
    for a_tag in a_tags:
        href = a_tag.get('href')
        try:
            if href and '#' in href:
                if href.startswith('#'):
                    file_name = href.split('#')[0]
                    sid_ref = href.split('#')[1] if '#' in href else None
                    if sid_ref in all_ids:
                        #print(f"same filename {file_name}: {href}")
                        #print("same html", a_tag)
                        same_file_ids = {tag.get('id') for tag in soup.find_all(attrs={"id": True})}
                        if sid_ref in same_file_ids:
                            #print("same_file_ids", sid_ref)
                            element = soup.find(id=sid_ref)
                            first_text = element.get_text()
                            a_tag_text = a_tag.text
                            differ = difflib.Differ()
                            diff = list(differ.compare(first_text.lower().split(), a_tag_text.lower().split()))
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
                            line, col = a_tag.sourceline, a_tag.sourcepos
                            with open(directory+xhtmlfile+"_all_link.htm", "a", encoding="utf-8") as fs:
                                fs.write(f'''<p>{xhtmlfile}\t{line}:{col}\t{a_tag}\t<-->\t<span class="IDREF">{first_text}</span><br/><span class="DIFF">{jointext1_text2}</span></p>\n''')
                    else:
                        #print(f"Invalid ID reference: {href}")
                        line, col = a_tag.sourceline, a_tag.sourcepos
                        with open(directory+"RSC-012_Error.htm", "a", encoding="utf-8") as fs:
                            fs.write(f"{xhtmlfile}\t{line}:{col}:RSC-012: Fragment identifier is not defined.\t{a_tag}\n<br></br>")
                        
                    
                else:
                    #print(a_tag)
                    file_name = href.split('#')[0]
                    id_ref2 = href.split('#')[1] if '#' in href else None
                    linked_file_path = os.path.join("D:\\link\\all_xhtml\\", file_name)
                    try:
                        with open(linked_file_path, encoding="utf-8", errors="ignore") as f:
                                other_htmlfile = f.read()
                        soup2 = BeautifulSoup(other_htmlfile, 'html.parser')
                        
                        other_file_ids = {tag.get('id') for tag in soup2.find_all(attrs={"id": True})}
                        if id_ref2 in other_file_ids:
                            #print("id_ref", id_ref2)
                            element2 = soup2.find(id=id_ref2)
                            first_text2 = element2.get_text()
                            a_tag_text = a_tag.text
                            differ = difflib.Differ()
                            diff = list(differ.compare(first_text2.lower().split(), a_tag_text.lower().split()))
                            #print(diff)
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
                            line, col = a_tag.sourceline, a_tag.sourcepos
                            with open(directory+xhtmlfile+"_all_link.htm", "a", encoding="utf-8") as fs:
                                fs.write(f'''<p>{xhtmlfile}\t{line}:{col}\t{a_tag}\t<-->\t<span class="IDREF">{first_text2}</span><br/><span class="DIFF">{jointext1_text2}</span></p>\n''')
                            #else:    
                                #line, col = a_tag.sourceline, a_tag.sourcepos
                                #with open(directory+xhtmlfile+"_all_link.htm", "a", encoding="utf-8") as fs:
                                    #fs.write("<p>" + str(xhtmlfile) +"\t" + str(line) + ":" + str(col)+ "\t" + str(a_tag) + '''<br><span style="color:red"> ''' + str(first_text2) + "</p>\n")
                        else:
                            line, col = a_tag.sourceline, a_tag.sourcepos
                            with open(directory+"invalidlink.htm", "a", encoding="utf-8") as fs:
                                fs.write("<p>" + str(xhtmlfile)+ "\t" + str(line) + ":" + str(col)+ "\t" + str(a_tag) + "\n")

                    except Exception as e:
                        with open(directory+"Hash_weblink.htm", "a", encoding="utf-8") as fs:
                            fs.write(f"<p>{xhtmlfile}\t{line}:{col}\t{a_tag}\n<br></br>")

            else:
                try:
                    if href.startswith('http') or href.startswith('//') or 'www.' in href:
##                        r = requests.get(href)
##                        errorcode = r.status_code
                        line, col = a_tag.sourceline, a_tag.sourcepos
                        with open(output_path+"External_link.html", "a", encoding="utf-8") as fs:
                            fs.write(f'''<p>{xhtmlfile}\t{line}:{col}:\t{a_tag}<br></br></p>\n''')
                    else:
                        with open(directory+"NO_LINK.htm", "a", encoding="utf-8") as fs:
                            fs.write(f"{xhtmlfile}\t{line}:{col}\t{href}\t{a_tag}<br />\n")
                except Exception as e:
                    line, col = a_tag.sourceline, a_tag.sourcepos
                    with open(directory+"URLERROR.htm", "a", encoding="utf-8") as fs:
                        fs.write(f"{xhtmlfile}\t{line}:{col}\t{href}\t{a_tag}<br />\n")
                    print(e, "-> URLERROR")

        except Exception as e:
            line, col = a_tag.sourceline, a_tag.sourcepos
            with open(directory+"link_has_no_HASH_HREF_check_manually.htm", "a", encoding="utf-8") as fs:
                fs.write(f"{xhtmlfile}\t{line}:{col}\t{e}\t{a_tag}<br />\n")
                

print("Finished")


with open(directory+"finished.htm", "a", encoding="utf-8") as fs:
    fs.write("Task completed")

