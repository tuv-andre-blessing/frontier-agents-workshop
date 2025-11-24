# Scenarios

## Project setup



## Technical foundation

- Code is written in Python
- MCP Server

## Hello world agent with Agent framework

Feature: Ask questions via a Hello World Agent using Agent Framework and MCP

  As a developer using the Agent Framework
  I want a simple "Hello World" agent that can ask questions
  So that I can retrieve answers from a connected MCP server as a data source

  Background:
    Given an MCP server is running and reachable
    And the MCP server exposes a "knowledge-base" tool for answering questions
    And an Agent Framework-based "Hello World Agent" is configured
    And the agent is connected to the MCP server as a tool provider

  Scenario: Ask a simple question and get an answer from the MCP server
    When I send the message "Hello, what is the capital of France?" to the agent
    Then the agent should call the MCP "knowledge-base" tool with the question text
    And the MCP server should return an answer containing "Paris"
    And the agent should respond to me with the answer from the MCP server
    And the agent response should clearly indicate the answer source is the MCP server

  Scenario: Handle unknown questions gracefully
    When I ask the agent "Tell me about an unknown concept X123"
    And the MCP "knowledge-base" tool returns no results
    Then the agent should respond that it cannot find an answer
    And the response should suggest I try rephrasing or another question

  Scenario: Log MCP interaction for observability
    When I ask the agent "Hello, what is 2 + 2?"
    Then the agent should call the MCP "knowledge-base" tool with the question text
    And the agent should log the tool call and the returned answer
    And the agent should respond "4" (or equivalent) to the user