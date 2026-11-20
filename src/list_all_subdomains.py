
def find_subdomains(filename, base_domain):
    subdomains = set()  # To store unique subdomains

    with open(filename, 'r') as file:
        for line in file:
            # Remove any extra whitespace or newline
            domain = line.strip()
            # force lower case
            domain = domain.lower()
            # must be a subdomain of target domain
            if domain.endswith(f'.{base_domain}'):
                # store
                subdomains.add(domain)


    # Convert set to list and sort it in ascending order
    sorted_subdomains = sorted(subdomains)

    # Print the results
    if sorted_subdomains:
        print("Found subdomains:")
        for subdomain in sorted_subdomains:
            print(subdomain)
    else:
        print(f"No subdomains found for {base_domain}")

if __name__ == '__main__':
    # list of all domains
    filename = '../data/all_domains.txt'

    # base domain to search

    base_domain = 'torget.se'


    # perform search
    find_subdomains(filename, base_domain)
