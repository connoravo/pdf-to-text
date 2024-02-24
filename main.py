import os
from datetime import datetime
from pypdf import PdfReader

def capture_pdf_location():
    print('Specify the full or relative file path for the PDF file.')
    filevalid = False
    while not filevalid:
        filepath = input('Enter a file path: ')

        if os.path.exists(filepath):
            filevalid = True
            return filepath
        else:
            print(f'Invalid file path {filepath}')


def capture_sensitives():
    print('Specify the full or relative file path for the sensitive words list.')    
    filevalid = False
    while not filevalid:
        filepath = input('Enter a file path: ')

        if os.path.exists(filepath):
            filevalid = True
            return filepath
        else:
            print(f'Invalid file path {filepath}')


def transpose_pdf(fileloc):
    reader = PdfReader(fileloc)

    payload = ""
    for page in reader.pages:
        payload += page.extract_text() + "\n"
    return payload


def scrub_sensitive_data(sensitive_fileloc, payload):
    with open(sensitive_fileloc, 'r') as f:
        sensitives = f.readlines()
        for item in sensitives:
            sensitive_word_combinations = [item.upper(), item.lower(), item.strip()]
            for combination in sensitive_word_combinations:
                payload.replace(combination, "REDACTED")
        return payload


def produce_output(payload):
    dt_now = datetime.now()
    with open(f'output-{dt_now}.txt', 'w') as f:
        f.write(payload)
        f.close()
    return f'output-{dt_now}.txt'
    

location = capture_pdf_location()
print(f'PDF LOCATION: {location}')

sensitive_file = capture_sensitives()
print(f'SENSITIVE LOCATION: {sensitive_file}')

unsanitised_payload = transpose_pdf(location)
scrubbed_payload = scrub_sensitive_data(sensitive_file, unsanitised_payload)

output_file = produce_output(scrubbed_payload)

print(f'Output file: {output_file}')
print('DONE')
