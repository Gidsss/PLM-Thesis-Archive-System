from django.core.management.base import BaseCommand
from faker import Faker
from archive_app.models import User, Document
from fpdf import FPDF
import random, os
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

          # Define the media/documents path
        base_media_path = 'media'
        documents_path = os.path.join(base_media_path, 'documents')
        os.makedirs(documents_path, exist_ok=True)  # Create directory if not exists

        # Clear existing data
        User.objects.all().delete()
        Document.objects.all().delete()

        self.stdout.write("Seeding users...")

        # Create Admin User
        User.objects.create_superuser(
            email='admin@example.com',
            password='password',
            full_name='Admin User',
            role='admin'
        )

        # Create Students with specific names and emails
        students = [
            {'name': 'Gideon', 'email': 'gideon@plm.com'},
            {'name': 'Melissa', 'email': 'melissa@plm.com'},
            {'name': 'Jayson', 'email': 'jayson@plm.com'},
            {'name': 'Markcy', 'email': 'markcy@plm.com'},
            {'name': 'Dawn', 'email': 'dawn@plm.com'}
        ]
        student_users = []
        for student in students:
            user = User.objects.create_user(
                email=student['email'],
                password='password',
                full_name=student['name'],
                role='student'
            )
            student_users.append(user)

        self.stdout.write("Seeding documents...")

        # Predefined list of computer-related thesis titles
        thesis_data = [
            {
                "title": "Development of an AI-Powered Chatbot for E-Learning Platforms",
                "keywords": "AI, Chatbot, E-Learning, Natural Language Processing, Automation"
            },
            {
                "title": "A Machine Learning Approach to Detecting Cybersecurity Threats",
                "keywords": "Machine Learning, Cybersecurity, Threat Detection, Anomaly Detection, AI"
            },
            {
                "title": "Blockchain-Based Identity Verification for Secure Transactions",
                "keywords": "Blockchain, Identity Verification, Secure Transactions, Decentralization, Cryptography"
            },
            {
                "title": "Augmented Reality Applications in Online Retail Systems",
                "keywords": "Augmented Reality, Online Retail, Virtual Shopping, AR Applications, User Experience"
            },
            {
                "title": "Implementation of a Cloud-Based File Sharing Platform Using Zero-Knowledge Encryption",
                "keywords": "Cloud Computing, File Sharing, Zero-Knowledge Encryption, Security, Data Privacy"
            },
            {
                "title": "A Study on the Efficiency of Quantum Computing Algorithms for Cryptography",
                "keywords": "Quantum Computing, Cryptography, Algorithms, Quantum Efficiency, Encryption"
            },
            {
                "title": "Design and Development of a Mobile App for Mental Health Tracking",
                "keywords": "Mobile App, Mental Health, Tracking, User Interface, Health Monitoring"
            },
            {
                "title": "Big Data Analytics for Enhancing Customer Experience in E-Commerce",
                "keywords": "Big Data, Analytics, Customer Experience, E-Commerce, Data Mining"
            },
            {
                "title": "IoT-Based Smart Home Automation System with Security Features",
                "keywords": "IoT, Smart Home, Automation, Security, Sensors"
            },
            {
                "title": "Development of a Deep Learning Model for Automated Medical Image Diagnosis",
                "keywords": "Deep Learning, Medical Imaging, Automated Diagnosis, AI, Neural Networks"
            }
        ]

        # Generate PDF Files and Create Documents
        used_titles = set()  # Keep track of used titles
        for i in range(10):  # Create 10 documents
             # Ensure unique titles
            thesis = random.choice(thesis_data)
            while thesis["title"] in used_titles:
                thesis = random.choice(thesis_data)
            used_titles.add(thesis["title"])

             # Generate a PDF file
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Title: {thesis['title']}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Abstract: {fake.paragraph()}", ln=True, align="L")
            file_name = f"thesis_{i + 1:02}.pdf"
            file_path = os.path.join(documents_path, file_name)
            pdf.output(file_path)

            # Create Document object
            Document.objects.create(
                title=thesis["title"],
                abstract=fake.paragraph(),
                publication_date=date.today() - timedelta(days=random.randint(0, 1000)),
                document_type=random.choice(['Thesis', 'Dissertation', 'Research Paper']),
                degree_name=random.choice(['Bachelor of Science', 'Master of Science', 'PhD']),
                subject_categories=random.choice(["AI", "Cybersecurity", "Blockchain"]),
                college=fake.company(),
                department=random.choice(['Computer Science', 'Information Technology']),
                advisor=fake.name(),
                panel_members=', '.join([fake.name() for _ in range(3)]),
                keywords=thesis["keywords"],
                language=random.choice(['English', 'Filipino', 'Spanish']),
                file_path=os.path.relpath(file_path, base_media_path),  # Assign the generated file path
                uploaded_by=random.choice(student_users),
                status=random.choice(['Pending', 'Approved'])
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
