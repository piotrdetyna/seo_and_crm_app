
# SEO and CRM app <!-- omit from toc -->
Web application for interactive agencies to manage clients with useful SEO features. Written in Django with a fully functional, convention-compliant REST API made in the Django Rest Framework. It has integrations with, including REGON_API (API for retrieving data of Polish business entities) and WHOIS domain database. In addition, it scrapes data (e.g. automatically collects outgoing links from the website, checks positions in Google) from the Internet.

<span float="left"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> <img src="https://res.cloudinary.com/apideck/image/upload/w_128,f_auto/v1616206512/icons/django-rest-framework.png" alt="git" width="40" height="40"/>  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/>&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://static-00.iconduck.com/assets.00/postman-icon-497x512-beb7sy75.png" alt="javascript" width="40" height="40"/> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/></span>


- [About me](#about-me)
  - [What to pay attention to and what to pay less attention to?](#what-to-pay-attention-to-and-what-to-pay-less-attention-to)
- [General overview](#general-overview)
  - [SEO](#seo)
  - [CRM](#crm)
- [Technical overview](#technical-overview)
  - [Stack and used technologies](#stack-and-used-technologies)
  - [How it works?](#how-it-works)
    - [Finding outgoing links](#finding-outgoing-links)
    - [Checking outgoing links status](#checking-outgoing-links-status)
    - [Checking backlinks status](#checking-backlinks-status)
    - [Checking domain expiry date](#checking-domain-expiry-date)
    - [Retrieving client's data](#retrieving-clients-data)
    - [Checking positions in Google](#checking-positions-in-google)
  - [RESTFUL API Design](#restful-api-design)
  - [API Security](#api-security)
- [Database](#database)
- [Endpoints](#endpoints)
  - [Sites](#sites)
  - [Clients](#clients)
  - [Notes](#notes)
  - [Contracts](#contracts)
  - [Invoices](#invoices)
  - [Backlinks](#backlinks)
  - [External links managers](#external-links-managers)
  - [Keywords](#keywords)
  - [Session](#session)


## About me
Hi, my name is Piotr Detyna, I'm 17 years old and I'm a beginner backend developer and cybersecurity enthusiast. This is my first big project, so there are definitely some oversights, but I'm still really proud of it.

### What to pay attention to and what to pay less attention to?

As I like the backend much more than the frontend, **I encourage you to look more at the API structure, database design and Django code**. While the UI/UX is less refined, I hope the robust backend functionalities of the application will be of primary interest.

## General overview
The application consists of two main parts - SEO related functions and CRM. 


### SEO
- **Backlinks** - The application allows you to track acquired incoming links to customer websites. In addition to storing all links in one place, it checks whether a given link still exists (if it is active) and checks whether the rel attribute has changed.
  ![Backlinks gif](https://piotr.detyna.pl/seo-crm-app/backlinks.gif)

- **External links (outgoing links)** - The application searches for outgoing links from customer websites and checks whether the pages they lead to are still operational. Except that
saves the rel attributes of these links.
  ![External links gif](https://piotr.detyna.pl/seo-crm-app/external-links.gif)

- **Notes** - It allows you to conveniently save notes about a given page.
  ![Notes gif](https://piotr.detyna.pl/seo-crm-app/notes.gif)

- **Position checker** - Checks the current positions of clients' websites for given keywords.
  ![Position checker gif](https://piotr.detyna.pl/seo-crm-app/keywords.gif)

- **Sites** - Organizes data about clients' websites. This information is used in almost every other function of the app. Among the things worth mentioning, the application checks the **expiration date of the domain of each website using the WHOIS library**.
  ![Sites gif](https://piotr.detyna.pl/seo-crm-app/sites.gif)

### CRM
- **Clients** - Organizes information about customers, which is useful primarily when issuing invoices and adding contracts.
  ![Clients gif](https://piotr.detyna.pl/seo-crm-app/clients.gif)

- **Contracts** - Makes it easier to manage contracts. You can create many contracts for each website (e.g. positioning contract, website development contract).
  
    In turn, for each contract, you add information such as the frequency of invoices, the amount on the invoice and the date of the next invoice. In addition, if the next invoice is due in a few days (you can specify the number of these days by editing the contract), the contract is marked as urgent.
  ![Contracts gif](https://piotr.detyna.pl/seo-crm-app/contracts.gif?)
- **Invoices** - It improves management and issuing invoices on many levels. 

    Firstly, it supports you when issuing an invoice by displaying all the necessary data, such as the amount (using the contract to which the invoice is assigned) and customer details, Tax Identification Number and other company data. This is possible thanks to **integration with the REGON API**, which provides information about the company based on the Tax Identification Number (NIP) that you provide when adding a client to the program.

    Secondly, the application allows you to **send invoices and reports as a PDF file to the server**. Storing these files in the program makes it easier for you to stay organized.

    In addition, invoices are marked as paid or unpaid, so you can easily track which invoices you have issued are still unpaid.
    ![Invoices gif](https://piotr.detyna.pl/seo-crm-app/invoices.gif)

_Are you interested in the technical details of the application? You will find them below._


## Technical overview

### Stack and used technologies
<span float="left"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> <img src="https://res.cloudinary.com/apideck/image/upload/w_128,f_auto/v1616206512/icons/django-rest-framework.png" alt="git" width="40" height="40"/>  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/>&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://static-00.iconduck.com/assets.00/postman-icon-497x512-beb7sy75.png" alt="javascript" width="40" height="40"/> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/></span>

### How it works?
Below I will describe, in my opinion, the most interesting functionalities of the application. I'll skip the "usual stuff", like CRUD operations.

#### Finding outgoing links
The app takes advantage of given site's sitemap(s), it scrapes each sitemap (e.g. sitemap-posts.xml, sitemap-categories.xml), retrieves from them a list of all pages in the site. Then it scrapes each of these sites and, with help of BeautifulSoup4 library, retrieves all outgoing links.

#### Checking outgoing links status
After finding the outgoing links from the site, the app lets user easily check, if linked sites still works by sending some requests to those sites and checking response code. It is significant from SEO point of view. 

#### Checking backlinks status
When user has added some backlinks to the database, he can check, if they are still active, or if the rel attribute is as it should be. To achieve that, the app also uses requests and BS4 libraries to retrieve outgoing links from specified linking page.

#### Checking domain expiry date
The app, thanks to the WHOIS library, can check when your domain will expire.

#### Retrieving client's data
Program uses the [API REGON](https://api.stat.gov.pl/Home/RegonApi) interface to retrieve information about your clients, everyting you have to do, is entering client's company NIP (_Tax Identification Number_). It especially useful while issuing invoices.

#### Checking positions in Google
The application can check positions of your sites in Google's SERP (search engine results page) on specified keywords. Similarly to some previous functionalities, the app scrapes SERPs, and retrieves positions. 

### RESTFUL API Design
- [x] Use resources endpoint and HTTP Verbs
- [x] Return correct HTTP codes
- [x] Fields projection support

### API Security

Below you'll find several aspects of the API, which increase the broadly understood API security. They come from _[https://roadmap.sh/best-practices/api-security](https://roadmap.sh/best-practices/api-security)_ site. 
- [x] Avoid ‘Basic Authentication’
- [x] Use `Max Retry’ and jail features in Login
- [x] Limit requests (throttling) to avoid DDoS / Brute Force attacks
- [x] Use HSTS header with SSL to avoid SSL Strip attacks.
- [x] Turn off directory listings
- [x] Use proper HTTP methods for the operation
- [x] Validate user input to avoid common vulnerabilities
- [x] Send X-Content-Type-Options: nosniff header
- [x] Send X-Frame-Options: deny header
- [x] Only return the data that is needed for the client to function.
- [x] Return the proper status code according to the operation completed





## Database
[![Databse diagram](https://piotr.detyna.pl/seo-crm-app/crm-app-db-diagram.svg "Databse diagram")](https://piotr.detyna.pl/seo-crm-app/db-diagram.html)

[Open in interactive mode](https://piotr.detyna.pl/seo-crm-app/db-diagram.html)
## Endpoints

### Sites
- **api/sites/**
  -  Allowed methods: 
<span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> 
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of all sites.
    - Example response from `api/sites/` using the GET method:
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
    - Example request data for `api/clients` with the POST method:
      ``` 
      {
          "url": "site.net"
          "logo": (binary)
          "client_id": 1
      }
      ```
      _note: the `logo` field is optional_


- **api/sites/{site_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> 

  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of site with given id
    - Example response from `api/sites/{site_id}/` with the GET method where `site_id` = 1:
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
    - Available values for the query parameter **attributes**: `id, url, logo, date, domain_expiry_date, contracts, notes, external_links_manager, backlinks, client`:
  
    - Example response from `api/sites/{site_id}?attributes=url,date,id,notes,backlinks,client` with the GET method where `site_id` = 1:
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
    - Example request data for `api/sites/{site_id}/` with the PATCH method, where `site_id` is the id of site we want to change its data, in this case `id` = 1 and we want to update `url` field.
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
   

### Clients
- **api/clients/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of clients' data.
    - Example response from `api/clients` with the GET method:
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
    - Example request data for `api/clients` with the POST method:
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
    note: `address` and `full_name` fields are necessary only if `is_company` field is set to false, `nip` is necessary only if `is_company` is set to true.


- **api/clients/{client_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of client with given id
    - Example response from `api/clients/{client_id}/` with the GET method where `client_id` = 1:
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
    - Available values for the query parameter **attributes**: `name, nip, email, full_name, address, id, is_company, sites`.
    
      Example response from `api/clients/{client_id}?attributes=name,nip,id,sites` with the GET method where `client_id` = 1:
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

      - **Query parameter regon_api** - set this to true if you want data about your client retrieved from the REGON API to be appended to the response.
      
        Example response from `api/clients/{client_id}/?regon_api=true`:
        ```
          {
              "client": {
                  "name": "InPost",
                  "nip": "6793108059",
                  "email": "inpost@inpost.pl",
                  "full_name": "",
                  "address": "",
                  "id": 11,
                  "is_company": true
              },
              "company": {
                  "Regon": "360781085",
                  "Nip": "6793108059",
                  "StatusNip": null,
                  "Nazwa": "INPOST SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ",
                  "Wojewodztwo": "MAŁOPOLSKIE",
                  "Powiat": "Kraków",
                  "Gmina": "Kraków-Podgórze",
                  "Miejscowosc": "Kraków",
                  "KodPocztowy": "30-727",
                  "Ulica": "ul. Pana Tadeusza",
                  "NrNieruchomosci": "4",
                  "NrLokalu": null,
                  "Typ": "P",
                  "SilosID": "6",
                  "DataZakonczeniaDzialalnosci": null,
                  "MiejscowoscPoczty": "Kraków"
              }
          }
        ```


  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given client object with passed values.
    - Example request data for `api/clients/{client_id}/` with the PATCH method, where `client_id` is the id of client we want to change his data, in this case id = 1 and we want to update nip and name fields.
      ```
        {
          "nip": "1234567890",
          "name": "Microsoft"
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given client from the database. As well as all his sites. 
  
### Notes
- **api/notes/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of notes objects.
    - Example response from `api/notes/` with the GET method:
      ```
        
      {
        "notes": [
            {
                "text": "Content of the note",
                "title": "Info",
                "id": 1,
                "date": "2023-09-24"
            },
            {
                "text": "",
                "title": "Title",
                "id": 2,
                "date": "2023-09-24"
            },
            ...
          ]
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new note.
    - Example request data for `api/notes/` with the POST method:
      ```
        {
          "text": "Content",
          "title": "New note",
          "site_id": 1,
        }
      ``` 
- **api/notes/{note_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of note with given id
    - Example response from `api/notes/{note_id}/` with the GET method where `note_id` = 1:
      ```
      {
          "notes": {
              "text": "",
              "title": "ez2e",
              "id": 1,
              "date": "2023-09-24"
          }
      }
      ```
    - Available values for the query parameter **attributes**: `text, title, id, date`.


  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given note object with passed values.
    - Example request data for `api/notes/{note_id}/` with the PATCH method, we want to update text and title fields.
      ```
        {
          "title": "new title",
          "content": "new content"
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given note from the database. 


### Contracts
- **api/contracts/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of contracts objects.
    - Example response from `api/contracts/` with the GET method:
      ``` 
        {
          "contracts": [
              {
                  "invoice_frequency": 12,
                  "value": 12,
                  "category": "seo",
                  "invoice_date": "2023-09-29",
                  "days_before_invoice_date_to_mark_urgent": 12,
                  "is_urgent": true,
                  "id": 5
              },
              {
                  "invoice_frequency": 1,
                  "value": 1000,
                  "category": "seo",
                  "invoice_date": "2023-11-30",
                  "days_before_invoice_date_to_mark_urgent": 40,
                  "is_urgent": false,
                  "id": 1
              },
              ...
          ]
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new contract.
    - Example request data for `api/contracts/` with the POST method:
      ```
        {
            "invoice_frequency": 1,
            "value": 599,
            "category": "seo",
            "site_id": 1,
            "invoice_date": "2023-12-12",
            "days_before_invoice_date_to_mark_urgent": 1
        }
      ``` 
- **api/contracts/{contract_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of contract with given `id`
    - Example response from `api/contracts/{contract_id}/` with the GET method where `contract_id` = 1:
      ```
      {
          "contracts": {
              "invoice_frequency": 1,
              "value": 1000,
              "category": "seo",
              "invoice_date": "2023-11-30",
              "days_before_invoice_date_to_mark_urgent": 40,
              "is_urgent": false,
              "id": 1
          }
      }
      ```
    - Available values for the query parameter **attributes**: `invoice_frequency, value, category, invoice_date, is_urgent, id, days_before_invoice_date_to_mark_urgent`.


  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given contract object with passed values. As well as all its invoices.
    - Example request data for `api/contracts/{contract_id}/` with the PATCH method, we want to update `value` and `invoice_date` fields.
      ```
        {
          "value": 123,
          "invoice_date": "2023-12-30"
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given contract from the database. 

- **api/contracts/{contract_id}/urgency**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint updates the `is_urgent` field in given contract. If `invoice_date` is passing in less than `days_before_invoice_date_to_mark_urgent` days, the contract is marked as urgent (`is_urgent = True`).

- **api/contracts/urgency**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint does the same as `api/contracts/{contract_id}/urgency`, but for every contract in the database.



### Invoices
- **api/invoices/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of invoices objects.
    - Example response from `api/invoices/` with the GET method:
      ``` 
      {
        "invoices": [
            {
                "invoice_file": "/media/clients/1/contracts/1/invoices/invoice_35_3_jWzXZfK.pdf",
                "report_file": null,
                "is_paid": false,
                "id": 3,
                "payment_date": "2023-10-01"
            },
            {
                "invoice_file": "/media/clients/1/contracts/2/invoices/invoice_2_3.pdf",
                "report_file": null,
                "is_paid": false,
                "id": 5,
                "payment_date": "2023-10-05"
            },
            ...
        ]
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new invoice.
    - Example request data for `api/invoices/` with the POST method:
      ```
        {
            "contract_id": 5,
            "payment_date": "2023-11-17",
            "invoice_file": (binary),
            "report_file": (binary), [optional]
        }
      ``` 
- **api/invoices/{invoice_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of invoice with given `id`
    - Example response from `api/invoices/{invoice_id}/` with the GET method where `invoice_id` = 1:
      ```
      {
          "invoices": {
              "invoice_file": "/media/clients/1/contracts/1/invoices/invoice_35_3.pdf",
              "report_file": null,
              "is_paid": true,
              "id": 1,
              "payment_date": "2023-10-01"
          }
      }
      ```
    - Available values for the query parameter **attributes**: `invoice_file*, report_file*, is_paid, id, payment_date`.
      
      If `invoice_file` or `report_file` is passed through _attribute_ query parameter, *the server will respond with a file only* (invoice or report, first based on the order of the attribute parameter values)



  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given invoice object with passed values.
    - Example request data for `api/invoices/{invoice_id}/` with the PATCH method, we want to update the `is_paid` field.
      ```
        {
          "is_paid": false,
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given invoice from the database. 

- **api/invoices/{invoice_id}/overduity/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint updates the `is_overdue` field in given invoice. If the `payment_date` has passed and `is_paid == False`, the invoice will be marked as overdued (`is_overdue = True`)
  
- **api/invoices/overduity**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint does the same as `api/invoices/{invoice_id}/overduity/`, but for every invoice in the database.


### Backlinks
- **api/backlinks/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of backlinks objects.
    - Example response from `api/backlinks/` with the GET method:
      ``` 
      {
        "backlinks": [
            {
                "id": 7,
                "linking_page": "https://linking-page.pl",
                "active": false,
                "rel": null,
                "rel_changed": true,
                "status_changed": true,
                "site": 3
            },
            {
                "id": 9,
                "linking_page": "https://linking-page.com",
                "active": false,
                "rel": null,
                "rel_changed": false,
                "status_changed": true,
                "site": 1
            },
            ...
        ]
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new backlink.
    - Example request data for `api/backlinks/` with the POST method:
      ```
        {
          "linking_page": "https://linking-site.pl",
          "site_id": 3
        }
      ``` 
- **api/backlinks/{backlink_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of backlink with given id
    - Example response from `api/backlinks/{backlink_id}/` with the GET method where `backlink_id` = 2:
      ```
      {
          "backlinks": {
              "id": 2,
              "linking_page": "https://links.pl",
              "active": false,
              "rel": null,
              "rel_changed": false,
              "status_changed": false,
              "site": 2
          }
      }
      ```
    - Available values for the query parameter **attributes**: `id, linking_page, active, rel, rel_changed, status_changed, site`.


  - <span float="left"><img src="https://piotr.detyna.pl/patch.png" style="width: 40px; margin-bottom: -5px;"></span> Updates given backlink object with passed values.
    - Example request data for `api/backlinks/{backlink_id}/` with the PATCH method, we want to update the `linking_page` field.
      ```
        {
          "linking_page": "https://new-links.pl"
        }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given backlink from the database. 

- **api/backlinks/{backlink_id}/status/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint updates the `rel`, `active`, `rel_changed` and `status_changed` fields in given backlink. The app scrapes the `linking_page` and retrieves information about the link.
  
- **api/backlinks/status**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - **Site query parameter** - if you want to update every backlink related to given page, you can use this parameter. Example: `/api/backlinks/status/?site=1`.
  - This endpoint does the same as `api/backlinks/{backlink_id}/status/`, but for every backlink, or for every backlink associated with the given site in the database.



### External links managers
- **api/external-links-managers/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of external links managers objects.
    - Example response from `api/external-links-managers/` with the GET method:
      ``` 
      {
        "external_links_managers": [
            {
                "id": 1,
                "external_links": [
                    {
                        "id": 54,
                        "linking_page": "https://linking-page.pl",
                        "linked_page": "https://linked-page.com",
                        "rel": "dofollow",
                        "is_linked_page_available": true,
                        "manager": 1
                    },
                    ...
                ],
                "excluded": [
                    "facebook",
                    "reddit",
                    "pinterest"
                ],
                "date": "2023-09-26",
                "progress_current": 0,
                "progress_target": 1,
                "site": 1

            },
            {
                "id": 3,
                "external_links": [...],
                "excluded": [...],
                "date": "2023-11-20",
                "progress_current": 0,
                "progress_target": 1,
                "site": 3
            },
            ...
        ]
      }
      ```
- **api/external-links-managers/{site_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of external links manager object related to `site` with the given `id`
    - Example response from `api/external-links-managers/{site_id}/` with the GET method where `site_id` = 1:
      ``` 
      {
        "external_links_managers": {
            {
                "id": 1,
                "external_links": [
                    {
                        "id": 54,
                        "linking_page": "https://linking-page.pl",
                        "linked_page": "https://linked-page.com",
                        "rel": "dofollow",
                        "is_linked_page_available": true,
                        "manager": 1
                    },
                    ...
                ],
                "excluded": [
                    "facebook",
                    "reddit",
                    "pinterest"
                ],
                "date": "2023-09-26",
                "progress_current": 0,
                "progress_target": 1,
                "site": 1

            }
        }
      }
      ```
    - Available values for the query parameter **attributes**: `id, external_links, excluded, date, progress_current, progress_target, site`.


  - <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span> Creates new external links objects and replaces current external links in the external links manager with them.

    The app scrapes every page of given site in search for outgoing links, and updates your external links manager object.

- **api/external-links-managers/{site_id}/status/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint updates the `is_linked_page_available` field in external links manager related to given site. The app goes through every `linked_page` in `external_links` field, scrapes the page and retrieves information about the link.
  
- **api/external-links-managers/status/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint does the same as `api/external-links-managers/status/`, but for every external links manager. It is worth mentioning it is very time-expensive operation, so it probably isn't desired approach.



### Keywords
- **api/keywords/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns list of keywords objects.
    - Example response from `api/keywords/` with the GET method:
      ``` 
      {
          "keywords": [
              {
                  "id": 1,
                  "position": 2,
                  "keyword": "keyword",
                  "site": 1
              },
              {
                  "id": 2,
                  "position": null,
                  "keyword": "google",
                  "site": 1
              },
              ...
        ]
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> adds new keyword.
    - Example request data for `api/keywords/` with the POST method:
      ```
      {
        "keyword": "new keyword",
        "site_id": 1
      }
      ``` 
- **api/keywords/{keyword_id}/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns data of keyword with given `id`
    - Example response from `api/keywords/{keyword_id}/` with the GET method where `keyword_id` = 1:
      ```
      {
          "keywords": {
              "id": 1,
              "position": 2,
              "keyword": "keyword",
              "site": 1,
          },
      }
      ```
    - Available values for the query parameter **attributes**: `id, position, keyword, site, checks`.


  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> deletes given `keyword` from the database. As well as all its checks objects. 

- **api/keywords/{keyword_id}/position/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - This endpoint creates a new check object and adds it to the keyword's `checks` field.

      The app scrapes the Google results page for query `keyword` and returns your site's position.
  
- **api/keywords/position**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span>
  - **Site query parameter** - if you want to check position of every keyword related to given page, you can use this parameter. Example: `/api/keywords/position/?site=1`.
  - This endpoint does the same as `api/keywords/{keyword_id}/position/`, but for every keyword in a site or in the whole database. It is worth mentioning it is very time-expensive operation, and you will be quickly blocked by Google, so it probably isn't desired approach.

### Session

- **api/session/current-site/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"> <img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/get.png" style="width: 40px; margin-bottom: -5px;"></span> returns current site data (if it is set in the session)
    - Example response from `api/session/current-site/` using the GET method when `current_site` in the session is set to 12 (`id` of the site):
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
  - <span float="left"><img src="https://piotr.detyna.pl/put.png" style="width: 40px; margin-bottom: -5px;"></span> updates (or adds if it isn't set) current_site value in the session with a new site `id`
    - Example request data for `api/session/current-site/` using the PUT method:
      ```
      {
        "site_id": 10
      }
      ```
  - <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span> removes `current_site` from the session, of course it doesn't delete a whole site object.
  
- **api/session/login/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span>
  - <span float="left"><img src="https://piotr.detyna.pl/post.png" style="width: 40px; margin-bottom: -5px;"></span> Example request data:
    ```
    {
      "username": "username",
      "password": "password",
    }
    ```
- **api/session/logout/**
  - Allowed methods: <span float="left"><img src="https://piotr.detyna.pl/delete.png" style="width: 40px; margin-bottom: -5px;"></span>
  




