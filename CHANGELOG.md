<!-- markdownlint-disable-file MD024 -->
# Changelog

## 0.8.1

### Features

- Composition API Migration for moving towards real-time collaboration
- New annotation linkouts for COSMIC, and gnomAD4 Variant, and annotations for REVEL and AlphaMissense.  New data source
using OpenCravat. VCF string provided by Ensembl's API is cached in the MongoDB database.
- Updated a row to render datasets horizontal if the associated class is included in the rendering configuration.
Variant annotations were rendering vertically and it was taking too much space.
- Analyses have a version manifest of annotation's dataset, source, and version
- Increased VueJS version to 3.5.12 to use TemplateRef as a feature

### Development

- Minimum NodeJS version increased to v23.4 to support upgrading package dependencies to avoid reported vulnerabilities
- ESlint upgrade to 9 and migrating configuration to flat file config

### Bugs

- Fixed developer API endpoint so that existing analyses can queue their annotations to be rendered again if desired.
- Backend starts takes over the shell process allowing it to receive SIGTERM for graceful shutdown

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
