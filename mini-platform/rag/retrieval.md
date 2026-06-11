# RAG Retrieval Plan

## Purpose

This file explains how the AI Docs Agent will find relevant official documentation before answering a question.

## Simple Explanation

Retrieval means finding the right page in the official documentation before answering.

## Flow

```text
User Question
→ Search related official docs
→ Select relevant document chunks
→ Generate beginner-friendly answer
→ Include source references
```

## Example

Question:

```text
Docker Image와 Container는 뭐가 달라?
```

Retrieval should find Docker documentation about images and containers before generating the final answer.

## Mini Platform Connection

Retrieval helps the agent answer accurately instead of guessing.
