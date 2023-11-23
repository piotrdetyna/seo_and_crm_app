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

### Sites
- **api/sites/**
  -  Allowed methods: 
<span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> 
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of all sites.
    - Example response from _api/sites/_ using the GET method:
      ``` 
      {
          "sites": [
              {
                  "id": 12,
                  "url": "site.com",
                  "logo": "/media/sites/12/logo.png",
                  "date": "2023-11-22",
                  "domain_expiry_date": "2024-05-21",
                  "client": 2
              },
              {
                  "id": 11,
                  "url": "google.pl",
                  "logo": "/media/default.jpg",
                  "date": "2023-10-07",
                  "domain_expiry_date": null,
                  "client": 1
              },
              ...
          ]
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new site.
    - Example request data for _api/clients_ with the POST method:
      ``` 
      {
          "url": "site.net"
          "logo": (binary)
          "client_id": 1
      }
      ```
      _note: the logo field is optional_


- **api/sites/{site_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> 

  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of site with given id
    - Example response from _api/sites/{site_id}/_ with the GET method where site_id = 1:
      ```
      {
          "sites": {
              "id": 1,
              "url": "test.com",
              "logo": "/media/sites/1/logo.jpg",
              "date": "2023-09-23",
              "domain_expiry_date": null,
              "client": 1
          }
      }
      ```
    - Available values for the query parameter **attributes**: _id, url, logo, date, domain_expiry_date, contracts, notes, external_links_manager, backlinks, client_:
  
    - Example response from _api/sites/{site_id}**?attributes=url,date,id,notes,backlinks,client**_ with the GET method where site_id = 1:
      ```
      {
        "sites": {
            "id": 1,
            "notes": [
                {
                    "text": "Content of the note",
                    "title": "Info",
                    "id": 1,
                    "date": "2023-09-24"
                },
                ...
            ],
            "backlinks": [
                {
                    "id": 9,
                    "linking_page": "https://linking-site.org",
                    "active": false,
                    "rel": null,
                    "rel_changed": false,
                    "status_changed": true,
                    "site": 1
                },
                ...
            ],
            "client": {
                "name": "Facebook",
                "nip": "65622341349",
                "email": "piotrek.detyna@gmail.com",
                "full_name": "",
                "address": "",
                "id": 1,
                "is_company": true
            },
            "url": "test.com",
            "date": "2023-09-24"
          }
      }
      ```
    
  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given site object with passed values.
    - Example request data for _api/sites/{site_id}/_ with the PATCH method, where site_id is the id of site we want to change its data, in this case id = 1 and we want to update url field.
      ```
      {
        "url": "new-domain.com"
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given site from the database. As well as all its related records.

- **api/sites/expiry/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint updates **all** sites domains expiry dates
  
- **api/sites/{site_id}/expiry/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"> </span>
  - This endpoint updates the expiry date of the site's domain
   

  
  
### Session

- **api/session/current-site/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns current site data (if it is set in the session)
    - Example response from _api/session/current-site/_ using the GET method when current_site in the session is set to 12 (id of the site):
        ```
          {
            "sites": {
              "id": 12,
              "url": "site.com",
              "logo": "/media/sites/12/logo.png",
              "date": "2023-11-22",
              "domain_expiry_date": "2024-05-21",
              "client": 2
            }
          }
        ```
  - <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span> updates (or adds if it isn't set) current_site value in the session with a new site id
    - Example request data for api/session/current-site/ using the PUT method:
      ```
      {
        "site_id": 10
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> removes current_site from the session, of course it doesn't deletes a whole site object.

### Clients
- **api/clients/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of clients' data.
    - Example response from _api/clients_ with the GET method:
      ```
      {
          "clients": [
              {
                  "name": "Facebook",
                  "nip": "65622341349",
                  "email": "piotrek.detyna@gmail.com",
                  "full_name": "",
                  "address": "",
                  "id": 1,
                  "is_company": true
              },
              {
                  "name": "Piotrek Detyna",
                  "nip": "",
                  "email": "piotrek.detyna@gmail.com",
                  "full_name": "Piotr Detyna",
                  "address": "Emilii Plater 53, 00-113 Warszawa",
                  "id": 2,
                  "is_company": false
              },
          ...
          ]
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new client.
    - Example request data for _api/clients_ with the POST method:
      ```
        {
          "name":"Google",
          "email":"google@gmail.com",
          "nip":"770493581",
          "full_name":"",
          "address":"",
          "is_company":true
        }
      ``` 
    _note: address and full_name fields are necessary only if is_company field is set to false, nip is necessary only if is_company is set to true_
- **api/clients/{client_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of client with given id
    - Example response from _api/clients/{client_id}/_ with the GET method where client_id = 1:
      ```
      {
        "clients": {
            "name": "Facebook",
            "nip": "65622341349",
            "email": "piotrek.detyna@gmail.com",
            "full_name": "",
            "address": "",
            "id": 1,
            "is_company": true
        }
      }
      ```
    - Available values for the query parameter **attributes**: _name, nip, email, full_name, address, id, is_company, sites_:
    - Example response from _api/clients/{client_id}**?attributes=name,nip,id,sites**_ with the GET method where client_id = 1:
      ```
      {
        "clients": {
            "name": "Facebook",
            "nip": "65622341349",
            "id": 1,
            "sites": [
                {
                    "id": 11,
                    "url": "google.pl",
                    "logo": "/media/default.jpg",
                    "date": "2023-10-07",
                    "domain_expiry_date": null,
                    "client": 1
                },
                {
                    "id": 5,
                    "url": "site.pl",
                    "logo": "/media/default.jpg",
                    "date": "2023-09-26",
                    "domain_expiry_date": "2024-01-23",
                    "client": 1
                },
                ...
            ]
        }
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given client object with passed values.
    - Example request data for _api/clients/{client_id}/_ with the PATCH method, where client_id is the id of client we want to change his data, in this case id = 1 and  we want to update nip and name fields.
      ```
        {
          "nip": "1234567890",
          "name": "Microsoft"
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given client from the database. As well as all his sites. 
  




## Database
![Databse diagram](https://piotr.detyna.pl/crm-app-db-diagram.svg? "Databse diagram")