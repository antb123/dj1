#!/usr/bin/env python
"""
Script to process uploaded documents.
Example usage:
    python process_files.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'document_manager.settings')
django.setup()

from documents.models import Document


def process_documents():
    """Process all uploaded documents."""
    documents = Document.objects.all()

    print(f"Found {documents.count()} documents\n")

    for doc in documents:
        print(f"{'='*80}")
        print(f"Processing: {doc.name}")
        print(f"Type: {doc.file_type}")
        print(f"Owner: {doc.owner.email}")
        print(f"Path: {doc.file.path}")
        print(f"{'='*80}\n")

        try:
            # Read and process based on file type
            if doc.file_type in ['txt', 'md']:
                with open(doc.file.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"Content length: {len(content)} characters")
                    print(f"First 200 characters:\n{content[:200]}\n")

            elif doc.file_type == 'pdf':
                print("PDF file detected")
                # To process PDFs, install: pip install PyPDF2
                # Example:
                # import PyPDF2
                # with open(doc.file.path, 'rb') as f:
                #     pdf = PyPDF2.PdfReader(f)
                #     text = ''.join(page.extract_text() for page in pdf.pages)
                print("Install PyPDF2 to extract text from PDFs\n")

            elif doc.file_type in ['doc', 'docx']:
                print("Word document detected")
                # To process Word docs, install: pip install python-docx
                # Example:
                # import docx
                # doc_file = docx.Document(doc.file.path)
                # text = '\n'.join(paragraph.text for paragraph in doc_file.paragraphs)
                print("Install python-docx to extract text from Word documents\n")

            # Add your custom processing logic here
            # For example:
            # - Extract text content
            # - Run NLP analysis
            # - Generate summaries
            # - Extract metadata
            # - Convert formats
            # etc.

        except Exception as e:
            print(f"Error processing {doc.name}: {str(e)}\n")

    print(f"Processing complete!")


if __name__ == '__main__':
    process_documents()
