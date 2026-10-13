# Company

> Team-owned document. Replace all placeholders during Session 1.

## Name

Eventai

## Mission

To improve the world through software

## Team members

- Francisco
- Caitlin
- Daniil
- Rafael

## Working rules

Technical decisions are made by discussing options within our team, ensuring that anyone with relevant experience is consulted. If an agent has a technical decision to make, the suggested course of action must be approved by the accountable human. Any code made by an agent must pass all tests before a pull request is made and then this pull request must be approved by a human.

Human approval is mandatory for areas which may have security concerns, which concern the future of the company or which include any sensitive data. More specifically, any push to main must be reviewed and approved by a human. Any changes to the database schema also needs reviewing and approval from the accountable human for that role. If an agent needs more permissions or a new tool, this must be given by a human.

Agents may only create artifacts in their designated branch (or in the logging system). They can only merge into main by creating a pull request. 

If an incident is caused by an agent encountering errors, the agent will inform the accountable human, who can then escalate to the rest of the team if needed. If we notice an incident, we will inform the rest of the team. We will have a log system in place that we will review.

Cost overruns will be prevented by agents aborting their task and informing their accountable human if they go over 90% of their budget. If an overrun does happend, the agent will immediately be aborted. We will then conduct a review of what went wrong, and why the cost observability engineer did not notice this.

## Required Decisions

The first role to receive technical support from an agent will be the software architect.

The project manager and customer lead roles will deliberately remain human initially as it is important that customers interact with humans that have a full understanding of the context.

A human approval gate is important for merging into main and any changes to the database schema, as well as any important decisions the agents make.