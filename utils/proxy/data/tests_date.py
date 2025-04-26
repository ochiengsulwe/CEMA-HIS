from models.diagnostics.category import DiagnosticCategory
from models.diagnostics.test import DiagnosticTest

models_with_data = {
    DiagnosticCategory: [
        {'name': 'Laboratory Tests'},
        {'name': 'Imaging Tests'},
        {'name': 'Genetic Tests'},
        {'name': 'Pathology Tests'},
        {'name': 'Cardiac Diagnostic Tests'},
        {'name': 'Neurological Diagnostic Tests'},
        {'name': 'Pulmonary Function Tests'},
        {'name': 'Endocrine Diagnostic Tests'},
        {'name': 'Gastrointestinal Diagnostic Tests'},
        {'name': 'Infectious Disease Diagnostic Tests'},
        {'name': 'Ophthalmic Diagnostic Tests'},
        {'name': 'Dermatological Diagnostic Tests'},
        {'name': 'Rheumatologic Diagnostic Tests'},
        {'name': 'Urological Diagnostic Tests'},
        {'name': 'Obstetric & Gynecological Diagnostic Tests'},
        {'name': 'Toxicology and Drug Screening'}
    ],
    DiagnosticTest: [
        # Laboratory Tests
        {'name': 'Complete Blood Count (CBC)', 'test_for': 'Infections, anemia',
         'category_name': 'Laboratory Tests'},
        {'name': 'Liver Function Test', 'test_for': 'Liver disease, hepatitis',
         'category_name': 'Laboratory Tests'},
        {'name': 'Kidney Function Test', 'test_for': 'Kidney disorders, dehydration',
         'category_name': 'Laboratory Tests'},
        {'name': 'Lipid Profile', 'test_for': 'Cholesterol levels, heart disease risk',
         'category_name': 'Laboratory Tests'},
        {'name': 'Blood Sugar Test', 'test_for': 'Diabetes, hypoglycemia',
         'category_name': 'Laboratory Tests'},
        {'name': 'Electrolyte Panel', 'test_for': 'Electrolyte imbalances, dehydration',
         'category_name': 'Laboratory Tests'},

        # Imaging Tests
        {'name': 'X-ray', 'test_for': 'Bone fractures, lung infections',
         'category_name': 'Imaging Tests'},
        {'name': 'MRI Scan', 'test_for': 'Soft tissue injuries, brain tumors',
         'category_name': 'Imaging Tests'},
        {'name': 'CT Scan', 'test_for': 'Internal bleeding, organ injuries',
         'category_name': 'Imaging Tests'},
        {'name': 'Ultrasound', 'test_for': 'Pregnancy monitoring, organ examination',
         'category_name': 'Imaging Tests'},
        {'name': 'Mammogram', 'test_for': 'Breast cancer screening',
         'category_name': 'Imaging Tests'},

        # Genetic Tests
        {'name': 'BRCA Genetic Test', 'test_for': 'Breast and ovarian cancer risk',
         'category_name': 'Genetic Tests'},
        {'name': 'Carrier Screening', 'test_for': 'Inherited genetic disorders',
         'category_name': 'Genetic Tests'},
        {'name': 'Newborn Screening', 'test_for': 'Genetic conditions in infants',
         'category_name': 'Genetic Tests'},
        {'name': 'Pharmacogenomic Test', 'test_for': 'Drug metabolism and response',
         'category_name': 'Genetic Tests'},

        # Pathology Tests
        {'name': 'Biopsy', 'test_for': 'Cancer diagnosis, abnormal tissue analysis',
         'category_name': 'Pathology Tests'},
        {'name': 'Pap Smear', 'test_for': 'Cervical cancer screening',
         'category_name': 'Pathology Tests'},
        {'name': 'Skin Lesion Examination', 'test_for': 'Skin cancer, infections',
         'category_name': 'Pathology Tests'},
        {'name': 'Bone Marrow Test', 'test_for': 'Blood disorders, leukemia',
         'category_name': 'Pathology Tests'},

        # Cardiac Diagnostic Tests
        {'name': 'Electrocardiogram (ECG/EKG)',
         'test_for': 'Heart rhythm disorders, heart attack',
         'category_name': 'Cardiac Diagnostic Tests'},
        {'name': 'Echocardiogram', 'test_for': 'Heart function, valve diseases',
         'category_name': 'Cardiac Diagnostic Tests'},
        {'name': 'Cardiac Stress Test', 'test_for': 'Heart disease, exercise tolerance',
         'category_name': 'Cardiac Diagnostic Tests'},

        # Neurological Diagnostic Tests
        {'name': 'EEG (Electroencephalogram)', 'test_for': 'Epilepsy, brain activity',
         'category_name': 'Neurological Diagnostic Tests'},
        {'name': 'Nerve Conduction Study', 'test_for': 'Nerve damage, neuropathy',
         'category_name': 'Neurological Diagnostic Tests'},

        # Pulmonary Function Tests
        {'name': 'Spirometry', 'test_for': 'Asthma, COPD',
         'category_name': 'Pulmonary Function Tests'},
        {'name': 'Peak Flow Test', 'test_for': 'Lung capacity, asthma control',
         'category_name': 'Pulmonary Function Tests'},

        # Endocrine Diagnostic Tests
        {'name': 'Thyroid Function Test', 'test_for': 'Hypothyroidism, hyperthyroidism',
         'category_name': 'Endocrine Diagnostic Tests'},
        {'name': 'Cortisol Test', 'test_for': 'Adrenal gland disorders',
         'category_name': 'Endocrine Diagnostic Tests'},

        # Gastrointestinal Diagnostic Tests
        {'name': 'Endoscopy', 'test_for': 'Stomach ulcers, digestive disorders',
         'category_name': 'Gastrointestinal Diagnostic Tests'},
        {'name': 'Colonoscopy', 'test_for': 'Colon cancer, polyps',
         'category_name': 'Gastrointestinal Diagnostic Tests'},

        # Infectious Disease Diagnostic Tests
        {'name': 'HIV Test', 'test_for': 'HIV/AIDS diagnosis',
         'category_name': 'Infectious Disease Diagnostic Tests'},
        {'name': 'Tuberculosis Test', 'test_for': 'Tuberculosis infection',
         'category_name': 'Infectious Disease Diagnostic Tests'},

        # Ophthalmic Diagnostic Tests
        {'name': 'Visual Acuity Test', 'test_for': 'Vision sharpness',
         'category_name': 'Ophthalmic Diagnostic Tests'},
        {'name': 'Tonometry', 'test_for': 'Glaucoma detection',
         'category_name': 'Ophthalmic Diagnostic Tests'},

        # Dermatological Diagnostic Tests
        {'name': 'Patch Test', 'test_for': 'Allergic skin reactions',
         'category_name': 'Dermatological Diagnostic Tests'},
        {'name': 'Dermoscopy', 'test_for': 'Skin cancer assessment',
         'category_name': 'Dermatological Diagnostic Tests'},

        # Rheumatologic Diagnostic Tests
        {'name': 'Rheumatoid Factor Test', 'test_for': 'Rheumatoid arthritis diagnosis',
         'category_name': 'Rheumatologic Diagnostic Tests'},
        {'name': 'ANA Test', 'test_for': 'Lupus and autoimmune diseases',
         'category_name': 'Rheumatologic Diagnostic Tests'},

        # Urological Diagnostic Tests
        {'name': 'Urinalysis', 'test_for': 'Kidney disease, urinary tract infections',
         'category_name': 'Urological Diagnostic Tests'},
        {'name': 'Prostate-Specific Antigen (PSA) Test',
         'test_for': 'Prostate cancer risk',
         'category_name': 'Urological Diagnostic Tests'},

        # Obstetric & Gynecological Diagnostic Tests
        {'name': 'Pelvic Ultrasound',
         'test_for': 'Pregnancy monitoring, reproductive health',
         'category_name': 'Obstetric & Gynecological Diagnostic Tests'},
        {'name': 'Hysteroscopy', 'test_for': 'Uterine abnormalities',
         'category_name': 'Obstetric & Gynecological Diagnostic Tests'},

        # Toxicology and Drug Screening
        {'name': 'Drug Screening Test', 'test_for': 'Substance abuse detection',
         'category_name': 'Toxicology and Drug Screening'},
        {'name': 'Blood Alcohol Test', 'test_for': 'Alcohol intoxication level',
         'category_name': 'Toxicology and Drug Screening'}
    ]
}
