<!-- markdownlint-disable-file MD024 -->
# Changelog

## 0.9.0

### Features - In Progress

## 0.8.7

### Features

- Files, links, and existing attachments are attachable to discussion replies within a discussion post thread
- Content for discusion posts and replies support new lines for multiline content
- Soft delete support for posts that have threads. A deleted post placeholder rendered when a post with a thread is
  deleted.  The deleted post author, content, and attachments are deleted.

## 0.8.6

### Bugs

- Catching HTTP Error exceptions from the Python requests module during annotation; Uncaught HTTPError exceptions
  cause the annotation background task in FastAPI to crash without completing annotations in the queue.

## 0.8.5

### Features

- Discussion Post Threads - Users can collaborate by replying to existing discussion posts in a discussion thread in
  order to capture insights and have relevant conversations with other experts to make more robust decisions on an
  analysis in Rosalution. Also includes support to edit and delete replies a user has authored.
- Caching calls to HTTP datasources configured as a dataset, and forge annotation tasks can be enabled to read value
  from the cached call dataset.
- Caching versions in-memory temporarily when processing annotations.  A version is cached used its datasource &
  versioning type.
- Consolidating user experience for Attachments by renaming "Supporting Evidence" to "Attachments" application wide.

### Bugs

- Action menu on an analysis' landing page renders as expected when navigating using the 'backwards navigation'
  button in a browser.
- Titles of attachments on discussions now use elipses when the attachment titles are too long to fit on the row.
  Full attachment name is visible by hovering over the attachment with a mouse.

### Chores

- Updated Python Backend to not use `datetime.utcnow()` which is being deprecated.
- Revised invalid HTML DOM that mixed `<table>` HTML DOM elements within `<div>`s and `<span>`s.
- Upgrading jq Python module to 1.8.0 to be to support building the backend for Python 3.13+.
- Consolidated administrative script for adding users to a Rosalution deployment.

## 0.8.4

### Features

- Discussion Attachments
- Application and VueJS Dataset Component's CSS maintenance and consolidation to resolve rendering layout challenges
  to support upcoming new annotations to visualize.
- Upgraded to FastAPI from 0.110.1 to 0.115.11 to resolve issue that existed until 0.113.0 in FastAPI.
  [Optional Multiple File Uploads Broken When Using Pydantic v2.3.0 #10280](https://github.com/fastapi/fastapi/discussions/10280)
- Upgraded `python-multipart` package in backend dependencies from version 0.0.18 to version 0.0.20 to take
  advantage of FastAPI's type annotations for improved `python-multipart`.
- New Annotation Task Type, SubprocessAnnotationTask which executes a CLI process to access annotations. Applied
  to running `tabix` cli tool to fetch DITTO scores from CGDS's public LTS, UAB's long term storage available
  via an S3 interface.

### Bugs

- Analyses landing page feed adheres to the CSS grid that structures the application visually. Including the footer,
and card feed representing each analysis.  CSS and HTML DOM streamlined.

## 0.8.3

### Features

- Rendering layout for annotations of genes and variants are configurable without code update.

## 0.8.2

### Features

- New annotation linkouts for COSMIC, and gnomAD4 Variant, and annotations for REVEL and AlphaMissense.  New data source
using OpenCravat. VCF string provided by Ensembl's API is cached in the MongoDB database.
- Updated a row to render datasets horizontal if the associated class is included in the rendering configuration.
Variant annotations were rendering vertically and it was taking too much space.
- Added support for attaching genbank (.gb) files for supporting evidence attachments

### Development

- Minimum NodeJS version increased to v23.4 to support upgrading package dependencies to avoid reported vulnerabilities
- ESlint upgrade to 9 and migrating configuration to flat file config

### Bugs

- Backend starts takes over the shell process allowing it to receive SIGTERM for graceful shutdown

## 0.8.1

### Features

- Composition API Migration for moving towards real-time collaboration
- New annotation linkouts for COSMIC, and gnomAD4 Variant, and annotations for REVEL and AlphaMissense.  New data source
using OpenCravat. VCF string provided by Ensembl's API is cached in the MongoDB database.
- Updated a row to render datasets horizontal if the associated class is included in the rendering configuration.
Variant annotations were rendering vertically and it was taking too much space.
- Analyses have a version manifest of annotation's dataset, source, and version
- Increased VueJS version to 3.5.12 to use TemplateRef as a feature

### Bugs

- Fixed developer API endpoint so that existing analyses can queue their annotations to be rendered again if desired.\

## 0.8.0

### Features

- Support for attaching documents, URLs, and Images to fields on an Analysis landing page.
- HTTPs by default for deployments
- Versioning for Annotations as dictated by configuration
- Analyses have a version manifest of annotation's dataset, source, and version
- Render's annotations for an analysis according to it's version manifest
- Timestamped discussions for analyses to which allow users to create, update, and remove text-based
  messages to each other within an analysis.

### Bugs

- Fixed developer API endpoint so that existing analyses can queue their annotations to be rendered again if desired.

## 0.7.0

### Features

- Support for attaching documents, URLs, and Images to fields on an Analysis landing page.
- HTTPs by default for deployments
- Versioning for Annotations as dictated by configuration
- Analyses have a version manifest of annotation's dataset, source, and version
- Render's annotations for an analysis according to it's version manifest
- Timestamped discussions for analyses to which allow users to create, update, and remove text-based
  messages to each other within an analysis.

## 0.6.0

### Features

- Importing cases for analysis, with support of automated configured annotations of genomic units with support at
  curating evidence for analysis review.
- Attachment of supporting evidence as files or URLs
- Support for researchers entering case relevant information to be disseminated to research team
- Multi image attachment for curated figures for analyses
- Attachment of visual annotations associated with genomic units
- Viewing annotations for the genomic units in a case for analysis
- CAS user login, enabling organizations to connect to their Center Authentication Service for user credentials
- Filtering available analyses by data presented on analysis cards in the analysis feed
- Workflows to change analyses from being in preparation to ready, active, approved, declined, on-hold
- 3rd party attachments to link Monday.com and Phenotips to the specific analysis
