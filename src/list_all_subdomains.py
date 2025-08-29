
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

    # base_domain = 'stomped.com'
    # base_domain = 'planetquake.com'
    # base_domain = 'telefragged.com'
    # base_domain = 'frag.com'
    # base_domain = 'bluesnews.com'
    # base_domain = 'fragzone.se'
    # base_domain = 'warzone.com'
    # base_domain = 'planetquake.gamespy.com'
    # base_domain = 'quakeintosh.com'
    # base_domain = 'quakedev.com'
    # base_domain = 'barrysworld.com'
    # base_domain = 'tfdomain.com'
    # base_domain = 'lockandload.com'
    # base_domain = 'gamers.org'
    # base_domain = 'minos.co.uk'
    # base_domain = 'gameaholic.com'
    # base_domain = 'idsoftware.com'
    # base_domain = 'time2quake.com'
    # base_domain = 'gamespy.com'
    base_domain = 'macquakeinfinity.com'


    # perform search
    find_subdomains(filename, base_domain)
