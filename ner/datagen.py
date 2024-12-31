"""
Generate JSON-formatted data for named entity recognition (NER) tasks.

Generates sentence and log message samples that include name entities of
differnet types:
- Company Names
- Domain Names
- Email Addresses
- IP Addresses
- URLs
"""

import random
import json
from urllib.parse import urlparse
import dask.dataframe as dd

COMPANY_NAMES = DOMAIN_NAMES = EMAIL_ADDRESSES = IPV4_ADDRESSES = IPV6_ADDRESSES = URLS = None
COMPANY_TEMPLATES = DOMAIN_TEMPLATES = EMAIL_TEMPLATES = IP_TEMPLATES = URL_TEMPLATES = \
    DOMAIN_LOG_TEMPLATES = IP_LOG_TEMPLATES = URL_LOG_TEMPLATES = EMAIL_LOG_TEMPLATES = None


def load_datasets():
    """
    Load datasets into dataframes from text files.
    """
    global COMPANY_NAMES, DOMAIN_NAMES, EMAIL_ADDRESSES, IPV4_ADDRESSES, IPV6_ADDRESSES, URLS
    # Load company names
    COMPANY_NAMES = dd.read_csv("data/companies.txt", header=None, names=["company_name"], sep="\t")
    # Load domain names
    DOMAIN_NAMES = dd.read_csv("data/domains.txt", header=None, names=["domain_name"], sep="\t")
    # Load email addresses
    EMAIL_ADDRESSES = dd.read_csv("data/emails.txt", header=None, names=["email_address"], sep="\t")
    # Load IPv4 addresses
    IPV4_ADDRESSES = dd.read_csv("data/ipv4_addresses.txt", header=None, names=["ip_address"], sep="\t")
    # Load IP addresses
    IPV6_ADDRESSES = dd.read_csv("data/ipv6_addresses.txt", header=None, names=["ip_address"], sep="\t")
    # Load URLs
    URLS = dd.read_csv("data/urls.txt", header=None, names=["url"], sep="\t")


def read_template_strings():
    """
    Read template strings from files.
    """
    global COMPANY_TEMPLATES, DOMAIN_TEMPLATES, EMAIL_TEMPLATES, IP_TEMPLATES, URL_TEMPLATES, \
           DOMAIN_LOG_TEMPLATES, IP_LOG_TEMPLATES, URL_LOG_TEMPLATES, EMAIL_LOG_TEMPLATES
    with open("sample_templates/company.txt", "r") as file:
        COMPANY_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/domain.txt", "r") as file:
        DOMAIN_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/email.txt", "r") as file:
        EMAIL_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/ip.txt", "r") as file:
        IP_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/url.txt", "r") as file:
        URL_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/domain-log.txt", "r") as file:
        DOMAIN_LOG_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/ip-log.txt", "r") as file:
        IP_LOG_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/url-log.txt", "r") as file:
        URL_LOG_TEMPLATES = [s.strip() for s in file.readlines()]
    with open("sample_templates/email-log.txt", "r") as file:
        EMAIL_LOG_TEMPLATES = [s.strip() for s in file.readlines()]

def generate_ner_dataset(output_file):
    """
    Generate a JSON dataset for NER training.

    Args:
        output_file (str): Path to the output JSON file.
    """
    global COMPANY_NAMES, DOMAIN_NAMES, EMAIL_ADDRESSES, IPV4_ADDRESSES, IPV6_ADDRESSES, URLS
    global COMPANY_TEMPLATES, DOMAIN_TEMPLATES, EMAIL_TEMPLATES, IP_TEMPLATES, URL_TEMPLATES, \
           DOMAIN_LOG_TEMPLATES, IP_LOG_TEMPLATES, URL_LOG_TEMPLATES, EMAIL_LOG_TEMPLATES
    if COMPANY_NAMES is None:
        load_datasets()
        read_template_strings()

    # Define entity types and their corresponding globals and templates
    entity_types = [
        ("company", COMPANY_NAMES, COMPANY_TEMPLATES),
        ("domain", DOMAIN_NAMES, DOMAIN_TEMPLATES),
        ("domain", DOMAIN_NAMES, DOMAIN_LOG_TEMPLATES),
        ("email", EMAIL_ADDRESSES, EMAIL_TEMPLATES),
        ("email", EMAIL_ADDRESSES, EMAIL_LOG_TEMPLATES),
        ("ip_addr", IPV4_ADDRESSES, IP_TEMPLATES),
        ("ip_addr", IPV4_ADDRESSES, IP_LOG_TEMPLATES),
        ("ip_addr", IPV6_ADDRESSES, IP_TEMPLATES),
        ("ip_addr", IPV6_ADDRESSES, IP_LOG_TEMPLATES),
        ("url", URLS, URL_TEMPLATES),
        ("url", URLS, URL_LOG_TEMPLATES)
    ]

    with open(output_file, "w") as f:
        f.write("[")  # Start of the JSON array
        first_item = True

        for entity_type, data_frame, templates in entity_types:
            # Process the data in chunks to avoid loading entire DataFrame into memory
            for partition in data_frame.to_delayed():
                try:
                    partition_df = partition.compute()
                    values = partition_df.iloc[:, 0].dropna().tolist()  # Filter out null values

                    # Generate samples for all items in the raw data
                    for entity in values:
                        try:
                            template = random.choice(templates)  # Select a random template
                            sentence = template.format(**{entity_type: entity})
                            start_idx = sentence.find(entity)
                            end_idx = start_idx + len(entity)

                            # Create the sample with full entity annotation
                            entities = [
                                {
                                    "start": start_idx,
                                    "end": end_idx,
                                    "label": entity_type.upper()
                                }
                            ]

                            # Additional entity for domain name if email or url
                            if entity_type in ["email", "url"]:
                                if entity_type == "email":
                                    domain_start = entity.find("@") + 1
                                    domain = entity[domain_start:]
                                else:  # URL
                                    parsed_url = urlparse(entity)
                                    domain = parsed_url.netloc

                                domain_idx = sentence.find(domain)
                                if domain_idx != -1:
                                    entities.append({
                                        "start": domain_idx,
                                        "end": domain_idx + len(domain),
                                        "label": "DOMAIN"
                                    })

                            sample = {
                                "text": sentence,
                                "entities": entities
                            }

                            # Write the sample to the file
                            if not first_item:
                                f.write(",\n")  # Add a comma and newline before the next item
                            json.dump(sample, f, indent=2)
                            first_item = False
                        except Exception as e:
                            print(f"Error processing entity '{entity}': {e}")
                except Exception as e:
                    print(f"Error processing partition: {e}")

        f.write("]")  # End of the JSON array
