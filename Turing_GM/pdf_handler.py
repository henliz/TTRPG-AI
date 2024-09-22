import PyPDF2

class PDFStoryHandler:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = None
        self.pages_text = []  # List to store text from each page
        self._load_pdf()

    def _load_pdf(self):
        """Load the PDF file into a PdfReader object and extract text from each page."""
        with open(self.pdf_path, 'rb') as pdf_file:
            self.reader = PyPDF2.PdfReader(pdf_file)
            print(f"debug:{len(self.reader.pages)}")
            for page_num in range(len(self.reader.pages)):
                page = self.reader.pages[page_num]
                text = page.extract_text()  # Extract text from the page
                print(f"debug:{text}")
                self.pages_text.append(text)  # Store text in the list

    def search(self, query):
        """Search for a query in the PDF and return the first few pages containing it."""
        results = []
        for page in self.pages_text:
            if page and query.lower() in page.lower():
                results.append(page)
        return "\n".join(results[:5])  # Return the first few pages containing the query


test=PDFStoryHandler(r"C:\Users\Henrietta\PycharmProjects\TTRPG-AI\Campaigns\DnD\curse_of_strahd.pdf")
results=test.search("the")
print(results)