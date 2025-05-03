from bs4 import BeautifulSoup
import json
import os

def parse_services_html(file_path):
    """
    Parse the services.html file and extract service information
    Returns a structured representation of the services
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    services = []
    
    # Try to find service sections with different strategies
    # Strategy 1: Look for service-related class names
    service_sections = soup.find_all(['section', 'div'], class_=lambda c: c and ('service' in c.lower() if c else False))
    
    if service_sections:
        for section in service_sections:
            # Find the service name
            name_elem = section.find(['h1', 'h2', 'h3', 'h4'])
            service_name = name_elem.text.strip() if name_elem else "Unknown Service"
            
            # Find the service description
            desc_elems = section.find_all('p')
            description = " ".join([p.text.strip() for p in desc_elems]) if desc_elems else ""
            
            # Get features if available
            features = []
            feature_list = section.find('ul')
            if feature_list:
                features = [li.text.strip() for li in feature_list.find_all('li')]
            
            services.append({
                "name": service_name,
                "description": description,
                "features": features
            })
    
    # Strategy 2: Look for service-related headings
    if not services:
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            if 'service' in heading.text.lower():
                service_name = heading.text.strip()
                
                # Find description (next paragraph or div after heading)
                description = ""
                next_elem = heading.find_next_sibling()
                if next_elem and next_elem.name in ['p', 'div']:
                    description = next_elem.text.strip()
                
                services.append({
                    "name": service_name,
                    "description": description,
                    "features": []
                })
    
    return services

def save_services_to_json(services, output_file):
    """Save parsed services to a JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(services, f, indent=4)

if __name__ == "__main__":
    services_html_path = "C:\\Users\\robbi\\Rpasquale\\remtech website\\services.html"
    output_json_path = "C:\\Users\\robbi\\Rpasquale\\remtech website\\services_data.json"
    
    services = parse_services_html(services_html_path)
    save_services_to_json(services, output_json_path)
    
    print(f"Successfully parsed {len(services)} services and saved to {output_json_path}")
