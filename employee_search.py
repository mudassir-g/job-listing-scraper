import re

from duckduckgo_search import DDGS


def search(search_query, results_wanted=10):
    ddg = DDGS()
    results = ddg.text(search_query, max_results=results_wanted)
    return results


def search_employees(company_name, designation, results_wanted=10):
    search_query = f'site:linkedin.com/in/ {company_name} {designation or "employees"}'
    results = search(search_query, results_wanted)
    return parse_employee_results(results)


def parse_employee_results(results):
    employees = []
    # Regular expression to match the pattern
    pattern = r'^(.*?) - (.*?) - (.*?) \| LinkedIn$'
    for result in results:
        # Search for the pattern in the input string
        match = re.search(pattern, result.get('title'))

        if match:
            name = match.group(1).strip()
            designation = match.group(2).strip()
            company = match.group(3).strip()

            employees.append({
                'name': name,
                'designation': designation,
                'company': company,
                'url': result.get('href')
            })
    return employees


if __name__ == '__main__':
    COMPANY_NAME = 'Delloite'
    DESIGNATION = 'Human Resource'
    employees = search_employees(COMPANY_NAME, DESIGNATION, 10)
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(employees)
