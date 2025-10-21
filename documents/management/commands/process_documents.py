from django.core.management.base import BaseCommand
from documents.models import Document
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Process uploaded documents'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Process documents for a specific user email',
        )
        parser.add_argument(
            '--file-type',
            type=str,
            help='Filter by file type (txt, md, pdf, doc, docx)',
        )
        parser.add_argument(
            '--list-only',
            action='store_true',
            help='Only list documents without processing',
        )

    def handle(self, *args, **options):
        # Filter documents
        documents = Document.objects.all()

        if options['user_email']:
            try:
                user = User.objects.get(email=options['user_email'])
                documents = documents.filter(owner=user)
                self.stdout.write(f"Filtering documents for user: {user.email}")
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User not found: {options['user_email']}"))
                return

        if options['file_type']:
            documents = documents.filter(file_type=options['file_type'])
            self.stdout.write(f"Filtering by file type: {options['file_type']}")

        total_docs = documents.count()
        self.stdout.write(self.style.SUCCESS(f"\nFound {total_docs} document(s)\n"))

        # List documents
        for doc in documents:
            self.stdout.write("-" * 80)
            self.stdout.write(f"ID: {doc.id}")
            self.stdout.write(f"Name: {doc.name}")
            self.stdout.write(f"Type: {doc.file_type}")
            self.stdout.write(f"Size: {doc.get_readable_size()}")
            self.stdout.write(f"Owner: {doc.owner.email}")

            # Show full folder path
            if doc.folder:
                folder_path = doc.folder.get_full_path()
                self.stdout.write(f"Folder: {folder_path}")
            else:
                self.stdout.write(f"Folder: My Documents (Root)")

            self.stdout.write(f"File Path: {doc.file.path}")
            self.stdout.write(f"Uploaded: {doc.uploaded_at}")

            if not options['list_only']:
                # Process the document here
                self.stdout.write(f"\n{self.style.WARNING('Processing...')}")

                # Example: Read file content
                try:
                    if doc.file_type in ['txt', 'md']:
                        with open(doc.file.path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.stdout.write(f"Content preview (first 200 chars):")
                            self.stdout.write(content[:200])
                    elif doc.file_type == 'pdf':
                        self.stdout.write("PDF file - use PyPDF2 or pdfplumber to extract text")
                    elif doc.file_type in ['doc', 'docx']:
                        self.stdout.write("Word file - use python-docx to extract text")

                    self.stdout.write(self.style.SUCCESS("✓ Processed successfully"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"✗ Error processing: {str(e)}"))

            self.stdout.write("")

        self.stdout.write(self.style.SUCCESS(f"\nTotal processed: {total_docs}"))
