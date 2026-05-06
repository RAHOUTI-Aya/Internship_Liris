Introduction
======================================

Overview of Textra Tender
---------------------------
**Textra Tender** is an evolution of the previous version **(Textra)**. In this project, we aim to develop a document processing AI tool designed to extract and structure data from various types of tender documents. By leveraging Optical Character Recognition (OCR) and Large Language Models (LLMs), Textra Tender automates the extraction of critical information, improving efficiency and accuracy in tender management by helping to facilitate the task of tender evaluation.



Pipeline Overview
---------------------------

Textra Tender follows a modular, automated pipeline that integrates OCR, AI-based extraction, and categorization. The complete pipeline is visualized below:

.. figure:: ../Images/pipeline.png
   :width: 100%
   :align: center
   :alt: pipeline
   :name: pipeline


This pipeline illustrates the end-to-end workflow, starting from raw document input to structured and categorized output.


Platform Architecture
---------------------------

To support scalability and user interaction, the Textra Tender platform is built on a robust architecture. It outlines the major components of the user interface, backend processing, and interaction between OCR and LLM modules.

.. figure:: ../Images/psedo_pipeline.png
   :width: 100%
   :align: center
   :alt: psedo_pipeline
   :name: psedo_pipeline



Key Features
---------------------------

Textra Tender includes the following key features:

  - **Multi-format Document Support:** Processing PDFs (both digital and scanned), HTML, and images.

  - **OCR Integration:** Using OCR techniques for accurate text extraction from scanned documents.

  - **AI-Powered Data Structuring:** Utilizing LLMs for intelligent data organization and extraction.

  - **Automated Processing Pipeline:** Integrating OCR and LLMs to extract, structure, and present information in a usable format.

  - **Configurable Workflows:** Allowing customization of processing parameters to suit specific business needs.

  - **Scalability & Performance:** Optimizing for handling large volumes of documents efficiently.

  - **Data Security & Privacy:** Ensuring sensitive document processing remains secure and private.

Input
---------------------------

The process starts with one or multiple documents (images or PDF files), which can be either client tenders or supplier bids.

**Clarification:**

- **Tenders** usually refer to formal procurement processes where companies invite suppliers to submit proposals for a project or contract.
- **Bids** are the offers submitted by suppliers in response to a tender.

Information Extraction
---------------------------

Textra Tender extracts key elements from tender documents (both client and supplier tenders) to facilitate further analysis and decision-making. The extracted fields include:

- Tender reference number
- Submission deadline
- Total budget or estimated cost
- Currency used
- Tender issuer details (name, email, phone, address, etc.)
- Supplier details (for supplier bids)
- Project description and requirements

Modular approach (categorization)
---------------------------

Categorization in Textra Tender is a key step that organizes extracted information based on relevant fields. Since tenders from different clients or suppliers may require multiple fields for proper classification, the system ensures that each tender is assigned to the appropriate category based on its content.

 **Textra Tender categorizes tenders using a field-based approach** , where key extracted fields influence the classification. The main categorization fields include:

- Industry sector (Construction, IT, Healthcare, Energy, etc.)
- Tender type (Goods supply, Services, Consultancy, Turnkey project, etc.)
- Contract type (Fixed-price, Time and materials, Framework agreement, etc.)
- Budget range (Small, Medium, Large-scale projects)
- Geographic scope (Local, National, International)
- Evaluation criteria (Lowest price, Best technical offer, Combination of both)

Since some tenders require multiple classification fields, Textra Tender dynamically adjusts categorization based on the extracted data, ensuring a flexible and accurate organization of tenders.
