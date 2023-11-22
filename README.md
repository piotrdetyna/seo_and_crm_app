# SEO and CRM app 
Web application for interactive agencies for customer management with useful SEO functions.

## General overview
The application consists of two main parts - SEO related functions and CRM.

### SEO
- **Backlinks** - The application allows you to track acquired incoming links to customer websites. In addition to storing all links in one place, it checks whether a given link still exists (if it is active) and checks whether the rel attribute has changed.

- **External links (outgoing links)** - The application searches for outgoing links from customer websites and checks whether the pages they lead to are still operational. Except that
saves the rel attributes of these links.

- **Notes** - It allows you to conveniently save notes about a given page.

- **Position checker** - Checks the current positions of clients' websites for given keywords.

- **Sites** - Orgnanizes data about clients' websites. This information is used in almost every other function of the app. Among the things worth mentioning, the application checks the **expiration date of the domain of each website using the WHOIS library**.


### CRM
- **Clients** - Organizes information about customers, which is useful primarily when issuing invoices and adding contracts.

- **Contracts** - Makes it easier to manage contracts. You can create many contracts for each website (e.g. positioning contract, website development contract).
  
    In turn, for each contract, you add information such as the frequency of invoices, the amount on the invoice and the date of the next invoice. In addition, if the next invoice is due in a few days (you can specify the number of these days by editing the contract), the contract is marked as urgent.

- **Invoices** - It improves management and issuing invoices on many levels. 

    Firstly, it supports you when issuing an invoice by displaying all the necessary data, such as the amount (using the contract to which the invoice is assigned) and customer details, Tax Identification Number and other company data. This is possible thanks to **integration with the REGON API**, which provides information about the company based on the Tax Identification Number (NIP) that you provide when adding a client to the program.

    Secondly, the application allows you to **send invoices and reports as a PDF file to the server**. Storing these files in the program makes it easier for you to stay organized.

    In addition, invoices are marked as paid or unpaid, so you can easily track which invoices you have issued are still unpaid.

_Are you interested in the technical details of the application? You will find them below._

## Endpoints
- **api/sites/**
  -  Allowed methods: 
<img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> 
<img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"> 
  - <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"> request data: 
    - url - text
    - logo (optional) - graphic file
    - client_id - integer
- **api/sites/{site_id}/**
  - Allowed methods: 
<img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> 
<img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> 
<img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"> 
  - <img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> available query parameters (e.g api/sites/1?attributes=attr1,attr2):
    - id
    - url
    - logo
    - date
    - domain_expiry_date
    - contracts
    - notes
    - external_links_manager
    - backlinks
    - client
    
  - <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> request data: 
    - url - text
    - logo (optional) - graphic file
- **api/sites/{site_id}/expiry/**
  - This endpoint updates the expiration date of the site's domain
  - Allowed methods: <img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"> 
- **api/sites/expiry/**
  - This endpoint updates **all** sites domain expiration dates
  - Allowed methods: <img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"> 
  



## Database
![Databse diagram](https://piotr.detyna.pl/crm-app-db-diagram.svg? "Databse diagram")