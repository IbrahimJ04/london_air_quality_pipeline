# London Air Quality Pipeline

## What I built and who for

**Status: In development**

This project aims to build an incremental data pipeline using the London Air Quality Network (LAQN) API.

The proposed audience is London local authority transport and environmental teams.

The initial project idea is to investigate nitrogen dioxide (NO₂) measurements at selected roadside and urban-background monitoring sites, focusing on rush-hour patterns and the completeness of monitoring data.

The proposed output includes a geographical monitoring-site map, hourly comparisons and data-quality summaries.

The final scope will be confirmed after exploring the API and checking data availability.


## About Me

I am a First Class Mathematics with Computer Science graduate with a strong interest in data, programming and problem solving. Python is the language I am most confident using, and I have been developing my experience with APIs, SQL and data pipelines through practical projects such as this one.

I am interested in The Information Lab's programme because it would allow me to develop my technical skills further while also gaining experience in consultancy. I like the idea of working with different clients, understanding their requirements and helping to turn data into useful solutions. The combination of structured training, practical project work and working collaboratively with others is particularly appealing to me.

## The data

**Source:** London Air Quality Network (LAQN), Environmental Research Group, Imperial College London.

- API reference: https://api.erg.ic.ac.uk/AirQuality/help
- API documentation: https://api.erg.ic.ac.uk/AirQuality/Information/Documentation/pdf
- Network website: https://www.londonair.org.uk

The project will explore monitoring-site information, pollutant details and historical air-quality measurements.

The selected sites, measurement fields, dates, units and data-quality considerations will be documented after investigating the API.

## How it works

The planned pipeline will:

1. Retrieve relevant information from the LAQN API.
2. Preserve collected source data.
3. Clean and validate the measurements.
4. Store structured historical data.
5. Add new measurements across repeated runs without creating duplicates.
6. Produce useful analytical outputs.

Implementation details and the data model will be documented as development progresses.

## How to run it

Setup instructions and execution commands will be added once the pipeline components have been implemented and tested.

## What I would do next

Potential improvements and extensions will be documented as the project develops.

## Where AI helped

I used ChatGPT mainly as a learning and review tool while working on areas that were new to me, particularly the London Air Quality Network API and the requirements for building an incremental data pipeline.

I used it to explain unfamiliar concepts, discuss possible approaches, and help review the initial project structure and documentation. As I develop the pipeline, I will be responsible for implementing and testing each stage, checking the outputs, investigating any issues, and making the final decisions about the project scope, data model and output.

I intend to keep only suggestions that I understand and can explain, and to avoid unnecessary complexity so that the focus remains on building a reliable, reproducible pipeline.

This section will be updated as the project develops to include specific examples of how AI was used and which technical decisions I made.