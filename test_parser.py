from app.parser import parse_file

file_path = r"C:\resume\Official Resume.docx"   
text = parse_file(file_path)
print(text)
