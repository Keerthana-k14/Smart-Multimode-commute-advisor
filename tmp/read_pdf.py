import PyPDF2
import sys

def extract_text(pdf_path, output_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text() + '\n'
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(text)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    extract_text(sys.argv[1], sys.argv[2])
